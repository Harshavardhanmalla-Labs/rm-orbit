"""Event Ledger and Store for System 2."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4
from typing import Any, Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from AgentTheater.events.db_models import EventLog, EventOutbox, AggregateSequence
from AgentTheater.events.outbox import TransactionalOutbox


class EventType(str, Enum):
    """Event types for AgentTheatre."""

    # System 1 & 2
    DECISION_CREATED = "decision.created"
    DECISION_UPDATED = "decision.updated"
    DECISION_OUTCOME_RECORDED = "decision.outcome_recorded"
    GITHUB_ISSUE_ADDED = "github_issue.added"
    GITHUB_ISSUES_CREATED = "github_issues.created"

    # System 3: Decision Accountability Engine
    DECISION_VERSION_CREATED = "decision.version_created"
    DECISION_RATIONALE_ADDED = "decision.rationale_added"
    DECISION_CONFIDENCE_SCORED = "decision.confidence_scored"
    DECISION_RISK_ASSESSED = "decision.risk_assessed"
    DECISION_STATE_TRANSITIONED = "decision.state_transitioned"

    # System 4: Decision Execution & Outcome Tracker
    EXECUTION_CREATED = "execution.created"
    EXECUTION_ASSIGNED = "execution.assigned"
    EXECUTION_STARTED = "execution.started"
    EXECUTION_BLOCKED = "execution.blocked"
    EXECUTION_COMPLETED = "execution.completed"
    OUTCOME_RECORDED = "outcome.recorded"
    OUTCOME_VALIDATED = "outcome.validated"
    ARTIFACT_LINKED = "artifact.linked"
    EXECUTION_STALE_DETECTED = "execution.stale_detected"
    ARTIFACT_SYNC_RETRIED = "artifact.sync_retried"


@dataclass
class DomainEvent:
    """Represents an immutable domain event."""

    event_id: Optional[UUID] = None
    event_type: str = None
    aggregate_id: UUID = None
    aggregate_type: str = None
    tenant_id: UUID = None
    operator_id: Optional[UUID] = None
    data: dict[str, Any] = None
    meta: Optional[dict[str, Any]] = None
    version: int = 1
    schema_version: str = "v1"
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    sequence_number: Optional[int] = None

    def __post_init__(self):
        if self.event_id is None:
            self.event_id = uuid4()
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if self.data is None:
            self.data = {}
        if self.correlation_id is None:
            self.correlation_id = str(uuid4())


class EventLedger:
    """Immutable append-only event log."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.pending_events: List[DomainEvent] = []

    async def _next_sequence(self, aggregate_id: UUID) -> int:
        """Return the next sequence number for aggregate, atomically incrementing the counter.

        Uses SELECT … FOR UPDATE (PostgreSQL) or relies on SQLite WAL serialization to
        guarantee no duplicate sequence numbers under concurrent writers.
        """
        seq_row = await self.db.scalar(
            select(AggregateSequence)
            .where(AggregateSequence.aggregate_id == aggregate_id)
            .with_for_update()
        )
        if seq_row is None:
            seq_row = AggregateSequence(aggregate_id=aggregate_id, next_sequence=1)
            self.db.add(seq_row)
            await self.db.flush()
            return 0

        current = seq_row.next_sequence
        seq_row.next_sequence = current + 1
        seq_row.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return current

    async def append(self, event: DomainEvent) -> DomainEvent:
        """Append event to ledger.

        Must be called within transaction context.
        """
        sequence_number = await self._next_sequence(event.aggregate_id)
        event.sequence_number = sequence_number

        # Create event log entry
        event_log = EventLog(
            event_id=event.event_id,
            event_type=event.event_type,
            aggregate_id=event.aggregate_id,
            aggregate_type=event.aggregate_type,
            sequence_number=sequence_number,
            tenant_id=event.tenant_id,
            operator_id=event.operator_id,
            data=event.data,
            meta=event.meta,
            version=event.version,
            schema_version=event.schema_version,
            correlation_id=event.correlation_id,
            request_id=event.request_id,
            timestamp=event.timestamp,
        )

        self.db.add(event_log)
        self.pending_events.append(event)

        return event

    async def get_aggregate_events(self, aggregate_id: UUID) -> List[EventLog]:
        """Get all events for an aggregate."""
        result = await self.db.execute(
            select(EventLog)
            .where(EventLog.aggregate_id == aggregate_id)
            .order_by(EventLog.sequence_number)
        )
        return result.scalars().all()

    async def get_events_for_tenant(self, tenant_id: UUID) -> List[EventLog]:
        """Get all events for a tenant."""
        result = await self.db.execute(
            select(EventLog)
            .where(EventLog.tenant_id == tenant_id)
            .order_by(EventLog.timestamp)
        )
        return result.scalars().all()

    async def get_pending_events(self) -> List[DomainEvent]:
        """Get events pending publication."""
        return self.pending_events

    async def commit(self):
        """Publish pending events (called after transaction commits)."""
        self.pending_events = []


class EventStore:
    """High-level domain operations with events."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.ledger = EventLedger(db_session)
        self.outbox = TransactionalOutbox(db_session)
        self.pending_events: List[DomainEvent] = []

    async def append(self, event: DomainEvent) -> DomainEvent:
        """Append event to ledger."""
        return await self.ledger.append(event)

    async def record_decision_created(
        self,
        decision_id: UUID,
        project_id: UUID,
        tenant_id: UUID,
        operator_id: UUID,
        question: str,
        roles: List[str],
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision created event."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_CREATED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "project_id": str(project_id),
                "question": question,
                "roles": roles,
            }
        )

        # Append to ledger
        await self.ledger.append(event)

        # Append to outbox with same event_id
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )

        return event

    async def record_decision_outcome(
        self,
        decision_id: UUID,
        tenant_id: UUID,
        operator_id: UUID,
        outcome: str,
        note: Optional[str] = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision outcome event."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_OUTCOME_RECORDED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "outcome": outcome,
                "note": note,
            }
        )

        # Append to ledger
        await self.ledger.append(event)

        # Append to outbox with same event_id
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )

        return event

    async def record_decision_version_created(
        self,
        decision_id: UUID,
        version: int,
        tenant_id: UUID,
        operator_id: UUID,
        question: str,
        state: str,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision version created event (System 3)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_VERSION_CREATED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "version": version,
                "question": question,
                "state": state,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_decision_rationale_added(
        self,
        decision_id: UUID,
        role: str,
        reasoning: str,
        tenant_id: UUID,
        operator_id: UUID,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision rationale added event (System 3)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_RATIONALE_ADDED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "role": role,
                "reasoning": reasoning,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_decision_confidence_scored(
        self,
        decision_id: UUID,
        technical: float,
        market: float,
        team: float,
        overall: float,
        tenant_id: UUID,
        operator_id: UUID,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision confidence scored event (System 3)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_CONFIDENCE_SCORED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "technical_confidence": technical,
                "market_confidence": market,
                "team_confidence": team,
                "overall_confidence": overall,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_decision_risk_assessed(
        self,
        decision_id: UUID,
        technical_risk: float,
        market_risk: float,
        financial_risk: float,
        team_risk: float,
        overall_risk: float,
        tenant_id: UUID,
        operator_id: UUID,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision risk assessed event (System 3)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_RISK_ASSESSED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "technical_risk": technical_risk,
                "market_risk": market_risk,
                "financial_risk": financial_risk,
                "team_risk": team_risk,
                "overall_risk": overall_risk,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_decision_state_transitioned(
        self,
        decision_id: UUID,
        from_state: str,
        to_state: str,
        tenant_id: UUID,
        operator_id: UUID,
        reason: str = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record decision state transitioned event (System 3)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.DECISION_STATE_TRANSITIONED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "from_state": from_state,
                "to_state": to_state,
                "reason": reason,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=decision_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_execution_created(
        self,
        execution_id: UUID,
        decision_id: UUID,
        tenant_id: UUID,
        operator_id: UUID,
        predicted_outcome: str = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record execution created event (System 4)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.EXECUTION_CREATED,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "decision_id": str(decision_id),
                "predicted_outcome": predicted_outcome,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=execution_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_artifact_linked(
        self,
        execution_id: UUID,
        artifact_type: str,
        artifact_id: str,
        artifact_url: str = None,
        tenant_id: UUID = None,
        operator_id: UUID = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record artifact linked event (System 4)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.ARTIFACT_LINKED,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "artifact_type": artifact_type,
                "artifact_id": artifact_id,
                "artifact_url": artifact_url,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=execution_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    _STATE_TO_EVENT = {
        "in_progress": EventType.EXECUTION_STARTED,
        "blocked": EventType.EXECUTION_BLOCKED,
        "completed": EventType.EXECUTION_COMPLETED,
        "assigned": EventType.EXECUTION_ASSIGNED,
        "succeeded": EventType.EXECUTION_COMPLETED,
        "failed": EventType.EXECUTION_COMPLETED,
        "pivoted": EventType.EXECUTION_COMPLETED,
        "abandoned": EventType.EXECUTION_COMPLETED,
        "approved": EventType.EXECUTION_CREATED,
    }

    async def record_execution_state_transitioned(
        self,
        execution_id: UUID,
        from_state: str,
        to_state: str,
        tenant_id: UUID,
        operator_id: UUID,
        reason: str = None,
        blocked_reason: str = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record execution state transitioned event (System 4)."""
        event_type = self._STATE_TO_EVENT.get(to_state, EventType.EXECUTION_CREATED)
        event = DomainEvent(
            event_id=uuid4(),
            event_type=event_type,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "from_state": from_state,
                "to_state": to_state,
                "reason": reason,
                "blocked_reason": blocked_reason,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=execution_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_outcome_recorded(
        self,
        execution_id: UUID,
        actual_outcome: str,
        tenant_id: UUID,
        operator_id: UUID,
        success_metrics: dict = None,
        failure_reason: str = None,
        lessons_learned: str = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record outcome recorded event (System 4)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.OUTCOME_RECORDED,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "actual_outcome": actual_outcome,
                "success_metrics": success_metrics,
                "failure_reason": failure_reason,
                "lessons_learned": lessons_learned,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=execution_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_outcome_validated(
        self,
        execution_id: UUID,
        tenant_id: UUID,
        operator_id: UUID,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record outcome validated event (System 4)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.OUTCOME_VALIDATED,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={}
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=execution_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def record_execution_stale_detected(
        self,
        execution_id: UUID,
        tenant_id: UUID = None,
        operator_id: UUID = None,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record execution stale detected event (background worker)."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.EXECUTION_STALE_DETECTED,
            aggregate_id=execution_id,
            aggregate_type="Execution",
            tenant_id=tenant_id,
            operator_id=operator_id,
            correlation_id=correlation_id or str(uuid4()),
            data={"detected_at": datetime.now(timezone.utc).isoformat()}
        )
        await self.ledger.append(event)
        if tenant_id:
            await self.outbox.append_event(
                event_type=event.event_type,
                aggregate_id=execution_id,
                tenant_id=tenant_id,
                event_payload=event.data,
                event_id=event.event_id,
            )
        return event

    async def record_artifact_sync_retried(
        self,
        artifact_id: UUID,
        execution_id: UUID,
        tenant_id: UUID,
        retry_count: int,
        correlation_id: str = None,
    ) -> DomainEvent:
        """Record artifact sync retry event."""
        event = DomainEvent(
            event_id=uuid4(),
            event_type=EventType.ARTIFACT_SYNC_RETRIED,
            aggregate_id=artifact_id,
            aggregate_type="ExecutionArtifact",
            tenant_id=tenant_id,
            correlation_id=correlation_id or str(uuid4()),
            data={
                "execution_id": str(execution_id),
                "retry_count": retry_count,
            }
        )
        await self.ledger.append(event)
        await self.outbox.append_event(
            event_type=event.event_type,
            aggregate_id=artifact_id,
            tenant_id=tenant_id,
            event_payload=event.data,
            event_id=event.event_id,
        )
        return event

    async def commit(self):
        """Clear in-memory pending list after DB transaction commits.

        Actual delivery is handled by the OutboxRelay background worker,
        which polls event_outbox and marks entries published atomically.
        """
        await self.ledger.commit()
