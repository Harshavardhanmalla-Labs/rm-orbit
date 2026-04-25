from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database import get_paper, update_paper

router = APIRouter(prefix="/api/export", tags=["export"])


class ReformatRequest(BaseModel):
    venue: str


@router.get("/{paper_id}/latex")
async def download_latex(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    path = paper.get("latex_path")
    if not path or not Path(path).exists():
        raise HTTPException(404, "LaTeX file not yet generated. Run the pipeline first.")
    return FileResponse(path, media_type="application/x-tex", filename="paper.tex")


@router.get("/{paper_id}/pdf")
async def download_pdf(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    path = paper.get("pdf_path")
    if not path or not Path(path).exists():
        raise HTTPException(404, "PDF not yet generated. LaTeX compilation may have failed — download .tex instead.")
    return FileResponse(path, media_type="application/pdf", filename="paper.pdf")


@router.get("/{paper_id}/docx")
async def download_docx(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    path = paper.get("docx_path")
    if not path or not Path(path).exists():
        raise HTTPException(404, "DOCX not generated. Install pandoc and re-run export.")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="paper.docx"
    )


@router.post("/{paper_id}/reformat")
async def reformat_paper(paper_id: str, body: ReformatRequest):
    from app.pipeline.stage8_export import run as export_run
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    if paper.get("status") != "complete":
        raise HTTPException(400, "Paper must be complete before reformatting")

    allowed_venues = ("ieee", "acm", "arxiv", "nature", "springer", "custom")
    venue = body.venue.lower()
    if venue not in allowed_venues:
        raise HTTPException(400, f"Invalid venue. Choose from: {', '.join(allowed_venues)}")

    await update_paper(paper_id, target_venue=venue, status="processing", current_stage="stage_8_export", stage_progress=91.0)
    paper["target_venue"] = venue
    sections = paper.get("sections", {})
    citations = paper.get("citations", [])
    result = await export_run(paper_id, sections, citations, paper)
    await update_paper(paper_id, status="complete", stage_progress=100.0)
    return {"message": f"Reformatted for {venue}", "result": result}


@router.post("/{paper_id}/regenerate")
async def regenerate_exports(paper_id: str):
    """Re-generate PDF and DOCX for a completed paper without re-running the full pipeline."""
    from app.services.export_service import compile_pdf, export_docx
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    if paper.get("status") != "complete":
        raise HTTPException(400, "Paper must be complete before regenerating exports")

    tex_path = paper.get("latex_path")
    if not tex_path or not Path(tex_path).exists():
        raise HTTPException(404, "LaTeX file not found — run the pipeline first")

    sections = paper.get("sections", {})
    citations = paper.get("citations", [])
    author_name = paper.get("author_name", "")
    author_affiliation = paper.get("author_affiliation", "")

    pdf_path = await compile_pdf(
        tex_path,
        sections=sections,
        citations=citations,
        author_name=author_name,
        author_affiliation=author_affiliation,
    )
    docx_path = await export_docx(
        tex_path,
        sections=sections,
        citations=citations,
        author_name=author_name,
        author_affiliation=author_affiliation,
    )

    await update_paper(paper_id, pdf_path=pdf_path, docx_path=docx_path)

    return {
        "pdf_available": bool(pdf_path),
        "docx_available": bool(docx_path),
        "pdf_path": pdf_path,
        "docx_path": docx_path,
    }


@router.get("/{paper_id}/confidence-report")
async def get_confidence_report(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")
    return paper.get("confidence_report", {})
