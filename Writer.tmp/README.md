# RM Writer

RM Writer is the structured, AI-native writing workspace for the RM Orbit ecosystem.

Current state:
- Frontend prototype UI is runnable.
- Backend baseline is now runnable (`FastAPI + SQLAlchemy`) with workspace-scoped document/block graph APIs.
- Dashboard and Document View now use live backend APIs for document listing/creation, block editing, new block creation, and version history snapshots.
- Optional Gate-compatible JWT enforcement is now available for backend APIs.
- Writer backend now publishes normalized Redis events for core mutations (`writer.document.created`, `writer.block.created/updated`, `writer.relation.created`) when `org_id` context is available.
- Shared Orbit Bar (`orbit-ui`) is now mounted in Writer UI (`app launcher`, `org switcher`, `identity menu`) and synced via `../scripts/sync-orbit-ui-assets.sh`.

## Run locally

```bash
cd Writer
./start.sh
```

Default URLs:
- Frontend: `http://localhost:45010`
- Backend: `http://localhost:6011`

Optional env overrides:
- `WRITER_PORT` (default `45010`)
- `WRITER_HOST` (default `0.0.0.0`)
- `WRITER_START_BACKEND` (default `1`)
- `WRITER_BACKEND_PORT` (default `6011`)
- `WRITER_BACKEND_HOST` (default `0.0.0.0`)
- `WRITER_DATABASE_URL` (default `sqlite:///Writer/data/writer.db`)
- `WRITER_MIGRATE_ON_START` (default `1`, runs `alembic upgrade head` in `start-backend.sh`)
- `WRITER_DB_INIT_MODE` (`create_all` or `skip`; defaults to `create_all` for sqlite and `skip` for postgres)
- `WRITER_AUTH_REQUIRED` (default `0`, require `Authorization: Bearer <token>` for `/api/*`)
- `GATE_JWKS_URL` (optional, RS256 key discovery endpoint)
- `GATE_PUBLIC_KEY_PATH` (default `Gate/authx/certs/public.pem`)
- `GATE_EXPECTED_ISSUER` (optional issuer validation)
- `GATE_EXPECTED_AUDIENCE` (optional audience/client_id validation)
- `ALLOW_LOCAL_HS256_FALLBACK` (default `1`, local HS256 fallback)
- `JWT_SECRET` / `WRITER_JWT_SECRET` (HS256 fallback secret)
- `WRITER_REQUIRE_ORG_HEADER` (default `0`, enforce `X-Org-Id` when auth is present)
- `WRITER_REQUIRE_WORKSPACE_CLAIM_MATCH` (default `0`, enforce token/header workspace match)

Run backend only:

```bash
cd Writer
./start-backend.sh
```

Run DB migrations explicitly:

```bash
cd Writer/backend
./migrate.sh
```

## Backend API baseline

Core endpoints:
- `GET /health`
- `GET /api/render-modes`
- `POST /api/documents`
- `GET /api/documents`
- `GET /api/documents/{document_id}`
- `PATCH /api/documents/{document_id}`
- `GET /api/documents/{document_id}/blocks`
- `POST /api/documents/{document_id}/blocks`
- `PATCH /api/blocks/{block_id}`
- `DELETE /api/blocks/{block_id}`
- `GET /api/blocks/{block_id}/versions`
- `POST /api/blocks/{block_id}/relations`
- `GET /api/documents/{document_id}/graph`
- `POST /api/feedback`
- `GET /api/feedback/summary`

Auth behavior:
- `/health` is always open.
- `/api/*` endpoints accept optional bearer tokens by default.
- If `WRITER_AUTH_REQUIRED=1`, `/api/*` requires a valid bearer token.
- Workspace-scoped endpoints require `X-Workspace-Id`.
- Writer frontend automatically sends `auth_token` from `localStorage` (if present) as a bearer token.

Event behavior:
- Mutation endpoints publish envelopes to Redis channels using the shared contract format (`schema_version`, `event_type`, `org_id`, `user_id`, `data`).
- Publisher sends to both the typed channel (for example `writer.block.updated`) and `writer.activity`.
- Publishing is non-blocking and safely no-ops when Redis is unavailable.

Test backend:

```bash
cd Writer/backend
pytest -q
```

## Postgres baseline

Writer now includes migration-first Postgres support:
- Alembic config: `Writer/backend/alembic.ini`
- Migration env: `Writer/backend/app/alembic/env.py`
- Initial schema revision: `Writer/backend/app/alembic/versions/0001_initial.py`

Root compose (`docker-compose.orbit.yml`) now runs Writer against `orbit-postgres` (`55432 -> 5432`).

## Pre-flight checks

From workspace root:
- `./runtime-matrix-gate.sh`
- `./contract-gate.sh`

From `Writer/`:
- `./qa-gate.sh`

CI release block:
- `.github/workflows/writer-qa.yml` must be green
- `.github/workflows/writer-release-gate.yml` fails on the default release branch whenever Writer QA is non-success

Weekly operating commands:
- `./weekly-feedback-triage.sh --days 7 --top 3`

## UI source

The provided design prototype is preserved in:
- `Writer/code 3.html`

Runnable static page:
- `Writer/site/index.html`

To refresh the runnable page from the design reference:

```bash
cd Writer
./build-site.sh
```

`build-site.sh` also syncs shared `orbit-ui` assets/fonts into `Writer/site/assets` and `Writer/site/fonts`.

## Backend source

- `Writer/backend/app/main.py`
- `Writer/backend/app/models.py`
- `Writer/backend/app/schemas.py`
- `Writer/backend/tests/test_api.py`
- `Writer/start-backend.sh`

## Product architecture reference

See `Writer/readme.txt` for the full product and system design reference, including:
- block-graph data model
- rendering mode strategy
- AI action model
- enterprise security requirements
- 90-day MVP scope

Foundation-first execution operating model:
- `Writer/FOUNDATION_EXECUTION.md`
- `Writer/FOUNDATION_BACKLOG.md`
- `Writer/SCOPE_DRIFT_REVIEW.md`
- `docs/adr/ADR-005-writer-feedback-persistence-model.md`
