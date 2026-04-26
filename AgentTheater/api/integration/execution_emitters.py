"""Emitters for System 4: Decision Execution & Outcome Tracker."""
from uuid import UUID
from typing import Optional, Dict, Any
from AgentTheater.events import EventStore
from AgentTheater.events.security import EventSecurityContext


class ExecutionEmitters:
    """Emit events for execution lifecycle."""

    def __init__(self, event_store: EventStore):
        self.store = event_store

    async def emit_execution_created(
        self,
        execution_id: UUID,
        decision_id: UUID,
        security_context: EventSecurityContext,
        correlation_id: str = None,
        predicted_outcome: str = None,
    ):
        """Emit execution.created event."""
        await self.store.record_execution_created(
            execution_id=execution_id,
            decision_id=decision_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            predicted_outcome=predicted_outcome,
            correlation_id=correlation_id,
        )

    async def emit_artifact_linked(
        self,
        execution_id: UUID,
        artifact_type: str,
        artifact_id: str,
        security_context: EventSecurityContext,
        correlation_id: str = None,
        artifact_url: str = None,
    ):
        """Emit artifact.linked event."""
        await self.store.record_artifact_linked(
            execution_id=execution_id,
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            artifact_url=artifact_url,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )

    async def emit_execution_state_transition(
        self,
        execution_id: UUID,
        from_state: str,
        to_state: str,
        security_context: EventSecurityContext,
        correlation_id: str = None,
        reason: str = None,
        blocked_reason: str = None,
    ):
        """Emit execution state transition event based on target state."""
        await self.store.record_execution_state_transitioned(
            execution_id=execution_id,
            from_state=from_state,
            to_state=to_state,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            reason=reason,
            blocked_reason=blocked_reason,
            correlation_id=correlation_id,
        )

    async def emit_outcome_recorded(
        self,
        execution_id: UUID,
        actual_outcome: str,
        security_context: EventSecurityContext,
        correlation_id: str = None,
        success_metrics: Optional[Dict[str, Any]] = None,
        failure_reason: str = None,
        lessons_learned: str = None,
    ):
        """Emit outcome.recorded event."""
        await self.store.record_outcome_recorded(
            execution_id=execution_id,
            actual_outcome=actual_outcome,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            success_metrics=success_metrics,
            failure_reason=failure_reason,
            lessons_learned=lessons_learned,
            correlation_id=correlation_id,
        )

    async def emit_outcome_validated(
        self,
        execution_id: UUID,
        security_context: EventSecurityContext,
        correlation_id: str = None,
    ):
        """Emit outcome.validated event."""
        await self.store.record_outcome_validated(
            execution_id=execution_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )
