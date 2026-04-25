# Orbit Search (Aggregator)

Orbit Search is the minimal cross-app search aggregator baseline for RM Orbit.

Current scope:
- Contract-first global search endpoint (`/api/search`)
- Source adapters for:
  - Writer documents (via Writer backend API)
  - Learn docs pages (from local `Learn/site` HTML)

## Run locally

```bash
cd Search
./start.sh
```

Default URL:
- `http://localhost:6200`

## Endpoints

- `GET /health`
- `GET /api/search/sources`
- `GET /api/search?q=...&limit=...`

Context headers:
- `X-Org-Id` (optional)
- `X-Workspace-Id` (optional, required for Writer-source search results)

## Contract

See:
- `docs/contracts/global-search-v1.md`

## Test

```bash
cd Search/backend
pytest -q
```
