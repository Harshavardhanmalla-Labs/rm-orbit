from app.services.export_service import export_latex, compile_pdf, export_docx
from app.database import update_paper


async def run(paper_id: str, sections: dict, citations: list[dict], paper: dict) -> dict:
    venue = paper.get("target_venue", "arxiv")
    custom_template_path = paper.get("custom_template_path")
    author_name = paper.get("author_name", "")
    author_affiliation = paper.get("author_affiliation", "")

    # Build sections dict including acknowledgements for template
    export_sections = dict(sections)

    tex_path = await export_latex(
        paper_id=paper_id,
        sections=export_sections,
        citations=citations,
        venue=venue,
        custom_template_path=custom_template_path,
        author_name=author_name,
        author_affiliation=author_affiliation,
    )

    pdf_path = await compile_pdf(
        tex_path,
        sections=export_sections,
        citations=citations,
        author_name=author_name,
        author_affiliation=author_affiliation,
    )
    docx_path = await export_docx(
        tex_path,
        sections=export_sections,
        citations=citations,
        author_name=author_name,
        author_affiliation=author_affiliation,
    )

    await update_paper(paper_id, latex_path=tex_path, pdf_path=pdf_path, docx_path=docx_path)

    return {
        "latex_path": tex_path,
        "pdf_path": pdf_path,
        "docx_path": docx_path,
        "latex_available": bool(tex_path),
        "pdf_available": bool(pdf_path),
        "docx_available": bool(docx_path),
    }
