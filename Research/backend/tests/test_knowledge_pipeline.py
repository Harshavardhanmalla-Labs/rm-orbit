import pytest
from unittest.mock import AsyncMock, patch

import app.pipeline.stage2_knowledge as stage2


@pytest.mark.asyncio
async def test_defaults_applied_when_llm_returns_empty():
    with patch.object(stage2.ai, "generate_json", new=AsyncMock(return_value={})):
        km = await stage2.run("some text", [])

    assert km["domain"] == "Interdisciplinary Research"
    assert km["claims"] == []
    assert km["results"] == []
    assert km["has_quantitative_data"] is False
    assert km["paper_language"] == "en"


@pytest.mark.asyncio
async def test_existing_citations_merged_into_km():
    citations = [{"title": "A Study", "year": 2022}]
    with patch.object(stage2.ai, "generate_json", new=AsyncMock(return_value={"domain": "CS"})):
        km = await stage2.run("text", citations)

    assert km["existing_citations"] == citations


@pytest.mark.asyncio
async def test_string_claims_normalised_to_dicts():
    raw = {"claims": ["Claim A", "Claim B"], "results": []}
    with patch.object(stage2.ai, "generate_json", new=AsyncMock(return_value=raw)):
        km = await stage2.run("text", [])

    assert all(isinstance(c, dict) for c in km["claims"])
    assert km["claims"][0]["text"] == "Claim A"
    assert km["claims"][0]["claim_type"] == "empirical"


@pytest.mark.asyncio
async def test_string_results_normalised_to_dicts():
    raw = {"claims": [], "results": ["92.3% accuracy"]}
    with patch.object(stage2.ai, "generate_json", new=AsyncMock(return_value=raw)):
        km = await stage2.run("text", [])

    assert isinstance(km["results"][0], dict)
    assert km["results"][0]["value"] == "92.3% accuracy"
    assert km["results"][0]["metric"] == "result"


@pytest.mark.asyncio
async def test_midpoint_sample_appended_for_long_documents():
    long_text = "A" * 30000
    captured = {}

    async def fake_generate(system, user, **kwargs):
        captured["user"] = user
        return {}

    with patch.object(stage2.ai, "generate_json", new=fake_generate):
        await stage2.run(long_text, [])

    assert "[...document continues...]" in captured["user"]


@pytest.mark.asyncio
async def test_short_document_no_midpoint_sample():
    short_text = "B" * 5000
    captured = {}

    async def fake_generate(system, user, **kwargs):
        captured["user"] = user
        return {}

    with patch.object(stage2.ai, "generate_json", new=fake_generate):
        await stage2.run(short_text, [])

    assert "[...document continues...]" not in captured["user"]


@pytest.mark.asyncio
async def test_none_fields_replaced_with_defaults():
    raw = {"domain": None, "claims": None, "results": None, "paper_language": None}
    with patch.object(stage2.ai, "generate_json", new=AsyncMock(return_value=raw)):
        km = await stage2.run("text", [])

    assert km["domain"] == "Interdisciplinary Research"
    assert km["claims"] == []
    assert km["paper_language"] == "en"
