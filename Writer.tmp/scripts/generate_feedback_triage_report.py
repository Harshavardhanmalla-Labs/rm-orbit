#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


@dataclass
class AreaSummary:
    area: str
    count: int
    average_rating: float


def default_database_url() -> str:
    writer_root = Path(__file__).resolve().parents[1]
    return f"sqlite:///{writer_root / 'data' / 'writer.db'}"


def resolve_database_url() -> str:
    return os.getenv("WRITER_DATABASE_URL") or default_database_url()


def build_where_clause(workspace_id: str | None) -> tuple[str, dict]:
    clauses = ["created_at >= :since"]
    params: dict[str, object] = {}
    if workspace_id:
        clauses.append("workspace_id = :workspace_id")
        params["workspace_id"] = workspace_id
    return " AND ".join(clauses), params


def clean_message(message: str | None) -> str:
    if not message:
        return ""
    compact = " ".join(message.strip().split())
    return compact[:200] + ("..." if len(compact) > 200 else "")


def build_report(
    generated_at: datetime,
    since: datetime,
    days: int,
    workspace_id: str | None,
    total: int,
    average: float,
    areas: list[AreaSummary],
    area_quotes: dict[str, str],
) -> str:
    workspace_label = workspace_id or "all workspaces"
    lines: list[str] = []
    lines.append("# Writer Weekly Feedback Triage Report")
    lines.append("")
    lines.append(f"- Generated at (UTC): {generated_at.isoformat()}")
    lines.append(f"- Time window: last {days} days (since {since.date().isoformat()})")
    lines.append(f"- Workspace scope: {workspace_label}")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append(f"- Total feedback responses: {total}")
    lines.append(f"- Average rating: {average:.2f}/5")
    lines.append("")
    lines.append("## Top Pain Points")
    lines.append("")

    if not areas:
        lines.append("No feedback entries found in this window.")
    else:
        for index, area in enumerate(areas, start=1):
            lines.append(
                f"{index}. `{area.area}` - {area.count} responses, average {area.average_rating:.2f}/5"
            )
            quote = area_quotes.get(area.area, "")
            if quote:
                lines.append(f"   Evidence quote: \"{quote}\"")
            else:
                lines.append("   Evidence quote: No free-text comment captured for this area.")
            lines.append(
                f"   Suggested ticket: `Writer feedback: improve {area.area} experience (weekly triage)`"
            )
            lines.append("")

    lines.append("## This Week Commitments")
    lines.append("")
    lines.append("- Convert each pain point into one actionable ticket with owner and target date.")
    lines.append("- Prioritize one ticket for shipping this week (`You asked, we changed`).")
    lines.append("- Review impact in next weekly triage and carry over unresolved items.")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Writer weekly feedback triage report.")
    parser.add_argument("--days", type=int, default=7, help="Lookback window in days (default: 7).")
    parser.add_argument("--top", type=int, default=3, help="Number of top pain points (default: 3).")
    parser.add_argument(
        "--workspace-id",
        default=os.getenv("WRITER_WORKSPACE_ID", "").strip() or None,
        help="Optional workspace scope. Defaults to WRITER_WORKSPACE_ID if set.",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Optional output path. Defaults to Writer/reports/feedback-triage-<date>.md",
    )
    args = parser.parse_args()

    if args.days < 1:
        raise SystemExit("--days must be >= 1")
    if args.top < 1:
        raise SystemExit("--top must be >= 1")

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    where_clause, where_params = build_where_clause(args.workspace_id)
    params = {"since": since, **where_params}

    db_url = resolve_database_url()
    engine = create_engine(db_url, future=True)

    totals_sql = text(
        f"""
        SELECT COUNT(*) AS total_count, AVG(rating) AS average_rating
        FROM feedback_entries
        WHERE {where_clause}
        """
    )
    areas_sql = text(
        f"""
        SELECT area, COUNT(*) AS item_count, AVG(rating) AS average_rating
        FROM feedback_entries
        WHERE {where_clause}
        GROUP BY area
        ORDER BY item_count DESC, average_rating ASC, area ASC
        """
    )
    quotes_sql = text(
        f"""
        SELECT area, message, rating, created_at
        FROM feedback_entries
        WHERE {where_clause}
          AND message IS NOT NULL
          AND TRIM(message) != ''
        ORDER BY rating ASC, created_at DESC
        """
    )

    try:
        with engine.connect() as conn:
            totals_row = conn.execute(totals_sql, params).one()
            areas_rows = conn.execute(areas_sql, params).all()
            quote_rows = conn.execute(quotes_sql, params).all()
    except SQLAlchemyError as exc:
        raise SystemExit(
            "Failed to read feedback data. "
            "Ensure migrations are applied and WRITER_DATABASE_URL points to Writer DB.\n"
            f"Details: {exc}"
        ) from exc

    total = int(totals_row._mapping["total_count"] or 0)
    average = float(totals_row._mapping["average_rating"] or 0.0)

    areas = [
        AreaSummary(
            area=str(row._mapping["area"]),
            count=int(row._mapping["item_count"] or 0),
            average_rating=float(row._mapping["average_rating"] or 0.0),
        )
        for row in areas_rows
    ][: args.top]

    area_quotes: dict[str, str] = {}
    for row in quote_rows:
        area = str(row._mapping["area"])
        if area in area_quotes:
            continue
        area_quotes[area] = clean_message(str(row._mapping["message"]))

    report = build_report(
        generated_at=now,
        since=since,
        days=args.days,
        workspace_id=args.workspace_id,
        total=total,
        average=average,
        areas=areas,
        area_quotes=area_quotes,
    )

    writer_root = Path(__file__).resolve().parents[1]
    default_output = writer_root / "reports" / f"feedback-triage-{now.date().isoformat()}.md"
    output_path = Path(args.out) if args.out else default_output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Report generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
