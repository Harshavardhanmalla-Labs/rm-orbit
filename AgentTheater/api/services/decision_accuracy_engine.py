"""System 6: Decision accuracy computation against validated outcomes."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import (
    Decision, DecisionConfidence, DecisionAccuracy
)


class DecisionAccuracyEngine:
    """Computes accuracy by comparing predicted outcome vs actual validated outcome."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def compute_accuracy_for_outcome(
        self,
        tenant_id: UUID,
        decision_id: UUID,
        actual_outcome: str,
        validation_source: str = "outcome_recorded",
    ) -> DecisionAccuracy:
        """Called when an outcome is validated. Compares to prediction, stores result."""
        decision = await self.db.scalar(
            select(Decision).where(
                Decision.id == decision_id,
                Decision.tenant_id == tenant_id,
            )
        )
        if not decision:
            raise ValueError(f"Decision {decision_id} not found")

        confidence = await self.db.scalar(
            select(DecisionConfidence).where(
                DecisionConfidence.decision_id == decision_id,
                DecisionConfidence.tenant_id == tenant_id,
            )
        )
        predicted_confidence = (confidence.overall_confidence / 100.0) if confidence else 0.5

        acc = await self.db.scalar(
            select(DecisionAccuracy).where(
                DecisionAccuracy.decision_id == decision_id,
                DecisionAccuracy.tenant_id == tenant_id,
            )
        )
        if not acc:
            acc = DecisionAccuracy(
                tenant_id=tenant_id,
                decision_id=decision_id,
                role_id=decision.created_by,
                predicted_outcome=decision.outcome or "UNKNOWN",
                predicted_confidence=predicted_confidence,
                predicted_at=decision.created_at,
            )
            self.db.add(acc)

        acc.actual_outcome = actual_outcome
        acc.actual_at = datetime.now(timezone.utc)
        acc.validation_source = validation_source
        acc.is_correct = (acc.predicted_outcome == actual_outcome)
        acc.accuracy_score = 1.0 if acc.is_correct else 0.0
        acc.confidence_error = abs(predicted_confidence - acc.accuracy_score)
        acc.updated_at = datetime.now(timezone.utc)

        await self.db.flush()
        return acc

    async def get_accuracy(self, tenant_id: UUID, decision_id: UUID) -> Optional[DecisionAccuracy]:
        return await self.db.scalar(
            select(DecisionAccuracy).where(
                DecisionAccuracy.decision_id == decision_id,
                DecisionAccuracy.tenant_id == tenant_id,
            )
        )
