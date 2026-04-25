import pytest
from unittest.mock import AsyncMock, patch

import app.pipeline.stage3_contribution as stage3

BASE_KM = {
    "domain": "Computer Science",
    "sub_domain": "NLP",
    "core_contribution": "A fast tokenizer for low-resource languages.",
    "research_questions": ["How to improve tokenization speed?"],
    "claims": [],
    "methodology_steps": [],
    "results": [],
    "author_frameworks": [],
    "datasets": [],
    "evaluation_metrics": [],
}

BASE_PAPER = {"topic": "Tokenization", "niche": "Low-resource NLP", "paper_type": "original_research"}


@pytest.mark.asyncio
async def test_defaults_applied_when_llm_returns_empty():
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value={})):
        anchor = await stage3.run(BASE_KM, BASE_PAPER)

    assert "problem_statement" in anchor
    assert "novel_contribution" in anchor
    assert anchor["novelty_confidence"] == "medium"
    assert anchor["contribution_type"] == "algorithm"


@pytest.mark.asyncio
async def test_novel_contribution_falls_back_to_km_core_contribution():
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value={})):
        anchor = await stage3.run(BASE_KM, BASE_PAPER)

    assert anchor["novel_contribution"] == BASE_KM["core_contribution"]


@pytest.mark.asyncio
async def test_key_claim_falls_back_to_km_core_contribution():
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value={})):
        anchor = await stage3.run(BASE_KM, BASE_PAPER)

    assert anchor["key_claim"] == BASE_KM["core_contribution"]


@pytest.mark.asyncio
async def test_paper_position_defaults_to_paper_type():
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value={})):
        anchor = await stage3.run(BASE_KM, BASE_PAPER)

    assert anchor["paper_position"] == BASE_PAPER["paper_type"]


@pytest.mark.asyncio
async def test_llm_values_preserved_when_provided():
    llm_response = {
        "problem_statement": "Custom problem.",
        "prior_art_gap": "Existing gap.",
        "novel_contribution": "Our specific method.",
        "supporting_evidence": ["evidence 1"],
        "significance": "High impact.",
        "novelty_confidence": "high",
        "paper_position": "survey",
        "key_claim": "Custom key claim.",
        "contribution_type": "framework",
    }
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value=llm_response)):
        anchor = await stage3.run(BASE_KM, BASE_PAPER)

    assert anchor["novelty_confidence"] == "high"
    assert anchor["contribution_type"] == "framework"
    assert anchor["novel_contribution"] == "Our specific method."


@pytest.mark.asyncio
async def test_domain_used_in_default_problem_statement():
    km = dict(BASE_KM)
    km["domain"] = "Biology"
    with patch.object(stage3.ai, "generate_json", new=AsyncMock(return_value={})):
        anchor = await stage3.run(km, BASE_PAPER)

    assert "Biology" in anchor["problem_statement"]
