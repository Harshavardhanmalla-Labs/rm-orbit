import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
from app.database import (
    create_pipeline_run,
    get_latest_pipeline_run,
    get_paper,
    get_pipeline_run,
    get_pipeline_runs,
    get_run_logs,
    update_paper,
    get_logs,
    update_pipeline_run,
)
from app.pipeline.orchestrator import build_stage_snapshot, run_pipeline, progress_store
from app.services import ollama_client as llm_client

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


@router.post("/{paper_id}/start")
async def start_pipeline(paper_id: str, background_tasks: BackgroundTasks):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    if paper.get("status") == "processing":
        return {"message": "Pipeline already running", "paper_id": paper_id}
    if not await llm_client.is_alive():
        raise HTTPException(
            503,
            f"Configured LLM is not ready: {llm_client.provider_name()} / {llm_client.model_name()}",
        )

    run_id = await create_pipeline_run(paper_id)
    await update_paper(paper_id, status="processing", current_stage="stage_0_gate", stage_progress=0.0, error_message=None)
    background_tasks.add_task(run_pipeline, paper_id, run_id)
    return {"message": "Pipeline started", "paper_id": paper_id, "run_id": run_id}


@router.get("/{paper_id}/status")
async def get_status(paper_id: str):
    # Check in-memory store first (most recent)
    if paper_id in progress_store:
        status = progress_store[paper_id]
        if "run" not in status:
            status["run"] = await get_latest_pipeline_run(paper_id)
        return status
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return {
        "paper_id": paper_id,
        "status": paper.get("status", "intake"),
        "current_stage": paper.get("current_stage", "intake"),
        "stage_progress": paper.get("stage_progress", 0.0),
        "message": paper.get("error_message") or "",
        "error_message": paper.get("error_message"),
        "stages": build_stage_snapshot(paper.get("current_stage", "intake"), paper.get("status", "intake")),
        "run": await get_latest_pipeline_run(paper_id),
    }


@router.get("/{paper_id}/runs")
async def list_runs(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return await get_pipeline_runs(paper_id)


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    run = await get_pipeline_run(run_id)
    if not run:
        raise HTTPException(404, "Pipeline run not found")
    return run


@router.get("/runs/{run_id}/logs")
async def get_run_log_entries(run_id: str):
    run = await get_pipeline_run(run_id)
    if not run:
        raise HTTPException(404, "Pipeline run not found")
    logs = await get_run_logs(run_id)
    if logs:
        return logs
    return await get_logs(run["paper_id"])


@router.post("/{paper_id}/cancel")
async def cancel_pipeline(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    await update_paper(paper_id, status="cancelled")
    latest_run = await get_latest_pipeline_run(paper_id)
    if latest_run and latest_run.get("status") == "processing":
        await update_pipeline_run(latest_run["id"], status="cancelled", completed_at="now")
    progress_store.pop(paper_id, None)
    return {
        "message": "Cancelled",
        "paper_id": paper_id,
        "run_id": latest_run["id"] if latest_run else None,
    }


@router.websocket("/ws/{paper_id}")
async def ws_pipeline(websocket: WebSocket, paper_id: str):
    await websocket.accept()
    try:
        while True:
            status = progress_store.get(paper_id)
            if not status:
                paper = await get_paper(paper_id)
                if paper:
                    status = {
                        "paper_id": paper_id,
                        "status": paper.get("status", "intake"),
                        "current_stage": paper.get("current_stage", "intake"),
                        "stage_progress": paper.get("stage_progress", 0.0),
                        "message": "",
                        "stages": build_stage_snapshot(paper.get("current_stage", "intake"), paper.get("status", "intake")),
                        "run": await get_latest_pipeline_run(paper_id),
                    }
            if status:
                await websocket.send_json(status)
                if status.get("status") in ("complete", "failed", "cancelled"):
                    break
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
