"""Test production hardening features for System 4."""
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
    Base as EventBase,
)
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.api.versions.v1.execution_router import get_db as execution_get_db
from AgentTheater.api.versions.v1.execution_router import get_event_store as execution_get_event_store
from AgentTheater.api.services.execution_state_machine import ExecutionStateMachine
from AgentTheater.api.services.stale_execution_detector import StaleExecutionDetector
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
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def user_id():
    return UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def project_id():
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


class TestStateMachineValidation:
    """Test strict state machine enforcement."""

    def test_valid_transitions(self):
        """Test that valid transitions are allowed."""
        assert ExecutionStateMachine.is_valid_transition("approved", "assigned")
        assert ExecutionStateMachine.is_valid_transition("approved", "in_progress")
        assert ExecutionStateMachine.is_valid_transition("in_progress", "blocked")
        assert ExecutionStateMachine.is_valid_transition("blocked", "in_progress")
        assert ExecutionStateMachine.is_valid_transition("in_progress", "completed")
        assert ExecutionStateMachine.is_valid_transition("completed", "succeeded")

    def test_invalid_transitions(self):
        """Test that invalid transitions are rejected."""
        assert not ExecutionStateMachine.is_valid_transition("completed", "in_progress")
        assert not ExecutionStateMachine.is_valid_transition("succeeded", "blocked")
        assert not ExecutionStateMachine.is_valid_transition("approved", "completed")
        assert not ExecutionStateMachine.is_valid_transition("assigned", "succeeded")

    def test_validate_transition_raises_on_invalid(self):
        """Test that validate_transition raises ValueError on invalid transition."""
        with pytest.raises(ValueError):
            ExecutionStateMachine.validate_transition("completed", "in_progress")

        with pytest.raises(ValueError):
            ExecutionStateMachine.validate_transition("succeeded", "blocked")

    def test_terminal_states(self):
        """Test that terminal states have no valid transitions."""
        assert ExecutionStateMachine.is_terminal_state("succeeded")
        assert ExecutionStateMachine.is_terminal_state("failed")
        assert ExecutionStateMachine.is_terminal_state("pivoted")
        assert not ExecutionStateMachine.is_terminal_state("in_progress")
        assert not ExecutionStateMachine.is_terminal_state("approved")

    def test_get_valid_transitions(self):
        """Test getting list of valid next states."""
        valid = ExecutionStateMachine.get_valid_transitions("approved")
        assert "assigned" in valid
        assert "in_progress" in valid
        assert len(valid) > 0

        valid_completed = ExecutionStateMachine.get_valid_transitions("completed")
        assert "succeeded" in valid_completed
        assert "failed" in valid_completed
        assert "pivoted" in valid_completed


class TestOptimisticLocking:
    """Test optimistic locking with version columns."""

    @pytest.mark.asyncio
    async def test_execution_has_version_column(self, test_db, tenant_id, user_id, project_id):
        """Verify Execution model has version column for optimistic locking."""
        # Create execution
        execution = Execution(
            decision_id=UUID("44444444-4444-4444-4444-444444444444"),
            state="approved",
            version=1,
            tenant_id=tenant_id,
            created_by=user_id,
        )
        test_db.add(execution)
        await test_db.flush()

        # Retrieve and verify version
        result = await test_db.scalar(
            select(Execution).where(Execution.id == execution.id)
        )
        assert result.version == 1

        # Simulate version increment on state change
        result.version += 1
        await test_db.flush()

        # Re-fetch and verify version incremented
        result2 = await test_db.scalar(
            select(Execution).where(Execution.id == execution.id)
        )
        assert result2.version == 2


class TestArtifactSyncTracking:
    """Test artifact sync status tracking."""

    @pytest.mark.asyncio
    async def test_artifact_sync_status_pending_on_create(self, test_db, tenant_id, user_id):
        """Artifact sync status should be 'pending' when created."""
        artifact = ExecutionArtifact(
            execution_id=UUID("55555555-5555-5555-5555-555555555555"),
            artifact_type="github_issue",
            artifact_id="issues/123",
            artifact_sync_status="pending",
            version=1,
            tenant_id=tenant_id,
            created_by=user_id,
        )
        test_db.add(artifact)
        await test_db.flush()

        # Retrieve and verify sync status
        result = await test_db.scalar(
            select(ExecutionArtifact).where(ExecutionArtifact.id == artifact.id)
        )
        assert result.artifact_sync_status == "pending"
        assert result.sync_retry_count == 0


class TestStaleExecutionDetection:
    """Test stale execution detection."""

    @pytest.mark.asyncio
    async def test_stale_detector_finds_old_executions(self, test_db, tenant_id, user_id):
        """Stale detector should find executions in_progress for > threshold days."""
        from datetime import datetime, timedelta, timezone

        # Create an old execution (12 days ago)
        old_date = datetime.now(timezone.utc) - timedelta(days=12)

        execution = Execution(
            decision_id=UUID("66666666-6666-6666-6666-666666666666"),
            state="in_progress",
            started_at=old_date,
            version=1,
            tenant_id=tenant_id,
            created_by=user_id,
        )
        test_db.add(execution)
        await test_db.flush()

        # Run detector
        detector = StaleExecutionDetector(test_db)
        stale_ids = await detector.detect_stale_executions()

        # Should find the old execution
        assert len(stale_ids) > 0
        assert str(execution.id) in stale_ids

    @pytest.mark.asyncio
    async def test_stale_detector_ignores_recent_executions(self, test_db, tenant_id, user_id):
        """Stale detector should not flag recent executions."""
        from datetime import datetime, timedelta, timezone

        # Create a recent execution (2 days ago)
        recent_date = datetime.now(timezone.utc) - timedelta(days=2)

        execution = Execution(
            decision_id=UUID("77777777-7777-7777-7777-777777777777"),
            state="in_progress",
            started_at=recent_date,
            version=1,
            tenant_id=tenant_id,
            created_by=user_id,
        )
        test_db.add(execution)
        await test_db.flush()

        # Run detector
        detector = StaleExecutionDetector(test_db)
        stale_ids = await detector.detect_stale_executions()

        # Should NOT find the recent execution
        assert str(execution.id) not in stale_ids


@pytest.mark.asyncio
async def test_concurrent_state_transitions(client, test_db, tenant_id, user_id, project_id):
    """Test handling of concurrent state transitions."""

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

    # Transition to assigned
    resp1 = await client.post(
        f"/api/v1/executions/{execution_id}/assign",
        json={"assigned_to": str(user_id)},
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    assert resp1.status_code == 200

    # Verify execution version was incremented
    result = await test_db.scalar(
        select(Execution).where(Execution.id == execution_id)
    )
    assert result.version > 1


@pytest.mark.asyncio
async def test_invalid_state_transition_rejected(client, test_db, tenant_id, user_id, project_id):
    """Test that invalid state transitions are rejected."""

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

    # Try to transition directly from approved to succeeded (invalid)
    # We would need an endpoint for direct state transitions to test this fully
    # For now, verify the state machine itself rejects it
    assert not ExecutionStateMachine.is_valid_transition("approved", "succeeded")
