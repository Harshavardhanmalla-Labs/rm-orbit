# ADR-005: Writer Feedback Persistence Model

Status: Accepted (Foundation baseline)  
Date: 2026-04-22

## Context

Writer added in-product feedback capture (`rating`, `area`, `page`, `message`) for rapid product iteration.
The first implementation emitted audit/event records but lacked durable queryable storage for trend analysis.
We need a persistence model that supports:

- workspace-scoped aggregation
- low-latency dashboard summaries
- auditable, append-only feedback history

## Decision

1. Persist feedback in a dedicated append-only table: `feedback_entries`.
2. Store each submission as a single row with:
   - tenant scope (`workspace_id`, `org_id`)
   - actor trace (`user_id`)
   - product context (`area`, `page`)
   - payload (`rating`, `message`)
   - immutable timestamp (`created_at`)
3. Keep the event/audit path as a parallel side effect (`writer.feedback.submitted`) rather than the source of truth for reads.
4. Optimize read paths with workspace-leading indexes for summary queries:
   - `ix_feedback_entries_workspace_id`
   - `ix_feedback_entries_workspace_created_at`
   - `ix_feedback_entries_workspace_area`
5. Expose aggregated reads through `GET /api/feedback/summary` (windowed by `days`, bounded `recent_limit`) and keep writes through `POST /api/feedback`.

## Consequences

Positive:

- feedback trends become directly queryable without replaying events
- dashboard insight card can load quickly from indexed workspace queries
- weekly feedback triage can be generated from persistent data

Tradeoffs:

- extra schema/migration surface area to maintain
- dual-write behavior (DB + event publish) requires observability for partial failure scenarios
