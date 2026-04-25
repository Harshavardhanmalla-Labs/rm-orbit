import json
from app.services import ollama_client as ai


async def run(knowledge_map: dict, paper: dict) -> dict:
    """Discover and structure the contribution anchor."""
    km_summary = {
        "domain": knowledge_map.get("domain"),
        "sub_domain": knowledge_map.get("sub_domain"),
        "core_contribution": knowledge_map.get("core_contribution"),
        "research_questions": knowledge_map.get("research_questions", []),
        "claims": knowledge_map.get("claims", [])[:8],
        "methodology_steps": knowledge_map.get("methodology_steps", [])[:6],
        "results": knowledge_map.get("results", [])[:6],
        "author_frameworks": knowledge_map.get("author_frameworks", []),
        "datasets": knowledge_map.get("datasets", []),
        "evaluation_metrics": knowledge_map.get("evaluation_metrics", []),
    }

    anchor = await ai.generate_json(
        system=(
            "You are an expert academic contribution analyst and peer reviewer. "
            "Your task is to identify and articulate the novel contribution of a research work "
            "based on extracted knowledge. Be precise, specific, and grounded — only state what the evidence supports. "
            "Use formal academic language. Output JSON only."
        ),
        user=f"""Based on the following knowledge map, identify the research contribution with precision.

Topic: {paper.get('topic', '')}
Niche: {paper.get('niche', '')}
Paper Type: {paper.get('paper_type', 'original_research')}

Knowledge Map:
{json.dumps(km_summary, indent=2)}

Answer these questions and return as JSON:
{{
  "problem_statement": "What specific problem or gap does this work address? (2-3 sentences — be precise about the pain point)",
  "prior_art_gap": "What have previous approaches failed to do or address? (2-3 sentences, grounded in the content — name specific limitations)",
  "novel_contribution": "What exactly is new — the specific method, result, framework, or insight? (2-3 sentences — avoid vague claims like 'we propose a novel approach')",
  "supporting_evidence": [
    "specific evidence item 1 from results or methodology",
    "specific evidence item 2",
    "specific evidence item 3",
    "specific evidence item 4"
  ],
  "significance": "Why does this matter — who benefits and what changes in practice? (2-3 sentences)",
  "novelty_confidence": "high|medium|low|none",
  "paper_position": "original_research|survey|opinion|case_study",
  "key_claim": "The single most important testable claim this paper makes (1 sentence)",
  "contribution_type": "algorithm|framework|dataset|evaluation|theory|system|survey"
}}

Guidance:
- 'high' novelty: clear original method/algorithm/experiment/dataset with measurable results
- 'medium' novelty: incremental improvement or new application of existing method
- 'low' novelty: mostly re-implementation or summary with minor additions
- 'none': pure survey or literature review with no original contribution""",
    )

    defaults = {
        "problem_statement": f"This work addresses challenges in {knowledge_map.get('domain', 'the research domain')}.",
        "prior_art_gap": "Existing approaches have not fully addressed the problem described in this work.",
        "novel_contribution": knowledge_map.get("core_contribution", "This work presents a new approach to the stated problem."),
        "supporting_evidence": [],
        "significance": "This contribution advances the state of knowledge in the field.",
        "novelty_confidence": "medium",
        "paper_position": paper.get("paper_type", "original_research"),
        "key_claim": knowledge_map.get("core_contribution", ""),
        "contribution_type": "algorithm",
    }
    for key, default in defaults.items():
        if key not in anchor or anchor[key] is None:
            anchor[key] = default

    return anchor
