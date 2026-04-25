# API Contract Hardening - Summary Report

**Date:** 2026-04-25  
**Status:** ✅ Complete

---

## 🎯 Objective

Prevent the API contract mismatch bug from happening again by establishing bidirectional type safety and validation between FastAPI backend and React frontend.

**Bug Fixed:** Backend returned `[papers]`, frontend expected `{papers: [...]}` → "all counts = 0"

---

## 📋 What Was Implemented

### 1. Backend Response Schemas (Pydantic Models)

**File:** `backend/app/api/papers.py`

**Changes:**
- ✅ Added `PaperBase` model for individual paper
- ✅ Added `PapersListCounts` model for status counts
- ✅ Added `PapersListResponse` model for complete response
- ✅ Updated `list_papers()` endpoint to use response model
- ✅ Added counts calculation (complete, failed, draft, running, cancelled)

**Response Format (Now Required):**
```json
{
  "papers": [...],
  "total": number,
  "counts": {
    "total": number,
    "complete": number,
    "failed": number,
    "draft": number,
    "running": number,
    "cancelled": number
  }
}
```

**Lines Changed:** ~90 lines added (models + updated endpoint)

---

### 2. Frontend TypeScript Types

**File:** `frontend/src/api/types.ts` (NEW)

**Added:**
- ✅ `Paper` interface
- ✅ `PapersListCounts` interface
- ✅ `PapersListResponse` interface
- ✅ `BrainStatus` and `BrainComponent` interfaces
- ✅ JSDoc comments explaining each type

**Purpose:** TypeScript ensures frontend code cannot use wrong response structure

**Lines Added:** 95

---

### 3. API Client Contract Validation

**File:** `frontend/src/api/client.js`

**Changes:**
- ✅ Added `validatePapersListResponse()` function
- ✅ Integrated validation into response interceptor
- ✅ Detailed error messages for debugging
- ✅ Catches the original bug (raw array response)

**Validation Checks:**
1. Response is object (not raw array)
2. `papers` field exists and is array
3. `total` field exists and is number
4. `counts` field exists and is object
5. All count subfields exist and are numbers
6. Clear errors guide developers to fix

**Lines Added:** 75

---

### 4. Backend Contract Tests

**File:** `backend/tests/test_papers_contract.py` (NEW)

**Test Coverage:**
- ✅ Response has all required fields
- ✅ `papers` is array (not raw response)
- ✅ `total` is number
- ✅ `counts` has all subfields
- ✅ Sum of counts equals total
- ✅ Paper fields are present and correct types
- ✅ Status values are valid
- ✅ **Regression test:** Raw array response rejected
- ✅ OpenAPI schema matches implementation

**Lines Added:** 238

**Run Tests:**
```bash
cd backend
pytest tests/test_papers_contract.py -v
```

---

### 5. Frontend Contract Tests

**File:** `frontend/src/api/__tests__/client.test.js` (NEW)

**Test Coverage:**
- ✅ Valid response accepted
- ✅ Raw array response rejected (catches original bug)
- ✅ Missing fields rejected
- ✅ Wrong types rejected
- ✅ Null/undefined rejected
- ✅ Error messages are helpful
- ✅ All count fields required

**Lines Added:** 262

**Run Tests:**
```bash
cd frontend
npm run test -- src/api/__tests__/client.test.js
```

---

### 6. API Contract Documentation

**File:** `API_CONTRACT.md` (NEW)

**Contains:**
- ✅ Full schema documentation
- ✅ Required vs optional fields
- ✅ How validation works (both sides)
- ✅ How to test the contract
- ✅ What happens if contract breaks
- ✅ Contract versioning strategy
- ✅ Checklist for adding new endpoints

**Lines Added:** 450+

---

### 7. Verification Test Script

**File:** `test_contract.sh` (NEW)

**Runs:**
1. Backend pytest suite
2. Checks if backend API is responding
3. Validates live API response structure
4. Frontend vitest suite (if npm available)
5. Provides clear pass/fail output

**Usage:**
```bash
cd Research
./test_contract.sh
```

---

## 🔍 Files Changed Summary

| File | Type | Changes | Purpose |
|------|------|---------|---------|
| `backend/app/api/papers.py` | Edit | +90 lines | Pydantic models, response wrapping |
| `frontend/src/api/types.ts` | NEW | +95 lines | TypeScript interfaces |
| `frontend/src/api/client.js` | Edit | +75 lines | Response validation |
| `backend/tests/test_papers_contract.py` | NEW | +238 lines | Backend tests |
| `frontend/src/api/__tests__/client.test.js` | NEW | +262 lines | Frontend tests |
| `API_CONTRACT.md` | NEW | +450 lines | Documentation |
| `test_contract.sh` | NEW | +170 lines | Verification script |

**Total Lines Added:** ~1,380 (documentation + tests + safety checks)

---

## ✅ How It Works

### Scenario 1: Correct Response (Success Path)

```
Backend: return PapersListResponse(papers=papers, total=total, counts=counts)
         ↓
FastAPI: Validates with Pydantic → generates OpenAPI schema
         ↓
Frontend: JSON response arrives
         ↓
API Client: validatePapersListResponse() checks structure
           - Is object? ✓
           - Has papers array? ✓
           - Has total number? ✓
           - Has counts object? ✓
         ↓
React: setState(papers) → UI renders correctly
```

### Scenario 2: Raw Array Response (Bug Caught)

```
Backend: return papers  # ❌ WRONG (the original bug)
         ↓
FastAPI: Validation error (response_model mismatch)
         OR response sent as-is
         ↓
Frontend: Validation rejects response
         Throws: "API contract violation: Expected {papers: Array, total: number, counts: {...}}, 
                  but got raw array. Backend needs to return {papers: [...]}. 
                  See app/api/papers.py list_papers() endpoint."
         ↓
Test: FAIL ❌ (catches immediately)
Browser Console: Clear error message with fix location
```

### Scenario 3: Missing Field (Contract Break)

```
Backend: return {"papers": [...], "total": total}  # Missing counts
         ↓
FastAPI: Validation error (Pydantic enforces required field)
         ↓
Frontend: Even if response sent, validation catches it
         Throws: "API contract violation: 'counts' must be object..."
         ↓
Test: FAIL ❌ (catches immediately)
```

---

## 🧪 Verification Steps

### Option 1: Quick Check (Backend Only)

```bash
cd Research/backend
pytest tests/test_papers_contract.py::TestPapersListContract::test_papers_list_response_not_raw_array -v
```

**Expected Output:**
```
test_papers_list_response_not_raw_array PASSED ✓
```

### Option 2: Full Backend Tests

```bash
cd Research/backend
pytest tests/test_papers_contract.py -v
```

**Expected Output:**
```
test_papers_list_response_has_required_fields PASSED
test_papers_list_response_papers_is_array PASSED
test_papers_list_total_is_number PASSED
test_papers_list_counts_structure PASSED
test_papers_list_counts_total_matches PASSED
test_papers_list_counts_sum_equals_total PASSED
test_papers_list_paper_fields PASSED
test_papers_list_status_values PASSED
test_papers_list_response_format_not_raw_array PASSED
test_openapi_schema_matches_implementation PASSED

10 passed ✓
```

### Option 3: Full Verification (Both Sides)

```bash
# Terminal 1: Start backend
cd Research/backend
python -m uvicorn app.main:app --port 6420

# Terminal 2: Start frontend
cd Research/frontend
npm run dev

# Terminal 3: Run tests
cd Research
./test_contract.sh
```

**Expected Output:**
```
✅ Backend contract tests PASSED
✅ Backend API is running on http://localhost:6420
✅ API response is valid JSON
✅ Response structure valid
   - Papers: 4
   - Total: 4
   - Complete: 1
   - Failed: 1
   - Draft: 2
   - Running: 0
✅ Frontend contract tests PASSED
✅ Contract Verification Complete
```

---

## 🛡️ Protection Guarantees

| Threat | Protection | How It Works |
|--------|-----------|-------------|
| Raw array response returned | Backend response_model enforcement + Frontend validation | Pydantic + client validation catches immediately |
| Missing required field | Pydantic validation + TypeScript | Code won't compile (TypeScript) + runtime error (Pydantic) |
| Wrong field type (e.g., total="5") | Pydantic validation + Frontend validation | Rejected with clear error message |
| Field renamed (e.g., "count" → "counts") | TypeScript error + Backend test failure | Build fails or test fails |
| New optional field added | Backward compatible (TypeScript optional) | No issues, safe to add |
| Response structure changes | Tests fail, requiring explicit updates | Forces contract version update |

---

## 🚀 What This Prevents

1. **Silent Data Loss** - Frontend showing empty list because API mismatch goes unnoticed
2. **Type Mismatches** - Frontend assuming string, backend sending number
3. **Breaking Changes** - API changes that break client without notification
4. **Future Bugs** - Same class of bug in new endpoints
5. **Integration Issues** - Frontend and backend diverging without knowing

---

## 📚 Documentation Reference

**For Developers:**
- Read: `API_CONTRACT.md` - Full contract specification
- Read: `backend/app/api/papers.py` - See Pydantic models (lines 8-90)
- Read: `frontend/src/api/types.ts` - See TypeScript interfaces
- Read: `frontend/src/api/client.js` - See validation logic (lines 23-95)

**For Testing:**
- Run: `backend/tests/test_papers_contract.py`
- Run: `frontend/src/api/__tests__/client.test.js`
- Run: `./test_contract.sh` (both sides)

**For Adding New Endpoints:**
1. Check `API_CONTRACT.md` "Checklist: Adding New Endpoints" section
2. Define Pydantic model first
3. Write tests before implementation
4. Update TypeScript types
5. Add client validation
6. Update contract document

---

## 🔄 How to Update Contract

If you intentionally change the API response:

1. **Update Pydantic Model** (`backend/app/api/papers.py`):
   ```python
   class PapersListResponse(BaseModel):
       # Add/remove/change fields
   ```

2. **Update TypeScript Type** (`frontend/src/api/types.ts`):
   ```typescript
   export interface PapersListResponse {
       // Add/remove/change fields
   }
   ```

3. **Update Validation** (`frontend/src/api/client.js`):
   ```javascript
   function validatePapersListResponse(data) {
       // Add/remove/change checks
   }
   ```

4. **Update Tests** (both backend + frontend)

5. **Update Contract Document** (`API_CONTRACT.md`):
   - Increment version number
   - Document what changed
   - Mark old version as deprecated

6. **Run Tests** to verify everything works

---

## ✨ Final Notes

This hardening ensures:
- ✅ Type safety between backend and frontend
- ✅ Clear error messages when contracts break
- ✅ Original bug class is now impossible
- ✅ Future developers guided by tests
- ✅ Breaking changes caught immediately
- ✅ Easy to add new endpoints safely

**The system will now catch API contract violations before they reach production.** 🎯

