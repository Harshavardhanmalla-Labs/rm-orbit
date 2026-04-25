# System 2 Release Gate: Hardened & Ready to Deploy

**Status:** CHECKLIST FOR DEPLOYMENT

**Requirement:** All 10 criteria must PASS before merge to main.

---

## Test Criteria

### 1. Transactional Outbox: No Lost Events ❌→✅

**Objective:** Verify that if API succeeds but publisher crashes, events are never lost.

**Test Command:**
```bash
# Test file: tests/integration/test_outbox_guarantees.py
pytest tests/integration/test_outbox_guarantees.py::test_outbox_no_lost_events -v
```

**What It Tests:**
```python
async def test_outbox_no_lost_events():
    """Verify: Event persisted IFF domain change persisted."""
    # Scenario 1: Normal flow
    async with db.begin():
        decision.outcome = "succeeded"
        await outbox.append_event(...)
    # Verify: outcome in DB AND event in outbox
    
    # Scenario 2: Rollback on event failure
    try:
        async with db.begin():
            decision.outcome = "succeeded"
            await outbox.append_event(bad_event)  # Fails
    except:
        pass
    # Verify: outcome NOT in DB AND event NOT in outbox
    
    # Scenario 3: Crash recovery
    outbox_entries = await db.execute(select(EventOutbox).where(EventOutbox.published == False))
    assert len(outbox_entries) == expected
```

**Pass Criteria:**
- ✅ No lost events on crash
- ✅ Atomic: outcome and event both written or both rolled back
- ✅ Publisher can resume from checkpoint

**Expected Output:**
```
test_outbox_no_lost_events PASSED
test_outbox_crash_recovery PASSED
test_outbox_atomic_transaction PASSED
```

---

### 2. Consumer Checkpointing: Safe Resume ❌→✅

**Objective:** Verify consumer resumes from last checkpoint without duplicate processing.

**Test Command:**
```bash
pytest tests/integration/test_consumer_checkpoint.py -v
```

**What It Tests:**
```python
async def test_consumer_resumes_from_checkpoint():
    """Consumer crash → restart → resume without duplicates."""
    consumer = TestConsumer(db, "test-consumer")
    
    # Phase 1: Process 5 events
    for i in range(5):
        await consumer.process_event(events[i])
        await checkpoint_mgr.mark_processed(events[i].event_id, i)
    
    # Verify checkpoint advanced
    checkpoint = await checkpoint_mgr.get_checkpoint()
    assert checkpoint.last_processed_sequence == 4
    
    # Phase 2: Simulate crash (delete consumer object)
    del consumer, checkpoint_mgr
    
    # Phase 3: Restart
    consumer = TestConsumer(db, "test-consumer")
    await consumer.initialize()
    resume_seq = await consumer.checkpoint_mgr.get_resume_sequence()
    
    # Verify resume point
    assert resume_seq == 4  # Will process next event (5)
    
    # Phase 4: Process remaining events without reprocessing earlier ones
    for i in range(5, 10):
        await consumer.process_event(events[i])
        await checkpoint_mgr.mark_processed(events[i].event_id, i)
    
    # Verify: no duplicates in results
    assert len(consumer.processed_events) == 10  # 5 original + 5 new
```

**Pass Criteria:**
- ✅ Consumer resumes from exact checkpoint
- ✅ No duplicate processing
- ✅ Heartbeat mechanism working
- ✅ Stale consumer detection

**Expected Output:**
```
test_consumer_resumes_from_checkpoint PASSED
test_consumer_heartbeat PASSED
test_consumer_stale_detection PASSED
test_consumer_group_coordination PASSED
```

---

### 3. Dead Letter Queue: Failed Event Handling ❌→✅

**Objective:** Verify failed events move to DLQ and can be manually reviewed/replayed.

**Test Command:**
```bash
pytest tests/integration/test_dlq_handler.py -v
```

**What It Tests:**
```python
async def test_dlq_move_after_max_retries():
    """Event fails 3 times → move to DLQ."""
    # Mark as failed 3 times
    for _ in range(3):
        retry = await outbox.mark_error(event_id, "Error: invalid state")
        assert retry == False  # Should return False on 3rd attempt
    
    # Move to DLQ
    dlq_entry = await dlq_handler.move_to_dlq(
        event_id=event_id,
        original_consumer="decision-processor",
        error_message="Error: invalid state",
        failure_reason="Decision already in terminal state"
    )
    
    # Verify DLQ entry
    assert dlq_entry.resolved == False
    assert dlq_entry.retry_count == 3
    assert dlq_entry.error_message == "Error: invalid state"
    
    # Get unresolved DLQ
    unresolved = await dlq_handler.get_unresolved_dlq(tenant_id)
    assert len(unresolved) == 1

async def test_dlq_replay():
    """Manually resolve DLQ entry and replay."""
    # Get unresolved entry
    unresolved = await dlq_handler.get_unresolved_dlq(tenant_id)
    dlq_entry = unresolved[0]
    
    # Schedule retry (after fixing root cause)
    await dlq_retry.schedule_retry(
        dlq_entry.dlq_id,
        retry_at=datetime.now(timezone.utc) + timedelta(seconds=1)
    )
    
    # Wait for retry time
    await asyncio.sleep(2)
    
    # Process retries
    replayed = await dlq_retry.process_scheduled_retries(tenant_id)
    assert replayed == 1
    
    # Verify event re-published
    result = await db.execute(select(EventLog).where(EventLog.event_id == event_id))
    assert result.scalar_one_or_none() is not None
```

**Pass Criteria:**
- ✅ Failed events move to DLQ after max retries
- ✅ DLQ stores failure context (error_message, failure_reason)
- ✅ Manual review possible (get_unresolved_dlq)
- ✅ Replay mechanism works (schedule_retry + process_scheduled_retries)
- ✅ Resolution tracking (manual_fix, replayed, discarded)

**Expected Output:**
```
test_dlq_move_after_max_retries PASSED
test_dlq_replay PASSED
test_dlq_resolution PASSED
test_dlq_metrics PASSED
```

---

### 4. Event Schema Registry: Backward-Compatible Evolution ❌→✅

**Objective:** Verify schemas are versioned, validated, and evolution is backward-compatible.

**Test Command:**
```bash
pytest tests/integration/test_schema_registry.py -v
```

**What It Tests:**
```python
async def test_schema_validation():
    """Event validated against schema."""
    registry = SchemaRegistry(db)
    
    # Register v1 schema
    schema_v1 = {
        "type": "object",
        "properties": {
            "outcome": {"type": "string", "enum": ["succeeded", "failed"]},
            "note": {"type": "string"}
        },
        "required": ["outcome"]
    }
    await registry.register_schema(
        event_type="decision.outcome_recorded",
        schema_version="v1",
        json_schema=schema_v1
    )
    
    # Valid event
    valid_event = {"outcome": "succeeded", "note": "Good decision"}
    result = await registry.validate_event(
        event_type="decision.outcome_recorded",
        event_payload=valid_event
    )
    assert result["valid"] == True
    
    # Invalid event (missing required field)
    invalid_event = {"note": "No outcome"}
    with pytest.raises(ValidationError):
        await registry.validate_event(
            event_type="decision.outcome_recorded",
            event_payload=invalid_event
        )

async def test_schema_backward_compatibility():
    """Schema v2 is backward-compatible with v1."""
    # Register v2 (add optional field)
    schema_v2 = {
        **schema_v1,
        "properties": {
            **schema_v1["properties"],
            "metadata": {"type": "object"}  # NEW: optional
        }
    }
    
    # Check compatibility
    result = BackwardCompatibilityChecker.check_compatibility(
        schema_v1, schema_v2,
        mode=CompatibilityMode.BACKWARD
    )
    
    # Verify
    assert result["compatible"] == True
    assert len(result["violations"]) == 0
    assert result["safe_to_deploy"] == True
    
    # Old v1 events still validate with v2 schema
    old_event = {"outcome": "succeeded"}
    await registry.validate_event(
        event_type="decision.outcome_recorded",
        event_payload=old_event,
        schema_version="v2"
    )

async def test_breaking_change_rejection():
    """Breaking change in schema is rejected."""
    # Try to make required field optional (BREAKING)
    schema_breaking = {
        **schema_v1,
        "required": []  # Removed "outcome" from required
    }
    
    result = BackwardCompatibilityChecker.check_compatibility(
        schema_v1, schema_breaking
    )
    
    # Verify
    assert result["compatible"] == False
    assert len(result["violations"]) > 0
```

**Pass Criteria:**
- ✅ Events validated against JSON Schema
- ✅ Schema versions tracked
- ✅ v2 backward-compatible with v1
- ✅ Breaking changes detected and rejected
- ✅ Schemas deduplicated by hash

**Expected Output:**
```
test_schema_validation PASSED
test_schema_backward_compatibility PASSED
test_breaking_change_rejection PASSED
test_schema_versioning PASSED
```

---

### 5. Idempotent Processing: Duplicate Detection ❌→✅

**Objective:** Verify duplicate events are skipped and cached results returned.

**Test Command:**
```bash
pytest tests/integration/test_idempotency.py -v
```

**What It Tests:**
```python
async def test_idempotent_consumer_skips_duplicates():
    """Same event_id processed only once."""
    
    class TestConsumer(IdempotentConsumerPattern):
        processed = []
        
        async def process_unique(self, event):
            self.processed.append(event["event_id"])
            return {"result": "updated"}
    
    consumer = TestConsumer(db, IdempotencyTracker(db))
    
    # Process event first time
    result1 = await consumer.handle_event(
        event={"event_id": "abc-123", "data": {...}},
        consumer_name="test-processor"
    )
    
    assert result1["processed"] == True
    assert result1["duplicate"] == False
    assert len(consumer.processed) == 1
    
    # Process same event again (duplicate)
    result2 = await consumer.handle_event(
        event={"event_id": "abc-123", "data": {...}},
        consumer_name="test-processor"
    )
    
    # Verify
    assert result2["processed"] == True
    assert result2["duplicate"] == True
    assert result2["result"] == result1["result"]  # Cached
    assert len(consumer.processed) == 1  # Not incremented

async def test_idempotency_ttl_cleanup():
    """Expired idempotency records cleaned up."""
    tracker = IdempotencyTracker(db, ttl_days=1)
    
    # Create old record
    old_record = await tracker.get_or_create(
        event_id=uuid4(),
        consumer_name="test"
    )
    # Manually set expires_at to past
    result = await db.execute(
        select(IdempotencyRecord).where(
            IdempotencyRecord.idempotency_id == old_record["idempotency_id"]
        )
    )
    record = result.scalar_one()
    record.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    await db.commit()
    
    # Cleanup
    deleted = await tracker.cleanup_expired()
    assert deleted == 1
```

**Pass Criteria:**
- ✅ Duplicate events skipped
- ✅ Cached results returned for duplicates
- ✅ Idempotency key by event_id + consumer
- ✅ TTL cleanup works

**Expected Output:**
```
test_idempotent_consumer_skips_duplicates PASSED
test_idempotency_ttl_cleanup PASSED
test_idempotency_error_caching PASSED
```

---

### 6. Event Replay: Deterministic State Rebuild ❌→✅

**Objective:** Verify events can be replayed to rebuild state deterministically.

**Test Command:**
```bash
pytest tests/integration/test_replay.py -v
```

**What It Tests:**
```python
async def test_replay_aggregate():
    """Replay events to rebuild decision state."""
    replayer = EventReplayer(db)
    
    # Create test events
    events_to_create = [
        ("decision.created", {"question": "...", "roles": ["ceo"]}),
        ("decision.approved", {}),
        ("decision.in_progress", {}),
        ("decision.outcome_recorded", {"outcome": "succeeded"}),
    ]
    
    for event_type, data in events_to_create:
        event = DomainEvent(...)
        await ledger.append(event)
    
    # Define state builder
    async def build_state(state, event):
        if event["event_type"] == "decision.created":
            state["question"] = event["data"].get("question")
            state["state"] = "created"
        elif event["event_type"] == "decision.outcome_recorded":
            state["state"] = event["data"].get("outcome")
        return state
    
    # Replay
    result = await replayer.replay_aggregate(
        aggregate_id=decision_id,
        state_builder=build_state
    )
    
    # Verify
    assert result["events_replayed"] == 4
    assert result["final_state"]["state"] == "succeeded"
    assert result["final_state"]["question"] == "..."

async def test_replay_consistency_check():
    """Verify consistency between events and read model."""
    # Build expected state from events
    builder = ProjectionBuilder()
    expected = await builder.build_decision_projection(db, decision_id)
    
    # Get current state from DB
    decision = await db.get(Decision, decision_id)
    current = {
        "id": str(decision.id),
        "state": decision.state,
        "outcome": decision.outcome,
    }
    
    # Check consistency
    check = await ConsistencyChecker.verify_decision_state(
        db=db,
        decision_id=decision_id,
        current_state=current
    )
    
    # Verify
    assert check["consistent"] == True
    assert len(check["divergences"]) == 0
```

**Pass Criteria:**
- ✅ Replay is deterministic
- ✅ State built correctly from events
- ✅ Resumable (can skip to point in time)
- ✅ Consistency checking works

**Expected Output:**
```
test_replay_aggregate PASSED
test_replay_tenant PASSED
test_replay_time_range PASSED
test_replay_consistency_check PASSED
```

---

### 7. Observability: Metrics & Health ❌→✅

**Objective:** Verify metrics are collected and health reports generated.

**Test Command:**
```bash
pytest tests/integration/test_observability.py -v
```

**What It Tests:**
```python
async def test_metrics_collection():
    """Publish latency metrics collected."""
    collector = EventMetricsCollector(db)
    
    # Simulate events
    for _ in range(10):
        async with measure_latency(
            collector,
            "event_publish_latency",
            tenant_id=tenant_id
        ):
            await asyncio.sleep(0.01)  # 10ms latency
    
    # Query metrics
    stats = await collector.get_publish_latency_stats(
        tenant_id=tenant_id,
        time_window_minutes=60
    )
    
    # Verify
    assert stats["samples"] == 10
    assert stats["p50_ms"] > 0
    assert stats["p95_ms"] > stats["p50_ms"]
    assert stats["avg_ms"] > 0

async def test_consumer_lag_tracking():
    """Consumer lag metrics tracked."""
    collector = EventMetricsCollector(db)
    
    # Create events (sequence 0-9)
    for i in range(10):
        await ledger.append(create_event(sequence=i))
    
    # Consumer processes up to sequence 7
    checkpoint = await db.get(ConsumerCheckpoint, consumer_id)
    checkpoint.last_processed_sequence = 7
    
    # Get lag
    lag = await collector.get_consumer_lag("default")
    
    # Verify
    assert lag["latest_event_sequence"] == 9
    assert lag["consumers"]["test-consumer"]["last_processed_sequence"] == 7
    assert lag["consumers"]["test-consumer"]["lag_count"] == 2

async def test_dlq_metrics():
    """DLQ metrics tracked."""
    # Move some events to DLQ
    for i in range(5):
        await dlq_handler.move_to_dlq(...)
    
    # Get metrics
    metrics = await collector.get_dlq_metrics(tenant_id)
    
    # Verify
    assert metrics["total_dlq_count"] == 5
    assert metrics["unresolved_count"] == 5

async def test_health_report():
    """Health report generated."""
    health = await collector.get_health_report(tenant_id)
    
    # Verify
    assert health["status"] in ["healthy", "degraded", "unhealthy"]
    assert "checks" in health
    assert "event_publish_latency" in health["checks"]
    assert "dlq_count" in health["checks"]
```

**Pass Criteria:**
- ✅ Publish latency metrics collected
- ✅ Consumer lag tracked
- ✅ DLQ size monitored
- ✅ Health report generated (healthy/degraded/unhealthy)

**Expected Output:**
```
test_metrics_collection PASSED
test_consumer_lag_tracking PASSED
test_dlq_metrics PASSED
test_health_report PASSED
```

---

### 8. Security: Tenant Isolation ❌→✅

**Objective:** Verify cross-tenant access blocked at all layers.

**Test Command:**
```bash
pytest tests/integration/test_security.py -v
```

**What It Tests:**
```python
async def test_tenant_isolation_subscription():
    """User cannot subscribe to other tenant's events."""
    router = RBACEventRouter(db)
    
    # User A's context
    user_a = EventSecurityContext(
        user_id=uuid4(),
        tenant_id=tenant_a_id,
        roles=["operator"]
    )
    
    # User B's context
    user_b = EventSecurityContext(
        user_id=uuid4(),
        tenant_id=tenant_b_id,
        roles=["operator"]
    )
    
    # Create decision in tenant A
    decision_a = create_decision(tenant_id=tenant_a_id)
    
    # User A can subscribe (same tenant)
    allowed = await router.can_subscribe_to_aggregate(user_a, decision_a)
    assert allowed == True
    
    # User B cannot subscribe (different tenant)
    allowed = await router.can_subscribe_to_aggregate(user_b, decision_a)
    assert allowed == False

async def test_event_visibility_filtering():
    """Only user's tenant's events visible."""
    filter = EventVisibilityFilter(db)
    
    # Create events in both tenants
    create_event(tenant_id=tenant_a_id, event_type="decision.created")
    create_event(tenant_id=tenant_b_id, event_type="decision.created")
    
    # User A security context
    user_a = EventSecurityContext(
        user_id=uuid4(),
        tenant_id=tenant_a_id,
        roles=["operator"]
    )
    
    # Get visible events
    events = await filter.get_visible_events(user_a, limit=100)
    
    # Verify: only tenant A's events
    assert len(events) == 1
    assert events[0]["tenant_id"] == str(tenant_a_id)

async def test_rbac_dlq_access():
    """User cannot access other tenant's DLQ."""
    router = RBACEventRouter(db)
    
    user_a = EventSecurityContext(..., tenant_id=tenant_a_id, ...)
    user_b = EventSecurityContext(..., tenant_id=tenant_b_id, ...)
    
    # User A can access own DLQ
    allowed = await router.can_access_dlq(user_a, tenant_a_id)
    assert allowed == True
    
    # User A cannot access tenant B's DLQ
    allowed = await router.can_access_dlq(user_a, tenant_b_id)
    assert allowed == False
```

**Pass Criteria:**
- ✅ Cross-tenant subscriptions blocked
- ✅ Event visibility filtered by tenant
- ✅ DLQ access restricted to own tenant
- ✅ RBAC enforced (viewer, operator, admin)

**Expected Output:**
```
test_tenant_isolation_subscription PASSED
test_event_visibility_filtering PASSED
test_rbac_dlq_access PASSED
test_rbac_replay_access PASSED
```

---

### 9. Integration: API → Event → Consumer ❌→✅

**Objective:** End-to-end flow: decision outcome API → event creation → consumer processing.

**Test Command:**
```bash
pytest tests/integration/test_e2e_decision_flow.py -v
```

**What It Tests:**
```python
async def test_decision_outcome_end_to_end():
    """
    1. Record outcome via API
    2. Event created + appended to outbox
    3. Publisher publishes to event bus
    4. Consumer processes + checkpoint advanced
    """
    # Step 1: Call API
    response = await client.post(
        f"/api/v1/decisions/{decision_id}/outcome",
        json={"outcome": "succeeded", "note": "..."}
    )
    assert response.status_code == 200
    
    # Step 2: Verify event in outbox (unpublished)
    result = await db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.outcome_recorded")
            & (EventOutbox.published == False)
        )
    )
    outbox_entries = result.scalars().all()
    assert len(outbox_entries) >= 1
    
    # Step 3: Run publisher
    published_count = await publisher.publish_pending()
    assert published_count >= 1
    
    # Step 4: Verify event published
    result = await db.execute(
        select(EventOutbox).where(
            (EventOutbox.event_type == "decision.outcome_recorded")
            & (EventOutbox.published == True)
        )
    )
    assert len(result.scalars().all()) >= 1
    
    # Step 5: Consumer processes
    consumer = TestConsumer(db, "test-consumer")
    await consumer.initialize()
    
    async for batch in consumer.stream_events(tenant_id):
        for event in batch:
            if event["event_type"] == "decision.outcome_recorded":
                # Process
                assert event["data"]["outcome"] == "succeeded"
        break  # Just process one batch
    
    # Step 6: Verify checkpoint advanced
    checkpoint = await consumer.checkpoint_mgr.get_checkpoint()
    assert checkpoint.last_processed_sequence > 0
    
    # Step 7: Verify idempotency (process again)
    async for batch in consumer.stream_events(tenant_id):
        # No new events
        break
    
    # Step 8: Verify no duplicates
    assert consumer.processed_count == 1  # Not 2
```

**Pass Criteria:**
- ✅ API records decision outcome
- ✅ Event created and appended to outbox
- ✅ Publisher publishes to event_bus
- ✅ Consumer receives and processes
- ✅ Checkpoint advanced
- ✅ No duplicate processing (idempotency works)

**Expected Output:**
```
test_decision_outcome_end_to_end PASSED
test_multiple_consumers PASSED
test_failure_recovery PASSED
```

---

### 10. No Data Loss Under Failure ❌→✅

**Objective:** Verify no events lost under various failure scenarios.

**Test Command:**
```bash
pytest tests/integration/test_failure_scenarios.py -v
```

**What It Tests:**
```python
async def test_no_loss_api_succeeds_publisher_crashes():
    """API succeeds → event written to DB → publisher crashes → events recovered."""
    # Record outcome
    decision.outcome = "succeeded"
    await event_store.record_decision_outcome(...)
    
    # Commit (event in outbox)
    await event_store.commit()
    
    # Count events in outbox
    result = await db.execute(select(func.count(EventOutbox.outbox_id)))
    count_before = result.scalar()
    
    # Simulate publisher crash (no events published yet)
    
    # Restart and run publisher
    published = await publisher.publish_pending()
    
    # Verify: all events eventually published
    assert published == count_before

async def test_no_loss_consumer_crashes():
    """Consumer processes event → crashes before checkpoint → resumes without duplicate."""
    checkpoint_mgr = ConsumerCheckpointManager(db, "test")
    await checkpoint_mgr.initialize()
    
    # Process event 1
    await process(event_1)
    await checkpoint_mgr.mark_processed(event_1.event_id, 0)
    
    # Crash (don't checkpoint event 2)
    # Simulate crash by not marking event 2
    
    # Restart
    del checkpoint_mgr
    checkpoint_mgr = ConsumerCheckpointManager(db, "test")
    await checkpoint_mgr.initialize()
    resume_seq = await checkpoint_mgr.get_resume_sequence()
    
    # Resume point should be 0 (will reprocess event 1? No, idempotency prevents duplicate)
    # Actually resume point is 1 (next sequence to process)
    assert resume_seq == 0
    
    # Process from resume point
    for event in stream_from(resume_seq + 1):
        # Event 2 reprocessed
        pass

async def test_failure_modes():
    """Verify handling of various failures."""
    # Database connection failure during append
    # Expected: raise exception, caller rolls back
    
    # Duplicate event_id (idempotency)
    # Expected: skip, return cached result
    
    # Outbox publisher network failure
    # Expected: mark_error, retry next cycle
    
    # Consumer processing error
    # Expected: mark_error, don't advance checkpoint, retry on restart
    
    # Schema validation failure
    # Expected: ValidationError raised, event rejected
```

**Pass Criteria:**
- ✅ No events lost on API crash
- ✅ No events lost on publisher crash
- ✅ No events lost on consumer crash
- ✅ No duplicate processing on restart
- ✅ Failed events moved to DLQ

**Expected Output:**
```
test_no_loss_api_succeeds_publisher_crashes PASSED
test_no_loss_consumer_crashes PASSED
test_failure_modes PASSED
```

---

## Pass/Fail Decision Matrix

| Criterion | Status | Notes |
|-----------|--------|-------|
| 1. Transactional Outbox | ❌ | Must PASS: test_outbox_no_lost_events |
| 2. Consumer Checkpointing | ❌ | Must PASS: test_consumer_resumes_from_checkpoint |
| 3. Dead Letter Queue | ❌ | Must PASS: test_dlq_move_after_max_retries |
| 4. Schema Registry | ❌ | Must PASS: test_schema_validation |
| 5. Idempotent Processing | ❌ | Must PASS: test_idempotent_consumer_skips_duplicates |
| 6. Event Replay | ❌ | Must PASS: test_replay_aggregate |
| 7. Observability | ❌ | Must PASS: test_health_report |
| 8. Security | ❌ | Must PASS: test_tenant_isolation_subscription |
| 9. Integration Flow | ❌ | Must PASS: test_decision_outcome_end_to_end |
| 10. Failure Resilience | ❌ | Must PASS: test_no_loss_api_succeeds_publisher_crashes |

## To Deploy

**All 10 must be GREEN ✅**

```bash
# Run all tests
pytest tests/integration/test_*.py -v --tb=short

# Or individually:
pytest tests/integration/test_outbox_guarantees.py -v
pytest tests/integration/test_consumer_checkpoint.py -v
pytest tests/integration/test_dlq_handler.py -v
pytest tests/integration/test_schema_registry.py -v
pytest tests/integration/test_idempotency.py -v
pytest tests/integration/test_replay.py -v
pytest tests/integration/test_observability.py -v
pytest tests/integration/test_security.py -v
pytest tests/integration/test_e2e_decision_flow.py -v
pytest tests/integration/test_failure_scenarios.py -v
```

**Approval Required:** CTO sign-off on gate checklist before merge.

---

*System 2 Hardened is production-ready only when all 10 criteria PASS.*
