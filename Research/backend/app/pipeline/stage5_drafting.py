import json
from app.services import ollama_client as ai

ACADEMIC_SYSTEM = (
    "You are an expert academic writer with 20 years of experience writing peer-reviewed research papers. "
    "Write in formal academic prose: third-person passive voice where appropriate, precise technical language, "
    "hedging language for claims (may suggest, appears to indicate, preliminary evidence shows), "
    "complex sentence structures with subordinate clauses. "
    "Every claim must be grounded in the provided research content. "
    "Never invent data, statistics, or citations not present in the source material. "
    "Write complete, publication-ready prose. No bullet points, no headings within the section unless appropriate."
)


async def _ensure_length(content: str, target: int, context_hint: str) -> str:
    """Extend the content if it is below 80 % of the target word count."""
    if len(content.split()) >= int(target * 0.80):
        return content
    shortfall = target - len(content.split())
    extension = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""Continue and expand the following academic text by approximately {shortfall} words.
Add more detail, deeper analysis, or additional supporting points. Do NOT repeat what is already written.
Context: {context_hint[:300]}

Text to extend:
{content[-2000:]}

Continue seamlessly from where the text ends:""",
    )
    return content + "\n\n" + extension.strip()


def _km_context(km: dict, anchor: dict) -> str:
    datasets = km.get("datasets", [])
    metrics = km.get("evaluation_metrics", [])
    limitations = km.get("limitations_mentioned", [])
    rq = km.get("research_questions", [])
    context = f"""Research Context:
Domain: {km.get('domain', '')} — {km.get('sub_domain', '')}
Core contribution: {anchor.get('novel_contribution', '')}
Key claim: {anchor.get('key_claim', '')}
Contribution type: {anchor.get('contribution_type', '')}
Problem: {anchor.get('problem_statement', '')}
Gap in prior art: {anchor.get('prior_art_gap', '')}
Key findings: {json.dumps(km.get('results', [])[:6])}
Key terms: {', '.join(km.get('key_terms', [])[:12])}
Author frameworks/systems: {', '.join(km.get('author_frameworks', []))}
Supporting evidence: {json.dumps(anchor.get('supporting_evidence', [])[:5])}"""
    if datasets:
        context += f"\nDatasets used: {', '.join(datasets)}"
    if metrics:
        context += f"\nEvaluation metrics: {', '.join(metrics)}"
    if limitations:
        context += f"\nAuthors' stated limitations: {json.dumps(limitations[:3])}"
    if rq:
        context += f"\nResearch questions: {json.dumps(rq[:2])}"
    return context


async def write_title(km: dict, anchor: dict, venue: str) -> str:
    result = await ai.generate_json(
        "You are an expert at crafting academic paper titles. Output JSON only.",
        f"""Generate 5 title candidates for a research paper.

{_km_context(km, anchor)}
Target venue: {venue}

Rules:
- 8-14 words each
- Must contain: domain keyword + method/approach keyword + contribution/result keyword
- Avoid: 'Novel approach to', 'An investigation into', 'A study of', 'Towards'
- Format: clear, informative, searchable on Google Scholar

Return: {{"titles": ["title1", "title2", "title3", "title4", "title5"], "recommended": 0}}"""
    )
    titles = result.get("titles", [])
    recommended = result.get("recommended", 0)
    if titles and isinstance(recommended, int) and 0 <= recommended < len(titles):
        return titles[recommended]
    return titles[0] if titles else f"Research on {km.get('domain', 'Emerging Topics')}: {anchor.get('novel_contribution', '')[:60]}"


async def write_keywords(km: dict, venue: str) -> list[str]:
    terms = km.get("key_terms", [])
    domain = km.get("domain", "")
    sub = km.get("sub_domain", "")
    # Build keyword list: domain + sub-domain + top key terms
    keywords = []
    if domain and domain not in keywords:
        keywords.append(domain)
    if sub and sub not in keywords:
        keywords.append(sub)
    keywords.extend([t for t in terms if t not in keywords])
    return keywords[:7]


async def write_introduction(km: dict, anchor: dict, outline_section: dict, venue: str, word_target: int) -> str:
    context = _km_context(km, anchor)
    target = max(400, word_target)

    # CARS Model: 3 moves as separate calls merged
    move1 = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write Move 1 of the Introduction (CARS model): Establish the research territory.
- Describe why {km.get('domain', 'this field')} is important and active
- Cite the general problem space
- 2-3 paragraphs, approximately {target // 4} words
- End with a transition toward the specific gap this work addresses
- Do not mention this paper's contribution yet"""
    )

    move2 = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write Move 2 of the Introduction (CARS model): Establish the niche.
Prior art gap: {anchor.get('prior_art_gap', '')}
Available existing citations: {json.dumps(km.get('existing_citations', [])[:5])}

- Describe what prior work has done (2-3 specific approaches with limitations)
- Identify the specific gap: {anchor.get('prior_art_gap', '')}
- Use hedging: 'however', 'nevertheless', 'despite these advances'
- 2 paragraphs, approximately {target // 4} words
- Reference prior work as (Author et al., Year) format"""
    )

    move3 = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write Move 3 of the Introduction (CARS model): Occupy the niche.
- State what this paper does: {anchor.get('novel_contribution', '')}
- Significance: {anchor.get('significance', '')}
- End with an explicit contributions list:
  "The contributions of this paper are as follows:
   \\begin{{itemize}}
   \\item [contribution 1]
   \\item [contribution 2]
   \\end{{itemize}}"
- Then briefly describe the paper's structure: "The remainder of this paper is organized as follows: Section 2..."
- 2 paragraphs + contributions list, approximately {target // 3} words"""
    )

    combined = f"{move1.strip()}\n\n{move2.strip()}\n\n{move3.strip()}"
    return await _ensure_length(combined, target, f"Introduction for a paper on {km.get('domain', '')}")


async def write_literature_review(km: dict, anchor: dict, outline_section: dict, word_target: int) -> str:
    context = _km_context(km, anchor)
    citations = km.get("existing_citations", [])
    cite_text = json.dumps(citations[:10], indent=2)

    text = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write the Literature Review / Related Work section.

Available citations to reference:
{cite_text}

Requirements:
- Organize thematically by sub-problem, not chronologically
- For EACH cited work provide: what it did + its specific limitation + how our work differs
- Use citation format: (AuthorLastName et al., Year) or [N] depending on venue
- Minimum 4 paragraphs
- Target: {word_target} words
- End with a paragraph that synthesizes the gap and positions this work
- Never copy text verbatim from the source material
- Use hedging: 'proposed', 'demonstrated', 'reported', 'suggested'
- Venue: {km.get('domain', '')}

Gap to establish: {anchor.get('prior_art_gap', '')}"""
    )
    return await _ensure_length(text, word_target, f"Literature review on {km.get('domain', '')}")


async def write_methodology(km: dict, anchor: dict, outline_section: dict, word_target: int) -> str:
    context = _km_context(km, anchor)
    steps = km.get("methodology_steps", [])

    datasets = km.get("datasets", [])
    metrics = km.get("evaluation_metrics", [])

    text = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write the Methodology section.

Methodology steps from source material:
{json.dumps(steps, indent=2)}

Requirements:
- Step-by-step, precise, reproducible — a reader should be able to replicate this work
- Name ALL tools, libraries, datasets, parameters, and hyperparameters mentioned in the source material
- Use passive voice: 'The model was trained on...', 'Data was pre-processed by...', 'The system was evaluated using...'
- Include subsections with \\subsection{{}} for: Data Collection, Model Architecture, Training Procedure, Evaluation Setup
- Target: {word_target} words
- Banned phrases: 'standard techniques', 'well-known methods', 'state-of-the-art methods', 'various approaches'
- If datasets are referenced, describe them: size, domain, split ratios
- Datasets referenced: {', '.join(datasets) if datasets else 'not specified'}
- Evaluation metrics used: {', '.join(metrics) if metrics else 'not specified'}
- Author frameworks/systems: {', '.join(km.get('author_frameworks', []))}
- Describe each component of the proposed system/approach in detail"""
    )
    return await _ensure_length(text, word_target, f"Methodology for {anchor.get('novel_contribution', '')}")


async def write_results(km: dict, outline_section: dict, word_target: int) -> str:
    context = _km_context(km, {})
    results_data = km.get("results", [])
    figures = km.get("figures", [])

    text = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write the Results section.

Quantitative/qualitative results from source material:
{json.dumps(results_data, indent=2)}

Figures and tables available:
{json.dumps(figures[:5], indent=2)}

Requirements:
- Describe results ONLY — do not interpret or discuss implications (that goes in Discussion)
- Reference figures and tables: 'As shown in Table 1...', 'Figure 2 illustrates...'
- If quantitative results are available, report exact numbers
- If only qualitative results: describe findings precisely and note the qualitative nature
- Passive voice throughout
- Target: {word_target} words
- Present in logical order (primary results first, secondary results second)"""
    )
    return await _ensure_length(text, word_target, f"Results for {km.get('domain', '')}")


async def write_discussion(km: dict, anchor: dict, results_text: str, outline_section: dict, word_target: int) -> str:
    context = _km_context(km, anchor)
    citations = km.get("existing_citations", [])

    limitations = km.get("limitations_mentioned", [])
    limitations_hint = (
        f"Author-stated limitations to include: {json.dumps(limitations)}"
        if limitations
        else "No explicit limitations stated — derive 2-3 specific ones from the methodology and results."
    )

    text = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write the Discussion section.

Results summary: {results_text[:1500]}
Available prior work for comparison: {json.dumps(citations[:6], indent=2)}
{limitations_hint}

Required structure (4 parts — each must be a substantive paragraph):
1. Interpretation: What do these results mean? Explain WHY the results are what they are. Connect each result to the contribution claim specifically.
2. Comparison to prior work: How do results compare to at least 2 cited works explicitly? State where this work outperforms or falls short.
3. Limitations: Enumerate specific, honest limitations. Be precise: 'The evaluation was conducted on a single dataset of X size' not 'More data is needed'.
4. Implications and future work: What does this mean for the field? Name 2-3 concrete future research directions.

Requirements:
- Target: {word_target} words
- Limitations must be specific — generic phrases like 'Future work is needed' are banned
- Use passive voice and impersonal constructions
- Contribution restated: {anchor.get('novel_contribution', '')}
- Significance: {anchor.get('significance', '')}"""
    )
    return await _ensure_length(text, word_target, f"Discussion on {anchor.get('novel_contribution', '')}")


async def write_conclusion(km: dict, anchor: dict, discussion_text: str, outline_section: dict, word_target: int) -> str:
    context = _km_context(km, anchor)

    text = await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""{context}

Write the Conclusion section.

Discussion summary: {discussion_text[:1000]}

Required 3-part structure:
1. Summary (what was done): Restate the problem and approach in 2-3 sentences
2. Key findings (what was found): Summarize the main results and contribution
3. Future work (what comes next): Specific, actionable future directions (NOT vague — must name specific extensions)

Rules:
- NO new information — only reframe what's already in the paper
- NO 'In conclusion,' as the opening words
- Future work must be specific: 'Future work will extend this approach to X' NOT 'More research is needed'
- Target: {word_target} words
- Contribution to restate: {anchor.get('novel_contribution', '')}"""
    )
    return await _ensure_length(text, word_target, f"Conclusion for paper on {km.get('domain', '')}")


async def write_abstract(sections: dict, anchor: dict, venue: str, word_target: int = 200) -> str:
    # Build a summary from actual sections — abstract is written from the body
    intro_snippet = (sections.get("introduction") or "")[:800]
    results_snippet = (sections.get("results") or "")[:600]
    conclusion_snippet = (sections.get("conclusion") or "")[:400]

    return await ai.generate_long(
        ACADEMIC_SYSTEM,
        f"""Write the Abstract for this research paper. The abstract must be written FROM the actual paper content below.

Paper content:
Introduction (excerpt): {intro_snippet}
Results (excerpt): {results_snippet}
Conclusion (excerpt): {conclusion_snippet}

Contribution: {anchor.get('novel_contribution', '')}
Problem: {anchor.get('problem_statement', '')}
Significance: {anchor.get('significance', '')}

Abstract formula (strictly follow):
Sentence 1: State the problem this paper addresses
Sentence 2-3: State what this paper does (the method/approach)
Sentence 4: State the key result or finding
Sentence 5: State the significance/implication

Rules:
- Target: {min(word_target, 250)} words (never exceed 250 for most venues)
- No citations
- No undefined acronyms
- Passive voice dominant
- Must be self-contained — a reader should understand the full paper from this alone
- Venue: {venue}"""
    )


async def write_acknowledgements(author_name: str, affiliation: str) -> str:
    parts = [f"The author thanks the research community for valuable discussions and feedback on this work."]
    if affiliation:
        parts.append(f"This work was conducted at {affiliation}.")
    return " ".join(parts)


async def run(
    paper_id: str,
    knowledge_map: dict,
    contribution_anchor: dict,
    outline: dict,
    paper: dict,
) -> dict:
    """Run all section writers in sequence. Abstract is written last."""
    from app.database import update_paper

    venue = paper.get("target_venue", "arxiv")
    word_target = paper.get("word_count_target", 8000)
    author_name = paper.get("author_name", "")
    author_affiliation = paper.get("author_affiliation", "")
    section_outlines = outline.get("section_outlines", {})

    sections: dict = {}

    # Title and keywords first
    sections["title"] = await write_title(knowledge_map, contribution_anchor, venue)
    sections["keywords"] = await write_keywords(knowledge_map, venue)
    await update_paper(paper_id, sections=sections)

    # Introduction
    intro_outline = section_outlines.get("introduction", {})
    intro_target = intro_outline.get("target_word_count", 600)
    sections["introduction"] = await write_introduction(knowledge_map, contribution_anchor, intro_outline, venue, intro_target)
    await update_paper(paper_id, sections=sections)

    # Literature review
    lit_outline = section_outlines.get("literature_review", {})
    lit_target = lit_outline.get("target_word_count", 800)
    sections["literature_review"] = await write_literature_review(knowledge_map, contribution_anchor, lit_outline, lit_target)
    await update_paper(paper_id, sections=sections)

    # Methodology
    method_outline = section_outlines.get("methodology", {})
    method_target = method_outline.get("target_word_count", 700)
    sections["methodology"] = await write_methodology(knowledge_map, contribution_anchor, method_outline, method_target)
    await update_paper(paper_id, sections=sections)

    # Results
    results_outline = section_outlines.get("results", {})
    results_target = results_outline.get("target_word_count", 600)
    sections["results"] = await write_results(knowledge_map, results_outline, results_target)
    await update_paper(paper_id, sections=sections)

    # Discussion
    discussion_outline = section_outlines.get("discussion", {})
    discussion_target = discussion_outline.get("target_word_count", 700)
    sections["discussion"] = await write_discussion(
        knowledge_map, contribution_anchor,
        sections.get("results", ""), discussion_outline, discussion_target
    )
    await update_paper(paper_id, sections=sections)

    # Conclusion
    conclusion_outline = section_outlines.get("conclusion", {})
    conclusion_target = conclusion_outline.get("target_word_count", 300)
    sections["conclusion"] = await write_conclusion(
        knowledge_map, contribution_anchor,
        sections.get("discussion", ""), conclusion_outline, conclusion_target
    )
    await update_paper(paper_id, sections=sections)

    # Acknowledgements
    sections["acknowledgements"] = await write_acknowledgements(author_name, author_affiliation)

    # Abstract LAST — from actual body
    sections["abstract"] = await write_abstract(sections, contribution_anchor, venue)
    await update_paper(paper_id, sections=sections, title=sections["title"])

    return sections
