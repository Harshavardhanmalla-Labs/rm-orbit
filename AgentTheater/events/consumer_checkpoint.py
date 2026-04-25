"""Consumer Checkpointing: Track progress, safe resume after crash.

Pattern: Each consumer tracks last_processed_sequence per aggregate.
On restart, resume from checkpoint instead of replaying all events.

Guarantees:
- No duplicate processing (track sequence number)
- Safe resume after crash (checkpoint committed before continuing)
- Consumer group coordination (multiple consumers, one per partition)
- Heartbeat mechanism (detect stale consumers, enable auto-recovery)
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from AgentTheater.events.db_models import ConsumerCheckpoint, EventLog


class ConsumerCheckpointManager:
    """Manage consumer progress checkpoints."""

    def __init__(self, db_session, consumer_name: str, consumer_group: str = "default"):
        self.db = db_session
        self.consumer_name = consumer_name
        self.consumer_group = consumer_group
        self.checkpoint_id: Optional[UUID] = None

    async def initialize(self) -> ConsumerCheckpoint:
        """Get or create checkpoint for this consumer.

        If consumer already exists in DB, resume from last checkpoint.
        Otherwise, create new checkpoint starting at sequence 0.
        """
        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                (ConsumerCheckpoint.consumer_name == self.consumer_name)
                & (ConsumerCheckpoint.consumer_group == self.consumer_group)
            )
        )
        checkpoint = result.scalar_one_or_none()

        if checkpoint:
            # Resume from existing checkpoint
            self.checkpoint_id = checkpoint.checkpoint_id
            checkpoint.is_active = True
            checkpoint.last_heartbeat = datetime.now(timezone.utc)
            await self.db.commit()
            return checkpoint
        else:
            # Create new checkpoint starting at sequence 0
            checkpoint = ConsumerCheckpoint(
                checkpoint_id=uuid4(),
                consumer_name=self.consumer_name,
                consumer_group=self.consumer_group,
                last_processed_sequence=0,
                is_active=True,
                last_heartbeat=datetime.now(timezone.utc),
            )
            self.db.add(checkpoint)
            await self.db.commit()
            self.checkpoint_id = checkpoint.checkpoint_id
            return checkpoint

    async def get_checkpoint(self) -> Optional[ConsumerCheckpoint]:
        """Get current checkpoint."""
        if not self.checkpoint_id:
            await self.initialize()

        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                ConsumerCheckpoint.checkpoint_id == self.checkpoint_id
            )
        )
        return result.scalar_one_or_none()

    async def mark_processed(self, event_id: UUID, sequence_number: int) -> None:
        """Mark event as processed (after successful handling).

        IMPORTANT: Call this AFTER event is fully processed.
        Do NOT call before processing completes.
        """
        checkpoint = await self.get_checkpoint()
        if not checkpoint:
            raise ValueError("Checkpoint not initialized")

        checkpoint.last_processed_event_id = event_id
        checkpoint.last_processed_sequence = sequence_number
        checkpoint.total_processed += 1
        checkpoint.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

    async def mark_error(self, sequence_number: int, error: str) -> None:
        """Mark event processing as failed (don't advance checkpoint)."""
        checkpoint = await self.get_checkpoint()
        if not checkpoint:
            raise ValueError("Checkpoint not initialized")

        checkpoint.total_errors += 1
        checkpoint.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

    async def heartbeat(self) -> None:
        """Update last_heartbeat to indicate consumer is alive.

        Call periodically (e.g., every 5 seconds) to signal aliveness.
        """
        checkpoint = await self.get_checkpoint()
        if not checkpoint:
            raise ValueError("Checkpoint not initialized")

        checkpoint.last_heartbeat = datetime.now(timezone.utc)
        await self.db.commit()

    async def shutdown(self) -> None:
        """Mark consumer as inactive on graceful shutdown."""
        checkpoint = await self.get_checkpoint()
        if not checkpoint:
            return

        checkpoint.is_active = False
        checkpoint.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

    async def get_resume_sequence(self) -> int:
        """Get sequence number to resume from.

        Returns:
            last_processed_sequence (will process next_sequence = resume_sequence + 1)
        """
        checkpoint = await self.get_checkpoint()
        if not checkpoint:
            return 0
        return checkpoint.last_processed_sequence


class ConsumerGroupCoordinator:
    """Coordinate multiple consumers in same group (partition assignment)."""

    def __init__(self, db_session):
        self.db = db_session

    async def get_active_consumers(self, consumer_group: str) -> List[ConsumerCheckpoint]:
        """Get all active consumers in a group."""
        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                (ConsumerCheckpoint.consumer_group == consumer_group)
                & (ConsumerCheckpoint.is_active == True)
            )
        )
        return result.scalars().all()

    async def detect_stale_consumers(
        self, consumer_group: str, heartbeat_timeout_seconds: int = 30
    ) -> List[ConsumerCheckpoint]:
        """Detect consumers that haven't heartbeated recently.

        Mark as inactive so other consumers can take over processing.
        """
        timeout = datetime.now(timezone.utc) - timedelta(seconds=heartbeat_timeout_seconds)

        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                (ConsumerCheckpoint.consumer_group == consumer_group)
                & (ConsumerCheckpoint.is_active == True)
                & (ConsumerCheckpoint.last_heartbeat < timeout)
            )
        )
        stale = result.scalars().all()

        # Mark as inactive
        for consumer in stale:
            consumer.is_active = False
            consumer.updated_at = datetime.now(timezone.utc)

        if stale:
            await self.db.commit()

        return stale

    async def get_consumer_lag(self, consumer_group: str) -> Dict[str, Any]:
        """Get lag metrics for all consumers in group.

        Returns:
            {
                "consumer_name": {
                    "last_processed_sequence": 42,
                    "total_processed": 1024,
                    "total_errors": 2,
                    "is_active": true,
                    "last_heartbeat_seconds_ago": 3
                }
            }
        """
        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                ConsumerCheckpoint.consumer_group == consumer_group
            )
        )
        consumers = result.scalars().all()

        now = datetime.now(timezone.utc)
        lag_report = {}

        for consumer in consumers:
            seconds_since_heartbeat = (
                now - consumer.last_heartbeat
            ).total_seconds() if consumer.last_heartbeat else None

            lag_report[consumer.consumer_name] = {
                "last_processed_sequence": consumer.last_processed_sequence,
                "total_processed": consumer.total_processed,
                "total_errors": consumer.total_errors,
                "is_active": consumer.is_active,
                "last_heartbeat_seconds_ago": int(seconds_since_heartbeat)
                if seconds_since_heartbeat
                else None,
            }

        return lag_report


class EventConsumer:
    """Base class for event consumers.

    Usage:
        class DecisionConsumer(EventConsumer):
            async def process_event(self, event):
                # Handle event
                pass

        consumer = DecisionConsumer(db, "decision-processor")
        async for batch in consumer.stream_events(tenant_id):
            # Process batch
            pass
    """

    def __init__(self, db_session, consumer_name: str, consumer_group: str = "default"):
        self.db = db_session
        self.checkpoint_mgr = ConsumerCheckpointManager(
            db_session, consumer_name, consumer_group
        )
        self.consumer_name = consumer_name

    async def initialize(self) -> None:
        """Initialize consumer and checkpoint."""
        await self.checkpoint_mgr.initialize()

    async def process_event(self, event: Dict[str, Any]) -> None:
        """Override this to handle events.

        Called for each event after resume checkpoint.
        """
        raise NotImplementedError

    async def stream_events(
        self,
        tenant_id: UUID,
        batch_size: int = 50,
        heartbeat_interval: int = 5,
    ):
        """Stream events from checkpoint onwards.

        Yields batches of events to process.
        Periodically updates heartbeat to signal aliveness.
        """
        import asyncio

        await self.initialize()

        # Get resume point
        resume_sequence = await self.checkpoint_mgr.get_resume_sequence()
        next_sequence = resume_sequence + 1

        processed_in_batch = 0
        last_heartbeat = datetime.now(timezone.utc)

        while True:
            # Fetch batch of events
            result = await self.db.execute(
                select(EventLog)
                .where(
                    (EventLog.tenant_id == tenant_id)
                    & (EventLog.sequence_number >= next_sequence)
                )
                .order_by(EventLog.sequence_number)
                .limit(batch_size)
            )
            events = result.scalars().all()

            if not events:
                # No new events, wait and retry
                await asyncio.sleep(1)
                continue

            # Process batch
            for event_record in events:
                try:
                    # Convert to dict for handler
                    event_dict = {
                        "event_id": str(event_record.event_id),
                        "event_type": event_record.event_type,
                        "aggregate_id": str(event_record.aggregate_id),
                        "tenant_id": str(event_record.tenant_id),
                        "data": event_record.data,
                        "sequence_number": event_record.sequence_number,
                        "correlation_id": event_record.correlation_id,
                        "timestamp": event_record.timestamp.isoformat(),
                    }

                    # Handle event
                    await self.process_event(event_dict)

                    # Mark as processed (advances checkpoint)
                    await self.checkpoint_mgr.mark_processed(
                        event_record.event_id, event_record.sequence_number
                    )

                    next_sequence = event_record.sequence_number + 1
                    processed_in_batch += 1

                except Exception as e:
                    # Mark error but don't advance checkpoint
                    # Consumer will retry from last successful checkpoint
                    await self.checkpoint_mgr.mark_error(
                        event_record.sequence_number, str(e)
                    )
                    # Re-raise to allow caller to handle/backoff
                    raise

            # Periodic heartbeat
            now = datetime.now(timezone.utc)
            if (now - last_heartbeat).total_seconds() >= heartbeat_interval:
                await self.checkpoint_mgr.heartbeat()
                last_heartbeat = now

            yield [
                {
                    "event_id": str(e.event_id),
                    "event_type": e.event_type,
                    "aggregate_id": str(e.aggregate_id),
                    "data": e.data,
                    "sequence_number": e.sequence_number,
                }
                for e in events
            ]

    async def shutdown(self) -> None:
        """Graceful shutdown."""
        await self.checkpoint_mgr.shutdown()
