# Global Search API Contract (v1)

Status: Active baseline  
Date: 2026-03-01

## Purpose

Define a single cross-app search contract that aggregates results from multiple Orbit services with org/workspace-aware filtering.

## Endpoint

`GET /api/search`

## Query Params

- `q` (required, string, min length 2): search query text.
- `limit` (optional, int, default `20`, max `50`): max result count.
- `org_id` (optional, string): explicit org context override.
- `workspace_id` (optional, string): explicit workspace context override.

## Headers

- `X-Org-Id` (optional): org context if query param not provided.
- `X-Workspace-Id` (optional): workspace context if query param not provided.

## Response Shape

```json
{
  "query": "q4",
  "org_id": "org-1",
  "workspace_id": "ws-1",
  "total": 2,
  "took_ms": 18,
  "sources": ["writer", "learn"],
  "results": [
    {
      "id": "doc-123",
      "source": "writer",
      "entity_type": "document",
      "title": "Q4 Planning",
      "snippet": "Draft milestones for Q4...",
      "url": "/document?id=doc-123",
      "score": 17.0,
      "updated_at": "2026-03-01T10:00:00Z",
      "metadata": {
        "workspace_id": "ws-1"
      }
    }
  ]
}
```

## Result Contract

Each result item must include:

- `id` (string)
- `source` (string; e.g. `writer`, `learn`)
- `entity_type` (string)
- `title` (string)
- `snippet` (string, optional but recommended)
- `url` (string, optional)
- `score` (number, descending sort)
- `updated_at` (string, optional ISO timestamp)
- `metadata` (object)

## Ranking Rules (Baseline)

1. Results are sorted by `score` descending.
2. Services may use source-specific scoring internals.
3. Aggregator is responsible for final ordering + limit clipping.

## Error Semantics

- `422`: validation errors (for example missing/short `q`).
- `500`: unexpected adapter failure (should be rare; partial failures should degrade gracefully).

## Current Source Adapters (Baseline)

- `writer`: queries `GET /api/documents` from Writer backend (workspace-scoped).
- `learn`: indexes Learn docs HTML titles/snippets from local `Learn/site`.

## Non-Goals (v1)

- Full-text indexing backend (Elasticsearch/OpenSearch).
- Cross-tenant semantic ranking.
- Permission-aware filtering beyond org/workspace context.
