from __future__ import annotations

import json
from pathlib import Path

from app.eventbus import build_writer_event_envelope


def _load_writer_cases() -> list[dict]:
    fixture_path = Path(__file__).resolve().parents[3] / "docs" / "contracts" / "event-envelope-v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    return [entry for entry in fixture.get("publisher_cases", []) if entry.get("service") == "writer"]


def test_writer_event_envelope_matches_shared_publisher_fixture_pack() -> None:
    cases = _load_writer_cases()
    assert len(cases) > 0

    for fixture_case in cases:
        envelope = build_writer_event_envelope(
            fixture_case["channel"],
            fixture_case.get("event") or {},
        )
        expected = fixture_case.get("expected") or {}

        assert envelope["source"] == expected["source"], f"case {fixture_case['id']} source mismatch"
        assert envelope["event_type"] == expected["event_type"], f"case {fixture_case['id']} event_type mismatch"
        assert (
            envelope["schema_version"] == expected["schema_version"]
        ), f"case {fixture_case['id']} schema_version mismatch"
        assert envelope["org_id"] == expected["org_id"], f"case {fixture_case['id']} org_id mismatch"

        if "user_id" in expected:
            assert envelope["user_id"] == expected["user_id"], f"case {fixture_case['id']} user_id mismatch"
        if "event_id" in expected:
            assert envelope["event_id"] == expected["event_id"], f"case {fixture_case['id']} event_id mismatch"

        assert envelope.get("timestamp"), f"case {fixture_case['id']} missing timestamp"
        assert envelope.get("event_id"), f"case {fixture_case['id']} missing event_id"
