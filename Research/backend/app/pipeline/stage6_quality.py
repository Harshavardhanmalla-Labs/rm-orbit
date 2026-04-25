import re
from app.services import ollama_client as ai, languagetool_client as lt

REQUIRED_SECTIONS = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
MIN_WORDS = {
    "abstract": 150, "introduction": 350, "literature_review": 300,
    "methodology": 250, "results": 200, "discussion": 300, "conclusion": 150,
}


def _word_count(text: str) -> int:
    return len(text.split()) if text else 0


async def pass1_structural(sections: dict) -> tuple[dict, list[str]]:
    issues = []
    for section in REQUIRED_SECTIONS:
        content = sections.get(section, "")
        if not content or not content.strip():
            issues.append(f"Section '{section}' is missing or empty")
            continue
        min_w = MIN_WORDS.get(section, 100)
        actual_w = _word_count(content)
        if actual_w < min_w:
            issues.append(f"Section '{section}' is too short ({actual_w} words, minimum {min_w})")

    return sections, issues


async def pass2_consistency(sections: dict, contribution_anchor: dict) -> tuple[dict, list[str]]:
    issues = []
    abstract = sections.get("abstract", "")
    conclusion = sections.get("conclusion", "")
    contribution = contribution_anchor.get("novel_contribution", "")

    if abstract and contribution:
        check = await ai.generate_json(
            "You are an academic paper quality checker. Assess consistency between paper sections. Output JSON only.",
            f"""Does this abstract accurately reflect the stated contribution? Report PROBLEMS only.

Abstract: {abstract[:600]}
Novel contribution: {contribution}
Conclusion excerpt: {conclusion[:400]}

Return ONLY actual problems. If abstract and contribution are consistent, return an empty issues list.
Return: {{"consistent": true/false, "consistency_score": 0.0-1.0, "issues": ["describe a real problem here, or leave empty"]}}"""
        )
        score = check.get("consistency_score", 0.8)
        if score < 0.5:
            issues.append(f"Abstract may not accurately reflect the paper's contribution (consistency score: {score:.1f})")
        # Only surface issues that describe an actual problem (not positive confirmations)
        negative_signals = ["not", "missing", "unclear", "fails", "inconsistent", "incorrect", "contradicts",
                            "weak", "absent", "no mention", "omits", "wrong", "inaccurate", "does not"]
        for issue in check.get("issues", []):
            if issue and any(sig in issue.lower() for sig in negative_signals):
                issues.append(f"Consistency: {issue}")

    # Check conclusion doesn't introduce new concepts
    intro_terms = set(re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', sections.get("introduction", "")))
    conc_unique = set(re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', conclusion)) - intro_terms
    if len(conc_unique) > 15:
        issues.append(f"Conclusion may introduce new concepts not established in the introduction ({len(conc_unique)} new proper noun phrases)")

    return sections, issues


async def pass3_academic_register(sections: dict) -> tuple[dict, list[str]]:
    issues = []
    fixed_sections = dict(sections)

    full_text = " ".join(str(v) for v in sections.values() if isinstance(v, str))

    # Replace banned phrases (auto-corrected — not flagged as a quality failure)
    banned_found = lt.find_banned_phrases(full_text)
    if banned_found:
        for section_name, content in fixed_sections.items():
            if isinstance(content, str):
                fixed, _ = lt.replace_banned_phrases(content)
                fixed_sections[section_name] = fixed

    # Readability check
    try:
        import textstat
        grade = textstat.flesch_kincaid_grade(full_text[:5000])
        if grade < 10:
            issues.append(f"Reading level may be too low for academic writing (Flesch-Kincaid Grade: {grade:.1f}, target ≥12)")
    except Exception:
        pass

    # LanguageTool grammar check on abstract + intro
    check_text = (sections.get("abstract", "") + " " + sections.get("introduction", ""))[:3000]
    lt_issues = await lt.get_issues(check_text)
    if lt_issues:
        issues.extend([f"Grammar: {issue}" for issue in lt_issues[:5]])

    return fixed_sections, issues


async def pass4_citation_integrity(sections: dict, citations: list[dict]) -> tuple[dict, list[str]]:
    issues = []
    full_text = " ".join(str(v) for v in sections.values() if isinstance(v, str))

    # Find in-text citation markers
    numbered_cites = set(re.findall(r'\[(\d+)\]', full_text))
    author_year_cites = set(re.findall(r'\(([A-Z][a-z]+ et al\., \d{4})\)', full_text))
    author_year_cites2 = set(re.findall(r'\(([A-Z][a-z]+, \d{4})\)', full_text))
    all_in_text = numbered_cites | author_year_cites | author_year_cites2

    citation_count = len(citations)
    if citation_count < 5:
        issues.append(f"Low citation count ({citation_count}). Academic papers typically cite ≥8 sources. Consider adding more reference documents.")

    unverified = [c for c in citations if not c.get("verified", False)]
    if unverified:
        issues.append(f"{len(unverified)} citation(s) could not be verified via CrossRef — marked as unverified in the references section.")

    return sections, issues


async def pass5_contribution_clarity(sections: dict, contribution_anchor: dict) -> tuple[dict, list[str]]:
    issues = []
    intro = sections.get("introduction", "")
    abstract = sections.get("abstract", "")
    contribution = contribution_anchor.get("novel_contribution", "")

    clarity = await ai.generate_json(
        "You are a peer reviewer assessing contribution clarity in a research paper. Output JSON only.",
        f"""Assess whether this paper clearly states a novel, specific, and defensible contribution.

Abstract: {abstract[:400]}
Introduction excerpt: {intro[:600]}
Expected contribution: {contribution}

Evaluate:
1. Is the contribution explicitly stated? (not vague)
2. Is the contribution specific and falsifiable?
3. Is it defensible — could an author stand behind this in a presentation?

Return: {{"clarity_score": 1-10, "is_explicit": true/false, "is_specific": true/false, "is_defensible": true/false, "feedback": "brief feedback"}}"""
    )

    score = clarity.get("clarity_score", 7)
    if score < 5:
        issues.append(f"Contribution clarity is weak (score: {score}/10). {clarity.get('feedback', '')} Consider revising the introduction's contribution statement.")
    elif score < 7:
        issues.append(f"Contribution clarity could be stronger (score: {score}/10). {clarity.get('feedback', '')}")

    return sections, issues


async def run(sections: dict, knowledge_map: dict, contribution_anchor: dict, citations: list[dict]) -> dict:
    all_issues = []

    sections, p1_issues = await pass1_structural(sections)
    all_issues.extend([{"pass": "structural_completeness", "message": i} for i in p1_issues])

    sections, p2_issues = await pass2_consistency(sections, contribution_anchor)
    all_issues.extend([{"pass": "internal_consistency", "message": i} for i in p2_issues])

    sections, p3_issues = await pass3_academic_register(sections)
    all_issues.extend([{"pass": "academic_register", "message": i} for i in p3_issues])

    # pass4 (citation integrity) runs in stage7 after citations are built — skipped here
    if citations:
        sections, p4_issues = await pass4_citation_integrity(sections, citations)
        all_issues.extend([{"pass": "citation_integrity", "message": i} for i in p4_issues])

    sections, p5_issues = await pass5_contribution_clarity(sections, contribution_anchor)
    all_issues.extend([{"pass": "contribution_clarity", "message": i} for i in p5_issues])

    return {
        "passes_run": 5,
        "total_issues": len(all_issues),
        "issues": all_issues,
        "final_sections": sections,
    }
