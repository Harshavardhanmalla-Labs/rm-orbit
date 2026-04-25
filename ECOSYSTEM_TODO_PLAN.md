# RM Orbit Ecosystem Todo + Execution Plan (Draft)

Date: 2026-03-09
Status: Active execution (implementation in progress + new ticketing/intelligence backlog)

## Product Governance Lock (Effective 2026-03-09)

- Ecosystem expansion freeze is active.
- No additional major RM Orbit applications should be added until current applications reach production readiness and real-user adoption.
- Mandatory reference: `docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md`
- Interoperability directive reference: `docs/specs/orbit-interoperability-migration-bridge-v1.md`
- Approved near-term path: deliver time card submission and approval as a module in `Control Center` (no new app).
- Controlled future concept only: `RM People` as a scoped employee-lifecycle capability (not payroll), deferred until production-readiness gates are met.

## Implementation Progress (Updated 2026-03-02)

- Legacy checklist completion (through Phase 4 baseline): `28/28` (`100%`).
- New backlog kickoff (added 2026-03-09): `10/13` (`77%`) with web baselines in progress.
- TurboTick kickoff started (2026-03-09):
  - renamed ticketing tool to **TurboTick** across ecosystem docs
  - created `TurboTick/` module scaffold and baseline backend API (`/health`, `/api/tickets*`)
  - expanded TurboTick backend to core platform modules (tickets/incidents/requests/workflows/sla/timeline/kb/analytics/ai-config)
  - implemented TurboTick queue/link/escalation/SLA API endpoints with upgraded org-isolation test suite (`10 passed`)
  - delivered TurboTick web MVP (`TurboTick/frontend/index.html`) with dark-mode high-density operations workspace
  - added Mail compose right-click smart actions (`Ask Atlas`, `Create TurboTick Ticket`, `Open TurboTick`)
  - added Connect message + composer right-click/long-press smart actions and command palette actions for Atlas/TurboTick
  - added TurboTick auth modes (`headers|gate|hybrid`) and domain event producer baseline (`/api/events` + optional sink webhook)
  - added TurboTick durable publish transport baseline (`redis_streams`) for event-bus compatibility
  - added TurboTick event consumer API baseline (`/api/events/consume`) for external intake and status sync flows
  - added TurboTick Redis ingress drain endpoint (`/api/events/consume/redis-streams/drain`) with cursor/idempotency runtime state
  - added TurboTick optional continuous ingest worker (`TURBOTICK_EVENT_CONSUMER_WORKER_*`) with retry + DLQ handling and worker status endpoint
  - added TurboTick DLQ operator tooling (`/api/events/consume/redis-streams/dlq` + `/api/events/consume/redis-streams/dlq/replay`)
  - added TurboTick integration connector endpoints for secure/monitoring alerts (`/api/integrations/secure/alerts`, `/api/integrations/monitoring/alerts`)
  - added TurboTick external connector onboarding endpoints (`/api/integrations/external/template`, `/api/integrations/external/events`)
  - added TurboTick incident war-room collaboration bridge with RM Meet (`/api/incidents/{id}/war-room/start`, `/api/incidents/{id}/war-room`, `/api/incidents/{id}/war-room/end`)
  - expanded TurboTick API tests to `37` passing (connector templates + connector flows + worker/retry/DLQ + war-room + drain/contract/isolation coverage)
- RM Wallet + RM Dock kickoff started (2026-03-09):
  - added `Wallet/` backend MVP with secret vault, share grants, and reveal controls plus lightweight web UI (`6` tests passing)
  - added `Dock/` backend MVP with app catalog, license assignment, and CARF lifecycle plus lightweight web UI (`6` tests passing)
  - wired Connect command palette/app launcher and Mail integration map to open RM Wallet/RM Dock and create CARF requests
  - upgraded Wallet backend with encrypted-at-rest persistent state + Gate token actor mode (`9` tests passing)
  - upgraded Wallet audit trail with secret access envelope fields (`request_id`, `org_id`, `secret_id`)
  - added Connect + Mail Atlas task-finder (confidence scoring) and thread-to-task conversion web flows
  - shipped Mail compose command bar (`/` + `Cmd/Ctrl+K`) with cross-app Atlas/TurboTick/Wallet/Dock actions
  - shipped Connect composer Atlas live preview cards (in-modal task/project preview + one-click insert)
  - shipped Connect composer smart follow-up assistant baseline for next-action insertion
  - shipped Connect cross-app mention chip baseline (`@task/@project/@doc/@ticket`) with deep-link open behavior
  - shipped Connect contextual reply suggestions (Atlas/TurboTick enriched), thread action timeline, and one-click brief handoff
  - shipped Dock CARF automation baseline to auto-create TurboTick follow-up tickets on approved/provisioned requests
  - shipped Mail parity upgrades for cross-app intelligence: Atlas preview cards, smart follow-up assistant, mention chips with deep links, reader contextual reply suggestions
  - shipped Dock Gate-token auth middleware (`headers|gate|hybrid`) with Gate userinfo validation tests
  - shipped Dock audit event emission for app/license/request flows with `X-Request-Id` correlation
  - recorded interoperability + migration-bridge directive in the hivemind backlog (`docs/specs/orbit-interoperability-migration-bridge-v1.md`)

- Completed runtime availability stabilization pass:
  - Brought Calendar API online under PM2 (`RM Calendar API`, port `5001`)
  - Restored Planet to assigned frontend port `45006` and fixed missing dependency (`react-hot-toast`)
  - Added PM2-managed app processes for Learn (`5180`), Writer UI (`5183`), Writer API (`6011`), Search API (`6200`), and Fonts (`45007`)
  - Validated domain/port routing health for auth/mail/calendar/planet/chat/fonts plus learn/writer/search endpoints
  - Re-ran root gates (`runtime-matrix`, `contract`, `smoke`) successfully after runtime changes
- Completed assigned-port runtime hardening pass (2026-03-03 latest follow-up):
  - added deterministic assigned-port validator (`./assigned-runtime-gate.sh` -> `scripts/verify_assigned_runtime.py`) covering mapped frontend domains plus core backend ports
  - aligned startup/runtime metadata and parser coverage for `Fonts`, `Secure`, and `Capital Hub` in `start-all.sh` + runtime-matrix validation
  - connected Connect Docker backend to internal Redis service (`connect-redis`) and removed container crash loops caused by missing root-level shared scripts
  - patched Snitch TURN startup logging to avoid runtime crash on undefined `server.options` access
  - validation pass:
    - `./assigned-runtime-gate.sh` (pass)
    - `./runtime-matrix-gate.sh` (pass)
    - `./contract-gate.sh` (pass)
- Completed Mail settings realism pass:
  - replaced local-only settings actions with backend endpoints for password change + session revoke
  - added backend tests for settings flows
  - converted mailbox mark-read UI control from toast-only to API-backed behavior
- Completed Mail SSO + settings persistence pass:
  - added real OAuth2 PKCE SSO wiring for Stitch login (`/api/auth/sso/config`, `/api/auth/sso/exchange`)
  - added backend-persisted settings/integration snapshot endpoints (`/api/settings/preferences`, `/api/settings/integrations`)
  - runtime now syncs settings/integrations via backend APIs instead of local-only state
  - normalized SSO error messaging and containerized Gate reachability for Mail backend (`GATE_BASE_URL` + host-gateway mapping in compose)
  - registered Gate `Mail` OAuth client and wired Mail env/client-id config for active SSO config responses
- Completed Atlas dual-lane onboarding hardening pass:
  - personal lane now has live Gate-backed signup/login with strict upstream-status handling (non-2xx responses fail fast)
  - enterprise lane now supports OAuth PKCE end-to-end (`code_challenge` on authorize URL + `code_verifier` on callback token exchange)
  - Atlas now supports public OAuth clients (no client secret required when PKCE verifier is supplied)
  - Atlas local runtime defaults now target local Gate (`http://127.0.0.1:45001`) with JWKS verification enabled by default (`/api/v1/oidc/jwks`)
  - Atlas now auto-discovers `GATE_OAUTH_CLIENT_ID` from `Gate/authx/registered_apps.json` when env is not set
  - added/expanded Atlas tests for onboarding, PKCE callback, public-client verifier enforcement, and upstream redirect/3xx handling (`12` passing auth migration + onboarding tests)
- Completed Atlas onboarding production-policy pass (2026-03-02 latest follow-up):
  - backend now enforces personal-password policy for signup (`12+` chars with upper/lower/digit/symbol) to match UI contract
  - onboarding lane controls are now environment-driven (`ATLAS_PERSONAL_ONBOARDING_ENABLED`, `ATLAS_ENTERPRISE_ONBOARDING_ENABLED`, `ATLAS_ENTERPRISE_SETUP_DOCS_URL`)
  - onboarding config endpoint now reflects runtime lane toggles and enterprise docs URL
  - frontend login now consumes live onboarding config (lane availability + setup docs) instead of hardcoded values
  - enterprise OAuth start path now surfaces backend policy errors directly (no silent fallback bypass for 4xx policy responses)
  - callback page now resolves nested API/OAuth errors into user-readable toasts and clears transient auth state consistently
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`47 passed`)
    - `npm run build` in `Atlas/frontend`
- Completed Atlas Gate-unreachable resilience pass (2026-03-02 latest follow-up):
  - backend auth flows now map Gate transport failures to explicit `502` responses (personal signup/login + enterprise OAuth token exchange)
  - upstream-unreachable responses now return user-actionable details instead of generic internal errors
  - added onboarding regressions for unreachable Gate path handling in signup/login/callback tests
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`50 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas request-tracing + audit observability pass (2026-03-02 latest follow-up):
  - added global backend request middleware to issue/preserve `X-Request-Id` and attach it to all HTTP responses
  - added structured audit envelopes for Atlas backend requests using shared Orbit audit contract (`orbit.audit.atlas`)
  - auth endpoints now emit dedicated `auth.request` audit event category with request metadata
  - added middleware regression tests for request-id propagation and auth audit event emission
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`53 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas auth rollout-safeguards pass (2026-03-02 latest follow-up):
  - added non-secret operational endpoint `GET /api/auth/rollout-status` exposing lane readiness and config diagnostics
  - added fail-fast auth preflight checks so misconfigured personal/enterprise Gate URLs or missing OAuth client now return explicit `503` responses
  - hardened enterprise login-url and callback paths to reject incomplete OAuth rollout config before runtime exchange attempts
  - added regression tests for rollout-status readiness/degraded states and new `503` misconfiguration behavior
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`57 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas login preflight UX pass (2026-03-02 latest follow-up):
  - frontend now consumes `GET /api/auth/rollout-status` in addition to onboarding config to surface lane readiness warnings/errors before user action
  - personal/enterprise login lane selectors now disable when rollout diagnostics indicate configuration is not usable
  - personal sign-up action now blocks when Gate registration endpoint is not configured and surfaces clear guidance
  - login page now renders rollout diagnostics summary panel (issues/warnings) so operators can identify rollout gaps quickly
  - added backend regression for rollout status when both onboarding lanes are disabled
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`58 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas rollout-status strict/probe operations pass (2026-03-02 latest follow-up):
  - `GET /api/auth/rollout-status` now supports:
    - `strict=true` returning `503` when rollout status is degraded (monitoring-friendly)
    - `include_probes=true` adding live Gate endpoint reachability probe snapshots
  - rollout diagnostics now include probe-derived issue codes for unreachable Gate auth/OAuth endpoints (error) and userinfo enrichment reachability (warning)
  - added regressions for strict degraded response, probe payload snapshot, signup preflight register-url guard, and callback preflight token-url guard
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`62 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas rollout diagnostics signal-quality pass (2026-03-02 latest follow-up):
  - rollout status now reports explicit userinfo-endpoint configuration signal (`oidc_userinfo_url_configured`)
  - probe-mode diagnostics now avoid duplicate/unhelpful `*unreachable` issues when endpoints are invalid (configuration errors are reported instead)
  - added targeted regressions for invalid-url probe behavior and degraded rollout issue composition
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`63 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas frontend route code-splitting pass (2026-03-02 latest follow-up):
  - converted Atlas app shell/page imports to lazy route loading (`React.lazy` + `Suspense`) with shared route loader fallback
  - significantly reduced primary frontend bundle footprint (main chunk now ~`232 KB`, no large-chunk warning in build output)
  - retained route/error-boundary semantics while improving initial load performance for production
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`63 passed`)
    - `npm run build` in `Atlas/frontend` (split chunk output verified)
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas FastAPI lifespan startup migration pass (2026-03-02 latest follow-up):
  - replaced deprecated `@app.on_event("startup")` usage with `FastAPI(lifespan=...)` startup lifecycle wiring
  - preserved optional Redis event-consumer boot behavior and non-fatal warning fallback on startup errors
  - added startup lifecycle regressions (`backend/tests/test_startup_lifespan.py`) for disabled/enabled/error-tolerant consumer boot paths
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`66 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas Pydantic-v2 config migration pass (2026-03-02 latest follow-up):
  - migrated schema/router response models from deprecated class-based `Config` to `model_config` (`from_attributes=True`)
  - removed residual Pydantic deprecation warnings in Atlas backend test runs
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`66 passed`, no warnings)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas schema mutable-default safety pass (2026-03-02 latest follow-up):
  - replaced list defaults in task/project/comment/integration schemas with `Field(default_factory=list)` to prevent shared mutable state across model instances
  - ensured request/response payload defaults remain behavior-compatible while improving production safety
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`66 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas OAuth callback state/PKCE hardening pass (2026-03-03 latest follow-up):
  - migrated transient OAuth state/PKCE/redirect values from `localStorage` to `sessionStorage` with backward-compatible local fallback reads during callback handling
  - callback flow now fails closed when expected auth state is missing/mismatched and when PKCE verifier is missing (prevents soft-fallback callback completion)
  - centralized transient auth cleanup to clear both session + legacy local keys on success/failure/logout
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`66 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas enterprise OAuth PKCE enforcement pass (2026-03-03 latest follow-up):
  - backend `/api/auth/orbit-callback` now requires `code_verifier` for all enterprise OAuth callbacks (including confidential-client configuration), eliminating non-PKCE exchange paths
  - callback token exchange payload now always includes the PKCE verifier to align with frontend PKCE login flow
  - expanded onboarding regressions with confidential-client verifier enforcement and updated unreachable/token-endpoint tests under strict PKCE requirement
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`67 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Atlas strict OAuth-init PKCE validation pass (2026-03-03 latest follow-up):
  - backend `/api/auth/orbit-login-url` now enforces:
    - URL-safe state token format (`8-200` chars)
    - required PKCE `code_challenge` (`43-128` base64url chars)
    - `S256` as the only allowed `code_challenge_method`
  - frontend OAuth state generation now uses cryptographically random tokens (with deterministic fallback only when Web Crypto is unavailable)
  - expanded onboarding regressions for missing challenge, invalid state, and rejected `plain` PKCE method
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Atlas/backend` (`70 passed`)
    - `npm run build` in `Atlas/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Gate registration reliability repair:
  - fixed Gate user email-lower index model expression from `lower('email')` to `lower(email)`
  - added startup auto-repair (`repair_users_email_lower_index`) to correct existing DBs without manual SQL
  - added Gate DB repair tests (`tests/test_database_repair.py`)
  - validated Gate + Atlas live flow after repair (Gate register/login pass; Atlas personal signup/login pass)
- Completed Atlas enterprise OAuth callback compatibility pass:
  - Atlas `/auth/orbit-login-url` and `/auth/orbit-callback` now support explicit runtime `redirect_uri` values (validated path + PKCE)
  - Atlas frontend now stores and reuses the exact OAuth redirect URI for callback token exchange to prevent local/domain mismatch failures
  - live enterprise OAuth flow verification completed against Gate (`authorize -> token -> Atlas callback`) with real PKCE verifier and successful Atlas session return
- Completed Gate OAuth org-claim propagation pass:
  - OAuth authorization-code access tokens now include `org_id` (plus profile/email claims when scoped)
  - OIDC userinfo now includes `org_id`
  - OIDC discovery claims list now declares `org_id`
  - added Gate tests `test_oauth_org_claims.py` and validated full suite pass (`16` tests across auth/oauth/repair set)
- Completed Gate role-model hardening baseline:
  - Gate login tokens now include `org_role`, `roles`, and `permissions` claims (plus backward-compatible `role`)
  - refresh-token exchanges now preserve org/role/permission claims in newly minted access tokens
  - OIDC userinfo now includes `org_role`, `roles`, and `permissions`
  - OAuth authorization-code tokens now include role and permission claims
  - live smoke validation confirms role/permission claims in login token + userinfo and successful Atlas enterprise callback compatibility
- Completed Orbit Flow backend baseline (Control Center):
  - added persistent models `FlowRule` and `FlowExecution` (org-scoped)
  - added authenticated tenant-scoped API routes:
    - `GET /api/flows`
    - `POST /api/flows`
    - `PATCH /api/flows/:id`
    - `POST /api/flows/:id/toggle`
    - `POST /api/flows/:id/trigger`
    - `GET /api/flows/executions`
  - role-gated flow management (`admin`/`organizer`) and execution logging now active
  - added service-level tests and included them in Control Center tenant test gate (`11` passing tests total)
- Completed Orbit Pulse executive analytics baseline (Control Center):
  - added authenticated tenant-scoped API route `GET /api/ops/pulse` with admin/organizer role gate
  - added executive KPI aggregation (`meetings`, `actions`, `engagement`, `automation`, `service health`)
  - added trend timelines (14-day meeting and automation runs) and risk radar flags
  - added new frontend `Pulse` view in Control Center sidebar wired to live backend data
  - added `pulseService` contract tests and expanded Control Center tenant test gate (`13` passing tests total)
- Completed cross-app UI/UX modernization sprint baseline (Mail -> Atlas -> Connect -> Meet):
  - Mail frontend now supports real global navigation hotkeys (`I/S/D/T/C` + `/`) and accessible skip-to-content behavior in the stitched runtime shell
  - Atlas layout now includes accessibility skip-link/main landmark wiring, command palette quick access (`/` and `Cmd/Ctrl+K`), and improved Orbit app-switcher links (including `chat.freedomlabs.in`)
  - Connect app now supports fast global search hotkey (`/`) outside typing contexts and includes skip-link/main landmark support for keyboard users
  - Meet lobby now uses live runtime status (online/offline + live clock + current user avatar), supports Enter-to-join, dynamic copyright year, and navigation quick-jump shortcuts (`Alt+1..8`)
  - builds validated for all modernized frontends (`Mail`, `Atlas`, `Connect`, `Meet`)
- Completed post-sprint realism hardening (Meet + Mail):
  - Meet pre-join device check now uses real camera preview and real audio/video input selectors
  - Meet active call startup now honors pre-join media preferences/device IDs for mesh and SFU startup paths
  - Mail stitch runtime now binds mailbox hotkeys directly inside iframe document context (`I/S/D/T/C` + `/`)
  - validated with `node --check` on runtime bridge plus fresh Mail and Meet frontend builds
- Completed host/routing hardening + Mail runtime reliability pass (2026-03-02 follow-up):
  - Added missing Vite `server.allowedHosts` / `preview.allowedHosts` support for `Connect`, `Control Center`, and `Snitch/frontend` (`.freedomlabs.in` + localhost aliases)
  - Added Mail runtime popup-safe integrated app launcher fallback (calendar/chat/connect now fall back to same-tab navigation when popups are blocked)
  - Added Mail inline mailbox chat action (`Chat` on each mailbox card) opening thread-aware in-mail chat drawer
  - Added Mail viewport layout enforcement during runtime boot to mitigate partial/collapsed iframe rendering edge cases
  - validation pass:
    - `npm run build` (`Connect`, `Control Center`, `Mail/frontend`)
    - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail archive/star persistence pass (2026-03-02 latest):
  - added backend flag APIs for email actions:
    - `GET /api/mail/{email_id}/flags`
    - `POST /api/mail/{email_id}/flags`
    - `DELETE /api/mail/{email_id}/flags/{flag}`
  - added backend flag-aware mailbox responses (`flags` array per email) and real archive folder support (`/api/mail/archive`) with archived-email filtering out of inbox/sent/drafts
  - Mail stitched runtime now uses real backend flag endpoints for reader star/unstar and archive/unarchive actions (not local-only toggles)
  - added archive mailbox route support in Mail frontend (`/archive`) and runtime route/link mapping
  - added runtime card badges/actions for starred/archived state and archive/unarchive action from mailbox list
  - backend resiliency hardening:
    - SQLite-safe `body_tsv` fallback in tests/dev (while preserving Postgres `to_tsvector` in production)
    - graceful degradation when Redis rate-limiter infra is unavailable
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Mail/backend` (`24 passed`)
    - `npm run build` in `Mail/frontend`
    - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail consistency hardening pass (2026-03-02 latest follow-up):
  - backend:
    - inbox notification feed now excludes archived emails (consistent with archive mailbox behavior)
    - soft-delete now clears `archived` flag to prevent stale state after move to trash
    - added coverage in `test_mail_flags.py` to assert notification behavior while archived and after restore
  - stitched UI:
    - mailbox cards now support real star/unstar quick action (backend-persisted, not local-only)
    - improved card action wiring to prevent accidental open-thread navigation during star/archive actions
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Mail/backend` (`24 passed`)
    - `npm run build` in `Mail/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail contacts backend persistence pass (2026-03-02 latest):
  - backend:
    - added contact APIs:
      - `POST /api/mail/contacts`
      - `DELETE /api/mail/contacts/{email}`
    - manual contacts are now persisted server-side via tenant/user scoped audit snapshots (`mail.contacts.updated`) and merged into `/api/mail/contacts` results
    - added service-level regression tests for add/list/remove manual contacts
  - stitched UI:
    - contact add flows now persist to backend (utility quick-add, call flow contact prompt, directory new-contact action, search-result inferred sender capture)
    - contact cards now support real remove action with backend delete call + immediate directory refresh
    - retained local fallback behavior when backend/session is unavailable
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Mail/backend` (`25 passed`)
    - `npm run build` in `Mail/frontend`
    - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail trash-restore functionality pass (2026-03-02 latest follow-up):
  - backend:
    - added `POST /api/mail/{email_id}/restore`
    - implemented restore service logic (`deleted_at -> null`) with audit logging (`mail.restore`)
    - added tests covering soft-delete + restore flow and archive-flag cleanup behavior
  - stitched UI/demo runtime:
    - trash mailbox cards now expose real `Restore` action (calls restore endpoint)
    - archive icon navigation now routes to `/archive` (not `/trash`)
    - demo API now supports restore path and preserves previous folder when moving message to/from trash
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Mail/backend` (`26 passed`)
    - `npm run build` in `Mail/frontend`
    - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail stitched-runtime explicit demo opt-in pass (2026-03-03 latest follow-up):
  - runtime bridge demo mode now requires explicit opt-in (`?demo=1` or previously persisted opt-in); default login/runtime behavior remains real backend mode
  - added `?demo=0` override to disable demo opt-in and clear active demo mode state
  - login page no longer auto-prefills demo credentials or renders demo-only sign-in controls unless demo mode is explicitly enabled
  - validation pass:
    - `node --check Mail/stitch_rm_mail_secure_login/runtime-bridge.js`
    - `npm run build` in `Mail/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail backend startup lifespan migration pass (2026-03-03 latest follow-up):
  - replaced deprecated FastAPI `@app.on_event("startup")` usage with app lifespan handler
  - preserved demo-seed bootstrap behavior with explicit coverage for disabled mode, production-blocked mode, and enabled mode
  - added startup regression tests: `Mail/backend/tests/test_lifespan_startup.py`
  - validation pass:
    - `PYTHONPATH=. pytest -q` in `Mail/backend` (`40 passed`)
    - `npm run build` in `Mail/frontend`
    - root gates: `./runtime-matrix-gate.sh`, `./contract-gate.sh`, `./smoke-gate.sh` (all pass)
- Completed Mail repo hygiene baseline pass (2026-03-03 latest follow-up):
  - expanded Mail `.gitignore` to cover generated runtime artifacts (`__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `frontend/dist/`, `*.log`)
  - reduces churn/noise from local test/build runs and keeps production-facing diffs focused on source changes

- Completed ADR contract: `docs/adr/ADR-001-tenant-org-workspace-context.md`
- Completed service-token validation ADR: `docs/adr/ADR-002-service-to-service-token-validation.md`
- Completed tenant-context middleware + tests for:
  - Atlas (FastAPI)
  - Control Center (Express/TS)
  - Calendar (Express)
  - Planet (FastAPI)
  - Connect (Express + Socket.io)
- Completed negative leakage tests in Connect for:
  - HTTP header/token mismatch
  - Socket handshake org mismatch
  - Org-scoped storage and event broadcast checks
- Completed Atlas event-consumer hardening:
  - non-blocking listener path
  - pattern-correct dispatch
  - org-aware event filtering
  - optional startup via `ENABLE_EVENT_CONSUMER`
- Completed cross-service event contract coverage:
  - Calendar publisher now emits org-scoped envelopes (`event_type`, `org_id`, `user_id`, `data`)
  - Planet and Mail publishers now expose normalized envelope builders
  - Connect integration tests validate cross-service event relay remains org-isolated
  - Atlas compatibility tests validate Calendar/Planet/Mail envelope consumption
- Completed Control Center operations dashboard baseline:
  - New backend route `GET /api/ops/overview` with auth + tenant-context enforcement
  - Role-gated visibility (`admin`/`organizer`)
  - Service health probes, event bus snapshot, and scoped runtime metrics
  - Frontend `Operations` view wired into sidebar navigation
  - Added server contract tests for ops metrics + role policy
- Completed Meet backend baseline:
  - New `Meet/server` signaling service (Socket.io) on port `6001`
  - org-scoped signaling relay for offer/answer/ICE messages
  - ICE config endpoint with STUN/TURN env support
  - recording lifecycle APIs (start/stop/list) with tenant enforcement
  - tenant isolation and signaling integration tests
- Completed Meet frontend wiring to backend baseline:
  - Gate OAuth auth context active in `Meet/src`
  - Live lobby route for room code + device preview
  - Active meeting route uses Socket.io signaling + WebRTC peer negotiation
  - Meeting joins now pass token + org context to backend signaling
- Added missing READMEs for Gate, Control Center, Calendar, Planet.
- Added CI workflow for tenant-context contract tests:
  - `.github/workflows/tenant-context.yml`
- Normalized runtime registry:
  - Updated `PORTS.md` with canonical Profile A (`start-all.sh`/`start.sh`) and Profile B (PM2) tables
  - Updated `start-all.sh` port comments/output and added Planet startup (`45006`/`46000`)
- Normalized runtime docs:
  - Updated root `README.md` runtime profile notes and ecosystem status table
  - Updated `Connect/README.md`, `Planet/README.md`, `Snitch/README.md`, and `Mail/README.md` for current ports/profile behavior
- Re-ran tenant/event contract suites (2026-03-01):
  - Atlas `28/28` pass
  - Control Center `6/6` pass
  - Calendar `5/5` pass
  - Planet `6/6` pass
  - Mail `1/1` pass
  - Connect `26 total` pass (`7` skipped)
  - Meet `10 total` pass (`1` skipped)
- Added shared event-envelope fixture pack:
  - `docs/contracts/event-envelope-v1.json` defines canonical cross-service envelopes and expected normalization/rejection outcomes
  - Atlas, Connect, Calendar, Planet, Mail, and Meet now run data-driven contract tests directly from this shared fixture source
- Added unified contract gate command:
  - `./contract-gate.sh` runs envelope contract checks across all active publisher/consumer services
  - `.github/workflows/tenant-context.yml` now includes a `contract-gate` job that executes this root script in CI
- Added runtime matrix drift gate:
  - `./runtime-matrix-gate.sh` validates `PORTS.md` against `start-all.sh` and `ecosystem.config.cjs`
  - `scripts/validate_runtime_matrix.py` also infers implicit backend defaults where PM2 args omit `--port`
  - `scripts/validate_runtime_matrix.py` now also enforces core README runtime/pre-flight token checks
  - `.github/workflows/tenant-context.yml` now includes a `runtime-matrix` job
- Propagated pre-flight gate usage into docs:
  - Root + service READMEs now explicitly instruct contributors to run `./runtime-matrix-gate.sh` and `./contract-gate.sh` before changes/PRs
  - Added `CONTRIBUTING.md` and `.github/pull_request_template.md` so the same gate checks are required in PR workflow
- Expanded cross-app consumer registration coverage:
  - Atlas event consumer now registers handlers for `mail.*`, `planet.*`, `meeting.*`, and `*.activity` (in addition to existing auth/project/calendar)
  - Connect event consumer now subscribes wildcard `*.activity` channel pattern
- Added Atlas durable ecosystem event sink:
  - New model `ecosystem_event_inbox` persists normalized external events (`event_type`, `schema_version`, `org_id`, full payload) for diagnostics and follow-up workflows
  - Event consumer sink failures are non-blocking and covered by tests
  - New Atlas endpoint `GET /api/ecosystem/events` exposes org-scoped consumed event history for runtime validation
  - Added endpoint contract tests covering org scoping, filters, ordering, and pagination
  - Added API-level endpoint tests (`TestClient`) with dependency overrides to validate HTTP behavior end-to-end
  - Added project activity side-effect sink for selected events (`project.*` always; `calendar.*` when `project_id` is present), with org/project/user guard checks
  - Expanded ecosystem compatibility contract tests to include Meet and Connect publisher envelope shapes (with schema-version assertions)
- Expanded Connect runtime relay behavior:
  - Socket relay now emits both `ecosystem_event` (compatibility stream) and typed org-scoped channels based on payload type (e.g. `project_event`, `calendar_event`)
  - Event consumer now classifies domain events (`project.*`, `calendar.*`, `mail.*`, `planet.*`) into typed relay payloads
  - Outbound publisher path now uses shared event envelope builder with normalized `event_type`, `schema_version`, `org_id`, `user_id`, and `data`
- Added explicit event envelope versioning baseline:
  - Calendar, Mail, Planet, Meet, and Connect event publishers now emit `schema_version` (default `1`)
  - Atlas and Connect consumers now normalize missing version to `schema_version=1`
  - Contract tests now validate default/preserved schema version behavior, including shared fixture-pack cases
- Added event idempotency baseline:
  - Publisher envelopes across Calendar/Planet/Mail/Connect/Meet/Snitch/Writer now emit `event_id` (preserve existing or generate fallback)
  - Atlas and Connect consumers now normalize/retain `event_id` for downstream routing
  - Shared fixture-pack contract tests now validate `event_id` presence and preservation
- Added cross-app global search baseline:
  - New contract doc `docs/contracts/global-search-v1.md`
  - New minimal aggregator service `Search/` (FastAPI) with Writer + Learn source adapters
  - Search backend tests and local smoke validation (`Search/backend/tests/test_search_api.py`)
- Added centralized audit-log baseline:
  - Shared Python helper `scripts/orbit_audit.py` and Node helper `scripts/orbit-audit.js`
  - Writer/Search/Meet now emit structured request audit logs with `request_id`, `org_id`, and `workspace_id`
  - Contract reference added at `docs/contracts/audit-log-envelope-v1.md`
- Extended normalized envelope coverage to Snitch prototype publishers:
  - Added shared builder `Snitch/backend/event-envelope.js` and fixture-driven tests (`event-envelope.test.js`)
  - Learn/Capital Hub/Secure prototype services now publish org-scoped envelopes on typed channels plus compatibility `global` channel
  - Shared `tenant-context` middleware now enforces token/header org consistency across Snitch services
  - `Snitch/backend/eventbus.js` now requires authenticated org-scoped publish requests
  - Unified contract gate (`./contract-gate.sh`) and CI workflow now execute Snitch envelope tests (plus tenant-context tests in `snitch` CI job)
- Added service-token validation baseline (JWKS + issuer/audience checks):
  - Added shared Node verifier `scripts/gate-token-verifier.js` used by Connect, Meet, Calendar, and Snitch auth middleware
  - Planet and Mail gate-auth middleware now support optional JWKS verification (`GATE_JWKS_URL`) and enforce configurable issuer/audience claims
  - Atlas auth decode path now enforces configurable issuer/audience claims for accepted tokens
  - Added Planet auth-claim contract tests (`test_gate_auth_claims.py`) covering issuer/audience validation behavior
  - Added ADR-002 reference and service README env guidance for `GATE_JWKS_URL`/`GATE_EXPECTED_ISSUER`/`GATE_EXPECTED_AUDIENCE`
- Added platform unification baseline (`orbit-ui` + Orbit Bar):
  - New shared package source in `orbit-ui/` (`orbit-ui.css`, `orbit-bar.js`)
  - New sync utility `scripts/sync-orbit-ui-assets.sh` to publish shared UI assets/fonts into Meet/Learn/Writer runtime web roots
  - Meet now mounts shared Orbit Bar directly from `Meet/index.html`
  - Learn docs now auto-mount shared Orbit Bar via `Learn/site/assets/learn-nav.js`
  - Writer prototype now mounts shared Orbit Bar via `Writer/code 3.html` (`Writer/site/index.html` generated by `build-site.sh`)
- Added Postgres standardization baseline:
  - Accepted ADR `docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md`
  - Added tenant indexing + partition strategy reference `docs/db/postgres-tenant-partitioning-strategy.md`
  - Writer backend now ships Alembic migration baseline (`Writer/backend/alembic.ini`, `Writer/backend/app/alembic/versions/0001_initial.py`)
  - Root compose now provisions `orbit-postgres` and runs Writer with migration-first startup (`alembic upgrade head` + `WRITER_DB_INIT_MODE=skip`)
- Added shared object-storage baseline:
  - New contract `docs/contracts/object-storage-v1.md` for local + S3-compatible storage
  - Atlas attachments now use pluggable object storage provider (`Atlas/backend/app/services/object_storage.py`) with local/S3 backends
  - Atlas attachment upload/download/delete endpoints now route through storage provider abstraction instead of direct disk coupling
  - Atlas config now includes storage backend envs (`STORAGE_BACKEND`, `STORAGE_BUCKET`, `S3_*`)
- Completed Atlas Gate-token migration baseline:
  - Atlas local `/auth/login` and `/auth/register` endpoints are disabled (SSO-only)
  - Atlas OAuth callback now returns Gate-issued access token (no local token minting)
  - Atlas auth now verifies Gate tokens via JWKS/PEM with controlled HS256 fallback toggle
  - Atlas now JIT-syncs local user/org records from Gate claims (`sub`, `org_id`, profile claims)
  - Atlas frontend login is SSO-only and API client now sends `X-Org-Id`/tenant/workspace context headers from session token
  - Added migration tests for Gate sync paths and disabled-local-auth contract (`Atlas/backend/tests/test_auth_gate_migration.py`)
- Completed Connect Phase-10 hardening baseline:
  - Backend now enforces security middleware stack (Helmet + strict CORS options + rate limits + JSON/upload size limits)
  - Socket and message flows now sanitize identifiers/content before persistence/broadcast (`Connect/server/message-sanitizer.js`)
  - Connect now emits structured audit logs for HTTP and socket actions (`Connect/server/audit-middleware.js`)
  - Frontend received a11y/perf baseline updates:
    - lazy-loaded overlay components in app shell
    - dialog semantics + aria labels on core modal/nav controls
    - sign-out wiring in profile/settings menus
  - Added hardening tests:
    - `Connect/server/security-config.test.js`
    - `Connect/server/message-sanitizer.test.js`
    - `Connect/server/audit-middleware.test.js`
- Completed Mail Gate-boundary + tenant controls baseline:
  - Mail auth dependency now supports Gate-token fallback with optional `X-Org-Id` consistency enforcement
  - Gate claims (`sub`, `org_id`) now JIT-provision tenant/user/mailbox records (`org::<org_id>` tenant mapping)
  - Added admin tenant operational-control APIs:
    - `GET /api/admin/tenant-controls`
    - `POST /api/admin/retention/apply`
  - Added focused Mail tests:
    - `backend/tests/test_deps_auth_context.py`
    - `backend/tests/test_admin_service.py`
    - SQLite test fixture now compiles Postgres `TSVECTOR` as `TEXT` in tests
- Completed Meet production video path baseline:
  - Added media session contract endpoint `GET /api/meetings/:meetingId/media-session` with mode resolution (`mesh` default, `livekit` SFU support)
  - Added TURN credential baseline supporting static credentials and ephemeral shared-secret mode
  - Added room participant visibility endpoint `GET /api/meetings/:meetingId/participants`
  - Meet frontend now resolves media mode at join and supports LiveKit SFU connection flow with mesh fallback
  - Added backend coverage for media session contracts and participant tracking behavior:
    - `Meet/server/media-session.test.js`
    - expanded `Meet/server/signaling-runtime.integration.test.js`
- Started cross-app UI/UX modernization track with a major Mail frontend refresh:
  - Replaced placeholder shell with responsive productivity layout (workspace topbar, folder nav, split-view inbox, compose/search/admin/settings experiences)
  - Added richer interaction states (priority badges, toolbar actions, keyboard-accessible search shortcut, responsive mobile collapse)
  - Mail demo runtime now aligned to assigned frontend port `45004` with collision-safe backend mapping for local ecosystem demos
  - Mail frontend now serves exact approved Stitch UI screens from `Mail/stitch_rm_mail_secure_login` with explicit route mapping (`/login`, `/inbox`, `/drafts`, `/compose`, `/settings/*`, `/reader`)
  - Added shared Stitch runtime bridge to make approved Mail screens real (live auth, mailbox list loading, thread reader, compose/reply, search, settings persistence) without redesigning templates
- Completed Capital Hub backend MVP baseline (prototype graduation target):
  - `Snitch/backend/capitalhub-service.js` now provides org-isolated asset ledger, lifecycle transitions, renewal queue/renew execution, and financial overview APIs
  - Added mutation event publishing on `capitalhub.asset.created`, `capitalhub.ledger.entry_added`, `capitalhub.lifecycle.updated`, and `capitalhub.renewal.completed`
  - Added service tests `Snitch/backend/capitalhub-service.test.js` and included them in `npm test`
  - Updated `tenant-context` CI workflow `snitch` job to install dependencies and run full Snitch backend test suite
- Completed Secure backend MVP baseline (prototype graduation target):
  - `Snitch/backend/secure-service.js` now provides org-isolated endpoint inventory, vulnerability lifecycle APIs, scanner-ingest baseline, and risk overview metrics
  - Added mutation event publishing on `secure.endpoint.registered`, `secure.endpoint.updated`, `secure.vulnerability.detected`, `secure.vulnerability.updated`, `secure.vulnerability.remediated`, and `secure.scan.ingested`
  - Added service tests `Snitch/backend/secure-service.test.js` and included them in `npm test`
  - Snitch backend package/runtime now includes valid installable dependency pin for `node-turn` (`^0.0.6`)

## 1) Sources Reviewed

README files reviewed:
- `README.md` (root)
- `Atlas/README.md`
- `Connect/README.md`
- `Mail/README.md`
- `Learn/README.md`
- `Secure/README.md`
- `Capital Hub/README.md`
- `Snitch/README.md`
- `Meet/README.md`
- `Meet/meet-app/README.md`
- `RM Fonts/RM Fonts/README.md`
- `RM Fonts/manrope/README.md`

Existing backlog files found:
- `Connect/todo.txt`
- `Control Center/todo.txt`
- `PRODUCTION_PLAN.md`

## 2) Current State (From Docs)

- Core ecosystem foundation is documented as available: Gate SSO, PKCE flow, JWT verification, Redis event bus, and org header propagation.
- `Learn`, `Capital Hub`, and `Secure` are still prototype-stage services (mainly via `Snitch`).
- `Meet` is in progress. Scheduling/workflow exists, but live video stack is still pending integration.
- `Mail` has a strong backend baseline and clear scale path.
- `Connect` has a near-complete feature set with a remaining production hardening backlog.

Documentation gaps:
- README coverage exists for `Gate`, `Control Center`, `Calendar`, and `Planet`.
- Runtime drift across `PORTS.md`/startup scripts/active service READMEs is now gated.
- Remaining gap is legacy narrative doc overlap and stale status wording outside active runtime docs.

## 3) Existing Todo Items Already Documented

From `Snitch/README.md`:
- Replace scaffolds with full business logic.
- Real OAuth clients in frontends.
- Shared design system package.
- CI/CD + production orchestration.

From `Connect/todo.txt`:
- Security hardening (rate limits, sanitization, headers, CORS).
- Admin/audit, accessibility, performance, push notifications, tests, CI/CD.

From `Control Center/todo.txt` (Meet area):
- WebRTC signaling.
- SFU for multi-party meetings.
- `/room/:id` live video UI.
- TURN/STUN production networking.

From `Mail/README.md`:
- RM Auth SSO integration.
- Async worker pipeline, search upgrades, cache strategy, tenant-scale operations.

## 4) Consolidated Priority Todo List

### P0 - Multi-Enterprise Architecture Contract (Must-Do First)
- [x] Define canonical tenancy model and terminology:
  - `tenant` (enterprise account boundary)
  - `org` (division/unit within tenant)
  - `workspace` (app-level collaboration boundary, if needed)
- [x] Publish mandatory request context contract for all services:
  - JWT claims (`sub`, `tenant_id`, `org_id`, `roles`, `permissions`)
  - Header usage (`x-org-id`) and validation rules
- [x] Add shared tenant-context middleware/libs for FastAPI and Express.
- [x] Add cross-tenant isolation tests (negative tests included) as a release gate.
- [x] Define service-to-service auth standard (JWKS + service audience checks).

### P1 - Platform Unification
- [x] Create shared UI package (`orbit-ui`) with fonts/tokens/components used by all apps.
- [x] Implement global workspace shell ("Orbit Bar"): app launcher + identity menu + org switcher.
- [x] Implement cross-app global search API contract and minimal aggregator service (`docs/contracts/global-search-v1.md` + `Search/` service baseline).
- [x] Enforce common event schema versioning and event idempotency policy (`docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md` + fixture-driven `event_id` contract checks in `contract-gate.sh`).
- [x] Centralize structured audit logs with tenant/org correlation IDs (`docs/contracts/audit-log-envelope-v1.md` + shared helpers in `scripts/orbit_audit.py` and `scripts/orbit-audit.js`, adopted by Writer/Search/Meet).

### P1 - Product Alignment (Highest Impact Apps First)
- [x] Atlas: migrate fully to Gate-issued tokens and tenant/org scoped access checks everywhere.
- [x] Connect: finish Phase 10 hardening (security, a11y, performance, audit logs).
- [x] Mail: complete Gate SSO boundary integration and tenant-scale operational controls.
- [x] Meet: implement production video path (signaling + SFU + TURN + room UI).

### P2 - Prototype Graduation (Snitch -> First-Class Apps)
- [x] Learn: move from content concept to versioned docs platform MVP (static docs portal delivered at `Learn/` on port `5180`).
- [x] Writer: onboard standalone UI + backend baseline (`Writer/`, ports `5183` / `6011`), add live document/block/version UI wiring, add optional Gate-compatible JWT API enforcement, and publish normalized writer events with fixture-driven contract coverage.
- [x] Capital Hub: implement ledger + lifecycle + renewal MVP with tenant/org isolation.
- [x] Secure: implement endpoint inventory + vulnerability baseline MVP.
- [x] Define graduation checklist for any prototype (`docs/PROTOTYPE_GRADUATION_CHECKLIST.md`):
  - Auth compliance
  - Tenant isolation tests
  - Event contract compliance
  - Observability and runbooks

### P2 - Operations and Reliability
- [x] Run cross-app UI/UX modernization sprint (Mail -> Atlas -> Connect -> Meet):
  - align each app to shared Orbit visual system + responsive behavior
  - replace placeholder views with production-quality task flows
  - add a11y/keyboard/navigation standards and interaction consistency checks
- [x] Add unified root orchestration (`docker-compose.orbit.yml` baseline + `compose-up.sh` / `compose-down.sh`).
- [x] Standardize on Postgres (migrations, tenant-aware indexing/partitioning strategy).
- [x] Move attachments/files to shared S3-compatible object store.
- [x] Add CI pipelines with contract tests and integration smoke tests (`.github/workflows/tenant-context.yml` + `smoke-gate.sh`).

### P2 - Interoperability + Migration Bridge (Directive 2026-03-09)
- [ ] Publish connector + migration architecture contract:
  - canonical object mapping for `project/task/thread/ticket/user/team`
  - lifecycle modes: `import_once`, `dual_sync`, `orbit_authoritative`
- [ ] Build Integration Hub baseline:
  - connector registry + credential profiles + health probes
  - first-party connectors (Jira, Slack, Google Workspace baseline)
- [ ] Build Migration Bridge baseline:
  - dry-run validation + mapping preview + idempotent replay
  - pause/resume/rollback checkpoints with audit envelopes
- [ ] Add cross-app migration continuity checks:
  - preserve relationship graph (`ticket <-> task <-> thread <-> incident`)
  - enforce tenant/org/workspace isolation in all migration jobs

### P3 - Enterprise Completeness
- [x] Enrollment model implementation in Gate (personal vs enterprise).
- [x] Role model hardening (RBAC -> policy-driven authorization where required).
- [x] Cross-app workflow automation engine (Orbit Flow concept).
- [x] Executive analytics hub for tenant-level operations (Orbit Pulse concept).
- [x] Control Center time cards module (no new app):
  - [x] employee time card submit/edit lifecycle (`Draft -> Submitted`)
  - [x] manager approval lifecycle (`Approved/Rejected`)
  - [x] tenant-aware time-card summary reporting (`/api/time-cards/summary`)
  - [x] audit event envelopes for time-card actions
  - [x] reporting by department/cost-center dimensions
  - [x] integration hooks to TurboTick for approval SLA reminders

### P4 - Cross-App Intelligence + Ticketing (Requested 2026-03-09)
- Governance note:
  - Expansion freeze applies to new major applications outside the current app set.
  - RM People remains a deferred scoped proposal only and must not start implementation until production-readiness gates are passed.
- [ ] Feature 1: Atlas Smart Insert in compose/chat context menu:
  - [x] web: right-click context menu action (Mail compose + Connect composer/message)
  - [ ] iOS/Android: long-press action sheet parity
  - [x] include "Ask Atlas" one-click lookup with non-AI fallback to deterministic search
- [x] Feature 2: Universal command bar (`/` + `Cmd/Ctrl+K`) in compose/chat for Atlas/CRM/files/tickets insertion.
  - web baseline active in Connect command palette (Atlas ask/insert + TurboTick + Wallet + Dock actions)
  - Mail compose command bar shipped with Atlas/TurboTick/Wallet/Dock actions and insertion shortcuts
- [x] Feature 3: AI task finder that resolves natural-language queries to task IDs with confidence score.
  - deterministic web baseline shipped in Connect command palette + composer context menu and Mail compose smart menu
  - AI-provider scoring upgrade remains optional follow-up via AI adapter
- [x] Feature 4: Thread-to-task conversion flow for Mail/Connect threads.
  - Connect message context menu now supports "Convert to Atlas task"
  - Mail reader overflow menu now supports "Convert Thread to Atlas Task"
- [ ] Feature 5: Live task preview cards in compose/chat without route switch.
  - web baseline shipped in Connect composer + Mail compose smart menu (`Preview Atlas matches` modal cards + one-click insert)
  - iOS/Android parity + richer card metadata pending
- [ ] Feature 6: Smart follow-up assistant for reminders and suggested next actions.
  - web baseline shipped in Connect composer + Mail compose (`Follow-up Suggestions` deterministic assistant)
  - AI-enhanced suggestion mode + iOS/Android parity pending
- [ ] Feature 7: Cross-app mention chips (`@task`, `@project`, `@doc`, `@ticket`) with deep links.
  - web baseline shipped in Connect + Mail compose/reader (`@task(...)`, `@project(...)`, `@doc(...)`, `@ticket(...)` insertion + click-through deep links)
  - richer chip UX + iOS/Android parity pending
- [ ] Feature 8: Contextual reply suggestions enriched with Atlas/TurboTick status.
  - web baseline shipped in Connect composer + Mail reader (`Context Reply Suggestions`) with Atlas + TurboTick enrichment
  - iOS/Android parity pending
- [ ] Feature 9: Action timeline side panel aggregating blockers/updates for the active thread.
  - web baseline shipped in Connect thread right panel + Mail reader thread card (`Action Timeline`) with blocker/status/reference aggregation
  - cross-app rollup + iOS/Android parity pending
- [ ] Feature 10: One-click brief generator (thread digest -> Atlas/wiki/ticket update).
  - web baseline shipped in Connect thread panel + Mail reader timeline card and reader menu (`Generate Thread Brief`)
  - Wiki/Docs publish target + iOS/Android parity pending
- [ ] TurboTick tool (new app) delivery baseline:
  - [x] create `TurboTick/` app scaffolding + README + todo backlog
  - [x] define ticketing contract (ticket, queue, SLA, assignee, comment, attachment, links)
  - [x] implement MVP web + API
  - [x] implement auth modes (`headers|gate|hybrid`) with Gate userinfo actor resolution
  - [x] implement event producer baseline (`/api/events` + optional sink webhook)
  - [x] implement durable publish transport baseline (`redis_streams`)
  - [x] implement event consumer API baseline (`/api/events/consume`) for intake/status sync
  - [x] implement operator-triggered durable ingress drain endpoint (`/api/events/consume/redis-streams/drain`) with cursor/idempotency state
  - [x] implement optional continuous ingress worker + retry/DLQ with status endpoint (`/api/events/consume/worker/status`)
  - [x] implement DLQ visibility + replay endpoints (`/api/events/consume/redis-streams/dlq`, `/api/events/consume/redis-streams/dlq/replay`)
  - [x] implement integration connectors for secure + monitoring alerts
  - [x] implement external connector template + ingest endpoints for custom sources
  - [x] implement RM Meet incident war-room bridge endpoints + event/timeline hooks
  - [x] define iOS/Android parity scope and mobile quick-action UX (`docs/specs/mobile-parity-cross-app-intelligence-v1.md`)
  - connect Mail/Connect/Atlas intake and status sync over continuous durable event-bus consumers (deeper connector wiring pending)
- [ ] RM Wallet app delivery baseline:
  - [x] create `Wallet/` app scaffolding + README + todo backlog
  - [x] implement MVP backend API (secrets + shares + reveal + org isolation tests)
  - [x] implement lightweight web baseline (create/list/reveal/share)
  - [x] implement Gate JWT + encrypted persistent vault storage
  - [x] implement secret audit envelope fields (`request_id`, `org_id`, `secret_id`)
  - [ ] implement web + mobile UX parity for secure reveal/share workflows
- [ ] RM Dock app delivery baseline:
  - [x] create `Dock/` app scaffolding + README + todo backlog
  - [x] implement MVP backend API (catalog + licenses + assignments + CARF lifecycle)
  - [x] implement lightweight web baseline (catalog + CARF + request state updates)
  - [x] implement Gate JWT middleware modes (`headers|gate|hybrid`) with tests
  - [x] emit dock audit events (`dock.app.*`, `dock.license.*`, `dock.request.*`) with request correlation
  - [ ] implement web + mobile UX parity for procurement/assignment operations
  - [x] add cross-functional CARF automation into Atlas/TurboTick workflows (TurboTick ticket automation + Atlas handoff hint baseline)

## 5) Execution Plan (Phased)

## Phase 0 (Week 1): Contract First
Goal: freeze architecture rules before adding features.
- Deliverables:
  - Tenancy and auth ADR document.
  - Shared request context contract.
  - Isolation test blueprint used by all services.
  - Missing READMEs for Gate/Control Center/Calendar/Planet.

Exit criteria:
- No service can merge code without tenant-context compliance checks.

## Phase 1 (Weeks 2-3): Identity + Isolation Rollout
Goal: enforce tenant/org guarantees in live services.
- Deliverables:
  - Shared middleware packages (FastAPI + Express).
  - Atlas + Connect migrated and passing isolation suite.
  - Service auth audience validation in place.

Exit criteria:
- Cross-tenant access attempts fail consistently in automated tests.

## Phase 2 (Weeks 4-6): Workspace Unification
Goal: make apps feel like one workspace.
- Deliverables:
  - `orbit-ui` package integrated baseline in Meet/Learn/Writer (rollout to Atlas/Connect/Mail pending in product-specific tracks).
  - Orbit Bar with org switch + app launcher.
  - Cross-app search MVP.
  - Centralized audit/trace pipeline.

Exit criteria:
- Users can switch apps/orgs without re-auth and preserve workspace context.

## Phase 3 (Weeks 7-10): Product Maturity
Goal: graduate in-progress/prototype products.
- Deliverables:
  - Meet live video stack operational.
  - Capital Hub/Secure/Learn MVPs with real backend logic.
  - Mail SSO and scale baseline complete.

Exit criteria:
- All core products meet auth/isolation/event/observability gate.

## Phase 4 (Weeks 11-12): Production Hardening
Goal: prepare for multi-enterprise scale.
- Deliverables:
  - Unified deployment topology and runbooks.
  - CI/CD with integration test gates.
  - Postgres + object storage production migration plan.

Exit criteria:
- Repeatable, monitored, rollback-safe releases across ecosystem.

## Phase 5 (Weeks 13-16): Contextual Intelligence + Workflow Ops Launch
Goal: turn cross-app collaboration into one-click workflows and ship TurboTick + RM Wallet + RM Dock MVPs.
- Deliverables:
  - Atlas Smart Insert context actions live in Mail + Connect on web and mobile parity specs complete.
  - TurboTick backend + web MVP live with Gate auth, org isolation, and audit/event contracts.
  - RM Wallet backend + web MVP live with Gate auth, encrypted secret storage, and permissioned share controls.
  - RM Dock backend + web MVP live with catalog/license/CARF workflows and assignment controls.
  - Mail/Connect/Atlas ticket intake and status sync active with traceable events.
  - CARF approvals and secure-share actions can trigger Atlas/TurboTick follow-up tasks with traceable events.
  - Mobile quick actions (`long-press -> create/link ticket`) implemented for iOS/Android clients.

Exit criteria:
- Users can create, triage, and link tickets plus request/provision software and manage secure secrets without app switching, with org-safe audit/event traces.

## 6) Proposed First Implementation Slice (After Approval)

1. Create architecture ADR for tenant/org/workspace contract.
2. Implement shared tenant-context middleware for one FastAPI service and one Express service.
3. Add isolation tests for both pilots.
4. Fill missing READMEs for Gate/Control Center/Calendar/Planet with run/auth/integration details.

No feature implementation should begin before these four items are accepted.

## 7) Immediate Kickoff Slice (2026-03-09)

1. Add `TurboTick/README.md` and `TurboTick/todo.txt` as the canonical product backlog anchors.
2. Reserve frontend/backend runtime ports for TurboTick in `PORTS.md`.
3. Add TurboTick system role + connectors in `ECOSYSTEM_BLUEPRINT.md`.
4. Add cross-app intelligence + ticketing backlog items (web + iOS + Android parity) to this plan.
5. Add `Wallet/README.md` + `Wallet/todo.txt` and ship backend MVP (`secrets + sharing + reveal`).
6. Add `Dock/README.md` + `Dock/todo.txt` and ship backend MVP (`catalog + licenses + CARF`).
7. Reserve frontend/backend runtime ports for RM Wallet and RM Dock in `PORTS.md`.
8. Add RM Wallet/RM Dock connectors and execution backlog scope to the ecosystem blueprint and plan.
