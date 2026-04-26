"""System 7: Detects system-wide risk signals from outcome and cluster data."""
from __future__ import annotations

import json
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import DecisionAccuracy, DecisionCluster, GlobalRiskSignal


class GlobalRiskDetector:
    """Scans all outcomes and clusters; creates GlobalRiskSignal rows when patterns emerge."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_signals(self, tenant_id: UUID) -> list[GlobalRiskSignal]:
        signals = []

        accuracies = (await self.db.execute(
            select(DecisionAccuracy).where(
                DecisionAccuracy.tenant_id == tenant_id,
                DecisionAccuracy.is_correct.isnot(None),
            )
        )).scalars().all()

        # Signal 1: outcome-specific high failure rate
        by_outcome: dict[str, list] = {}
        for acc in accuracies:
            by_outcome.setdefault(acc.predicted_outcome, []).append(acc)

        for outcome, rows in by_outcome.items():
            if len(rows) < 10:
                continue
            fail_rate = sum(1 for a in rows if not a.is_correct) / len(rows)
            if fail_rate > 0.70:
                s = await self._upsert_signal(
                    tenant_id,
                    f"outcome_failure_{outcome}",
                    "outcome_failure",
                    {"outcome": outcome, "min_sample": 10},
                    fail_rate,
                    len(rows),
                    f"Decisions predicted as '{outcome}' fail {fail_rate * 100:.0f}% of the time",
                    f"Escalate all {outcome} predictions for peer review",
                    "escalate",
                )
                signals.append(s)

        # Signal 2: systemic overconfidence
        if len(accuracies) >= 20:
            avg_conf = sum(a.predicted_confidence for a in accuracies) / len(accuracies)
            avg_succ = sum(1 for a in accuracies if a.is_correct) / len(accuracies)
            gap = avg_conf - avg_succ
            if gap > 0.25:
                s = await self._upsert_signal(
                    tenant_id,
                    "systemic_overconfidence",
                    "systemic_bias",
                    {"confidence_gap": round(gap, 3)},
                    gap,
                    len(accuracies),
                    f"System confidence exceeds actual accuracy by {gap * 100:.0f}%",
                    "Apply a 20% confidence reduction to all new predictions",
                    "adjust_confidence",
                )
                signals.append(s)

        # Signal 3: unhealthy clusters
        unhealthy = (await self.db.execute(
            select(DecisionCluster).where(
                DecisionCluster.tenant_id == tenant_id,
                DecisionCluster.is_healthy == False,
                DecisionCluster.cluster_failure_rate >= 0.65,
            )
        )).scalars().all()

        for cluster in unhealthy:
            s = await self._upsert_signal(
                tenant_id,
                f"cluster_degradation_{cluster.id}",
                "cluster_degradation",
                {"cluster_id": str(cluster.id), "cluster_name": cluster.cluster_name},
                cluster.cluster_failure_rate,
                cluster.decision_count,
                f"Cluster '{cluster.cluster_name}' has {cluster.cluster_failure_rate * 100:.0f}% failure rate",
                f"Block or escalate all decisions matching cluster '{cluster.cluster_name}'",
                "block",
            )
            signals.append(s)

        return signals

    async def _upsert_signal(
        self,
        tenant_id: UUID,
        signal_name: str,
        signal_type: str,
        criteria: dict,
        failure_rate: float,
        count: int,
        description: str,
        recommendation: str,
        mitigation: str,
    ) -> GlobalRiskSignal:
        s = await self.db.scalar(
            select(GlobalRiskSignal).where(
                GlobalRiskSignal.tenant_id == tenant_id,
                GlobalRiskSignal.signal_name == signal_name,
            )
        )
        if not s:
            s = GlobalRiskSignal(
                tenant_id=tenant_id,
                signal_name=signal_name,
                signal_type=signal_type,
                criteria=json.dumps(criteria),
            )
            self.db.add(s)

        s.failure_rate = failure_rate
        s.affected_decisions_count = count
        s.recommendation = recommendation
        s.mitigation_action = mitigation
        s.confidence = min(0.95, failure_rate * 0.9)
        s.last_validated_at = datetime.now(timezone.utc)
        s.severity = (
            "critical" if failure_rate >= 0.75 else
            "high" if failure_rate >= 0.60 else
            "medium" if failure_rate >= 0.45 else "low"
        )

        await self.db.flush()
        return s

    async def get_active_signals(self, tenant_id: UUID) -> list[GlobalRiskSignal]:
        return (await self.db.execute(
            select(GlobalRiskSignal).where(
                GlobalRiskSignal.tenant_id == tenant_id,
                GlobalRiskSignal.is_active == True,
            ).order_by(GlobalRiskSignal.failure_rate.desc())
        )).scalars().all()
