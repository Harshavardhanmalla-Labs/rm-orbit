"""
API Contract Tests for /api/papers/ endpoint

These tests ensure that the backend response matches the contract expected by the frontend.
If these tests fail, the API contract has been broken and the frontend will fail.

Contract Schema (from PapersListResponse):
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
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestPapersListContract:
    """Verify /api/papers/ endpoint response contract."""

    def test_papers_list_response_has_required_fields(self):
        """Response must have papers, total, counts fields."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        # Check top-level fields
        assert "papers" in data, "Missing 'papers' field in response"
        assert "total" in data, "Missing 'total' field in response"
        assert "counts" in data, "Missing 'counts' field in response"

    def test_papers_list_response_papers_is_array(self):
        """papers field must be an array, not a raw response."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        # This test prevents the original bug (returning raw array)
        assert isinstance(data, dict), "Response must be object, not raw array"
        assert isinstance(data["papers"], list), "'papers' must be array"

    def test_papers_list_total_is_number(self):
        """total field must be a number."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data["total"], int), "'total' must be integer"
        assert data["total"] >= 0, "'total' must be non-negative"

    def test_papers_list_counts_structure(self):
        """counts field must have all required subfields."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()
        counts = data["counts"]

        # Check all required fields exist
        required_fields = ["total", "complete", "failed", "draft", "running", "cancelled"]
        for field in required_fields:
            assert field in counts, f"Missing 'counts.{field}' field"
            assert isinstance(counts[field], int), f"counts.{field} must be integer"
            assert counts[field] >= 0, f"counts.{field} must be non-negative"

    def test_papers_list_counts_total_matches(self):
        """top-level 'total' must equal papers array length."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        # These should be equal
        assert data["total"] == len(data["papers"]), \
            f"total ({data['total']}) must equal papers length ({len(data['papers'])})"
        assert data["counts"]["total"] == data["total"], \
            f"counts.total ({data['counts']['total']}) must equal response.total ({data['total']})"

    def test_papers_list_counts_sum_equals_total(self):
        """Sum of status counts must equal total."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()
        counts = data["counts"]

        # Sum of all statuses should equal total
        status_sum = counts["complete"] + counts["failed"] + counts["draft"] + counts["running"] + counts["cancelled"]
        assert status_sum == counts["total"], \
            f"Sum of status counts ({status_sum}) must equal total ({counts['total']})"

    def test_papers_list_paper_fields(self):
        """Each paper must have required fields."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        if len(data["papers"]) == 0:
            # Skip if no papers
            pytest.skip("No papers to validate")

        paper = data["papers"][0]

        # Check required fields
        required_fields = ["id", "status", "created_at"]
        for field in required_fields:
            assert field in paper, f"Paper missing required field: {field}"

        # Check field types
        assert isinstance(paper["id"], str), "Paper.id must be string"
        assert isinstance(paper["status"], str), "Paper.status must be string"
        assert isinstance(paper["created_at"], str), "Paper.created_at must be string"

        # Check optional fields are correct type if present
        if paper.get("title") is not None:
            assert isinstance(paper["title"], str), "Paper.title must be string or null"
        if paper.get("stage_progress") is not None:
            assert isinstance(paper["stage_progress"], (int, float)), "Paper.stage_progress must be number or null"

    def test_papers_list_status_values(self):
        """Paper statuses must be valid values."""
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        valid_statuses = {"intake", "processing", "running", "complete", "failed", "cancelled"}

        for paper in data["papers"]:
            assert paper["status"] in valid_statuses, \
                f"Paper status '{paper['status']}' not in valid values: {valid_statuses}"

    def test_papers_list_response_format_not_raw_array(self):
        """
        REGRESSION TEST: Prevent original bug where endpoint returned raw array.

        This test would fail if someone accidentally changed the endpoint back to:
            return [dict(r) for r in rows]

        Instead of:
            return PapersListResponse(papers=papers, total=total, counts=counts)
        """
        response = client.get("/api/papers/")
        assert response.status_code == 200

        data = response.json()

        # This MUST be an object with 'papers' key, not a raw array
        assert isinstance(data, dict), \
            "BUG REINTRODUCED: Response is raw array instead of {papers: [...], total: ..., counts: {...}}"
        assert not isinstance(data, list), \
            "BUG REINTRODUCED: Response is raw array instead of {papers: [...], total: ..., counts: {...}}"

    def test_openapi_schema_matches_implementation(self):
        """
        Verify that FastAPI OpenAPI schema matches actual response.
        This helps catch response_model mismatches.
        """
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()

        # Check that /api/papers/ endpoint is documented
        assert "/api/papers/" in schema["paths"], "Missing /api/papers/ in OpenAPI schema"

        # Check response schema exists
        papers_endpoint = schema["paths"]["/api/papers/"]["get"]
        assert "responses" in papers_endpoint, "Missing responses in OpenAPI schema"
        assert "200" in papers_endpoint["responses"], "Missing 200 response in OpenAPI schema"

        # Verify schema references PapersListResponse
        response_schema = papers_endpoint["responses"]["200"].get("content", {}).get("application/json", {}).get("schema", {})
        assert response_schema, "Missing response schema in OpenAPI documentation"

        # Should reference the model or be inline
        if "$ref" in response_schema:
            assert "PapersListResponse" in response_schema["$ref"], \
                "OpenAPI schema should reference PapersListResponse model"
