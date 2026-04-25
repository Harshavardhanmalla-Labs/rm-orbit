const { randomUUID } = require('node:crypto');

function isObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function normalizeSchemaVersion(value) {
  const parsed = Number.parseInt(value, 10);
  if (Number.isFinite(parsed) && parsed > 0) {
    return parsed;
  }
  return 1;
}

function buildSnitchEventEnvelope(channel, event = {}, options = {}) {
  const payload = isObject(event) ? { ...event } : {};
  const nestedData = isObject(payload.data) ? { ...payload.data } : {};

  const eventType =
    options.event_type ||
    options.eventType ||
    payload.event_type ||
    payload.eventType ||
    payload.event ||
    payload.type ||
    channel;

  const source = options.source || payload.source || 'snitch';

  const orgId =
    options.org_id ||
    options.orgId ||
    payload.org_id ||
    payload.orgId ||
    nestedData.org_id ||
    nestedData.orgId ||
    null;

  const userId =
    options.user_id ||
    options.userId ||
    payload.user_id ||
    payload.userId ||
    payload.sub ||
    nestedData.user_id ||
    nestedData.userId ||
    null;

  const schemaVersion =
    options.schema_version ||
    options.schemaVersion ||
    payload.schema_version ||
    payload.schemaVersion ||
    nestedData.schema_version ||
    nestedData.schemaVersion;

  return {
    ...payload,
    timestamp: payload.timestamp || new Date().toISOString(),
    source,
    event_type: eventType,
    schema_version: normalizeSchemaVersion(schemaVersion),
    event_id:
      payload.event_id ||
      payload.eventId ||
      nestedData.event_id ||
      nestedData.eventId ||
      randomUUID(),
    org_id: orgId,
    user_id: userId,
    data: nestedData,
  };
}

module.exports = {
  buildSnitchEventEnvelope,
  normalizeSchemaVersion,
};
