let sessionIdCache = null;

export function getSessionId() {
  if (sessionIdCache) return sessionIdCache;

  let sessionId = sessionStorage.getItem('decision_session_id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('decision_session_id', sessionId);
  }
  sessionIdCache = sessionId;
  return sessionId;
}

export function generateDecisionId() {
  return `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function trackEvent(eventName, value = null, decisionId = null) {
  const event = {
    event_name: eventName,
    timestamp: new Date().toISOString(),
    session_id: getSessionId(),
    decision_id: decisionId,
    value: value,
  };

  console.log('[Analytics]', event);

  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/events', JSON.stringify(event));
  } else {
    fetch('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
      keepalive: true,
    }).catch(() => {});
  }
}
