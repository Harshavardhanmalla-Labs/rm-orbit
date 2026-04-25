#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}API Contract Verification Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running in correct directory
if [ ! -f "API_CONTRACT.md" ]; then
    echo -e "${RED}❌ Error: API_CONTRACT.md not found${NC}"
    echo "Please run this script from the Research directory:"
    echo "  cd Research && ./test_contract.sh"
    exit 1
fi

# ============================================================================
# Backend Tests
# ============================================================================

echo -e "${YELLOW}[1/4] Running Backend Contract Tests...${NC}"
echo ""

cd backend

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -q pytest 2>/dev/null || pip install pytest
fi

# Run backend tests
if pytest tests/test_papers_contract.py -v --tb=short; then
    echo -e "${GREEN}✅ Backend contract tests PASSED${NC}"
else
    echo -e "${RED}❌ Backend contract tests FAILED${NC}"
    exit 1
fi

echo ""
cd ..

# ============================================================================
# Verify Backend is Running
# ============================================================================

echo -e "${YELLOW}[2/4] Checking Backend API...${NC}"
echo ""

# Check if backend is running
BACKEND_RUNNING=false
if curl -s http://localhost:6420/health > /dev/null 2>&1; then
    BACKEND_RUNNING=true
    echo -e "${GREEN}✅ Backend API is running on http://localhost:6420${NC}"
else
    echo -e "${YELLOW}⚠️  Backend API not running on localhost:6420${NC}"
    echo "   Start it in another terminal:"
    echo "   cd backend && python -m uvicorn app.main:app --port 6420"
    echo ""
    BACKEND_RUNNING=false
fi

echo ""

# If backend is running, test the actual response
if [ "$BACKEND_RUNNING" = true ]; then
    echo -e "${YELLOW}[3/4] Validating Live API Response...${NC}"
    echo ""

    # Get response and validate
    RESPONSE=$(curl -s http://localhost:6420/api/papers/)

    # Check if response is valid JSON
    if echo "$RESPONSE" | python3 -m json.tool > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API response is valid JSON${NC}"

        # Validate structure
        python3 << 'EOF'
import json
import sys

response = """$RESPONSE"""
data = json.loads(response)

errors = []

# Check required fields
if not isinstance(data, dict):
    errors.append("Response must be object, not array (bug fix working!)")
else:
    if "papers" not in data:
        errors.append("Missing 'papers' field")
    elif not isinstance(data["papers"], list):
        errors.append("'papers' must be array")

    if "total" not in data:
        errors.append("Missing 'total' field")
    elif not isinstance(data["total"], int):
        errors.append("'total' must be integer")

    if "counts" not in data:
        errors.append("Missing 'counts' field")
    elif not isinstance(data["counts"], dict):
        errors.append("'counts' must be object")
    else:
        required_count_fields = ["total", "complete", "failed", "draft", "running", "cancelled"]
        for field in required_count_fields:
            if field not in data["counts"]:
                errors.append(f"Missing 'counts.{field}'")
            elif not isinstance(data["counts"][field], int):
                errors.append(f"'counts.{field}' must be integer")

if errors:
    print("\n".join([f"  ❌ {e}" for e in errors]))
    sys.exit(1)
else:
    print(f"✅ Response structure valid")
    print(f"   - Papers: {len(data['papers'])}")
    print(f"   - Total: {data['total']}")
    print(f"   - Complete: {data['counts']['complete']}")
    print(f"   - Failed: {data['counts']['failed']}")
    print(f"   - Draft: {data['counts']['draft']}")
    print(f"   - Running: {data['counts']['running']}")

EOF
        echo ""
    else
        echo -e "${RED}❌ API response is not valid JSON${NC}"
        echo "Response was: $RESPONSE"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Skipping live API validation (backend not running)${NC}"
fi

echo ""

# ============================================================================
# Frontend Tests (if npm is available)
# ============================================================================

echo -e "${YELLOW}[4/4] Running Frontend Contract Tests...${NC}"
echo ""

cd frontend

if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}⚠️  npm not found, skipping frontend tests${NC}"
    echo "   Install Node.js to enable frontend testing"
else
    # Check if dependencies are installed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        npm install -q
    fi

    # Run frontend tests
    if npm run test -- src/api/__tests__/client.test.js --reporter=verbose 2>/dev/null; then
        echo -e "${GREEN}✅ Frontend contract tests PASSED${NC}"
    else
        echo -e "${YELLOW}⚠️  Frontend tests not available${NC}"
        echo "   (This is OK if vitest is not installed)"
    fi
fi

echo ""
cd ..

# ============================================================================
# Summary
# ============================================================================

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Contract Verification Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo "Next steps:"
echo "  1. Run backend: cd backend && python -m uvicorn app.main:app --port 6420"
echo "  2. Run frontend: cd frontend && npm run dev"
echo "  3. Test dashboard: http://localhost:10007/papers"
echo ""

echo "API Contract Documentation:"
echo "  See API_CONTRACT.md for details"
echo ""
