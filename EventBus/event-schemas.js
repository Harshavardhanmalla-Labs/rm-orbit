/**
 * RM-Orbit Ecosystem Event Protocol (v1)
 * This file defines the specific message schemas for all applications
 * and enforces structural consistency across the event bus.
 */
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv({ allErrors: true, removeAdditional: false });
addFormats(ajv);

// ─── Base Envelope Schema ───────────────────────────────────────────
const baseEnvelopeSchema = {
  type: 'object',
  required: ['event_id', 'event_type', 'org_id', 'source', 'data'],
  properties: {
    event_id: { type: 'string', format: 'uuid' },
    event_type: { type: 'string', minLength: 3 },
    org_id: { type: 'string' },
    user_id: { type: ['string', 'null'] },
    source: { type: 'string' },
    timestamp: { type: 'string', format: 'date-time' },
    schema_version: { type: 'number', minimum: 1 },
    data: { type: 'object' },
  },
};

// ─── Application-Specific Payloads ─────────────────────────────────
const schemas = {
  // Atlas (Project Management)
  'atlas.task.created': {
    type: 'object',
    required: ['task_id', 'title', 'workspace_id'],
    properties: {
      task_id: { type: 'string' },
      title: { type: 'string' },
      workspace_id: { type: 'string' },
      priority: { enum: ['low', 'medium', 'high', 'critical'] },
    },
  },
  'atlas.task.updated': {
    type: 'object',
    required: ['task_id', 'changes'],
    properties: {
      task_id: { type: 'string' },
      changes: { type: 'object' },
    },
  },

  // Connect (Messaging)
  'connect.message.sent': {
    type: 'object',
    required: ['channel_id', 'message_id', 'content'],
    properties: {
      channel_id: { type: 'string' },
      message_id: { type: 'string' },
      content: { type: 'string' },
      sender_id: { type: 'string' },
    },
  },

  // Meet (Video Conferencing)
  'meet.call.started': {
    type: 'object',
    required: ['room_id', 'host_id'],
    properties: {
      room_id: { type: 'string' },
      host_id: { type: 'string' },
      topic: { type: 'string' },
    },
  },

  // Mail
  'mail.email.received': {
    type: 'object',
    required: ['message_id', 'from', 'to', 'subject'],
    properties: {
      message_id: { type: 'string' },
      from: { type: 'string' },
      to: { type: 'string' },
      subject: { type: 'string' },
    },
  },

  // Planet (CRM)
  'planet.deal.created': {
    type: 'object',
    required: ['deal_id', 'value', 'currency'],
    properties: {
      deal_id: { type: 'string' },
      value: { type: 'number' },
      currency: { type: 'string', minLength: 3, maxLength: 3 },
      stage: { type: 'string' },
    },
  },

  // Learn
  'learn.article.published': {
    type: 'object',
    required: ['article_id', 'title', 'slug'],
    properties: {
      article_id: { type: 'string' },
      title: { type: 'string' },
      slug: { type: 'string' },
    },
  },
};

// Compile all schemas
const validators = {};
for (const [type, schema] of Object.entries(schemas)) {
  validators[type] = ajv.compile(schema);
}

const baseValidator = ajv.compile(baseEnvelopeSchema);

/**
 * Validates an ecosystem event envelope and its data payload.
 */
function validateEvent(envelope) {
  // 1. Validate envelope structure
  if (!baseValidator(envelope)) {
    return { valid: false, errors: baseValidator.errors, context: 'envelope' };
  }

  // 2. Validate data payload if schema exists for this type
  const type = envelope.event_type;
  if (validators[type]) {
    const dataValid = validators[type](envelope.data);
    if (!dataValid) {
      return { valid: false, errors: validators[type].errors, context: 'payload' };
    }
  }

  return { valid: true };
}

// ─── TypeScript Definitions Generation (Simulated) ──────────────────
function generateTypescriptDefinitions() {
  let output = '/** Automatically generated from event-schemas.js */\n\n';
  output += 'export interface OrbitEventEnvelope<T = any> {\n';
  output += '  event_id: string;\n';
  output += '  event_type: string;\n';
  output += '  org_id: string;\n';
  output += '  user_id: string | null;\n';
  output += '  source: string;\n';
  output += '  timestamp: string;\n';
  output += '  schema_version: number;\n';
  output += '  data: T;\n';
  output += '}\n\n';

  for (const [type, schema] of Object.entries(schemas)) {
    const interfaceName = type.split('.').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('') + 'Data';
    output += `export interface ${interfaceName} {\n`;
    for (const [prop, meta] of Object.entries(schema.properties)) {
      const typeStr = meta.type === 'number' ? 'number' : (meta.enum ? meta.enum.map(e => `'${e}'`).join(' | ') : 'string');
      const optional = schema.required.includes(prop) ? '' : '?';
      output += `  ${prop}${optional}: ${typeStr};\n`;
    }
    output += '}\n\n';
  }

  return output;
}

module.exports = {
  validateEvent,
  generateTypescriptDefinitions,
  eventTypes: Object.keys(schemas),
};
