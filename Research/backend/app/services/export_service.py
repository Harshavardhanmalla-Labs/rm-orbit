import subprocess
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
EXPORTS_BASE = Path(__file__).parent.parent.parent / "exports"


def _get_template(venue: str, custom_path: str | None) -> str:
    if custom_path and Path(custom_path).exists():
        return Path(custom_path).read_text()
    template_file = TEMPLATES_DIR / venue / "template.tex"
    if template_file.exists():
        return template_file.read_text()
    # fallback to arxiv
    return (TEMPLATES_DIR / "arxiv" / "template.tex").read_text()


def _build_bibliography(citations: list[dict]) -> str:
    entries = []
    for i, c in enumerate(citations, 1):
        bibtex = c.get("bibtex_entry", "")
        if bibtex:
            entries.append(bibtex)
        else:
            authors = " and ".join(c.get("authors", ["Unknown Author"]))
            year = c.get("year", "2024")
            title = c.get("title", "Untitled")
            key = c.get("bibtex_key", f"ref{i}")
            journal = c.get("journal", c.get("venue", ""))
            doi = c.get("doi", "")
            entry = f"\\bibitem{{{key}}}\n{authors}.\n\\textit{{{title}}}."
            if journal:
                entry += f"\n{journal},"
            if year:
                entry += f" {year}."
            if doi:
                entry += f"\nDOI: {doi}"
            entries.append(entry)
    return "\n\n".join(entries)


def _escape_latex(text: str) -> str:
    if not text:
        return ""
    replacements = [
        ("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"),
        ("_", "\\_"), ("{", "\\{"), ("}", "\\}"), ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]
    # Don't escape LaTeX commands that are already in the text
    # Only escape bare special chars
    result = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            result.append(text[i])
            i += 1
        else:
            char = text[i]
            escaped = False
            for orig, repl in replacements:
                if char == orig:
                    result.append(repl)
                    escaped = True
                    break
            if not escaped:
                result.append(char)
        i += 1
    return "".join(result)


async def export_latex(
    paper_id: str,
    sections: dict,
    citations: list[dict],
    venue: str,
    custom_template_path: str | None,
    author_name: str = "",
    author_affiliation: str = "",
) -> str:
    export_dir = EXPORTS_BASE / paper_id
    export_dir.mkdir(parents=True, exist_ok=True)

    template = _get_template(venue, custom_template_path)
    bibliography = _build_bibliography(citations)

    replacements = {
        "{{TITLE}}": sections.get("title", "Untitled"),
        "{{ABSTRACT}}": sections.get("abstract", ""),
        "{{KEYWORDS}}": ", ".join(sections.get("keywords", [])) if isinstance(sections.get("keywords"), list) else sections.get("keywords", ""),
        "{{INTRODUCTION}}": sections.get("introduction", ""),
        "{{LITERATURE_REVIEW}}": sections.get("literature_review", ""),
        "{{METHODOLOGY}}": sections.get("methodology", ""),
        "{{RESULTS}}": sections.get("results", ""),
        "{{DISCUSSION}}": sections.get("discussion", ""),
        "{{CONCLUSION}}": sections.get("conclusion", ""),
        "{{ACKNOWLEDGEMENTS}}": sections.get("acknowledgements", ""),
        "{{BIBLIOGRAPHY}}": bibliography,
        "{{AUTHOR_NAME}}": author_name,
        "{{AUTHOR_AFFILIATION}}": author_affiliation,
    }

    filled = template
    for placeholder, content in replacements.items():
        filled = filled.replace(placeholder, content or "")

    tex_path = export_dir / "paper.tex"
    tex_path.write_text(filled, encoding="utf-8")
    return str(tex_path)


def _build_markdown(
    sections: dict,
    citations: list[dict],
    author_name: str = "",
    author_affiliation: str = "",
) -> str:
    """Build a clean markdown representation of the paper for pandoc PDF rendering."""
    title = sections.get("title", "Untitled")
    lines = [
        f"% {title}",
        f"% {author_name}" if author_name else "% Author",
        f"% {author_affiliation}" if author_affiliation else "",
        "",
    ]

    abstract = sections.get("abstract", "")
    if abstract:
        lines += ["# Abstract", "", abstract, ""]

    keywords = sections.get("keywords", "")
    if keywords:
        kw = ", ".join(keywords) if isinstance(keywords, list) else keywords
        lines += [f"**Keywords:** {kw}", ""]

    section_order = [
        ("introduction", "Introduction"),
        ("literature_review", "Related Work"),
        ("methodology", "Methodology"),
        ("results", "Results"),
        ("discussion", "Discussion"),
        ("conclusion", "Conclusion"),
        ("acknowledgements", "Acknowledgements"),
    ]
    for key, heading in section_order:
        content = sections.get(key, "")
        if content and content.strip():
            lines += [f"# {heading}", "", content, ""]

    if citations:
        lines += ["# References", ""]
        for i, c in enumerate(citations, 1):
            authors = ", ".join(c.get("authors", ["Unknown Author"]))
            year = c.get("year", "")
            title_c = c.get("title", "Untitled")
            journal = c.get("journal", c.get("venue", ""))
            doi = c.get("doi", "")
            ref = f"{i}. {authors}"
            if year:
                ref += f" ({year})."
            ref += f" {title_c}."
            if journal:
                ref += f" *{journal}*."
            if doi:
                ref += f" doi:{doi}"
            lines.append(ref)

    return "\n".join(lines)


async def compile_pdf(tex_path: str, sections: dict = None, citations: list = None,
                      author_name: str = "", author_affiliation: str = "") -> str | None:
    tex_file = Path(tex_path)
    if not tex_file.exists():
        return None

    # Try LaTeX compilers first (best quality)
    for compiler_name in ("tectonic", "pdflatex", "xelatex", "lualatex"):
        compiler = shutil.which(compiler_name)
        if not compiler:
            continue
        if compiler_name == "tectonic":
            args = [compiler, str(tex_file)]
        else:
            args = [compiler, "-interaction=nonstopmode", "-output-directory",
                    str(tex_file.parent), str(tex_file)]
        try:
            subprocess.run(args, capture_output=True, text=True, timeout=120, cwd=str(tex_file.parent))
            pdf_path = tex_file.with_suffix(".pdf")
            if pdf_path.exists():
                return str(pdf_path)
        except Exception:
            continue

    # Fallback: pandoc + weasyprint (no LaTeX installation required)
    pandoc = shutil.which("pandoc")
    weasyprint_bin = shutil.which("weasyprint")
    if not pandoc:
        return None

    pdf_path = tex_file.with_suffix(".pdf")

    # First try: convert the .tex file directly via pandoc + weasyprint
    if weasyprint_bin:
        try:
            result = subprocess.run(
                [pandoc, str(tex_file), "--pdf-engine=weasyprint", "-o", str(pdf_path)],
                capture_output=True, text=True, timeout=120,
            )
            if pdf_path.exists():
                return str(pdf_path)
        except Exception:
            pass

    # Second try: build clean markdown and convert via pandoc + weasyprint
    if sections:
        md_content = _build_markdown(sections, citations or [], author_name, author_affiliation)
        md_path = tex_file.with_suffix(".md")
        md_path.write_text(md_content, encoding="utf-8")

        if weasyprint_bin:
            try:
                result = subprocess.run(
                    [pandoc, str(md_path), "--pdf-engine=weasyprint",
                     "--metadata", f"title={sections.get('title', 'Paper')}",
                     "-o", str(pdf_path)],
                    capture_output=True, text=True, timeout=120,
                )
                if pdf_path.exists():
                    return str(pdf_path)
            except Exception:
                pass

        # Third try: pandoc via wkhtmltopdf
        wkhtmltopdf = shutil.which("wkhtmltopdf")
        if wkhtmltopdf:
            try:
                result = subprocess.run(
                    [pandoc, str(md_path), "--pdf-engine=wkhtmltopdf", "-o", str(pdf_path)],
                    capture_output=True, text=True, timeout=120,
                )
                if pdf_path.exists():
                    return str(pdf_path)
            except Exception:
                pass

    return None


async def export_docx(
    tex_path: str,
    sections: dict = None,
    citations: list = None,
    author_name: str = "",
    author_affiliation: str = "",
) -> str | None:
    tex_file = Path(tex_path)
    if not tex_file.exists():
        return None
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return None
    docx_path = tex_file.with_suffix(".docx")

    # First try: convert .tex directly (works when LaTeX is clean)
    try:
        subprocess.run(
            [pandoc, str(tex_file), "-o", str(docx_path), "--standalone"],
            capture_output=True, text=True, timeout=60,
        )
        if docx_path.exists() and docx_path.stat().st_size > 1000:
            return str(docx_path)
    except Exception:
        pass

    # Fallback: build clean markdown and convert (more reliable)
    if sections:
        md_content = _build_markdown(sections, citations or [], author_name, author_affiliation)
        md_path = tex_file.with_suffix(".md")
        md_path.write_text(md_content, encoding="utf-8")
        try:
            subprocess.run(
                [pandoc, str(md_path), "-o", str(docx_path), "--standalone",
                 "--metadata", f"title={sections.get('title', 'Paper')}"],
                capture_output=True, text=True, timeout=60,
            )
            if docx_path.exists():
                return str(docx_path)
        except Exception:
            pass

    return None
