# RM Wallet

RM Wallet is the secure credential vault for RM Orbit. It allows companies to store API keys/passwords and share them with users based on permission and project scope.

## MVP Status
- Backend API baseline implemented (`FastAPI`) with encrypted persistent local state.
- Lightweight web UI baseline added (`Wallet/frontend/index.html`) for create/list/reveal/share flows.
- Secret CRUD with org/user context headers.
- Permissioned sharing (`user` or `role`) with `read`, `use`, `manage` grants.
- Reveal endpoint restricted by owner/admin/share permissions.
- Test suite covers org isolation and sharing behavior.
- Read-only Shared Info registry for `domains`, `cloudflare`, and `misc` operational references.

## API Baseline
- `GET /health`
- `GET /api/wallet/secrets`
- `POST /api/wallet/secrets`
- `GET /api/wallet/secrets/{id}`
- `PATCH /api/wallet/secrets/{id}`
- `DELETE /api/wallet/secrets/{id}`
- `GET /api/wallet/secrets/{id}/shares`
- `POST /api/wallet/secrets/{id}/shares`
- `DELETE /api/wallet/secrets/{id}/shares/{share_id}`
- `GET /api/wallet/secrets/{id}/reveal`
- `GET /api/wallet/audit`
- `GET /api/wallet/shared-info` (read-only catalog)

## Required Headers
- `X-Org-Id`
- `X-User-Id`
- `X-User-Role` (`admin`, `manager`, `member`)
- Optional but recommended: `X-Request-Id` for audit trace correlation

## Auth Modes
- `WALLET_AUTH_MODE=headers`: require `X-Org-Id`/`X-User-Id`/`X-User-Role`.
- `WALLET_AUTH_MODE=gate`: require `Authorization: Bearer ...`; actor resolved from Gate `userinfo`.
- `WALLET_AUTH_MODE=hybrid` (default): prefer Bearer token, fallback to headers.

Gate userinfo config:
- `WALLET_GATE_USERINFO_URL` (default: `http://localhost:45001/api/v1/oidc/userinfo`)
- `WALLET_GATE_TIMEOUT_SECONDS` (default: `3.0`)

Encrypted persistence config:
- `WALLET_MASTER_KEY` (recommended; if missing, dev fallback key is derived)
- `WALLET_STATE_FILE` (default: `Wallet/backend/app/wallet_state.json`)
- `WALLET_PERSISTENCE_ENABLED` (`true` by default)

Shared info catalog config:
- `WALLET_SHARED_INFO_FILE` (default: `Wallet/backend/app/wallet_shared_info.json`)
- Supports JSON array or `{ "items": [...] }` payload.
- Each record can be global (`org_id: "*"`) or org-specific (`org_id: "org-123"`).
- Endpoint remains listing-only; no create/update/delete API is exposed.

## Local Run
- `cd Wallet/backend && python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- `PYTHONPATH=. pytest -q`
- `cd .. && ./start-backend.sh` (port `6110`)
- `./start-frontend.sh` (port `45019`)

## Security Note
Current implementation encrypts secret values before persistence, supports Gate-backed token actor resolution, and records audit envelopes (`request_id`, `org_id`, `secret_id`) for secret actions. For full enterprise rollout, migrate to KMS/HSM envelope keys and database-backed immutable audit trails.
