# ADR-003: Event Envelope Versioning and Idempotency

Status: Accepted (Phase 1.5)  
Date: 2026-03-01

## Context

RM Orbit services publish and consume cross-app events through Redis channels.  
`schema_version` normalization was already partially implemented, but idempotency keys were not uniformly present across publisher envelopes.

Without a stable event identity field, consumers cannot reliably deduplicate retries/replays.

## Decision

All ecosystem event publishers must emit a normalized envelope with:

- `timestamp`
- `source`
- `event_type`
- `schema_version`
- `event_id`
- `org_id`
- `data` (when payload body exists)

Rules:

1. `schema_version` defaults to `1` when absent.
2. `event_id` must always be present.
3. If an inbound payload already includes `event_id`, publisher/normalizer must preserve it.
4. If `event_id` is missing, publisher/normalizer must generate one.
5. Events without `org_id` remain invalid for org-scoped broadcast/consumption paths.

## Enforcement

Enforcement is implemented through shared fixture-driven contract tests:

- `docs/contracts/event-envelope-v1.json`
- `contract-gate.sh`

Current services under this enforcement path include:

- Calendar
- Planet
- Mail
- Connect
- Meet
- Snitch prototype publishers
- Writer
- Atlas consumer normalization path

## Consequences

Positive:

- Cross-service consumers receive consistent schema/version metadata.
- Event replay protection and deduplication workflows can key on `event_id`.
- Contract drift is caught in CI via a single gate.

Tradeoffs:

- Legacy publishers without `event_id` must be normalized or updated before promotion.
- Event volume analysis should account for generated IDs in local/dev fallback paths.
