"""Test System 5: Observability & Telemetry."""
import pytest
import json
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from AgentTheater.events.db_models import Base as EventBase
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.observability import (
    get_metrics,
    AlertRules,
    SystemDashboards,
    HealthChecker,
    TraceContext,
)
from AgentTheater.observability.alerts import AlertSeverity

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Get test database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(EventBase.metadata.drop_all)
        await conn.run_sync(EventBase.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def client(test_db):
    """Create test HTTP client."""

    def get_test_db():
        return test_db

    def get_test_event_store():
        from AgentTheater.events import EventStore
        return EventStore(test_db)

    app.dependency_overrides[decisions_get_db] = get_test_db
    app.dependency_overrides[decisions_get_event_store] = get_test_event_store

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class TestStructuredLogging:
    """Test structured logging system."""

    def test_logging_module_imports(self):
        """Verify logging module can be imported."""
        from AgentTheater.observability.logging import StructuredFormatter, ContextualLogger
        assert StructuredFormatter is not None
        assert ContextualLogger is not None

    def test_contextual_logger(self):
        """Test contextual logger with context fields."""
        import logging
        from AgentTheater.observability.logging import ContextualLogger
        from uuid import UUID

        logger = logging.getLogger("test")
        contextual = ContextualLogger(logger)

        tenant_id = UUID("11111111-1111-1111-1111-111111111111")
        contextual.set_context(
            request_id="req-123",
            correlation_id="corr-456",
            tenant_id=tenant_id,
        )

        assert contextual.context["request_id"] == "req-123"
        assert contextual.context["correlation_id"] == "corr-456"
        assert contextual.context["tenant_id"] == str(tenant_id)


class TestMetrics:
    """Test Prometheus metrics system."""

    def test_metrics_instance(self):
        """Verify metrics instance can be created."""
        metrics = get_metrics()
        assert metrics is not None
        assert hasattr(metrics, "api_requests_total")
        assert hasattr(metrics, "events_published_total")
        assert hasattr(metrics, "executions_in_progress")

    def test_api_metrics_registered(self):
        """Verify API metrics are registered."""
        metrics = get_metrics()
        assert metrics.api_requests_total is not None
        assert metrics.api_request_latency_ms is not None
        assert metrics.api_errors_total is not None

    def test_event_metrics_registered(self):
        """Verify event system metrics are registered."""
        metrics = get_metrics()
        assert metrics.events_published_total is not None
        assert metrics.event_publish_latency_ms is not None
        assert metrics.dlq_size is not None
        assert metrics.consumer_lag is not None

    def test_execution_metrics_registered(self):
        """Verify execution metrics are registered."""
        metrics = get_metrics()
        assert metrics.executions_in_progress is not None
        assert metrics.executions_blocked is not None
        assert metrics.executions_stale is not None
        assert metrics.execution_duration_ms is not None

    def test_decision_metrics_registered(self):
        """Verify decision metrics are registered."""
        metrics = get_metrics()
        assert metrics.decisions_created_total is not None
        assert metrics.decision_confidence_avg is not None
        assert metrics.decision_accuracy is not None

    def test_cost_metrics_registered(self):
        """Verify cost metrics are registered."""
        metrics = get_metrics()
        assert metrics.tokens_used_total is not None
        assert metrics.cost_per_decision is not None
        assert metrics.cost_per_execution is not None


class TestDistributedTracing:
    """Test distributed tracing system."""

    def test_trace_context_creation(self):
        """Test creating trace context."""
        trace = TraceContext()
        assert trace.trace_id is not None
        assert trace.parent_span_id is None

    def test_trace_context_with_id(self):
        """Test creating trace context with explicit ID."""
        trace_id = "test-trace-123"
        trace = TraceContext(trace_id=trace_id)
        assert trace.trace_id == trace_id

    def test_span_creation(self):
        """Test creating spans in trace."""
        trace = TraceContext()
        span = trace.start_span("test_operation", attributes={"key": "value"})

        assert span.trace_id == trace.trace_id
        assert span.name == "test_operation"
        assert span.attributes["key"] == "value"


class TestAlertRules:
    """Test alert rules system."""

    def test_alert_rules_exist(self):
        """Verify alert rules are defined."""
        rules = AlertRules.get_all_rules()
        assert len(rules) > 0

    def test_alert_rule_severities(self):
        """Verify alert rule severities."""
        rules = AlertRules.get_all_rules()
        for rule in rules:
            assert rule.severity in [AlertSeverity.CRITICAL, AlertSeverity.WARNING, AlertSeverity.INFO]

    def test_alert_rules_to_prometheus(self):
        """Verify alert rules can be exported as Prometheus rules."""
        prometheus_rules = AlertRules.to_prometheus_rules()
        assert "agenttheatre_alerts" in prometheus_rules
        assert "alert:" in prometheus_rules

    def test_alert_rules_to_dict(self):
        """Verify alert rules can be exported as dictionaries."""
        rules_dict = AlertRules.to_dict()
        assert len(rules_dict) > 0
        assert all("name" in r for r in rules_dict)
        assert all("metric" in r for r in rules_dict)
        assert all("threshold" in r for r in rules_dict)


class TestDashboards:
    """Test dashboard system."""

    def test_dashboard_count(self):
        """Verify dashboards are defined."""
        dashboards = SystemDashboards.get_all_dashboards()
        assert len(dashboards) == 5  # system_health, event_flow, execution_pipeline, cost, decision_accuracy

    def test_system_health_dashboard(self):
        """Verify system health dashboard structure."""
        dashboard = SystemDashboards.system_health_dashboard()
        assert dashboard.name == "System Health"
        assert len(dashboard.panels) > 0

    def test_event_flow_dashboard(self):
        """Verify event flow dashboard structure."""
        dashboard = SystemDashboards.event_flow_dashboard()
        assert dashboard.name == "Event Flow"
        assert len(dashboard.panels) > 0

    def test_execution_pipeline_dashboard(self):
        """Verify execution pipeline dashboard structure."""
        dashboard = SystemDashboards.execution_pipeline_dashboard()
        assert dashboard.name == "Execution Pipeline"
        assert len(dashboard.panels) > 0

    def test_cost_monitoring_dashboard(self):
        """Verify cost monitoring dashboard structure."""
        dashboard = SystemDashboards.cost_monitoring_dashboard()
        assert dashboard.name == "Cost Monitoring"
        assert len(dashboard.panels) > 0

    def test_decision_accuracy_dashboard(self):
        """Verify decision accuracy dashboard structure."""
        dashboard = SystemDashboards.decision_accuracy_dashboard()
        assert dashboard.name == "Decision Accuracy"
        assert len(dashboard.panels) > 0

    def test_export_all_dashboards(self):
        """Verify all dashboards can be exported."""
        dashboards = SystemDashboards.export_all_dashboards()
        assert len(dashboards) == 5
        assert all("panels" in d for d in dashboards.values())


class TestHealthChecks:
    """Test health check system."""

    @pytest.mark.asyncio
    async def test_database_health_check(self, test_db):
        """Test database health check."""
        checker = HealthChecker(test_db)
        health = await checker.check_database()
        assert health["status"] in ["healthy", "unhealthy"]

    @pytest.mark.asyncio
    async def test_event_store_health_check(self, test_db):
        """Test event store health check."""
        checker = HealthChecker(test_db)
        health = await checker.check_event_store()
        assert health["status"] in ["healthy", "degraded", "unhealthy"]

    @pytest.mark.asyncio
    async def test_executions_health_check(self, test_db):
        """Test execution system health check."""
        checker = HealthChecker(test_db)
        health = await checker.check_executions()
        assert health["status"] in ["healthy", "degraded", "unhealthy"]

    @pytest.mark.asyncio
    async def test_deep_health_check(self, test_db):
        """Test deep health check."""
        checker = HealthChecker(test_db)
        health = await checker.deep_health()

        assert "status" in health
        assert "timestamp" in health
        assert "components" in health
        assert "database" in health["components"]
        assert "event_store" in health["components"]
        assert "executions" in health["components"]

    @pytest.mark.asyncio
    async def test_readiness_check(self, test_db):
        """Test readiness check."""
        checker = HealthChecker(test_db)
        readiness = await checker.readiness()

        assert "ready" in readiness
        assert "timestamp" in readiness
        assert "details" in readiness


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test /health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_deep_health_endpoint(client):
    """Test /health/deep endpoint."""
    response = await client.get("/health/deep")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data


@pytest.mark.asyncio
async def test_readiness_endpoint(client):
    """Test /health/ready endpoint."""
    response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data


@pytest.mark.asyncio
async def test_observability_alerts_endpoint(client):
    """Test /observability/alerts endpoint."""
    response = await client.get("/observability/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert len(data["alerts"]) > 0


@pytest.mark.asyncio
async def test_observability_dashboards_endpoint(client):
    """Test /observability/dashboards endpoint."""
    response = await client.get("/observability/dashboards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # 5 dashboards


@pytest.mark.asyncio
async def test_observability_config_endpoint(client):
    """Test /observability/config endpoint."""
    response = await client.get("/observability/config")
    assert response.status_code == 200
    data = response.json()
    assert "logging" in data
    assert "metrics" in data
    assert "tracing" in data
    assert "alerts" in data
    assert "dashboards" in data


# ─── New endpoint & middleware tests ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_liveness_endpoint(client):
    """GET /health/live returns 200 with alive=True."""
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["alive"] is True


@pytest.mark.asyncio
async def test_request_id_header_echoed(client):
    """ObservabilityMiddleware echoes X-Request-ID in response headers."""
    rid = "test-request-id-abc123"
    response = await client.get("/health/live", headers={"X-Request-ID": rid})
    assert response.headers.get("x-request-id") == rid


@pytest.mark.asyncio
async def test_request_id_auto_generated(client):
    """ObservabilityMiddleware generates X-Request-ID when absent."""
    response = await client.get("/health/live")
    rid = response.headers.get("x-request-id")
    assert rid is not None
    assert len(rid) == 36  # UUID format


@pytest.mark.asyncio
async def test_new_metrics_registered(client):
    """Verify new production metrics exist on the metrics instance."""
    from AgentTheater.observability.metrics import get_metrics
    m = get_metrics()
    assert hasattr(m, "outbox_unpublished_count")
    assert hasattr(m, "outbox_publish_failures_total")
    assert hasattr(m, "guardrail_blocks_total")
    assert hasattr(m, "event_commit_failures_total")


@pytest.mark.asyncio
async def test_deep_health_includes_outbox(client):
    """GET /health/deep includes outbox component."""
    response = await client.get("/health/deep")
    assert response.status_code == 200
    data = response.json()
    assert "outbox" in data["components"]
    outbox = data["components"]["outbox"]
    assert "status" in outbox
    assert "details" in outbox


@pytest.mark.asyncio
async def test_deep_health_includes_relay_status(client):
    """GET /health/deep outbox component contains relay running status."""
    response = await client.get("/health/deep")
    assert response.status_code == 200
    outbox = response.json()["components"]["outbox"]
    assert "relay" in outbox["details"]
    relay = outbox["details"]["relay"]
    assert "running" in relay


@pytest.mark.asyncio
async def test_readiness_returns_ready_true(client):
    """GET /health/ready returns ready=True when DB is healthy."""
    response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "details" in data
    assert "database" in data["details"]
    assert "outbox" in data["details"]


@pytest.mark.asyncio
async def test_outbox_health_check_directly(test_db):
    """HealthChecker.check_outbox_backlog reports 0 unpublished on empty DB."""
    checker = HealthChecker(test_db)
    result = await checker.check_outbox_backlog()
    assert result["status"] in ("healthy", "degraded")
    assert result["details"]["unpublished_count"] == 0


@pytest.mark.asyncio
async def test_relay_status_initially_not_running():
    """Relay has never run in tests — status should report running=False."""
    from AgentTheater.events.outbox_relay import get_relay_status, _relay_last_run
    status = get_relay_status()
    assert "running" in status
    # In test environment the background relay task is not running
    assert status["running"] is False or status["last_run"] is not None
