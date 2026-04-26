"""System 6: Detects recurring failure patterns per role from accuracy history."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import DecisionAccuracy, FailurePattern


class FailurePatternDetector:
    """Identifies patterns correlating with decision failures."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_patterns_for_role(self, tenant_id: UUID, role_id: UUID) -> list[FailurePattern]:
        rows = (await self.db.execute(
            select(DecisionAccuracy).where(
                DecisionAccuracy.tenant_id == tenant_id,
                DecisionAccuracy.role_id == role_id,
                DecisionAccuracy.is_correct.isnot(None),
            )
        )).scalars().all()

        if not rows:
            return []

        patterns = []

        # Pattern: low-confidence failures
        low_conf = [a for a in rows if a.predicted_confidence < 0.5]
        if low_conf:
            fail_rate = sum(1 for a in low_conf if not a.is_correct) / len(low_conf)
            if fail_rate > 0.6:
                p = await self._upsert_pattern(
                    tenant_id, role_id,
                    "low_confidence_failures",
                    "Decisions with <50% predicted confidence fail >60% of the time",
                    len([a for a in low_conf if not a.is_correct]),
                    len(low_conf),
                    fail_rate,
                    "critical" if fail_rate > 0.8 else "warning",
                    "Avoid decisions with <50% confidence or escalate for review first.",
                )
                patterns.append(p)

        # Pattern: high-confidence overconfidence
        high_conf = [a for a in rows if a.predicted_confidence > 0.8]
        if high_conf:
            fail_rate = sum(1 for a in high_conf if not a.is_correct) / len(high_conf)
            if fail_rate > 0.3:
                p = await self._upsert_pattern(
                    tenant_id, role_id,
                    "overconfidence",
                    "Decisions with >80% confidence still fail >30% of the time",
                    len([a for a in high_conf if not a.is_correct]),
                    len(high_conf),
                    fail_rate,
                    "warning",
                    "Recalibrate confidence estimates. This role may be systematically overconfident.",
                )
                patterns.append(p)

        return patterns

    async def _upsert_pattern(
        self,
        tenant_id: UUID,
        role_id: UUID,
        name: str,
        description: str,
        failure_count: int,
        total_count: int,
        failure_rate: float,
        severity: str,
        recommendation: str,
    ) -> FailurePattern:
        p = await self.db.scalar(
            select(FailurePattern).where(
                FailurePattern.tenant_id == tenant_id,
                FailurePattern.role_id == role_id,
                FailurePattern.pattern_name == name,
            )
        )
        if not p:
            p = FailurePattern(
                tenant_id=tenant_id,
                role_id=role_id,
                pattern_name=name,
                pattern_description=description,
                conditions="{}",
            )
            self.db.add(p)

        p.failure_count = failure_count
        p.total_count = total_count
        p.failure_rate = failure_rate
        p.severity = severity
        p.recommendation = recommendation
        p.last_updated = datetime.now(timezone.utc)

        await self.db.flush()
        return p
