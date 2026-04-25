# RM Orbit Product Governance and RM People Module Proposal

Status: Draft for execution alignment
Date: 2026-03-09
Owner: RM Orbit Product and Engineering

## Purpose

This document defines:

1. Product governance controls for RM Orbit scope growth
2. Boundaries for a possible RM People module
3. Integration patterns between RM People and existing RM Orbit applications
4. Focus rules that prioritize production readiness over uncontrolled expansion

The objective is to keep RM Orbit cohesive, secure, and production-ready instead of becoming a fragmented collection of partially developed applications.

## Decision Update (2026-03-09)

Approved immediate direction:

- Implement time card submission and approval inside RM Control Center
- Do not create a new standalone HR application at this stage

Implications:

- RM People remains a deferred capability concept, not an active app build
- Time card workflows should be delivered as a Control Center module with shared auth, tenancy, and audit controls
- Lifecycle automation integrations should reuse existing RM Orbit services (Gate, Dock, Wallet, TurboTick)

## 1. Product Governance Rule (Critical)

Effective immediately:

No additional new major applications should be added to RM Orbit until the current platform reaches production readiness and active real-user adoption.

This means:

- No new major app launches
- No unrelated experimental product additions
- No ecosystem expansion that weakens delivery focus

Current priority:

- Stabilize existing apps
- Complete production architecture
- Launch with real users
- Validate reliability, security, and workflows

## 2. Current RM Orbit Application Set

The current ecosystem under this governance rule:

- RM Gate: Identity and access management
- RM TurboTick: Workflow orchestration and service operations
- RM Dock: Enterprise software catalog and license portal
- RM Wallet: Secure secrets vault
- RM Atlas: Infrastructure and project operations
- RM Secure: Security posture and endpoint compliance
- RM Mail: Communication gateway
- RM Meet: Collaboration and incident war rooms
- RM Control Center: Unified operational dashboard

These applications must reach production maturity before additional ecosystem expansion.

## 2A. Current Execution Scope: Time Cards in RM Control Center

Time card delivery should be implemented as a Control Center module, not a new standalone product.

Recommended module scope:

- Employee can submit daily or weekly time cards
- Manager can approve or reject submitted cards
- Admin can view audit and export summaries
- Tenant-scoped reporting for hours by department, team, and cost center

Suggested data model for the Control Center module:

```text
time_cards
----------
time_card_id
organization_id
workspace_id
employee_id
week_start_date
week_end_date
total_hours
status
submitted_at
approved_at
approved_by
notes
created_at
updated_at
```

Status values:

```text
Draft
Submitted
Approved
Rejected
```

## 3. Deferred Capability Under Controlled Scope: RM People

The only new capability under consideration is a lightweight HR and employee lifecycle module called RM People.

Important boundary:

RM People is not a payroll product.

RM People focuses on identity lifecycle and operational automation, not payroll, tax, or benefits processing.

## 4. RM People Scope In

RM People should cover:

- Employee directory
- Department and manager hierarchy
- Onboarding workflows
- Offboarding workflows
- Access lifecycle orchestration
- Basic time tracking

RM People becomes an employee lifecycle event source for RM Orbit automations.

## 5. RM People Scope Out

RM People will not implement payroll, tax, or benefits management.

Examples of systems not in build scope:

- ADP-like payroll logic
- Workday-like HRIS/payroll suites
- Gusto-like tax/benefits processing

If needed later, payroll systems should be integrated through APIs rather than built in RM Orbit.

## 6. RM People Core Data Model

### Employee Directory

```text
employees
---------
employee_id
first_name
last_name
display_name
email
department_id
manager_id
job_title
employment_type
status
hire_date
created_at
updated_at
```

Status values:

```text
Active
On Leave
Suspended
Terminated
```

### Organizational Structure

```text
departments
-----------
department_id
name
parent_department_id
created_at
```

Manager hierarchy uses `manager_id -> employee_id` relationship.

### Basic Time Tracking

```text
timesheets
----------
timesheet_id
employee_id
date
clock_in
clock_out
hours_worked
status
approved_by
```

Timesheet statuses:

```text
Draft
Submitted
Approved
Rejected
```

## 7. Lifecycle Events and Automation

RM People should emit lifecycle events to RM Orbit event bus.

Core event set:

- employee.created
- employee.updated
- employee.terminated
- employee.role.changed
- employee.department.changed

### Onboarding Flow

```text
Employee created
-> RM Gate creates identity
-> RM Dock assigns required software
-> RM Wallet provisions credentials
-> RM TurboTick creates onboarding tasks
```

### Offboarding Flow

```text
Employee terminated
-> RM Gate disables access
-> RM Wallet revokes secret access
-> RM Dock reclaims licenses
-> RM TurboTick creates offboarding checklist
```

## 8. Integration Contracts with Existing Apps

### RM Gate

- Identity creation and status updates
- Access disablement on offboarding

### RM Dock

- Role-based software assignment
- License recovery during offboarding

### RM Wallet

- Role or team-based vault access provisioning
- Secret share revocation during offboarding

### RM TurboTick

- Automated onboarding and offboarding workflow tickets
- Status-driven checklist execution

## 9. Technical Architecture Guidance

Backend stack:

```text
Python
FastAPI
PostgreSQL
Redis
```

Service boundaries:

```text
people-service
directory-service
lifecycle-service
timesheet-service
integration-service
```

Event bus options:

```text
Kafka
NATS
Redis Streams
```

Example event payload:

```json
{
  "event_type": "employee.created",
  "employee_id": "E1023",
  "department": "Engineering",
  "timestamp": "2026-03-08T10:00:00Z"
}
```

Frontend guidance:

- Rebuild UI in component architecture
- Treat prototype HTML as visual reference only
- Recommended stack: Next.js, React, TypeScript, TailwindCSS

## 10. Security and Multi-Tenant Requirements

Security controls:

- Role-based access control
- API authentication and service identity checks
- Audit logging for sensitive actions
- Data encryption at rest and in transit

Multi-tenant requirements:

- Include `organization_id`, `workspace_id`, and `team_id` on records
- Enforce tenant isolation with PostgreSQL row-level security

## 11. Development Phases for RM People (Deferred Until Governance Gate Opens)

Phase 1:

- Employee directory
- Department management
- Manager hierarchy
- Lifecycle event emission

Phase 2:

- Onboarding and offboarding workflows
- Dock, Wallet, and TurboTick integration automation

Phase 3:

- Timesheets
- Org chart UI
- HR analytics

## 12. Product Focus Directive

RM Orbit must evolve as a cohesive enterprise platform, not as disconnected prototypes.

Execution priorities:

- Stability
- Security
- Scalability
- Real-user adoption
- Operational reliability

Only after production maturity and validated usage should the ecosystem expand beyond the current app set and approved governance scope.
