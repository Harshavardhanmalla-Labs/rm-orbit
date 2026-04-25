# RM Orbit: Ecosystem Blueprint & Connectivity Map 💎

This document provides a granular analysis of every application in the RM Orbit ecosystem, its current development status, required enterprise features, and the specific "Connectors" and "Plugins" needed to achieve full interoperability.

Interoperability directive: RM Orbit must support both native-app adoption and external-platform connectivity/migration so enterprises can transition without workflow disruption. Reference: `docs/specs/orbit-interoperability-migration-bridge-v1.md`.

---

## 🔐 1. Gate (AuthX) — The Identity Core
*   **Status**: **Production Ready (v1.0)** - High-performance FastAPI backend with OIDC support.
*   **Role**: The single source of truth for identity, organizations, and permissions.
*   **Key Features**: MFA, OIDC Discovery, Rate Limiting, Multi-tenancy (Organizations).
*   **Enterprise Requirements**:
    *   [ ] **Tenant-Specific Branding**: UI for organizations to upload logos and custom CSS via the "Branding" JSONB field.
    *   [ ] **Directory Sync (SCIM)**: Plugin to sync users from Azure AD or Okta.
*   **Connectors**:
    *   `GATE_SSO_PLUGIN`: A drop-in JS/TS SDK for all other Orbit apps to handle OIDC flows effortlessly.
    *   `GATE_AUDIT_STREAM`: Real-time export of auth logs to the **Orbit Pulse** analytics app.

## 🚀 2. Atlas — Project Management
*   **Status**: **Functional MVP** - FastAPI Backend + React Frontend.
*   **Features**: Task tracking, project boards, file uploads.
*   **Enterprise Requirements**:
    *   [ ] **Resource Allocation**: Gantt charts and workload balancing.
    *   [ ] **Client Portals**: Shared project views for users from **Planet CRM**.
*   **Connectors**:
    *   `ATLAS_CALENDAR_SYNC`: Push task deadlines to **Orbit Calendar** (iCal/Internal API).
    *   `ATLAS_SECURE_DEPLOY`: Plugin to trigger CI/CD deployment jobs managed in **Secure**.
    *   `ATLAS_MAIL_TICKET`: Connector to convert an incoming email in **Orbit Mail** to an Atlas task.

## 📅 3. Calendar — Enterprise Scheduling
*   **Status**: **UI-Heavy MVP** - Feature-rich React frontend, requires backend hardening.
*   **Features**: Day/Week/Month views, event modals, drag-and-drop.
*   **Enterprise Requirements**:
    *   [ ] **Availability Lookup**: Automatically suggest meeting times based on team schedules.
    *   [ ] **Room/Resource Booking**: Integration with **Capital Hub** to book hardware/meeting rooms.
*   **Connectors**:
    *   `CALENDAR_MEET_HOOK`: Plugin to auto-generate an **Orbit Meet** link for every virtual event.
    *   `CALENDAR_PLANET_FOLLOWUP`: connector to auto-schedule follow-ups after a sales call in **Planet CRM**.

## 📊 4. Planet — Advanced CRM
*   **Status**: **Frontend Mature** - Advanced analytics and pipeline UI.
*   **Features**: Sales pipeline, predictive modeling, user management, audit logs.
*   **Enterprise Requirements**:
    *   [ ] **Lead Scoring Engine**: Integration with **Orbit Pulse** for behavioral analytics.
    *   [ ] **Automated Outreach**: Multi-channel sequencing (Email/Chat).
*   **Connectors**:
    *   `PLANET_MAIL_INGEST`: Real-time sync of all client emails from **Orbit Mail**.
    *   `PLANET_CONNECT_SYNC`: Create a private chat room in **Orbit Connect** for every new high-value deal.

## 💬 5. Connect — Enterprise Messaging
*   **Status**: **UI-Ready** - Modern glassmorphism UI, requires WebSocket backend.
*   **Features**: Real-time chat (mock), channel management, file sharing.
*   **Enterprise Requirements**:
    *   [ ] **Message Retention Policies**: Enterprise-grade compliance logging.
    *   [ ] **Admin Controls**: Master-switch for emergency communications.
*   **Connectors**:
    *   `CONNECT_GATE_PRESENCE`: Plugin to show "Active" status based on **Gate** session activity.
    *   `CONNECT_BOT_ENGINE`: Integration for other apps to post notifications (e.g., "New Asset Assigned" from Capital Hub).

## 🛠 6. Capital Hub — Asset & Finance Ledger
*   **Status**: **Concept Phase** (README drafted).
*   **Vision**: The "ERP-lite" of the ecosystem.
*   **Enterprise Requirements**:
    *   [ ] **SaaS License Management**: Track renewals and unused seats.
    *   [ ] **Hardware Inventory**: Integrated barcoding/QR code system for physical assets.
*   **Connectors**:
    *   `CAPITAL_SECURE_SYNC`: Connector that marks an asset as "At Risk" if **Secure** detects a vulnerability.
    *   `CAPITAL_ATLAS_BILLING`: Link project costs to asset depreciation.

## 🛡 7. Secure — Endpoint & Vulnerability
*   **Status**: **Concept Phase** (README drafted).
*   **Vision**: Unified Endpoint Management (UEM).
*   **Enterprise Requirements**:
    *   [ ] **Agent Deployment**: Lightweight background agent for Linux/Windows/macOS.
    *   [ ] **Zero-Trust Policy Engine**: Dynamically block **Gate** login if a device is unpatched.
*   **Connectors**:
    *   `SECURE_HEALTH_FEED`: Real-time health metrics to **Capital Hub**.
    *   `SECURE_AUDIT_LOG`: Compliance reporting for **Atlas** enterprise projects.

## 🎥 8. Control Center (formerly RM Meet)
*   **Status**: **Backend Mature** - Note/Agenda/Action Item logic implementation.
*   **Vision**: Lifecycle management for large-scale meetings.
*   **Enterprise Requirements**:
    *   [ ] **Transcript Auto-Sync**: Push meeting transcripts to **Learn** knowledge base.
    *   [ ] **Action Item Export**: One-click convert meeting action items to **Atlas** sub-tasks.
*   **Connectors**:
    *   `CONTROL_CENTER_MEET_STREAM`: Bridge to the lightweight **Orbit Meet** video layer.

## 🎫 9. TurboTick — Support, Incident, and Workflow Triage
*   **Status**: **MVP Web + Backend Baseline Added** - Core-mode API modules and dark-mode web workspace are now delivered.
*   **Vision**: A shared ticketing layer that turns emails/chats/incidents into assignable, SLA-tracked work across Orbit.
*   **Enterprise Requirements**:
    *   [ ] **Queue and SLA Engine**: Priority queues, response/resolve SLA timers, and escalation rules.
    *   [ ] **Multi-Channel Intake**: Create tickets from Mail, Connect, API/webhooks, and mobile quick actions.
    *   [ ] **Cross-App Linking**: Bidirectional links with Atlas tasks, Control Center actions, and Secure vulnerabilities.
*   **Connectors**:
    *   `TURBOTICK_MAIL_INGEST`: Convert incoming emails in **Orbit Mail** to tickets with requester context.
    *   `TURBOTICK_CONNECT_ESCALATE`: Create/escalate tickets directly from **Orbit Connect** messages or threads.
    *   `TURBOTICK_ATLAS_LINK`: Link tickets to **Atlas** projects/tasks and sync ticket/task status.
    *   `TURBOTICK_SECURE_INCIDENT_BRIDGE`: Open incident tickets from **Secure** findings and policy alerts.

## 🔐 10. RM Wallet — Secrets Vault + Permissioned Sharing
*   **Status**: **MVP Web + Backend Baseline Added** - FastAPI API scaffold with org/user/role context, share grants, reveal controls, and a lightweight web UI.
*   **Vision**: Store API keys, passwords, and confidential values with least-privilege sharing at company scale.
*   **Enterprise Requirements**:
    *   [ ] **KMS/HSM Encryption**: Envelope encryption with per-tenant key rotation and break-glass controls.
    *   [ ] **Access Governance**: Approval workflows, expiry policies, and immutable secret-access audit logs.
    *   [ ] **Service Accounts**: Non-human secret leasing with short-lived credentials.
*   **Connectors**:
    *   `WALLET_ATLAS_PROJECT_SCOPE`: Project-bound secret bundles for deployment and task automation.
    *   `WALLET_CONNECT_CONTEXT_INSERT`: Permission-checked insert of vault references from chat/command palette.
    *   `WALLET_MAIL_SECURE_SHARE`: Secure handoff pattern from compose window to vault-backed credentials.

## 🏢 11. RM Dock — Enterprise Software + License Portal
*   **Status**: **MVP Web + Backend Baseline Added** - FastAPI API scaffold for software catalog, licenses, assignments, and CARF workflow plus a lightweight web UI.
*   **Vision**: Company control plane for software procurement, seat assignment, and employee app requests.
*   **Enterprise Requirements**:
    *   [ ] **Procurement Policy Engine**: Budget/cost-center approval chains and vendor risk checks.
    *   [ ] **Lifecycle Automation**: Auto-renewal, renewal alerts, and unused-seat reclamation.
    *   [ ] **Cross-Functional Workflow**: CARF requests that trigger Atlas/TurboTick tasks automatically.
*   **Connectors**:
    *   `DOCK_CARF_TURBOTICK`: Convert software requests to tracked implementation tickets.
    *   `DOCK_ASSIGNMENT_SECURE_POSTURE`: Sync app assignments with Secure policy/risk posture.
    *   `DOCK_ATLAS_PROCUREMENT_FLOW`: Link approvals and rollout tasks to Atlas project plans.

---

## 🧩 Global Connectors & Shared Infrastructure

| Component | Description | Integration Type |
| :--- | :--- | :--- |
| **Orbit Event Bus** | A central Redis/RabbitMQ bus for cross-app events (e.g., `user.created`). | Backend |
| **Orbit UI Library** | Shared React components + CSS (RM Samplet/Forma) + Glassmorphism. | Frontend |
| **Orbit Files** | Centralized S3/MinIO bucket management with ACLs from **Gate**. | Service |
| **Orbit Search** | A unified Elasticsearch index for Atlas, Planet, Mail, and Learn. | Search |
| **TurboTick Link Graph** | Shared cross-link model for `ticket <-> task <-> thread <-> incident` with deep links. | Service |
| **Wallet Access Ledger** | Immutable secret-access event stream for RM Wallet governance and audits. | Service |
| **Dock Procurement Hub** | Shared approval + request routing for CARF workflows and license lifecycle. | Service |
| **Orbit Integration Hub** | Connector registry + external app adapters (Jira/Slack/Google Workspace/etc.) with health and retry controls. | Service |
| **Orbit Migration Bridge** | Project/data/workflow migration engine with `import_once`, `dual_sync`, and rollback checkpoints. | Service |

## 📦 Required External Plugins (3rd Party)
1.  **Stripe/Paddle**: For Personal and Enterprise billing.
2.  **AWS/GCP/Azure SDKs**: For multi-cloud asset tracking in **Capital Hub**.
3.  **Twilio/SendGrid**: For external communication in **Mail** and **Planet**.
4.  **Sentry**: Centralized error tracking for all apps.
5.  **Prometheus/Grafana**: Ecosystem-wide health monitoring.

---
"Connectivity is the multiplier of productivity."
