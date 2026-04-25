# RM Orbit Interoperability + Migration Bridge Spec (v1)

Date: 2026-03-09  
Status: Active directive (hivemind backlog)

## 1) Intent

Even while RM Orbit prioritizes adoption of native Orbit apps, the platform must support:

- Connecting external third-party apps and data sources.
- Migrating from incumbent platforms with minimal downtime.
- Running in hybrid mode (Orbit apps + external apps) during transition.

This is a growth and onboarding requirement, not optional nice-to-have scope.

## 2) Core Requirements

- Integration-first posture:
  - Inbound and outbound connectors for project, ticket, chat, mail, docs, and identity data.
- Migration bridge:
  - One-time import and continuous sync modes.
  - Field mapping templates and dry-run validation.
  - Idempotent replay and rollback checkpoints.
- Cross-project continuity:
  - Preserve project/task/thread relationships and references during migration.
  - Maintain actor ownership mapping (users/teams/roles) through Gate identities.

## 3) Connector Targets (Priority)

- Project/Work Management:
  - Jira, Asana, Trello, Monday.com
- Communication:
  - Slack, Microsoft Teams, Gmail/Google Workspace, Outlook/Microsoft 365
- Docs/Knowledge:
  - Notion, Confluence, Google Docs (export/import bridge)
- Identity:
  - Azure AD / Entra ID, Okta (via Gate + SCIM/OIDC patterns)

## 4) Migration Bridge Modes

- `import_once`: snapshot ingest for cutover waves.
- `dual_sync`: temporary bidirectional sync during transition.
- `orbit_authoritative`: Orbit becomes source of truth; external side read-only/bridge-only.

## 5) Platform Components

- `integration-hub-service`:
  - connector registry, credentials, health, retry policy
- `migration-bridge-service`:
  - mapping profiles, import jobs, replay logs, checkpoint states
- Shared contracts:
  - event envelopes (`event_id`, `request_id`, `org_id`, `workspace_id`)
  - object mapping contract (`external_id`, `orbit_id`, `mapping_version`)

## 6) Delivery Backlog

1. Publish canonical mapping schema for projects/tasks/threads/tickets.
2. Add migration job API (`start`, `dry-run`, `pause`, `resume`, `rollback`, `status`).
3. Add connector health and rate-limit handling.
4. Add audit trail for every migrated object and mapping decision.
5. Ship first-party connector pack (Jira + Slack + Google Workspace baseline).

## 7) Exit Criteria

- At least one enterprise can migrate a real project portfolio with relationship integrity preserved.
- Hybrid mode supports concurrent Orbit + external app operations without data loss.
- Migration and connector actions are fully auditable and tenant-isolated.
