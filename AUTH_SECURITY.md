# RM Orbit Unified Authentication & Security

## Architecture Overview

RM Orbit uses a **centralized SSO** model with Gate (AuthX) as the identity provider for all applications.

```
┌─────────────────────────────────────────────────────┐
│                  Gate (AuthX)                       │
│         Central Identity Provider (OIDC/OAuth2)     │
│    - User accounts & credentials                    │
│    - Public/Private key pair (RS256)                │
│    - Client registration & management               │
└─────────────────────────────────────────────────────┘
              ↓                    ↓
    ┌─────────────────┐  ┌─────────────────┐
    │  Control Center │  │     Calendar    │
    │  (React + Gate) │  │  (Node + Gate)  │
    └─────────────────┘  └─────────────────┘
              ↓                    ↓
    ┌─────────────────┐  ┌─────────────────┐
    │     Atlas       │  │      Mail       │
    │  (FastAPI +RC)  │  │  (FastAPI +RC)  │
    └─────────────────┘  └─────────────────┘
```

---

## OAuth2 / OIDC Flow (PKCE)

### Client Setup (Gate)

All applications are registered as OAuth2 clients in Gate with PKCE support.

```bash
# Register a client
POST /auth/register-client
{
  "name": "control-center",
  "type": "confidential | public",
  "redirect_uris": ["http://localhost:3001/oauth-callback"],
  "scopes": ["openid", "profile", "email"],
  "grant_types": ["authorization_code", "refresh_token"]
}
```

### Protected Redirect URI Storage

```
Gate/.env
  CONTROL_CENTER_REDIRECT_URI=http://localhost:3001/oauth-callback
  CALENDAR_REDIRECT_URI=http://localhost:5173/oauth-callback
  ATLAS_REDIRECT_URI=http://localhost:8001/oauth-callback
  MAIL_REDIRECT_URI=http://localhost:8002/oauth-callback
```

### 1. User Initiates Login (Frontend)

```javascript
// Control Center example
const { login } = useAuth();

function handleLogin() {
  login(); // Initiates PKCE flow
}
```

### 2. Generate PKCE Challenge

```javascript
// Frontend generates and stores code verifier
function generateCodeVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return btoa(String.fromCharCode.apply(null, Array.from(array)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(hash))))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

const codeVerifier = generateCodeVerifier();
const codeChallenge = await generateCodeChallenge(codeVerifier);
sessionStorage.setItem('pkce_verifier', codeVerifier);
```

### 3. Authorization Request

```
GET http://localhost:8000/oauth/authorize?
  client_id=control-center
  &redirect_uri=http://localhost:3001/oauth-callback
  &response_type=code
  &scope=openid%20profile%20email
  &code_challenge=<SHA256_HASH>
  &code_challenge_method=S256
  &state=<RANDOM_STATE>
```

### 4. User Authenticates at Gate

- User provides credentials (email + password)
- Gate verifies in database
- Issues authorization code (5 min expiry)

### 5. Authorization Code Callback

```
GET http://localhost:3001/oauth-callback?
  code=AUTH_CODE_123
  &state=RANDOM_STATE
```

### 6. Token Exchange (Backend Only)

```javascript
// Frontend calls backend with code
POST /api/oauth/callback
{
  "code": "AUTH_CODE_123",
  "code_verifier": "PKCE_VERIFIER",
  "state": "RANDOM_STATE"
}

// Backend exchanges code for token
POST http://localhost:8000/oauth/token
{
  "grant_type": "authorization_code",
  "code": "AUTH_CODE_123",
  "client_id": "control-center",
  "redirect_uri": "http://localhost:3001/oauth-callback",
  "code_verifier": "PKCE_VERIFIER"
}

// Response
{
  "access_token": "eyJhbGc...",  // RS256 JWT
  "token_type": "Bearer",
  "expires_in": 28800,  // 8 hours
  "refresh_token": "refresh_eyJhbGc..."
}
```

### 7. JWT Payload (RS256)

```json
{
  "sub": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "org_id": "org_456",
  "iat": 1709298600,
  "exp": 1709327400,
  "iss": "http://localhost:8000",
  "aud": "control-center"
}
```

---

## Token Verification

### At Frontend

```javascript
// Store token
localStorage.setItem('auth_token', accessToken);

// Attach to API requests
const headers = {
  'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
  'X-Org-Id': userOrgId,
};
```

### At Backend

#### Method 1: RS256 with Gate Public Key (Recommended)

```python
# FastAPI/Python
from jose import jwt
import os

gate_public_key = open(os.getenv('GATE_PUBLIC_KEY_PATH')).read()

def verify_gate_token(token: str):
    payload = jwt.decode(token, gate_public_key, algorithms=['RS256'])
    return payload
```

#### Method 2: Introspection Endpoint (For Validation)

```bash
POST http://localhost:8000/oauth/introspect
Authorization: Basic base64(client_id:client_secret)

token=ACCESS_TOKEN

# Response
{
  "active": true,
  "sub": "user_123",
  "email": "user@example.com",
  "org_id": "org_456",
  "exp": 1709327400
}
```

#### Method 3: Hybrid (RS256 + Fallback)

```javascript
// Node.js
const jwt = require('jsonwebtoken');

function verifyToken(token) {
  try {
    // Try RS256 with Gate's public key
    const publicKey = fs.readFileSync('./Gate/authx/certs/public.pem');
    return jwt.verify(token, publicKey, { algorithms: ['RS256'] });
  } catch (err) {
    // Fallback to HS256 for local tokens
    return jwt.verify(token, process.env.SECRET_KEY, { algorithms: ['HS256'] });
  }
}
```

---

## Multi-Tenancy & Organization Access

### Organization Enforcement (All APIs)

```python
# Middleware in all services
def verify_org_access(request: Request):
    org_id = request.headers.get('X-Org-Id')
    if not org_id:
        raise HTTPException(status_code=400, detail="X-Org-Id required")
    
    token_org = request.user.get('org_id')
    if token_org and token_org != org_id:
        raise HTTPException(status_code=403, detail="Org mismatch")
    
    return org_id
```

### API Usage

```bash
# All requests must include organization header
GET http://localhost:8001/api/projects
Authorization: Bearer eyJhbGc...
X-Org-Id: org_456
```

---

## Token Refresh

### Short-lived Access Token Flow

```javascript
// Access token: 8 hours
// Refresh token: 30 days

// When access token expires:
POST http://localhost:8000/oauth/token
{
  "grant_type": "refresh_token",
  "refresh_token": "REFRESH_TOKEN",
  "client_id": "control-center"
}

// Get new access token
{
  "access_token": "NEW_ACCESS_TOKEN",
  "expires_in": 28800
}
```

### Frontend Token Refresh Interceptor

```javascript
// Add to API client
const api = axios.create({
  baseURL: process.env.VITE_API_URL,
});

api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await fetch(`${GATE_URL}/oauth/token`, {
          method: 'POST',
          body: JSON.stringify({
            grant_type: 'refresh_token',
            refresh_token: refreshToken,
            client_id: 'control-center',
          }),
        });
        
        const { access_token } = await response.json();
        localStorage.setItem('auth_token', access_token);
        
        // Retry original request
        error.config.headers.Authorization = `Bearer ${access_token}`;
        return api(error.config);
      } catch (err) {
        // Refresh failed, redirect to login
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);
```

---

## Service-to-Service Authentication

### Backend API Calls with JWT

```python
# Atlas backend calling Calendar API
import httpx

async def call_calendar_api():
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Org-Id': org_id,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'http://localhost:5001/api/events',
            headers=headers,
        )
```

### Microservice Token Persistence

For service-to-service calls, services can:

1. **Use client credentials** (2-legged OAuth)
   ```python
   # AtlasBackend → CalendarAPI
   token = await get_service_token('atlas', 'calendar')
   ```

2. **Forward user token** (preferred for audit)
   ```python
   # Pass user's token through
   headers = {
     'Authorization': f'Bearer {user_token}',
     'X-Org-Id': org_id,
   }
   ```

3. **Use service account**
   ```python
   # Register service account in Gate
   service_token = await gate.authenticate('service_account', secret)
   ```

---

## Logout & Session Termination

### Frontend Logout

```javascript
function handleLogout() {
  // Clear local storage
  localStorage.removeItem('auth_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('auth_user');
  
  // Notify gate (optional)
  fetch(`${GATE_URL}/oauth/logout`, {
    method: 'POST',
    body: JSON.stringify({
      refresh_token: oldRefreshToken,
    }),
  });
  
  // Redirect to login
  window.location.href = '/';
}
```

### Backend Session Cleanup

```python
@router.post('/logout')
async def logout(request: Request, user: User = Depends(get_current_user)):
    # Invalidate refresh token
    await db.revoke_token(user.id)
    
    # Publish logout event
    await publish_event('auth.logout', {
      'user_id': user.id,
      'timestamp': datetime.utcnow().isoformat(),
    })
    
    return {'status': 'logged_out'}
```

---

## Security Best Practices

✅ **DO**
- Store tokens in secure, HTTPOnly cookies (production)
- Use HTTPS only in production
- Validate `state` parameter in OAuth flow
- Implement PKCE for all clients
- Refresh tokens every 8 hours
- Include `X-Org-Id` on all requests
- Log all auth failures
- Rotate keys annually

❌ **DON'T**
- Store tokens in localStorage (XSS risk)
- Expose tokens in URLs
- Send tokens in logs
- Share tokens between users
- Disable HTTPS in production
- Hardcode secrets in code
- Skip state validation
- Cache tokens longer than 8 hours

---

## Gate Public Key Rotation

### Current Key Path

```
Gate/authx/certs/public.pem
```

### Key Rotation Procedure

1. Generate new key pair in Gate
2. Mark old key as deprecated (grace period)
3. Update all services with new public.pem
4. Monitor verification failures
5. Retire old key after grace period

### For Operators

```bash
# Generate new RS256 key pair
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# Update Gate
cp public.pem Gate/authx/certs/public.pem

# All services fetch new public key on startup
# or reload via environment variable
export GATE_PUBLIC_KEY_PATH=/path/to/new/public.pem
```

---

## Environment Variables Required

### Frontend (.env.local)
```
VITE_GATE_URL=http://localhost:8000
VITE_GATE_CLIENT_ID=control-center|calendar|...
VITE_API_URL=http://localhost:8001
```

### Backend (.env)
```
GATE_PUBLIC_KEY_PATH=../Gate/authx/certs/public.pem
REDIS_URL=redis://localhost:6379
SECRET_KEY=local-fallback-secret
```

### Gate (.env)
```
PRIVATE_KEY_PATH=./authx/certs/private.pem
PUBLIC_KEY_PATH=./authx/certs/public.pem
ALLOWED_ORIGINS=http://localhost:*
```

---

## Troubleshooting

### "Invalid Token" Error
```
→ Check token expiration: jwt.io
→ Verify gate public key is current
→ Ensure X-Org-Id matches token org_id
```

### "PKCE Verifier Mismatch"
```
→ Clear sessionStorage and retry login
→ Check browser privacy settings
→ Verify code_verifier is stored before redirect
```

### "Unauthorized Org Access"
```
→ Fetch new token from Gate with correct org
→ Verify X-Org-Id header is sent
→ Check user membership in organization
```

### Service-to-Service Auth Failures
```
→ Confirm both services have Gate public key
→ Check Redis is running for event bus
→ Verify X-Org-Id is forwarded in calls
```

---

Last updated: 2026-03-01
Version: 1.0
