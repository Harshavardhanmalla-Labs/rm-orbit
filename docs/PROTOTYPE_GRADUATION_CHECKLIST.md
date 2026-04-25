# Prototype Graduation Checklist

Date: 2026-03-01  
Status: Active baseline for Snitch-to-first-class service graduation

This checklist is the minimum release gate for moving a prototype service into first-class ecosystem status.

## Scope

Applies to services that start in prototype mode (for example under `Snitch/`) and later move to standalone service ownership (`<Service>/`).

## Graduation Gates

### 1) Auth Compliance

- [ ] Service validates Gate-compatible bearer tokens (JWKS or configured public key path).
- [ ] Issuer and audience checks are configurable and tested.
- [ ] Local fallback mode (if any) is explicit, env-gated, and disabled for production profiles.
- [ ] Protected APIs reject missing/invalid credentials with consistent 401/403 behavior.

Evidence:
- Service README auth env section
- Auth middleware/unit tests
- Runtime smoke check with auth-required mode

### 2) Tenant Isolation Tests

- [ ] Service resolves org context from token/header contract.
- [ ] Header/token mismatch is rejected.
- [ ] Cross-org data access is blocked in API tests.
- [ ] Tenant/org context is preserved in background consumers/jobs where relevant.

Evidence:
- Tenant context middleware and tests
- Negative isolation tests in CI

### 3) Event Contract Compliance

- [ ] Publisher envelope includes `event_type`, `schema_version`, `org_id`, and normalized `data`.
- [ ] Missing `schema_version` defaults to `1` (unless explicitly overridden).
- [ ] Service has fixture-driven contract tests using `docs/contracts/event-envelope-v1.json`.
- [ ] Service is included in `./contract-gate.sh`.

Evidence:
- Event envelope builder
- Contract tests against shared fixture pack
- Passing `contract-gate.sh`

### 4) Observability and Runbooks

- [ ] `/health` (or equivalent) endpoint exists and is documented.
- [ ] Startup/shutdown commands and port mapping are documented in service README and `PORTS.md`.
- [ ] Common failure modes and recovery steps are documented.
- [ ] Logs are structured enough for correlation by org/request where applicable.

Evidence:
- Service README runbook section
- Root runtime matrix gate passes

## Promotion Decision

A prototype can be promoted only when all four gate groups above are complete.

Recommended approval record:
- Update `ECOSYSTEM_TODO_PLAN.md` with the promotion note.
- Update `AGENT_HANDOFF_YYYY-MM-DD.md` with validation evidence.
- Include latest pass status for:
  - `./runtime-matrix-gate.sh`
  - `./contract-gate.sh`
