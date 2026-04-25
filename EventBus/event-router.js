/**
 * RM-Orbit Event Routing Engine.
 * Handles fan-out, wildcard subscriptions, and reliable delivery (DLQ).
 */
const { saveEvent } = require('./event-store');

class EventRouter {
  constructor(options = {}) {
    this.subscriptions = new Map(); // Map<TopicPattern, Set<Subscriber>>
    this.dlq = []; // Dead Letter Queue for failed deliveries (internal)
    this.maxRetries = options.maxRetries || 3;
    this.logger = options.logger || console;
  }

  /**
   * Subscribes a listener to a topic pattern (supports wildcards like *).
   * @param {string} pattern E.g. "atlas.*" or "mail.email.received"
   * @param {function} listener Delivery callback
   */
  subscribe(pattern, listener) {
    if (!this.subscriptions.has(pattern)) {
      this.subscriptions.set(pattern, new Set());
    }
    this.subscriptions.get(pattern).add(listener);
    this.logger.log(`event-router: subscribed to pattern ${pattern}`);
  }

  /**
   * Unsubscribes a listener.
   */
  unsubscribe(pattern, listener) {
    const set = this.subscriptions.get(pattern);
    if (set) {
      set.delete(listener);
      if (set.size === 0) {
        this.subscriptions.delete(pattern);
      }
    }
  }

  /**
   * Checks if an event type matches a pattern.
   * "atlas.task.created" matches "atlas.*" and "atlas.task.created".
   */
  matches(eventType, pattern) {
    if (pattern === '*' || pattern === '#') return true;
    if (pattern === eventType) return true;

    // Convert pattern to regex
    // "atlas.*" -> /^atlas\.[^.]+$/
    // "atlas.#" -> /^atlas\..+$/ (NOT standard in this case, but let's support * as simple segment wildcard)
    const regexStr = '^' + pattern.replace(/\./g, '\\.').replace(/\*/g, '[^.]+') + '$';
    const regex = new RegExp(regexStr);
    return regex.test(eventType);
  }

  /**
   * Routes an event to all matching subscribers.
   */
  async route(envelope) {
    const { event_type: eventType, event_id: eventId } = envelope;
    const subscribers = new Set();

    // 1. Persist first (Reliability)
    await saveEvent(envelope);

    // 2. Identify all matching subscribers
    for (const [pattern, listeners] of this.subscriptions.entries()) {
      if (this.matches(eventType, pattern)) {
        for (const listener of listeners) {
          subscribers.add(listener);
        }
      }
    }

    if (subscribers.size === 0) {
      this.logger.log(`event-router: no subscribers for ${eventType} (${eventId})`);
      return { status: 'no_subscribers' };
    }

    // 3. Fan-out delivery
    const tasks = Array.from(subscribers).map(listener => this.deliver(envelope, listener));
    await Promise.allSettled(tasks);

    return { status: 'routed', count: subscribers.size };
  }

  /**
   * Reliable delivery with retry and DLQ.
   */
  async deliver(envelope, listener, attempt = 1) {
    try {
      await listener(envelope);
    } catch (err) {
      if (attempt < this.maxRetries) {
        this.logger.warn(`event-router: delivery failed for ${envelope.event_id}, retry ${attempt + 1}/${this.maxRetries}`);
        // Wait 1s before retry
        await new Promise(r => setTimeout(r, 1000));
        return this.deliver(envelope, listener, attempt + 1);
      } else {
        this.logger.error(`event-router: delivery failed for ${envelope.event_id} after ${this.maxRetries} attempts. Sending to DLQ.`);
        this.dlq.push({
          envelope,
          failed_at: new Date().toISOString(),
          error: err?.message || 'unknown error',
        });
      }
    }
  }

  /**
   * Dead Letter Queue management.
   */
  getDLQ() {
    return [...this.dlq];
  }

  clearDLQ() {
    this.dlq = [];
  }
}

module.exports = new EventRouter();
