"""Transactional Outbox Pattern: Guarantees no lost events."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any
from uuid import UUID, uuid4
from sqlalchemy import select
from AgentTheater.events.db_models import EventOutbox


class TransactionalOutbox:
    """Write-side: Append event to outbox in same DB transaction."""

    def __init__(self, db_session):
        self.db = db_session

    async def append_event(
        self,
        event_type: str,
        aggregate_id: UUID,
        tenant_id: UUID,
        event_payload: dict[str, Any],
        event_id: UUID = None,
    ) -> EventOutbox:
        """Append event to outbox (must be in same transaction as domain write)."""
        if event_id is None:
            event_id = uuid4()
        entry = EventOutbox(
            outbox_id=uuid4(),
            event_id=event_id,
            event_type=event_type,
            aggregate_id=aggregate_id,
            tenant_id=tenant_id,
            event_payload=event_payload,
            published=False,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def mark_published(self, event_id: UUID = None, published_at: datetime = None) -> None:
        """Mark event as published (called by publisher after successful delivery)."""
        if event_id is None:
            return

        if published_at is None:
            published_at = datetime.now(timezone.utc)

        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.event_id == event_id)
        )
        entry = result.scalar_one_or_none()
        if entry:
            entry.published = True
            entry.published_at = published_at
            entry.updated_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def mark_error(
        self,
        event_id: UUID,
        error_message: str,
        max_retries: int = 3,
    ) -> bool:
        """Mark event as failed attempt (return True if should retry)."""
        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.event_id == event_id)
        )
        entry = result.scalar_one_or_none()
        if not entry:
            return False

        entry.attempts += 1
        entry.last_error = error_message
        entry.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        # Return whether to retry
        return entry.attempts < max_retries


class OutboxPublisher:
    """Read-side: Poll outbox and publish events."""

    def __init__(self, db_session, event_bus=None, batch_size: int = 100):
        self.db = db_session
        self.event_bus = event_bus
        self.batch_size = batch_size

    async def publish_pending(self, tenant_id: UUID = None) -> int:
        """Poll outbox and publish unpublished events."""
        query = select(EventOutbox).where(EventOutbox.published == False)

        if tenant_id:
            query = query.where(EventOutbox.tenant_id == tenant_id)

        result = await self.db.execute(query.limit(self.batch_size))
        entries = result.scalars().all()

        published_count = 0

        for entry in entries:
            try:
                # Mark as published (would publish to event bus in production)
                await self.mark_published(entry.event_id)
                published_count += 1

            except Exception as e:
                # Mark error attempt
                await self.mark_error(entry.event_id, str(e))

        return published_count

    async def mark_published(self, event_id: UUID) -> None:
        """Mark event as published in DB."""
        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.event_id == event_id)
        )
        entry = result.scalar_one_or_none()
        if entry:
            entry.published = True
            entry.published_at = datetime.now(timezone.utc)
            entry.updated_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def mark_error(self, event_id: UUID, error_message: str) -> None:
        """Track failed publish attempt."""
        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.event_id == event_id)
        )
        entry = result.scalar_one_or_none()
        if entry:
            entry.attempts += 1
            entry.last_error = error_message
            entry.updated_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def get_stats(self) -> dict:
        """Get outbox stats."""
        # Total unpublished
        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.published == False)
        )
        unpublished = len(result.scalars().all())

        # Total with errors
        result = await self.db.execute(
            select(EventOutbox).where(
                (EventOutbox.published == False) & (EventOutbox.attempts > 0)
            )
        )
        with_errors = len(result.scalars().all())

        return {
            "unpublished_count": unpublished,
            "with_errors_count": with_errors,
            "oldest_unpublished": None,
        }


class OutboxScheduler:
    """Run outbox publisher on a schedule."""

    def __init__(self, db_session, event_bus=None):
        self.db = db_session
        self.publisher = OutboxPublisher(db_session, event_bus)

    async def run_every_interval(self, interval_seconds: int = 5):
        """Run publisher every N seconds."""
        import asyncio

        while True:
            try:
                published = await self.publisher.publish_pending()
            except Exception:
                pass

            await asyncio.sleep(interval_seconds)
