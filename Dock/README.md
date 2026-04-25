# RM Dock

RM Dock is the enterprise software portal for RM Orbit. It manages software catalog entries, licenses, assignments, and CARF requests (Change App Request Form).

## MVP Status
- Backend API baseline implemented (`FastAPI`, in-memory store).
- Lightweight web UI baseline added (`Dock/frontend/index.html`) for catalog + CARF workflows.
- Company-side controls for app catalog + license purchase + assignment management.
- User-side visibility for advertised apps and apps assigned to the user.
- CARF workflow included (request, review, approve/reject, provisioned).
- CARF approval/provisioning now auto-creates TurboTick follow-up tickets with tracked automation state on requests.
- Tests cover role boundaries, seat enforcement, and org isolation.

## API Baseline
- `GET /health`
- `GET /api/dock/apps`
- `GET /api/dock/apps/advertised`
- `GET /api/dock/apps/assigned`
- `POST /api/dock/apps`
- `PATCH /api/dock/apps/{id}`
- `GET /api/dock/licenses`
- `POST /api/dock/licenses`
- `GET /api/dock/assignments`
- `POST /api/dock/assignments`
- `PATCH /api/dock/assignments/{id}`
- `GET /api/dock/requests`
- `POST /api/dock/requests`
- `PATCH /api/dock/requests/{id}`
- `GET /api/dock/audit/events`
- `GET /api/dock/carf` (alias)
- `POST /api/dock/carf` (alias)

## Required Headers
- `X-Org-Id`
- `X-User-Id`
- `X-User-Role` (`admin`, `manager`, `member`)
- Optional but recommended on mutations: `X-Request-Id`

## Authentication Modes
- `DOCK_AUTH_MODE=headers|gate|hybrid` (default: `hybrid`)
- `headers`: trust `X-Org-Id`, `X-User-Id`, `X-User-Role`
- `gate`: require `Authorization: Bearer <token>` and resolve actor via Gate userinfo
- `hybrid`: prefer Bearer token when provided, otherwise fallback to header mode
- Optional Gate settings:
  - `DOCK_GATE_USERINFO_URL` (default `http://localhost:45001/api/v1/oidc/userinfo`)
  - `DOCK_GATE_TIMEOUT_SECONDS` (default `3.0`)

Audit/event emission settings:
- `DOCK_AUDIT_ENABLED` (`true` by default)
- `DOCK_EVENT_SINK_URL` (optional webhook/event sink endpoint)
- `DOCK_AUDIT_TIMEOUT_SECONDS` (default `3.0`)

## Local Run
- `cd Dock/backend && python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- `PYTHONPATH=. pytest -q`
- `cd .. && ./start-backend.sh` (port `6120`)
- `./start-frontend.sh` (port `45020`)

## Scope Notes
Current implementation is an integration-first MVP. Production rollout should add persistent storage, procurement policy hooks, and audit-event publishing.
