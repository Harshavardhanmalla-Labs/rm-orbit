import uuid
import json
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import PaperCreate
from app.database import DB_PATH, update_paper, get_paper
from app.services.nougat_client import detect_equations
import aiosqlite

router = APIRouter(prefix="/api/intake", tags=["intake"])

UPLOADS_BASE = Path(__file__).parent.parent.parent / "uploads"
ALLOWED_SOURCE_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/plain": "txt",
    "text/markdown": "md",
    "application/json": "json",
    "text/csv": "csv",
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
}
ALLOWED_TEMPLATE_TYPES = {
    "application/pdf": "pdf",
    "text/plain": "tex",
    "application/x-tex": "tex",
    "application/octet-stream": "cls",
}


@router.post("/create")
async def create_paper(body: PaperCreate):
    paper_id = str(uuid.uuid4())
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            """INSERT INTO papers (id, topic, niche, paper_type, target_venue, author_name, author_affiliation, word_count_target, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'intake')""",
            (paper_id, body.topic, body.niche, body.paper_type.value, body.target_venue.value,
             body.author_name, body.author_affiliation, body.word_count_target)
        )
        await db.commit()
    return {"paper_id": paper_id}


@router.post("/{paper_id}/upload")
async def upload_file(paper_id: str, file: UploadFile = File(...)):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")

    content_type = file.content_type or ""
    # Guess type from extension if content_type is generic
    ext = Path(file.filename or "").suffix.lower().lstrip(".")
    ext_map = {"pdf": "pdf", "docx": "docx", "txt": "txt", "md": "md", "json": "json", "csv": "csv", "png": "png", "jpg": "jpg", "jpeg": "jpg"}
    file_type = ALLOWED_SOURCE_TYPES.get(content_type) or ext_map.get(ext, "")
    if not file_type:
        raise HTTPException(400, f"Unsupported file type: {content_type or ext}")

    upload_dir = UPLOADS_BASE / paper_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    upload_id = str(uuid.uuid4())
    stored_filename = f"{upload_id}.{file_type}"
    stored_path = upload_dir / stored_filename

    content = await file.read()
    stored_path.write_bytes(content)

    has_equations = 0
    if file_type == "pdf":
        has_equations = 1 if detect_equations(str(stored_path)) else 0

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "INSERT INTO uploads (id, paper_id, original_filename, stored_path, file_type, file_size, has_equations) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (upload_id, paper_id, file.filename, str(stored_path), file_type, len(content), has_equations)
        )
        await db.commit()

    return {
        "upload_id": upload_id,
        "filename": file.filename,
        "file_type": file_type,
        "file_size": len(content),
        "has_equations": bool(has_equations),
    }


@router.post("/{paper_id}/upload-template")
async def upload_template(paper_id: str, file: UploadFile = File(...)):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")

    ext = Path(file.filename or "template").suffix.lower().lstrip(".")
    if ext not in ("tex", "cls", "pdf", "sty"):
        raise HTTPException(400, "Template must be .tex, .cls, .sty, or .pdf")

    template_dir = UPLOADS_BASE / paper_id / "template"
    template_dir.mkdir(parents=True, exist_ok=True)
    template_path = template_dir / f"template.{ext}"
    content = await file.read()
    template_path.write_bytes(content)

    await update_paper(paper_id, custom_template_path=str(template_path), target_venue="custom")
    return {"template_path": str(template_path), "ext": ext}


@router.get("/{paper_id}/uploads")
async def list_uploads(paper_id: str):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT id, original_filename, file_type, file_size, has_equations,
                      extraction_method, extracted_word_count, parse_warnings, created_at
               FROM uploads WHERE paper_id = ?""",
            (paper_id,)
        ) as cur:
            rows = await cur.fetchall()
            uploads = []
            for row in rows:
                item = dict(row)
                try:
                    item["parse_warnings"] = json.loads(item.get("parse_warnings") or "[]")
                except Exception:
                    item["parse_warnings"] = []
                uploads.append(item)
            return uploads


@router.get("/{paper_id}/ingestion-report")
async def ingestion_report(paper_id: str):
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")

    uploads = await list_uploads(paper_id)
    total_words = sum(int(upload.get("extracted_word_count") or 0) for upload in uploads)
    warnings = [
        warning
        for upload in uploads
        for warning in upload.get("parse_warnings", [])
    ]
    method_counts: dict[str, int] = {}
    for upload in uploads:
        method = upload.get("extraction_method") or "pending"
        method_counts[method] = method_counts.get(method, 0) + 1

    return {
        "paper_id": paper_id,
        "upload_count": len(uploads),
        "total_extracted_words": total_words,
        "methods": list(method_counts.keys()),       # array of distinct method names
        "method_counts": method_counts,              # dict for detailed breakdown
        "warnings": warnings,
        "uploads": uploads,
        "ready_for_pipeline": total_words >= 80 or any(
            upload.get("file_type") in ("txt", "md", "docx", "pdf") for upload in uploads
        ),
    }
