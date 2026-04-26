"""System 7: Cluster similar decisions for cross-decision learning."""
from __future__ import annotations

import json
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import Decision, DecisionAccuracy, DecisionSimilarity, DecisionCluster


class DecisionClusteringEngine:
    """Groups decisions into clusters using similarity graph connected-components."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cluster_by_pattern(
        self,
        tenant_id: UUID,
        cluster_name: str,
        cluster_type: str,
        criteria: dict,
        description: str,
    ) -> DecisionCluster:
        """Create a cluster by filtering decisions against explicit criteria."""
        decisions = (await self.db.execute(
            select(Decision).where(Decision.tenant_id == tenant_id)
        )).scalars().all()

        accuracies = {
            a.decision_id: a
            for a in (await self.db.execute(
                select(DecisionAccuracy).where(DecisionAccuracy.tenant_id == tenant_id)
            )).scalars().all()
        }

        member_ids = []
        for d in decisions:
            acc = accuracies.get(d.id)
            if not acc:
                continue
            if "recommendation" in criteria and d.outcome != criteria["recommendation"]:
                continue
            if "confidence_max" in criteria and acc.predicted_confidence > criteria["confidence_max"]:
                continue
            if "confidence_min" in criteria and acc.predicted_confidence < criteria["confidence_min"]:
                continue
            if criteria.get("failed") is True and acc.is_correct is not False:
                continue
            member_ids.append(str(d.id))

        cluster = DecisionCluster(
            tenant_id=tenant_id,
            cluster_name=cluster_name,
            cluster_type=cluster_type,
            description=description,
            decision_count=len(member_ids),
            member_decision_ids=json.dumps(member_ids),
            defining_criteria=json.dumps(criteria),
        )
        self.db.add(cluster)
        await self._compute_metrics(cluster, accuracies)
        await self.db.flush()
        return cluster

    async def auto_cluster_by_similarity(
        self, tenant_id: UUID, threshold: float = 0.65
    ) -> list[DecisionCluster]:
        """Connected-components clustering on the similarity graph."""
        edges = (await self.db.execute(
            select(DecisionSimilarity).where(
                DecisionSimilarity.tenant_id == tenant_id,
                DecisionSimilarity.similarity_score >= threshold,
            )
        )).scalars().all()

        graph: dict[UUID, list[UUID]] = {}
        for e in edges:
            graph.setdefault(e.decision_id_a, []).append(e.decision_id_b)
            graph.setdefault(e.decision_id_b, []).append(e.decision_id_a)

        visited: set[UUID] = set()
        components: list[list[UUID]] = []
        for node in graph:
            if node in visited:
                continue
            component = []
            queue = [node]
            while queue:
                cur = queue.pop(0)
                if cur in visited:
                    continue
                visited.add(cur)
                component.append(cur)
                queue.extend(n for n in graph.get(cur, []) if n not in visited)
            if len(component) >= 3:
                components.append(component)

        accuracies = {
            a.decision_id: a
            for a in (await self.db.execute(
                select(DecisionAccuracy).where(DecisionAccuracy.tenant_id == tenant_id)
            )).scalars().all()
        }

        clusters = []
        for i, comp in enumerate(components):
            c = DecisionCluster(
                tenant_id=tenant_id,
                cluster_name=f"similarity_cluster_{i}",
                cluster_type="feature_similarity",
                decision_count=len(comp),
                member_decision_ids=json.dumps([str(d) for d in comp]),
                defining_criteria=json.dumps({"similarity_threshold": threshold}),
            )
            self.db.add(c)
            await self._compute_metrics(c, accuracies)
            clusters.append(c)

        await self.db.flush()
        return clusters

    async def _compute_metrics(
        self, cluster: DecisionCluster, accuracies: dict
    ) -> None:
        member_ids = [UUID(m) for m in json.loads(cluster.member_decision_ids)]
        decided = [
            accuracies[mid]
            for mid in member_ids
            if mid in accuracies and accuracies[mid].is_correct is not None
        ]
        if not decided:
            cluster.is_healthy = True
            return
        correct = sum(1 for a in decided if a.is_correct)
        cluster.cluster_accuracy = correct / len(decided)
        cluster.cluster_failure_rate = 1.0 - cluster.cluster_accuracy
        cluster.cluster_confidence_avg = sum(a.predicted_confidence for a in decided) / len(decided)
        fr = cluster.cluster_failure_rate
        cluster.cluster_risk_level = (
            "critical" if fr >= 0.75 else
            "high" if fr >= 0.50 else
            "medium" if fr >= 0.30 else "low"
        )
        cluster.is_healthy = fr < 0.4

    async def get_unhealthy_clusters(
        self, tenant_id: UUID, limit: int = 10
    ) -> list[DecisionCluster]:
        return (await self.db.execute(
            select(DecisionCluster)
            .where(DecisionCluster.tenant_id == tenant_id, DecisionCluster.is_healthy == False)
            .order_by(DecisionCluster.cluster_failure_rate.desc())
            .limit(limit)
        )).scalars().all()
