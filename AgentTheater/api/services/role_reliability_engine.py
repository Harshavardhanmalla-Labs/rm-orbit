"""System 6.5: Role reliability score used to weight decision influence."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import RoleReliabilityScore, RolePerformance


class RoleReliabilityEngine:
    """Computes a composite reliability score: accuracy × calibration × recency."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def compute_reliability(
        self, tenant_id: UUID, role_id: UUID, role_name: str
    ) -> RoleReliabilityScore:
        rec = await self.db.scalar(
            select(RoleReliabilityScore).where(
                RoleReliabilityScore.tenant_id == tenant_id,
                RoleReliabilityScore.role_id == role_id,
            )
        )
        if not rec:
            rec = RoleReliabilityScore(
                tenant_id=tenant_id, role_id=role_id, role_name=role_name
            )
            self.db.add(rec)

        perf = await self.db.scalar(
            select(RolePerformance).where(
                RolePerformance.tenant_id == tenant_id,
                RolePerformance.role_id == role_id,
            )
        )
        if perf:
            rec.accuracy_score = perf.accuracy_score
            rec.decision_volume = perf.total_decisions
            if perf.is_overconfident:
                rec.confidence_calibration = max(0.5, 1.0 - perf.calibration_gap)
            else:
                rec.confidence_calibration = min(1.2, 1.0 + (perf.calibration_gap * 0.5))
            if perf.decisions_last_30_days > 0 and perf.accuracy_last_30_days is not None:
                rec.recency_factor = perf.accuracy_last_30_days

        # Weighted composite: accuracy 50%, calibration 30%, recency 20%
        rec.reliability_score = (
            rec.accuracy_score * 0.5
            + rec.confidence_calibration * 0.3
            + rec.recency_factor * 0.2
        )

        if rec.reliability_score >= 0.85:
            rec.reliability_tier = "expert"
        elif rec.reliability_score >= 0.70:
            rec.reliability_tier = "trusted"
        elif rec.reliability_score >= 0.55:
            rec.reliability_tier = "developing"
        else:
            rec.reliability_tier = "unproven"

        rec.last_calculated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return rec

    async def get_reliability(
        self, tenant_id: UUID, role_id: UUID
    ) -> Optional[RoleReliabilityScore]:
        return await self.db.scalar(
            select(RoleReliabilityScore).where(
                RoleReliabilityScore.tenant_id == tenant_id,
                RoleReliabilityScore.role_id == role_id,
            )
        )
