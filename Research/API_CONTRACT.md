# API Contract Documentation

**Last Updated:** 2026-04-25  
**Version:** 1.1.0  
**Status:** Active

## Overview

This document defines the API contract between the FastAPI backend and React frontend. Both sides MUST conform to this contract, or tests will fail and alert the team.

---

## Endpoints

### GET /api/papers/

**Purpose:** List all papers with metadata and status counts.

**Backend Implementation:**
- File: `app/api/papers.py` 
- Response Model: `PapersListResponse` (Pydantic)
- Function: `list_papers()` (lines ~141-177)

**Frontend Usage:**
- File: `src/pages/PapersList.jsx`
- Type: `PapersListResponse` (TypeScript)
- Parser: `validatePapersListResponse()` in `src/api/client.js`

**Response Schema:**

```json
{
  "papers": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Advanced ML Techniques",
      "topic": "Machine Learning",
      "niche": "Deep Learning",
      "target_venue": "arxiv",
      "paper_type": "original_research",
      "status": "complete",
      "current_stage": "complete",
      "stage_progress": 100.0,
      "created_at": "2026-04-25T10:30:00Z"
    }
  ],
  "total": 1,
  "counts": {
    "total": 1,
    "complete": 1,
    "failed": 0,
    "draft": 0,
    "running": 0,
    "cancelled": 0
  }
}
```

**Required Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `papers` | Array | ✓ | List of PaperBase objects |
| `total` | integer | ✓ | Total number of papers (must equal papers.length) |
| `counts` | object | ✓ | Status count breakdown |
| `counts.total` | integer | ✓ | Total papers |
| `counts.complete` | integer | ✓ | Papers with status="complete" |
| `counts.failed` | integer | ✓ | Papers with status="failed" |
| `counts.draft` | integer | ✓ | Papers with status="intake" |
| `counts.running` | integer | ✓ | Papers with status="processing" or "running" |
| `counts.cancelled` | integer | ✓ | Papers with status="cancelled" |

**Paper Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✓ | UUID |
| `title` | string | null | Paper title |
| `topic` | string | null | Research topic |
| `niche` | string | null | Academic niche |
| `target_venue` | string | null | Publication venue |
| `paper_type` | string | null | Paper category |
| `status` | string | ✓ | One of: intake, processing, running, complete, failed, cancelled |
| `current_stage` | string | null | Current pipeline stage |
| `stage_progress` | number | null | Progress 0-100 |
| `created_at` | string | ✓ | ISO timestamp |

---

## How Contract Validation Works

### Backend (Python/FastAPI)

1. **Pydantic Models Define Schema** (`app/api/papers.py`):
   ```python
   class PapersListResponse(BaseModel):
       papers: List[PaperBase] = Field(...)
       total: int = Field(..., ge=0)
       counts: PapersListCounts = Field(...)
   ```

2. **Endpoint Uses Response Model** (`app/api/papers.py`):
   ```python
   @router.get("/", response_model=PapersListResponse)
   async def list_papers() -> PapersListResponse:
       # Build response
       return PapersListResponse(papers=papers, total=total, counts=counts)
   ```

3. **FastAPI Auto-Validates**:
   - Pydantic validates at runtime
   - OpenAPI schema is auto-generated from models
   - Invalid responses raise 500 error

### Frontend (TypeScript/React)

1. **TypeScript Types Match Backend** (`src/api/types.ts`):
   ```typescript
   export interface PapersListResponse {
     papers: Paper[]
     total: number
     counts: PapersListCounts
   }
   ```

2. **API Client Validates Responses** (`src/api/client.js`):
   ```javascript
   api.interceptors.response.use((response) => {
     if (response.config.url?.includes('/api/papers/')) {
       validatePapersListResponse(response.data)
     }
     return response
   })
   ```

3. **Clear Errors on Mismatch**:
   - Raw array response: "API contract violation: Expected {papers: Array...}, but got raw array"
   - Missing field: "API contract violation: 'papers' must be array..."
   - Type mismatch: "API contract violation: 'total' must be number..."

---

## Testing the Contract

### Backend Tests

Run backend contract tests:

```bash
cd Research/backend

# Run only papers contract tests
pytest tests/test_papers_contract.py -v

# Run with coverage
pytest tests/test_papers_contract.py --cov=app.api.papers

# Specific test
pytest tests/test_papers_contract.py::TestPapersListContract::test_papers_list_response_not_raw_array -v
```

**Key Tests:**

- ✓ Response has papers, total, counts fields
- ✓ Papers field is array (not raw response)
- ✓ Total is number
- ✓ Counts has all subfields
- ✓ Sum of counts equals total
- ✓ Paper statuses are valid
- ✓ Regression: raw array is rejected

### Frontend Tests

Run frontend contract tests:

```bash
cd Research/frontend

# Run API client tests
npm run test -- src/api/__tests__/client.test.js

# Watch mode
npm run test:watch -- src/api/__tests__/client.test.js

# Coverage
npm run test -- --coverage src/api/__tests__/client.test.js
```

**Key Tests:**

- ✓ Valid response accepted
- ✓ Raw array rejected
- ✓ Missing fields rejected
- ✓ Wrong types rejected
- ✓ Clear error messages

### Integration Test (Both Sides)

```bash
# Terminal 1: Backend
cd Research/backend
python -m uvicorn app.main:app --port 6420

# Terminal 2: Frontend
cd Research/frontend
npm run dev

# Terminal 3: Test
cd Research
./test_contract.sh  # (see script below)
```

**Script:** `Research/test_contract.sh`

```bash
#!/bin/bash
set -e

echo "Testing API Contract..."
echo ""

# Test 1: Backend API returns correct structure
echo "1. Testing backend response format..."
curl -s http://localhost:6420/api/papers/ | python3 -c "
import sys, json
data = json.load(sys.stdin)
assert isinstance(data, dict), 'Response must be object'
assert 'papers' in data, 'Missing papers'
assert 'total' in data, 'Missing total'
assert 'counts' in data, 'Missing counts'
assert isinstance(data['papers'], list), 'papers must be array'
assert isinstance(data['total'], int), 'total must be int'
print('✓ Backend response format valid')
"

# Test 2: Frontend can consume the response
echo "2. Testing frontend type compatibility..."
cd frontend
npm run test -- src/api/__tests__/client.test.js --reporter=verbose
cd ..

echo ""
echo "✅ All contract tests passed!"
```

---

## What Happens If Contract Breaks

### Scenario 1: Backend Returns Raw Array

**Error Trace:**
```
Frontend: API contract violation: Expected {papers: Array, total: number, counts: {...}}, but got raw array.
          Backend needs to return {papers: [...]}.
          See app/api/papers.py list_papers() endpoint.
Test: FAIL - test_papers_list_response_not_raw_array
```

**Fix:**
```python
# In app/api/papers.py, list_papers():
return PapersListResponse(papers=papers, total=total, counts=counts)  # ✓ Correct
# NOT: return papers  # ✗ Wrong
```

### Scenario 2: Backend Adds Optional Field

**No Problem** - TypeScript types use optional fields:
```typescript
title?: string  // Optional = null ok
```

Backward compatible.

### Scenario 3: Backend Removes Required Field

**Error Trace:**
```
Frontend: API contract violation: 'counts' must be object, got undefined.
Test: FAIL - test_papers_list_counts_structure
```

**Fix:** Add the field back, or update contract version and both test suites.

### Scenario 4: Backend Changes Field Type

**Error Trace:**
```
Backend: pydantic_core._pydantic_core.ValidationError: 'total' must be int, got str
Frontend: API contract violation: 'total' must be number, got string.
Test: FAIL - test_papers_list_total_is_number
```

**Fix:** Use correct type in endpoint.

---

## Contract Versioning

When you intentionally change the contract:

1. **Update Version Number** (this file):
   ```markdown
   **Version:** 1.2.0  (was 1.1.0)
   ```

2. **Document Change**:
   ```markdown
   ### v1.2.0 - 2026-05-15
   - Added `draft_count` field to counts
   - Changed `stage_progress` from integer to float
   ```

3. **Update Both Sides**:
   - Backend: Update Pydantic models
   - Frontend: Update TypeScript types
   - Both: Update tests

4. **Migration Support** (if needed):
   - New endpoint version (e.g., `/api/papers/v2/`)
   - Or deprecation period with both formats

---

## Checklist: Adding New Endpoints

When adding a new endpoint, ensure:

- [ ] Define Pydantic response model in backend
- [ ] Use `response_model=YourModel` in endpoint decorator
- [ ] Document schema in this file
- [ ] Create matching TypeScript interface
- [ ] Add validation in API client (if complex response)
- [ ] Write backend contract tests (pytest)
- [ ] Write frontend validation tests (vitest)
- [ ] Update this CONTRACT document
- [ ] Run both test suites to verify
- [ ] Update version number if breaking change

---

## References

**Backend:**
- Pydantic models: `app/api/papers.py` (lines 8-90)
- Endpoint: `app/api/papers.py` (lines 141-177)
- Tests: `tests/test_papers_contract.py`
- OpenAPI docs: `http://localhost:6420/docs` (when running)

**Frontend:**
- Types: `src/api/types.ts`
- Client: `src/api/client.js` (lines 23-95)
- Tests: `src/api/__tests__/client.test.js`
- Usage: `src/pages/PapersList.jsx` (line 28)

**History:**
- v1.0.0: Initial - raw array response (BUG)
- v1.1.0: Fixed - wrapped in object with counts (2026-04-25)
