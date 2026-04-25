# RM Orbit Documentation Index

Welcome to the RM Orbit ecosystem! This index helps you find the documentation you need.

---

## 🎯 **Start Here** (First Time?)

1. **[README.md](README.md)** - Ecosystem overview and app status
2. **[DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md)** - 5-minute quick start
3. **[PORTS.md](PORTS.md)** - Where each service runs
4. **[docker-compose.orbit.yml](docker-compose.orbit.yml)** - Root Docker Compose baseline (Postgres + Redis + Writer + Meet + Learn + Search)
5. **[orbit-ui/README.md](orbit-ui/README.md)** - Shared UI package + Orbit Bar shell contract
6. **[docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md](docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md)** - Product governance freeze + RM People scoped proposal
7. **[docs/specs/mobile-parity-cross-app-intelligence-v1.md](docs/specs/mobile-parity-cross-app-intelligence-v1.md)** - iOS/Android parity scope for Mail/Connect/TurboTick/Wallet/Dock
8. **[docs/specs/orbit-interoperability-migration-bridge-v1.md](docs/specs/orbit-interoperability-migration-bridge-v1.md)** - External-app connector and platform migration-bridge directive

---

## 🔐 **Authentication & Security**

### For Developers
- **[AUTH_SECURITY.md](AUTH_SECURITY.md)** - Complete guide (2,500 lines)
  - OAuth2/OIDC PKCE flow with diagrams
  - JWT token generation & RS256 verification
  - Multi-tenant enforcement patterns
  - Token refresh implementation
  - Service-to-service auth
  - Security best practices
  - Environment variable setup
  - Troubleshooting guide
- **[docs/adr/ADR-002-service-to-service-token-validation.md](docs/adr/ADR-002-service-to-service-token-validation.md)** - Accepted JWKS + issuer/audience service-token validation standard
- **[docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md](docs/adr/ADR-003-event-envelope-versioning-and-idempotency.md)** - Accepted event envelope versioning + idempotency (`event_id`) policy
- **[docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md](docs/adr/ADR-004-postgres-standardization-and-tenant-indexing.md)** - Accepted Postgres + migration + tenant-indexing baseline
- **[docs/contracts/audit-log-envelope-v1.md](docs/contracts/audit-log-envelope-v1.md)** - Shared structured audit-log envelope (`request_id`, `org_id`, `workspace_id`)
- **[docs/contracts/object-storage-v1.md](docs/contracts/object-storage-v1.md)** - Shared attachment/file storage contract (local + S3-compatible)
- **[docs/db/postgres-tenant-partitioning-strategy.md](docs/db/postgres-tenant-partitioning-strategy.md)** - Tenant-aware indexing and partitioning thresholds

### For DevOps  
- **[PRODUCTION_PLAN.md](PRODUCTION_PLAN.md)** - Deployment checklist
  - Pre-deployment verification
  - Key rotation procedures
  - Production configuration
  - Monitoring & alerting setup

---

## 📡 **Events & Integration**

### For Developers
- **[EVENT_SCHEMA.md](EVENT_SCHEMA.md)** - Event catalog (1,000 lines)
  - auth.* events (login, logout)
  - project.* events (create, update, delete)
  - calendar.* events (event actions)
  - mail.* events (send, receive, attachments)
  - meeting.* events (schedule, start, end)
  - user.* events (create, update, delete)
  - org.* events (member management)
  - Redis channel mapping
  - Consumer code examples
  - Publishing patterns

### For Architects
- **[ECOSYSTEM_BLUEPRINT.md](ECOSYSTEM_BLUEPRINT.md)** - System design
  - App interconnections
  - Data flow diagrams
  - Service boundaries
  - Technology choices

---

## 🧪 **Testing & Validation**

### For QA & Developers
- **[INTEGRATION_TESTING.md](INTEGRATION_TESTING.md)** - Test procedures (800 lines)
  - **Test 1:** OAuth2 PKCE flow
  - **Test 2:** Backend JWT verification
  - **Test 3:** Multi-tenancy enforcement
  - **Test 4:** Redis event bus
  - **Test 5:** Event consumer
  - **Test 6:** Token refresh
  - **Test 7:** Cross-service calls
  - Automated test examples
  - Troubleshooting guide
  - Success criteria checklist
- **[smoke-gate.sh](smoke-gate.sh)** - Runtime integration smoke baseline (Writer + Meet)
- **[scripts/sync-orbit-ui-assets.sh](scripts/sync-orbit-ui-assets.sh)** - Sync shared Orbit UI assets/fonts into Meet/Learn/Writer runtimes

---

## 📊 **Status Reports**

### Phase 1 Completion
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What's built (5,000 lines)
  - Phase 1 objectives (all ✅ complete)
  - Architecture details
  - File inventory
  - Service status matrix
  - Security implementation
  - Validation checklist
  - Known limitations
  - Phase 2 roadmap

### Prototype Promotion
- **[docs/PROTOTYPE_GRADUATION_CHECKLIST.md](docs/PROTOTYPE_GRADUATION_CHECKLIST.md)** - Required readiness gates before promoting any prototype service to first-class status
- **[docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md](docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md)** - Ecosystem expansion governance rule and RM People boundaries

---

## 👨‍💻 **Quick Reference**

### For Developers
- **[DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md)** - Cheat sheets & examples
  - 5-minute setup
  - Auth cheat sheet
  - Event bus cheat sheet
  - Multi-tenancy patterns
  - Debugging guide
  - Common tasks
  - Mistake prevention
  - Performance tips

---

## 📍 **Service Directory**

| Service | Port | Auth | Events | Docs |
|---------|------|------|--------|------|
| **Gate** | 8000 | Provider | N/A | [Gate README](Gate/README.md) |
| **Atlas** | 8001 | ✅ Gate SSO + RS256 | ✅ Pub/Sub | [Atlas README](Atlas/README.md) |
| **Calendar** | 5001 | ✅ RS256 | ✅ Pub/Sub | [Calendar README](Calendar/README.md) |
| **Control Center** | 5173 | ✅ PKCE | N/A | See [Control Center/README.md](Control%20Center/README.md) |
| **Mail** | 8002 | ✅ RS256 | ✅ Pub/Sub | [Mail README](Mail/README.md) |
| **Connect** | 5000 | ✅ JWT | ✅ Consumer | [Connect README](Connect/README.md) |
| **Learn** | 5180 / 6002 | ✅ JWT | ✅ Pub/Sub | [Learn README](Learn/README.md) |
| **Writer** | 5183 / 6011 | ✅ Optional Gate JWT | ✅ Published (baseline) | [Writer README](Writer/README.md) |
| **Search** | 6200 | Optional (`X-Org-Id` / `X-Workspace-Id`) | Aggregating | [Search README](Search/README.md) |
| **Capital Hub** | 3001 | ✅ JWT | ✅ Pub/Sub | [Capital Hub README](Capital%20Hub/README.md) |
| **Secure** | 3003 | ✅ JWT | ✅ Pub/Sub | [Secure README](Secure/README.md) |
| **TurboTick** | 45018 / 6100 | ✅ Gate SSO + RS256 (planned) | ✅ Pub/Sub (planned) | [TurboTick README](TurboTick/README.md) |
| **RM Wallet** | 45019 / 6110 | ✅ Gate SSO + RS256 (planned) | ✅ Pub/Sub (planned) | [RM Wallet README](Wallet/README.md) |
| **RM Dock** | 45020 / 6120 | ✅ Gate SSO + RS256 (planned) | ✅ Pub/Sub (planned) | [RM Dock README](Dock/README.md) |

---

## 🗂️ **File Structure**

```
RM Orbit/
├── README.md                      ← You are here (overview)
├── PORTS.md                       ← Service ports
├── AUTH_SECURITY.md               ← Auth implementation (2,500 lines)
├── EVENT_SCHEMA.md                ← Event catalog (1,000 lines)
├── ECOSYSTEM_BLUEPRINT.md         ← System architecture
├── PRODUCTION_PLAN.md             ← Deployment guide
├── INTEGRATION_TESTING.md         ← Test procedures (800 lines)
├── IMPLEMENTATION_SUMMARY.md      ← Phase 1 report (5,000 lines)
├── DEVELOPER_QUICKREF.md          ← Quick reference
│
├── Gate/                          ← OAuth2 Provider
│   ├── authx/
│   ├── register_internal_apps.py  ← Register OAuth clients
│   └── .env
│
├── Atlas/                         ← Project Manager
│   ├── backend/
│   │   ├── app/auth.py           ← RS256 JWT verification
│   │   ├── app/config.py         ← GATE_PUBLIC_KEY_PATH
│   │   └── services/
│   │       ├── eventbus.py       ← Event publishing
│   │       └── eventbus_consumer.py ← Event consumption
│   └── frontend/
│
├── Calendar/                      ← Schedule Manager
│   ├── server/
│   │   ├── auth-middleware.js
│   │   ├── eventbus.js
│   │   └── index.js              ← Auth integration
│   └── frontend/
│
├── Control Center/                ← Collaboration Hub
│   ├── src/
│   │   ├── contexts/AuthContext.tsx ← PKCE OAuth
│   │   ├── pages/OAuthCallback.tsx
│   │   └── pages/Auth.tsx        ← Gate login UI
│   └── .env.example
│
├── Mail/                          ← Email Service
│   ├── backend/
│   │   ├── app/
│   │   │   ├── middleware/gate_auth.py
│   │   │   ├── services/eventbus.py
│   │   │   └── core/config.py
│   │   └── .env.example
│   └── frontend/
│
├── Connect/                       ← Real-time Chat
│   ├── server/
│   │   ├── eventbus-consumer.js  ← Event consumption
│   │   └── index.js              ← Socket.io integration
│   └── frontend/
│
├── Snitch/                        ← Prototype Apps
│   ├── backend/
│   │   ├── middleware/
│   │   │   ├── auth-middleware.js
│   │   │   └── org-middleware.js
│   │   ├── services/
│   │   │   ├── eventbus.js
│   │   │   ├── turn-server.js
│   │   │   └── media-service.js
│   │   └── index.js
│   └── frontend/
│       └── src/App.jsx            ← Unified login
│
└── Learn/, Writer/, TurboTick/, Wallet/, Dock/, Capital Hub/, Secure/, Meet/, Planet/ ...
    └── Similar structure
```

---

## 🔍 **Finding What You Need**

### "How do I authenticate users?"
→ [AUTH_SECURITY.md](AUTH_SECURITY.md) - Complete guide with examples

### "What events can services publish?"
→ [EVENT_SCHEMA.md](EVENT_SCHEMA.md) - Event catalog with JSON examples

### "How do I test the OAuth flow?"
→ [INTEGRATION_TESTING.md](INTEGRATION_TESTING.md) - Test 1: OAuth2 PKCE Flow

### "Where does service X run?"
→ [PORTS.md](PORTS.md) - Port directory

### "What's the status of service X?"
→ [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Service status matrix

### "I'm new, where do I start?"
→ [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md) - 5-minute setup

### "How do I add auth to a new endpoint?"
→ [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md) - Common tasks section

### "The API is returning 401, how do I fix it?"
→ [AUTH_SECURITY.md](AUTH_SECURITY.md#troubleshooting) - Troubleshooting section

### "Event bus isn't working, how do I debug?"
→ [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md#-debugging-guide) - Debugging guide

### "I need to deploy this, what do I do?"
→ [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md) - Pre-deployment checklist

---

## 📈 **Learning Path**

### For Frontend Developers
1. [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md) - Get started in 5 min
2. [AUTH_SECURITY.md](AUTH_SECURITY.md#oauth2--oidc-flow-pkce) - OAuth flow
3. [Control Center/src/contexts/AuthContext.tsx](Control%20Center/src/contexts/AuthContext.tsx) - Implementation example

### For Backend Developers
1. [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md) - Quick start
2. [AUTH_SECURITY.md](AUTH_SECURITY.md#token-verification) - Token verification
3. [EVENT_SCHEMA.md](EVENT_SCHEMA.md#event-categories) - Event publishing
4. [Atlas/backend/app/auth.py](Atlas/backend/app/auth.py) - Implementation example

### For DevOps / SRE
1. [PORTS.md](PORTS.md) - Service ports
2. [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md) - Deployment checklist
3. [AUTH_SECURITY.md](AUTH_SECURITY.md#gate-public-key-rotation) - Key rotation
4. [INTEGRATION_TESTING.md](INTEGRATION_TESTING.md) - Validation tests

### For Architects
1. [ECOSYSTEM_BLUEPRINT.md](ECOSYSTEM_BLUEPRINT.md) - System design
2. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What's implemented
3. [EVENT_SCHEMA.md](EVENT_SCHEMA.md) - Event-driven patterns
4. [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md) - Scalability planning

---

## 🎓 **Key Concepts**

### Unified SSO
All users authenticate once at Gate (AuthX). Every service accepts the same JWT token.

### RS256 JWT
Gate signs tokens with its private key. Services verify with Gate's public key. No shared secret needed.

### Multi-Tenancy
User organizations are enforced via X-Org-Id header. Services verify both token org_id and header match.

### Event Bus
Services publish events to Redis Pub/Sub. Other services subscribe and react. Decoupled, real-time.

### PKCE
Web frontends use PKCE to securely obtain tokens without exposing a client secret.

### Token Refresh
Access tokens expire in 8 hours. Refresh tokens (30 days) allow getting new access tokens.

---

## 📞 **Getting Help**

| Issue | Resource |
|-------|----------|
| Auth flow not working | [AUTH_SECURITY.md](AUTH_SECURITY.md#troubleshooting) Troubleshooting |
| Event not publishing | [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md#-common-mistakes) Check for mistakes |
| Multi-tenancy failing | [AUTH_SECURITY.md](AUTH_SECURITY.md#multi-tenancy--organization-access) Multi-tenancy section |
| Can't login | [INTEGRATION_TESTING.md](INTEGRATION_TESTING.md#test-1-oauth2-pkce-flow) Run Test 1 |
| API returning 401 | [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md#-debugging-guide) Debugging |
| Redis not working | [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md#-common-mistakes) Redis check |

---

## 🚀 **Next Steps**

### Phase 1 Complete ✅
- [x] Unified SSO with Gate
- [x] RS256 JWT verification
- [x] Multi-tenancy enforcement
- [x] Event bus integration
- [x] Services migrated

### Phase 2 (Planned)
- [ ] Kafka for event persistence
- [ ] gRPC for service-to-service
- [ ] GraphQL federation
- [ ] Machine learning anomaly detection

---

## 📟 **Version Info**

- **Ecosystem Version:** 1.0-production
- **Creation Date:** March 1, 2026
- **Last Updated:** March 1, 2026
- **Documentation Lines:** 15,000+
- **Implementation Files:** 50+

---

## 📋 **Documentation Statistics**

| Document | Lines | Topics | Focus |
|----------|-------|--------|-------|
| AUTH_SECURITY.md | 2,500 | OAuth, JWT, PKCE, Multi-tenancy | Complete reference |
| EVENT_SCHEMA.md | 1,000 | Event types, Redis, Consumers | Event-driven architecture |
| INTEGRATION_TESTING.md | 800 | Test procedures, Debugging | Quality assurance |
| IMPLEMENTATION_SUMMARY.md | 5,000 | Phase 1 completion | Project status |
| DEVELOPER_QUICKREF.md | 800 | Cheat sheets, Examples | Day-to-day development |
| ECOSYSTEM_BLUEPRINT.md | 500 | Architecture, Design | System overview |
| PRODUCTION_PLAN.md | 400 | Deployment, Operations | Go-to-production |
| PORTS.md | 100 | Service locations | Quick reference |
| README.md | 200 | Overview, Links | Entry point |

**Total:** 15,000+ lines of documentation

---

**Last Updated:** 2026-03-01  
**Maintained by:** Development Team  
**For support, see:** [DEVELOPER_QUICKREF.md](DEVELOPER_QUICKREF.md#-getting-help)
