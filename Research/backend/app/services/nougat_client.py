import httpx
import fitz  # PyMuPDF
from pathlib import Path

NOUGAT_URL = "http://localhost:8071"

MATH_INDICATORS = [
    "∑", "∫", "∂", "√", "σ", "μ", "∞", "≤", "≥", "≠", "∈", "∀", "∃",
    "\\frac", "\\sum", "\\int", "\\partial", "\\sqrt", "\\alpha", "\\beta",
    "\\gamma", "\\theta", "\\lambda", "\\sigma", "\\mu", "\\pi", "\\Delta",
    "\\nabla", "\\forall", "\\exists", "\\mathbb", "\\mathrm",
]


def detect_equations(pdf_path: str) -> bool:
    """Scan PDF text for math indicators using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = " ".join(page.get_text() for page in doc)
        doc.close()
        return any(ind in text for ind in MATH_INDICATORS)
    except Exception:
        return False


async def is_alive() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{NOUGAT_URL}/health")
            return r.status_code == 200
    except Exception:
        return False


async def process_pdf(pdf_path: str) -> str:
    """Send PDF to Nougat, get markdown with LaTeX equations."""
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            with open(pdf_path, "rb") as f:
                r = await client.post(
                    f"{NOUGAT_URL}/predict",
                    files={"file": (Path(pdf_path).name, f, "application/pdf")},
                )
            if r.status_code == 200:
                return r.text
            return ""
    except Exception:
        return ""


async def extract_text_fallback(pdf_path: str) -> str:
    """PyMuPDF text extraction as fallback when Nougat is offline.
    Uses block-sorted extraction for correct reading order and strips
    repetitive headers/footers."""
    try:
        doc = fitz.open(pdf_path)
        page_texts = []
        header_footer_lines: set[str] = set()

        # First pass: collect lines that repeat on 3+ pages (headers/footers)
        line_freq: dict[str, int] = {}
        for page in doc:
            for line in page.get_text("text").splitlines():
                stripped = line.strip()
                if stripped:
                    line_freq[stripped] = line_freq.get(stripped, 0) + 1
        n_pages = len(doc)
        if n_pages >= 3:
            header_footer_lines = {
                ln for ln, count in line_freq.items()
                if count >= max(3, n_pages // 3) and len(ln) < 120
            }

        # Second pass: extract with reading-order sort (top→bottom, left→right)
        for page in doc:
            blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, type)
            blocks.sort(key=lambda b: (round(b[1] / 20) * 20, b[0]))  # row-bucket + x
            lines = []
            for block in blocks:
                if block[6] != 0:  # skip image blocks
                    continue
                for line in block[4].splitlines():
                    stripped = line.strip()
                    if stripped and stripped not in header_footer_lines:
                        lines.append(stripped)
            if lines:
                page_texts.append("\n".join(lines))

        doc.close()
        return "\n\n".join(page_texts)
    except Exception:
        return ""
