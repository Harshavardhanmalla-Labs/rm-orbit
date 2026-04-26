"""Tests for critical production fixes: JWT security, atomic sequences, outbox relay, optimistic locking."""
from __future__ import annotations

import os
import asyncio
import pytest
import jwt
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from AgentTheater.events.db_models import (
    Base,
    EventOutbox,
    EventLog,
    AggregateSequence,
    Decision,
    Execution,
)
from AgentTheater.events.ledger import EventLedger, DomainEvent
from AgentTheater.events.outbox_relay import OutboxRelay
from AgentTheater.main import app
from AgentTheater.api.versions.v1.decisions_router import get_db as decisions_get_db
from AgentTheater.api.versions.v1.decisions_router import get_event_store as decisions_get_event_store
from AgentTheater.api.versions.v1.execution_router import get_db as execution_get_db
from AgentTheater.api.versions.v1.execution_router import get_event_store as execution_get_event_store
from AgentTheater.events import EventStore

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
pytest_plugins = ("pytest_asyncio",)

_JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production-key!")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with SessionLocal() as session:
            yield session

    async def override_get_event_store():
        async with SessionLocal() as session:
            yield EventStore(session)

    app.dependency_overrides[decisions_get_db] = override_get_db
    app.dependency_overrides[decisions_get_event_store] = override_get_event_store
    app.dependency_overrides[execution_get_db] = override_get_db
    app.dependency_overrides[execution_get_event_store] = override_get_event_store

    yield SessionLocal

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.fixture
async def client(test_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def make_token(user_id: UUID, tenant_id: UUID, roles=None, exp_delta_hours=1):
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "roles": roles or ["operator"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=exp_delta_hours),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm="HS256")


def auth_headers(user_id: UUID, tenant_id: UUID):
    return {
        "Authorization": f"Bearer {make_token(user_id, tenant_id)}",
        "X-Tenant-ID": str(tenant_id),
    }


# ─────────────────────────────────────────────────────
# Fix 1: JWT Security
# ─────────────────────────────────────────────────────

class TestJWTSecurity:

    @pytest.mark.asyncio
    async def test_valid_token_accepted(self, client, test_db):
        """A properly signed token with matching tenant is accepted."""
        tenant_id = uuid4()
        user_id = uuid4()
        project_id = uuid4()

        resp = await client.post(
            "/api/v1/decisions",
            json={
                "project_id": str(project_id),
                "question": "Valid token test?",
                "roles": ["ceo"],
                "tenant_id": str(tenant_id),
            },
            headers=auth_headers(user_id, tenant_id),
        )
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_forged_token_rejected(self, client, test_db):
        """A token signed with wrong secret is rejected with 401."""
        tenant_id = uuid4()
        user_id = uuid4()
        project_id = uuid4()

        forged = jwt.encode(
            {
                "sub": str(user_id),
                "tenant_id": str(tenant_id),
                "roles": ["operator"],
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            },
            "wrong-secret",
            algorithm="HS256",
        )

        resp = await client.post(
            "/api/v1/decisions",
            json={
                "project_id": str(project_id),
                "question": "Forged token test?",
                "roles": ["ceo"],
                "tenant_id": str(tenant_id),
            },
            headers={
                "Authorization": f"Bearer {forged}",
                "X-Tenant-ID": str(tenant_id),
            },
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_expired_token_rejected(self, client, test_db):
        """An expired token is rejected with 401."""
        tenant_id = uuid4()
        user_id = uuid4()
        project_id = uuid4()

        expired_token = make_token(user_id, tenant_id, exp_delta_hours=-1)

        resp = await client.post(
            "/api/v1/decisions",
            json={
                "project_id": str(project_id),
                "question": "Expired token test?",
                "roles": ["ceo"],
                "tenant_id": str(tenant_id),
            },
            headers={
                "Authorization": f"Bearer {expired_token}",
                "X-Tenant-ID": str(tenant_id),
            },
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_tenant_mismatch_rejected(self, client, test_db):
        """Header tenant_id that differs from token's tenant_id claim → 401."""
        tenant_id = uuid4()
        other_tenant = uuid4()
        user_id = uuid4()
        project_id = uuid4()

        token = make_token(user_id, tenant_id)

        resp = await client.post(
            "/api/v1/decisions",
            json={
                "project_id": str(project_id),
                "question": "Tenant mismatch test?",
                "roles": ["ceo"],
                "tenant_id": str(other_tenant),
            },
            headers={
                "Authorization": f"Bearer {token}",
                "X-Tenant-ID": str(other_tenant),  # Header says other_tenant, token says tenant_id
            },
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_missing_auth_header_rejected(self, client, test_db):
        """Request with no Authorization header → 401."""
        resp = await client.post(
            "/api/v1/decisions",
            json={
                "project_id": str(uuid4()),
                "question": "Should we proceed with this initiative?",
                "roles": ["ceo"],
                "tenant_id": str(uuid4()),
            },
        )
        assert resp.status_code == 401


# ─────────────────────────────────────────────────────
# Fix 2: Outbox Relay
# ─────────────────────────────────────────────────────

class TestOutboxRelay:

    @pytest.mark.asyncio
    async def test_relay_publishes_unpublished_events(self, test_db):
        """OutboxRelay marks unpublished outbox entries as published."""
        async with test_db() as session:
            entry = EventOutbox(
                event_id=uuid4(),
                event_type="test.event",
                aggregate_id=uuid4(),
                tenant_id=uuid4(),
                event_payload={"key": "value"},
                published=False,
            )
            session.add(entry)
            await session.commit()
            event_id = entry.event_id

        relay = OutboxRelay(test_db, batch_size=10)
        published = await relay.run_once()

        assert published == 1

        async with test_db() as session:
            result = await session.scalar(
                select(EventOutbox).where(EventOutbox.event_id == event_id)
            )
            assert result.published is True
            assert result.published_at is not None

    @pytest.mark.asyncio
    async def test_relay_does_not_republish(self, test_db):
        """Entries already marked published are skipped by the relay."""
        async with test_db() as session:
            entry = EventOutbox(
                event_id=uuid4(),
                event_type="already.published",
                aggregate_id=uuid4(),
                tenant_id=uuid4(),
                event_payload={},
                published=True,
                published_at=datetime.now(timezone.utc),
            )
            session.add(entry)
            await session.commit()

        relay = OutboxRelay(test_db, batch_size=10)
        published = await relay.run_once()
        assert published == 0

    @pytest.mark.asyncio
    async def test_relay_skips_max_attempts(self, test_db):
        """Entries that hit max attempts are not retried."""
        relay = OutboxRelay(test_db, batch_size=10)

        async with test_db() as session:
            entry = EventOutbox(
                event_id=uuid4(),
                event_type="exhausted.event",
                aggregate_id=uuid4(),
                tenant_id=uuid4(),
                event_payload={},
                published=False,
                attempts=relay.MAX_ATTEMPTS,
            )
            session.add(entry)
            await session.commit()

        published = await relay.run_once()
        assert published == 0

    @pytest.mark.asyncio
    async def test_concurrent_relay_runs_use_lock(self, test_db):
        """Concurrent relay.run_once() calls don't double-publish (lock held)."""
        async with test_db() as session:
            for _ in range(3):
                session.add(EventOutbox(
                    event_id=uuid4(),
                    event_type="concurrent.test",
                    aggregate_id=uuid4(),
                    tenant_id=uuid4(),
                    event_payload={},
                    published=False,
                ))
            await session.commit()

        relay = OutboxRelay(test_db, batch_size=10)
        results = await asyncio.gather(relay.run_once(), relay.run_once())
        # One run gets the lock, the other sees lock held and returns 0
        assert sum(results) == 3


# ─────────────────────────────────────────────────────
# Fix 3: Atomic Sequence (no duplicates)
# ─────────────────────────────────────────────────────

class TestAtomicSequence:

    @pytest.mark.asyncio
    async def test_sequence_starts_at_zero(self, test_db):
        """First event for an aggregate gets sequence 0."""
        async with test_db() as session:
            ledger = EventLedger(session)
            agg_id = uuid4()
            tenant_id = uuid4()

            event = DomainEvent(
                event_type="test.created",
                aggregate_id=agg_id,
                aggregate_type="TestAggregate",
                tenant_id=tenant_id,
            )
            await ledger.append(event)
            await session.commit()

        assert event.sequence_number == 0

    @pytest.mark.asyncio
    async def test_sequence_increments_monotonically(self, test_db):
        """Subsequent events for the same aggregate get consecutive sequence numbers."""
        async with test_db() as session:
            ledger = EventLedger(session)
            agg_id = uuid4()
            tenant_id = uuid4()

            events = []
            for i in range(5):
                e = DomainEvent(
                    event_type="test.updated",
                    aggregate_id=agg_id,
                    aggregate_type="TestAggregate",
                    tenant_id=tenant_id,
                )
                await ledger.append(e)
                events.append(e)

            await session.commit()

        seqs = [e.sequence_number for e in events]
        assert seqs == list(range(5))

    @pytest.mark.asyncio
    async def test_different_aggregates_have_independent_sequences(self, test_db):
        """Separate aggregate streams have independent sequence counters."""
        async with test_db() as session:
            ledger = EventLedger(session)
            agg_a = uuid4()
            agg_b = uuid4()
            tenant_id = uuid4()

            ea = DomainEvent(event_type="a.evt", aggregate_id=agg_a, aggregate_type="A", tenant_id=tenant_id)
            eb = DomainEvent(event_type="b.evt", aggregate_id=agg_b, aggregate_type="B", tenant_id=tenant_id)
            ea2 = DomainEvent(event_type="a.evt2", aggregate_id=agg_a, aggregate_type="A", tenant_id=tenant_id)

            await ledger.append(ea)
            await ledger.append(eb)
            await ledger.append(ea2)
            await session.commit()

        assert ea.sequence_number == 0
        assert eb.sequence_number == 0  # Independent
        assert ea2.sequence_number == 1

    @pytest.mark.asyncio
    async def test_aggregate_sequence_row_created(self, test_db):
        """AggregateSequence row is created/incremented in DB."""
        agg_id = uuid4()
        tenant_id = uuid4()

        async with test_db() as session:
            ledger = EventLedger(session)
            for _ in range(3):
                await ledger.append(DomainEvent(
                    event_type="seq.test",
                    aggregate_id=agg_id,
                    aggregate_type="Seq",
                    tenant_id=tenant_id,
                ))
            await session.commit()

        async with test_db() as session:
            row = await session.scalar(
                select(AggregateSequence).where(AggregateSequence.aggregate_id == agg_id)
            )
            assert row is not None
            assert row.next_sequence == 3  # 0, 1, 2 used → next is 3


# ─────────────────────────────────────────────────────
# Fix 4: Optimistic Locking (If-Match / ETag)
# ─────────────────────────────────────────────────────

class TestOptimisticLocking:

    async def _create_decision_and_execution(self, client, tenant_id, user_id, project_id):
        """Helper: create decision + execution; return execution_id."""
        token = make_token(user_id, tenant_id)
        headers = {"Authorization": f"Bearer {token}", "X-Tenant-ID": str(tenant_id)}

        d_resp = await client.post(
            "/api/v1/decisions",
            json={"project_id": str(project_id), "question": "Should we proceed with this initiative?", "roles": ["ceo"], "tenant_id": str(tenant_id)},
            headers=headers,
        )
        assert d_resp.status_code == 201
        decision_id = d_resp.json()["id"]

        e_resp = await client.post(
            "/api/v1/executions",
            json={"decision_id": decision_id, "predicted_outcome": "succeeded"},
            headers=headers,
        )
        assert e_resp.status_code == 200
        return e_resp.json()["id"], headers

    @pytest.mark.asyncio
    async def test_start_with_correct_version_succeeds(self, client, test_db):
        """If-Match: '1' matches initial version → transition succeeds."""
        tenant_id, user_id, project_id = uuid4(), uuid4(), uuid4()
        execution_id, headers = await self._create_decision_and_execution(client, tenant_id, user_id, project_id)

        resp = await client.post(
            f"/api/v1/executions/{execution_id}/start",
            headers={**headers, "If-Match": '"1"'},
        )
        assert resp.status_code == 200
        assert resp.headers.get("ETag") == '"2"'

    @pytest.mark.asyncio
    async def test_start_with_stale_version_returns_409(self, client, test_db):
        """If-Match with wrong version → 409 Conflict."""
        tenant_id, user_id, project_id = uuid4(), uuid4(), uuid4()
        execution_id, headers = await self._create_decision_and_execution(client, tenant_id, user_id, project_id)

        resp = await client.post(
            f"/api/v1/executions/{execution_id}/start",
            headers={**headers, "If-Match": '"99"'},
        )
        assert resp.status_code == 409
        assert "Conflict" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_no_if_match_proceeds_without_check(self, client, test_db):
        """Without If-Match header, state transition proceeds as before."""
        tenant_id, user_id, project_id = uuid4(), uuid4(), uuid4()
        execution_id, headers = await self._create_decision_and_execution(client, tenant_id, user_id, project_id)

        resp = await client.post(f"/api/v1/executions/{execution_id}/start", headers=headers)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_etag_increments_after_each_transition(self, client, test_db):
        """ETag version increments with each successful state change."""
        tenant_id, user_id, project_id = uuid4(), uuid4(), uuid4()
        execution_id, headers = await self._create_decision_and_execution(client, tenant_id, user_id, project_id)

        # Start
        r1 = await client.post(f"/api/v1/executions/{execution_id}/start", headers=headers)
        assert r1.status_code == 200
        etag1 = r1.headers.get("ETag")

        # Block
        r2 = await client.post(
            f"/api/v1/executions/{execution_id}/block",
            json={"to_state": "blocked", "blocked_reason": "Pending review"},
            headers={**headers, "If-Match": etag1},
        )
        assert r2.status_code == 200
        etag2 = r2.headers.get("ETag")
        assert etag2 != etag1
