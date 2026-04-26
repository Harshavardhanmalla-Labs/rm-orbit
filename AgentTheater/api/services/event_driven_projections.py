"""Event-driven projection updates for ExecutionReadModel and DecisionReadModel."""
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import ExecutionReadModel, DecisionReadModel


class ExecutionProjector:
    """Project execution events into denormalized read model."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def project_execution_created(
        self,
        execution_id: UUID,
        decision_id: UUID,
        decision_question: str,
        predicted_outcome: str = None,
        tenant_id: UUID = None,
    ):
        """Create or update read model on execution.created event."""
        # Check if read model already exists
        existing = await self.db.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )

        if not existing:
            read_model = ExecutionReadModel(
                execution_id=execution_id,
                decision_id=decision_id,
                decision_question=decision_question,
                state="approved",
                predicted_outcome=predicted_outcome,
                tenant_id=tenant_id,
            )
            self.db.add(read_model)
            await self.db.flush()

    async def project_artifact_linked(
        self,
        execution_id: UUID,
        artifact_type: str,
    ):
        """Increment artifact count on artifact.linked event."""
        read_model = await self.db.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )

        if read_model:
            if artifact_type == "github_issue":
                read_model.github_issues_count += 1
            elif artifact_type == "github_pr":
                read_model.github_prs_count += 1
            elif artifact_type == "task":
                read_model.tasks_count += 1
            elif artifact_type == "doc":
                read_model.docs_count += 1
            elif artifact_type == "deployment":
                read_model.deployments_count += 1

            read_model.updated_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def project_state_transitioned(
        self,
        execution_id: UUID,
        to_state: str,
        started_at: datetime = None,
        completed_at: datetime = None,
        assigned_to: UUID = None,
    ):
        """Update state in read model on state transition event."""
        read_model = await self.db.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )

        if read_model:
            read_model.state = to_state

            if to_state == "in_progress" and started_at:
                read_model.started_at = started_at
            elif to_state == "completed" and completed_at:
                read_model.completed_at = completed_at

            if assigned_to:
                read_model.assigned_to = assigned_to

            read_model.updated_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def project_outcome_recorded(
        self,
        execution_id: UUID,
        actual_outcome: str,
        outcome_validated: bool = False,
    ):
        """Update outcome in read model on outcome.recorded event."""
        read_model = await self.db.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )

        if read_model:
            read_model.actual_outcome = actual_outcome
            read_model.outcome_validated = outcome_validated
            read_model.updated_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def project_outcome_validated(
        self,
        execution_id: UUID,
    ):
        """Mark outcome as validated in read model."""
        read_model = await self.db.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )

        if read_model:
            read_model.outcome_validated = True
            read_model.updated_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def rebuild_from_events(self, execution_id: UUID):
        """Rebuild read model from scratch by replaying events.

        Used for recovery or debugging. In production, would be called
        by event replay process after schema migrations.
        """
        pass


class DecisionReadModelProjector:
    """Project decision domain events into the denormalized DecisionReadModel table."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def project_decision_created(
        self,
        decision_id: UUID,
        question: str,
        project_id: UUID,
        owner_id: UUID,
        tenant_id: UUID,
    ) -> None:
        """Create read model entry when a decision is created."""
        existing = await self.db.scalar(
            select(DecisionReadModel).where(DecisionReadModel.decision_id == decision_id)
        )
        if existing:
            return
        now = datetime.now(timezone.utc)
        rm = DecisionReadModel(
            decision_id=decision_id,
            question=question,
            project_id=project_id,
            owner_id=owner_id,
            current_state="ideation",
            current_version=1,
            tenant_id=tenant_id,
            last_activity_at=now,
            last_activity_by=owner_id,
        )
        self.db.add(rm)
        await self.db.flush()

    async def project_rationale_added(self, decision_id: UUID, actor_id: UUID) -> None:
        rm = await self._get(decision_id)
        if rm:
            rm.rationale_count += 1
            self._touch(rm, actor_id)
            await self.db.flush()

    async def project_confidence_scored(
        self, decision_id: UUID, overall_confidence: float, actor_id: UUID
    ) -> None:
        rm = await self._get(decision_id)
        if rm:
            rm.overall_confidence = overall_confidence
            rm.confidence_count += 1
            self._touch(rm, actor_id)
            await self.db.flush()

    async def project_risk_assessed(
        self, decision_id: UUID, overall_risk: float, actor_id: UUID
    ) -> None:
        rm = await self._get(decision_id)
        if rm:
            rm.overall_risk = overall_risk
            rm.risk_count += 1
            self._touch(rm, actor_id)
            await self.db.flush()

    async def project_state_transitioned(
        self, decision_id: UUID, to_state: str, actor_id: UUID
    ) -> None:
        rm = await self._get(decision_id)
        if rm:
            rm.current_state = to_state
            rm.current_version += 1
            self._touch(rm, actor_id)
            await self.db.flush()

    async def project_guardrail_blocked(
        self, decision_id: UUID, block_reason: str
    ) -> None:
        rm = await self._get(decision_id)
        if rm:
            rm.is_blocked = True
            rm.block_reason = block_reason
            rm.updated_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def _get(self, decision_id: UUID) -> Optional[DecisionReadModel]:
        return await self.db.scalar(
            select(DecisionReadModel).where(DecisionReadModel.decision_id == decision_id)
        )

    def _touch(self, rm: DecisionReadModel, actor_id: UUID) -> None:
        now = datetime.now(timezone.utc)
        rm.last_activity_at = now
        rm.last_activity_by = actor_id
        rm.updated_at = now
