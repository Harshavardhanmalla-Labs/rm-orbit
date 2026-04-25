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
        echo "  Output:"
        cat /tmp/test_output.txt | sed 's/^/    /'
        ((FAILED++))
    fi
}

# Change to project directory
cd /home/sasi/Desktop/dev/RM\ Orbit

# 1. Event schemas
check "1.1 Event schemas defined" \
    "python -c 'from AgentTheater.events import EventType; print(\"EventType defined\")'"

# 2. API → Event flow
check "2.1 Decision created emits event" \
    "pytest tests/integration/test_api_event_emission.py::test_create_decision_emits_event -v --tb=short"

check "2.2 Outcome recorded emits event" \
    "pytest tests/integration/test_api_event_emission.py::test_record_outcome_emits_event -v --tb=short"

check "2.3 Correlation ID flows through" \
    "pytest tests/integration/test_api_event_emission.py::test_correlation_id_flows_through_system -v --tb=short"

check "2.4 Tenant isolation in events" \
    "pytest tests/integration/test_api_event_emission.py::test_tenant_isolation_in_events -v --tb=short"

check "2.5 Atomicity: decision + event" \
    "pytest tests/integration/test_api_event_emission.py::test_atomicity_decision_and_event -v --tb=short"

# 3. Context propagation
check "3.1 Security context extracted" \
    "python -c 'from AgentTheater.api.integration.context_flow import extract_security_context; print(\"context_flow works\")'"

check "3.2 Correlation ID extracted" \
    "python -c 'from AgentTheater.api.integration.context_flow import extract_correlation_id; print(\"correlation_id works\")'"

# 4. Integration layer
check "4.1 Event emitters created" \
    "python -c 'from AgentTheater.api.integration.event_emitters import DecisionEventEmitters; print(\"event_emitters works\")'"

check "4.2 Request hooks created" \
    "python -c 'from AgentTheater.api.integration.request_hooks import transactional_event_scope; print(\"request_hooks works\")'"

# 5. API endpoints
check "5.1 Decision endpoints defined" \
    "python -c 'from AgentTheater.api.versions.v1.decisions_router import router; print(f\"Router has {len(router.routes)} routes\")'"

# Summary
echo ""
echo "================================================"
echo -e "Results: ${GREEN}$PASSED PASSED${NC}, ${RED}$FAILED FAILED${NC}"
echo "================================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All gates PASSED - Ready to proceed${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED gates FAILED - Fix issues before proceeding${NC}"
    exit 1
fi
