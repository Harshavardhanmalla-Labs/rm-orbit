const { randomUUID } = require('node:crypto');

function isoNow() {
  return new Date().toISOString();
}

function resolveRequestId(req) {
  return req.get('X-Request-Id') || randomUUID();
}

function buildAuditRecord({
  service,
  event,
  requestId,
  method,
  path,
  statusCode,
  durationMs,
  orgId = null,
  workspaceId = null,
  userId = null,
  extra = null,
}) {
  const record = {
    timestamp: isoNow(),
    record_type: 'audit_log',
    service,
    event,
    request_id: requestId,
    method,
    path,
    status_code: Number(statusCode || 0),
    duration_ms: Number(durationMs || 0),
    org_id: orgId,
    workspace_id: workspaceId,
    user_id: userId,
  };
  if (extra) {
    record.extra = extra;
  }
  return record;
}

function emitAudit(record) {
  console.log(JSON.stringify(record));
}

module.exports = {
  resolveRequestId,
  buildAuditRecord,
  emitAudit,
};
