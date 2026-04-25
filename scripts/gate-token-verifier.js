const fs = require('fs');
const crypto = require('crypto');
const { createRequire } = require('module');

let jwtLib = null;
const localKeyCache = new Map();
const jwksCache = new Map();

function envBool(name, defaultValue) {
  const value = process.env[name];
  if (value === undefined) {
    return defaultValue;
  }
  return ['1', 'true', 'yes', 'on'].includes(String(value).trim().toLowerCase());
}

function firstEnv(...names) {
  for (const name of names) {
    const value = process.env[name];
    if (value !== undefined && String(value).trim() !== '') {
      return String(value).trim();
    }
  }
  return '';
}

function getJwtLib() {
  if (jwtLib) {
    return jwtLib;
  }
  try {
    jwtLib = require('jsonwebtoken');
    return jwtLib;
  } catch (_err) {
    // Fallback for monorepo service execution where deps live under service cwd.
    const cwdRequire = createRequire(`${process.cwd()}/`);
    jwtLib = cwdRequire('jsonwebtoken');
  }
  return jwtLib;
}

function normalizeAudience(audienceClaim) {
  if (Array.isArray(audienceClaim)) {
    return audienceClaim.map((value) => String(value));
  }
  if (typeof audienceClaim === 'string' && audienceClaim.trim() !== '') {
    return [audienceClaim.trim()];
  }
  return [];
}

function validateIssuerAndAudience(payload) {
  const expectedIssuer = firstEnv('GATE_EXPECTED_ISSUER');
  if (expectedIssuer) {
    const issuer = typeof payload.iss === 'string' ? payload.iss : '';
    if (issuer !== expectedIssuer) {
      throw new Error(`Invalid token issuer: expected '${expectedIssuer}'`);
    }
  }

  const expectedAudience = firstEnv('GATE_EXPECTED_AUDIENCE');
  if (!expectedAudience) {
    return;
  }

  const audiences = normalizeAudience(payload.aud);
  if (audiences.includes(expectedAudience)) {
    return;
  }

  const allowClientIdFallback = envBool('ALLOW_CLIENT_ID_AUDIENCE_FALLBACK', true);
  if (allowClientIdFallback && payload.client_id === expectedAudience) {
    return;
  }

  throw new Error(`Invalid token audience: expected '${expectedAudience}'`);
}

function getLocalPublicKey(defaultPath) {
  const keyPath = firstEnv('GATE_PUBLIC_KEY_PATH') || defaultPath;
  if (!keyPath) {
    return null;
  }

  if (localKeyCache.has(keyPath)) {
    return localKeyCache.get(keyPath);
  }

  try {
    if (fs.existsSync(keyPath)) {
      const key = fs.readFileSync(keyPath, 'utf8');
      localKeyCache.set(keyPath, key);
      return key;
    }
    console.error(`[Gate] Public key file not found at configured path: ${keyPath}`);
  } catch (_err) {
    console.error(`[Gate] Failed to read public key file: ${keyPath}`);
    return null;
  }

  return null;
}

function jwkToPem(jwk) {
  return crypto
    .createPublicKey({ key: jwk, format: 'jwk' })
    .export({ type: 'spki', format: 'pem' })
    .toString();
}

async function fetchJson(url, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`JWKS fetch failed with ${response.status}`);
    }
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

async function getJwksEntries(jwksUrl) {
  const now = Date.now();
  const cached = jwksCache.get(jwksUrl);
  if (cached && cached.expiresAt > now) {
    return cached.entries;
  }

  const timeoutMs = Number.parseInt(process.env.GATE_JWKS_TIMEOUT_MS || '2000', 10);
  const ttlMs = Number.parseInt(process.env.GATE_JWKS_CACHE_TTL_MS || '300000', 10);
  const body = await fetchJson(jwksUrl, timeoutMs);
  const keys = Array.isArray(body?.keys) ? body.keys : [];
  const entries = keys
    .filter((key) => key && key.kty === 'RSA' && key.n && key.e)
    .map((key) => ({
      kid: typeof key.kid === 'string' ? key.kid : '',
      pem: jwkToPem(key),
    }));

  if (!entries.length) {
    throw new Error('JWKS payload did not include RSA signing keys');
  }

  jwksCache.set(jwksUrl, { entries, expiresAt: now + ttlMs });
  return entries;
}

async function verifyWithJwks(token, jwt, jwksUrl) {
  const decoded = jwt.decode(token, { complete: true }) || {};
  const header = decoded.header || {};
  const tokenKid = typeof header.kid === 'string' ? header.kid : '';

  const entries = await getJwksEntries(jwksUrl);
  const ordered = [];
  if (tokenKid) {
    const preferred = entries.find((entry) => entry.kid === tokenKid);
    if (preferred) {
      ordered.push(preferred);
    }
  }
  for (const entry of entries) {
    if (ordered.includes(entry)) {
      continue;
    }
    ordered.push(entry);
  }

  let lastError = null;
  for (const entry of ordered) {
    try {
      return jwt.verify(token, entry.pem, { algorithms: ['RS256'] });
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError || new Error('RS256 verification failed for all JWKS keys');
}

async function verifyGateTokenWithFallback(token, options = {}) {
  const jwt = getJwtLib();
  const normalizePayload = options.normalizePayload || ((payload) => payload);
  const allowLocalHsFallback = envBool(
    'ALLOW_LOCAL_HS256_FALLBACK',
    process.env.NODE_ENV !== 'production'
  );
  const localSecret =
    options.localSecret ||
    process.env.SECRET_KEY ||
    process.env.JWT_SECRET ||
    'dev-secret-key';
  const defaultPublicKeyPath = options.defaultPublicKeyPath || '';
  const useJwks = envBool('GATE_USE_JWKS', true);
  const jwksUrl = firstEnv('GATE_JWKS_URL', 'GATE_JWKS_URI');

  if (useJwks && jwksUrl) {
    try {
      const payload = verifyWithJwks(token, jwt, jwksUrl);
      const resolved = await payload;
      validateIssuerAndAudience(resolved);
      return { payload: normalizePayload(resolved), source: 'jwks' };
    } catch (_err) {
      // fall through to local public key and local HS256 fallback
    }
  }

  const gateKey = getLocalPublicKey(defaultPublicKeyPath);
  if (gateKey) {
    try {
      const payload = jwt.verify(token, gateKey, { algorithms: ['RS256'] });
      validateIssuerAndAudience(payload);
      return { payload: normalizePayload(payload), source: 'pem' };
    } catch (_err) {
      // fall through to local HS256 fallback
    }
  }

  if (!allowLocalHsFallback) {
    throw new Error('RS256 verification failed and local HS256 fallback is disabled');
  }

  const payload = jwt.verify(token, localSecret, { algorithms: ['HS256'] });
  validateIssuerAndAudience(payload);
  return { payload: normalizePayload(payload), source: 'hs256' };
}

module.exports = {
  verifyGateTokenWithFallback,
  validateIssuerAndAudience,
  envBool,
};
