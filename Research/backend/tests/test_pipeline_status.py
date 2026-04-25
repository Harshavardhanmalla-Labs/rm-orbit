from fastapi.testclient import TestClient
import pytest

from app.api import pipeline_router
from app.main import app
from app.pipeline import orchestrator
from app.pipeline.orchestrator import PipelineCancelled, build_stage_snapshot


client = TestClient(app)


def test_build_stage_snapshot_for_completed_pipeline():
    stages = build_stage_snapshot("complete", "complete")

    assert stages
    assert set(stages.values()) == {"complete"}


def test_build_stage_snapshot_for_failed_stage():
    stages = build_stage_snapshot("stage_4_outline", "failed")

    assert stages["quality_gate"] == "complete"
    assert stages["ingesting"] == "complete"
    assert stages["knowledge_map"] == "complete"
    assert stages["contribution"] == "complete"
    assert stages["outline"] == "failed"
    assert stages["drafting"] == "pending"


def test_build_stage_snapshot_for_cancelled_stage():
    stages = build_stage_snapshot("stage_5_drafting", "cancelled")

    assert stages["outline"] == "complete"
    assert stages["drafting"] == "cancelled"
    assert stages["quality_passes"] == "pending"


@pytest.mark.asyncio
async def test_pipeline_cancel_check_raises_for_cancelled_run(monkeypatch):
    async def fake_get_paper(paper_id):
        return {"id": paper_id, "status": "processing"}

    async def fake_get_pipeline_run(run_id):
        return {"id": run_id, "status": "cancelled"}

    monkeypatch.setattr(orchestrator, "get_paper", fake_get_paper)
    monkeypatch.setattr(orchestrator, "get_pipeline_run", fake_get_pipeline_run)

    try:
        await orchestrator._raise_if_cancelled("paper-123", "run-123", "stage_5_drafting")
    except PipelineCancelled as exc:
        assert str(exc) == "stage_5_drafting"
    else:
        raise AssertionError("Expected PipelineCancelled")


def test_pipeline_status_reconstructs_stages_from_persisted_paper(monkeypatch):
    async def fake_get_paper(paper_id):
        return {
            "id": paper_id,
            "status": "processing",
            "current_stage": "stage_6_quality",
            "stage_progress": 72.0,
            "error_message": None,
        }

    async def fake_latest_run(paper_id):
        return {"id": "run-123", "paper_id": paper_id, "status": "processing"}

    monkeypatch.setattr(pipeline_router, "get_paper", fake_get_paper)
    monkeypatch.setattr(pipeline_router, "get_latest_pipeline_run", fake_latest_run)
    pipeline_router.progress_store.clear()

    response = client.get("/api/pipeline/paper-123/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"
    assert data["stages"]["drafting"] == "complete"
    assert data["stages"]["quality_passes"] == "running"
    assert data["stages"]["citations"] == "pending"
    assert data["run"]["id"] == "run-123"


def test_pipeline_start_fails_cleanly_when_llm_missing(monkeypatch):
    async def fake_get_paper(paper_id):
        return {"id": paper_id, "status": "intake"}

    async def llm_missing():
        return False

    monkeypatch.setattr(pipeline_router, "get_paper", fake_get_paper)
    monkeypatch.setattr(pipeline_router.llm_client, "is_alive", llm_missing)
    monkeypatch.setattr(pipeline_router.llm_client, "provider_name", lambda: "openai")
    monkeypatch.setattr(pipeline_router.llm_client, "model_name", lambda: "research-model")

    response = client.post("/api/pipeline/paper-123/start")

    assert response.status_code == 503
    assert "Configured LLM is not ready" in response.json()["detail"]


def test_pipeline_start_returns_run_id(monkeypatch):
    async def fake_get_paper(paper_id):
        return {"id": paper_id, "status": "intake"}

    async def llm_ready():
        return True

    async def fake_create_pipeline_run(paper_id):
        return "run-456"

    async def fake_update_paper(paper_id, **fields):
        return None

    async def fake_run_pipeline(paper_id, run_id=None):
        return None

    monkeypatch.setattr(pipeline_router, "get_paper", fake_get_paper)
    monkeypatch.setattr(pipeline_router.llm_client, "is_alive", llm_ready)
    monkeypatch.setattr(pipeline_router, "create_pipeline_run", fake_create_pipeline_run)
    monkeypatch.setattr(pipeline_router, "update_paper", fake_update_paper)
    monkeypatch.setattr(pipeline_router, "run_pipeline", fake_run_pipeline)

    response = client.post("/api/pipeline/paper-123/start")

    assert response.status_code == 200
    assert response.json()["run_id"] == "run-456"


def test_pipeline_run_history_endpoint(monkeypatch):
    async def fake_get_paper(paper_id):
        return {"id": paper_id, "status": "complete"}

    async def fake_get_pipeline_runs(paper_id):
        return [
            {"id": "run-new", "paper_id": paper_id, "status": "complete"},
            {"id": "run-old", "paper_id": paper_id, "status": "failed"},
        ]

    monkeypatch.setattr(pipeline_router, "get_paper", fake_get_paper)
    monkeypatch.setattr(pipeline_router, "get_pipeline_runs", fake_get_pipeline_runs)

    response = client.get("/api/pipeline/paper-123/runs")

    assert response.status_code == 200
    data = response.json()
    assert [run["id"] for run in data] == ["run-new", "run-old"]


def test_pipeline_cancel_endpoint_marks_paper_and_run(monkeypatch):
    calls = {"paper": None, "run": None}

    async def fake_get_paper(paper_id):
        return {"id": paper_id, "status": "processing"}

    async def fake_get_latest_pipeline_run(paper_id):
        return {"id": "run-789", "paper_id": paper_id, "status": "processing"}

    async def fake_update_paper(paper_id, **fields):
        calls["paper"] = {"paper_id": paper_id, **fields}

    async def fake_update_pipeline_run(run_id, **fields):
        calls["run"] = {"run_id": run_id, **fields}

    monkeypatch.setattr(pipeline_router, "get_paper", fake_get_paper)
    monkeypatch.setattr(pipeline_router, "get_latest_pipeline_run", fake_get_latest_pipeline_run)
    monkeypatch.setattr(pipeline_router, "update_paper", fake_update_paper)
    monkeypatch.setattr(pipeline_router, "update_pipeline_run", fake_update_pipeline_run)
    pipeline_router.progress_store["paper-123"] = {"status": "processing"}

    response = client.post("/api/pipeline/paper-123/cancel")

    assert response.status_code == 200
    assert response.json()["run_id"] == "run-789"
    assert calls["paper"]["status"] == "cancelled"
    assert calls["run"]["status"] == "cancelled"
    assert "paper-123" not in pipeline_router.progress_store


def test_pipeline_run_logs_fallback_to_paper_logs(monkeypatch):
    async def fake_get_pipeline_run(run_id):
        return {"id": run_id, "paper_id": "paper-123", "status": "complete"}

    async def fake_get_run_logs(run_id):
        return []

    async def fake_get_logs(paper_id):
        return [{"id": 1, "paper_id": paper_id, "stage": "stage_0_gate", "status": "completed", "message": "ok"}]

    monkeypatch.setattr(pipeline_router, "get_pipeline_run", fake_get_pipeline_run)
    monkeypatch.setattr(pipeline_router, "get_run_logs", fake_get_run_logs)
    monkeypatch.setattr(pipeline_router, "get_logs", fake_get_logs)

    response = client.get("/api/pipeline/runs/run-123/logs")

    assert response.status_code == 200
    assert response.json()[0]["paper_id"] == "paper-123"
