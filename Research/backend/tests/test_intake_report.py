from fastapi.testclient import TestClient

from app.api import intake
from app.main import app


client = TestClient(app)


def test_ingestion_report_summarizes_upload_metadata(monkeypatch):
    async def fake_get_paper(paper_id):
        return {"id": paper_id, "topic": "Test"}

    async def fake_list_uploads(paper_id):
        return [
            {
                "id": "upload-1",
                "file_type": "pdf",
                "extraction_method": "pymupdf",
                "extracted_word_count": 150,
                "parse_warnings": ["GROBID unavailable; using fallback extraction."],
            },
            {
                "id": "upload-2",
                "file_type": "txt",
                "extraction_method": "plain-text",
                "extracted_word_count": 120,
                "parse_warnings": [],
            },
        ]

    monkeypatch.setattr(intake, "get_paper", fake_get_paper)
    monkeypatch.setattr(intake, "list_uploads", fake_list_uploads)

    response = client.get("/api/intake/paper-123/ingestion-report")

    assert response.status_code == 200
    data = response.json()
    assert data["upload_count"] == 2
    assert data["total_extracted_words"] == 270
    assert set(data["methods"]) == {"pymupdf", "plain-text"}
    assert data["method_counts"] == {"pymupdf": 1, "plain-text": 1}
    assert data["ready_for_pipeline"] is True
    assert data["warnings"] == ["GROBID unavailable; using fallback extraction."]
