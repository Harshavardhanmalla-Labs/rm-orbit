"""System 6.5: Decision risk assessment before finalization."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import (
    DecisionAccuracy, FailurePattern, RoleReliabilityScore, DecisionInfluenceRecord
)


class DecisionRiskEngine:
    """Assesses decision risk using accuracy history, failure patterns, and role reliability."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def assess_decision_risk(
        self,
        tenant_id: UUID,
        decision_id: UUID,
        predicted_outcome: str,
        predicted_confidence: float,
        role_id: UUID,
    ) -> DecisionInfluenceRecord:
        influence = await self.db.scalar(
            select(DecisionInfluenceRecord).where(
                DecisionInfluenceRecord.decision_id == decision_id,
                DecisionInfluenceRecord.tenant_id == tenant_id,
            )
        )
        if not influence:
            influence = DecisionInfluenceRecord(
                tenant_id=tenant_id,
                decision_id=decision_id,
                original_confidence=predicted_confidence,
                adjusted_confidence=predicted_confidence,
            )
            self.db.add(influence)

        risk_factors = []
        risk_score = 0.0

        # Factor 1: low historical accuracy for this role
        accuracies = (await self.db.execute(
            select(DecisionAccuracy).where(
                DecisionAccuracy.tenant_id == tenant_id,
                DecisionAccuracy.role_id == role_id,
                DecisionAccuracy.is_correct.isnot(None),
            )
        )).scalars().all()

        if accuracies:
            avg_acc = sum(1 for a in accuracies if a.is_correct) / len(accuracies)
            if avg_acc < 0.6:
                risk_factors.append("low_accuracy_history")
                risk_score += 0.30
            avg_err = sum(
                a.confidence_error for a in accuracies if a.confidence_error is not None
            ) / len(accuracies)
            if avg_err > 0.3:
                risk_factors.append("overconfidence")
                risk_score += 0.15

        # Factor 2: applicable failure patterns
        patterns = (await self.db.execute(
            select(FailurePattern).where(
                FailurePattern.tenant_id == tenant_id,
                FailurePattern.role_id == role_id,
            )
        )).scalars().all()
        for p in patterns:
            if p.failure_rate and p.failure_rate > 0.5:
                risk_factors.append(f"pattern:{p.pattern_name}")
                risk_score += 0.20
                influence.similar_failed_decisions = (influence.similar_failed_decisions or 0) + 1

        # Factor 3: role reliability tier
        reliability = await self.db.scalar(
            select(RoleReliabilityScore).where(
                RoleReliabilityScore.tenant_id == tenant_id,
                RoleReliabilityScore.role_id == role_id,
            )
        )
        if reliability and reliability.reliability_tier == "unproven":
            risk_factors.append("low_role_reliability")
            risk_score += 0.25

        # Factor 4: low confidence
        if predicted_confidence < 0.5:
            risk_factors.append("low_confidence")
            risk_score += 0.20

        influence.risk_factors = str(risk_factors)
        influence.risk_score = min(1.0, risk_score)

        if influence.risk_score >= 0.75:
            influence.risk_level = "critical"
            influence.is_flagged = True
            influence.requires_additional_review = True
            influence.requires_multi_role_consensus = True
        elif influence.risk_score >= 0.50:
            influence.risk_level = "high"
            influence.is_flagged = True
            influence.requires_additional_review = True
        elif influence.risk_score >= 0.30:
            influence.risk_level = "medium"
            influence.is_flagged = True
        else:
            influence.risk_level = "low"

        influence.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return influence
