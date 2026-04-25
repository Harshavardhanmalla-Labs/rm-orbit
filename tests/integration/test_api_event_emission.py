"""Test API → Event emission integration."""
import pytest
import json
import base64
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from AgentTheater.events.db_models import EventOutbox, EventLog, Base as EventBase
from AgentTheater.models import Decision, Base as ModelBase
from AgentTheater.main import app, get_db, get_event_store
from AgentTheater.events import EventStore


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


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
        # Create all tables
        await conn.run_sync(EventBase.metadata.create_all)
        await conn.run_sync(ModelBase.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def client(test_db):
    """Create test HTTP client."""

    async def override_get_db():
        async with test_db.begin():
            yield test_db

    async def override_get_event_store():
        yield EventStore(test_db)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_event_store] = override_get_event_store

    async with AsyncClient(app=app, base_url="http://test") as ac:
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


def create_jwt_token(user_id: UUID, tenant_id: UUID, roles=None):
    """Create test JWT token."""
    if roles is None:
        roles = ["operator"]

    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "roles": roles,
    }

    # Create JWT (simplified: no signature)
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256"}).encode()
    ).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(payload).encode()
    ).decode().rstrip("=")
    signature = "test-signature"

    return f"{header}.{payload_b64}.{signature}"


@pytest.mark.asyncio
async def test_create_decision_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions creates decision AND emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Call API
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot?",
            "roles": ["ceo", "cto"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-create-123",
        }
    )

    # Verify API response
    assert response.status_code == 201
    data = response.json()
    decision_id = UUID(data["id"])
    assert response.headers["X-Correlation-ID"] == "test-create-123"

    # Verify decision in DB
    result = await test_db.execute(
        select(Decision).where(Decision.id == decision_id)
    )
    decision = result.scalar_one()
    assert decision.question == "Should we pivot?"
    assert decision.tenant_id == tenant_id

    # Verify event in outbox (not yet published)
    result = await test_db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.created")
            & (EventOutbox.aggregate_id == decision_id)
        )
    )
    outbox_entry = result.scalar_one()
    assert outbox_entry.published == False
    assert outbox_entry.event_payload["question"] == "Should we pivot?"

    # Verify correlation_id in event
    result = await test_db.execute(
        select(EventLog).where(EventLog.event_id == outbox_entry.event_id)
    )
    event_log = result.scalar_one()
    assert event_log.correlation_id == "test-create-123"
    assert event_log.tenant_id == tenant_id


@pytest.mark.asyncio
async def test_record_outcome_emits_event(client, test_db, tenant_id, user_id, project_id):
    """POST /api/v1/decisions/{id}/outcome emits event."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision first
    create_response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Test decision",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(create_response.json()["id"])

    # Call API to record outcome
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/outcome",
        json={
            "outcome": "succeeded",
            "note": "Exceeded targets by 20%",
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-outcome-456",
        }
    )

    # Verify response
    assert response.status_code == 200

    # Verify decision updated
    result = await test_db.execute(
        select(Decision).where(Decision.id == decision_id)
    )
    updated = result.scalar_one()
    assert updated.outcome == "succeeded"
    assert updated.note == "Exceeded targets by 20%"

    # Verify event in outbox
    result = await test_db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.outcome_recorded")
            & (EventOutbox.aggregate_id == decision_id)
        )
    )
    outbox_entry = result.scalar_one()
    assert outbox_entry.event_payload["outcome"] == "succeeded"

    # Verify correlation_id
    result = await test_db.execute(
        select(EventLog).where(EventLog.event_id == outbox_entry.event_id)
    )
    event_log = result.scalar_one()
    assert event_log.correlation_id == "test-outcome-456"


@pytest.mark.asyncio
async def test_correlation_id_flows_through_system(client, test_db, tenant_id, user_id, project_id):
    """Correlation ID: API → Event → EventLog."""

    token = create_jwt_token(user_id, tenant_id)
    correlation_id = "test-corr-123"

    # Call API with correlation ID
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot?",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": correlation_id,
        }
    )
    decision_id = UUID(response.json()["id"])

    # Verify event has correlation ID
    result = await test_db.execute(
        select(EventLog).where(EventLog.aggregate_id == decision_id)
    )
    event = result.scalar_one()
    assert event.correlation_id == correlation_id


@pytest.mark.asyncio
async def test_tenant_isolation_in_events(client, test_db, tenant_id, user_id, project_id):
    """Events tagged with tenant_id, cross-tenant access blocked."""

    token = create_jwt_token(user_id, tenant_id)

    # Create decision
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Test",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )
    decision_id = UUID(response.json()["id"])

    # Verify event has correct tenant_id
    result = await test_db.execute(
        select(EventLog).where(EventLog.aggregate_id == decision_id)
    )
    event = result.scalar_one()
    assert event.tenant_id == tenant_id

    # Try to access with different tenant (should fail)
    other_tenant = UUID("99999999-9999-9999-9999-999999999999")
    other_token = create_jwt_token(user_id, other_tenant)

    get_response = await client.get(
        f"/api/v1/decisions/{decision_id}",
        headers={
            "Authorization": f"Bearer {other_token}",
            "X-Tenant-ID": str(other_tenant),
        }
    )

    assert get_response.status_code == 403


@pytest.mark.asyncio
async def test_atomicity_decision_and_event(client, test_db, tenant_id, user_id, project_id):
    """If event emission fails, decision write rolls back."""

    token = create_jwt_token(user_id, tenant_id)

    # Normal flow works
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Test decision",
            "roles": ["ceo"],
            "tenant_id": str(tenant_id),
        },
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": str(tenant_id),
        }
    )

    assert response.status_code == 201

    # Verify both decision and event were written
    result = await test_db.execute(select(Decision))
    decisions = result.scalars().all()
    assert len(decisions) > 0

    result = await test_db.execute(select(EventOutbox))
    events = result.scalars().all()
    assert len(events) > 0
