import json
from pathlib import Path
from app.services import grobid_client, nougat_client
from app.database import DB_PATH
import aiosqlite


def _word_count(text: str) -> int:
    return len(text.split()) if text else 0


async def _update_ingestion_metadata(upload_id: str, text: str, method: str, warnings: list[str], **extra):
    fields = {
        "parsed_text": text[:50000] if text else "",
        "extraction_method": method,
        "extracted_word_count": _word_count(text),
        "parse_warnings": json.dumps(warnings),
        **extra,
    }
    set_clause = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [upload_id]
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(f"UPDATE uploads SET {set_clause} WHERE id = ?", values)
        await db.commit()


async def run(paper_id: str) -> dict:
    """Parse all uploaded files for a paper. Returns unified content dict."""
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM uploads WHERE paper_id = ?", (paper_id,)) as cur:
            uploads = [dict(r) for r in await cur.fetchall()]

    if not uploads:
        return {"full_text": "", "structured": [], "tables": [], "figures": [], "existing_citations": []}

    all_texts = []
    all_figures = []
    all_citations = []
    structured = []

    for upload in uploads:
        stored_path = upload["stored_path"]
        file_type = upload["file_type"]
        has_equations = bool(upload.get("has_equations", 0))
        warnings = []
        method = ""
        result = {"filename": upload["original_filename"], "text": "", "figures": [], "citations": [], "method": "", "warnings": []}

        if file_type == "pdf":
            grobid_alive = await grobid_client.is_alive()
            if grobid_alive:
                parsed = await grobid_client.process_pdf(stored_path)
                if not parsed.get("error"):
                    method = "grobid"
                    body = parsed.get("body_text", "")
                    abstract = parsed.get("abstract", "")
                    result["text"] = f"{abstract}\n\n{body}".strip()
                    result["figures"] = parsed.get("figures", [])
                    result["citations"] = parsed.get("references", [])
                    all_figures.extend(parsed.get("figures", []))
                    all_citations.extend(parsed.get("references", []))

                    # update upload record with grobid result
                    async with aiosqlite.connect(str(DB_PATH)) as db:
                        await db.execute(
                            "UPDATE uploads SET grobid_xml = ?, parsed_text = ? WHERE id = ?",
                            (json.dumps(parsed), result["text"], upload["id"])
                        )
                        await db.commit()
                else:
                    warnings.append(f"GROBID parse failed: {parsed.get('error')}")
            else:
                warnings.append("GROBID unavailable; using fallback extraction.")

            # Nougat: activate if equations detected
            if has_equations:
                nougat_alive = await nougat_client.is_alive()
                if nougat_alive:
                    markdown = await nougat_client.process_pdf(stored_path)
                    if markdown:
                        method = "nougat"
                        result["text"] = markdown  # nougat output supersedes grobid body text for math papers
                        async with aiosqlite.connect(str(DB_PATH)) as db:
                            await db.execute(
                                "UPDATE uploads SET nougat_markdown = ? WHERE id = ?",
                                (markdown, upload["id"])
                            )
                            await db.commit()
                    else:
                        warnings.append("Nougat returned no markdown; keeping previous extraction.")
                else:
                    warnings.append("Nougat unavailable for math-heavy PDF.")

            # Always fall back to PyMuPDF if no text yet
            if not result["text"]:
                method = "pymupdf"
                result["text"] = await nougat_client.extract_text_fallback(stored_path)
                if not result["text"]:
                    warnings.append("PyMuPDF fallback extracted no text.")

        elif file_type in ("docx",):
            try:
                from docx import Document
                doc = Document(stored_path)
                method = "python-docx"
                result["text"] = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            except Exception as e:
                method = "python-docx"
                result["text"] = f"[DOCX parse error: {e}]"
                warnings.append(f"DOCX parse error: {e}")

        elif file_type in ("txt", "md", "markdown"):
            method = "plain-text"
            result["text"] = Path(stored_path).read_text(errors="replace")

        elif file_type in ("csv",):
            try:
                import csv
                method = "csv"
                rows = []
                with open(stored_path, newline="", encoding="utf-8", errors="replace") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        rows.append(", ".join(row))
                result["text"] = "\n".join(rows[:200])
            except Exception:
                method = "csv"
                result["text"] = ""
                warnings.append("CSV parser extracted no text.")

        elif file_type in ("json",):
            try:
                method = "json"
                data = json.loads(Path(stored_path).read_text())
                result["text"] = json.dumps(data, indent=2)[:5000]
            except Exception:
                method = "json"
                result["text"] = ""
                warnings.append("JSON parser extracted no text.")

        method = method or "unknown"
        result["method"] = method
        result["warnings"] = warnings
        await _update_ingestion_metadata(upload["id"], result["text"], method, warnings)

        all_texts.append(result["text"])
        structured.append(result)

    full_text = "\n\n---\n\n".join(t for t in all_texts if t)

    # Deduplicate citations by title
    seen_titles = set()
    deduped_citations = []
    for c in all_citations:
        t = (c.get("title", "") or "").lower().strip()
        if t and t not in seen_titles:
            seen_titles.add(t)
            deduped_citations.append(c)

    return {
        "full_text": full_text,
        "structured": structured,
        "figures": all_figures,
        "existing_citations": deduped_citations,
    }
