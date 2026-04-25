const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres_secret',
  database: process.env.DB_NAME || 'rm_eventbus',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

/**
 * Persists an event envelope to PostgreSQL.
 */
async function saveEvent(envelope) {
  const query = `
    INSERT INTO events (
      id, event_type, payload, org_id, user_id, source, timestamp, schema_version
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
  `;
  const values = [
    envelope.event_id,
    envelope.event_type,
    JSON.stringify(envelope.data),
    envelope.org_id,
    envelope.user_id,
    envelope.source,
    envelope.timestamp || new Date().toISOString(),
    envelope.schema_version || 1,
  ];

  try {
    await pool.query(query, values);
    return true;
  } catch (err) {
    console.error('event-store save error', err);
    return false;
  }
}

/**
 * Retrieves events for replay.
 */
async function getEventsForReplay(options = {}) {
  const { org_id, event_type, days = 7, limit = 1000 } = options;
  let query = 'SELECT * FROM events WHERE timestamp > NOW() - INTERVAL \'$1 days\'';
  const values = [days];

  if (org_id) {
    query += ` AND org_id = $${values.length + 1}`;
    values.push(org_id);
  }
  if (event_type) {
    query += ` AND event_type = $${values.length + 1}`;
    values.push(event_type);
  }

  query += ` ORDER BY timestamp ASC LIMIT $${values.length + 1}`;
  values.push(limit);

  try {
    const res = await pool.query(query, values);
    return res.rows.map(row => ({
      event_id: row.id,
      event_type: row.event_type,
      org_id: row.org_id,
      user_id: row.user_id,
      source: row.source,
      timestamp: row.timestamp,
      schema_version: row.schema_version,
      data: row.payload,
    }));
  } catch (err) {
    console.error('event-store replay query error', err);
    return [];
  }
}

/**
 * Archives/Deletes old events based on retention policy.
 */
async function runRetentionPolicy(days = 30) {
  const query = 'DELETE FROM events WHERE timestamp < NOW() - INTERVAL \'$1 days\'';
  try {
    const res = await pool.query(query, [days]);
    console.log(`event-store retention: removed ${res.rowCount} old events`);
  } catch (err) {
    // ignore
  }
}

module.exports = {
  saveEvent,
  getEventsForReplay,
  runRetentionPolicy,
};
