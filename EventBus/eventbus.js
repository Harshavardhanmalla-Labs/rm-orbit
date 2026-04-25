const express = require('express');
const http = require('http');
const redis = require('redis');
const cors = require('cors');
const { validateEvent, generateTypescriptDefinitions } = require('./event-schemas');
const { runRetentionPolicy } = require('./event-store');
const eventRouter = require('./event-router');
const WebSocketManager = require('./websocket-manager');
const requireOrg = require('./org-middleware');
const requireAuth = require('./auth-middleware');
const { enforceTenantContext } = require('./tenant-context');

const app = express();
const server = http.createServer(app);
const wsManager = new WebSocketManager(server);

app.use(cors());
app.use(express.json());

const redisClient = redis.createClient({ url: process.env.REDIS_URL || 'redis://localhost:6379' });
redisClient.connect().catch(console.error);

const SNITCH_INTERNAL_TOKEN = String(process.env.SNITCH_INTERNAL_TOKEN || '').trim();

function requireInternalToken(req, res, next) {
  const supplied = req.get('X-Internal-Token');
  if (SNITCH_INTERNAL_TOKEN && supplied !== SNITCH_INTERNAL_TOKEN) {
    return res.status(403).json({ error: 'Invalid internal token' });
  }
  return next();
}

/**
 * Publishes an event into the ecosystem.
 * All events flow through this endpoint (or sink).
 */
app.post('/publish', requireOrg, requireAuth, enforceTenantContext, async (req, res) => {
  const envelope = req.body;
  
  // 1. Schema Validation
  const validation = validateEvent(envelope);
  if (!validation.valid) {
    return res.status(400).json({ 
      error: 'Schema validation failed', 
      context: validation.context,
      details: validation.errors 
    });
  }

  // 2. Routing & Persistence
  const result = await eventRouter.route(envelope);
  
  // 3. WebSocket Real-time Broadcast
  wsManager.broadcastEvent(envelope);

  res.json({ status: 'ok', event_id: envelope.event_id, routing: result });
});

/**
 * Ingestion Sink (Legacy Compatibility)
 */
app.post(['/sink', '/ingest'], requireInternalToken, async (req, res) => {
  const envelope = req.body;
  // Automatically validate and route
  const validation = validateEvent(envelope);
  if (!validation.valid) {
    return res.status(400).json({ error: 'Invalid sink payload' });
  }

  await eventRouter.route(envelope);
  wsManager.broadcastEvent(envelope);
  
  res.json({ status: 'sinked', event_id: envelope.event_id });
});

/**
 * Typescript Definitions Generation
 */
app.get('/protocol/typescript', (req, res) => {
  const ts = generateTypescriptDefinitions();
  res.setHeader('Content-Type', 'text/plain');
  res.send(ts);
});

/**
 * Monitoring Dashboard Metadata
 */
app.get('/stats', (req, res) => {
  res.json({
    active_connections: wsManager.connections.size,
    pending_acks: wsManager.pendingAcks.size,
    dlq_size: eventRouter.getDLQ().length,
    timestamp: new Date().toISOString(),
  });
});

app.get('/health', (req, res) => res.json({ status: 'eventbus production ok' }));

/**
 * Maintenance Cron (Simulated via setInterval)
 */
setInterval(() => {
  runRetentionPolicy(30).catch(() => {});
}, 3600000); // Hourly

const PORT = process.env.PORT || 6005;
server.listen(PORT, () => console.log(`🚀 RM-Orbit Event Bus listening on ${PORT}`));

// Topic Subscription Hook (Internal Bridge)
// This enables the router to reach WS manager
eventRouter.subscribe('*', (envelope) => {
  wsManager.broadcastEvent(envelope);
});
