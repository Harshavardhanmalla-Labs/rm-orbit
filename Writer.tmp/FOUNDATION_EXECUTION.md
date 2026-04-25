# Writer Foundation-First Execution (April 22, 2026)

This document locks the four foundations before feature expansion.

## 1) Clear Product Scope

Goal:
- Build an AI-native structured workspace for operators.

In scope now (Phase 1):
- Block-based document editing
- Core block graph APIs
- Version snapshots
- Workspace-scoped access controls
- Structured feedback capture

Out of scope now:
- Full Excel engine parity
- Full PowerPoint renderer parity
- Mobile apps
- Offline-first engine

Definition of Done:
- Every sprint item explicitly tagged `in_scope` or `deferred`
- Any new feature PR references this scope doc

## 2) Strong Architecture

Current baseline:
- FastAPI + SQLAlchemy backend
- Block graph model (documents, blocks, relations, versions)
- Event envelope publishing (`writer.*`)
- Workspace/org-aware request context

Architecture guardrails:
- No duplicate data models for docs/slides/sheets views
- APIs must be workspace-scoped (`X-Workspace-Id`)
- Cross-app events must use shared envelope contracts

Definition of Done:
- Contract tests pass for writer publisher
- API/frontend contracts documented and enforced by tests

## 3) Tight QA/Release Discipline

Mandatory gate before merge/release:
- `Writer/backend`: `pytest -q`
- `Writer/frontend`: `npm run lint`
- `Writer/frontend`: `npm run build`

Single command:
- `Writer/qa-gate.sh`

Definition of Done:
- Gate is green in local and CI runs
- No release if any of the three checks fail

## 4) Fast Iteration with Real User Feedback

Implemented baseline:
- `POST /api/feedback` captures rating + area + page + optional message
- Feedback is audited (`writer.feedback.submitted`) and event-published
- In-app quick feedback widget available in Writer layout

Weekly operating loop:
1. Review top feedback themes (by area and rating)
2. Convert top 3 issues into actionable tickets
3. Ship at least one feedback-driven improvement
4. Report back in release notes with `You asked, we changed`

Operational command:
- `./Writer/weekly-feedback-triage.sh --days 7 --top 3`

Definition of Done:
- Feedback submitted every week by pilot users
- At least one shipped fix per week directly traced to feedback

## 30-Day Priority Plan

Week 1:
- Keep QA gate green continuously
- Stabilize API/UI contracts
- Remove placeholder routes from critical paths

Week 2:
- Scope lock enforcement in planning
- Add release checklist to Writer deployment flow

Week 3:
- Feedback triage dashboard (basic aggregation)
- Start measuring document task completion and failure points

Week 4:
- Deliver first feedback-driven UX cycle
- Publish a short quality report (failures, fixes, lead time)
