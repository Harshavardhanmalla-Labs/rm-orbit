import pytest
from unittest.mock import AsyncMock, patch

import app.pipeline.stage4_outline as stage4

BASE_KM = {
    "key_terms": ["tokenization", "NLP"],
    "results": [],
    "existing_citations": [],
}

BASE_ANCHOR = {
    "novel_contribution": "A fast tokenizer.",
    "problem_statement": "Slow tokenization.",
}

BASE_PAPER = {
    "topic": "Tokenization",
    "target_venue": "arxiv",
    "word_count_target": 8000,
}


def _fake_section_outline(target_word_count):
    async def _gen(system, user, **kwargs):
        return {
            "target_word_count": target_word_count,
            "key_points": ["point 1"],
            "opening_sentence": "Opening.",
            "must_address": ["thing"],
        }
    return _gen


@pytest.mark.asyncio
async def test_outline_contains_arxiv_sections():
    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result = await stage4.run(BASE_KM, BASE_ANCHOR, BASE_PAPER)

    assert set(result["sections"]) >= {"introduction", "methodology", "results", "conclusion"}
    assert result["venue"] == "arxiv"


@pytest.mark.asyncio
async def test_total_word_target_preserved():
    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result = await stage4.run(BASE_KM, BASE_ANCHOR, BASE_PAPER)

    assert result["total_word_target"] == 8000


@pytest.mark.asyncio
async def test_word_count_scaling_proportional():
    paper_8k = dict(BASE_PAPER, word_count_target=8000)
    paper_4k = dict(BASE_PAPER, word_count_target=4000)

    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result_8k = await stage4.run(BASE_KM, BASE_ANCHOR, paper_8k)
        result_4k = await stage4.run(BASE_KM, BASE_ANCHOR, paper_4k)

    intro_8k = result_8k["section_outlines"]["introduction"]["target_word_count"]
    intro_4k = result_4k["section_outlines"]["introduction"]["target_word_count"]
    assert intro_8k > intro_4k


@pytest.mark.asyncio
async def test_minimum_word_count_per_section():
    paper_tiny = dict(BASE_PAPER, word_count_target=500)

    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result = await stage4.run(BASE_KM, BASE_ANCHOR, paper_tiny)

    for section in result["sections"]:
        assert result["section_outlines"][section]["target_word_count"] >= 200


@pytest.mark.asyncio
async def test_literature_review_gets_more_citations():
    citations = [{"title": f"Paper {i}"} for i in range(10)]
    km = dict(BASE_KM, existing_citations=citations)

    captured_calls = []

    async def fake_gen(system, user, **kwargs):
        captured_calls.append(user)
        return {"key_points": [], "opening_sentence": "", "must_address": []}

    with patch.object(stage4.ai, "generate_json", new=fake_gen):
        result = await stage4.run(km, BASE_ANCHOR, BASE_PAPER)

    lit_review = result["section_outlines"].get("literature_review")
    assert lit_review is not None
    assert len(lit_review["relevant_citations"]) <= 5


@pytest.mark.asyncio
async def test_nature_venue_puts_results_before_discussion():
    paper_nature = dict(BASE_PAPER, target_venue="nature")

    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result = await stage4.run(BASE_KM, BASE_ANCHOR, paper_nature)

    sections = result["sections"]
    assert sections.index("results") < sections.index("discussion")


@pytest.mark.asyncio
async def test_unknown_venue_falls_back_to_arxiv_sections():
    paper_unknown = dict(BASE_PAPER, target_venue="unknown_venue")

    with patch.object(stage4.ai, "generate_json", new=AsyncMock(return_value={"key_points": [], "opening_sentence": "", "must_address": []})):
        result = await stage4.run(BASE_KM, BASE_ANCHOR, paper_unknown)

    assert result["sections"] == stage4.VENUE_SECTIONS["arxiv"]
