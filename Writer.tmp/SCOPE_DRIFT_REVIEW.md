# Writer Weekly Scope-Drift Review

This ritual keeps the active Writer phase focused on `in_scope` outcomes and prevents silent roadmap creep.

## Cadence

- Frequency: Weekly (30 minutes)
- Suggested day: Tuesday
- Required attendees: Product owner, engineering lead, design lead
- Source of truth: `Writer/FOUNDATION_EXECUTION.md`

## Inputs

- PRs merged since last review (`Writer/**`)
- Open PRs labeled for current sprint
- New requests from feedback triage (`Writer/weekly-feedback-triage.sh` output)
- Backlog exceptions proposed as `deferred -> in_scope` or `in_scope -> deferred`

## Agenda

1. Confirm current phase scope still matches `FOUNDATION_EXECUTION.md`.
2. Review each merged/open PR and verify `in_scope` or `deferred` classification.
3. List any drift candidates:
   - Unplanned work merged without explicit scope tag
   - Items added without impact estimate
   - Deferred work silently started
4. Decide one action per drift candidate:
   - Keep in current scope
   - Move to deferred queue
   - Split into a smaller in-scope increment
5. Record owner and due date for each action.

## Decision Log Template

Use this table in sprint notes each week.

| Date (UTC) | Candidate | Decision | Owner | Due Date | Notes |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | Example: full XLSX formula parity | Deferred | Product | YYYY-MM-DD | Keep Phase 1 focused on block editor quality |

## Exit Criteria

- Every open Writer PR has an explicit scope classification.
- Any accepted scope expansion has a written tradeoff and owner.
- `Writer/FOUNDATION_BACKLOG.md` is updated when a foundational item changes status.
