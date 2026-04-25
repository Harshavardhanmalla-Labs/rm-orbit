"""Tests for Stage 6 quality passes and Stage 7 confidence report."""
import pytest
from app.pipeline import stage6_quality, stage7_citations


# --------------- pass1_structural ---------------

@pytest.mark.asyncio
async def test_pass1_structural_missing_section():
    sections = {
        "abstract": "A " * 200,
        "introduction": "B " * 400,
        # methodology missing
        "results": "D " * 250,
        "discussion": "E " * 350,
        "conclusion": "F " * 200,
    }
    _, issues = await stage6_quality.pass1_structural(sections)
    assert any("methodology" in i for i in issues)


@pytest.mark.asyncio
async def test_pass1_structural_section_too_short():
    sections = {
        "abstract": "short",
        "introduction": "B " * 400,
        "methodology": "C " * 300,
        "results": "D " * 250,
        "discussion": "E " * 350,
        "conclusion": "F " * 200,
    }
    _, issues = await stage6_quality.pass1_structural(sections)
    assert any("abstract" in i.lower() and "short" in i.lower() for i in issues)


@pytest.mark.asyncio
async def test_pass1_structural_all_present_and_long_enough():
    sections = {
        "abstract": "Word " * 160,
        "introduction": "Word " * 360,
        "methodology": "Word " * 260,
        "results": "Word " * 210,
        "discussion": "Word " * 310,
        "conclusion": "Word " * 160,
    }
    _, issues = await stage6_quality.pass1_structural(sections)
    assert issues == []


# --------------- pass3_academic_register (banned phrases) ---------------

@pytest.mark.asyncio
async def test_pass3_replaces_banned_phrases_silently(monkeypatch):
    from app.services import languagetool_client as lt

    async def _no_issues(text):
        return []
    monkeypatch.setattr(lt, "get_issues", _no_issues)

    sections = {
        "introduction": "We leverage deep learning to build a cutting-edge solution.",
        "conclusion": "This innovative solution demonstrates synergy.",
    }
    fixed_sections, issues = await stage6_quality.pass3_academic_register(sections)

    # Banned phrases should be replaced, not reported as issues
    assert "leverage" not in fixed_sections["introduction"].lower()
    assert "cutting-edge" not in fixed_sections["introduction"].lower()
    assert not any("leverage" in i.lower() for i in issues)
    assert not any("cutting-edge" in i.lower() for i in issues)


# --------------- confidence report ---------------

def test_build_confidence_report_coverage_score():
    sections = {
        "abstract": "A " * 200,
        "introduction": "B " * 400,
        "methodology": "C " * 300,
        "results": "D " * 250,
        "discussion": "E " * 350,
        "conclusion": "F " * 200,
    }
    knowledge_map = {
        "claims": [{"text": f"claim {i}"} for i in range(10)],
        "results": [{"metric": "F1", "value": "0.92", "description": "test", "is_primary": True}] * 5,
        "methodology_steps": ["step1", "step2", "step3", "step4"],
        "key_terms": ["NLP", "transformer", "attention", "BERT", "GPT", "fine-tuning", "tokenization",
                      "embedding", "classification", "sequence"],
        "datasets": ["SQuAD"],
        "evaluation_metrics": ["F1"],
        "author_frameworks": ["CustomBERT"],
    }
    citations = [
        {"title": f"Paper {i}", "doi": f"10.1/{i}", "verified": True, "authors": ["Author A"], "year": "2023"}
        for i in range(10)
    ]
    quality_result = {"issues": [], "passes_run": 5}

    report = stage7_citations.build_confidence_report(sections, knowledge_map, citations, quality_result)

    assert report["source_coverage_pct"] > 60
    assert report["total_citations"] == 10
    assert report["verified_citations"] == 10
    assert report["section_completeness"] == "6/6"
    assert report["total_word_count"] > 0
    assert isinstance(report["flags"], list)


def test_build_confidence_report_low_citations_flag():
    sections = {"abstract": "A " * 200, "introduction": "B " * 400,
                "methodology": "C " * 300, "results": "D " * 250,
                "discussion": "E " * 350, "conclusion": "F " * 200}
    knowledge_map = {"claims": [], "results": [], "methodology_steps": [],
                     "key_terms": [], "datasets": [], "evaluation_metrics": [], "author_frameworks": []}
    quality_result = {"issues": []}

    report = stage7_citations.build_confidence_report(sections, knowledge_map, [], quality_result)

    assert any("citation" in f["message"].lower() for f in report["flags"])


def test_build_confidence_report_unverified_flag():
    sections = {"abstract": "A " * 200, "introduction": "B " * 400,
                "methodology": "C " * 300, "results": "D " * 250,
                "discussion": "E " * 350, "conclusion": "F " * 200}
    knowledge_map = {"claims": [], "results": [], "methodology_steps": [],
                     "key_terms": [], "datasets": [], "evaluation_metrics": [], "author_frameworks": []}
    quality_result = {"issues": []}
    citations = [{"title": f"P {i}", "verified": False, "authors": ["A"], "year": "2023"} for i in range(10)]

    report = stage7_citations.build_confidence_report(sections, knowledge_map, citations, quality_result)

    assert any("unverified" in f["message"].lower() or "verified" in f["message"].lower() for f in report["flags"])
