"""Tests for Systems 6, 6.5, and 7: Learning, Influence, and Graph."""
from __future__ import annotations

import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from AgentTheater.events.db_models import (
    Base,
    Decision, DecisionConfidence, DecisionAccuracy, RolePerformance,
    ConfidenceCalibration, FailurePattern,
    RoleReliabilityScore, DecisionInfluenceRecord, DecisionGuardrail,
    DecisionCluster, DecisionSimilarity, GlobalRiskSignal,
)
from AgentTheater.api.services.decision_accuracy_engine import DecisionAccuracyEngine
from AgentTheater.api.services.role_performance_tracker import RolePerformanceTracker
from AgentTheater.api.services.confidence_calibration_engine import ConfidenceCalibrationEngine
from AgentTheater.api.services.failure_pattern_detector import FailurePatternDetector
from AgentTheater.api.services.role_reliability_engine import RoleReliabilityEngine
from AgentTheater.api.services.decision_risk_engine import DecisionRiskEngine
from AgentTheater.api.services.guardrail_enforcement_engine import GuardrailEnforcementEngine
from AgentTheater.api.services.decision_similarity_engine import DecisionSimilarityEngine
from AgentTheater.api.services.decision_clustering_engine import DecisionClusteringEngine
from AgentTheater.api.services.global_risk_detector import GlobalRiskDetector

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session


# ─────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────

def _decision(tenant_id, role_id, outcome="succeeded"):
    d = Decision(
        id=uuid4(),
        project_id=uuid4(),
        question="Should we proceed with this initiative?",
        roles=[],
        outcome=outcome,
        tenant_id=tenant_id,
        created_by=role_id,
        created_at=datetime.now(timezone.utc),
    )
    return d


def _accuracy(tenant_id, decision_id, role_id, predicted_conf=0.7, is_correct=True):
    return DecisionAccuracy(
        id=uuid4(),
        tenant_id=tenant_id,
        decision_id=decision_id,
        role_id=role_id,
        predicted_outcome="succeeded" if is_correct else "failed",
        predicted_confidence=predicted_conf,
        predicted_at=datetime.now(timezone.utc),
        actual_outcome="succeeded" if is_correct else "failed",
        actual_at=datetime.now(timezone.utc),
        is_correct=is_correct,
        accuracy_score=1.0 if is_correct else 0.0,
        confidence_error=abs(predicted_conf - (1.0 if is_correct else 0.0)),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


# ─────────────────────────────────────────────────────
# System 6: Decision Accuracy
# ─────────────────────────────────────────────────────

class TestDecisionAccuracyEngine:
    @pytest.mark.asyncio
    async def test_correct_prediction_scores_one(self, db):
        tenant = uuid4()
        role = uuid4()
        d = _decision(tenant, role, outcome="succeeded")
        db.add(d)
        conf = DecisionConfidence(
            id=uuid4(), decision_id=d.id, tenant_id=tenant,
            technical_confidence=70, market_confidence=70,
            team_confidence=70, overall_confidence=70, scored_by=role,
            created_at=datetime.now(timezone.utc),
        )
        db.add(conf)
        await db.flush()

        engine = DecisionAccuracyEngine(db)
        acc = await engine.compute_accuracy_for_outcome(tenant, d.id, "succeeded")

        assert acc.is_correct is True
        assert acc.accuracy_score == 1.0

    @pytest.mark.asyncio
    async def test_wrong_prediction_scores_zero(self, db):
        tenant = uuid4()
        role = uuid4()
        d = _decision(tenant, role, outcome="succeeded")
        db.add(d)
        await db.flush()

        engine = DecisionAccuracyEngine(db)
        acc = await engine.compute_accuracy_for_outcome(tenant, d.id, "failed")

        assert acc.is_correct is False
        assert acc.accuracy_score == 0.0

    @pytest.mark.asyncio
    async def test_tenant_isolation(self, db):
        t1, t2, role = uuid4(), uuid4(), uuid4()
        d1 = _decision(t1, role)
        d2 = _decision(t2, role)
        db.add_all([d1, d2])
        await db.flush()

        engine = DecisionAccuracyEngine(db)
        await engine.compute_accuracy_for_outcome(t1, d1.id, "succeeded")

        result = await engine.get_accuracy(t2, d1.id)
        assert result is None


# ─────────────────────────────────────────────────────
# System 6: Role Performance
# ─────────────────────────────────────────────────────

class TestRolePerformanceTracker:
    @pytest.mark.asyncio
    async def test_accuracy_aggregation(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(10):
            a = _accuracy(tenant, uuid4(), role, is_correct=i < 7)
            db.add(a)
        await db.flush()

        tracker = RolePerformanceTracker(db)
        perf = await tracker.update_role_performance(tenant, role, "CTO")

        assert perf.total_decisions == 10
        assert perf.decisions_correct == 7
        assert abs(perf.accuracy_score - 0.7) < 0.01

    @pytest.mark.asyncio
    async def test_overconfidence_detected(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(5):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.9, is_correct=i < 3)
            db.add(a)
        await db.flush()

        tracker = RolePerformanceTracker(db)
        perf = await tracker.update_role_performance(tenant, role, "CEO")

        assert perf.is_overconfident is True

    @pytest.mark.asyncio
    async def test_leaderboard_ordered_by_accuracy(self, db):
        tenant = uuid4()
        roles = [uuid4(), uuid4(), uuid4()]
        accuracies = [0.9, 0.5, 0.7]
        for role, acc_val in zip(roles, accuracies):
            a = _accuracy(tenant, uuid4(), role, is_correct=acc_val > 0.6)
            db.add(a)
        await db.flush()

        tracker = RolePerformanceTracker(db)
        for role, name in zip(roles, ["A", "B", "C"]):
            await tracker.update_role_performance(tenant, role, name)

        board = await tracker.get_role_leaderboard(tenant, limit=3)
        scores = [p.accuracy_score for p in board]
        assert scores == sorted(scores, reverse=True)


# ─────────────────────────────────────────────────────
# System 6: Confidence Calibration
# ─────────────────────────────────────────────────────

class TestConfidenceCalibrationEngine:
    @pytest.mark.asyncio
    async def test_calibration_band_computed(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(10):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.85, is_correct=i < 8)
            db.add(a)
        await db.flush()

        engine = ConfidenceCalibrationEngine(db)
        cals = await engine.calibrate_for_role(tenant, role)

        band = next(c for c in cals if c.confidence_band_low == 0.8)
        assert band.predictions_in_band == 10
        assert band.successes_in_band == 8
        assert abs(band.actual_success_rate - 0.8) < 0.01

    @pytest.mark.asyncio
    async def test_overconfident_band_has_adjustment_below_one(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(10):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.85, is_correct=i < 4)
            db.add(a)
        await db.flush()

        engine = ConfidenceCalibrationEngine(db)
        cals = await engine.calibrate_for_role(tenant, role)

        band = next((c for c in cals if c.confidence_band_low == 0.8), None)
        assert band is not None
        assert band.adjustment_factor is not None
        assert band.adjustment_factor < 1.0


# ─────────────────────────────────────────────────────
# System 6: Failure Pattern Detection
# ─────────────────────────────────────────────────────

class TestFailurePatternDetector:
    @pytest.mark.asyncio
    async def test_low_confidence_pattern_detected(self, db):
        tenant, role = uuid4(), uuid4()
        for _ in range(5):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.3, is_correct=False)
            db.add(a)
        await db.flush()

        detector = FailurePatternDetector(db)
        patterns = await detector.detect_patterns_for_role(tenant, role)

        names = [p.pattern_name for p in patterns]
        assert "low_confidence_failures" in names

    @pytest.mark.asyncio
    async def test_no_patterns_when_accurate(self, db):
        tenant, role = uuid4(), uuid4()
        for _ in range(5):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.8, is_correct=True)
            db.add(a)
        await db.flush()

        detector = FailurePatternDetector(db)
        patterns = await detector.detect_patterns_for_role(tenant, role)
        assert len(patterns) == 0


# ─────────────────────────────────────────────────────
# System 6.5: Role Reliability
# ─────────────────────────────────────────────────────

class TestRoleReliabilityEngine:
    @pytest.mark.asyncio
    async def test_high_accuracy_earns_trusted_tier(self, db):
        tenant, role = uuid4(), uuid4()
        perf = RolePerformance(
            id=uuid4(), tenant_id=tenant, role_id=role, role_name="CTO",
            total_decisions=50, decisions_correct=45, accuracy_score=0.90,
            avg_predicted_confidence=0.85, is_overconfident=False,
            calibration_gap=0.05, decisions_last_30_days=10,
            accuracy_last_30_days=0.90, trend="improving",
            updated_at=datetime.now(timezone.utc),
        )
        db.add(perf)
        await db.flush()

        engine = RoleReliabilityEngine(db)
        rel = await engine.compute_reliability(tenant, role, "CTO")
        assert rel.reliability_tier in ("expert", "trusted")
        assert rel.reliability_score >= 0.7

    @pytest.mark.asyncio
    async def test_low_accuracy_earns_unproven_tier(self, db):
        tenant, role = uuid4(), uuid4()
        perf = RolePerformance(
            id=uuid4(), tenant_id=tenant, role_id=role, role_name="Intern",
            total_decisions=5, decisions_correct=1, accuracy_score=0.2,
            avg_predicted_confidence=0.8, is_overconfident=True,
            calibration_gap=0.6, decisions_last_30_days=5,
            accuracy_last_30_days=0.2, trend="declining",
            updated_at=datetime.now(timezone.utc),
        )
        db.add(perf)
        await db.flush()

        engine = RoleReliabilityEngine(db)
        rel = await engine.compute_reliability(tenant, role, "Intern")
        assert rel.reliability_tier in ("unproven", "developing")


# ─────────────────────────────────────────────────────
# System 6.5: Decision Risk
# ─────────────────────────────────────────────────────

class TestDecisionRiskEngine:
    @pytest.mark.asyncio
    async def test_low_accuracy_history_raises_risk(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(8):
            a = _accuracy(tenant, uuid4(), role, is_correct=i >= 6)
            db.add(a)
        await db.flush()

        engine = DecisionRiskEngine(db)
        influence = await engine.assess_decision_risk(tenant, uuid4(), "succeeded", 0.6, role)

        assert influence.is_flagged is True
        assert "low_accuracy_history" in influence.risk_factors

    @pytest.mark.asyncio
    async def test_low_confidence_flagged(self, db):
        tenant, role = uuid4(), uuid4()
        engine = DecisionRiskEngine(db)
        influence = await engine.assess_decision_risk(tenant, uuid4(), "succeeded", 0.25, role)

        assert "low_confidence" in influence.risk_factors
        assert influence.risk_score > 0.1


# ─────────────────────────────────────────────────────
# System 6.5: Guardrail Enforcement
# ─────────────────────────────────────────────────────

class TestGuardrailEnforcementEngine:
    @pytest.mark.asyncio
    async def test_low_confidence_blocked(self, db):
        tenant, role = uuid4(), uuid4()
        engine = GuardrailEnforcementEngine(db)
        await engine.setup_default_guardrails(tenant)
        await db.flush()

        # Create an influence record (required by check_guardrails)
        inf = DecisionInfluenceRecord(
            id=uuid4(), tenant_id=tenant, decision_id=uuid4(),
            original_confidence=0.2, adjusted_confidence=0.2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(inf)
        await db.flush()

        inf = await engine.check_guardrails(tenant, inf.decision_id, 0.2, "low", role)
        assert inf.is_blocked is True

    @pytest.mark.asyncio
    async def test_sufficient_confidence_not_blocked(self, db):
        tenant, role = uuid4(), uuid4()
        engine = GuardrailEnforcementEngine(db)
        await engine.setup_default_guardrails(tenant)

        inf = DecisionInfluenceRecord(
            id=uuid4(), tenant_id=tenant, decision_id=uuid4(),
            original_confidence=0.75, adjusted_confidence=0.75,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(inf)
        await db.flush()

        inf = await engine.check_guardrails(tenant, inf.decision_id, 0.75, "low", role)
        assert inf.is_blocked is False


# ─────────────────────────────────────────────────────
# System 7: Decision Similarity
# ─────────────────────────────────────────────────────

class TestDecisionSimilarityEngine:
    @pytest.mark.asyncio
    async def test_same_outcome_boosts_similarity(self, db):
        tenant, role = uuid4(), uuid4()
        d1 = _decision(tenant, role, outcome="succeeded")
        d2 = _decision(tenant, role, outcome="succeeded")
        db.add_all([d1, d2])
        await db.flush()

        engine = DecisionSimilarityEngine(db)
        sim = await engine.compute_similarity_for_pair(tenant, d1.id, d2.id)

        assert sim.similarity_score > 0.3

    @pytest.mark.asyncio
    async def test_different_outcome_lower_similarity(self, db):
        tenant = uuid4()
        r1, r2 = uuid4(), uuid4()
        d1 = _decision(tenant, r1, outcome="succeeded")
        d2 = _decision(tenant, r2, outcome="failed")
        d1.question = "Approve budget expansion"
        d2.question = "Reject vendor contract"
        db.add_all([d1, d2])
        await db.flush()

        engine = DecisionSimilarityEngine(db)
        sim = await engine.compute_similarity_for_pair(tenant, d1.id, d2.id)

        assert sim.similarity_score < 0.8


# ─────────────────────────────────────────────────────
# System 7: Decision Clustering
# ─────────────────────────────────────────────────────

class TestDecisionClusteringEngine:
    @pytest.mark.asyncio
    async def test_cluster_groups_failed_decisions(self, db):
        tenant, role = uuid4(), uuid4()
        for _ in range(5):
            d = _decision(tenant, role, outcome="failed")
            db.add(d)
            a = _accuracy(tenant, d.id, role, predicted_conf=0.3, is_correct=False)
            db.add(a)
        await db.flush()

        engine = DecisionClusteringEngine(db)
        cluster = await engine.create_cluster_by_pattern(
            tenant, "failed-low-conf", "outcome_pattern",
            {"confidence_max": 0.5, "failed": True},
            "Low confidence failures",
        )

        assert cluster.decision_count == 5
        assert cluster.cluster_failure_rate == 1.0
        assert cluster.is_healthy is False

    @pytest.mark.asyncio
    async def test_cluster_risk_level_critical_at_high_failure(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(10):
            d = _decision(tenant, role, outcome="failed")
            db.add(d)
            a = _accuracy(tenant, d.id, role, predicted_conf=0.3, is_correct=i >= 9)
            db.add(a)
        await db.flush()

        engine = DecisionClusteringEngine(db)
        cluster = await engine.create_cluster_by_pattern(
            tenant, "high-fail-cluster", "outcome_pattern",
            {"confidence_max": 0.5, "failed": True},
            "High failure cluster",
        )

        assert cluster.cluster_risk_level in ("high", "critical")


# ─────────────────────────────────────────────────────
# System 7: Global Risk Detector
# ─────────────────────────────────────────────────────

class TestGlobalRiskDetector:
    @pytest.mark.asyncio
    async def test_high_outcome_failure_rate_produces_signal(self, db):
        tenant, role = uuid4(), uuid4()
        for i in range(12):
            a = _accuracy(tenant, uuid4(), role,
                          predicted_conf=0.7, is_correct=i >= 10)
            a.predicted_outcome = "approved"
            db.add(a)
        await db.flush()

        detector = GlobalRiskDetector(db)
        signals = await detector.detect_signals(tenant)

        assert any(s.signal_type == "outcome_failure" for s in signals)

    @pytest.mark.asyncio
    async def test_systemic_overconfidence_signal(self, db):
        tenant, role = uuid4(), uuid4()
        for _ in range(25):
            a = _accuracy(tenant, uuid4(), role, predicted_conf=0.9, is_correct=False)
            db.add(a)
        await db.flush()

        detector = GlobalRiskDetector(db)
        signals = await detector.detect_signals(tenant)

        assert any(s.signal_name == "systemic_overconfidence" for s in signals)

    @pytest.mark.asyncio
    async def test_signals_are_tenant_isolated(self, db):
        t1, t2, role = uuid4(), uuid4(), uuid4()
        for _ in range(12):
            a = _accuracy(t1, uuid4(), role, predicted_conf=0.9, is_correct=False)
            a.predicted_outcome = "approved"
            db.add(a)
        await db.flush()

        detector = GlobalRiskDetector(db)
        await detector.detect_signals(t1)

        t2_signals = await detector.get_active_signals(t2)
        assert len(t2_signals) == 0
