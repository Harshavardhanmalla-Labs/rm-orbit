# RM Orbit Mobile Parity Spec (v1)

Date: 2026-03-09
Owners: Connect, Mail, TurboTick, Wallet, Dock
Status: Approved scope for iOS + Android implementation

## 1. Objective

Deliver parity for the web intelligence flows on iOS and Android without introducing AI dependencies. AI enhancement remains optional behind existing adapter modes.

## 2. Shared UX Contract

- Primary interaction for contextual tools: long-press action sheet.
- Secondary interaction: inline quick-action chips in compose/reply surfaces.
- Keyboard command equivalents on mobile: floating command launcher button (`+`/spark icon).
- Offline behavior:
  - queue action payloads locally
  - mark queued actions in UI
  - replay on reconnect with idempotency key
- Required telemetry fields on each action:
  - `request_id`
  - `org_id`
  - `workspace_id`
  - `source_app`
  - `source_surface`

## 3. Feature Mapping by App

### 3.1 Mail (Compose + Reader)

- Compose long-press sheet:
  - Insert Atlas reference
  - Find Atlas task ID
  - Preview Atlas matches
  - Follow-up suggestions
  - Insert mention (`@task/@project/@doc/@ticket`)
  - Create TurboTick ticket
  - Create RM Dock CARF
  - Open RM Wallet
- Reader quick actions:
  - Convert thread to Atlas task
  - Generate thread brief
  - Context reply suggestions
  - Tap-able mention chips

### 3.2 Connect (Composer + Message Bubble)

- Long-press parity with current web context actions.
- Mention chips preserve deep-link behavior to Atlas/TurboTick/Mail Search.
- Thread panel parity:
  - action timeline card
  - one-tap brief handoff

### 3.3 TurboTick (Ticket/Incident/Request)

- Long-press action sheet on list rows:
  - assign
  - escalate
  - change priority/status
  - copy deep link
  - add comment
- Detail screen quick actions:
  - timeline event add
  - SLA snapshot view
  - knowledge suggestions open
- Push categories:
  - assignment
  - escalation
  - SLA breach warning

### 3.4 Wallet

- Secure reveal flow:
  - biometric gate (platform-native)
  - masked preview by default
  - timed reveal auto-hide
- Share flow parity:
  - subject picker (`user|role`)
  - permission picker (`read|use|manage`)
  - project requirement toggle
- Audit envelope attached to reveal/share mutations.

### 3.5 Dock

- CARF mobile lifecycle:
  - request create/edit/submit
  - manager approve/reject
  - automation status card (TurboTick follow-up)
- Assignment operations:
  - request seat
  - revoke assignment
  - renewal warning card

## 4. API/Contract Requirements

- No new backend auth model; use existing Gate JWT/header hybrid modes.
- All mobile mutations carry `X-Request-Id`.
- Idempotency header for queued offline replays: `X-Idempotency-Key`.
- Event bus compatibility retained (`ticket.*`, `dock.request.*`, `wallet.secret.*`).

## 5. Delivery Slices

1. Slice A (2 weeks): shared mobile action sheet + Mail/Connect compose parity.
2. Slice B (2 weeks): TurboTick list/detail parity + push notifications.
3. Slice C (2 weeks): Wallet secure reveal/share + Dock CARF approvals.
4. Slice D (1 week): offline replay, telemetry validation, contract tests.

## 6. Exit Criteria

- iOS and Android both support all listed long-press actions.
- No action is AI-required.
- Action success/failure is observable with request correlation.
- Offline queued actions replay safely with no duplicate writes.
