# ADR-002: Service-to-Service Token Validation Standard

Status: Accepted (Phase 0)
Date: 2026-03-01

## Context

RM Orbit services currently validate Gate tokens, but issuer and audience rules were not enforced uniformly.
This creates drift risk for backend-to-backend and machine-to-machine API calls.

Gate already exposes OIDC discovery and JWKS, so services can validate RS256 signatures without private key sharing.

## Decision

All internal service APIs that accept Gate JWTs will use a common validation contract:

1. Verify RS256 signature using Gate public material.
2. Prefer JWKS (`GATE_JWKS_URL`) when configured.
3. Allow local PEM fallback (`GATE_PUBLIC_KEY_PATH`) for offline/local workflows.
4. Enforce issuer match when `GATE_EXPECTED_ISSUER` is set.
5. Enforce audience match when `GATE_EXPECTED_AUDIENCE` is set.
6. Transitional compatibility: if `aud` is missing, `client_id` may satisfy audience when `ALLOW_CLIENT_ID_AUDIENCE_FALLBACK=true`.
7. Local HS256 compatibility remains opt-in and controlled by `ALLOW_LOCAL_HS256_FALLBACK`.

## Canonical Environment Variables

- `GATE_JWKS_URL` (optional, recommended in deployed environments)
- `GATE_PUBLIC_KEY_PATH` (local/offline fallback)
- `GATE_EXPECTED_ISSUER` (recommended, service-specific)
- `GATE_EXPECTED_AUDIENCE` (recommended, service-specific)
- `ALLOW_CLIENT_ID_AUDIENCE_FALLBACK` (default `true` during migration)
- `ALLOW_LOCAL_HS256_FALLBACK` (default `true` in local dev, disable in hardened environments)

## Consequences

Positive:

- Consistent trust boundary checks across Node and Python services.
- Safer service-to-service token acceptance with explicit audience targeting.
- Compatibility with both hosted JWKS and local offline development.

Tradeoffs:

- Services must define expected audience values per environment.
- Legacy tokens without `aud` require temporary fallback (`client_id`) during migration.

## Rollout

- Node services (Connect, Meet, Calendar, Snitch) now share a common Gate token verifier utility.
- Python services (Planet, Mail, Atlas) now enforce issuer/audience checks on validated tokens.
- Tenant/event contract CI remains intact; claim checks activate when env vars are configured.
