# ADR-001: Tenant/Org/Workspace Request Context Contract

Status: Accepted (Phase 0)
Date: 2026-03-01

## Context

RM Orbit is moving from app-level isolation to ecosystem-wide multi-enterprise isolation.
Current implementations already pass `org_id` in JWTs and `X-Org-Id` in headers, but the rules are not yet centralized or enforced consistently across all services.

Without a single contract, services can drift and accidentally allow cross-organization access.

## Decision

All authenticated service requests in RM Orbit must carry a normalized request context:

- `tenant_id` (optional until all products support tenant-level billing/isolation)
- `org_id` (required for all protected APIs)
- `workspace_id` (optional; app-level collaboration scope)

The context is resolved from:

1. JWT claims (`tenant_id`, `org_id`, `workspace_id`)
2. Request headers (`X-Tenant-Id`, `X-Org-Id`, `X-Workspace-Id`)
3. Service-owned user record fallback (only for `org_id` during migration)

Validation rules:

1. If org header enforcement is enabled, `X-Org-Id` is mandatory.
2. If both token and header provide `org_id`, they must match.
3. If both token and header provide `tenant_id`, they must match.
4. If both token and header provide `workspace_id`, they must match.
5. Requests without a resolvable `org_id` are rejected.

## Consequences

Positive:

- Uniform multi-enterprise boundary checks in FastAPI and Express stacks.
- Easier cross-service debugging with a predictable context model.
- Clear migration path from legacy local JWTs to Gate-issued JWTs.

Tradeoffs:

- Services with legacy clients may need a temporary compatibility mode.
- Frontends must consistently send `X-Org-Id` once strict mode is enabled.

## Rollout

Phase 0 pilots:

- FastAPI: `Atlas`
- Express: `Control Center`

Strict org-header mode is controlled per service through `REQUIRE_ORG_HEADER`.

## Contract Reference

Canonical headers:

- `Authorization: Bearer <JWT>`
- `X-Org-Id: <org_id>` (required when strict mode is enabled)
- `X-Tenant-Id: <tenant_id>` (optional)
- `X-Workspace-Id: <workspace_id>` (optional)

Canonical JWT claims:

- `sub` (required)
- `org_id` (required for Gate ecosystem tokens)
- `tenant_id` (recommended)
- `workspace_id` (optional)
- `roles`, `permissions` (optional authz surface)

## Non-Goals (This ADR)

- Does not define DB schema migration for every service.
- Does not replace existing RBAC authorization logic.
- Does not define event versioning policy (covered separately).
