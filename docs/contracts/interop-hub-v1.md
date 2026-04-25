# RM Orbit Interoperability Hub V1 Contract

## 1. Overview
The Interoperability Hub defines how data is mapped and synchronized between RM Orbit services and external systems. It enables event-driven automations, such as automatically creating a project task based on a high-priority support ticket.

## 2. Terminology
- **Connector**: A bridge between two services or an external system.
- **Sync Rule**: A mapping of fields and triggers that defines when and how data flows.
- **Direction**: One-way (Inbound/Outbound) or Bi-directional.
- **Lifecycle Modes**: 
  - `import_once`: One-time migration.
  - `dual_sync`: Keeping two records in lock-step.
  - `orbit_authoritative`: Orbit is the master; external is a mirror.

## 3. Data Mapping Shapes

### 3.1. Project/Task Mapping (Atlas)
```json
{
  "type": "atlas_task",
  "fields": {
    "title": "string",
    "description": "text",
    "priority": "low|medium|high|critical",
    "status": "todo|in_progress|done",
    "assignee_id": "string",
    "external_ref": "string"
  }
}
```

### 3.2. Ticket Mapping (TurboTick)
```json
{
  "type": "turbotick_ticket",
  "fields": {
    "title": "string",
    "description": "text",
    "priority_level": "low|medium|high|critical",
    "status": "open|acknowledged|in_progress|resolved|closed",
    "queue": "string",
    "external_id": "string"
  }
}
```

## 4. Integration Hub Registry
Connectors MUST be registered with:
- `connector_id`: Unique identifier (e.g., `tt-atlas-bridge`).
- `source_service`: Service originating the event.
- `target_service`: Service receiving the action.
- `auth_payload`: Credentials for the target service (stored in RM Wallet).

## 5. Automation Triggers
Connectors listen for standardized events on the Redis Event Bus:
- `ticket.created` / `ticket.updated`
- `project.task.created` / `project.task.updated`
- `dock.procurement.approved`

## 6. Audit & Traceability
Every cross-app action MUST include:
- `X-Correlation-ID`: Inherited from the original request.
- `X-Connector-ID`: Identifying the bridge that took the action.
- `audit.metadata`: Link to the source object.
