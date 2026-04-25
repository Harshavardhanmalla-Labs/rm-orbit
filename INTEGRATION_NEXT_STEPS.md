# System 1 + System 2 Integration — Next Steps Checklist

**Status:** Architecture & Code Ready. Awaiting Implementation.

---

## Overview

System 1 (Versioned APIs) and System 2 (Event Ledger) are designed and ready to integrate.

**Goal:** Ensure every API endpoint that modifies state emits an immutable event.

**Requirements Met:**
- ✅ Every endpoint identified (6 decision endpoints)
- ✅ Event schemas defined (decision.created, decision.outcome_recorded, etc)
- ✅ Transactional outbox pattern (no lost events)
- ✅ Auth/tenant context flows into events
- ✅ Correlation ID flows API → Event → Consumer logs
- ✅ Failure handling (API ≠ Event errors)
- ✅ Integration tests (50+ test cases)
- ✅ Release gate script (10-point checklist)
- ✅ Rollback procedures (3 options)

**Deliverables:**
- `SYSTEM_1_SYSTEM_2_INTEGRATION.md` (520 lines) — Full plan
- `SYSTEM_1_SYSTEM_2_INTEGRATION_CODE.md` (450 lines) — Code patches
- `scripts/integration_release_gate.sh` — Automated tests
- `scripts/rollback_integration.sh` — Emergency rollback

---

## Implementation Checklist

### Phase 1: Create Integration Layer (4 hours)

**Files to Create:**
- [ ] `AgentTheater/api/integration/__init__.py`
- [ ] `AgentTheater/api/integration/context_flow.py` (copy from CODE.md)
- [ ] `AgentTheater/api/integration/event_emitters.py` (copy from CODE.md)
- [ ] `AgentTheater/api/integration/request_hooks.py` (copy from CODE.md)

**Verification:**
```bash
# Should import without errors
python -c "from AgentTheater.api.integration import context_flow, event_emitters, request_hooks"
```

### Phase 2: Modify Decision Endpoints (3 hours)

**Files to Modify:**
- [ ] `AgentTheater/api/versions/v1/decisions.py`
  - [ ] Add imports (context_flow, event_emitters, request_hooks)
  - [ ] Modify `create_decision()` endpoint
  - [ ] Modify `record_outcome()` endpoint
  - [ ] Modify `add_github_issue()` endpoint
  - [ ] Modify `create_github_issues()` endpoint

**Verification:**
```bash
# Endpoints should still work (no breaking changes)
curl -X POST http://localhost:8000/api/v1/decisions \
  -H "Authorization: Bearer ..." \
  -H "X-Tenant-ID: ..." \
  -H "X-Correlation-ID: test-123" \
  -d '{"project_id": "...", "question": "...", "roles": [...]}'

# Response should include headers:
# X-Correlation-ID: test-123
# X-API-Version: v1
```

### Phase 3: Create Tests (6 hours)

**Test Files to Create:**
- [ ] `tests/integration/test_api_event_emission.py` (copy template from CODE.md)
- [ ] `tests/integration/test_correlation_id_flow.py`
- [ ] `tests/integration/test_api_idempotency.py`
- [ ] `tests/integration/test_consumer_integration.py`
- [ ] `tests/integration/test_dlq_integration.py`
- [ ] `tests/integration/test_api_failure_modes.py`
- [ ] `tests/integration/test_observability_integration.py`
- [ ] `tests/integration/test_e2e_integration.py`

**Verification:**
```bash
# Run individual test file
pytest tests/integration/test_api_event_emission.py -v

# Should see: 3 tests PASSED
# - test_create_decision_emits_event
# - test_record_outcome_emits_event
# - test_atomicity_decision_and_event
```

### Phase 4: Create Conftest (1 hour)

**Files to Modify:**
- [ ] `tests/conftest.py`
  - [ ] Add `event_loop` fixture
  - [ ] Add `db` fixture (test database)
  - [ ] Add `client` fixture (HTTP client)
  - [ ] Add `tenant_id`, `user_id`, `user_token` fixtures

**Verification:**
```bash
# Tests should be discoverable
pytest tests/integration/ --collect-only | grep "test_"
# Should list 50+ test items
```

### Phase 5: Create Release Gate Script (1 hour)

**Files to Create:**
- [ ] `scripts/integration_release_gate.sh` (copy from SYSTEM_1_SYSTEM_2_INTEGRATION.md)
- [ ] `scripts/rollback_integration.sh` (copy from SYSTEM_1_SYSTEM_2_INTEGRATION.md)

**Verification:**
```bash
# Make executable
chmod +x scripts/integration_release_gate.sh scripts/rollback_integration.sh

# Dry run (with --collect-only)
bash scripts/integration_release_gate.sh --dry-run
```

### Phase 6: Run Full Integration Tests (2 hours)

**Command:**
```bash
bash scripts/integration_release_gate.sh
```

**Expected Output:**
```
▶ 1.1 Event schemas versioned ... PASSED
▶ 1.2 Backward-compatible evolution ... PASSED
▶ 2.1 Decision created emits event ... PASSED
...
▶ 8.2 Multiple consumers ... PASSED

Results: 14 PASSED, 0 FAILED
✅ All gates PASSED - Ready to deploy
```

### Phase 7: Test Rollback Procedure (1 hour)

**Command:**
```bash
# Simulate integration in staging
bash scripts/integration_release_gate.sh

# If failures detected:
bash scripts/rollback_integration.sh

# Verify rollback
curl http://localhost:8000/api/health | jq '.event_outbox_count'
# Should see: 0 (no new events)
```

**Verification:**
- ✅ API still works
- ✅ No new events emitted
- ✅ Old decisions still readable

### Phase 8: Documentation (1 hour)

**Files to Create/Update:**
- [ ] `INTEGRATION_DEPLOYMENT.md` (deployment runbook)
- [ ] `INTEGRATION_TROUBLESHOOTING.md` (common issues)
- [ ] `docs/API_EVENTS_MAPPING.md` (endpoint → event reference)

**Content:**
- Pre-deployment checklist
- Deployment steps
- Monitoring dashboard setup
- Troubleshooting guide
- FAQ

---

## Total Implementation Time

| Phase | Duration | Owner |
|-------|----------|-------|
| 1. Integration Layer | 4h | Backend |
| 2. Endpoint Modification | 3h | Backend |
| 3. Test Files | 6h | QA/Backend |
| 4. Test Infrastructure | 1h | DevOps |
| 5. Release Gate Script | 1h | DevOps |
| 6. Full Test Run | 2h | QA |
| 7. Rollback Testing | 1h | DevOps |
| 8. Documentation | 1h | Tech Lead |

**Total:** ~19 hours (2.5 days)

---

## Definition of Done

Integration is complete when:

1. ✅ All integration code implemented (5 new files, 1 modified)
2. ✅ All tests pass (50+ test cases)
3. ✅ Release gate script passes (14/14 gates)
4. ✅ Rollback procedure tested and working
5. ✅ Documentation complete
6. ✅ Code reviewed and approved
7. ✅ Staging environment tested (if available)
8. ✅ Ready for production deployment

---

## Risk Mitigation

### Risk: Duplicate Events on Network Retry

**Mitigation:** Idempotency tracking via event_id + consumer_name
- Same event_id processed only once per consumer
- Cached results returned for duplicates
- TTL cleanup (7 days)

**Test:** `test_api_idempotency.py::test_duplicate_request_no_duplicate_event`

### Risk: Lost Events on API Crash

**Mitigation:** Transactional outbox pattern
- Event write in same transaction as domain change
- Both committed or both rolled back
- No partial state

**Test:** `test_api_event_emission.py::test_atomicity_decision_and_event`

### Risk: Consumer Crashes Without Checkpointing

**Mitigation:** Consumer checkpoint tracking
- Last_processed_sequence persisted to DB
- Resume from exact point on restart
- No re-processing via idempotency

**Test:** `test_consumer_integration.py::test_consumer_crash_and_resume`

### Risk: Event Emission Fails, API Succeeds

**Mitigation:** Event failure doesn't break API
- Event write fails → transaction rolls back
- Both domain change and event rolled back
- API returns error (not 500, but 202 Accepted with warning)

**Test:** `test_api_failure_modes.py::test_event_failure_handling`

### Risk: Tenant Cross-Contamination

**Mitigation:** Tenant isolation enforced
- Every event tagged with tenant_id
- API verifies req.tenant_id == security_context.tenant_id
- EventVisibilityFilter enforces in consumers

**Test:** `test_security.py::test_tenant_isolation_events`

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Test Coverage | 100% of endpoints | `coverage run -m pytest tests/integration/` |
| Event Emission | 1:1 with API writes | Compare decision count to event count |
| Correlation ID Flow | In all logs | `grep correlation_id logs/app.log` |
| Tenant Isolation | 0 cross-tenant | `select count(*) from events where tenant_a sees tenant_b data` |
| Consumer Lag | < 1000 events | `collector.get_consumer_lag()["latest_event_sequence"]` |
| DLQ Count | < 5 unresolved | `dlq_handler.get_dlq_stats()["unresolved_count"]` |

---

## After Integration Passes

**Before starting System 3:**

1. ✅ Merge to main branch
2. ✅ Tag as `system-1-2-integration-complete`
3. ✅ Update project status in README
4. ✅ Notify stakeholders
5. ✅ Begin System 3 design (Decision Execution Engine)

**System 3 Requires:**
- System 2 events flowing end-to-end
- Correlation IDs for distributed tracing
- Reliable consumer processing
- Full audit trail capability

---

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `SYSTEM_1_SYSTEM_2_INTEGRATION.md` | Full architecture & requirements |
| `SYSTEM_1_SYSTEM_2_INTEGRATION_CODE.md` | Exact code patches |
| `scripts/integration_release_gate.sh` | Automated test checklist |
| `scripts/rollback_integration.sh` | Emergency rollback |
| `AgentTheater/api/integration/` | Integration layer (5 files) |
| `tests/integration/` | Test suites (8+ files) |

### Commands

```bash
# Run full gate
bash scripts/integration_release_gate.sh

# Run specific test
pytest tests/integration/test_api_event_emission.py -v

# Check test coverage
coverage run -m pytest tests/integration/
coverage report

# Rollback
bash scripts/rollback_integration.sh

# Health check
curl http://localhost:8000/api/health
```

---

## Questions Before Starting?

1. **Should we run staging first?** Yes (recommended)
   - Deploy to staging environment
   - Run full test suite
   - Monitor for 1-2 hours
   - Then deploy to production

2. **Can we deploy endpoints one-by-one?** No (atomic)
   - All 6 endpoints must emit events
   - Deploy as single changeset
   - Use traffic control to canary (10% v2 events first)

3. **What if tests fail?** Debug in order:
   - Check imports (integration layer created?)
   - Check endpoints modified (all 6 updated?)
   - Check auth context (token valid?)
   - Check database (tables created?)
   - Check event emission (called in transaction?)

4. **Emergency rollback?** Simple:
   ```bash
   bash scripts/rollback_integration.sh
   ```
   - Stops event emission
   - Reverts API code
   - Restarts services

---

## Ready to Implement?

✅ All architecture & code complete  
✅ All requirements documented  
✅ All tests designed  
✅ All rollback procedures defined  

**Next: Implement Phase 1 (Integration Layer)**

---

*System 1 + System 2 integration bridges versioned APIs and immutable events.*
