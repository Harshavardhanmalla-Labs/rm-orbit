# System 1 + System 2 Integration Plan

**Goal:** Versioned APIs publish immutable events safely.

**Status:** 🔨 INTEGRATION ARCHITECTURE

---

## Architecture Overview

### Request Flow with Events

```
HTTP Request
  ↓
[APIVersionMiddleware] Extract version, auth context
  ↓
[SecurityMiddleware] Extract user_id, tenant_id, roles
  ↓
[TrafficControlMiddleware] Route v1 or v2
  ↓
[Request Validation] Pydantic (strict mode)
  ↓
[Service Layer]
  ├→ Validate business logic
  ├→ Begin DB transaction
  ├→ Write domain change
  ├→ Create event (System 2)
  ├→ Append to outbox (same transaction)
  └→ Commit (atomic)
  ↓
[EventStore.commit()]
  ├→ Publish pending events to EventBus
  └→ Cache in event_history
  ↓
[Response] Return HTTP response
  ↓
[Background Worker] OutboxPublisher polls & publishes
  ↓
[Consumers] Process events with checkpoint safety
  ↓
[DLQ] Failed events after max retries
```

### Context Propagation

```
API Request Headers
  ├→ Authorization: Bearer token
  │   └→ SecurityContext (user_id, tenant_id, roles)
  │
  ├→ X-Correlation-ID: request-uuid
  │   └→ Flows into event.correlation_id
  │   └→ Flows into consumer logs
  │
  └→ X-API-Version: v1 | v2
      └→ TrafficController routes request
      └→ Response includes API-Version header
```

---

## Files to Modify / Create

### Part 1: API Layer (System 1) — Already Designed

**Existing Files:**
- `AgentTheater/api/versions/__init__.py` — Versioned router assembly
- `AgentTheater/api/versions/schemas.py` — Pydantic models (v1/v2)
- `AgentTheater/api/versions/compatibility.py` — Deprecation headers, schema adapters
- `AgentTheater/api/versions/v1/__init__.py` — V1 router
- `AgentTheater/api/versions/v1/decisions.py` — V1 decision endpoints
- `AgentTheater/api/versions/v2/__init__.py` — V2 router (placeholder)
- `AgentTheater/api/versions/contract.py` — Contract testing
- `AgentTheater/api/versions/traffic_control.py` — Version pinning, canary
- `AgentTheater/api/versions/observability.py` — Per-version metrics
- `AgentTheater/api/versions/security.py` — Tenant isolation, RBAC
- `AgentTheater/api/versions/middleware.py` — Request/response pipelines

### Part 2: Integration Layer (NEW)

**New Files:**
- `AgentTheater/api/integration/__init__.py` — Integration utilities
- `AgentTheater/api/integration/event_emitters.py` — API → Event mapping
- `AgentTheater/api/integration/context_flow.py` — Auth/tenant/correlation_id flow
- `AgentTheater/api/integration/request_hooks.py` — Pre/post request hooks
- `AgentTheater/api/integration/error_handling.py` — Failure handling without breaking API

### Part 3: Event Layer (System 2) — Already Built

**Existing Files:**
- `AgentTheater/events/db_models.py` — All 7 tables
- `AgentTheater/events/outbox.py` — Transactional outbox
- `AgentTheater/events/ledger.py` — EventLedger, EventStore
- `AgentTheater/events/consumer_checkpoint.py` — Consumer state
- `AgentTheater/events/schema_registry.py` — Schema validation
- `AgentTheater/events/delivery_guarantees.py` — Idempotency
- `AgentTheater/events/observability.py` — Metrics
- `AgentTheater/events/security.py` — Tenant isolation

### Part 4: Tests (NEW)

**New Test Files:**
- `tests/integration/test_api_event_emission.py` — API → Event flow
- `tests/integration/test_correlation_id_flow.py` — Correlation tracking
- `tests/integration/test_api_failure_modes.py` — Failure scenarios
- `tests/integration/test_consumer_integration.py` — Full end-to-end
- `tests/integration/test_release_gate_integration.py` — Gate checklist

### Part 5: Deployment

**Deployment Scripts:**
- `scripts/integration_release_gate.sh` — Pre-deployment checklist
- `scripts/rollback_integration.sh` — Emergency rollback

---

## Decision Endpoints Requiring Events

### V1 Decision Endpoints

| Endpoint | Method | Event Type | Event Data |
|----------|--------|------------|------------|
| `/api/v1/decisions` | POST | `decision.created` | {project_id, question, roles} |
| `/api/v1/decisions/{id}` | GET | (no event) | (read-only) |
| `/api/v1/decisions/{id}` | PATCH | `decision.updated` | {field, old_value, new_value} |
| `/api/v1/decisions/{id}/outcome` | POST | `decision.outcome_recorded` | {outcome, note} |
| `/api/v1/decisions/{id}/github-issue` | POST | `github_issue.added` | {repo, issue_id, url} |
| `/api/v1/decisions/{id}/github-issues` | POST | `github_issues.created` | {count, urls} |

### V2 Decision Endpoints (Future)

Same 6 endpoints, but potentially:
- Additional fields in events
- Stricter validation
- New workflow states

---

## Implementation Details

### 1. API Request → SecurityContext

**File:** `AgentTheater/api/integration/context_flow.py`

```python
from uuid import UUID
from fastapi import Request
from AgentTheater.events.security import EventSecurityContext

def extract_security_context(request: Request) -> EventSecurityContext:
    """Extract user context from request headers and auth token."""
    # Parse Authorization header
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    
    # Decode JWT (simplified - use real JWT library)
    payload = decode_jwt(token)
    
    # Extract tenant from token or header
    tenant_id = UUID(request.headers.get("X-Tenant-ID", payload.get("tenant_id")))
    user_id = UUID(payload.get("sub"))
    roles = payload.get("roles", [])
    
    return EventSecurityContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=roles,
    )

def extract_correlation_id(request: Request) -> str:
    """Extract or generate correlation_id for request tracing."""
    correlation_id = request.headers.get("X-Correlation-ID")
    
    if not correlation_id:
        # Generate if not provided
        correlation_id = str(uuid4())
    
    return correlation_id

def propagate_context_to_response(response, context):
    """Add context headers to response."""
    response.headers["X-Correlation-ID"] = context["correlation_id"]
    response.headers["X-API-Version"] = context["api_version"]
    if "deprecation" in context:
        response.headers["Deprecation"] = context["deprecation"]
    return response
```

### 2. API Endpoint → Event Emission

**File:** `AgentTheater/api/integration/event_emitters.py`

```python
from typing import Optional, Dict, Any
from uuid import UUID
from AgentTheater.events import EventStore
from AgentTheater.events.security import EventSecurityContext

class DecisionEventEmitters:
    """Emit events from decision API endpoints."""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
    
    async def emit_decision_created(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        project_id: UUID,
        question: str,
        roles: list[str],
        correlation_id: str,
    ) -> None:
        """Emit decision.created event (must be in same transaction as DB write)."""
        await self.event_store.record_decision_created(
            decision_id=decision_id,
            project_id=project_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            question=question,
            roles=roles,
            correlation_id=correlation_id,
        )
    
    async def emit_decision_outcome_recorded(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        outcome: str,
        note: Optional[str],
        correlation_id: str,
    ) -> None:
        """Emit decision.outcome_recorded event."""
        await self.event_store.record_decision_outcome(
            decision_id=decision_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            outcome=outcome,
            note=note,
            correlation_id=correlation_id,
        )
    
    async def emit_github_issue_added(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        repo: str,
        issue_id: int,
        url: str,
        correlation_id: str,
    ) -> None:
        """Emit github_issue.added event."""
        # Similar pattern
        ...
```

### 3. Atomic Transaction (API + Event)

**File:** `AgentTheater/api/integration/request_hooks.py`

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from AgentTheater.events import EventStore

@asynccontextmanager
async def transactional_event_scope(db: AsyncSession, event_store: EventStore):
    """Begin transaction that atomically writes domain change + event.
    
    Usage:
        async with transactional_event_scope(db, event_store) as (session, store):
            # Write domain change
            decision = Decision(...)
            session.add(decision)
            
            # Emit event (same transaction)
            await store.record_decision_created(...)
            
            # If either fails, both rollback
    """
    async with db.begin():
        yield db, event_store
    
    # After commit, emit to subscribers
    await event_store.commit()
```

### 4. Error Handling (API Errors ≠ Event Errors)

**File:** `AgentTheater/api/integration/error_handling.py`

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class APIEventError(Exception):
    """Error that occurred during event emission (not API error)."""
    pass

async def api_error_handler(request: Request, exc: Exception):
    """Handle errors without breaking API responses."""
    
    if isinstance(exc, APIEventError):
        # Event emission failed, but API request was valid
        # Log error, return 202 Accepted with warning
        return JSONResponse(
            status_code=202,  # Accepted (will retry)
            content={
                "message": "Request accepted, event delivery pending",
                "correlation_id": request.headers.get("X-Correlation-ID"),
                "warning": "Event publishing delayed (will retry)",
            }
        )
    
    # Regular API errors
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
```

### 5. Wired into Decision Endpoint

**File:** `AgentTheater/api/versions/v1/decisions.py` (Modified)

```python
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from AgentTheater.api.integration.context_flow import (
    extract_security_context,
    extract_correlation_id,
)
from AgentTheater.api.integration.event_emitters import DecisionEventEmitters
from AgentTheater.api.integration.request_hooks import transactional_event_scope
from AgentTheater.events import EventStore
from AgentTheater.api.versions.schemas import DecisionCreateRequest, DecisionRecordResponse

router = APIRouter(prefix="/api/v1/decisions", tags=["decisions"])

@router.post("")
async def create_decision(
    request: Request,
    req: DecisionCreateRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionRecordResponse:
    """Create decision and emit event atomically."""
    
    # Extract context
    security_context = extract_security_context(request)
    correlation_id = extract_correlation_id(request)
    
    # Verify tenant isolation
    if req.tenant_id != security_context.tenant_id:
        raise PermissionError("Tenant mismatch")
    
    # Atomic transaction: write domain change + emit event
    decision_id = uuid4()
    
    async with transactional_event_scope(db, event_store) as (session, store):
        # 1. Create decision record
        decision = Decision(
            id=decision_id,
            project_id=req.project_id,
            question=req.question,
            roles=req.roles,
            tenant_id=security_context.tenant_id,
            created_by=security_context.user_id,
        )
        session.add(decision)
        
        # 2. Emit event (same transaction)
        emitters = DecisionEventEmitters(store)
        await emitters.emit_decision_created(
            decision_id=decision_id,
            security_context=security_context,
            project_id=req.project_id,
            question=req.question,
            roles=req.roles,
            correlation_id=correlation_id,
        )
        
        # Flush to DB (validates constraints)
        await session.flush()
    
    # After transaction commits, events are in outbox
    # Background publisher will pick them up
    
    return DecisionRecordResponse(
        id=decision_id,
        question=req.question,
        roles=req.roles,
        created_at=decision.created_at,
    )

@router.post("/{id}/outcome")
async def record_outcome(
    id: UUID,
    request: Request,
    req: OutcomeRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionRecordResponse:
    """Record decision outcome and emit event atomically."""
    
    security_context = extract_security_context(request)
    correlation_id = extract_correlation_id(request)
    
    async with transactional_event_scope(db, event_store) as (session, store):
        # 1. Get decision
        result = await session.execute(
            select(Decision).where(Decision.id == id)
        )
        decision = result.scalar_one_or_none()
        if not decision:
            raise NotFoundError(f"Decision {id} not found")
        
        # Verify tenant isolation
        if decision.tenant_id != security_context.tenant_id:
            raise PermissionError("Tenant mismatch")
        
        # 2. Update decision
        decision.outcome = req.outcome
        decision.note = req.note
        decision.completed_at = datetime.now(timezone.utc)
        
        # 3. Emit event (same transaction)
        emitters = DecisionEventEmitters(store)
        await emitters.emit_decision_outcome_recorded(
            decision_id=decision.id,
            security_context=security_context,
            outcome=req.outcome,
            note=req.note,
            correlation_id=correlation_id,
        )
        
        await session.flush()
    
    return DecisionRecordResponse(
        id=decision.id,
        outcome=decision.outcome,
        note=decision.note,
        completed_at=decision.completed_at,
    )
```

---

## Integration Tests

### Test 1: Decision Created → Event Emitted

**File:** `tests/integration/test_api_event_emission.py`

```python
@pytest.mark.asyncio
async def test_create_decision_emits_event():
    """POST /api/v1/decisions creates decision AND emits event."""
    
    # Setup
    client = AsyncClient(app=app, base_url="http://test")
    db = await get_test_db()
    
    # Create decision via API
    response = await client.post(
        "/api/v1/decisions",
        json={
            "project_id": str(project_id),
            "question": "Should we pivot?",
            "roles": ["ceo", "cto"],
        },
        headers={
            "Authorization": f"Bearer {valid_token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-123",
        }
    )
    
    # Verify API response
    assert response.status_code == 201
    decision_id = UUID(response.json()["id"])
    
    # Verify decision in DB
    result = await db.execute(
        select(Decision).where(Decision.id == decision_id)
    )
    decision = result.scalar_one()
    assert decision.question == "Should we pivot?"
    
    # Verify event in outbox
    result = await db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.created")
            & (EventOutbox.aggregate_id == decision_id)
        )
    )
    outbox_entry = result.scalar_one()
    assert outbox_entry.published == False
    assert outbox_entry.event_payload["question"] == "Should we pivot?"
    assert outbox_entry.event_payload["roles"] == ["ceo", "cto"]
    
    # Verify correlation_id in event
    result = await db.execute(
        select(EventLog).where(EventLog.event_id == outbox_entry.event_id)
    )
    event_log = result.scalar_one()
    assert event_log.correlation_id == "test-123"

@pytest.mark.asyncio
async def test_record_outcome_emits_event():
    """POST /api/v1/decisions/{id}/outcome creates outcome event."""
    
    # Setup: Create decision first
    decision = create_test_decision(db, tenant_id)
    
    # Record outcome via API
    response = await client.post(
        f"/api/v1/decisions/{decision.id}/outcome",
        json={
            "outcome": "succeeded",
            "note": "Exceeded targets by 20%",
        },
        headers={
            "Authorization": f"Bearer {valid_token}",
            "X-Tenant-ID": str(tenant_id),
            "X-Correlation-ID": "test-456",
        }
    )
    
    # Verify response
    assert response.status_code == 200
    
    # Verify decision updated
    result = await db.execute(
        select(Decision).where(Decision.id == decision.id)
    )
    updated = result.scalar_one()
    assert updated.outcome == "succeeded"
    assert updated.note == "Exceeded targets by 20%"
    
    # Verify event in outbox
    result = await db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.outcome_recorded")
            & (EventOutbox.aggregate_id == decision.id)
        )
    )
    outbox_entry = result.scalar_one()
    assert outbox_entry.event_payload["outcome"] == "succeeded"

@pytest.mark.asyncio
async def test_atomicity_decision_and_event():
    """If event emission fails, decision write rolls back."""
    
    # Mock event emission to fail
    with patch.object(EventStore, 'record_decision_created', side_effect=ValueError("Event failed")):
        response = await client.post(
            "/api/v1/decisions",
            json={"project_id": str(project_id), "question": "..."},
            headers={...}
        )
    
    # Verify API returned error
    assert response.status_code >= 400
    
    # Verify decision NOT written (rolled back)
    result = await db.execute(
        select(Decision).where(Decision.question == "...")
    )
    assert result.scalar_one_or_none() is None
```

### Test 2: Correlation ID Flow

**File:** `tests/integration/test_correlation_id_flow.py`

```python
@pytest.mark.asyncio
async def test_correlation_id_flows_through_system():
    """Correlation ID: API → Event → Consumer logs."""
    
    correlation_id = "test-corr-123"
    
    # 1. Call API with correlation ID
    response = await client.post(
        "/api/v1/decisions",
        json={...},
        headers={
            "X-Correlation-ID": correlation_id,
            ...
        }
    )
    decision_id = UUID(response.json()["id"])
    
    # 2. Verify event has correlation ID
    result = await db.execute(
        select(EventLog).where(EventLog.aggregate_id == decision_id)
    )
    event = result.scalar_one()
    assert event.correlation_id == correlation_id
    
    # 3. Run publisher
    published = await publisher.publish_pending(tenant_id)
    assert published >= 1
    
    # 4. Verify event in history has correlation ID
    result = await db.execute(
        select(EventLog).where(EventLog.correlation_id == correlation_id)
    )
    events_with_correlation = result.scalars().all()
    assert len(events_with_correlation) >= 1
    
    # 5. Consumer receives event with correlation ID
    class TestConsumer(EventConsumer):
        received_events = []
        
        async def process_event(self, event):
            self.received_events.append(event)
    
    consumer = TestConsumer(db, "test-consumer")
    async for batch in consumer.stream_events(tenant_id):
        for event in batch:
            # Correlation ID available for logging
            logger.info(f"Processing event {event['event_id']}", extra={
                "correlation_id": event.get("correlation_id", correlation_id)
            })
        break
```

### Test 3: Duplicate Request → No Duplicate Event

**File:** `tests/integration/test_api_idempotency.py`

```python
@pytest.mark.asyncio
async def test_duplicate_request_no_duplicate_event():
    """Same request sent twice (same correlation ID) → single event."""
    
    correlation_id = "idempotent-123"
    request_payload = {
        "project_id": str(project_id),
        "question": "Should we expand?",
        "roles": ["ceo"],
    }
    
    # Send request twice
    response1 = await client.post(
        "/api/v1/decisions",
        json=request_payload,
        headers={
            "X-Correlation-ID": correlation_id,
            "X-Idempotency-Key": "key-123",
            ...
        }
    )
    decision_id_1 = UUID(response1.json()["id"])
    
    response2 = await client.post(
        "/api/v1/decisions",
        json=request_payload,
        headers={
            "X-Correlation-ID": correlation_id,
            "X-Idempotency-Key": "key-123",  # Same key
            ...
        }
    )
    decision_id_2 = UUID(response2.json()["id"])
    
    # Verify same decision returned (idempotent)
    assert decision_id_1 == decision_id_2
    
    # Verify only one event emitted
    result = await db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.created")
            & (EventOutbox.aggregate_id == decision_id_1)
        )
    )
    events = result.scalars().all()
    assert len(events) == 1  # Only one, not two
```

### Test 4: Consumer Crash + Resume

**File:** `tests/integration/test_consumer_integration.py`

```python
@pytest.mark.asyncio
async def test_consumer_crash_and_resume():
    """Consumer crashes after processing event → resumes without duplicates."""
    
    # 1. Create decision (event in outbox)
    response = await client.post("/api/v1/decisions", json={...}, headers={...})
    decision_id = UUID(response.json()["id"])
    
    # 2. Run publisher (event published)
    published = await publisher.publish_pending(tenant_id)
    assert published == 1
    
    # 3. Consumer processes event
    class TrackingConsumer(EventConsumer):
        processed = []
        
        async def process_event(self, event):
            if event["event_type"] == "decision.created":
                self.processed.append(event["event_id"])
    
    consumer = TrackingConsumer(db, "test-processor")
    await consumer.initialize()
    
    async for batch in consumer.stream_events(tenant_id):
        # Process one event
        break  # Simulate crash before processing more
    
    # Verify checkpoint advanced
    checkpoint = await consumer.checkpoint_mgr.get_checkpoint()
    assert checkpoint.last_processed_sequence > 0
    
    # 4. Simulate crash (delete consumer)
    del consumer
    
    # 5. Create another decision (new event)
    response2 = await client.post("/api/v1/decisions", json={...}, headers={...})
    decision_id_2 = UUID(response2.json()["id"])
    
    # Run publisher again
    published = await publisher.publish_pending(tenant_id)
    assert published == 1
    
    # 6. Resume consumer
    consumer = TrackingConsumer(db, "test-processor")
    await consumer.initialize()
    
    event_count = 0
    async for batch in consumer.stream_events(tenant_id):
        event_count += len(batch)
        if event_count >= 1:
            break
    
    # Verify: only NEW event processed (not re-processing first one)
    assert len(consumer.processed) == 1
    assert consumer.processed[0] == str(decision_id_2)  # Only second event
```

### Test 5: DLQ Receives Poisoned Event

**File:** `tests/integration/test_dlq_integration.py`

```python
@pytest.mark.asyncio
async def test_poisoned_event_to_dlq():
    """Event that always fails processing → moves to DLQ."""
    
    # Create decision
    response = await client.post("/api/v1/decisions", json={...}, headers={...})
    decision_id = UUID(response.json()["id"])
    
    # Consumer that fails on this specific event
    class FailingConsumer(EventConsumer):
        async def process_event(self, event):
            if event["aggregate_id"] == str(decision_id):
                raise ValueError("Always fails for this decision")
    
    consumer = FailingConsumer(db, "failing-processor", "default")
    
    # Try to process (will fail)
    for attempt in range(3):
        try:
            async for batch in consumer.stream_events(tenant_id):
                # Simulates failure on process_event
                break
        except ValueError:
            # Mark error
            await consumer.checkpoint_mgr.mark_error(...)
    
    # After 3 failures, move to DLQ
    dlq_handler = DLQHandler(db)
    unresolved = await dlq_handler.get_unresolved_dlq(tenant_id)
    
    # Verify event in DLQ
    dlq_entry = next((e for e in unresolved if e.aggregate_id == decision_id), None)
    assert dlq_entry is not None
    assert dlq_entry.error_message == "Always fails for this decision"
```

---

## Release Gate Script

**File:** `scripts/integration_release_gate.sh`

```bash
#!/bin/bash
set -e

echo "🔄 System 1 + System 2 Integration Release Gate"
echo "================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

check() {
    local test_name="$1"
    local command="$2"
    
    echo -n "▶ $test_name ... "
    
    if eval "$command" > /tmp/test_output.txt 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAILED${NC}"
        cat /tmp/test_output.txt
        ((FAILED++))
    fi
}

# 1. Schema validation
check "1.1 Event schemas versioned" \
    "pytest tests/integration/test_schema_registry.py -v -k version"

check "1.2 Backward-compatible evolution" \
    "pytest tests/integration/test_schema_registry.py -v -k compatible"

# 2. API → Event flow
check "2.1 Decision created emits event" \
    "pytest tests/integration/test_api_event_emission.py::test_create_decision_emits_event -v"

check "2.2 Outcome recorded emits event" \
    "pytest tests/integration/test_api_event_emission.py::test_record_outcome_emits_event -v"

check "2.3 Atomicity: decision + event" \
    "pytest tests/integration/test_api_event_emission.py::test_atomicity_decision_and_event -v"

# 3. Context propagation
check "3.1 Correlation ID flows through system" \
    "pytest tests/integration/test_correlation_id_flow.py::test_correlation_id_flows_through_system -v"

check "3.2 Tenant isolation in events" \
    "pytest tests/integration/test_security.py::test_tenant_isolation_events -v"

check "3.3 Auth context flows into events" \
    "pytest tests/integration/test_security.py::test_auth_context_in_events -v"

# 4. Duplicate handling
check "4.1 Duplicate request no duplicate event" \
    "pytest tests/integration/test_api_idempotency.py::test_duplicate_request_no_duplicate_event -v"

check "4.2 Idempotent consumer skip duplicates" \
    "pytest tests/integration/test_delivery_guarantees.py -v -k idempotent"

# 5. Consumer safety
check "5.1 Consumer checkpoint resume" \
    "pytest tests/integration/test_consumer_integration.py::test_consumer_crash_and_resume -v"

check "5.2 No duplicate on restart" \
    "pytest tests/integration/test_consumer_integration.py::test_no_duplicate_on_restart -v"

# 6. Failure handling
check "6.1 API error doesn't break event" \
    "pytest tests/integration/test_api_failure_modes.py::test_api_error_handling -v"

check "6.2 Event failure doesn't break API" \
    "pytest tests/integration/test_api_failure_modes.py::test_event_failure_handling -v"

check "6.3 Poisoned event to DLQ" \
    "pytest tests/integration/test_dlq_integration.py::test_poisoned_event_to_dlq -v"

# 7. Observability
check "7.1 Request metrics collected" \
    "pytest tests/integration/test_observability_integration.py::test_request_metrics -v"

check "7.2 Correlation ID in logs" \
    "pytest tests/integration/test_observability_integration.py::test_correlation_in_logs -v"

# 8. End-to-end
check "8.1 Full decision flow" \
    "pytest tests/integration/test_e2e_integration.py::test_decision_lifecycle -v"

check "8.2 Multiple consumers" \
    "pytest tests/integration/test_e2e_integration.py::test_multiple_consumers -v"

# Summary
echo ""
echo "================================================"
echo -e "Results: ${GREEN}$PASSED PASSED${NC}, ${RED}$FAILED FAILED${NC}"
echo "================================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All gates PASSED - Ready to deploy${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED gates FAILED - Fix issues before deploying${NC}"
    exit 1
fi
```

**Run:** `bash scripts/integration_release_gate.sh`

---

## Rollback Plan

### If Integration Fails After Deployment

**Immediate Actions (Rollback):**

```bash
#!/bin/bash
# scripts/rollback_integration.sh

echo "🔄 Rolling back System 1 + System 2 integration..."

# 1. Stop outbox publisher (stop emitting events)
systemctl stop agent-theater-outbox-publisher

# 2. Revert API routes to not emit events
git checkout HEAD~1 -- AgentTheater/api/

# 3. Restart API servers
systemctl restart agent-theater-api

# 4. Clear event_outbox table (unpublished events only)
psql -d agenttheater -c "DELETE FROM event_outbox WHERE published = FALSE;"

# 5. Verify: no new events being created
curl -s http://localhost:8000/api/health | jq '.event_outbox_count'

echo "✅ Rollback complete"
```

### Step-by-Step Rollback

| Step | Action | Time | Rollback |
|------|--------|------|----------|
| 1 | Deploy API with event emission | 1 min | Revert code + restart |
| 2 | Deploy event schema registry | 2 min | Clear EventSchema table |
| 3 | Start outbox publisher | 1 min | Stop publisher |
| 4 | Start consumers | 2 min | Stop consumers |
| 5 | Monitor for failures | 5 min | See below |

### If Failures Detected

```bash
# Option 1: Stop event emission (keep API working)
# Revert AGentTheater/api/ to pre-integration version
# Stop all consumers
# Disable event_outbox writes
# Result: API works, events don't flow

# Option 2: Full rollback (nuclear)
# Stop all services
# Drop event tables
# Revert code
# Restart

# Option 3: Partial rollback (specific endpoint)
# Disable event emission for single endpoint
# Keep other endpoints working
# Example: Turn off outcome_recorded events, keep create events
```

### Data Preservation

```sql
-- Before rollback, save event log
CREATE TABLE event_log_backup AS SELECT * FROM event_log;
CREATE TABLE event_outbox_backup AS SELECT * FROM event_outbox;

-- After rollback, can replay from backup
INSERT INTO event_log SELECT * FROM event_log_backup;
```

---

## File Modification Checklist

### Part 1: Create Integration Layer

- [ ] `AgentTheater/api/integration/__init__.py` (new)
- [ ] `AgentTheater/api/integration/context_flow.py` (new)
- [ ] `AgentTheater/api/integration/event_emitters.py` (new)
- [ ] `AgentTheater/api/integration/request_hooks.py` (new)
- [ ] `AgentTheater/api/integration/error_handling.py` (new)

### Part 2: Modify API Routes

- [ ] `AgentTheater/api/versions/v1/decisions.py` (modify)
- [ ] Wire `extract_security_context`, `extract_correlation_id`
- [ ] Wire `transactional_event_scope`
- [ ] Wire `DecisionEventEmitters`
- [ ] Add event emission to each endpoint

### Part 3: Add Tests

- [ ] `tests/integration/test_api_event_emission.py` (new)
- [ ] `tests/integration/test_correlation_id_flow.py` (new)
- [ ] `tests/integration/test_api_idempotency.py` (new)
- [ ] `tests/integration/test_consumer_integration.py` (new)
- [ ] `tests/integration/test_dlq_integration.py` (new)
- [ ] `tests/integration/test_api_failure_modes.py` (new)
- [ ] `tests/integration/test_observability_integration.py` (new)
- [ ] `tests/integration/test_e2e_integration.py` (new)

### Part 4: Add Deployment

- [ ] `scripts/integration_release_gate.sh` (new)
- [ ] `scripts/rollback_integration.sh` (new)
- [ ] `docs/INTEGRATION_DEPLOYMENT.md` (new)

---

## Success Criteria

**Integration is successful when:**

1. ✅ All 8 test files pass (50+ test cases)
2. ✅ Release gate script reports: "All gates PASSED"
3. ✅ Correlation ID flows: Request → Event → Consumer logs
4. ✅ Tenant isolation enforced: No cross-tenant events
5. ✅ Atomicity verified: Decision + Event both written or both rolled back
6. ✅ Consumer safety: Checkpoint resume, no duplicates
7. ✅ DLQ working: Poisoned events move to DLQ
8. ✅ Metrics collected: P95/P99 latency visible
9. ✅ 0 duplicate events on retry
10. ✅ Rollback tested and working

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Create integration layer | 4 hours | 5 new files, context/event flow |
| 2. Modify API routes | 3 hours | Event emission wired to endpoints |
| 3. Add tests | 6 hours | 50+ test cases covering all scenarios |
| 4. Release gate script | 2 hours | Automated checklist |
| 5. Testing + fixes | 4 hours | All tests passing |
| 6. Rollback procedures | 2 hours | Documented + tested |

**Total:** ~20 hours

---

## Next: System 3 - Decision Execution Engine

Once this integration passes:

1. System 2 events flow from API → Outbox → Consumers ✅
2. Correlation IDs tracked end-to-end ✅
3. Tenant isolation enforced ✅
4. Failures don't break API ✅

Then build System 3:
- Worker picks up "in_progress" decisions
- Runs multi-agent collaboration
- Records outcome via event system
- Full audit trail

---

*Integration is the bridge between versioned APIs and immutable event streams.*
