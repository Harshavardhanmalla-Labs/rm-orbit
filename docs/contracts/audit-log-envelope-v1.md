# Audit Log Envelope Contract (v1)

Status: Active baseline  
Date: 2026-03-01

## Purpose

Define a shared structured audit-log record shape for Orbit HTTP services so logs can be correlated by request, org, and workspace.

## Required Fields

- `timestamp` (ISO-8601 UTC)
- `record_type` (`audit_log`)
- `service` (service identifier)
- `event` (`http.request` for request logs)
- `request_id` (correlation id; stable for request lifecycle)
- `method` (HTTP method)
- `path` (request path or URL)
- `status_code` (integer)
- `duration_ms` (integer)

## Context Fields

- `org_id` (nullable string)
- `workspace_id` (nullable string)
- `user_id` (nullable string)

## Optional Fields

- `extra` (object for non-core metadata, e.g., query string)

## Correlation Rules

1. Services must set `X-Request-Id` on responses.
2. If inbound `X-Request-Id` exists, preserve it.
3. If missing, generate a new request id.
4. Log records for the request must include the same `request_id`.

## Current Baseline Adopters

- Writer backend (FastAPI middleware)
- Search aggregator backend (FastAPI middleware)
- Meet backend (Express middleware)

## Example

```json
{
  "timestamp": "2026-03-01T18:10:12.101Z",
  "record_type": "audit_log",
  "service": "writer-backend",
  "event": "http.request",
  "request_id": "9cb3f5d6-2a4b-4de6-9215-8c2cc4f8a20b",
  "method": "POST",
  "path": "/api/documents",
  "status_code": 201,
  "duration_ms": 24,
  "org_id": "org-1",
  "workspace_id": "ws-1",
  "user_id": "u-1",
  "extra": {
    "query": ""
  }
}
```
