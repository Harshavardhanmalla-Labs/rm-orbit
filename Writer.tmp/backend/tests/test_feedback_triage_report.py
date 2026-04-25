from __future__ import annotations

import os
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def test_weekly_feedback_triage_report_generation(tmp_path: Path) -> None:
    db_path = tmp_path / "writer-feedback.db"
    out_path = tmp_path / "feedback-report.md"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE feedback_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id TEXT NOT NULL,
                org_id TEXT,
                user_id TEXT,
                rating INTEGER NOT NULL,
                area TEXT NOT NULL,
                page TEXT,
                message TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT INTO feedback_entries
                (workspace_id, org_id, user_id, rating, area, page, message, created_at)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ws-test",
                "org-test",
                "user-test",
                2,
                "editor",
                "/document",
                "Saving draft sometimes feels slow on larger notes.",
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()

    script_path = Path(__file__).resolve().parents[2] / "weekly-feedback-triage.sh"
    env = {**os.environ, "WRITER_DATABASE_URL": f"sqlite:///{db_path}"}
    result = subprocess.run(
        [
            str(script_path),
            "--days",
            "7",
            "--top",
            "3",
            "--workspace-id",
            "ws-test",
            "--out",
            str(out_path),
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")
    assert "Top Pain Points" in content
    assert "`editor` - 1 responses, average 2.00/5" in content
