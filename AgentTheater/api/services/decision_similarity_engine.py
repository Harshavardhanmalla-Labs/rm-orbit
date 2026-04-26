"""System 7: Decision similarity computation using feature-based Jaccard scoring."""
from __future__ import annotations

import json
from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import Decision, DecisionAccuracy, DecisionSimilarity


class DecisionSimilarityEngine:
    """Computes pairwise similarity between decisions across multiple feature axes."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def compute_similarity_for_pair(
        self,
        tenant_id: UUID,
        decision_id_a: UUID,
        decision_id_b: UUID,
    ) -> DecisionSimilarity:
        decisions = {
            d.id: d
            for d in (await self.db.execute(
                select(Decision).where(Decision.id.in_([decision_id_a, decision_id_b]))
            )).scalars().all()
        }
        if len(decisions) != 2:
            raise ValueError("Both decisions must exist")

        da, db_ = decisions[decision_id_a], decisions[decision_id_b]
        accuracies = {
            a.decision_id: a
            for a in (await self.db.execute(
                select(DecisionAccuracy).where(
                    DecisionAccuracy.decision_id.in_([decision_id_a, decision_id_b])
                )
            )).scalars().all()
        }

        score = 0.0
        similar_features = []

        # Axis 1: question keyword overlap (Jaccard)
        qs = self._jaccard(da.question, db_.question)
        score += qs * 0.20
        if qs > 0.6:
            similar_features.append("question_similarity")

        # Axis 2: same outcome field
        if da.outcome and db_.outcome and da.outcome == db_.outcome:
            score += 0.25
            similar_features.append("outcome_agreement")

        # Axis 3: confidence band proximity
        acc_a = accuracies.get(decision_id_a)
        acc_b = accuracies.get(decision_id_b)
        if acc_a and acc_b:
            conf_sim = 1.0 - abs(acc_a.predicted_confidence - acc_b.predicted_confidence)
            score += conf_sim * 0.15
            if abs(acc_a.predicted_confidence - acc_b.predicted_confidence) < 0.2:
                similar_features.append("confidence_band")

        # Axis 4: same creator (role)
        if da.created_by == db_.created_by:
            score += 0.15
            similar_features.append("same_role")

        # Axis 5: temporal proximity (within 7 days)
        if da.created_at and db_.created_at:
            diff = abs((da.created_at - db_.created_at).total_seconds())
            if diff < 604800:
                score += 0.10
                similar_features.append("temporal_proximity")

        score = max(0.0, min(1.0, score))

        sim = await self.db.scalar(
            select(DecisionSimilarity).where(
                DecisionSimilarity.tenant_id == tenant_id,
                or_(
                    (DecisionSimilarity.decision_id_a == decision_id_a) &
                    (DecisionSimilarity.decision_id_b == decision_id_b),
                    (DecisionSimilarity.decision_id_a == decision_id_b) &
                    (DecisionSimilarity.decision_id_b == decision_id_a),
                ),
            )
        )
        if not sim:
            sim = DecisionSimilarity(
                tenant_id=tenant_id,
                decision_id_a=decision_id_a,
                decision_id_b=decision_id_b,
            )
            self.db.add(sim)

        sim.similarity_score = score
        sim.similarity_type = "feature"
        sim.similar_features = json.dumps(similar_features)
        if acc_a:
            sim.outcome_a = acc_a.actual_outcome
        if acc_b:
            sim.outcome_b = acc_b.actual_outcome
        if acc_a and acc_b and acc_a.actual_outcome and acc_b.actual_outcome:
            sim.outcome_agreement = acc_a.actual_outcome == acc_b.actual_outcome

        await self.db.flush()
        return sim

    def _jaccard(self, a: str, b: str) -> float:
        wa = set(a.lower().split())
        wb = set(b.lower().split())
        if not wa or not wb:
            return 0.0
        return len(wa & wb) / len(wa | wb)

    async def find_similar(
        self,
        tenant_id: UUID,
        decision_id: UUID,
        threshold: float = 0.6,
        limit: int = 10,
    ) -> list[DecisionSimilarity]:
        return (await self.db.execute(
            select(DecisionSimilarity).where(
                DecisionSimilarity.tenant_id == tenant_id,
                or_(
                    DecisionSimilarity.decision_id_a == decision_id,
                    DecisionSimilarity.decision_id_b == decision_id,
                ),
                DecisionSimilarity.similarity_score >= threshold,
            ).order_by(DecisionSimilarity.similarity_score.desc()).limit(limit)
        )).scalars().all()
