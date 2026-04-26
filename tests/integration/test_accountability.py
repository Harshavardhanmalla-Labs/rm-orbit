"""Test System 3: Decision Accountability engine."""
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
    EventOutbox,
    EventLog,
    Decision,
    DecisionRationale,
    DecisionConfidence,
    RiskAssessment,
    DecisionStateHistory,
    Base as EventBase,
)
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.api.versions.v1.accountability_router import get_db as accountability_get_db
from AgentTheater.api.versions.v1.accountability_router import get_event_store as accountability_get_event_store
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
    app.dependency_overrides[accountability_get_db] = get_test_db
    app.dependency_overrides[accountability_get_event_store] = get_test_event_store

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
async def test_add_rationale_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions/{id}/rationale emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision first
    create_response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot or persevere?",
            "roles": ["ceo", "cto"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_response.json()["id"])

    # Add rationale
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/rationale",
        json={
            "role": "ceo",
            "reasoning": "Based on market research and competitor analysis, we should pivot.",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-rationale-123",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "ceo"
    assert data["reasoning"] == "Based on market research and competitor analysis, we should pivot."

    # Verify rationale in DB
    result = await test_db.execute(
        select(DecisionRationale).where(DecisionRationale.decision_id == decision_id)
    )
    rationale = result.scalar_one()
    assert rationale.role == "ceo"

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            EventLog.aggregate_id == decision_id,
            EventLog.event_type == "decision.rationale_added"
        )
    )
    event = result.scalar_one()
    assert event.tenant_id == tenant_id


@pytest.mark.asyncio
async def test_score_confidence_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions/{id}/confidence emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_response = await client.post(
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
    decision_id = UUID(create_response.json()["id"])

    # Score confidence
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/confidence",
        json={
            "technical_confidence": 85.0,
            "market_confidence": 70.0,
            "team_confidence": 90.0,
            "reasoning": "Team is capable, market shows promise",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-confidence-456",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["technical_confidence"] == 85.0
    assert data["overall_confidence"] == pytest.approx((85 + 70 + 90) / 3, 0.1)

    # Verify confidence in DB
    result = await test_db.execute(
        select(DecisionConfidence).where(DecisionConfidence.decision_id == decision_id)
    )
    confidence = result.scalar_one()
    assert confidence.technical_confidence == 85.0

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == decision_id) &
            (EventLog.event_type == "decision.confidence_scored")
        )
    )
    event = result.scalar_one()
    assert event.data["technical_confidence"] == 85.0


@pytest.mark.asyncio
async def test_assess_risk_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions/{id}/risk emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_response = await client.post(
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
    decision_id = UUID(create_response.json()["id"])

    # Assess risk
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/risk",
        json={
            "technical_risk": 3.0,
            "market_risk": 5.0,
            "financial_risk": 4.0,
            "team_risk": 2.0,
            "contingency": "Have backup plan if pivot fails",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-risk-789",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["technical_risk"] == 3.0
    assert data["overall_risk"] == pytest.approx((3 + 5 + 4 + 2) / 4, 0.1)

    # Verify assessment in DB
    result = await test_db.execute(
        select(RiskAssessment).where(RiskAssessment.decision_id == decision_id)
    )
    assessment = result.scalar_one()
    assert assessment.technical_risk == 3.0

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == decision_id) &
            (EventLog.event_type == "decision.risk_assessed")
        )
    )
    event = result.scalar_one()
    assert event.data["overall_risk"] == pytest.approx(3.5, 0.1)


@pytest.mark.asyncio
async def test_state_transition_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions/{id}/state transitions state and emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    create_response = await client.post(
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
    decision_id = UUID(create_response.json()["id"])

    # Transition state
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/state",
        json={
            "to_state": "execution",
            "reason": "All stakeholders approved",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-state-999",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["to_state"] == "execution"

    # Verify state history in DB
    result = await test_db.execute(
        select(DecisionStateHistory).where(DecisionStateHistory.decision_id == decision_id)
    )
    history = result.scalar_one()
    assert history.to_state == "execution"

    # Verify event emitted
    result = await test_db.execute(
        select(EventLog).where(
            (EventLog.aggregate_id == decision_id) &
            (EventLog.event_type == "decision.state_transitioned")
        )
    )
    event = result.scalar_one()
    assert event.data["to_state"] == "execution"


