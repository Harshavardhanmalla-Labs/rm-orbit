from fastapi.testclient import TestClient

from app.api import system
from app.main import app


client = TestClient(app)


async def _true():
    return True


async def _false():
    return False


def test_brain_readiness_reports_required_llm(monkeypatch):
    monkeypatch.setattr(system, "_database_ready", _true)
    monkeypatch.setattr(system.ollama_client, "is_alive", _true)
    monkeypatch.setattr(system.ollama_client, "provider_name", lambda: "openai")
    monkeypatch.setattr(system.ollama_client, "model_name", lambda: "research-model")
    monkeypatch.setattr(system.grobid_client, "is_alive", _false)
    monkeypatch.setattr(system.languagetool_client, "is_alive", _true)
    monkeypatch.setattr(system.nougat_client, "is_alive", _false)
    monkeypatch.setattr(system.shutil, "which", lambda cmd: "/usr/bin/pandoc" if cmd == "pandoc" else None)

    response = client.get("/api/system/brain")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["can_generate"] is True
    assert data["can_export_docx"] is True
    assert data["can_export_pdf"] is True
    assert "grobid" in data["optional_missing"]
    assert data["components"][1]["name"] == "llm"
    assert data["components"][1]["message"] == "openai model: research-model"


def test_project_progress_returns_percentages(monkeypatch):
    async def fake_brain():
        return {
            "status": "degraded",
            "can_generate": True,
            "can_ingest_basic_files": True,
            "can_ingest_rich_pdfs": False,
            "can_parse_math_pdfs": False,
            "can_export_docx": True,
            "can_export_pdf": True,
            "optional_missing": ["grobid", "nougat", "latex"],
            "components": [],
        }

    monkeypatch.setattr(system, "brain_readiness", fake_brain)

    response = client.get("/api/system/progress")

    assert response.status_code == 200
    data = response.json()
    assert data["overall_percent"] >= 73
    assert len(data["areas"]) >= 8
    assert {area["key"] for area in data["areas"]} >= {
        "backend_brain",
        "paper_pipeline",
        "document_intake",
        "production_quality",
    }
    assert data["brain"]["can_generate"] is True


def test_request_context_headers_are_added():
    response = client.get("/health", headers={"x-request-id": "test-request-id"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "test-request-id"
    assert float(response.headers["x-response-time-ms"]) >= 0
