"""Event Replay System: Rebuild state from event history.

Pattern: Derive state by replaying events from start.
Useful for:
  - Rebuilding read models (projections)
  - Recovering from data corruption
  - Point-in-time analysis
  - Debugging state machines

Guarantees:
  - Replay is deterministic (same events = same state)
  - Can filter by tenant/aggregate/time range
  - Tracks replay progress (resumable)
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
from sqlalchemy import select
from AgentTheater.events.db_models import EventLog, ConsumerCheckpoint


class ReplayScope(str, Enum):
    """What events to replay."""

    ALL = "all"  # All events
    TENANT = "tenant"  # Single tenant
    AGGREGATE = "aggregate"  # Single decision/aggregate
    TENANT_AND_TYPE = "tenant_and_type"  # Events of specific type in tenant
    TIME_RANGE = "time_range"  # Events within date range


class ReplayStatus(str, Enum):
    """Replay progress tracking."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EventReplayer:
    """Replay events to rebuild state."""

    def __init__(self, db_session):
        self.db = db_session

    async def replay_aggregate(
        self,
        aggregate_id: UUID,
        state_builder: Callable,
        skip_until: int = 0,
    ) -> Dict[str, Any]:
        """Replay all events for a single aggregate.

        Args:
            aggregate_id: Decision ID to replay
            state_builder: Async function(state, event) → updated state
            skip_until: Skip events before this sequence number (resume)

        Returns:
            {
                "aggregate_id": UUID,
                "final_state": {...},
                "events_replayed": count,
                "errors": []
            }
        """
        result = await self.db.execute(
            select(EventLog)
            .where(EventLog.aggregate_id == aggregate_id)
            .where(EventLog.sequence_number >= skip_until)
            .order_by(EventLog.sequence_number)
        )
        events = result.scalars().all()

        state = {}
        errors = []

        for event in events:
            try:
                event_dict = {
                    "event_id": str(event.event_id),
                    "event_type": event.event_type,
                    "aggregate_id": str(event.aggregate_id),
                    "data": event.data,
                    "sequence_number": event.sequence_number,
                    "timestamp": event.timestamp.isoformat(),
                }

                state = await state_builder(state, event_dict)

            except Exception as e:
                errors.append({
                    "sequence_number": event.sequence_number,
                    "event_type": event.event_type,
                    "error": str(e),
                })

        return {
            "aggregate_id": str(aggregate_id),
            "final_state": state,
            "events_replayed": len(events),
            "errors": errors,
        }

    async def replay_tenant(
        self,
        tenant_id: UUID,
        event_handler: Callable,
        event_type: Optional[str] = None,
        batch_size: int = 100,
        skip_until: int = 0,
    ) -> Dict[str, Any]:
        """Replay events for entire tenant (for rebuilding projections).

        Args:
            tenant_id: Tenant to replay
            event_handler: Async function(event) for each event
            event_type: Filter to specific event type (optional)
            batch_size: Process in batches
            skip_until: Resume from sequence number

        Returns:
            {
                "tenant_id": UUID,
                "events_replayed": count,
                "batches_processed": count,
                "errors": []
            }
        """
        query = select(EventLog).where(
            (EventLog.tenant_id == tenant_id)
            & (EventLog.sequence_number >= skip_until)
        )

        if event_type:
            query = query.where(EventLog.event_type == event_type)

        query = query.order_by(EventLog.sequence_number)

        total_replayed = 0
        batches = 0
        errors = []

        while True:
            result = await self.db.execute(query.limit(batch_size))
            events = result.scalars().all()

            if not events:
                break

            for event in events:
                try:
                    event_dict = {
                        "event_id": str(event.event_id),
                        "event_type": event.event_type,
                        "aggregate_id": str(event.aggregate_id),
                        "data": event.data,
                        "sequence_number": event.sequence_number,
                        "timestamp": event.timestamp.isoformat(),
                    }
                    await event_handler(event_dict)
                    total_replayed += 1

                except Exception as e:
                    errors.append({
                        "event_id": str(event.event_id),
                        "event_type": event.event_type,
                        "error": str(e),
                    })

            batches += 1
            skip_until = events[-1].sequence_number + 1

        return {
            "tenant_id": str(tenant_id),
            "events_replayed": total_replayed,
            "batches_processed": batches,
            "errors": errors,
        }

    async def replay_time_range(
        self,
        tenant_id: UUID,
        start_time: datetime,
        end_time: datetime,
        event_handler: Callable,
        event_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Replay events within time range.

        Useful for analyzing events during specific period or
        replaying to a point-in-time.

        Args:
            tenant_id: Tenant to replay
            start_time: Replay events >= this timestamp
            end_time: Replay events <= this timestamp
            event_handler: Async function(event) for each event
            event_type: Filter to specific event type (optional)

        Returns:
            {
                "tenant_id": UUID,
                "start_time": ISO string,
                "end_time": ISO string,
                "events_replayed": count,
                "errors": []
            }
        """
        query = select(EventLog).where(
            (EventLog.tenant_id == tenant_id)
            & (EventLog.timestamp >= start_time)
            & (EventLog.timestamp <= end_time)
        )

        if event_type:
            query = query.where(EventLog.event_type == event_type)

        query = query.order_by(EventLog.timestamp)

        result = await self.db.execute(query)
        events = result.scalars().all()

        total_replayed = 0
        errors = []

        for event in events:
            try:
                event_dict = {
                    "event_id": str(event.event_id),
                    "event_type": event.event_type,
                    "aggregate_id": str(event.aggregate_id),
                    "data": event.data,
                    "sequence_number": event.sequence_number,
                    "timestamp": event.timestamp.isoformat(),
                }
                await event_handler(event_dict)
                total_replayed += 1

            except Exception as e:
                errors.append({
                    "event_id": str(event.event_id),
                    "event_type": event.event_type,
                    "error": str(e),
                })

        return {
            "tenant_id": str(tenant_id),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "events_replayed": total_replayed,
            "errors": errors,
        }


class ProjectionBuilder:
    """Build read models (projections) from events."""

    async def build_decision_projection(
        self,
        db_session,
        decision_id: UUID,
    ) -> Dict[str, Any]:
        """Build complete decision state by replaying events.

        This projection is used by API to return decision details.
        """
        replayer = EventReplayer(db_session)

        # State builder for decision
        async def build_decision_state(state, event):
            event_type = event["event_type"]

            if event_type == "decision.created":
                state = {
                    "id": str(decision_id),
                    "question": event["data"].get("question"),
                    "roles": event["data"].get("roles", []),
                    "created_at": event["timestamp"],
                    "state": "created",
                    "timeline": [],
                }

            elif event_type == "decision.approved":
                state["state"] = "approved"
                state["approved_at"] = event["timestamp"]

            elif event_type == "decision.in_progress":
                state["state"] = "in_progress"
                state["started_at"] = event["timestamp"]

            elif event_type == "decision.outcome_recorded":
                outcome = event["data"].get("outcome")
                state["state"] = outcome  # succeeded/failed/pivoted/abandoned
                state["outcome"] = outcome
                state["note"] = event["data"].get("note")
                state["completed_at"] = event["timestamp"]

            # Track timeline
            if "timeline" in state:
                state["timeline"].append({
                    "event": event_type,
                    "timestamp": event["timestamp"],
                })

            return state

        result = await replayer.replay_aggregate(decision_id, build_decision_state)
        return result["final_state"]

    async def build_tenant_summary(
        self,
        db_session,
        tenant_id: UUID,
    ) -> Dict[str, Any]:
        """Build tenant-wide summary from all events."""
        replayer = EventReplayer(db_session)

        summary = {
            "total_decisions": 0,
            "by_outcome": {},
            "timeline": [],
        }

        async def update_summary(event):
            if event["event_type"] == "decision.created":
                summary["total_decisions"] += 1

            elif event["event_type"] == "decision.outcome_recorded":
                outcome = event["data"].get("outcome", "unknown")
                summary["by_outcome"][outcome] = summary["by_outcome"].get(outcome, 0) + 1

            summary["timeline"].append({
                "event": event["event_type"],
                "timestamp": event["timestamp"],
            })

        await replayer.replay_tenant(
            tenant_id,
            update_summary,
        )

        return summary


class ConsistencyChecker:
    """Verify consistency between events and derived state."""

    @staticmethod
    async def verify_decision_state(
        db_session,
        decision_id: UUID,
        current_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Verify decision state matches what events say it should be.

        Returns:
            {
                "consistent": bool,
                "expected_state": {...},
                "current_state": {...},
                "divergences": [list of mismatches]
            }
        """
        # Rebuild state from events
        builder = ProjectionBuilder()
        expected_state = await builder.build_decision_projection(db_session, decision_id)

        divergences = []

        # Compare key fields
        for field in ["state", "outcome", "question"]:
            expected = expected_state.get(field)
            current = current_state.get(field)

            if expected != current:
                divergences.append({
                    "field": field,
                    "expected": expected,
                    "current": current,
                })

        return {
            "consistent": len(divergences) == 0,
            "expected_state": expected_state,
            "current_state": current_state,
            "divergences": divergences,
        }
