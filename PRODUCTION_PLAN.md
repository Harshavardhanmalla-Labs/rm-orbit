# RM Orbit: Enterprise Readiness Analysis & Roadmap 🗺️

This document provides a deep-dive analysis of the current state of the RM Orbit ecosystem and outlines the minute tasks required to transition from a collection of apps to a production-ready enterprise workspace.

## 📊 Current Ecosystem Analysis

| App                | Status     | Tech Stack             | Integration Level        |
| :----------------- | :--------- | :--------------------- | :----------------------- |
| **Gate (AuthX)**   | Functional | Python/FastAPI         | Core (Identity Provider) |
| **Atlas**          | Functional | Python/FastAPI + React | Independent Auth         |
| **Connect**        | Functional | React (Vite)           | UI-only / Local State    |
| **Planet**         | Functional | React (Vite)           | UI-only / Local State    |
| **Control Center** | Functional | Node/Express + React   | Independent Auth         |
| **Calendar**       | Functional | React (Vite)           | UI-only / Local State    |
| **Capital Hub**    | Concept    | -                      | -                        |
| **Secure**         | Concept    | -                      | -                        |
| **Learn**          | Concept    | -                      | -                        |
| **Meet**           | Concept    | -                      | -                        |
| **Mail**           | Concept    | -                      | -                        |

---

## 🛠 Minute Task List for Production Readiness

### ✅ Completed Infrastructure Work (Proof-of-concept)
- Snitch folder created to host in-progress UIs and backends for unlaunched apps.
- Basic OAuth/OIDC integration: frontends now redirect to Gate and exchange PKCE codes for tokens.
- JWT verification middleware added to every prototype service; Gate public key is consumed directly.
- Organization header (`X-Org-Id`) middleware added to enforce tenant separation across all prototypes.
- Central Redis event bus with HTTP bridge implemented; services publish/subscribe to `global` channel.
- CONNECT server extended to publish chat and call events to the bus.
- New real-time services added under Snitch:
  * TURN server (port 3478)
  * Media service placeholder (port 6006)
  * Learn, CapitalHub, Secure prototype services (ports 6002–6004)
- Starter `/oauth-config` endpoint returns client IDs for frontends.
- Start scripts (`start-all.sh` and PM2 config) updated to launch all prototypes along with existing apps.


### 1. Foundation & Cross-App Infrastructure

- [ ] **Shared UI Engine (`orbit-ui`)**:
  - Implement "RM Samplet" and "RM Forma" as global CSS variables.
  - Create a shared CSS library with Orbit's "Glassmorphism" standards.
  - Develop a `GlobalHeader` component to be used by all apps.
- [ ] **Global Navigation (The Orbit Bar)**:
  - Create a sidebar/topbar "Launcher" that allows instant switching between `atlas.orbit.local`, `planet.orbit.local`, etc.
  - Implement a "Global Search" bar that queries all apps via a central API.
- [ ] **Unified SSO (Gate Integration)**:
  - Register all apps as OIDC Clients in `Gate`.
  - Migrate `Atlas` and `Control Center` to use `Gate` JWT tokens instead of their internal sessions.
  - Implement "Auto-login" across subdomains (Single Sign-On).

### 2. Application-Specific Hardening

#### **Atlas (Project Management)**

- [ ] Implement "Team Workspaces" (Enterprise Tier).
- [ ] Connect "Time Tracking" to the global `Calendar`.
- [ ] Add "Asset Linking" (link an Atlas task to a hardware asset in `Capital Hub`).

#### **Connect (Communication)**

- [ ] Move from local mock data to a real WebSocket/Socket.io backend.
- [ ] Implement "Presence" (Offline/Online/In-Meeting).
- [ ] Add "Meet Now" button in chat threads that launches the `Meet` app.

#### **Planet (CRM)**

- [ ] Link CRM contacts to `Gate` Users (for client portal access).
- [ ] Implement "Deal Pipelines" with drag-and-drop.
- [ ] Sync "Interaction History" with `Mail`.

#### **Gate (Authentication)**

- [ ] Implement "Personal Enrollment" vs "Enterprise Enrollment" logic.
- _Personal_: Immediate access, individual billing.
- _Enterprise_: Requires Domain Verification + Admin Invite flow.

### 3. Operations & Reliability

- [ ] **Nginx Reverse Proxy**: Setup a unified gateway routing traffic (`*.rmorbit.com`).
- [ ] **Centralized Logging**: Implement a logging service where all backends (Atlas, Gate, Control Center) push structured JSON logs.
- [ ] **Database Consolidation**: Move from individual SQLite files to a Postgres cluster with schemas per app.
- [ ] **Vault (Storage)**: Implement a centralized S3-compatible storage service for all file uploads across the ecosystem.

---

## 🚀 Suggested New Additions

### 1. Orbit Pulse (Analytics Hub)

To make the ecosystem "Enterprise Ready", leadership needs a bird's-eye view.

- **Purpose**: A dashboard that aggregates KPIs from all apps (e.g., "Active Tasks" from Atlas + "Pending Invoices" from Capital Hub + "New Leads" from Planet).
- **Feature**: Real-time business "State of the Union".

### 2. Orbit Flow (Automation Engine)

- **Purpose**: A low-code automation tool.
- **Example**: "When a lead is closed in _Planet_, create a setup project in _Atlas_ and notify the team in _Connect_."

---

## 📂 Main Folder (`RM Orbit`) Analysis

- **Structure**: Currently a flat directory.
- **Recommendation**:
  - Add a root `docker-compose.yml` to spin up the entire stack.
  - Add a `Makefile` or `justfile` for common commands (`start-all`, `stop-all`, `check-status`).
  - Create a `docs/` folder for global architecture diagrams and API specs.

---

"Building an enterprise app isn't just about features; it's about the space between the features."
