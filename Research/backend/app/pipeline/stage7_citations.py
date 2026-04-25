import re
import json
from app.services import crossref_client, openalex_client


def _make_bibtex_key(authors: list[str], year: str, title: str) -> str:
    first_author = (authors[0].split(",")[0] if authors else "unknown").lower()
    first_author = re.sub(r'[^a-z]', '', first_author)
    year_str = str(year)[:4] if year else "2024"
    title_word = re.sub(r'[^a-z]', '', (title.split()[0] if title else "paper").lower())
    return f"{first_author}{year_str}{title_word}"


def _build_bibtex(citation: dict, key: str) -> str:
    authors = " and ".join(citation.get("authors", ["Unknown Author"]))
    year = citation.get("year", "2024")
    title = citation.get("title", "Untitled")
    journal = citation.get("journal", citation.get("venue", ""))
    doi = citation.get("doi", "")

    lines = [f"@article{{{key},"]
    lines.append(f'  author = {{{authors}}},')
    lines.append(f'  title = {{{{{title}}}}},')
    if journal:
        lines.append(f'  journal = {{{journal}}},')
    lines.append(f'  year = {{{year}}},')
    if doi:
        lines.append(f'  doi = {{{doi}}},')
        lines.append(f'  url = {{https://doi.org/{doi}}},')
    lines.append("}")
    return "\n".join(lines)


def _format_ieee(citation: dict, number: int) -> str:
    authors = ", ".join(citation.get("authors", ["Unknown"])[:3])
    if len(citation.get("authors", [])) > 3:
        authors += " et al."
    title = citation.get("title", "Untitled")
    journal = citation.get("journal", citation.get("venue", ""))
    year = citation.get("year", "n.d.")
    doi = citation.get("doi", "")
    result = f"[{number}] {authors}, \"{title},\" {journal}"
    if year:
        result += f", {year}."
    if doi:
        result += f" doi: {doi}"
    return result


def _format_apa(citation: dict) -> str:
    authors = citation.get("authors", ["Unknown"])
    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) <= 6:
        author_str = ", ".join(authors[:-1]) + ", & " + authors[-1]
    else:
        author_str = ", ".join(authors[:6]) + ", et al."
    year = citation.get("year", "n.d.")
    title = citation.get("title", "Untitled")
    journal = citation.get("journal", citation.get("venue", ""))
    doi = citation.get("doi", "")
    result = f"{author_str} ({year}). {title}."
    if journal:
        result += f" {journal}."
    if doi:
        result += f" https://doi.org/{doi}"
    return result


async def run(knowledge_map: dict, sections: dict, target_venue: str) -> list[dict]:
    raw_citations = knowledge_map.get("existing_citations", [])
    full_text = " ".join(str(v) for v in sections.values() if isinstance(v, str))

    # Supplement if fewer than 8 citations
    if len(raw_citations) < 8:
        topic_query = f"{knowledge_map.get('domain', '')} {knowledge_map.get('sub_domain', '')} {knowledge_map.get('core_contribution', '')}"
        additional = await openalex_client.search_works(topic_query.strip(), limit=max(0, 10 - len(raw_citations)))
        seen_titles = {c.get("title", "").lower() for c in raw_citations}
        for a in additional:
            if a.get("title", "").lower() not in seen_titles:
                raw_citations.append(a)
                seen_titles.add(a.get("title", "").lower())

    verified_citations = []
    for i, cite in enumerate(raw_citations, 1):
        doi = cite.get("doi", "")
        verified_data = None

        if doi:
            verified_data = await crossref_client.verify_doi(doi)

        if verified_data:
            merged = {**cite, **verified_data}
        else:
            merged = dict(cite)
            merged["verified"] = False

        key = _make_bibtex_key(
            merged.get("authors", []),
            merged.get("year", ""),
            merged.get("title", "")
        )
        merged["bibtex_key"] = key
        merged["bibtex_entry"] = _build_bibtex(merged, key)
        merged["formatted_ieee"] = _format_ieee(merged, i)
        merged["formatted_apa"] = _format_apa(merged)
        merged.setdefault("verified", bool(doi and verified_data))

        verified_citations.append(merged)

    return verified_citations


def build_confidence_report(sections: dict, knowledge_map: dict, citations: list[dict], quality_result: dict) -> dict:
    full_text = " ".join(str(v) for v in sections.values() if isinstance(v, str))
    all_words = full_text.split()
    total_words = len(all_words)

    claims = knowledge_map.get("claims", [])
    sourced = sum(1 for c in claims if c.get("source_paragraph"))
    claim_sourcing_pct = round((sourced / max(len(claims), 1)) * 100)

    # Compute source coverage from richness of extracted knowledge map
    n_claims = len(knowledge_map.get("claims", []))
    n_results = len(knowledge_map.get("results", []))
    n_steps = len(knowledge_map.get("methodology_steps", []))
    n_terms = len(knowledge_map.get("key_terms", []))
    has_datasets = bool(knowledge_map.get("datasets"))
    has_metrics = bool(knowledge_map.get("evaluation_metrics"))
    has_frameworks = bool(knowledge_map.get("author_frameworks"))

    coverage_score = (
        min(25, n_claims * 2)        # up to 25 pts from claims (12+ → 25)
        + min(20, n_results * 2)     # up to 20 pts from results
        + min(20, n_steps * 3)       # up to 20 pts from methodology steps
        + min(15, n_terms)           # up to 15 pts from key terms
        + (10 if has_datasets else 0)
        + (5 if has_metrics else 0)
        + (5 if has_frameworks else 0)
    )
    source_coverage_pct = min(100, coverage_score)

    verified = [c for c in citations if c.get("verified")]
    total_cites = len(citations)
    verified_count = len(verified)

    body_sections = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
    present = sum(1 for s in body_sections if sections.get(s, "").strip())
    section_completeness = f"{present}/{len(body_sections)}"

    register_issues = [i for i in quality_result.get("issues", []) if i["pass"] == "academic_register"]
    academic_register_pass = len(register_issues) == 0

    clarity_issues = [i for i in quality_result.get("issues", []) if i["pass"] == "contribution_clarity"]
    if not clarity_issues:
        contribution_clarity = "high"
    elif len(clarity_issues) == 1:
        contribution_clarity = "medium"
    else:
        contribution_clarity = "low"

    flags = []
    for issue in quality_result.get("issues", []):
        severity = "warning" if any(w in issue["message"].lower() for w in ["may", "could", "weak", "low"]) else "info"
        flags.append({"severity": severity, "message": issue["message"], "pass": issue["pass"]})

    # Citation count check — runs here after citations are available
    if total_cites < 8:
        flags.append({
            "severity": "warning",
            "message": f"Low citation count ({total_cites}). Academic papers typically cite ≥8 sources.",
            "pass": "citation_integrity"
        })
    if verified_count < total_cites:
        unverified_count = total_cites - verified_count
        flags.append({
            "severity": "warning",
            "message": f"{unverified_count} citation(s) could not be verified via CrossRef — marked unverified in references.",
            "pass": "citations"
        })

    return {
        "source_coverage_pct": source_coverage_pct,
        "claim_sourcing_pct": claim_sourcing_pct,
        "verified_citations": verified_count,
        "total_citations": total_cites,
        "section_completeness": section_completeness,
        "total_word_count": total_words,
        "academic_register_pass": academic_register_pass,
        "contribution_clarity": contribution_clarity,
        "flags": flags,
    }
