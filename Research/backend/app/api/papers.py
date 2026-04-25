from fastapi import APIRouter, HTTPException
from app.database import DB_PATH, get_paper, get_logs
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import aiosqlite
import json

# ============================================================================
# Response Models (API Contract)
# ============================================================================

class PaperBase(BaseModel):
    """Base paper fields."""
    id: str = Field(..., description="Unique paper ID (UUID)")
    title: Optional[str] = Field(None, description="Paper title")
    topic: Optional[str] = Field(None, description="Research topic")
    niche: Optional[str] = Field(None, description="Academic niche")
    target_venue: Optional[str] = Field(None, description="Target publication venue")
    paper_type: Optional[str] = Field(None, description="Paper type (original_research, survey, etc.)")
    status: str = Field(..., description="Current status (intake, processing, complete, failed, etc.)")
    current_stage: Optional[str] = Field(None, description="Current pipeline stage")
    stage_progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


class PapersListCounts(BaseModel):
    """Count breakdown by status."""
    total: int = Field(..., ge=0, description="Total papers")
    complete: int = Field(..., ge=0, description="Completed papers")
    failed: int = Field(..., ge=0, description="Failed papers")
    draft: int = Field(..., ge=0, description="Draft papers (intake status)")
    running: int = Field(..., ge=0, description="Running papers (processing/running status)")
    cancelled: int = Field(..., ge=0, description="Cancelled papers")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 4,
                "complete": 1,
                "failed": 1,
                "draft": 2,
                "running": 0,
                "cancelled": 0
            }
        }
    )


class PapersListResponse(BaseModel):
    """Response for GET /api/papers/"""
    papers: List[PaperBase] = Field(..., description="List of papers")
    total: int = Field(..., ge=0, description="Total number of papers")
    counts: PapersListCounts = Field(..., description="Count breakdown by status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


router = APIRouter(prefix="/api/papers", tags=["papers"])


@router.get("/", response_model=PapersListResponse)
async def list_papers() -> PapersListResponse:
    """
    List all papers with counts by status.

    Returns:
        PapersListResponse: Papers list with metadata

    Example:
        {
            "papers": [{...}, {...}],
            "total": 4,
            "counts": {
                "total": 4,
                "complete": 1,
                "failed": 1,
                "draft": 2,
                "running": 0,
                "cancelled": 0
            }
        }
    """
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, title, topic, niche, target_venue, paper_type, status, current_stage, stage_progress, created_at FROM papers ORDER BY created_at DESC"
        ) as cur:
            rows = await cur.fetchall()
            papers = [PaperBase(**dict(r)) for r in rows]

    # Calculate counts
    total = len(papers)
    counts = PapersListCounts(
        total=total,
        complete=sum(1 for p in papers if p.status == "complete"),
        failed=sum(1 for p in papers if p.status == "failed"),
        draft=sum(1 for p in papers if p.status == "intake"),
        running=sum(1 for p in papers if p.status in ("processing", "running")),
        cancelled=sum(1 for p in papers if p.status == "cancelled"),
    )

    return PapersListResponse(papers=papers, total=total, counts=counts)


@router.get("/{paper_id}")
async def get_paper_detail(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return paper


@router.delete("/{paper_id}")
async def delete_paper(paper_id: str):
    import shutil
    from pathlib import Path

    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute("DELETE FROM pipeline_logs WHERE paper_id = ?", (paper_id,))
        await db.execute("DELETE FROM pipeline_runs WHERE paper_id = ?", (paper_id,))
        await db.execute("DELETE FROM uploads WHERE paper_id = ?", (paper_id,))
        await db.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
        await db.commit()

    # Remove files
    for folder in ["uploads", "exports"]:
        path = Path(__file__).parent.parent.parent / folder / paper_id
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

    return {"deleted": paper_id}


@router.get("/{paper_id}/sections")
async def get_sections(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return paper.get("sections", {})


@router.get("/{paper_id}/citations")
async def get_citations(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return paper.get("citations", [])


@router.get("/{paper_id}/confidence")
async def get_confidence(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return paper.get("confidence_report", {})


@router.get("/{paper_id}/logs")
async def get_paper_logs(paper_id: str):
    return await get_logs(paper_id)
