# RM Orbit: The Unified Enterprise Ecosystem 🌌

RM Orbit is a comprehensive, interconnected suite of applications designed to serve both individual power users and large-scale enterprises. It provides a seamless experience for project management, communication, financial tracking, and security operations.

## 🚀 Core Features (Phase 1 Complete, Phase 1.5 In Progress)

✅ **Unified SSO** - Gate/AuthX OAuth2 with RS256 JWT across all apps  
✅ **Multi-Tenancy** - Organization isolation via X-Org-Id header  
✅ **Event Bus** - Redis pub/sub for cross-service communication  
✅ **Service Auth** - Token verification (RS256 + HS256 fallback)  
✅ **PKCE Flow** - Secure OAuth implementation for all frontends  
✅ **Workspace Shell** - Shared Orbit Bar (`orbit-ui`) with app launcher + org switcher + identity menu  
✅ **Object Storage Baseline** - Shared local/S3 contract with Atlas+Mail provider abstractions  
✅ **Atlas Gate-Only Auth** - Atlas local login/register removed; Gate-issued token path + org-header propagation active  
✅ **Connect Hardening Baseline** - Security middleware, structured audit logs, and message sanitization active  
✅ **Mail Gate Boundary Baseline** - Gate-token fallback with org consistency checks plus tenant operational-control endpoints active  
✅ **Meet Production Video Baseline** - Signaling + TURN credentialing + LiveKit SFU media-session path + room UI active  

## 📱 The Application Suite

| App | Status | Auth | Events |
|-----|--------|------|--------|
| **Atlas** | ✅ Online | Gate SSO + RS256 JWT | Published |
| **Calendar** | ✅ Online | RS256 JWT | Published |
| **Control Center** | ✅ Online | PKCE OAuth | Consuming |
| **Connect** | ✅ Online | JWT + Socket.io | Published + Consuming |
| **Gate (AuthX)** | ✅ Online | Provider | N/A |
| **Learn** | ✅ Docs Portal Online + Prototype Backend | JWT | Published |
| **Search** | ✅ Aggregator Baseline | Optional headers (`X-Org-Id`, `X-Workspace-Id`) | Aggregating |
| **Capital Hub** | 🔄 Prototype (Snitch) | JWT | Published |
| **Secure** | 🔄 Prototype (Snitch) | JWT | Published |
| **Meet** | ✅ Production Video Baseline | JWT + Socket.io + LiveKit SFU path | Published |
| **Writer** | ✅ UI + Backend Baseline (Live Docs/Blocks/Versions) | ✅ Optional Gate JWT | ✅ Published (backend baseline) |
| **Planet** | ✅ Online (Baseline) | PKCE + RS256 JWT | Published |
| **Mail** | ✅ Online | Gate SSO boundary + RS256/JWKS | Publishing |
| **TurboTick** | 🧱 MVP Web + Backend Baseline | Gate SSO + RS256 JWT (planned) | Published + Consuming (planned) |
| **RM Wallet** | 🧱 MVP Web + Backend Baseline | Gate SSO + RS256 JWT (planned) | Published (planned) |
| **RM Dock** | 🧱 MVP Web + Backend Baseline | Gate SSO + RS256 JWT (planned) | Published + Consuming (planned) |

### 🚧 Prototypes & `Snitch`  
Early‑stage apps are bootstrapped in `Snitch/` with shared org/auth middleware and Redis event publishing. Learn now has a dedicated docs portal (`Learn/`, port `45009`) while its prototype backend service remains in Snitch (`6002`) until backend graduation. Writer now has a dedicated runnable UI + FastAPI backend baseline in `Writer/` on ports `45010` and `6011`.

## 🎨 Design System & Experience

All apps in the Orbit ecosystem adhere to a consistent UI/UX language to ensure users feel "at home" regardless of which tool they are using.

### Typography
- **Primary Header Font**: `RM Samplet`
- **Secondary/Body Font**: `RM Forma`
- *Consistent use of weights and spacing across all platforms.*

### Shared UI Package
- **`orbit-ui/`** is the shared source for cross-app shell/tokens:
  - `orbit-ui/orbit-ui.css` (fonts + design tokens + shell styles)
  - `orbit-ui/orbit-bar.js` (global Orbit Bar custom element)
- `scripts/sync-orbit-ui-assets.sh` publishes the shared bundle + fonts into active frontend runtime roots (Meet/Learn/Writer/Atlas/Connect/Mail/Calendar/Planet/Control Center/Secure/Capital Hub/TurboTick/RM Wallet/RM Dock/Snitch).

### User Experience
- **User-Based Views**: Dashboards adapt based on the user's role and enrollment type.
- **Micro-Animations**: Purposeful transitions that enhance the "premium" feel.
- **Glassmorphism**: Subtle use of transparency and blur to create depth.

## 📚 Documentation & Architecture

### Quick Start
- **[PORTS.md](PORTS.md)** - All service ports and endpoints
- **[ECOSYSTEM_BLUEPRINT.md](ECOSYSTEM_BLUEPRINT.md)** - System architecture overview
- **[PRODUCTION_PLAN.md](PRODUCTION_PLAN.md)** - Deployment checklist
- **[AGENT_HANDOFF_2026-03-01.md](AGENT_HANDOFF_2026-03-01.md)** - Current execution handoff and verified test status
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Required pre-flight gates and PR expectations
- **[docs/adr/ADR-002-service-to-service-token-validation.md](docs/adr/ADR-002-service-to-service-token-validation.md)** - JWKS + issuer/audience service-token contract
- **[docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md](docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md)** - Envelope versioning + `event_id` idempotency contract
- **[docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md](docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md)** - Postgres standard + migration + tenant-indexing contract
- **[docs/adr/ADR-005-writer-feedback-persistence-model.md](docs/adr/ADR-005-writer-feedback-persistence-model.md)** - Writer feedback durability and workspace-summary query model
- **[docs/db/postgres-tenant-partitioning-strategy.md](docs/db/postgres-tenant-partitioning-strategy.md)** - Tenant-aware indexing and partitioning thresholds
- **[docs/PROTOTYPE_GRADUATION_CHECKLIST.md](docs/PROTOTYPE_GRADUATION_CHECKLIST.md)** - Mandatory gate checklist for promoting prototype services
- **[docs/contracts/global-search-v1.md](docs/contracts/global-search-v1.md)** - Cross-app global search API contract
- **[docs/contracts/audit-log-envelope-v1.md](docs/contracts/audit-log-envelope-v1.md)** - Structured audit log contract (`request_id` + org/workspace correlation)
- **[docs/contracts/object-storage-v1.md](docs/contracts/object-storage-v1.md)** - Shared local/S3 object-storage contract
- **[orbit-ui/README.md](orbit-ui/README.md)** - Shared UI package and Orbit Bar usage
- **[docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md](docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md)** - Product governance freeze policy and RM People scoped proposal
- **[docs/specs/orbit-interoperability-migration-bridge-v1.md](docs/specs/orbit-interoperability-migration-bridge-v1.md)** - External-app connector and migration-bridge directive for enterprise onboarding
- **Pre-flight validation gates**:
  - `./assigned-runtime-gate.sh` (live assigned-port runtime validation)
  - `./runtime-matrix-gate.sh`
  - `./contract-gate.sh`
  - `./smoke-gate.sh` (integration smoke baseline for Writer + Meet runtime)

### Local Runtime Profiles
- `./start-all.sh` uses per-service scripts and Docker where configured.
- `pm2 start ecosystem.config.cjs` uses a separate PM2-oriented dev profile.
- `docker compose -f docker-compose.orbit.yml up --build -d` provides a root compose baseline (Postgres + Redis + Writer + Meet + Learn + Search).
- Root compose now includes Postgres baseline for Writer migrations/runtime (`orbit-postgres` on `55432`).
- `PORTS.md` documents both profiles as canonical reference.

### Authentication & Security
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Phase 1 completion report
- **[AUTH_SECURITY.md](AUTH_SECURITY.md)** - OAuth2/OIDC flows and JWT verification
  - RS256 token signing & verification
  - PKCE implementation for web clients
  - Multi-tenant enforcement patterns
  - Token refresh strategy
  
- **[EVENT_SCHEMA.md](EVENT_SCHEMA.md)** - Event bus structure and integration
  - All event types (auth, project, calendar, mail, meeting, user, org)
  - Redis Pub/Sub channels
  - Event consumer examples (Node.js, Python)
  - Best practices for event handling

- **[INTEGRATION_TESTING.md](INTEGRATION_TESTING.md)** - End-to-end testing procedures
  - 7 complete test scenarios
  - OAuth flow validation
  - Token verification
  - Event bus testing
  - Multi-tenancy enforcement
  - Troubleshooting guide

## 🏢 Enrollment Models

### Personal Enrollment
- Focused on individual productivity.
- Simplified views of Capital Hub for personal wealth and gadgets.
- Direct access to Atlas for personal projects.

### Enterprise Enrollment
- Hierarchical structure with Organizations, Departments, and Teams.
- Advanced features in Secure (Fleet management) and Capital Hub (Budgets/Procurement).
- Centralized billing and audit logs in Gate.

---
"One Ecosystem. Infinite Possibilities."
