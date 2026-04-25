# RM Orbit Postgres Tenant Indexing + Partitioning Strategy (v1)

Date: 2026-03-02  
Scope: Writer baseline + pattern for other services

## 1) Indexing Rules

For multi-tenant tables, use this order:

1. tenant scope key (`tenant_id`, `org_id`, or `workspace_id`)
2. access-path key (`updated_at`, `created_at`, status, etc.)
3. entity key (`id`) only when needed by query plans

Writer baseline now follows:

- `documents(workspace_id)`
- `documents(workspace_id, updated_at)`
- `blocks(document_id, parent_block_id, position_index)`
- `block_versions(block_id, created_at)`
- `block_relations(document_id, relation_type)`

## 2) Migration Rules

- Use Alembic revisions only; do not rely on runtime `create_all` for deployed profiles.
- For schema updates:
  - add migration
  - verify upgrade on empty DB and existing DB
  - include downgrade when feasible

## 3) Partitioning Thresholds

Apply partitioning only after observed scale thresholds:

- `documents` > 50M rows
- `blocks` > 250M rows
- sustained write pressure > 3k inserts/sec on a single table

Before threshold, prefer:

- composite indexes
- vacuum/analyze tuning
- query plan optimization

## 4) Partitioning Approach (when threshold is reached)

Recommended default: hash partition by `workspace_id` to preserve tenant distribution.

Example (reference only):

```sql
ALTER TABLE documents PARTITION BY HASH (workspace_id);
CREATE TABLE documents_p0 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE documents_p1 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 1);
```

Use `8` partitions as a starting point; tune based on production metrics.

## 5) Operational Checks

- monitor index hit ratio per tenant-heavy table
- track bloat and autovacuum lag
- inspect query plans for `workspace_id` predicates
- keep migration runtime under deployment SLO
