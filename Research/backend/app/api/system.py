import shutil
import aiosqlite
from fastapi import APIRouter

from app.database import DB_PATH
from app.services import grobid_client, languagetool_client, nougat_client, ollama_client
from app.settings import get_llm_settings

router = APIRouter(prefix="/api/system", tags=["system"])


def _component(name: str, ok: bool, required: bool, message: str) -> dict:
    return {
        "name": name,
        "status": "ready" if ok else "missing",
        "required": required,
        "message": message,
    }


async def _database_ready() -> bool:
    try:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute("SELECT 1")
        return True
    except Exception:
        return False


@router.get("/brain")
async def brain_readiness():
    database_ok = await _database_ready()
    llm_ok = await ollama_client.is_alive()
    grobid_ok = await grobid_client.is_alive()
    languagetool_ok = await languagetool_client.is_alive()
    nougat_ok = await nougat_client.is_alive()

    latex_ok = any(shutil.which(cmd) for cmd in ("tectonic", "pdflatex", "xelatex", "lualatex"))
    pandoc_ok = shutil.which("pandoc") is not None

    components = [
        _component("database", database_ok, True, "SQLite metadata store"),
        _component("llm", llm_ok, True, f"{ollama_client.provider_name()} model: {ollama_client.model_name()}"),
        _component("grobid", grobid_ok, False, "Structured PDF parsing and citation extraction"),
        _component("languagetool", languagetool_ok, False, "Grammar and academic-register checks"),
        _component("nougat", nougat_ok, False, "Math-heavy PDF parsing"),
        _component("latex", latex_ok, False, "Native PDF compilation"),
        _component("pandoc", pandoc_ok, False, "DOCX/PDF export fallback"),
    ]

    required_ready = all(c["status"] == "ready" for c in components if c["required"])
    optional_missing = [c["name"] for c in components if not c["required"] and c["status"] != "ready"]
    status = "ready" if required_ready and not optional_missing else "degraded" if required_ready else "not_ready"

    return {
        "status": status,
        "can_generate": required_ready,
        "can_ingest_basic_files": database_ok,
        "can_ingest_rich_pdfs": grobid_ok,
        "can_parse_math_pdfs": nougat_ok,
        "can_export_docx": pandoc_ok,
        "can_export_pdf": latex_ok or pandoc_ok,
        "optional_missing": optional_missing,
        "components": components,
    }


def _completion_areas(brain: dict) -> list[dict]:
    can_generate = brain["can_generate"]
    can_ingest_rich_pdfs = brain["can_ingest_rich_pdfs"]
    can_parse_math_pdfs = brain["can_parse_math_pdfs"]
    can_export_docx = brain["can_export_docx"]
    can_export_pdf = brain["can_export_pdf"]

    areas = [
        {
            "key": "backend_brain",
            "label": "Backend Brain",
            "percent": 79 if can_generate else 45,
            "status": "degraded" if can_generate and brain["status"] != "ready" else brain["status"],
            "notes": "Provider-agnostic LLM layer, readiness checks, smoke test, and cooperative cancellation are in place.",
        },
        {
            "key": "paper_pipeline",
            "label": "Paper Pipeline",
            "percent": 82 if can_generate else 45,
            "status": "in_progress",
            "notes": "End-to-end pipeline exists with persistent run history, run logs, completed-run proof, cancellation checks, and status reconstruction tests. Stage 2/3/4 unit tests added (knowledge map normalisation, contribution defaults, outline word-count scaling).",
        },
        {
            "key": "document_intake",
            "label": "Document Intake",
            "percent": 78 if can_ingest_rich_pdfs else 70,
            "status": "degraded" if not can_ingest_rich_pdfs else "ready",
            "notes": "Block-sorted PyMuPDF fallback, header/footer stripping, equation detection, and ingestion reports are in place. GROBID/Nougat add structured citation extraction and math-heavy PDF support.",
        },
        {
            "key": "quality_system",
            "label": "Quality System",
            "percent": 71,
            "status": "in_progress",
            "notes": "Five quality passes (structural, consistency, register, citations, clarity), banned phrase replacement, and confidence report are tested. LanguageTool live. Needs benchmark evaluation dataset.",
        },
        {
            "key": "export_system",
            "label": "Export System",
            "percent": 78 if can_export_docx and can_export_pdf else 62,
            "status": "degraded" if not can_export_pdf else "ready",
            "notes": "DOCX/PDF fallback is available; native LaTeX compiler would improve PDF fidelity.",
        },
        {
            "key": "frontend_workflow",
            "label": "Frontend Workflow",
            "percent": 89,
            "status": "in_progress",
            "notes": "All screens complete: delete with 2-step confirm, WS→polling fallback, venue selector fix, DOCX markdown fallback, export regenerate endpoint. Minor: no retry/recovery UI after failed upload.",
        },
        {
            "key": "deployment_readiness",
            "label": "Deployment Readiness",
            "percent": 72,
            "status": "in_progress",
            "notes": "PM2 ecosystem, nginx config (research.nginx.conf), start.sh with docker-compose services, and host allowlist are in place. Pending: symlink nginx config and run pm2 start.",
        },
        {
            "key": "production_quality",
            "label": "Production Quality",
            "percent": 76,
            "status": "in_progress",
            "notes": "Lint/build/compile checks, request tracing, progress reporting, persistent run/log tracking, intake reporting, cooperative cancellation, control APIs, 41 backend tests, and /api/system/settings diagnostics endpoint are in.",
        },
    ]

    if can_parse_math_pdfs:
        for area in areas:
            if area["key"] == "document_intake":
                area["percent"] = max(area["percent"], 78)
                area["notes"] = "Basic, rich PDF, and math-heavy parsing services are available."

    overall = round(sum(area["percent"] for area in areas) / len(areas))
    return overall, areas


@router.get("/progress")
async def project_progress():
    brain = await brain_readiness()
    overall, areas = _completion_areas(brain)
    return {
        "overall_percent": overall,
        "status": "in_progress",
        "areas": areas,
        "blockers": [
            "GROBID image/service for rich PDF and citation extraction",
            "Nougat service for math-heavy PDFs",
            "Native LaTeX compiler for highest-fidelity PDF output",
            "Automated backend tests for pipeline and API contracts",
            "Regression coverage for frontend workflows",
            "Production process manager/reverse proxy validation for research.freedomlabs.in",
        ],
        "brain": brain,
    }


@router.get("/settings")
async def system_settings():
    s = get_llm_settings()
    return {
        "llm": {
            "provider": s.provider,
            "model": s.model,
            "base_url": s.base_url,
            "timeout_seconds": s.timeout_seconds,
            "max_retries": s.max_retries,
            "json_repair_attempts": s.json_repair_attempts,
            "api_key_set": bool(s.api_key and s.api_key != "ollama"),
        },
        "services": {
            "grobid_url": grobid_client.GROBID_URL,
            "languagetool_url": languagetool_client.LT_URL,
            "nougat_url": nougat_client.NOUGAT_URL,
        },
    }


@router.post("/llm/smoke")
async def llm_smoke():
    if not await ollama_client.is_alive():
        return {
            "ok": False,
            "provider": ollama_client.provider_name(),
            "model": ollama_client.model_name(),
            "message": "Configured LLM is not ready.",
        }

    result = await ollama_client.generate_json(
        "You are a strict JSON API health checker.",
        'Return exactly: {"ok": true, "service": "research-llm"}',
        temperature=0,
    )
    return {
        "ok": result.get("ok") is True,
        "provider": ollama_client.provider_name(),
        "model": ollama_client.model_name(),
        "result": result,
    }
