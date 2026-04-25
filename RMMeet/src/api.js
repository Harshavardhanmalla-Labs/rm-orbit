/**
 * api.js — Guest session endpoint wrapper.
 *
 * POST /api/guest/session
 *   Body: { name, email?, orgId? }
 *   Returns: { token, user: { id, name, org_id } }
 *
 * The token is a short-lived JWT signed by the Meet backend with role=guest.
 * It is passed in socket.io auth so the backend can verify identity without
 * requiring a full Gate (AuthX) account.
 */

const BACKEND_BASE = '/api';

/**
 * Create a guest session.
 * @param {{ name: string, email?: string, orgId?: string }} params
 * @returns {Promise<{ token: string, user: { id: string, name: string, org_id: string } }>}
 */
export async function createGuestSession({ name, email, orgId } = {}) {
  const body = { name: name.trim() };
  if (email) body.email = email.trim();
  if (orgId) body.orgId = orgId.trim();

  const response = await fetch(`${BACKEND_BASE}/guest/session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    let message = `Guest session failed (${response.status})`;
    try {
      const json = await response.json();
      message = json.error || json.message || message;
    } catch {
      // ignore parse error
    }
    throw new Error(message);
  }

  const data = await response.json();

  if (!data.token) {
    throw new Error('Backend did not return a session token. Make sure the /api/guest/session route is implemented.');
  }

  return data;
}
