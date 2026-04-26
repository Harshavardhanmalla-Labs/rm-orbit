"""System 6: Aggregated role performance metrics from decision accuracy records."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import RolePerformance, DecisionAccuracy


class RolePerformanceTracker:
    """Rolls up per-role accuracy, confidence, and calibration from DecisionAccuracy rows."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_role_performance(
        self,
        tenant_id: UUID,
        role_id: UUID,
        role_name: str,
    ) -> RolePerformance:
        """Recalculate and persist role performance metrics."""
        perf = await self.db.scalar(
            select(RolePerformance).where(
                RolePerformance.tenant_id == tenant_id,
                RolePerformance.role_id == role_id,
            )
        )
        if not perf:
            perf = RolePerformance(
                tenant_id=tenant_id,
                role_id=role_id,
                role_name=role_name,
            )
            self.db.add(perf)

        all_rows = (await self.db.execute(
            select(DecisionAccuracy).where(
                DecisionAccuracy.tenant_id == tenant_id,
                DecisionAccuracy.role_id == role_id,
            )
        )).scalars().all()

        perf.total_decisions = len(all_rows)
        perf.decisions_correct = sum(1 for a in all_rows if a.is_correct is True)
        perf.decisions_incorrect = sum(1 for a in all_rows if a.is_correct is False)
        perf.decisions_pending = sum(1 for a in all_rows if a.is_correct is None)

        decided = [a for a in all_rows if a.is_correct is not None]
        if decided:
            perf.accuracy_score = sum(a.accuracy_score for a in decided) / len(decided)
            perf.avg_predicted_confidence = sum(a.predicted_confidence for a in decided) / len(decided)
            perf.avg_confidence_error = sum(
                a.confidence_error for a in decided if a.confidence_error is not None
            ) / len(decided)
            perf.is_overconfident = perf.avg_predicted_confidence > perf.accuracy_score
            perf.calibration_gap = abs(perf.avg_predicted_confidence - perf.accuracy_score)

        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        cutoff_naive = cutoff.replace(tzinfo=None)
        recent = [
            a for a in all_rows
            if a.created_at and (
                a.created_at >= cutoff
                if a.created_at.tzinfo else
                a.created_at >= cutoff_naive
            )
        ]
        perf.decisions_last_30_days = len(recent)
        recent_decided = [a for a in recent if a.is_correct is not None]
        if recent_decided:
            perf.accuracy_last_30_days = sum(a.accuracy_score for a in recent_decided) / len(recent_decided)

        perf.trend = self._compute_trend(all_rows)
        perf.updated_at = datetime.now(timezone.utc)

        await self.db.flush()
        return perf

    def _compute_trend(self, rows: list) -> str:
        if len(rows) < 10:
            return "insufficient_data"
        now = datetime.now(timezone.utc)
        now_naive = now.replace(tzinfo=None)

        def _ge(dt, cutoff):
            if dt.tzinfo:
                return dt >= cutoff
            return dt >= cutoff.replace(tzinfo=None)

        def _between(dt, lo, hi):
            if dt.tzinfo:
                return lo <= dt < hi
            lo_n, hi_n = lo.replace(tzinfo=None), hi.replace(tzinfo=None)
            return lo_n <= dt < hi_n

        recent = [a for a in rows if a.created_at and _ge(a.created_at, now - timedelta(days=30))]
        prior = [a for a in rows if a.created_at and _between(a.created_at, now - timedelta(days=60), now - timedelta(days=30))]
        r_dec = [a for a in recent if a.is_correct is not None]
        p_dec = [a for a in prior if a.is_correct is not None]
        if not r_dec or not p_dec:
            return "insufficient_data"
        r_acc = sum(a.accuracy_score for a in r_dec) / len(r_dec)
        p_acc = sum(a.accuracy_score for a in p_dec) / len(p_dec)
        delta = r_acc - p_acc
        if abs(delta) < 0.05:
            return "stable"
        return "improving" if delta > 0 else "declining"

    async def get_role_leaderboard(
        self, tenant_id: UUID, limit: int = 10
    ) -> list[RolePerformance]:
        result = await self.db.execute(
            select(RolePerformance)
            .where(RolePerformance.tenant_id == tenant_id)
            .order_by(RolePerformance.accuracy_score.desc())
            .limit(limit)
        )
        return result.scalars().all()
