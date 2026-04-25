# RM Orbit Port Assignments

**Canonical source of truth: Cloudflare Tunnel config (`*.freedomlabs.in`)**

All frontend services MUST bind to their assigned `45xxx` port.
Backend APIs use internal ports not exposed via tunnel.

## Tunnel Port Map (authoritative)

| #   | Domain                   | Port  | App / Service                     |
| --- | ------------------------ | ----- | --------------------------------- |
| —   | atlas.freedomlabs.in     | 5173  | Atlas (Resource Planning)         |
| 15  | auth.freedomlabs.in      | 45001 | Gate (AuthX)                      |
| 16  | coparent.freedomlabs.in  | 45002 | _(Not this project)_              |
| 17  | meet.freedomlabs.in      | 45003 | Meet (Video Conferencing)         |
| 18  | mail.freedomlabs.in      | 45004 | Mail (Email Client)               |
| 19  | calendar.freedomlabs.in  | 45005 | Chronos Calendar                  |
| 20  | planet.freedomlabs.in    | 45006 | Planet (CRM)                      |
| 21  | fonts.freedomlabs.in     | 45007 | RM Fonts (specimen gallery)       |
| 22  | chat.freedomlabs.in      | 45008 | Connect (Chat / messaging)        |
| 23  | learn.freedomlabs.in     | 45009 | Learn (Documentation portal)      |
| 24  | docs.freedomlabs.in      | 45010 | Writer (Docs editor)              |
| 25  | center.freedomlabs.in    | 45011 | Control Center                    |
| 26  | secure.freedomlabs.in    | 45012 | Secure (compliance)               |
| 27  | capital.freedomlabs.in   | 45013 | **Tether** (Connection with Gravity — relationship science) |
| 28  | api.freedomlabs.in       | 45014 | _(Not this project)_              |
| 29  | backup.freedomlabs.in    | 45015 | _(Not this project)_              |
| 30  | ecosystem.freedomlabs.in | 45016 | FitterMe (ecosystem health)       |

## Proposed Reservations (Pending Tunnel Update)

| Domain                  | Port  | App / Service                     | Notes                                  |
| ----------------------- | ----- | --------------------------------- | -------------------------------------- |
| card.freedomlabs.in       | 45023 | RM Card (Identity Layer)            | Frontend + public card view |
| turbotick.freedomlabs.in  | 45018 | TurboTick (Support + Incident Tool) | Web MVP baseline frontend |
| wallet.freedomlabs.in     | 45019 | RM Wallet (Secrets Vault)          | Reserve for secure vault web frontend  |
| dock.freedomlabs.in       | 45020 | RM Dock (Software + License Portal) | Reserve for enterprise portal frontend |
| shell.freedomlabs.in      | 45021 | Orbit Shell (AI Conversational UI)  | Primary AI interface — serves frontend + API |
| admin.freedomlabs.in      | 45022 | Gate Admin Portal (Superadmin Console) | React SPA — proxies API to Gate on 45001 |
| scribe.freedomlabs.in     | 45017 | Scribe (AI Content Engine)          | LinkedIn, blog, newsletter auto-content     |
| rmm.freedomlabs.in        | 45026 | RMMeet Guest Join                   | Public guest join page — no account needed  |
| research.freedomlabs.in   | 10007 | Research (Autonomous Paper Writing) | Strict port — AI-powered end-to-end research paper generator |
| architect.freedomlabs.in  | 10005 | Imprint (Cognitive Twin)            | Frontend — brain OS UI                                       |

## Backend / Internal Ports

| Service                   | Port  | Transport               | Notes                                      |
| ------------------------- | ----- | ----------------------- | ------------------------------------------ |
| Gate (AuthX) API          | 45001 | Docker → container 8000 | Postgres 5444, Redis 6344                  |
| Atlas Backend             | 8000  | uvicorn (native)        | FastAPI                                    |
| Mail Backend              | 8004  | Docker → container 8000 | `maildemo` compose profile                 |
| Control Center Backend    | 8077  | node (native)           | Express                                    |
| Calendar Backend          | 5001  | node (native)           | Express                                    |
| Connect Backend           | 5000  | Docker → container 5000 | Node + better-sqlite3                      |
| Meet Backend              | 6001  | node (native)           | Express / Socket.io                        |
| Planet Backend            | 46000 | uvicorn (native)        | FastAPI                                    |
| Secure Backend            | 6004  | uvicorn (native)        | FastAPI — ⚠️ NOT 8000                      |
| Writer Backend            | 6011  | uvicorn (native)        | FastAPI                                    |
| Search Aggregator         | 6200  | uvicorn (native)        | FastAPI                                    |
| Search Frontend           | 6201  | Vite dev server         | React SPA — command-palette universal search|
| TurboTick Backend           | 6100  | uvicorn (native)        | Ticketing API MVP baseline                 |
| RM Wallet Backend           | 6110  | uvicorn (native)        | Secret vault API MVP baseline              |
| RM Dock Backend             | 6120  | uvicorn (native)        | Software-portal API MVP baseline           |
| Orbit Shell Backend         | 6300  | uvicorn (native)        | AI orchestrator — Claude API + tool router |
| Scribe Backend              | 6400  | uvicorn (native)        | FastAPI — AI content generation engine      |
| Research Backend            | 6420  | uvicorn (native)        | FastAPI — autonomous paper pipeline API     |
| Imprint Backend             | 6500  | uvicorn (native)        | FastAPI — Cognitive twin graph engine       |
| RM Card Backend             | 46023 | uvicorn (native)        | FastAPI — identity layer, card CRUD, vCard  |
| **Tether Backend**          | **6413** | uvicorn (native)     | FastAPI — relationship science API (tunnel: capital.freedomlabs.in:45013) |
| FitterMe API              | 8000  | Docker (internal)       | gunicorn + uvicorn — accessed by Vite proxy|
| FitterMe Frontend         | 45016 | Vite dev server         | React SPA — proxies /api + /auth → :8000  |
| Snitch Backend            | 6000  | node (native)           | Prototype                                  |
| Snitch Learn Service      | 6002  | node (native)           | Prototype                                  |
| Snitch CapitalHub Service | 6003  | node (native)           | Prototype                                  |
| Snitch Secure Service     | 6004  | node (native)           | Prototype — check for conflict with Secure |
| Snitch EventBus           | 6005  | node (native)           | Prototype                                  |
| Snitch Media              | 6006  | node (native)           | Prototype                                  |
| TURN server               | 3478  | node (native)           | WebRTC relay                               |

## Mail Infrastructure Ports (On-Prem)

| Service                | Port  | Transport         | Notes                             |
| ---------------------- | ----- | ----------------- | --------------------------------- |
| Postfix SMTP (receive) | 25    | Docker (on-prem)  | Inbound email from internet       |
| Postfix Submission     | 587   | Docker (on-prem)  | Authenticated outbound (STARTTLS) |
| Postfix SMTPS          | 465   | Docker (on-prem)  | Implicit TLS submission           |
| Dovecot IMAP           | 143   | Docker (on-prem)  | Plaintext IMAP (internal)         |
| Dovecot IMAPS          | 993   | Docker (on-prem)  | TLS-encrypted IMAP                |
| Dovecot LMTP           | 24    | Docker (on-prem)  | Local delivery from Postfix       |
| OpenDKIM               | 8891  | Docker (internal) | DKIM signing milter               |
| Rspamd Proxy (milter)  | 11332 | Docker (internal) | Spam filter milter for Postfix    |
| Rspamd Scanner         | 11333 | Docker (internal) | Spam scoring API                  |
| Rspamd Web UI          | 11334 | Docker (on-prem)  | Spam admin dashboard              |

## Launch Profiles

### Profile A: `./start-all.sh` + per-service `start.sh`

- Production-grade orchestrator with health checks, supervised restarts, and port-conflict detection.
- Phased startup: Docker infra → native backends → frontends → Snitch prototypes.

### Profile B: `pm2 start ecosystem.config.cjs`

- PM2 process manager — automatic restart on crash, log management.

## Notes

- `Secure/start.sh` backend runs on port **6004** (not 8000) to avoid conflict with Atlas.
- `Planet/start.sh` explicitly uses `--port 45006` to prevent Vite from picking a random port.
- Reserved ports (45002, 45014, 45015) have tunnel entries but no apps yet.
- FitterMe (45016) is Docker-managed and not included in `start-all.sh` (started separately).
