# RM Orbit
# RM Wallet & RM Dock
## Engineering Implementation Specification

Date: 2026-03-09
Status: Active implementation guide
Governance: Subject to ecosystem expansion controls in `docs/specs/rm-orbit-product-governance-rm-people-module-proposal.md`

---

## Developer Guidance & Design Expectations

### Purpose of the Provided UI Prototype
The UI prototypes already present in the repository are conceptual references only.

Current prototype locations in this repo:
- `Wallet/frontend/index.html`
- `Dock/frontend/index.html`
- Other app UI files remain in their respective product folders and should be treated similarly.

These files are intended to communicate:
- product direction
- feature flow intent
- layout and interaction ideas

They are not final production implementation.

### Mandatory Rule
Do not ship static prototype HTML directly to production. Rebuild in a component architecture.

### Design Responsibility
Engineering and design teams are expected to evaluate and improve the prototype using:
- enterprise UX standards
- accessibility and keyboard interaction standards
- performance and maintainability requirements
- consistency with RM Orbit shared UI patterns

### Competitor Benchmark Baseline
Before finalizing IA and workflows, benchmark:
- ServiceNow
- Jira Service Management
- Zendesk
- HashiCorp Vault (for secrets UX)
- Jamf Self Service (for software portal UX)

### UI/UX Outcome Expectations
The final product must prioritize:
- clarity
- efficiency
- data density
- consistency
- performance
- accessibility

### Required Frontend Architecture
Recommended stack:
- Next.js
- React
- TypeScript
- TailwindCSS
- Radix UI

Prototype HTML should be used as:
- visual reference
- layout inspiration
- feature illustration

Not as production code.

---

## 1) Development Principles

Developers must treat all Stitch/exported HTML as a visual reference only.

Prototype files are unsuitable for production due to:
- static structure
- no state architecture
- no API abstraction
- no security boundaries
- no accessibility guarantees
- no performance/runtime optimization

The production UI must be rebuilt using reusable components and tested interactions.

---

## 2) UI Conversion Strategy

### Recommended Frontend Stack
- Next.js
- React
- TypeScript
- TailwindCSS
- Radix UI

### Conversion Workflow

1. Prototype review and decomposition
- layouts
- components
- interaction patterns
- navigation
- forms
- tables
- modals

2. Build reusable components
```text
components/
  Sidebar.tsx
  TopNavigation.tsx
  DataTable.tsx
  DashboardCard.tsx
  ActivityFeed.tsx
  ModalDialog.tsx
  FormInput.tsx
```

3. Build layout shells
```text
layouts/
  DashboardLayout.tsx
  AuthLayout.tsx
```

4. Define route surfaces (Next.js app router)
```text
app/
  dashboard/
  secrets/
  vaults/
  software/
  requests/
```

5. Adopt state strategy
- React Query for server state
- Zustand or Redux Toolkit for client UI state

---

## 3) RM Wallet System Overview

RM Wallet is RM Orbit’s secure secret vault and credential sharing platform.

### Scope
Stores and governs:
- passwords
- API keys
- tokens
- SSH keys
- certificates
- database credentials

### Core Responsibilities
- secure storage
- permission-based access
- secret rotation
- audit logging
- integration APIs

### Core Modules

#### Vault Management
Example vaults:
- Infrastructure Vault
- DevOps Vault
- Production Vault
- Security Vault

Vault schema:
```text
vault_id
organization_id
workspace_id
team_id
name
description
owner_team
created_at
updated_at
```

#### Secret Management
Secret schema:
```text
secret_id
vault_id
organization_id
workspace_id
team_id
name
secret_type
encrypted_value
owner_id
created_at
updated_at
expiration_date
```

Secret types:
- password
- api_key
- ssh_key
- certificate
- database_credential
- token

#### Secret Encryption
Required pattern:
- AES-256 envelope encryption
- data encryption keys (DEK)
- key encryption keys (KEK)
- KEK lifecycle managed by key management system

Flow:
```text
Application encrypts secret
-> Encrypted secret stored in DB
-> KEK and rotation policy managed in KMS/HSM
```

#### Access Control
Must support:
- user-level access
- team-level access
- role-based access control
- time-limited grants

Permission schema:
```text
permission_id
resource_id
user_id
team_id
role
expiration
created_at
updated_at
```

#### Secret Rotation
Examples:
- database credentials every 90 days
- API tokens every 30 days

#### Audit Logging
Audit every sensitive action:
- secret viewed
- secret modified
- secret shared
- secret rotated

Audit schema:
```text
log_id
organization_id
workspace_id
user_id
action
resource_id
timestamp
ip_address
request_id
```

### RM Wallet Backend Architecture
Stack:
- Python
- FastAPI
- PostgreSQL
- Redis

Service domains:
- wallet-service
- encryption-service
- permission-service
- audit-service
- integration-service

### RM Wallet API Surface (target)
- `POST /api/secrets`
- `GET /api/secrets/{id}`
- `POST /api/secrets/{id}/rotate`
- `POST /api/secrets/{id}/share`
- `GET /api/secrets/{id}/audit`

---

## 4) RM Dock System Overview

RM Dock is RM Orbit’s enterprise software catalog and license management platform.

### Core Functions
- software catalog
- license pool management
- software request workflow
- deployment tracking
- version management

### Core Modules

#### Software Catalog
Schema:
```text
software_id
organization_id
workspace_id
team_id
name
description
category
vendor
supported_os
created_at
updated_at
```

#### License Pool
Schema:
```text
license_id
software_id
organization_id
workspace_id
license_key
status
assigned_user
expiration_date
created_at
updated_at
```

Status values:
- available
- assigned
- expired
- reserved

#### Software Requests
Schema:
```text
request_id
software_id
organization_id
workspace_id
user_id
status
approval_state
created_at
updated_at
```

Lifecycle:
- requested
- pending_approval
- approved
- deployment_started
- completed

#### Deployment Tracking
Schema:
```text
deployment_id
software_id
organization_id
workspace_id
device_id
user_id
status
installed_version
timestamp
```

#### Version Management
Schema:
```text
version_id
software_id
organization_id
workspace_id
version_number
release_date
supported_os
deployment_package
```

### RM Dock Backend Architecture
Stack:
- Python
- FastAPI
- PostgreSQL
- Redis

Service domains:
- software-service
- license-service
- deployment-service
- request-service
- integration-service

---

## 5) TurboTick Integration

RM Wallet and RM Dock must integrate with TurboTick workflow orchestration.

Example flow:
```text
User requests software
-> TurboTick creates operation ticket
-> Dock validates catalog/license availability
-> License assignment is executed
-> Wallet provides required credential
-> Deployment workflow proceeds
```

Required integration outputs:
- event publication for request/ticket/license state transitions
- cross-linking between ticket IDs, request IDs, deployment IDs, and secret IDs

---

## 6) Shared Infrastructure

Shared platform services:
- API gateway
- authentication service (Gate)
- event bus
- notification service
- audit service

Event bus candidates:
- Kafka
- NATS
- Redis Streams

---

## 7) Security Requirements

Mandatory controls:
- RBAC enforcement
- strong API authentication/authorization
- encryption in transit and at rest
- immutable audit logs for privileged actions
- secure secret material handling

---

## 8) Multi-Tenant Model

Every persisted record must include tenant context:
```text
organization_id
workspace_id
team_id
```

PostgreSQL implementation requirements:
- tenant-scoped indexes
- row-level security policies
- strict cross-tenant query guards

---

## 9) Deployment Architecture

Recommended deployment model:
- Docker for packaging
- Kubernetes for orchestration
- Terraform for infra provisioning

Service deployment guidance:
- separate service boundaries per domain
- independent scaling for high-traffic domains
- centralized observability, tracing, and audit pipelines

---

## 10) Implementation Phases

### Phase 1
- core UI shell
- vault management
- secure secret storage
- software catalog
- license tracking

### Phase 2
- request/approval workflows
- deployment tracking
- automation integration
- audit logging and governance controls

### Phase 3
- advanced security controls
- rotation orchestration
- analytics and reporting expansion
- optional AI enhancements

---

## Engineering Delivery Notes for Current Repo

Current local baselines (already implemented) should be used as migration starting points:
- `Wallet/backend/`
- `Wallet/frontend/`
- `Dock/backend/`
- `Dock/frontend/`

Next implementation step is not to preserve prototype structure, but to progressively migrate these baselines into a production-grade service architecture with:
- persistent storage
- Gate JWT hard enforcement
- event contracts
- shared design system alignment
- robust test coverage and runtime gates

---

## Final Instruction to Developers

Do not implement a direct prototype clone.

Expected final outcome:
- modern SaaS-grade enterprise UX
- scalable frontend and backend architecture
- consistent RM Orbit design patterns
- high operational reliability and security
- maintainable system boundaries for long-term growth
