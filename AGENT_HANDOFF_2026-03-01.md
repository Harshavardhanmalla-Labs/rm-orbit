# RM Orbit Agent Handoff Report

Date: 2026-03-02
Generated from workspace: `/home/sasi/Desktop/dev/RM Orbit`
Purpose: Provide a single, operational handoff so a new AI agent can resume delivery immediately.

## Latest Delta (2026-03-02, Workspace Git Hygiene)

- Added root workspace `.gitignore` to ensure `node_modules` directories are ignored across all apps:
  - `/.gitignore` with:
    - `node_modules/`
    - `**/node_modules/`
- Updated `RM Fonts` ignore coverage:
  - `RM Fonts/RM Fonts/.gitignore` now includes `node_modules/` patterns.
- Re-verified discovered app-level `.gitignore` files and confirmed `node_modules` ignore coverage is now present across active app repos.

## Latest Delta (2026-03-02, Meet + Mail Runtime Realism Hardening)

- Meet pre-join experience now uses live device plumbing (no static preview placeholders):
  - `Meet/src/views/PreJoinLobby.jsx`
  - real `getUserMedia` preview, live mic/camera toggles, and enumerated input device selectors
  - pre-join preferences persisted in session storage:
    - mic enabled state
    - camera enabled state
    - selected audio input device
    - selected video input device
- Meet active session startup now respects pre-join saved preferences:
  - `Meet/src/views/ActiveMeeting.jsx`
  - mesh and SFU join flows both apply preferred mic/camera states at initialization
  - mesh flow also applies preferred device IDs where available
- Mail stitch runtime now supports keyboard hotkeys directly inside iframe pages:
  - `Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
  - added route shortcuts (`I/S/D/T/C` + `/`) with typing-context protection
- Validation:
  - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` (PASS)
  - `cd Mail/frontend && npm run build` (PASS)
  - `cd Meet && npm run build` (PASS)

## Latest Delta (2026-03-02, Cross-App UI/UX Modernization Baseline)

- Completed the remaining cross-app modernization sprint checklist item for:
  - Mail
  - Atlas
  - Connect
  - Meet
- Mail frontend updates:
  - global keyboard route shortcuts wired for real navigation (`I/S/D/T/C` + `/`)
  - skip-link + focusable main content shell added for stitched runtime pages
  - document title now updates per route/mailbox context
- Atlas frontend updates:
  - layout now includes skip-link and focusable main content target
  - command palette now consistently opens with `/` and `Cmd/Ctrl+K` (typing-context safe)
  - escape key now closes overlay menus
  - Orbit bar app-switcher links refreshed to ecosystem-correct endpoints (`chat.freedomlabs.in` included)
- Connect frontend updates:
  - global `/` shortcut now opens command palette when not typing
  - skip-link + focusable main landmark added
- Meet frontend updates:
  - lobby runtime indicators now live (network online/offline + current clock)
  - static placeholder avatar replaced with user-derived identity badge
  - Enter-to-join added for meeting code input
  - footer year now dynamic
  - navigation quick-jumps added (`Alt+1..8`)
  - skip-link + route-aware title updates added
- Validation:
  - frontend builds pass in Atlas, Connect, Meet, and Mail after modernization changes

## Latest Delta (2026-03-02, Control Center Orbit Pulse Baseline)

- Implemented executive analytics hub baseline in Control Center:
  - new service `Control Center/server/src/services/pulseService.ts`
  - new API route `GET /api/ops/pulse` (tenant-context aware, role gated to `admin`/`organizer`)
- Pulse API now returns:
  - tenant executive KPIs (meetings, completion, actions, engagement, flow runs/success, service health score)
  - 14-day trend series for meetings and automation flow runs/failures
  - risk radar with severity-tagged operational alerts
- Backend wiring changes:
  - `Control Center/server/src/controllers/opsController.ts` (new `getOperationsPulse`)
  - `Control Center/server/src/routes/opsRoutes.ts` (new `/pulse` route)
- Frontend wiring changes:
  - `Control Center/src/pages/Pulse.tsx` new live page
  - `Control Center/src/App.tsx` view routing update
  - `Control Center/src/components/layout/Sidebar.tsx` new `Pulse` nav item
  - `Control Center/src/types/index.ts` new `PulseOverview` contract type
- Test + validation:
  - added `Control Center/server/src/tests/pulseService.test.ts`
  - updated `Control Center/server/package.json` tenant test gate
  - `cd Control Center/server && npm run test:tenant` (PASS, `13` tests)
  - frontend + backend builds pass

## Latest Delta (2026-03-02, Control Center Orbit Flow Baseline)

- Implemented org-scoped workflow automation persistence in Control Center:
  - `FlowRule` and `FlowExecution` models added in `Control Center/server/prisma/schema.prisma`
  - Prisma client regenerated and DB synced (`npx prisma generate`, `npx prisma db push`)
- Implemented backend flow orchestration module:
  - service: `Control Center/server/src/services/flowService.ts`
  - controller: `Control Center/server/src/controllers/flowController.ts`
  - routes: `Control Center/server/src/routes/flowRoutes.ts`
  - app mount: `Control Center/server/src/app.ts` (`/api/flows`)
- Flow endpoints now available behind existing auth + tenant context middleware:
  - `GET /api/flows`
  - `POST /api/flows`
  - `PATCH /api/flows/:id`
  - `POST /api/flows/:id/toggle`
  - `POST /api/flows/:id/trigger`
  - `GET /api/flows/executions`
- Enforcement and behavior:
  - role-gated (`admin`/`organizer`)
  - validation errors return typed `4xx` responses
  - manual rule trigger writes `FlowExecution` records for observability/audit
- Added unit coverage:
  - `Control Center/server/src/tests/flowService.test.ts`
  - `Control Center/server/package.json` test command updated to run flow tests
- Validation:
  - `cd Control Center/server && npm run build` (PASS)
  - `cd Control Center/server && npm run test:tenant` (PASS, `11` tests)

## Latest Delta (2026-03-02, Gate Role/Permission Claims Hardening)

- Introduced shared RBAC claim helper module:
  - `Gate/authx/app/core/roles.py`
- Gate token issuance now consistently propagates org role context:
  - login access token claims include `org_role`, `roles`, `permissions` (+ compatibility `role`)
  - refresh-token exchange now preserves the same org/role/permission claims in new access tokens
  - OAuth authorization-code token path now includes the same role/permission claim set
- OIDC userinfo and schema/discovery updates:
  - `org_role`, `roles`, `permissions` added to userinfo payload and OIDC claim metadata
- Test coverage updates:
  - `Gate/authx/tests/test_auth.py` extended for role/permission claims in login + refresh
  - `Gate/authx/tests/test_oauth_org_claims.py` extended for role/permission claims
  - containerized Gate test run pass: `16` tests (`auth + oauth + org claims + db repair`)
- Live smoke confirms:
  - login token includes role/permission claims
  - userinfo exposes role/permission claims
  - Atlas enterprise callback (`/api/auth/orbit-callback`) continues to succeed with updated claims

## Latest Delta (2026-03-02, Atlas Enterprise OAuth Stability)

- Atlas enterprise OAuth callback flow is now stable for both local and domain-routed runtimes:
  - `GET /api/auth/orbit-login-url` accepts runtime `redirect_uri` (with path validation)
  - `POST /api/auth/orbit-callback` accepts matching `redirect_uri` and uses it for token exchange
  - frontend PKCE state now persists/verifies:
    - `atlas_pkce_code_verifier`
    - `atlas_orbit_redirect_uri`
- This resolves a real failure mode where Atlas authorized with one redirect URI but exchanged the code using a different `SITE_URL` URI.
- Added Atlas tests for:
  - redirect URI passthrough in authorize URL
  - callback redirect URI forwarding
  - invalid redirect URI path rejection
  - current Atlas auth suite in this slice: `13` passing tests.

## Latest Delta (2026-03-02, Gate OAuth Org Claim Propagation)

- Gate OAuth code-flow access tokens now include `org_id` claim.
- Gate OIDC userinfo now returns `org_id` and discovery claims list includes `org_id`.
- New Gate tests:
  - `authx/tests/test_oauth_org_claims.py`
  - plus existing auth/oauth/repair tests pass together (`16` passing tests in container run).
- Live smoke verified:
  - OAuth access token includes `org_id`
  - `/api/v1/oidc/userinfo` includes matching `org_id`
  - Atlas `/api/auth/orbit-callback` now returns a valid session and mapped user organization in real OAuth+PKCE flow.

## Latest Delta (2026-03-02, Atlas-First Auth Completion Pass)

- Atlas personal auth lane is now live end-to-end against Gate:
  - `POST /api/auth/personal-signup` returns working Atlas session with Gate token
  - `POST /api/auth/personal-login` returns working Atlas session with Gate token
  - added strict upstream response handling (non-2xx from Gate now fails immediately; no false-success on redirects)
- Atlas enterprise SSO lane now supports OAuth PKCE:
  - `GET /api/auth/orbit-login-url` accepts `code_challenge` + `code_challenge_method`
  - `POST /api/auth/orbit-callback` accepts `code_verifier` and supports public OAuth client flow (no client secret required when verifier is present)
  - frontend now generates/stores PKCE pair and submits verifier on callback (`AuthContext.jsx`, `CallbackPage.jsx`)
- Atlas runtime bootstrap improvements:
  - local Gate defaults now target `http://127.0.0.1:45001`
  - JWKS default now derives to `/api/v1/oidc/jwks`
  - Atlas auto-discovers `GATE_OAUTH_CLIENT_ID` from `Gate/authx/registered_apps.json` if env is unset
- Gate production bug fixed that was blocking all new registrations:
  - corrected broken unique index expression on users email-lower index (`lower('email')` -> `lower(email)`)
  - added startup self-heal in Gate (`repair_users_email_lower_index`) to repair legacy DBs automatically
  - restart of `authx-authx-api-1` confirmed repair event logged and registration restored
- New/updated tests:
  - Atlas: `backend/tests/test_auth_onboarding.py` now covers personal org fallback, upstream redirect handling, PKCE authorize URL, PKCE callback, and verifier requirement
  - Gate: new `authx/tests/test_database_repair.py` validates index repair behavior
- Validation run in this pass:
  - Atlas backend tests: `12` passing (`test_auth_onboarding.py` + `test_auth_gate_migration.py`)
  - Gate tests (in container): `11` passing (`test_database_repair.py` + `test_auth.py`)
  - Atlas frontend build: PASS (`npm run build`)
  - Live smoke:
    - Gate register/login: PASS
    - Atlas personal signup/login: PASS
    - Atlas orbit login URL with PKCE params: PASS

## Latest Delta (2026-03-02, Runtime Continuation)

- Calendar is now fully online for integrated demos:
  - frontend on `45005` (PM2 `RM Calendar`)
  - backend API on `5001` (PM2 `RM Calendar API`, `/api/health` verified)
- Mail runtime progressed from template mode to real behavior extensions:
  - backend APIs added for notifications + contacts:
    - `GET /api/mail/notifications`
    - `POST /api/mail/notifications/mark-read`
    - `GET /api/mail/contacts`
  - frontend bridge now consumes those APIs and updates notification indicators
  - login flow no longer auto-falls back to demo session on backend errors (manual demo button remains)
- Domain-hosted dev stability improved:
  - expanded Vite `server.allowedHosts`/`preview.allowedHosts` to include `*.freedomlabs.in` in Mail, Calendar, Atlas, and Meet configs
- Planet runtime blocker fixed:
  - missing dependency `react-hot-toast` added
  - PM2 `RM Planet` now serves on assigned port `45006` (no longer drifted to `45007`)
- Writer startup reliability fixed:
  - `Writer/start-backend.sh` now detects legacy schema states and stamps Alembic head when tables exist without revision metadata
  - `Writer/start.sh` now fails fast if backend startup fails
- Additional services now persist under PM2:
  - `RM Learn` (`5180`)
  - `RM Writer UI` (`5183`)
  - `RM Writer API` (`6011`)
  - `RM Search API` (`6200`)
  - `RM Fonts` (`45007`)
- Validation re-run:
  - `./runtime-matrix-gate.sh` (PASS)
  - `./contract-gate.sh` (PASS)
  - `./smoke-gate.sh` (PASS)
  - Mail/Planet/Calendar builds (PASS)
  - Mail auth + notification/contacts API smoke (PASS)

## Latest Delta (2026-03-02, Mail Settings Hardening)

- Mail settings layer now has real backend operations (not local-only):
  - `POST /api/settings/password`
  - `POST /api/settings/sessions/revoke`
  - `GET /api/settings` enriched with user/security metadata
- New backend implementation:
  - `Mail/backend/app/services/settings_service.py`
  - `Mail/backend/app/schemas/settings.py`
  - updated `Mail/backend/app/api/settings.py`
- New coverage:
  - `Mail/backend/tests/test_settings_service.py` (password change + session revoke scenarios)
- Mail stitch runtime now calls real APIs for:
  - Change Password
  - Logout Other Devices
  - Mark visible mailbox messages read (via notifications mark-read endpoint)
  - Compose Schedule action now deep-links into Calendar after saving a draft
- Verified in live demo runtime (`maildemo`):
  - login with `hmalla@rmmail.com / Qwerty@123`
  - password rotate and rotate-back
  - session revoke
  - notification mark-read

## Latest Delta (2026-03-02, Mail Follow-up)

- Mail Stitch runtime is now functionally wired across all approved pages (`Mail/stitch_rm_mail_secure_login/*` via `runtime-bridge.js`) with concrete actions instead of placeholder behavior.
- Demo account `hmalla@rmmail.com / Qwerty@123` now consistently lands into a non-empty mailbox at startup after seed fix.
- Mail folder semantics improved:
  - `inbox` = inbound (sender != mailbox address)
  - `sent` = outbound (sender == mailbox address)
  - `drafts` = saved drafts by mailbox owner
  - `trash` = soft-deleted rows
- `/trash` route now renders as a real mailbox list view in frontend mapping.
- Mail demo standalone stack (`docker-compose.demo.standalone.yml`) has been rebuilt and validated healthy for `backend`, `worker`, and `frontend` on assigned frontend port `45004`.
- Mail stitch rendering no longer depends on runtime Tailwind CDN execution:
  - all stitch pages now load a bundled local stylesheet (`stitch-tailwind.css`)
  - inline Tailwind runtime config snippets were removed from page heads
  - style blocks converted to plain CSS so they apply even in restricted script/CSP environments.

## Latest Delta (2026-03-02, Mail SSO + Settings Persistence)

- Mail login now supports real Gate OAuth2 PKCE initiation from Stitch login:
  - runtime integrates `GET /api/auth/sso/config` and `POST /api/auth/sso/exchange`
  - callback code exchange is handled on `/login` route in runtime bridge
  - callback redirect now always uses browser origin (`<current-origin>/login`) to avoid proxy/internal host drift
- Mail backend now exposes persisted user settings state endpoints:
  - `GET /api/settings/preferences`
  - `POST /api/settings/preferences`
  - `GET /api/settings/integrations`
  - `POST /api/settings/integrations`
  - persistence is tenant/user scoped via audited snapshot records
- Stitch runtime settings/integrations pages now use backend APIs (local storage retained only as offline fallback cache).
- Mail container runtime now supports backend-to-Gate SSO token exchange path:
  - `Mail/docker-compose.demo.standalone.yml` and `Mail/docker-compose.yml` now set `GATE_BASE_URL=http://host.docker.internal:45001`
  - added `extra_hosts: host.docker.internal:host-gateway` for backend/worker services
- Gate now has a registered Mail OAuth application and Mail is configured to use it:
  - updated `Gate/authx/register_internal_apps.py` to include `Mail` app callback URIs
  - executed registration script and captured live Mail client id
  - updated `Mail/.env` (`GATE_MAIL_CLIENT_ID`) and `Mail/.env.example`
- Added tests and validation:
  - new `Mail/backend/tests/test_sso_service.py`
  - expanded `Mail/backend/tests/test_settings_service.py` (preferences/integrations round-trip)
  - backend suite pass (`19` tests), frontend stitch build pass, live API smoke pass

## 1) Executive State

RM Orbit is in a "Phase 1 foundation complete + Phase 1.5 hardening/migration in progress" state.

What is already in place:
- Centralized identity provider in `Gate` with OAuth2/PKCE and RS256 token flow.
- Tenant/org/workspace request-context contract documented and partially enforced across services.
- Redis event bus with cross-service publishers/consumers.
- Event envelope baseline implemented in core publishers/consumers (`schema_version=1` + `event_id` idempotency key).
- Shared canonical event-envelope fixture pack now exists for cross-service contract validation.
- Runtime matrix drift validator now exists (`runtime-matrix-gate.sh` + `scripts/validate_runtime_matrix.py`) for `PORTS.md` vs launch profiles and core runtime README contract checks.
- Root and service READMEs now include pre-flight gate commands (`./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh`) for contributor consistency.
- PR workflow now enforces the same via `.github/pull_request_template.md` and `CONTRIBUTING.md`.
- Service-token auth standard is now documented (`docs/adr/ADR-002-service-to-service-token-validation.md`) and baseline middleware support is implemented (JWKS + issuer/audience checks with controlled local fallback).
- Meet production-video baseline now exists (signaling + TURN + optional LiveKit SFU + room UI).
- Control Center operations dashboard baseline exists (`/api/ops/overview` + frontend page).
- CI workflow exists for tenant-context/event-contract checks across major services.

What is still in progress:
- Final consistency pass across docs, ports, and startup scripts.
- Cross-app consumers and runtime validation at ecosystem level.
- Prototype services now have delivered backend MVPs in Snitch:
  - Capital Hub: org-isolated asset ledger + lifecycle + renewal workflows
  - Secure: org-isolated endpoint inventory + vulnerability lifecycle + scanner ingest
  Learn now has a runnable docs portal with prototype backend still in Snitch; Writer now has a runnable standalone UI + FastAPI backend baseline with live block editing/version history flows.
- Cross-app global search baseline now exists via standalone `Search/` aggregator service (`/api/search`) using a shared contract (`docs/contracts/global-search-v1.md`) and source adapters for Writer + Learn.
- Structured audit-log baseline now exists with shared helpers (`scripts/orbit_audit.py`, `scripts/orbit-audit.js`) and correlation fields (`request_id`, `org_id`, `workspace_id`) for Writer/Search/Meet.
- Shared `orbit-ui` package baseline now exists at `orbit-ui/`, with synchronized asset/font distribution (`scripts/sync-orbit-ui-assets.sh`) and global Orbit Bar shell wiring in Meet/Learn/Writer.
- Postgres standardization baseline now exists for Writer:
  - Alembic migrations (`Writer/backend/alembic.ini`, `Writer/backend/app/alembic/versions/0001_initial.py`)
  - tenant-aware Writer indexes in schema/models
  - root compose includes `orbit-postgres` (`55432`) and migration-first Writer startup
- Shared object storage baseline now exists:
  - Contract `docs/contracts/object-storage-v1.md`
  - Atlas attachments now use local/S3 pluggable storage provider abstraction
- Atlas auth migration baseline now completed:
  - Atlas is Gate SSO-only (`/auth/login` + `/auth/register` disabled)
  - OAuth callback now returns Gate-issued token directly
  - Atlas verifier now supports JWKS/PEM validation with controlled local HS256 fallback
  - Atlas frontend now propagates org/tenant/workspace headers from token/session
- Connect hardening baseline now completed:
  - backend security middleware stack (helmet + strict CORS + rate limiting + payload limits)
  - structured request/socket audit logging envelopes
  - socket/message sanitization before persistence/broadcast
  - frontend a11y/performance baseline (lazy overlays + dialog semantics/aria + signout wiring)
- Mail Gate-boundary baseline now completed:
  - Gate-token fallback auth context in API dependency layer
  - `X-Org-Id` to token `org_id` consistency enforcement (when header is supplied)
  - JIT tenant/user/mailbox provisioning mapped by `org::<org_id>`
  - tenant operational-control endpoints for queue/storage/retention settings
- Meet production-video baseline now completed:
  - media-session endpoint supports `mesh` default and `livekit` SFU mode
  - TURN configuration supports static and ephemeral credentials
  - room participant roster endpoint added for tenant-scoped visibility

## 2) Verified Repo Snapshot (as of 2026-03-01)

Top-level repos detected:
- Gate
- Atlas
- Calendar (directory exists, but no top-level `.git`)
- Control Center
- Mail
- Connect
- Planet
- Meet
- Learn
- Writer
- Search
- Capital Hub
- Secure
- Snitch

Git pointers and change volume:

| Repo | Branch | HEAD | Modified | Untracked | Notes |
|---|---|---:|---:|---:|---|
| Gate | main | 4326fc6 | 0 | 0 | Clean at snapshot time |
| Atlas | main | 937dc1b | 15 | 12 | Active event-consumer implementation (durable inbox model/sink/API/tests + expanded compatibility contracts) |
| Control Center | main | dded29e | 0 | 0 | Clean at snapshot time |
| Mail | main | 013206e | 5 | 0 | Event schema/docs refinements |
| Connect | main | 00f9108 | 7 | 4 | Typed relay + publisher envelope contract/tests + docs |
| Planet | main | bd7b2cb | 5 | 0 | Event schema/docs refinements |
| Meet | main | 8c2c2dd | 3 | 1 | Event envelope schema-version coverage/tests added |
| Learn | main | 3926c96 | 0 | 1 | Static docs portal in `Learn/site` + `start.sh` server (5180); backend prototype remains in Snitch (6002) |
| Writer | n/a | n/a | n/a | n/a | Standalone UI + FastAPI backend baseline (`Writer/start.sh`) on `5183` / `6011` with optional Gate JWT + Writer event publishing |
| Search | n/a | n/a | n/a | n/a | FastAPI aggregator baseline (`Search/start.sh`) on `6200` with Writer + Learn source adapters |
| Capital Hub | main | 58dd7aa | 0 | 0 | Concept stage |
| Secure | main | 04218e4 | 0 | 0 | Concept stage |
| Snitch | main | eecfadd | 1 | 0 | README/runtime notes touched |
| Calendar | n/a | n/a | n/a | n/a | Not a git repo at this folder root |

Important: workspace is intentionally dirty across multiple repos. Do not reset/revert broadly.

## 3) Architecture Baseline (Current)

### 3.1 Identity/Auth
- Provider: `Gate/AuthX`
- Flow: OAuth2 Authorization Code + PKCE for frontends
- Token verification: RS256 (with HS256 fallback in some services for local compatibility)
- Core headers/claims:
  - `Authorization: Bearer <JWT>`
  - `X-Org-Id` required in strict mode
  - Optional `X-Tenant-Id`, `X-Workspace-Id`
  - JWT claims include `sub`, `org_id` and optionally `tenant_id`, `workspace_id`, `roles`, `permissions`

Contract reference:
- `docs/adr/ADR-001-tenant-org-workspace-context.md` (Accepted, 2026-03-01)

### 3.2 Tenant Isolation Contract
Validation behavior implemented in current pattern:
- Reject if org context cannot be resolved.
- Reject when header/token org mismatch.
- Optional tenant/workspace mismatch checks when both values are present.
- Route-level org params (where used) must match resolved org context.

### 3.3 Event Bus
- Transport: Redis pub/sub
- Pattern: domain channels (e.g., `calendar.*`, `planet.*`, `project.*`, `*.activity`)
- Envelope trend toward normalized shape:
  - `event_type`, `schema_version`, `org_id`, `user_id`, `data` (plus metadata)
  - Current default is `schema_version = 1` when publisher payload omits version
- Canonical fixture pack:
  - `docs/contracts/event-envelope-v1.json` (shared sample envelopes + expected normalization/rejection outcomes)
- Current publishers: Atlas, Calendar, Connect, Mail, Planet, Meet (plus prototype services in Snitch)
- Snitch prototype publishers (Learn/Capital Hub/Secure + EventBus bridge) now emit the same normalized envelope and are covered by fixture-driven contract tests.
- Current consumers: Connect (socket relay), Atlas (selective consumer path + durable event inbox persistence)

## 4) Service-by-Service Status

## Gate (AuthX)
- Role: identity provider.
- Runtime (README): Dockerized service on host `45001`, Postgres `5444`, Redis `6344`.
- Key files:
  - `Gate/authx/app/*`
  - `Gate/authx/register_internal_apps.py`
- Start:
  - `cd Gate && ./start.sh`
- Notes:
  - Login template/font updates are in local changes.

## Atlas
- Stack: FastAPI backend + React frontend.
- Runtime scripts currently target backend `8000`, frontend `5173`.
- Progress:
  - Atlas auth now runs Gate-only token flow with JIT local user/org synchronization from Gate claims.
  - Local Atlas credential endpoints are disabled; frontend login path is RM Orbit SSO only.
  - Tenant context middleware/tests added.
  - Event consumer hardening and compatibility tests added.
  - Event sink wiring added: normalized org-scoped ecosystem events are now persisted into Atlas `ecosystem_event_inbox` for diagnostics/integration workflows.
  - New org-scoped read endpoint for consumed events: `GET /api/ecosystem/events`.
  - Endpoint contract coverage now includes API-level tests via FastAPI `TestClient` + dependency overrides.
  - Project-side activity sink added for selected consumed events (org/project/user validated before write).
  - Cross-service compatibility contract now explicitly validates Calendar/Planet/Mail/Meet/Connect envelope ingestion and `schema_version` behavior.
  - Shared fixture-pack compatibility test added (`docs/contracts/event-envelope-v1.json`) for data-driven envelope validation.
- Key areas:
  - `Atlas/backend/app/tenant_context.py`
  - `Atlas/backend/app/services/*`
  - `Atlas/backend/app/models/ecosystem_event.py`
  - `Atlas/backend/app/routers/ecosystem_events.py`
  - `Atlas/backend/tests/test_ecosystem_events_endpoint.py`
  - `Atlas/backend/tests/test_ecosystem_events_api.py`
  - `Atlas/backend/tests/*`

## Calendar
- Stack: Express backend + React frontend.
- Runtime docs/scripts: backend `5001`, frontend `45005`.
- Progress:
  - Auth middleware + tenant context enforcement documented.
  - Event publishing via Redis.
- Note: Calendar folder currently lacks top-level `.git` metadata.

## Control Center
- Stack: React frontend + Express/TypeScript backend (Prisma SQLite).
- Runtime from `start.sh`: frontend `45003`, backend `8077`.
- Progress:
  - Tenant-context middleware implemented.
  - Operations API route and frontend view added.
  - OAuth auth context/callback wiring present.
- Key files:
  - `Control Center/server/src/middleware/tenantContext.ts`
  - `Control Center/server/src/routes/opsRoutes.ts`
  - `Control Center/server/src/controllers/opsController.ts`
  - `Control Center/src/pages/Operations.tsx`

## Mail
- Stack: FastAPI + React (enterprise baseline architecture).
- Progress:
  - Gate-boundary auth context integration completed in API dependency layer.
  - Gate claims now JIT-provision tenant/user/mailbox records (`org::<org_id>` mapping).
  - Admin operational controls added:
    - `GET /api/admin/tenant-controls`
    - `POST /api/admin/retention/apply`
  - Event envelope contract + focused auth/admin tests now present:
    - `tests/test_eventbus_contract.py`
    - `tests/test_deps_auth_context.py`
    - `tests/test_admin_service.py`

## Connect
- Stack: Node/Express + Socket.io + React frontend.
- Progress:
  - Tenant-context middleware for HTTP/socket boundaries.
  - Eventbus consumer and socket runtime isolation tests.
  - Auth middleware extracted with tests.
  - Typed org-scoped relay added in socket runtime (`ecosystem_event` + domain event channels such as `project_event`, `calendar_event`).
  - Outbound publisher envelope contract hardened with shared builder (`schema_version` default/preserve + org/user context normalization).
  - Phase-10 hardening baseline completed (security middleware + audit logs + input sanitization + a11y/perf baseline updates).
- Key files:
  - `Connect/server/tenant-context.js`
  - `Connect/server/auth-middleware.js`
  - `Connect/server/eventbus-consumer.js`
  - `Connect/server/event-envelope.js`
  - `Connect/server/socket-runtime.js`
  - `Connect/server/*test.js`

## Planet
- Stack: React frontend + new FastAPI backend.
- Runtime: frontend `45006`, backend `46000`.
- Progress:
  - Frontend moved to Gate OAuth PKCE flow.
  - Backend includes Gate auth middleware + tenant checks + event publishing.

## Meet
- Stack: React frontend + new Node signaling backend.
- Runtime: frontend `5178`, backend `6001`.
- Progress:
  - Backend now includes production media-session baseline:
    - `GET /api/meetings/:meetingId/media-session` (`mesh` default, optional `livekit` SFU)
    - `GET /api/meetings/:meetingId/participants` (org-scoped room roster)
    - TURN config supports static credentials and ephemeral shared-secret credentials.
  - Frontend active meeting route resolves media mode at join and supports LiveKit SFU connection with mesh fallback.
  - Existing signaling + recording APIs remain tenant-scoped and active.

## Learn / Capital Hub / Secure
- Current state: Learn has a runnable static documentation portal (`Learn/start.sh`, port `5180`).
- Capital Hub and Secure now have backend MVP APIs implemented under `Snitch/backend`:
  - `capitalhub-service.js` (asset ledger/lifecycle/renewals) on `6003`
  - `secure-service.js` (endpoint/vulnerability baseline) on `6004`
- Prototype frontends for Capital Hub and Secure remain in concept/design stage folders pending full app graduation.

## Search
- Stack: FastAPI aggregator backend.
- Runtime: backend `6200`.
- Progress:
  - Cross-app search contract baseline now exists (`docs/contracts/global-search-v1.md`).
  - Minimal aggregator service baseline exists in `Search/` with source adapters for Writer documents and Learn docs pages.

## Writer
- Current state: standalone runnable UI + backend baseline (`Writer/start.sh`, ports `5183` / `6011`) with detailed architecture notes in `Writer/readme.txt`.
- Backend currently provides a workspace-scoped document/block graph API baseline with version snapshots.
- Frontend dashboard/document screens now consume live Writer APIs for document listing, creation, block editing, block creation, and version-history inspection.
- Backend now supports optional Gate-compatible JWT enforcement (`WRITER_AUTH_REQUIRED`, JWKS/public-key/issuer/audience envs with local HS256 fallback).
- Backend now publishes normalized Writer mutation events to Redis (`writer.*` + `writer.activity`) with shared envelope contract alignment and fixture-driven contract coverage.

## Snitch
- Role: prototype incubator for unfinished apps.
- Includes sample backend services for Learn/Capital Hub/Secure and shared event bus utilities.
- Prototype publishers now use shared envelope builder (`Snitch/backend/event-envelope.js`) with org-aware channel publishing (`learn.*`, `capitalhub.*`, `secure.*`) and compatibility relay to `global`.
- Shared tenant-context middleware now enforces header/token org consistency in Snitch services.
- `Snitch/backend/eventbus.js` now enforces authenticated org-scoped publishing on `POST /publish`.

## 5) CI / Test Contract Status

Workflow present:
- `.github/workflows/tenant-context.yml`

Jobs included:
- Atlas (Python unittest tenant + ecosystem event contract tests)
- Control Center (npm `test:tenant`)
- Calendar (npm `test:tenant`)
- Planet (Python unittest tenant + event contract tests)
- Mail (pytest event contract test)
- Connect (npm `test:tenant`)
- Meet (npm `test:tenant`)
- Snitch (node tenant-context + event-envelope tests)
- Unified root contract gate (`./contract-gate.sh`) via `contract-gate` CI job
- Runtime matrix gate (`./runtime-matrix-gate.sh`) via `runtime-matrix` CI job
- Integration smoke gate (`./smoke-gate.sh`) via `integration-smoke` CI job

Local execution status in this handoff session:
- Tests were re-run on 2026-03-01.
- Results:
  - Atlas: `PASS` (`28` tests, `python3 -m unittest`)
  - Control Center: `PASS` (`6` tests)
  - Calendar: `PASS` (`5` tests)
  - Planet: `PASS` (`6` tests, `python3 -m unittest`)
  - Mail: `PASS` (`8` targeted tests, pytest)
  - Connect: `PASS` (`26` tests total, `7` skipped by design)
  - Meet: `PASS` (`15` tests total, `1` skipped by design)
  - Snitch: `PASS` (`6` tests, `node --test tenant-context.test.js event-envelope.test.js`)
  - Writer backend: `PASS` (`8` tests, `pytest -q`)
  - Root gates: `PASS` (`./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh`)

## 6) Operational Runbook (Current Practical Start)

Primary orchestration options:
- Global script: `./start-all.sh`
- PM2 config: `pm2 start ecosystem.config.cjs`
- Docker Compose baseline: `docker compose -f docker-compose.orbit.yml up --build -d`

Per-service convenience scripts exist:
- `Gate/start.sh`
- `Atlas/start.sh`
- `Calendar/start.sh`
- `Control Center/start.sh`
- `Mail/start.sh`
- `Connect/start.sh`
- `Planet/start.sh`
- `Meet/start.sh`
- `Learn/start.sh`
- `Writer/start.sh`

Health/status helper:
- `./status.sh`
Validation helpers:
- `./contract-gate.sh`
- `./runtime-matrix-gate.sh`
- `./smoke-gate.sh`

## 7) Known Inconsistencies to Resolve Early

1. Port/runtime drift across files.
- `PORTS.md`, `start-all.sh`, PM2 profile mappings, and core README runtime/pre-flight tokens are now checked by `runtime-matrix-gate.sh`.
- Remaining risk is primarily profile confusion (`start-all.sh` vs PM2) and cross-stack collisions (Mail vs Atlas defaults), not unnoticed table/script drift.
- Current canonical reference remains `PORTS.md` (Profile A and Profile B tables).

2. Calendar repository metadata gap.
- `Calendar/` has no top-level `.git` in this workspace snapshot, unlike sibling services.

3. Legacy/optimistic status docs.
- Several high-level docs mark production-ready/completed state broadly; codebase still shows active uncommitted implementation work across multiple services.

4. Duplicate narrative sources.
- `IMPLEMENTATION_SUMMARY.md`, `PHASE1_COMPLETE.md`, `CHANGES_LOG.md`, and `ECOSYSTEM_TODO_PLAN.md` overlap and can diverge.

## 8) Prioritized Backlog (Consolidated)

P0 (do first):
- Freeze one authoritative runtime matrix (ports, URLs, startup order, env vars).
- Standardize tenant context contract enforcement uniformly in all active services.
- Extend the now-explicit event envelope version policy (`schema_version=1`) to any remaining producers/consumers and enforce in CI contract checks.

P1:
- Complete cross-app event consumer behavior (especially Connect + Atlas integration paths).
- Expand and stabilize operations dashboard telemetry across services.
- Finish Meet production readiness (TURN/SFU, observability, failure-handling).

P2:
- Graduate Learn/Capital Hub/Secure from Snitch scaffolds to first-class services with auth/isolation/tests.

P3:
- Phase 2 architecture exploration (Kafka, gRPC, GraphQL federation) only after P0/P1 runtime consistency is complete.

## 9) Recommended First-Hour Plan for a New Agent

1. Baseline and validate runtime matrix.
- Use `PORTS.md` as canonical and reconcile remaining README drift to it.
- Keep PM2 profile (`ecosystem.config.cjs`) and `start-all.sh` profile differences explicitly documented.

2. Run contract tests locally for services that currently have suites.
- Atlas, Control Center, Calendar, Planet, Mail, Connect, Meet.
- Record pass/fail with failing test details.

3. Resolve highest-risk mismatches.
- Header/token org enforcement edge cases.
- Event envelope compatibility between publishers and consumers.

4. Update docs after code changes.
- Keep `ECOSYSTEM_TODO_PLAN.md` and this handoff report synchronized.

## 10) Command Checklist for Next Agent

From root:

```bash
cd "/home/sasi/Desktop/dev/RM Orbit"

# Optional: quick process snapshot
./status.sh

# Start ecosystem (one approach)
pm2 start ecosystem.config.cjs
# or
./start-all.sh

# Run CI-equivalent contract tests manually (examples)
./contract-gate.sh
./runtime-matrix-gate.sh
./smoke-gate.sh

# Or run full per-service suites:
cd Atlas/backend && python3 -m unittest discover -s tests -p "test_*.py"
cd "../../Control Center/server" && npm run test:tenant
cd ../../Calendar/server && npm run test:tenant
cd ../../Planet/backend && python3 -m unittest discover -s tests -p "test_*.py"
cd ../../Mail/backend && PYTHONPATH=. pytest tests/test_eventbus_contract.py
cd ../../Connect/server && npm run test:tenant
cd ../../Meet/server && npm run test:tenant
```

## 11) Source of Truth Files (Read First)

1. `ECOSYSTEM_TODO_PLAN.md` (most concrete execution tracker)
2. `docs/adr/ADR-001-tenant-org-workspace-context.md` (contract)
3. `docs/adr/ADR-002-service-to-service-token-validation.md` (JWKS + issuer/audience contract)
4. `docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md` (schema version + `event_id` idempotency contract)
5. `docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md` (database standard + migration contract)
6. `docs/db/postgres-tenant-partitioning-strategy.md` (tenant-aware indexing/partition thresholds)
7. `docs/PROTOTYPE_GRADUATION_CHECKLIST.md` (required promotion gates for prototype services)
8. `docs/contracts/event-envelope-v1.json` (shared event-envelope fixture pack)
9. `docs/contracts/global-search-v1.md` (cross-app search contract)
10. `docs/contracts/audit-log-envelope-v1.md` (structured audit-log contract)
11. `docs/contracts/object-storage-v1.md` (shared local/S3 object storage contract)
12. `.github/workflows/tenant-context.yml` (test expectations)
13. `contract-gate.sh` (single-command envelope contract gate)
14. `runtime-matrix-gate.sh` + `scripts/validate_runtime_matrix.py` (runtime drift gate)
15. `smoke-gate.sh` (runtime integration smoke gate)
16. `ecosystem.config.cjs` + `start-all.sh` (runtime reality)
17. `orbit-ui/README.md` + `scripts/sync-orbit-ui-assets.sh` (shared shell/tokens source + sync mechanism)
18. Service READMEs for Gate/Control Center/Calendar/Planet/Meet/Connect/Mail/Learn/Writer/Search

## 12) Handoff Integrity Notes

- This report reflects direct file inspection and git status snapshots from 2026-03-01.
- Contract tests were executed in this session with all suites passing (some suites include intentional `skip` cases).
- The worktree is intentionally mid-flight; preserve local changes unless explicitly instructed otherwise.

## 13) Incremental Update (2026-03-02 Follow-up, Latest)

### Host Allowlist + Port-Route Stability
- Added missing Vite host allowlist support for Cloudflare domains:
  - `Connect/vite.config.ts`
  - `Control Center/vite.config.ts`
  - `Snitch/frontend/vite.config.js`
- All now include:
  - `server.allowedHosts = ['.freedomlabs.in', 'localhost', '127.0.0.1']`
  - `preview.allowedHosts = ['.freedomlabs.in', 'localhost', '127.0.0.1']`

### Mail Runtime Hardening (Stitched UI)
- Updated `Mail/stitch_rm_mail_secure_login/runtime-bridge.js`:
  - integrated app open behavior now uses popup-safe fallback (new-tab first, same-tab fallback) for Calendar/Chat/Connect and support links
  - mailbox list cards now include inline `Chat` action opening thread-aware in-mail chat drawer
  - boot sequence now enforces viewport sizing (`html/body` width/height/min-height) to mitigate partial/collapsed rendering edge cases
  - switched external opener call sites to shared fallback handler for consistency

### Validation Snapshot (Latest)
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- Frontend builds:
  - `Connect npm run build` -> PASS
  - `Control Center npm run build` -> PASS
  - `Mail/frontend npm run build` -> PASS
- Root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 14) Incremental Update (2026-03-02, Mail Flags + Archive End-to-End)

### Backend Capabilities Added
- Added persistent Mail flag APIs:
  - `GET /api/mail/{email_id}/flags`
  - `POST /api/mail/{email_id}/flags`
  - `DELETE /api/mail/{email_id}/flags/{flag}`
- Added support for `archive` mailbox listing semantics and per-item `flags` in mailbox payload responses.
- Repository/service layer now supports:
  - list/set/clear flags (`read`, `starred`, `archived`)
  - archive filtering from inbox/sent/drafts
  - dedicated archive folder retrieval

### Mail Runtime Wiring Completed
- `Mail/stitch_rm_mail_secure_login/runtime-bridge.js` now uses backend flags for:
  - reader star/unstar action persistence
  - archive/unarchive action persistence
- Mailbox list cards now include:
  - starred/archived visual badges
  - archive/unarchive quick action
- Added route/link support for archive UI path:
  - Mail frontend shell route `/archive`
  - runtime route resolution and text-link navigation mapping

### Additional Backend Resilience Hardening
- Added SQLite-safe fallback for `body_tsv` generation during compose/send in non-Postgres contexts.
- Added graceful rate-limit fallback when Redis is unavailable (prevents local/test hard-fail sends).

### Latest Validation
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `24 passed`
- `cd Mail/frontend && npm run build` -> PASS
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- Root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 15) Incremental Update (2026-03-02, Mail Consistency Follow-up)

### Backend
- Notification feed consistency:
  - archived emails are now excluded from `list_recent_inbound`, keeping `/api/mail/notifications` aligned with archive-folder semantics.
- Trash/archive state cleanup:
  - when an email is soft-deleted (moved to trash), `archived` flag is now removed to avoid stale state.
- Added regression coverage:
  - `Mail/backend/tests/test_mail_flags.py` now validates:
    - archived message hidden from notifications
    - restored (unarchived) message returns to notifications.

### Mail Stitched UI
- Mailbox list now supports real star toggle action per card (backend persisted):
  - action uses `/api/mail/{email_id}/flags` and `/api/mail/{email_id}/flags/starred`
  - deterministic star-state read from explicit card attributes (`data-is-starred`)
  - click routing guards prevent star/archive/chat/delete controls from opening thread unintentionally.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `24 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 16) Incremental Update (2026-03-02, Mail Contacts Persistence Slice)

### Backend Mail Contacts
- Added endpoints:
  - `POST /api/mail/contacts`
  - `DELETE /api/mail/contacts/{email}`
- Manual contacts are persisted server-side using tenant/user-scoped audit snapshots (`mail.contacts.updated`).
- Contact listing now merges:
  - inferred contacts from email traffic
  - persisted manual contacts.

### Runtime/UI Contact Wiring
- `runtime-bridge.js` now uses backend for contact mutation flows:
  - quick add (`person_add`)
  - add during call flow
  - directory new-contact action
  - search sender capture
- Added contact deletion action in directory cards (backend delete + immediate refresh).
- Local fallback is preserved for non-auth/demo/offline scenarios.

### Validation (Latest)
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `25 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 17) Incremental Update (2026-03-02, Mail Trash Restore)

### Backend
- Added Mail restore API:
  - `POST /api/mail/{email_id}/restore`
- `MailService.restore_email` now restores soft-deleted emails and records `mail.restore` audit entries.
- Added test coverage for:
  - archive -> delete -> restore flow
  - archived flag cleanup on delete
  - restored message visibility in inbox/trash.

### Runtime/UI
- Trash mailbox cards now include `Restore` action wired to backend restore endpoint.
- Demo runtime now supports restore semantics and previous-folder recovery.
- Archive icon routing corrected to `/archive` for consistent folder navigation.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `26 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 18) Incremental Update (2026-03-02, Mail Draft Detail + Compose Hydration)

### Backend
- Added detail endpoint for direct email fetch:
  - `GET /api/mail/email/{email_id}`
- Added recipient lookup support in repository:
  - `MailRepository.list_email_recipients(tenant_id, email_id)`
- Added service-level email detail aggregation:
  - `MailService.get_email_detail(ctx, email_id)` now returns sender/subject/body, `to`/`cc`/`bcc`, and flags.
- Added backend test coverage:
  - `Mail/backend/tests/test_mail_detail.py`

### Runtime/UI (Stitched Mail)
- Draft mailbox cards now open compose with real identifiers:
  - include `email_id` and `thread_id` query params.
- Compose page now hydrates draft content from backend:
  - calls `/api/mail/email/{email_id}` and prefills recipients, subject, body.
- Compose submit now preserves thread continuity:
  - sends `thread_id` when available.
- Demo API parity added:
  - implemented `GET /api/mail/email/{id}`
  - compose demo path now persists `to`/`cc`/`bcc` in saved draft/sent payloads.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `27 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 19) Incremental Update (2026-03-02, Mail True Draft Edit Semantics)

### Backend
- Compose schema now accepts draft edit context:
  - `ComposeEmailRequest.draft_email_id`
- `MailService.send_or_draft` now supports updating an existing draft in place:
  - validates draft ownership/mailbox/tenant
  - preserves same email id
  - replaces recipients (instead of accumulating stale rows)
  - transitions draft -> sent when `save_draft=false`
- Added repository helper:
  - `MailRepository.replace_recipients(tenant_id, email_id, recipients)`
- Added regression tests:
  - `Mail/backend/tests/test_mail_draft_edit.py`
  - verifies save-existing-draft and send-existing-draft behaviors.

### Runtime/UI (Stitched Mail)
- Compose submit now sends `draft_email_id` when editing an existing draft, enabling true backend update semantics.
- Demo compose API now mirrors real behavior:
  - updates existing draft in place when `draft_email_id` is provided
  - enforces draft-only edits
  - supports draft -> sent transition on send.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `29 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 20) Incremental Update (2026-03-02, Mail Real Attachments End-to-End)

### Backend
- Added local storage upload/download API routes:
  - `PUT /api/storage/local/upload/{object_key}`
  - `GET /api/storage/local/download/{object_key}`
- Wired storage router into Mail backend app startup routing.
- Added repository helpers:
  - `list_attachments(tenant_id, email_id)`
  - `replace_attachments(tenant_id, email_id, attachments)`
- Draft edit behavior now replaces attachments in place (not stale append).
- Email detail endpoint now includes attachment metadata + `download_url` values.

### Runtime/UI (Stitched Mail)
- Compose page `attach_file` is now real:
  - file picker opens
  - calls `/api/mail/attachments/presign`
  - uploads to presigned URL (local auth upload and S3-compatible upload flows)
  - renders removable attachment chips with file name + size
  - submits real attachment payloads on draft/save/send.
  - compose attachment input lifecycle is reset per route bind (prevents stale handlers on repeated compose navigation).
- Draft compose hydration now restores existing draft attachments from `/api/mail/email/{id}`.
- Reader page attachment section now binds to real email-detail attachments and uses authenticated download flow (replacing previous blob placeholder behavior).
- Demo API parity expanded:
  - stores per-email attachments in compose path
  - returns attachments in email detail responses.

### Tests + Validation
- Expanded tests:
  - `test_mail_detail.py` now asserts attachment payload shape from detail endpoint.
  - `test_mail_draft_edit.py` now asserts attachment replacement/update semantics.
- Validation snapshot:
  - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
  - `cd Mail/backend && PYTHONPATH=. pytest -q` -> `29 passed`
  - `cd Mail/frontend && npm run build` -> PASS
  - root gates:
    - `./runtime-matrix-gate.sh` -> PASS
    - `./contract-gate.sh` -> PASS
    - `./smoke-gate.sh` -> PASS

## 21) Incremental Update (2026-03-02, Mail Cc/Bcc Real Wiring + Storage Scope Security)

### Backend Security Hardening
- Local storage API now enforces tenant-scoped attachment keys:
  - object keys must be rooted to the authenticated tenant prefix (e.g. `tenant_id/...`)
  - cross-tenant key access now returns `403 Forbidden`.
- Added storage API tests:
  - upload/download happy path within tenant scope
  - cross-tenant scope rejection checks.

### Runtime/UI Realism
- Compose page now has real `Cc/Bcc` behavior:
  - `Cc/Bcc` toggle reveals functional input rows
  - draft hydration now restores `cc` and `bcc` recipients
  - query prefill (`cc`, `bcc`) is supported
  - compose submit now sends actual `cc` and `bcc` arrays to backend.
- Maintained existing draft/thread/attachment semantics while extending recipient fidelity.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `31 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 22) Incremental Update (2026-03-02, Mail Signed Local Upload Tokens)

### Backend Security
- Local attachment presign generation now signs local upload URLs with short-lived JWT tokens containing:
  - `type=local_upload`
  - `tenant_id`
  - `mailbox_id`
  - `object_key`
  - `mime_type`
  - `exp`
- Local upload endpoint now requires and validates this signed token before accepting content.
- Validation now enforces token scope consistency for tenant/key/mime (not just path prefix).

### Tests Added/Expanded
- `Mail/backend/tests/test_storage_api.py`
  - updated for token-required upload flow
  - added missing-token rejection assertion.
- `Mail/backend/tests/test_attachment_presign.py`
  - asserts presign URL includes token and token claims match expected tenant/object/mime fields.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `33 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 23) Incremental Update (2026-03-02, Mail Signed Local Download Tokens)

### Backend Security
- Email detail attachment download URLs are now tokenized for local storage paths.
- Local download endpoint now requires and validates signed download token claims:
  - `type=local_download`
  - `tenant_id`
  - `object_key`
  - `exp`
- This closes the remaining gap where in-tenant users could potentially probe keyspace by path alone.

### Tests Added/Expanded
- `test_storage_api.py`
  - added missing-download-token rejection test
  - updated happy-path download to include signed token.
- `test_attachment_presign.py`
  - added coverage asserting email-detail attachment download URLs include valid signed local-download tokens.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `35 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 24) Incremental Update (2026-03-02, Mail Attachment Object-Key Scope Enforcement)

### Backend Security
- Added strict object-key normalization/validation for compose attachments:
  - attachment `object_key` must be non-empty and structurally valid
  - path traversal segments (`..`) are rejected
  - key must remain inside authenticated tenant prefix (`{tenant_id}/...`)
  - malformed or cross-tenant keys now fail with `INVALID_INPUT`.
- Validation is applied both to:
  - presign-generated keys (defensive check)
  - client-provided compose attachment payload keys.

### Tests Added
- Expanded `Mail/backend/tests/test_mail_draft_edit.py` with:
  - cross-tenant attachment key rejection test
  - malformed key-shape/path traversal rejection test.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `37 passed`
- `cd Mail/frontend && npm run build` -> PASS
- root gates:
  - `./runtime-matrix-gate.sh` -> PASS
  - `./contract-gate.sh` -> PASS
  - `./smoke-gate.sh` -> PASS

## 25) Incremental Update (2026-03-03, Meet + Calendar Real-Flow Wiring, Mail Port Alignment)

### Meet (Frontend + Backend Integration)
- `Meet/server/signaling-runtime.js`
  - added org-scoped room chat history and `chat.send` handling
  - emits `chat.history` on room join
  - publishes `meeting.chat.message` event bus payloads.
- `Meet/server/index.js`
  - added `POST /api/dev/session` for local dev session bootstrap
  - added `GET /api/meetings/:meetingId/chat/history`
  - kept participant/media/recording routes intact.
- `Meet/src/views/ActiveMeeting.jsx`
  - chat/participants navigation now keeps `meetingId`
  - recording start/stop wired to backend recording APIs
  - calendar handoff button added (opens Calendar with meeting context)
  - fullscreen button now functional.

### Calendar (Broken Flow Fixes)
- `Calendar/src/components/TeamView.tsx`
  - team timeline now uses selected calendar date (not only current day)
  - added shared availability panel and one-click team-slot scheduling.
- `Calendar/src/components/TaskModal.tsx` and `TasksView.tsx`
  - tasks now support tagging people (`@mentions`) in create/edit and display views
  - added in-view "New Task" and clearer task start actions.
- `Calendar/src/App.tsx`
  - notification items now open linked task/event context
  - ecosystem app links now map correctly under `*.freedomlabs.in`
  - meet->calendar intent bootstrap added via query params.
- `Calendar/server/index.js`
  - task normalization expanded to persist `mentions`
  - profile resolution improved for signed-in token user
  - task notification metadata includes mentions.

### Mail Runtime/Infra Alignment
- aligned Mail frontend runtime to assigned port `45004`:
  - `Mail/frontend/vite.config.ts` (`server` + `preview` -> `45004`)
  - `Mail/frontend/package.json` dev script -> `--port 45004`
  - proxy fallback adjusted to `http://localhost:8000` for local default.
- updated Mail backend and env defaults for matching CORS:
  - `Mail/backend/app/core/config.py`
  - `Mail/.env` and `Mail/.env.example`.
- updated compose mappings:
  - `Mail/docker-compose.yml` -> `45004:45004`
  - `Mail/docker-compose.demo.yml` -> `5184:45004`
  - `Mail/docker-compose.demo.standalone.yml` -> `45004:45004`.

### Validation Snapshot
- `cd Meet && npm run build` -> PASS
- `cd Meet/server && npm run test:tenant` -> PASS
- `cd Calendar && npm run build` -> PASS
- `cd Calendar/server && node --test *.test.js` -> PASS
- `cd Mail/frontend && npm run build` -> PASS
- `cd Mail/backend && PYTHONPATH=. pytest -q` -> `40 passed`

## 26) Incremental Update (2026-03-03, Calendar Real-API Runtime Hardening for Domain Access)

### Calendar Frontend Runtime Fixes
- Removed direct backend hardcode usage that breaks under `https://*.freedomlabs.in` due mixed-content/cross-origin constraints.
- Calendar frontend now uses configurable API base with safe default:
  - `VITE_CALENDAR_API_URL` when provided
  - fallback to relative `/api` (same-origin).
- Files updated:
  - `Calendar/src/App.tsx`
  - `Calendar/src/components/TeamView.tsx`

### Vite Proxy Alignment (Assigned Frontend Port Preserved)
- Added dev proxy to route `Calendar` frontend `/api/*` requests to backend `5001`:
  - `Calendar/vite.config.ts`
  - `server.proxy['/api'] -> http://127.0.0.1:5001`.
- Result: domain-hosted frontend (`calendar.freedomlabs.in` -> local `45005`) can use real APIs without frontend-side direct localhost backend calls.

### Auth Session Resilience (No Fake Profile Lockups)
- Added automatic recovery path for stale/invalid auth tokens:
  - Calendar boot now retries profile bootstrap by forcing local dev session creation when initial profile call fails with auth-like errors (`401/403/unauthorized/token` signals).
- Added token clearing utility:
  - `Calendar/src/lib/auth.ts` -> `clearStoredTokens()`.

### Team Availability UX Visibility
- Team availability/scheduling assistant now opens by default in Team view to expose timeline + free-slot scheduling without hidden discovery friction.
- File updated:
  - `Calendar/src/components/TeamView.tsx`.

### Type + Docs
- Added missing Vite TS env typing file:
  - `Calendar/src/vite-env.d.ts`.
- README updated for API proxy/runtime behavior:
  - `Calendar/README.md`.

### Validation Snapshot
- `cd Calendar && npm run build` -> PASS
- `cd Calendar/server && npm run test:tenant` -> PASS (`5` tests)
- Runtime smoke:
  - started `Calendar` dev frontend on `45005`
  - `curl http://127.0.0.1:45005/api/health` -> `{"status":"ok","service":"calendar"}` (proxy confirmed)

## 27) Incremental Update (2026-03-03, Mail Stitch Full-Viewport Reliability + Runtime Port Gate)

### Mail UI Runtime Reliability
- Added stitch stylesheet fallback handling so Mail pages do not collapse into a tiny corner when `stitch-tailwind.css` fails from absolute path resolution under domain routing.
- Runtime now:
  - verifies stitch stylesheet presence
  - auto-injects fallback `../stitch-tailwind.css` when missing
  - switches existing stylesheet to fallback path on load error.
- Files updated:
  - `Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
  - synced via frontend stitch sync/build pipeline to:
    - `Mail/frontend/public/stitch_rm_mail_secure_login/runtime-bridge.js`
    - `Mail/frontend/dist/stitch_rm_mail_secure_login/runtime-bridge.js`.

### Validation Snapshot
- `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js` -> PASS
- `cd Mail/frontend && npm run build` -> PASS
- assigned runtime gate:
  - `python3 scripts/verify_assigned_runtime.py` -> PASS
  - confirms assigned frontends `45001,45003-45013,5173` are `OPEN`, with `Mail/Calendar/Meet/...` returning HTTP `200`.

## 28) Incremental Update (2026-03-03, Calendar Settings/Profile Real Backend Wiring)

### Backend (Calendar API)
- Added real authenticated settings persistence endpoints:
  - `GET /api/settings`
  - `PUT /api/settings`
- Added real profile update endpoint:
  - `PUT /api/profile`
- Existing profile read now prefers persisted profile name over token-only display name for true profile edits.
- Persistence model:
  - `server/data.json` now includes:
    - `preferences.settingsByActor`
  - settings scope key is per actor context (`org + user`), preventing cross-user collisions.
- Input normalization/safety:
  - meeting duration clamped `15-180`
  - schedule layout constrained to `list|calendar`.

### Frontend (Calendar UI)
- Settings dialog now performs real backend save via `PUT /api/settings`.
- Calendar now pulls backend settings on load via `GET /api/settings` and applies them to UI state.
- Settings modal now has save state feedback (`saving/saved/error`) so users see operation outcome.
- Existing local storage fallback retained for resilience.

### Validation Snapshot
- `cd Calendar && npm run build` -> PASS
- `cd Calendar/server && npm run test:tenant` -> PASS (`5` tests)
- endpoint smoke against updated server (`PORT=5101`) with auth token:
  - `POST /api/dev/session` -> PASS
  - `GET /api/settings` -> PASS
  - `PUT /api/settings` -> PASS
  - `PUT /api/profile` -> PASS
  - `GET /api/profile` -> PASS

## 29) Incremental Update (2026-03-03, Calendar Session Bootstrap Incident Fix)

### Incident
- Calendar UI showed: `Failed to initialize local calendar session`.
- Root cause was a stale Calendar API process on `5001` serving older middleware ordering, causing:
  - `POST /api/dev/session` -> `401 No authorization token provided`.

### Remediation
- Restarted Calendar stack (`Calendar/start.sh`) so current server code is active.
- Verified session bootstrap endpoint:
  - `POST http://127.0.0.1:5001/api/dev/session` -> `200`
  - `POST http://127.0.0.1:45005/api/dev/session` (via Vite proxy) -> `200`.

### Recurrence Guard
- Added Calendar API process to PM2 ecosystem config so frontend is not orphaned from backend after restarts:
  - `ecosystem.config.cjs` now includes `Calendar-Backend` (`cwd: ./Calendar/server`, `npm start`).
- Started `Calendar-Backend` via PM2 and verified status `online`.
