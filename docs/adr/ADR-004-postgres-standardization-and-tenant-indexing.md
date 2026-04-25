# ADR-004: Postgres Standardization and Tenant-Aware Indexing

Status: Accepted (Phase 2 baseline)  
Date: 2026-03-02

## Context

RM Orbit services use mixed local database patterns (SQLite and Postgres) and inconsistent migration discipline.
To scale multi-tenant workloads safely, we need:

- migration-first schema management
- a primary relational engine standard
- explicit tenant/workspace-aware index patterns

## Decision

1. PostgreSQL is the standard relational engine for deployed RM Orbit services.
2. Schema changes must be migration-driven (Alembic for Python services).
3. Writer backend now ships a Postgres-ready migration baseline (`Writer/backend/alembic.ini`, `Writer/backend/app/alembic/versions/0001_initial.py`).
4. Tenant/workspace-aware indexes are mandatory for high-cardinality tables:
   - workspace/org identifier as leading index key
   - common access-path timestamp as secondary key where applicable
5. Service startup in deployed profiles should avoid `create_all` schema creation and rely on migrations (`WRITER_DB_INIT_MODE=skip` with `alembic upgrade head`).

## Initial Rollout

- Root compose now provisions `orbit-postgres` (port `55432`) and runs Writer on Postgres.
- Writer startup supports migration-on-start for consistency (`WRITER_MIGRATE_ON_START`, default `1`).
- Writer schema includes tenant-aware index coverage for document/block access patterns.

## Consequences

Positive:

- deterministic schema evolution across environments
- reduced drift between local/dev/compose/prod
- better query selectivity for workspace-scoped operations

Tradeoffs:

- local contributors need Postgres dependencies for full parity workflows
- migration review becomes a required step for schema changes
