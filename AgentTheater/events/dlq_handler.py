"""Dead Letter Queue Handler: Manage failed events for manual review and replay.

Pattern: Events that fail max_retries times move to DLQ.
DLQ stores full failure context (error_message, failure_reason, retry_count).
Manual process reviews DLQ and either:
  - Fixes root cause and replays the event
  - Discards if duplicate/invalid
  - Forwards to external system for investigation
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID
from typing import Optional, List, Dict, Any
from enum import Enum
from sqlalchemy import select
from AgentTheater.events.db_models import DeadLetterQueue, EventOutbox, EventLog


class ResolutionAction(str, Enum):
    """How to resolve a DLQ event."""

    MANUAL_FIX = "manual_fix"
    REPLAYED = "replayed"
    DISCARDED = "discarded"


class DLQHandler:
    """Handle failed events and move to dead letter queue."""

    def __init__(self, db_session):
        self.db = db_session

    async def move_to_dlq(
        self,
        event_id: UUID,
        original_consumer: str,
        error_message: str,
        failure_reason: str = None,
    ) -> DeadLetterQueue:
        """Move failed event to DLQ after max_retries exceeded.

        Args:
            event_id: The failed event
            original_consumer: Which consumer failed processing
            error_message: Exception message (e.g., "ValueError: invalid_state")
            failure_reason: Human-readable reason (e.g., "Decision is in terminal state")

        Returns:
            DLQ record for investigation
        """
        # Get original event from outbox
        result = await self.db.execute(
            select(EventOutbox).where(EventOutbox.event_id == event_id)
        )
        outbox_entry = result.scalar_one_or_none()

        if not outbox_entry:
            raise ValueError(f"Event {event_id} not found in outbox")

        # Create DLQ entry with full context
        dlq_entry = DeadLetterQueue(
            event_id=event_id,
            original_consumer=original_consumer,
            event_type=outbox_entry.event_type,
            aggregate_id=outbox_entry.aggregate_id,
            tenant_id=outbox_entry.tenant_id,
            event_payload=outbox_entry.event_payload,
            error_message=error_message,
            failure_reason=failure_reason,
            retry_count=outbox_entry.attempts,
            max_retries=3,  # Matches OutboxPublisher.mark_error max_retries
            next_retry_at=None,  # Manual review required
            resolved=False,
        )
        self.db.add(dlq_entry)

        # Mark outbox entry as handled (don't retry)
        outbox_entry.published = True
        outbox_entry.published_at = datetime.now(timezone.utc)
        outbox_entry.last_error = f"MOVED_TO_DLQ: {error_message}"

        await self.db.commit()
        return dlq_entry

    async def get_unresolved_dlq(
        self,
        tenant_id: UUID = None,
        limit: int = 50,
    ) -> List[DeadLetterQueue]:
        """Get unresolved DLQ entries for manual review.

        Args:
            tenant_id: Filter by tenant (None = all tenants)
            limit: Max entries to return

        Returns:
            List of unresolved DLQ entries, oldest first
        """
        query = select(DeadLetterQueue).where(DeadLetterQueue.resolved == False)

        if tenant_id:
            query = query.where(DeadLetterQueue.tenant_id == tenant_id)

        query = query.order_by(DeadLetterQueue.created_at).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_dlq_stats(
        self,
        tenant_id: UUID = None,
    ) -> Dict[str, Any]:
        """Get DLQ metrics for dashboard/alerts.

        Returns:
            {
                "total_unresolved": 5,
                "by_event_type": {"decision.outcome_recorded": 2, ...},
                "by_consumer": {"decision-processor": 3, ...},
                "oldest_unresolved_age_seconds": 3600,
                "retry_candidates": 2
            }
        """
        base_query = select(DeadLetterQueue)
        if tenant_id:
            base_query = base_query.where(DeadLetterQueue.tenant_id == tenant_id)

        # Total unresolved
        unresolved_result = await self.db.execute(
            base_query.where(DeadLetterQueue.resolved == False)
        )
        unresolved_entries = unresolved_result.scalars().all()
        total_unresolved = len(unresolved_entries)

        # By event type
        by_event_type = {}
        for entry in unresolved_entries:
            key = entry.event_type
            by_event_type[key] = by_event_type.get(key, 0) + 1

        # By consumer
        by_consumer = {}
        for entry in unresolved_entries:
            key = entry.original_consumer
            by_consumer[key] = by_consumer.get(key, 0) + 1

        # Oldest unresolved
        oldest_age = None
        if unresolved_entries:
            oldest = min(unresolved_entries, key=lambda e: e.created_at)
            oldest_age = int(
                (datetime.now(timezone.utc) - oldest.created_at).total_seconds()
            )

        # Retry candidates (retry_count < max_retries and no next_retry_at scheduled)
        retry_candidates = sum(
            1
            for e in unresolved_entries
            if e.retry_count < e.max_retries and e.next_retry_at is None
        )

        return {
            "total_unresolved": total_unresolved,
            "by_event_type": by_event_type,
            "by_consumer": by_consumer,
            "oldest_unresolved_age_seconds": oldest_age,
            "retry_candidates": retry_candidates,
        }

    async def resolve_dlq_entry(
        self,
        dlq_id: UUID,
        action: ResolutionAction,
        notes: str = None,
    ) -> DeadLetterQueue:
        """Resolve a DLQ entry (manual investigation complete).

        Args:
            dlq_id: DLQ entry to resolve
            action: How it was resolved (MANUAL_FIX, REPLAYED, DISCARDED)
            notes: Human notes about resolution

        Returns:
            Updated DLQ entry
        """
        result = await self.db.execute(
            select(DeadLetterQueue).where(DeadLetterQueue.dlq_id == dlq_id)
        )
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError(f"DLQ entry {dlq_id} not found")

        entry.resolved = True
        entry.resolved_at = datetime.now(timezone.utc)
        entry.resolution_action = action.value

        await self.db.commit()
        return entry

    async def schedule_retry(
        self,
        dlq_id: UUID,
        retry_at: datetime = None,
    ) -> DeadLetterQueue:
        """Schedule a DLQ event for retry.

        Call this after root cause is fixed and event is ready to retry.
        """
        result = await self.db.execute(
            select(DeadLetterQueue).where(DeadLetterQueue.dlq_id == dlq_id)
        )
        entry = result.scalar_one_or_none()

        if not entry:
            raise ValueError(f"DLQ entry {dlq_id} not found")

        if retry_at is None:
            retry_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        entry.next_retry_at = retry_at
        entry.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        return entry


class DLQRetryProcessor:
    """Retry scheduled DLQ events."""

    def __init__(self, db_session, event_bus):
        self.db = db_session
        self.event_bus = event_bus

    async def process_scheduled_retries(self, tenant_id: UUID = None) -> int:
        """Process DLQ entries scheduled for retry.

        Returns count of retried events.
        """
        now = datetime.now(timezone.utc)

        # Find entries ready to retry
        query = select(DeadLetterQueue).where(
            (DeadLetterQueue.resolved == False)
            & (DeadLetterQueue.next_retry_at.isnot(None))
            & (DeadLetterQueue.next_retry_at <= now)
        )

        if tenant_id:
            query = query.where(DeadLetterQueue.tenant_id == tenant_id)

        result = await self.db.execute(query)
        entries = result.scalars().all()

        retried_count = 0

        for entry in entries:
            try:
                # Re-publish event to event bus
                await self.event_bus.publish({
                    "event_id": str(entry.event_id),
                    "event_type": entry.event_type,
                    "aggregate_id": str(entry.aggregate_id),
                    "tenant_id": str(entry.tenant_id),
                    "data": entry.event_payload,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "dlq_retry": True,
                })

                # Clear next_retry_at (goes back to normal publishing flow)
                entry.next_retry_at = None
                entry.retry_count += 1
                entry.updated_at = datetime.now(timezone.utc)
                await self.db.commit()

                retried_count += 1

            except Exception as e:
                # Retry failed again, keep scheduled for next attempt
                entry.last_retry_at = datetime.now(timezone.utc)
                entry.next_retry_at = datetime.now(timezone.utc) + timedelta(
                    minutes=5
                )
                await self.db.commit()

        return retried_count

    async def get_retry_schedule(self, tenant_id: UUID = None) -> List[Dict[str, Any]]:
        """Get upcoming scheduled retries."""
        query = select(DeadLetterQueue).where(
            (DeadLetterQueue.resolved == False)
            & (DeadLetterQueue.next_retry_at.isnot(None))
        )

        if tenant_id:
            query = query.where(DeadLetterQueue.tenant_id == tenant_id)

        query = query.order_by(DeadLetterQueue.next_retry_at)

        result = await self.db.execute(query)
        entries = result.scalars().all()

        return [
            {
                "dlq_id": str(e.dlq_id),
                "event_id": str(e.event_id),
                "event_type": e.event_type,
                "next_retry_at": e.next_retry_at.isoformat(),
                "retry_count": e.retry_count,
                "max_retries": e.max_retries,
            }
            for e in entries
        ]
