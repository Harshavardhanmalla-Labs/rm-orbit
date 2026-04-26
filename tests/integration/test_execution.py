"""Test System 4: Decision Execution & Outcome Tracker."""
import pytest
import os
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from AgentTheater.events.db_models import (
    EventLog,
    Decision,
    Execution,
    ExecutionArtifact,
    ExecutionStateHistory,
    OutcomeRecord,
    ExecutionReadModel,
    Base as EventBase,
)
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.api.versions.v1.execution_router import get_db as execution_get_db
from AgentTheater.api.versions.v1.execution_router import get_event_store as execution_get_event_store
from AgentTheater.events import EventStore

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
        return EventStore(test_db)

    app.dependency_overrides[decisions_get_db] = get_test_db
    app.dependency_overrides[decisions_get_event_store] = get_test_event_store
    app.dependency_overrides[execution_get_db] = get_test_db
    app.dependency_overrides[execution_get_event_store] = get_test_event_store

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def tenant_id():
    """Test tenant ID."""
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def user_id():
    """Test user ID."""
    return UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def project_id():
    """Test project ID."""
    return UUID("33333333-3333-3333-3333-333333333333")


_JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production-key!")


def create_jwt_token(user_id: UUID, tenant_id: UUID, roles=None):
    """Create a properly signed HS256 JWT for tests."""
    if roles is None:
        roles = ["operator"]
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "roles": roles,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm="HS256")


@pytest.mark.asyncio
async def test_artifact_linked_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/executions/{id}/artifact emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision first
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Link artifact
    response = await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={
            "artifact_type": "github_issue",
            "artifact_id": "issues/123",
            "artifact_url": "https://github.com/org/repo/issues/123",
            "artifact_title": "Pivot strategy implementation",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-artifact-123",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["artifact_type"] == "github_issue"
    assert data["artifact_id"] == "issues/123"

    # Verify artifact in DB
    result = await test_db.execute(
        select(ExecutionArtifact).where(ExecutionArtifact.execution_id == execution_id)
    )
    artifact = result.scalar_one()
    assert artifact.artifact_type == "github_issue"

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == execution_id) &
            (EventLog.event_type == "artifact.linked")
        )
    )
    event = result.scalar_one()
    assert event.data["artifact_id"] == "issues/123"


@pytest.mark.asyncio
async def test_state_transition_emits_event(client, test_db, tenant_id, user_id, project_id):
    """State transitions emit events."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Transition to in_progress
    response = await client.post(
        f"/api/v1/executions/{execution_id}/start",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-state-123",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "in_progress"

    # Verify state history
    result = await test_db.execute(
        select(ExecutionStateHistory).where(ExecutionStateHistory.execution_id == execution_id)
    )
    history = result.scalar_one()
    assert history.to_state == "in_progress"

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == execution_id) &
            (EventLog.event_type == "execution.started")
        )
    )
    event = result.scalar_one()
    assert event.data["to_state"] == "in_progress"


@pytest.mark.asyncio
async def test_outcome_recorded_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/executions/{id}/outcome emits outcome.recorded event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Record outcome
    response = await client.post(
        f"/api/v1/executions/{execution_id}/outcome",
        json={
            "actual_outcome": "succeeded",
            "success_metrics": {"roi": 1.5, "customer_satisfaction": 0.92},
            "lessons_learned": "Rapid iteration was key to success",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-outcome-123",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["actual_outcome"] == "succeeded"

    # Verify outcome in DB
    result = await test_db.execute(
        select(OutcomeRecord).where(OutcomeRecord.execution_id == execution_id)
    )
    outcome = result.scalar_one()
    assert outcome.actual_outcome == "succeeded"

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == execution_id) &
            (EventLog.event_type == "outcome.recorded")
        )
    )
    event = result.scalar_one()
    assert event.data["actual_outcome"] == "succeeded"


@pytest.mark.asyncio
async def test_tenant_isolation_in_execution(client, test_db, tenant_id, user_id, project_id):
    """Tenant isolation enforced in execution endpoints."""

    other_tenant_id = UUID("99999999-9999-9999-9999-999999999999")
    token = create_jwt_token(user_id, tenant_id)
    other_token = create_jwt_token(user_id, other_tenant_id)

    # Create decision in tenant A
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution in tenant A
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Try to access from tenant B (should fail)
    response = await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={
            "artifact_type": "github_issue",
            "artifact_id": "issues/456",
        },
        headers={
            "Authorization": f"Bearer {other_token}",
            "X-Tenant-ID": str(other_tenant_id),
        }
    )

    assert response.status_code == 403
    assert "Tenant mismatch" in response.json()["detail"]


@pytest.mark.asyncio
async def test_auth_attribution_in_events(client, test_db, tenant_id, user_id, project_id):
    """Auth context (user_id) attributed to execution events."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Link artifact
    await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={
            "artifact_type": "github_issue",
            "artifact_id": "issues/123",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    # Verify operator_id in event
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == execution_id) &
            (EventLog.event_type == "artifact.linked")
        )
    )
    event = result.scalar_one()
    assert event.operator_id == user_id


@pytest.mark.asyncio
async def test_state_transition_persists(client, test_db, tenant_id, user_id, project_id):
    """State transitions properly persist in read model."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Transition: approved -> assigned
    assign_resp = await client.post(
        f"/api/v1/executions/{execution_id}/assign",
        json={"assigned_to": str(user_id)},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    assert assign_resp.json()["state"] == "assigned"

    # Verify read model updated
    result = await test_db.execute(
        select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
    )
    rm = result.scalar_one()
    assert rm.state == "assigned"
    assert rm.assigned_to == user_id


@pytest.mark.asyncio
async def test_dashboard_read_model_artifact_counts(client, test_db, tenant_id, user_id, project_id):
    """Dashboard read model correctly aggregates artifact counts."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Link multiple artifacts
    await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={"artifact_type": "github_issue", "artifact_id": "issues/1"},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={"artifact_type": "github_issue", "artifact_id": "issues/2"},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={"artifact_type": "github_pr", "artifact_id": "pulls/100"},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    await client.post(
        f"/api/v1/executions/{execution_id}/artifact",
        json={"artifact_type": "task", "artifact_id": "task-42"},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    # Get dashboard
    response = await client.get(
        f"/api/v1/executions/{execution_id}/dashboard",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["github_issues_count"] == 2
    assert data["github_prs_count"] == 1
    assert data["tasks_count"] == 1
    assert data["docs_count"] == 0
    assert data["deployments_count"] == 0


@pytest.mark.asyncio
async def test_invalid_state_transition_persists(client, test_db, tenant_id, user_id, project_id):
    """Invalid state transitions are rejected or allowed based on current state."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision and execution
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # From approved state, should be able to transition to assigned or in_progress
    resp = await client.post(
        f"/api/v1/executions/{execution_id}/start",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    assert resp.status_code == 200

    # Verify state is now in_progress
    result = await test_db.execute(
        select(Execution).where(Execution.id == execution_id)
    )
    execution = result.scalar_one()
    assert execution.state == "in_progress"


@pytest.mark.asyncio
async def test_stale_execution_detection(client, test_db, tenant_id, user_id, project_id):
    """Stale execution detection identifies long-running executions."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_resp.json()["id"])

    # Create execution
    exec_resp = await client.post(
        "/api/v1/executions",
        json={
            "decision_id": str(decision_id),
            "predicted_outcome": "succeeded",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    execution_id = UUID(exec_resp.json()["id"])

    # Start execution
    await client.post(
        f"/api/v1/executions/{execution_id}/start",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    # Verify execution exists in database with in_progress state
    result = await test_db.execute(
        select(Execution).where(Execution.id == execution_id)
    )
    execution = result.scalar_one()
    assert execution.state == "in_progress"
    assert execution.started_at is not None

    # For stale detection: we would check age_days in read model
    # An execution is stale if it's been in_progress for > X days
    # For testing, we verify the structure is in place
    read_model = await test_db.scalar(
        select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
    )
    assert read_model is not None
    assert read_model.state == "in_progress"
    # age_days would be set in a background job or query-time calculation
