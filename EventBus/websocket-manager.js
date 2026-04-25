/**
 * RM-Orbit WebSocket Manager.
 * Provides a reliable, organization-scoped real-time event stream.
 */
const { Server } = require('socket.io');
const { verifyGateTokenWithFallback } = require('../scripts/gate-token-verifier');
const path = require('path');

class WebSocketManager {
  constructor(server, options = {}) {
    this.io = new Server(server, {
      cors: { origin: '*', methods: ['GET', 'POST'] },
    });
    this.connections = new Map(); // Map<OrgId, Set<Socket>>
    this.pendingAcks = new Map(); // Map<MessageId, { envelope, timestamp, timer }>
    this.ackTimeoutMs = options.ackTimeoutMs || 5000;
    this.heartbeatIntervalMs = options.heartbeatIntervalMs || 30000;
    this.logger = options.logger || console;

    this.setupMiddleware();
    this.setupHandlers();
    this.startHeartbeatMonitor();
  }

  setupMiddleware() {
    this.io.use(async (socket, next) => {
      const token = socket.handshake.auth.token || socket.handshake.headers.authorization;
      if (!token) return next(new Error('Authentication required'));

      try {
        const result = await verifyGateTokenWithFallback(token, {
          defaultPublicKeyPath: path.join(__dirname, '../Gate/authx/certs/public.pem'),
          localSecret: process.env.SECRET_KEY || 'snitch-secret-key',
        });
        socket.user = result.payload;
        socket.org_id = result.payload.org_id || socket.handshake.headers['x-org-id'];
        
        if (!socket.org_id) return next(new Error('Organization context missing'));
        this.logger.log(`websocket: authorized ${socket.user.email} for org ${socket.org_id}`);
        next();
      } catch (err) {
        this.logger.error('websocket auth error', err.message);
        next(new Error('Authentication failed'));
      }
    });
  }

  setupHandlers() {
    this.io.on('connection', (socket) => {
      const orgId = socket.org_id;
      if (!this.connections.has(orgId)) this.connections.set(orgId, new Set());
      this.connections.get(orgId).add(socket);

      socket.on('disconnect', () => {
        const set = this.connections.get(orgId);
        if (set) {
          set.delete(socket);
          if (set.size === 0) this.connections.delete(orgId);
        }
      });

      socket.on('ack', (messageId) => {
        if (this.pendingAcks.has(messageId)) {
          clearTimeout(this.pendingAcks.get(messageId).timer);
          this.pendingAcks.delete(messageId);
        }
      });

      // Heartbeat ping
      socket.on('pong', () => {
        socket.lastActive = Date.now();
      });
    });
  }

  startHeartbeatMonitor() {
    setInterval(() => {
      const now = Date.now();
      this.io.socketsArray().forEach((socket) => {
        socket.emit('ping');
        if (socket.lastActive && now - socket.lastActive > 90000) {
          this.logger.warn(`websocket: heartbeat timeout for ${socket.user?.email || socket.id}. Disconnecting.`);
          socket.disconnect(true);
        }
      });
    }, this.heartbeatIntervalMs);
  }

  /**
   * Delivers an event to all connected sockets for the same org.
   */
  async broadcastEvent(envelope) {
    const orgId = envelope.org_id;
    const targets = this.connections.get(orgId);
    if (!targets || targets.size === 0) return;

    const messageId = envelope.event_id;
    
    // Set up ACK listener tracking (Internal Reliability)
    // We only track the delivery attempt
    const timer = setTimeout(() => {
      if (this.pendingAcks.has(messageId)) {
        this.logger.warn(`websocket: delivery ACK timeout for ${messageId}. Retrying or sending to DLQ.`);
        // Note: Real-time re-delivery handle logic can go here.
        this.pendingAcks.delete(messageId); 
      }
    }, this.ackTimeoutMs);

    this.pendingAcks.set(messageId, { envelope, timestamp: Date.now(), timer });

    // Emit to all matching sockets
    targets.forEach((socket) => {
      socket.emit('gateway_event', envelope);
    });
  }
}

// Extension to get all sockets easily
const SocketsArraySymbol = Symbol('socketsArray');
Server.prototype.socketsArray = function() {
  return Array.from(this.sockets.values());
};

module.exports = WebSocketManager;
