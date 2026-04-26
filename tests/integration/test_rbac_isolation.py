"""Tenant isolation and RBAC audit — every cross-tenant or unauthenticated access must be denied."""
import pytest
import os
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from AgentTheater.events.db_models import Base as EventBase
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.api.versions.v1.accountability_router import get_db as accountability_get_db
from AgentTheater.api.versions.v1.accountability_router import get_event_store as accountability_get_event_store
from AgentTheater.api.versions.v1.execution_router import get_db as execution_get_db
from AgentTheater.api.versions.v1.execution_router import get_event_store as execution_get_event_store
from AgentTheater.events import EventStore

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
pytest_plugins = ('pytest_asyncio',)

_JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production-key!")


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(EventBase.metadata.drop_all)
        await conn.run_sync(EventBase.metadata.create_all)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def client(test_db):
    def get_test_db():
        return test_db

    def get_test_event_store():
        return EventStore(test_db)

    app.dependency_overrides[decisions_get_db] = get_test_db
    app.dependency_overrides[decisions_get_event_store] = get_test_event_store
    app.dependency_overrides[accountability_get_db] = get_test_db
    app.dependency_overrides[accountability_get_event_store] = get_test_event_store
    app.dependency_overrides[execution_get_db] = get_test_db
    app.dependency_overrides[execution_get_event_store] = get_test_event_store

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


def make_token(user_id: UUID, tenant_id: UUID, roles=None, secret=_JWT_SECRET, exp_delta=timedelta(hours=1)):
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "roles": roles or ["operator"],
        "exp": datetime.now(timezone.utc) + exp_delta,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


# ─── Fixtures ────────────────────────────────────────────────────────────────
TENANT_A = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
TENANT_B = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
USER_A = UUID("11111111-1111-1111-1111-111111111111")
USER_B = UUID("22222222-2222-2222-2222-222222222222")
PROJECT_A = UUID("33333333-3333-3333-3333-333333333333")


# ─── Auth failure tests ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_missing_auth_header_returns_401(client):
    """No Authorization header → 401."""
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_forged_jwt_returns_401(client):
    """JWT signed with wrong secret → 401."""
    token = make_token(USER_A, TENANT_A, secret="wrong-secret-that-is-definitely-not-valid!")
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
        headers={"Authorization": f"Bearer {token}", "X-Tenant-ID": str(TENANT_A)},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expired_jwt_returns_401(client):
    """Expired JWT → 401."""
    token = make_token(USER_A, TENANT_A, exp_delta=timedelta(seconds=-1))
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
        headers={"Authorization": f"Bearer {token}", "X-Tenant-ID": str(TENANT_A)},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_tenant_header_mismatch_returns_401(client):
    """X-Tenant-ID header ≠ token tenant_id → 401."""
    token = make_token(USER_A, TENANT_A)
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(TENANT_B),  # mismatch
        },
    )
    assert response.status_code == 401


# ─── Cross-tenant isolation tests ────────────────────────────────────────────

async def _create_decision(client, tenant_id: UUID, user_id: UUID) -> UUID:
    """Helper: create a decision for tenant and return its ID."""
    token = make_token(user_id, tenant_id)
    resp = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market this year?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={"Authorization": f"Bearer {token}", "X-Tenant-ID": str(tenant_id)},
    )
    assert resp.status_code == 201, resp.text
    return UUID(resp.json()["id"])


@pytest.mark.asyncio
async def test_cross_tenant_get_decision_denied(client):
    """Tenant B cannot read Tenant A's decision."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.get(
        f"/api/v1/decisions/{decision_id}",
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_tenant_record_outcome_denied(client):
    """Tenant B cannot record outcome on Tenant A's decision."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/outcome",
        json={"outcome": "succeeded"},
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_tenant_add_rationale_denied(client):
    """Tenant B cannot add rationale to Tenant A's decision."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/rationale",
        json={"role": "ceo", "reasoning": "This is a cross-tenant attack attempt."},
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_tenant_score_confidence_denied(client):
    """Tenant B cannot score confidence on Tenant A's decision."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/confidence",
        json={"technical_confidence": 80, "market_confidence": 80, "team_confidence": 80},
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_tenant_assess_risk_denied(client):
    """Tenant B cannot assess risk on Tenant A's decision."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/risk",
        json={
            "technical_risk": 3.0,
            "market_risk": 3.0,
            "financial_risk": 3.0,
            "team_risk": 3.0,
        },
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_tenant_read_model_denied(client):
    """Tenant B cannot read Tenant A's decision read model."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)

    token_b = make_token(USER_B, TENANT_B)
    response = await client.get(
        f"/api/v1/decisions/{decision_id}/read-model",
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code in (403, 404)


@pytest.mark.asyncio
async def test_list_decisions_scoped_to_tenant(client):
    """list_decisions returns ONLY the caller's tenant decisions."""
    # Tenant A creates a decision
    token_a = make_token(USER_A, TENANT_A)
    await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we expand to APAC market this year?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
        headers={"Authorization": f"Bearer {token_a}", "X-Tenant-ID": str(TENANT_A)},
    )

    # Tenant B lists — must see 0 decisions (no cross-leak)
    token_b = make_token(USER_B, TENANT_B)
    response = await client.get(
        "/api/v1/decisions",
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_execution_cross_tenant_denied(client):
    """Tenant B cannot assign Tenant A's execution."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)
    token_a = make_token(USER_A, TENANT_A)

    exec_resp = await client.post(
        "/api/v1/executions",
        json={"decision_id": str(decision_id), "predicted_outcome": "succeeded"},
        headers={"Authorization": f"Bearer {token_a}", "X-Tenant-ID": str(TENANT_A)},
    )
    execution_id = exec_resp.json()["id"]

    token_b = make_token(USER_B, TENANT_B)
    response = await client.post(
        f"/api/v1/executions/{execution_id}/assign",
        json={"assigned_to": str(USER_B)},
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_execution_cross_tenant_dashboard_denied(client):
    """Tenant B cannot view Tenant A's execution dashboard."""
    decision_id = await _create_decision(client, TENANT_A, USER_A)
    token_a = make_token(USER_A, TENANT_A)

    exec_resp = await client.post(
        "/api/v1/executions",
        json={"decision_id": str(decision_id), "predicted_outcome": "succeeded"},
        headers={"Authorization": f"Bearer {token_a}", "X-Tenant-ID": str(TENANT_A)},
    )
    execution_id = exec_resp.json()["id"]

    token_b = make_token(USER_B, TENANT_B)
    response = await client.get(
        f"/api/v1/executions/{execution_id}/dashboard",
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_models_list_scoped_to_tenant(client):
    """GET /decisions/read-models returns only the caller's tenant read models."""
    # Tenant A creates a decision (read model auto-projected)
    token_a = make_token(USER_A, TENANT_A)
    await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(PROJECT_A),
            "question": "Should we invest in enterprise sales?",
            "roles": ["ceo"],
            "tenant_id": str(TENANT_A),
        },
        headers={"Authorization": f"Bearer {token_a}", "X-Tenant-ID": str(TENANT_A)},
    )

    # Tenant B lists read models — must get 0
    token_b = make_token(USER_B, TENANT_B)
    response = await client.get(
        "/api/v1/decisions/read-models",
        headers={"Authorization": f"Bearer {token_b}", "X-Tenant-ID": str(TENANT_B)},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
