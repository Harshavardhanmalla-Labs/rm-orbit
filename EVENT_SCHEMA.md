# RM Orbit Event Bus Schema

This document describes the complete event schema for the RM Orbit ecosystem.

## Event Structure

All events published to Redis follow this base structure:

```json
{
  "timestamp": "2026-03-01T10:30:00.000Z",
  "source": "service-name",
  "event_type": "resource.action",
  "schema_version": 1,
  "org_id": "org_123",
  "user_id": "user_456",
  "data": {}
}
```

### Fields
- **timestamp**: ISO 8601 timestamp in UTC
- **source**: Service publishing the event (e.g., "atlas", "calendar", "mail")
- **event_type**: Hierarchical event type: `resource.action`
- **schema_version**: Event envelope contract version (default/current: `1`)
- **org_id**: Organization ID (for multi-tenancy)
- **user_id**: User performing the action
- **data**: Event-specific payload

### Versioning Policy
- Publishers should include `schema_version` in every event envelope.
- Current baseline is `schema_version = 1`.
- Consumers should treat missing `schema_version` as `1` for backward compatibility.

### Canonical Contract Fixtures
- Shared fixture pack path: `docs/contracts/event-envelope-v1.json`
- Purpose:
  - Provide canonical, cross-service envelope examples for test re-use.
  - Encode expected normalization behavior (`event_type` fallback, `schema_version` default) and org-scope rejection cases.

## Event Categories

### Authentication Events (`auth.*`)

#### `auth.login`
User successfully authenticated
```json
{
  "event_type": "auth.login",
  "data": {
    "user_id": "user_123",
    "email": "user@example.com",
    "org_id": "org_123",
    "auth_method": "gate_oauth"
  }
}
```

#### `auth.logout`
User logged out
```json
{
  "event_type": "auth.logout",
  "data": {
    "user_id": "user_123"
  }
}
```

---

### Project Management Events (`project.*`)

#### `project.created`
New project created
```json
{
  "event_type": "project.created",
  "data": {
    "project_id": "proj_123",
    "name": "Q1 Planning",
    "created_by": "user_456"
  }
}
```

#### `project.updated`
Project details changed
```json
{
  "event_type": "project.updated",
  "data": {
    "project_id": "proj_123",
    "fields_changed": ["name", "status"]
  }
}
```

#### `project.deleted`
Project deleted
```json
{
  "event_type": "project.deleted",
  "data": {
    "project_id": "proj_123"
  }
}
```

---

### Calendar Events (`calendar.*`)

#### `calendar.event.created`
New calendar event created
```json
{
  "event_type": "calendar.event.created",
  "data": {
    "event_id": "evt_123",
    "title": "Weekly Standup",
    "start": "2026-03-01T09:00:00Z",
    "end": "2026-03-01T09:30:00Z"
  }
}
```

#### `calendar.event.updated`
Calendar event modified
```json
{
  "event_type": "calendar.event.updated",
  "data": {
    "event_id": "evt_123",
    "title": "Weekly Standup (Rescheduled)",
    "fields_changed": ["start", "end"]
  }
}
```

#### `calendar.event.deleted`
Calendar event removed
```json
{
  "event_type": "calendar.event.deleted",
  "data": {
    "event_id": "evt_123"
  }
}
```

---

### Mail Events (`mail.*`)

#### `mail.message.sent`
Email sent successfully
```json
{
  "event_type": "mail.message.sent",
  "data": {
    "message_id": "msg_123",
    "to": ["user@example.com"],
    "subject": "Project Update",
    "timestamp": "2026-03-01T10:15:00Z"
  }
}
```

#### `mail.message.received`
Email received
```json
{
  "event_type": "mail.message.received",
  "data": {
    "message_id": "msg_456",
    "from": "sender@example.com",
    "subject": "Re: Project Update",
    "timestamp": "2026-03-01T10:20:00Z"
  }
}
```

#### `mail.attachment.uploaded`
File attached to email
```json
{
  "event_type": "mail.attachment.uploaded",
  "data": {
    "message_id": "msg_123",
    "filename": "report.pdf",
    "size_bytes": 1048576
  }
}
```

---

### Meeting Events (`meeting.*`)

#### `meeting.scheduled`
New meeting scheduled
```json
{
  "event_type": "meeting.scheduled",
  "data": {
    "meeting_id": "mtg_123",
    "title": "Quarterly Review",
    "start": "2026-03-10T14:00:00Z",
    "attendees": ["user_123", "user_456"]
  }
}
```

#### `meeting.started`
Meeting started
```json
{
  "event_type": "meeting.started",
  "data": {
    "meeting_id": "mtg_123",
    "signalling_server": "ws://localhost:8080"
  }
}
```

#### `meeting.ended`
Meeting ended
```json
{
  "event_type": "meeting.ended",
  "data": {
    "meeting_id": "mtg_123",
    "duration_seconds": 3600,
    "participants_final": ["user_123", "user_456"]
  }
}
```

---

### User Events (`user.*`)

#### `user.created`
New user registered
```json
{
  "event_type": "user.created",
  "data": {
    "user_id": "user_123",
    "email": "new@example.com",
    "name": "New User"
  }
}
```

#### `user.updated`
User profile updated
```json
{
  "event_type": "user.updated",
  "data": {
    "user_id": "user_123",
    "fields_changed": ["name", "avatar"]
  }
}
```

#### `user.deleted`
User account deleted
```json
{
  "event_type": "user.deleted",
  "data": {
    "user_id": "user_123"
  }
}
```

---

### Organization Events (`org.*`)

#### `org.created`
New organization created
```json
{
  "event_type": "org.created",
  "data": {
    "org_id": "org_123",
    "name": "Acme Corp",
    "created_by": "user_456"
  }
}
```

#### `org.member.invited`
User invited to organization
```json
{
  "event_type": "org.member.invited",
  "data": {
    "org_id": "org_123",
    "invited_email": "user@example.com",
    "invited_by": "user_456"
  }
}
```

#### `org.member.joined`
User joined organization
```json
{
  "event_type": "org.member.joined",
  "data": {
    "org_id": "org_123",
    "user_id": "user_789"
  }
}
```

---

## Redis Channels

Events are published to Redis Pub/Sub under these channels:

| Channel | Events |
|---------|--------|
| `auth.*` | Authentication events |
| `project.*` | Project management events |
| `calendar.*` | Calendar events |
| `mail.*` | Email events |
| `meeting.*` | Meeting/Video events |
| `user.*` | User account events |
| `org.*` | Organization events |
| `ecosystem.broadcast` | Cross-service announcements |

## Consuming Events

### Example: Node.js/Express

```javascript
const redis = require('redis');

async function subscribeToEvents() {
  const client = redis.createClient({ url: 'redis://localhost:6379' });
  await client.connect();
  
  const subscriber = client.duplicate();
  await subscriber.connect();
  
  // Subscribe to calendar events
  await subscriber.subscribe('calendar.*', (message) => {
    const event = JSON.parse(message);
    console.log('Calendar event:', event);
    
    if (event.event_type === 'calendar.event.created') {
      // Handle new event
    }
  });
}
```

### Example: Python/FastAPI

```python
import redis
import json
import asyncio

async def consume_events():
    r = redis.from_url('redis://localhost:6379')
    p = r.pubsub()
    
    p.psubscribe('calendar.*')
    
    for message in p.listen():
        if message['type'] == 'pmessage':
            event = json.loads(message['data'])
            print('Calendar event:', event)
            
            if event['event_type'] == 'calendar.event.created':
                # Handle new event
                pass
```

---

## Publishing Events

All services MUST publish events following this pattern when:

- ✅ Resource creation succeeds
- ✅ Resource update succeeds
- ✅ Resource deletion succeeds
- ✅ User authentication/logout occurs
- ❌ Do NOT publish on validation errors
- ❌ Do NOT publish on authorization failures (for privacy)

## Best Practices

1. **Always include org_id** - For multi-tenant filtering
2. **Use ISO 8601 timestamps** - UTC timezone only
3. **Semantic event types** - `resource.action` format only
4. **Immutable event data** - Never modify published events
5. **Retry on failure** - Implement exponential backoff for publishing
6. **Audit critical events** - Log all auth, user, org changes
7. **Filter sensitively** - Don't expose passwords, tokens in events

---

## Event Processing Order Guarantees

- Events are published in the order they occur
- Services should NOT assume real-time delivery
- Use event timestamps, not receive time
- Implement idempotent event handlers (handle duplicates gracefully)

---

Last updated: 2026-03-01
Version: 1.0
