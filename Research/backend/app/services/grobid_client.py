import httpx
import xml.etree.ElementTree as ET
from pathlib import Path

GROBID_URL = "http://localhost:8070"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def _text(el, path: str, ns=NS) -> str:
    node = el.find(path, ns)
    return (node.text or "").strip() if node is not None else ""


def _all_text(el, path: str, ns=NS) -> str:
    node = el.find(path, ns)
    if node is None:
        return ""
    return " ".join((node.itertext()))


async def is_alive() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{GROBID_URL}/api/isalive")
            return r.status_code == 200
    except Exception:
        return False


async def process_pdf(pdf_path: str) -> dict:
    """Send PDF to GROBID, parse TEI XML, return structured dict."""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            with open(pdf_path, "rb") as f:
                r = await client.post(
                    f"{GROBID_URL}/api/processFulltextDocument",
                    files={"input": (Path(pdf_path).name, f, "application/pdf")},
                    data={"consolidateHeader": "1", "consolidateCitations": "0", "includeRawCitations": "1"},
                )
            if r.status_code != 200:
                return {"error": f"GROBID returned {r.status_code}", "body_text": "", "title": "", "references": [], "figures": []}
            return _parse_tei(r.text)
    except Exception as e:
        return {"error": str(e), "body_text": "", "title": "", "references": [], "figures": []}


def _parse_tei(xml_text: str) -> dict:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return {"error": "XML parse error", "body_text": xml_text[:5000], "title": "", "references": [], "figures": []}

    # Title
    title = _text(root, ".//tei:titleStmt/tei:title", NS)

    # Abstract
    abstract_el = root.find(".//tei:abstract", NS)
    abstract = " ".join(abstract_el.itertext()).strip() if abstract_el is not None else ""

    # Body text
    body_el = root.find(".//tei:body", NS)
    body_text = " ".join(body_el.itertext()).strip() if body_el is not None else ""

    # References
    references = []
    for bib in root.findall(".//tei:listBibl/tei:biblStruct", NS):
        authors = []
        for author in bib.findall(".//tei:author/tei:persName", NS):
            forename = _text(author, "tei:forename", NS)
            surname = _text(author, "tei:surname", NS)
            if surname:
                authors.append(f"{surname}, {forename}".strip(", "))
        year_el = bib.find(".//tei:date[@type='published']", NS)
        year = year_el.get("when", "")[:4] if year_el is not None else ""
        title_el = bib.find(".//tei:title[@level='a']", NS) or bib.find(".//tei:title", NS)
        ref_title = (title_el.text or "").strip() if title_el is not None else ""
        journal_el = bib.find(".//tei:title[@level='j']", NS)
        journal = (journal_el.text or "").strip() if journal_el is not None else ""
        doi_el = bib.find(".//tei:idno[@type='DOI']", NS)
        doi = (doi_el.text or "").strip() if doi_el is not None else ""
        references.append({"authors": authors, "year": year, "title": ref_title, "journal": journal, "doi": doi})

    # Figures
    figures = []
    for fig in root.findall(".//tei:figure", NS):
        fig_id = fig.get("{http://www.w3.org/XML/1998/namespace}id", "")
        caption_el = fig.find(".//tei:figDesc", NS)
        caption = " ".join(caption_el.itertext()).strip() if caption_el is not None else ""
        figures.append({"id": fig_id, "caption": caption})

    return {
        "title": title,
        "abstract": abstract,
        "body_text": body_text,
        "references": references,
        "figures": figures,
    }
