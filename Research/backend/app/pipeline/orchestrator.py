import asyncio
import traceback
from app.database import update_paper, get_paper, get_uploads, log_pipeline, update_pipeline_run, get_pipeline_run
from app.pipeline import (
    stage0_gate, stage1_ingest, stage2_knowledge, stage3_contribution,
    stage4_outline, stage5_drafting, stage6_quality, stage7_citations, stage8_export,
)

# In-memory progress store — WebSocket connections poll this
progress_store: dict[str, dict] = {}


class PipelineCancelled(Exception):
    """Raised when a persisted pipeline run has been cancelled by the user."""

# Ordered stage keys matching frontend PIPELINE_STAGES
STAGE_KEYS = [
    "quality_gate", "ingesting", "knowledge_map", "contribution",
    "outline", "drafting", "quality_passes", "citations", "exporting",
]

STAGE_LABEL_TO_KEY = {
    "Quality Gate": "quality_gate",
    "Ingesting Documents": "ingesting",
    "Building Knowledge Map": "knowledge_map",
    "Discovering Contribution": "contribution",
    "Generating Outline": "outline",
    "Drafting Sections": "drafting",
    "Quality Passes": "quality_passes",
    "Building Citations": "citations",
    "Exporting Paper": "exporting",
}

DB_STAGE_TO_KEY = {
    "stage_0_gate": "quality_gate",
    "stage_1_ingest": "ingesting",
    "stage_2_knowledge": "knowledge_map",
    "stage_3_contribution": "contribution",
    "stage_4_outline": "outline",
    "stage_5_drafting": "drafting",
    "stage_6_quality": "quality_passes",
    "stage_7_citations": "citations",
    "stage_8_export": "exporting",
}


def build_stage_snapshot(current_stage: str, status: str) -> dict:
    stages = {key: "pending" for key in STAGE_KEYS}
    if status == "complete":
        return {key: "complete" for key in STAGE_KEYS}

    current_key = DB_STAGE_TO_KEY.get(current_stage) or STAGE_LABEL_TO_KEY.get(current_stage)
    if not current_key:
        return stages

    current_idx = STAGE_KEYS.index(current_key)
    for i, key in enumerate(STAGE_KEYS):
        if i < current_idx:
            stages[key] = "complete"
        elif i == current_idx:
            if status == "failed":
                stages[key] = "failed"
            elif status == "cancelled":
                stages[key] = "cancelled"
            elif status == "processing":
                stages[key] = "running"
            else:
                stages[key] = "pending"
    return stages


def _set_progress(paper_id: str, status: str, stage_label: str, progress: float, message: str = "", run_id: str | None = None):
    existing = progress_store.get(paper_id, {})
    stages = existing.get("stages", {k: "pending" for k in STAGE_KEYS})
    stage_messages = existing.get("stage_messages", {})
    stage_completed_at = existing.get("stage_completed_at", {})

    current_key = STAGE_LABEL_TO_KEY.get(stage_label)

    if current_key and status == "processing":
        # Mark everything before current as complete, current as running, rest as pending
        current_idx = STAGE_KEYS.index(current_key) if current_key in STAGE_KEYS else -1
        for i, key in enumerate(STAGE_KEYS):
            if i < current_idx:
                stages[key] = "complete"
            elif i == current_idx:
                stages[key] = "running"
            else:
                stages[key] = "pending"
        stage_messages[current_key] = message
    elif status == "complete":
        for key in STAGE_KEYS:
            stages[key] = "complete"
    elif status == "failed" and current_key:
        stages[current_key] = "failed"
    elif status == "cancelled" and current_key:
        stages[current_key] = "cancelled"

    import datetime
    if current_key and stages.get(current_key) == "complete":
        stage_completed_at[current_key] = datetime.datetime.utcnow().isoformat()

    progress_store[paper_id] = {
        "paper_id": paper_id,
        "status": status,
        "current_stage": stage_label,
        "stage_progress": progress,
        "message": message,
        "stages": stages,
        "stage_messages": stage_messages,
        "stage_completed_at": stage_completed_at,
    }
    if run_id:
        progress_store[paper_id]["run"] = {
            "id": run_id,
            "paper_id": paper_id,
            "status": status,
            "current_stage": stage_label,
            "stage_progress": progress,
        }


async def _raise_if_cancelled(paper_id: str, run_id: str | None, stage: str):
    paper = await get_paper(paper_id)
    if paper and paper.get("status") == "cancelled":
        raise PipelineCancelled(stage)
    if run_id:
        run = await get_pipeline_run(run_id)
        if run and run.get("status") == "cancelled":
            raise PipelineCancelled(stage)


async def run_pipeline(paper_id: str, run_id: str | None = None):
    """Main pipeline coordinator. Runs all 8 stages in sequence."""
    try:
        paper = await get_paper(paper_id)
        if not paper:
            return

        await update_paper(paper_id, status="processing", current_stage="stage_0_gate", stage_progress=0.0)
        await update_pipeline_run(run_id, status="processing", current_stage="stage_0_gate", stage_progress=0.0)
        _set_progress(paper_id, "processing", "Quality Gate", 0.0, "Starting quality checks...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_0_gate")

        # --- STAGE 0: Quality Gate ---
        await log_pipeline(paper_id, "stage_0_gate", "started", "Running quality gate checks", run_id=run_id)
        uploads = await get_uploads(paper_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_0_gate")

        # Quick text extraction for gate check (no GROBID/Nougat yet)
        gate_texts = []
        for u in uploads:
            raw = u.get("parsed_text", "") or ""
            if not raw:
                # Read file directly for gate check
                from pathlib import Path
                fpath = u.get("stored_path", "")
                ftype = u.get("file_type", "")
                if fpath and Path(fpath).exists():
                    if ftype in ("txt", "md", "markdown", "json", "csv"):
                        raw = Path(fpath).read_text(errors="replace")[:8000]
                    elif ftype == "pdf":
                        from app.services.nougat_client import extract_text_fallback
                        raw = await extract_text_fallback(fpath)
                    elif ftype == "docx":
                        try:
                            from docx import Document
                            doc = Document(fpath)
                            raw = " ".join(p.text for p in doc.paragraphs if p.text.strip())
                        except Exception:
                            pass
            gate_texts.append(raw)
        all_text = " ".join(t for t in gate_texts if t)

        gate_result = await stage0_gate.run(paper, all_text)
        await _raise_if_cancelled(paper_id, run_id, "stage_0_gate")
        if not gate_result["passed"]:
            error_msg = "; ".join(gate_result["errors"])
            await update_paper(paper_id, status="failed", error_message=error_msg)
            await update_pipeline_run(run_id, status="failed", current_stage="stage_0_gate", stage_progress=0.0, error_message=error_msg, completed_at="now")
            _set_progress(paper_id, "failed", "Quality Gate", 0.0, error_msg, run_id)
            await log_pipeline(paper_id, "stage_0_gate", "failed", error_msg, run_id=run_id)
            return

        warnings = gate_result.get("warnings", [])
        await update_paper(paper_id, warnings=warnings, current_stage="stage_1_ingest", stage_progress=11.0)
        await update_pipeline_run(run_id, current_stage="stage_1_ingest", stage_progress=11.0)
        await log_pipeline(paper_id, "stage_0_gate", "completed", f"Gate passed. {len(warnings)} warnings.", run_id=run_id)
        _set_progress(paper_id, "processing", "Ingesting Documents", 11.0, f"Parsing {len(uploads)} uploaded file(s)...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_1_ingest")

        # --- STAGE 1: Ingest ---
        await log_pipeline(paper_id, "stage_1_ingest", "started", "Ingesting and parsing documents", run_id=run_id)
        ingested = await stage1_ingest.run(paper_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_1_ingest")
        full_text = ingested.get("full_text", "")
        existing_citations = ingested.get("existing_citations", [])

        await update_paper(paper_id, current_stage="stage_2_knowledge", stage_progress=22.0)
        await update_pipeline_run(run_id, current_stage="stage_2_knowledge", stage_progress=22.0)
        await log_pipeline(paper_id, "stage_1_ingest", "completed", f"Ingested {len(full_text.split())} words from {len(uploads)} files", run_id=run_id)
        _set_progress(paper_id, "processing", "Building Knowledge Map", 22.0, "Extracting claims, methods, and results...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_2_knowledge")

        # --- STAGE 2: Knowledge Map ---
        await log_pipeline(paper_id, "stage_2_knowledge", "started", "Building knowledge map", run_id=run_id)
        knowledge_map = await stage2_knowledge.run(full_text, existing_citations)
        await _raise_if_cancelled(paper_id, run_id, "stage_2_knowledge")
        await update_paper(paper_id, knowledge_map=knowledge_map, current_stage="stage_3_contribution", stage_progress=33.0)
        await update_pipeline_run(run_id, current_stage="stage_3_contribution", stage_progress=33.0)
        await log_pipeline(paper_id, "stage_2_knowledge", "completed", f"Knowledge map built: {len(knowledge_map.get('claims', []))} claims, {len(knowledge_map.get('results', []))} results", run_id=run_id)
        _set_progress(paper_id, "processing", "Discovering Contribution", 33.0, "Identifying novel contribution...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_3_contribution")

        # --- STAGE 3: Contribution Discovery ---
        await log_pipeline(paper_id, "stage_3_contribution", "started", "Discovering contribution anchor", run_id=run_id)
        contribution_anchor = await stage3_contribution.run(knowledge_map, paper)
        await _raise_if_cancelled(paper_id, run_id, "stage_3_contribution")
        await update_paper(paper_id, contribution_anchor=contribution_anchor, current_stage="stage_4_outline", stage_progress=42.0)
        await update_pipeline_run(run_id, current_stage="stage_4_outline", stage_progress=42.0)
        await log_pipeline(paper_id, "stage_3_contribution", "completed", f"Contribution: {contribution_anchor.get('novelty_confidence', 'medium')} confidence", run_id=run_id)
        _set_progress(paper_id, "processing", "Generating Outline", 42.0, "Planning paper structure...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_4_outline")

        # --- STAGE 4: Outline ---
        await log_pipeline(paper_id, "stage_4_outline", "started", "Generating paper outline", run_id=run_id)
        outline = await stage4_outline.run(knowledge_map, contribution_anchor, paper)
        await _raise_if_cancelled(paper_id, run_id, "stage_4_outline")
        await update_paper(paper_id, outline=outline, current_stage="stage_5_drafting", stage_progress=50.0)
        await update_pipeline_run(run_id, current_stage="stage_5_drafting", stage_progress=50.0)
        await log_pipeline(paper_id, "stage_4_outline", "completed", f"Outline ready for {paper.get('target_venue', 'arxiv')} venue", run_id=run_id)
        _set_progress(paper_id, "processing", "Drafting Sections", 50.0, "Writing sections — this takes a few minutes...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_5_drafting")

        # --- STAGE 5: Section Drafting ---
        await log_pipeline(paper_id, "stage_5_drafting", "started", "Writing all paper sections", run_id=run_id)
        sections = await stage5_drafting.run(
            paper_id=paper_id,
            knowledge_map=knowledge_map,
            contribution_anchor=contribution_anchor,
            outline=outline,
            paper=paper,
        )
        await _raise_if_cancelled(paper_id, run_id, "stage_5_drafting")
        await update_paper(paper_id, sections=sections, current_stage="stage_6_quality", stage_progress=72.0)
        await update_pipeline_run(run_id, current_stage="stage_6_quality", stage_progress=72.0)
        section_count = sum(1 for v in sections.values() if v and str(v).strip())
        await log_pipeline(paper_id, "stage_5_drafting", "completed", f"{section_count} sections drafted", run_id=run_id)
        _set_progress(paper_id, "processing", "Quality Passes", 72.0, "Running 5 quality validation passes...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_6_quality")

        # --- STAGE 6: Quality Passes ---
        await log_pipeline(paper_id, "stage_6_quality", "started", "Running quality validation passes", run_id=run_id)
        quality_result = await stage6_quality.run(sections, knowledge_map, contribution_anchor, [])
        await _raise_if_cancelled(paper_id, run_id, "stage_6_quality")
        sections = quality_result["final_sections"]
        await update_paper(paper_id, sections=sections, current_stage="stage_7_citations", stage_progress=83.0)
        await update_pipeline_run(run_id, current_stage="stage_7_citations", stage_progress=83.0)
        await log_pipeline(paper_id, "stage_6_quality", "completed", f"{quality_result['passes_run']} passes, {quality_result['total_issues']} issues found", run_id=run_id)
        _set_progress(paper_id, "processing", "Building Citations", 83.0, "Verifying references via CrossRef...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_7_citations")

        # --- STAGE 7: Citations ---
        await log_pipeline(paper_id, "stage_7_citations", "started", "Building and verifying citation list", run_id=run_id)
        citations = await stage7_citations.run(knowledge_map, sections, paper.get("target_venue", "arxiv"))
        await _raise_if_cancelled(paper_id, run_id, "stage_7_citations")
        confidence_report = stage7_citations.build_confidence_report(sections, knowledge_map, citations, quality_result)
        await update_paper(
            paper_id,
            citations=citations,
            confidence_report=confidence_report,
            current_stage="stage_8_export",
            stage_progress=91.0,
        )
        await update_pipeline_run(run_id, current_stage="stage_8_export", stage_progress=91.0)
        verified = sum(1 for c in citations if c.get("verified"))
        await log_pipeline(paper_id, "stage_7_citations", "completed", f"{len(citations)} citations, {verified} verified", run_id=run_id)
        _set_progress(paper_id, "processing", "Exporting Paper", 91.0, "Compiling LaTeX and generating PDF...", run_id)
        await _raise_if_cancelled(paper_id, run_id, "stage_8_export")

        # --- STAGE 8: Export ---
        await log_pipeline(paper_id, "stage_8_export", "started", "Exporting to LaTeX / PDF / DOCX", run_id=run_id)
        export_result = await stage8_export.run(paper_id, sections, citations, paper)
        await _raise_if_cancelled(paper_id, run_id, "stage_8_export")
        await update_paper(paper_id, status="complete", current_stage="complete", stage_progress=100.0)
        await update_pipeline_run(run_id, status="complete", current_stage="complete", stage_progress=100.0, completed_at="now")
        await log_pipeline(paper_id, "stage_8_export", "completed",
                           f"Export complete. PDF: {bool(export_result.get('pdf_path'))}, DOCX: {bool(export_result.get('docx_path'))}",
                           run_id=run_id)
        _set_progress(paper_id, "complete", "Complete", 100.0, "Paper is ready.", run_id)

    except PipelineCancelled as e:
        stage = str(e) or "cancelled"
        await update_paper(paper_id, status="cancelled", current_stage=stage, error_message=None)
        await update_pipeline_run(run_id, status="cancelled", current_stage=stage, completed_at="now")
        _set_progress(paper_id, "cancelled", stage, 0.0, "Pipeline cancelled by user.", run_id)
        try:
            await log_pipeline(paper_id, stage, "cancelled", "Pipeline cancelled by user.", run_id=run_id)
        except Exception:
            pass

    except Exception as e:
        tb = traceback.format_exc()
        error_msg = f"{type(e).__name__}: {str(e)}"
        await update_paper(paper_id, status="failed", error_message=error_msg)
        await update_pipeline_run(run_id, status="failed", error_message=error_msg, completed_at="now")
        _set_progress(paper_id, "failed", "Error", 0.0, error_msg, run_id)
        try:
            await log_pipeline(paper_id, "error", "failed", error_msg, {"traceback": tb[:2000]}, run_id=run_id)
        except Exception:
            pass
