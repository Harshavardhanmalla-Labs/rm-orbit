from app.services import ollama_client as ai


async def run(paper: dict, uploads_text: str) -> dict:
    warnings = []
    errors = []

    word_count = len(uploads_text.split())
    if word_count < 80:
        errors.append(f"Insufficient material: only {word_count} words extracted from uploaded files. Minimum 80 words required.")
        return {"passed": False, "warnings": warnings, "errors": errors}

    if word_count < 500:
        warnings.append(f"Limited source material ({word_count} words). Paper quality improves significantly with more content — consider adding experiment logs, results data, or reference papers.")

    # Topic/content alignment check
    topic = paper.get("topic", "")
    niche = paper.get("niche", "")
    sample = uploads_text[:3000]
    alignment_result = await ai.generate_json(
        "You are a research content analyst. Assess whether the provided text is relevant to the stated topic. Respond with JSON only.",
        f"""Topic: {topic}
Niche: {niche}
Content sample: {sample}

Assess alignment. Return:
{{"alignment_score": 0-10, "assessment": "brief explanation", "relevant": true/false}}"""
    )
    alignment_score = alignment_result.get("alignment_score", 5)
    if alignment_score < 3:
        warnings.append(f"Topic/content mismatch detected: uploaded documents may not align with declared topic '{topic}'. Assessment: {alignment_result.get('assessment', '')}")

    # Novelty detection for original research
    paper_type = paper.get("paper_type", "original_research")
    if paper_type == "original_research":
        novelty_result = await ai.generate_json(
            "You are a research novelty evaluator. Determine if the content contains original findings, methods, or frameworks. Respond with JSON only.",
            f"""Content: {uploads_text[:4000]}

Does this content contain:
- Original experiments or measurements?
- A novel methodology or algorithm?
- New frameworks or models proposed by the author?
- Original data or results?

Return: {{"novelty_score": 0-10, "novelty_indicators": ["...", "..."], "has_novelty": true/false, "paper_position": "original_research|survey|opinion"}}"""
        )
        novelty_score = novelty_result.get("novelty_score", 5)
        has_novelty = novelty_result.get("has_novelty", True)
        if not has_novelty or novelty_score < 3:
            warnings.append(
                f"Low novelty signal detected. The uploaded material appears to summarize existing work rather than presenting original findings. "
                f"The paper will be framed as a survey/review. To write an original research paper, upload your actual experiment results, datasets, or novel methodology documentation."
            )

    # Data presence check for quantitative papers
    has_numbers = any(c.isdigit() for c in uploads_text)
    has_table_markers = any(m in uploads_text.lower() for m in ["table", "figure", "fig.", "result", "accuracy", "performance", "%", "score"])
    if paper_type == "original_research" and not has_numbers:
        warnings.append("No quantitative data detected in uploaded files. Results section will be written qualitatively.")

    return {"passed": True, "warnings": warnings, "errors": errors, "word_count": word_count}
