const fetch = require('node-fetch');

const ATLAS_INTERNAL_TOKEN = process.env.ATLAS_INTERNAL_TOKEN || '';
const ATLAS_API_BASE_URL = process.env.ATLAS_API_BASE_URL || 'http://atlas-backend:8000';
const DEFAULT_ATLAS_PROJECT_ID = process.env.DEFAULT_ATLAS_PROJECT_ID || 'default_project';

async function createAtlasTask(orgId, payload) {
  if (!ATLAS_API_BASE_URL) return { error: 'Atlas API not configured' };

  const url = `${ATLAS_API_BASE_URL}/api/v1/internal/tasks`;
  const headers = {
    'Content-Type': 'application/json',
    'X-Org-Id': orgId,
    'X-Internal-Token': ATLAS_INTERNAL_TOKEN
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload)
    });
    return { status: response.status, ok: response.ok };
  } catch (err) {
    return { error: err.message };
  }
}

async function runAutomations(envelope, channel, severity) {
  const results = [];

  // Automation 1: TurboTick -> Atlas Bridge
  // Trigger on high/critical tickets
  if (channel === 'turbotick.alerts' && (severity === 'critical' || severity === 'high')) {
    const ticketId = envelope.payload?.ticket_id || envelope.payload?.id;
    if (ticketId) {
      const atlasPayload = {
        project_id: envelope.payload?.project_id || DEFAULT_ATLAS_PROJECT_ID,
        title: `[TICKET-${ticketId}] ${envelope.payload?.title || 'External Issue'}`,
        description: `Automated task from TurboTick ticket ${ticketId}.\n\nDescription: ${envelope.payload?.description || ''}`,
        priority: severity,
        external_ref: `turbotick:${ticketId}`,
        created_by: envelope.user_id || 'system'
      };
      
      const bridgeResult = await createAtlasTask(envelope.org_id, atlasPayload);
      results.push({ automation: 'turbotick_atlas_bridge', result: bridgeResult });
    }
  }

  // Automation 2: External Webhook Relay
  const webhookUrl = process.env.EXTERNAL_WEBHOOK_URL;
  if (webhookUrl && (severity === 'critical')) {
    try {
      await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert: 'CRITICAL_EVENT',
          org_id: envelope.org_id,
          source: envelope.source,
          message: envelope.payload?.message || envelope.payload?.description || 'Critical event detected'
        })
      });
      results.push({ automation: 'external_webhook', result: 'sent' });
    } catch (err) {
      results.push({ automation: 'external_webhook', error: err.message });
    }
  }

  return results;
}

module.exports = { runAutomations };
