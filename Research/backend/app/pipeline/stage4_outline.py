from app.services import ollama_client as ai

VENUE_SECTIONS = {
    "ieee": ["introduction", "literature_review", "methodology", "results", "discussion", "conclusion"],
    "acm": ["introduction", "background", "literature_review", "methodology", "results", "discussion", "conclusion"],
    "arxiv": ["introduction", "literature_review", "methodology", "results", "discussion", "conclusion"],
    "nature": ["introduction", "results", "discussion", "methodology", "literature_review", "conclusion"],
    "springer": ["introduction", "literature_review", "methodology", "results", "discussion", "conclusion"],
    "custom": ["introduction", "literature_review", "methodology", "results", "discussion", "conclusion"],
}

SECTION_WORD_TARGETS = {
    "introduction": 600,
    "literature_review": 800,
    "background": 400,
    "methodology": 700,
    "results": 600,
    "discussion": 700,
    "conclusion": 300,
}


async def run(knowledge_map: dict, contribution_anchor: dict, paper: dict) -> dict:
    venue = paper.get("target_venue", "arxiv")
    word_target = paper.get("word_count_target", 8000)
    sections = VENUE_SECTIONS.get(venue, VENUE_SECTIONS["arxiv"])

    # Scale section word targets proportionally to hit the requested word_count_target.
    # Reserve ~300 words for abstract + acknowledgements (not in section loop).
    body_target = max(word_target - 300, 1000)
    base_total = sum(SECTION_WORD_TARGETS.get(s, 500) for s in sections)
    scale = body_target / max(base_total, 1)

    outline = {}
    for section in sections:
        base_words = SECTION_WORD_TARGETS.get(section, 500)
        target_words = max(200, int(base_words * scale))

        # Get relevant citations for this section
        all_citations = knowledge_map.get("existing_citations", [])
        relevant_cites = all_citations[:5] if section in ("literature_review", "background") else all_citations[:2]

        # Generate key points for this section from knowledge map
        section_outline = await ai.generate_json(
            system="You are an academic writing planner. Generate a focused outline for a specific paper section. Output JSON only.",
            user=f"""Generate an outline for the '{section.replace('_', ' ').title()}' section.

Paper topic: {paper.get('topic', '')}
Contribution: {contribution_anchor.get('novel_contribution', '')}
Problem: {contribution_anchor.get('problem_statement', '')}
Key terms: {', '.join(knowledge_map.get('key_terms', [])[:8])}
Available results: {knowledge_map.get('results', [])[:4]}
Target word count: {target_words}

Return:
{{
  "target_word_count": {target_words},
  "key_points": ["point 1 to cover", "point 2", "point 3", "point 4"],
  "opening_sentence": "suggested opening sentence for this section",
  "must_address": ["specific thing from knowledge map to address", "..."]
}}""",
        )

        outline[section] = {
            "target_word_count": target_words,
            "key_points": section_outline.get("key_points", []),
            "opening_sentence": section_outline.get("opening_sentence", ""),
            "must_address": section_outline.get("must_address", []),
            "relevant_citations": [c.get("title", "") for c in relevant_cites],
        }

    return {"sections": sections, "venue": venue, "section_outlines": outline, "total_word_target": word_target}
