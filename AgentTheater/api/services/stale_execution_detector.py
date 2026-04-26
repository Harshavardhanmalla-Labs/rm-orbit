"""Background worker to detect stale executions."""
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import Execution, EventLog
from AgentTheater.events.ledger import EventType


class StaleExecutionDetector:
    """Detect executions stuck in progress state and emit events."""

    # Threshold: execution is stale if in_progress for more than this many days
    STALE_THRESHOLD_DAYS = 7

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def detect_stale_executions(self) -> list[str]:
        """Find stale executions and return their IDs.

        Stale = in_progress for > STALE_THRESHOLD_DAYS without completion or block.
        Returns list of execution IDs.
        """
        threshold_date = datetime.now(timezone.utc) - timedelta(days=self.STALE_THRESHOLD_DAYS)

        # Find executions that are in_progress and started before threshold
        stale_executions = await self.db.execute(
            select(Execution).where(
                (Execution.state == "in_progress") &
                (Execution.started_at.isnot(None)) &
                (Execution.started_at < threshold_date)
            )
        )

        return [str(exe.id) for exe in stale_executions.scalars()]

    async def has_stale_event_been_emitted(self, execution_id: str) -> bool:
        """Check if execution.stale_detected event has already been emitted."""
        from uuid import UUID

        result = await self.db.scalar(
            select(EventLog).where(
                (EventLog.aggregate_id == UUID(execution_id)) &
                (EventLog.event_type == EventType.EXECUTION_STALE_DETECTED)
            )
        )
        return result is not None

    async def run_detection_cycle(self, event_store=None):
        """Run one detection cycle: find stale and emit events.

        Args:
            event_store: EventStore instance to emit events (optional).
                       If provided, emits execution.stale_detected for each stale execution.
        """
        stale_ids = await self.detect_stale_executions()

        emitted_count = 0
        for execution_id in stale_ids:
            # Check if we've already emitted for this execution
            already_emitted = await self.has_stale_event_been_emitted(execution_id)

            if not already_emitted and event_store:
                # Emit event to signal staleness
                from uuid import UUID

                await event_store.record_execution_stale_detected(
                    execution_id=UUID(execution_id),
                    correlation_id=f"stale-detector-{datetime.now(timezone.utc).timestamp()}",
                )
                emitted_count += 1

        return {
            "stale_count": len(stale_ids),
            "events_emitted": emitted_count,
            "execution_ids": stale_ids,
        }
