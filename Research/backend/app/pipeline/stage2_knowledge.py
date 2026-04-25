import json
from app.services import ollama_client as ai


async def run(full_text: str, existing_citations: list[dict]) -> dict:
    """Build the Knowledge Map from ingested content."""

    # Use up to 20k chars from the beginning for primary extraction.
    # If document is long, also take a sample from the second half to improve coverage.
    primary_sample = full_text[:20000]
    supplement = ""
    if len(full_text) > 25000:
        mid = len(full_text) // 2
        supplement = full_text[mid: mid + 6000]

    context = primary_sample
    if supplement:
        context += f"\n\n[...document continues...]\n\n{supplement}"

    km = await ai.generate_json(
        system=(
            "You are a senior research analyst. Extract precise, structured, grounded information "
            "from academic content. Every extracted field must be directly supported by the provided text — "
            "never invent data, claims, or results. Prioritize specificity over completeness. "
            "Output exact JSON only."
        ),
        user=f"""Analyze the following research content and extract a complete knowledge map.

CONTENT:
{context}

Extract the following as strict JSON. All fields must be grounded in the text above:
{{
  "domain": "primary academic field (e.g. 'Computer Science', 'Biology', 'Medicine')",
  "sub_domain": "specific sub-field (e.g. 'Natural Language Processing', 'Oncology')",
  "core_contribution": "one precise sentence stating what this work uniquely contributes",
  "research_questions": [
    "specific research question this work addresses (if stated)"
  ],
  "claims": [
    {{
      "text": "a specific factual claim from the content",
      "source_paragraph": "first 15 words of the paragraph where this claim appears",
      "claim_type": "empirical|theoretical|methodological|comparative"
    }}
  ],
  "methodology_steps": [
    "step 1 — be specific: name tools, datasets, algorithms used",
    "step 2",
    "..."
  ],
  "results": [
    {{
      "metric": "exact metric name (e.g. 'F1 score', 'accuracy', 'BLEU')",
      "value": "exact value or range (e.g. '92.3%', '0.87', '+4.2 points')",
      "description": "what system/condition this applies to",
      "is_primary": true
    }}
  ],
  "key_terms": ["term1", "term2", "..."],
  "author_frameworks": ["any named models, systems, or frameworks the author proposes — use the exact names"],
  "datasets": ["named datasets mentioned (e.g. 'GLUE', 'ImageNet', 'Penn Treebank')"],
  "evaluation_metrics": ["named evaluation metrics (e.g. 'BLEU', 'F1', 'perplexity', 'AUC')"],
  "limitations_mentioned": ["any limitations explicitly stated by the authors"],
  "has_quantitative_data": true,
  "has_experiments": true,
  "paper_language": "en"
}}

Guidelines:
- Extract up to 15 claims, 10 methodology steps, 12 results, 15 key terms
- For results: only include values explicitly stated in the text
- For methodology: be specific — 'fine-tuned BERT on SQuAD' not 'used a neural network'
- If the text is a survey/review with no original experiments, set has_experiments: false
- Base everything strictly on the provided content — no extrapolation""",
    )

    # Merge existing citations from GROBID into knowledge map
    km["existing_citations"] = existing_citations or []

    # Ensure all required keys exist with sensible defaults
    defaults: dict = {
        "domain": "Interdisciplinary Research",
        "sub_domain": "",
        "core_contribution": "This work presents findings relevant to the stated research topic.",
        "research_questions": [],
        "claims": [],
        "methodology_steps": [],
        "results": [],
        "key_terms": [],
        "author_frameworks": [],
        "datasets": [],
        "evaluation_metrics": [],
        "limitations_mentioned": [],
        "existing_citations": [],
        "has_quantitative_data": False,
        "has_experiments": False,
        "paper_language": "en",
    }
    for key, default in defaults.items():
        if key not in km or km[key] is None:
            km[key] = default

    # Normalise nested list items — some LLMs return plain strings instead of dicts
    if km["claims"] and isinstance(km["claims"][0], str):
        km["claims"] = [{"text": c, "source_paragraph": "", "claim_type": "empirical"} for c in km["claims"]]
    if km["results"] and isinstance(km["results"][0], str):
        km["results"] = [{"metric": "result", "value": r, "description": "", "is_primary": True} for r in km["results"]]

    return km
