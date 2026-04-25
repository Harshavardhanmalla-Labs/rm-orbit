# Writer Foundation Backlog

Execution board for the four foundations from `FOUNDATION_EXECUTION.md`.

## Scope Lock

- [x] `WFR-001` Lock in-scope vs deferred list for Phase 1
  - Owner: Product
  - Evidence: `FOUNDATION_EXECUTION.md`
- [x] `WFR-002` Add PR template checkbox: in-scope/deferred classification
  - Owner: Engineering
  - Evidence: `.github/pull_request_template.md`
- [x] `WFR-003` Add weekly scope-drift review in sprint ritual
  - Owner: Product
  - Evidence: `Writer/SCOPE_DRIFT_REVIEW.md`

## Architecture Discipline

- [x] `WFR-010` Stabilize API/frontend contract for document title + block delete
  - Owner: Backend + Frontend
  - Evidence: `PATCH /api/documents/{id}`, `DELETE /api/blocks/{id}`
- [x] `WFR-011` Fix SPA catch-all route shadowing API responses
  - Owner: Backend
  - Evidence: SPA handler moved after API registration
- [x] `WFR-012` Add architecture decision update for feedback persistence model
  - Owner: Backend
  - Evidence: `docs/adr/ADR-005-writer-feedback-persistence-model.md`

## QA & Release Gates

- [x] `WFR-020` Add one-command Writer quality gate script
  - Owner: Engineering
  - Evidence: `Writer/qa-gate.sh`
- [x] `WFR-021` Get Writer gate green (tests + lint + build)
  - Owner: Engineering
  - Evidence: local run passed on 2026-04-22
- [x] `WFR-022` Add GitHub Actions workflow for Writer QA gate
  - Owner: Engineering
  - Evidence: `.github/workflows/writer-qa.yml`
- [x] `WFR-023` Fail release if Writer QA workflow is red
  - Owner: Release
  - Evidence: `.github/workflows/writer-release-gate.yml`

## Feedback Loop

- [x] `WFR-030` Add feedback submission API
  - Owner: Backend
  - Evidence: `POST /api/feedback`
- [x] `WFR-031` Persist feedback in DB + migration
  - Owner: Backend
  - Evidence: `feedback_entries` model + `0002_feedback_entries.py`
- [x] `WFR-032` Add feedback summary API
  - Owner: Backend
  - Evidence: `GET /api/feedback/summary`
- [x] `WFR-033` Add dashboard feedback insights card
  - Owner: Frontend
  - Evidence: `Dashboard.tsx`
- [x] `WFR-034` Weekly feedback triage report (top 3 pain points)
  - Owner: Product + Eng
  - Evidence: `Writer/weekly-feedback-triage.sh`, `Writer/scripts/generate_feedback_triage_report.py`
