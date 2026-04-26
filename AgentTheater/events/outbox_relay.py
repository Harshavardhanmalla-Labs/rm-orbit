"""Background outbox relay: polls unpublished events and publishes them atomically."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from AgentTheater.events.db_models import EventOutbox

logger = logging.getLogger(__name__)

# Global lock prevents concurrent relay runs (guards against concurrent asyncio tasks)
_relay_lock = asyncio.Lock()

# Heartbeat: updated after every successful relay cycle; read by health checker
_relay_last_run: Optional[datetime] = None
_RELAY_STALE_SECONDS = 30


def get_relay_status() -> dict:
    """Return relay running status for health endpoint."""
    if _relay_last_run is None:
        return {"running": False, "last_run": None, "age_seconds": None}
    age = (datetime.now(timezone.utc) - _relay_last_run).total_seconds()
    return {
        "running": age < _RELAY_STALE_SECONDS,
        "last_run": _relay_last_run.isoformat(),
        "age_seconds": round(age, 1),
    }


class OutboxRelay:
    """Polls event_outbox for unpublished entries and publishes them.

    Each relay cycle runs in its own DB session so it never interferes with
    request-handling sessions. Entries are marked published atomically within a
    single transaction after successful delivery.
    """

    MAX_ATTEMPTS = 5

    def __init__(self, session_factory: async_sessionmaker, batch_size: int = 50):
        self.session_factory = session_factory
        self.batch_size = batch_size

    async def run_once(self) -> int:
        """Publish one batch. Returns number of events published. Skips if already running."""
        global _relay_last_run
        if _relay_lock.locked():
            return 0
        async with _relay_lock:
            try:
                async with self.session_factory() as session:
                    published = await self._publish_batch(session)
                _relay_last_run = datetime.now(timezone.utc)
                return published
            except Exception as e:
                logger.error("outbox_relay_session_error", extra={"error": str(e)})
                return 0

    async def _publish_batch(self, session: AsyncSession) -> int:
        result = await session.execute(
            select(EventOutbox)
            .where(
                EventOutbox.published == False,
                EventOutbox.attempts < self.MAX_ATTEMPTS,
            )
            .order_by(EventOutbox.created_at)
            .limit(self.batch_size)
        )
        entries = result.scalars().all()

        from AgentTheater.observability.metrics import get_metrics
        m = get_metrics()

        published = 0
        for entry in entries:
            try:
                await self._deliver(entry)
                entry.published = True
                entry.published_at = datetime.now(timezone.utc)
                entry.updated_at = datetime.now(timezone.utc)
                m.events_published_total.labels(
                    event_type=entry.event_type, aggregate_type=""
                ).inc()
                published += 1
            except Exception as e:
                entry.attempts += 1
                entry.last_error = str(e)[:500]
                entry.updated_at = datetime.now(timezone.utc)
                m.outbox_publish_failures_total.labels(event_type=entry.event_type).inc()
                logger.warning(
                    "outbox_relay_delivery_failed",
                    extra={
                        "event_id": str(entry.event_id),
                        "event_type": entry.event_type,
                        "attempt": entry.attempts,
                        "error": str(e),
                    },
                )

        if entries:
            await session.commit()

        # Gauge: current unpublished backlog after this batch
        remaining = await session.execute(
            select(EventOutbox).where(EventOutbox.published == False)
        )
        m.outbox_unpublished_count.set(len(remaining.scalars().all()))

        if published:
            logger.info("outbox_relay_published", extra={"count": published})

        return published

    async def _deliver(self, entry: EventOutbox) -> None:
        """Deliver event to the event bus. Currently logs; replace with real broker call."""
        logger.info(
            "outbox_event_dispatched",
            extra={
                "event_id": str(entry.event_id),
                "event_type": entry.event_type,
                "aggregate_id": str(entry.aggregate_id),
                "tenant_id": str(entry.tenant_id),
            },
        )


async def run_outbox_relay(
    session_factory: async_sessionmaker,
    interval_seconds: float = 5.0,
) -> None:
    """Long-running coroutine: run relay every interval_seconds until cancelled."""
    relay = OutboxRelay(session_factory)
    while True:
        try:
            await relay.run_once()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error("outbox_relay_unexpected", extra={"error": str(e)})
        await asyncio.sleep(interval_seconds)
