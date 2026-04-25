# RM Orbit End-to-End Integration Testing Guide

This guide covers testing the complete OAuth2 flow and event bus integration across the ecosystem.

## Prerequisites

✅ All services running (see [PORTS.md](PORTS.md))  
✅ Redis running on port 6379  
✅ Gate registered clients (see Gate `register_internal_apps.py`)  
✅ .env files configured in each service

## Test 1: OAuth2 PKCE Flow

### Objective
Verify user can authenticate via Gate and receive valid RS256 JWT across all apps.

### Steps

#### 1.1 Start Gate Backend
```bash
cd Gate
python -m uvicorn authx.main:app --reload --port 8000
```

Verify: [http://localhost:8000/docs](http://localhost:8000/docs) - Swagger UI loads

#### 1.2 Register OAuth Client (if not done)
```bash
cd Gate
python register_internal_apps.py
```

Output should show:
```
✓ Registered: control-center
✓ Registered: calendar
...
✓ Client configs saved to gate_clients.json
```

#### 1.3 Start Control Center Frontend
```bash
cd "Control Center"
npm install
npm run dev
```

Verify: [http://localhost:5173](http://localhost:5173) loads with login button

#### 1.4 Click "Sign in with RM Gate" Button

Expected flow:
1. Redirects to [http://localhost:8000/oauth/authorize](http://localhost:8000/oauth/authorize)
2. Shows login form
3. Enter test credentials: `test@rmgate.local` / `password`
4. Redirects back to [http://localhost:3001/oauth-callback](http://localhost:3001/oauth-callback)
5. Shows loading spinner, then dashboard

**Verify in Browser Console:**
```javascript
localStorage.getItem('auth_token')
// Should output JWT starting with "eyJ"

localStorage.getItem('auth_user')
// Should output {"id": "...", "email": "test@rmgate.local", ...}
```

#### 1.5 Decode Token (jwt.io)

Copy  `auth_token` from localStorage and paste at [jwt.io](https://jwt.io)

Verify header:
```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

Verify payload contains:
```json
{
  "sub": "user_...",
  "email": "test@rmgate.local",
  "name": "Test User",
  "org_id": "org_...",
  "iat": 1709298600,
  "exp": 1709327400
}
```

---

## Test 2: Backend JWT Verification

### Objective
Verify services can verify RS256 tokens from Gate.

### Steps

#### 2.1 Test Atlas Backend Token Verification

```bash
cd Atlas/backend

# Get token from Control Center login above
TOKEN="eyJ..."
ORG_ID="org_..."

curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

Expected response:
```json
{
  "projects": [...]
}
```

NOT:
```json
{
  "detail": "Could not validate credentials"
}
```

#### 2.2 Test Calendar Backend Token Verification

```bash
TOKEN="eyJ..."
ORG_ID="org_..."

curl -X GET http://localhost:5001/api/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

#### 2.3 Test with Expired/Invalid Token

```bash
curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer invalid_token" \
  -H "X-Org-Id: org_123"
```

Expected: 401 Unauthorized

---

## Test 3: Multi-Tenancy Enforcement

### Objective
Verify X-Org-Id header is enforced and mismatches are rejected.

### Steps

#### 3.1 Get Valid Token & Org ID
From Test 2 above, you have:
```
TOKEN=eyJ...
ORG_ID=abc123  // User's actual org
WRONG_ORG=xyz789  // Different org
```

#### 3.2 Request with Correct Org
```bash
curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

Expected: ✅ 200 OK with projects

#### 3.3 Request with Wrong Org
```bash
curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $WRONG_ORG"
```

Expected: ❌ 403 Forbidden - "Unauthorized organization access"

#### 3.4 Request without Org Header
```bash
curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN"
```

Expected: ❌ 400 Bad Request - "X-Org-Id header required"

---

## Test 4: Redis Event Bus

### Objective
Verify events are published and consumed correctly.

### Steps

#### 4.1 Start Redis CLI Monitor
```bash
redis-cli monitor
```

This shows all Redis commands in real-time.

#### 4.2 Create a Project in Atlas

```bash
TOKEN="eyJ..."
ORG_ID="abc123"

curl -X POST http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "Event bus test"
  }'
```

#### 4.3 Check Redis Monitor Output

You should see:
```
3.1234567 [0 127.0.0.1:xxxxx] "publish" "project.created" "{...event data...}"
```

If no event appears:
- ✅ Check Atlas logs for errors
- ✅ Verify `REDIS_URL` in Atlas .env
- ✅ Confirm Redis is running (`redis-cli ping`)

#### 4.4 Create Calendar Event & Check Event

```bash
curl -X POST http://localhost:5001/api/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Event",
    "start": "2026-03-01T09:00:00Z",
    "end": "2026-03-01T10:00:00Z"
  }'
```

Redis monitor should show:
```
"publish" "calendar.event.created" "{...}"
```

---

## Test 5: Event Consumer (Connect)

### Objective
Verify Connect service consumes events and broadcasts to Socket.io clients.

### Steps

#### 5.1 Start Connect Server
```bash
cd Connect
npm install
npm run dev
```

Logs should show:
```
✓ Event bus consumer connected
✓ Subscribed to: auth.*, meeting.*, user.*
```

#### 5.2 Connect WebSocket Client
```bash
cd Connect
npm run dev  # Frontend dev server
```

Open [http://localhost:5000](http://localhost:5000) in browser.

#### 5.3 Trigger an Event

In another terminal, create a project:
```bash
TOKEN="eyJ..."
ORG_ID="abc123"

curl -X POST http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Event Test", "description": "Testing consumer"}'
```

#### 5.4 Check Connect Server Logs

Should see:
```
[EVENT] Project: project.created
```

And in browser console (if Connect is open):
```javascript
// Socket.io should receive:
socket.on('ecosystem_event', (message) => {
  console.log('Ecosystem event:', message);
});
```

---

## Test 6: Token Refresh

### Objective
Verify short-lived access tokens can be refreshed.

### Steps

#### 6.1 Capture Refresh Token

From Test 1, after login:
```javascript
// In Control Center browser console
localStorage.getItem('refresh_token')
// Copy value
```

#### 6.2 Exchange Refresh Token

```bash
REFRESH_TOKEN="refresh_eyJ..."

curl -X POST http://localhost:8000/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "refresh_token",
    "refresh_token": "'$REFRESH_TOKEN'",
    "client_id": "control-center"
  }'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 28800
}
```

#### 6.3 Use New Token

```bash
NEW_TOKEN="eyJ..."
ORG_ID="abc123"

curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

Expected: ✅ 200 OK

---

## Test 7: Cross-Service Communication

### Objective
Verify Atlas backend can call Calendar API while preserving auth.

### Steps

#### 7.1 Add Test Endpoint to Atlas

Create endpoint that fetches Calendar events:

```python
# Atlas/backend/app/routers/integration.py
from fastapi import APIRouter, Depends
import httpx
from app.auth import get_current_user

router = APIRouter(prefix="/integration")

@router.get("/calendar-sync")
async def sync_calendar(user: User = Depends(get_current_user)):
    """Fetch calendar events from Calendar service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:5001/api/events",
            headers={
                "Authorization": f"Bearer {user_token}",  # Use user's token
                "X-Org-Id": user.org_id,
            },
            timeout=10
        )
    return response.json()
```

#### 7.2 Test Cross-Service Call

```bash
TOKEN="eyJ..."
ORG_ID="abc123"

curl -X GET http://localhost:8001/api/integration/calendar-sync \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

Expected: Calendar events returned

---

## Troubleshooting

### "Invalid Token" at Any Service

**Check:**
```bash
# 1. Token valid?
echo "$TOKEN" | jq -R 'split(".") | .[1] | @base64d'

# 2. Gate public key present?
ls -la Gate/authx/certs/public.pem

# 3. Check service logs for JWT decode errors
docker logs <service>
```

### "Redis Connection Failed"

```bash
# Verify Redis is running
redis-cli ping
# Should output: PONG

# If not running:
redis-server --port 6379
```

### OAuth Callback Redirect Loop

- Clear browser cache: `Cmd+Shift+Delete`
- Check `sessionStorage` doesn't have stale PKCE verifier
- Verify `redirect_uri` matches Gate client config

### Events Not Publishing

```bash
# Check Redis is receiving publishes
redis-cli --csv SUBSCRIBE 'project.*'

# Check app logs for errors
docker logs atlas-backend | grep -i redis
```

---

## Automated Test Suite (Optional)

Create `tests/integration.test.js`:

```javascript
const axios = require('axios');

const API = {
  atlas: 'http://localhost:8001/api',
  calendar: 'http://localhost:5001/api',
  gate: 'http://localhost:8000',
};

let token, orgId;

describe('RM Orbit Integration Tests', () => {
  test('OAuth login flow', async () => {
    // 1. Get auth code
    const authUrl = `${API.gate}/oauth/authorize?...`;
    // 2. Exchange code for token
    const { data } = await axios.post(`${API.gate}/oauth/token`, ...);
    token = data.access_token;
  });

  test('Atlas JWT verification', async () => {
    const response = await axios.get(`${API.atlas}/projects`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'X-Org-Id': orgId,
      },
    });
    expect(response.status).toBe(200);
  });

  // ... more tests
});
```

Run with:
```bash
npm install -D jest supertest
npm test
```

---

## Monitoring & Logging

### View All Services Logs Together

```bash
# With docker-compose
docker-compose logs -f

# With PM2
pm2 logs
```

### Search for Errors

```bash
pm2 logs | grep -i error
docker-compose logs | grep -i "401\|403"
```

### Performance Check

```bash
# Response time
time curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

---

## Success Criteria ✅

All tests should pass:
- [ ] OAuth login redirects and returns token
- [ ] JWT decodes with RS256
- [ ] Atlas/Calendar verify token
- [ ] X-Org-Id enforcement works (allow correct, reject wrong)
- [ ] Events publish to Redis
- [ ] Connect consumes events
- [ ] Token refresh works
- [ ] Cross-service calls succeed
- [ ] No auth errors in logs

---

**Testing Date:** [Date]  
**Tester:** [Name]  
**Result:** ✅ PASS / ❌ FAIL
