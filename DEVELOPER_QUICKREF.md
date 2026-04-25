# RM Orbit Developer Quick Reference

## 🚀 Getting Started (5 minutes)

### 1. Clone & Setup
```bash
cd "RM Orbit"
npm install -g pm2
cp Gate/.env.example Gate/.env
cp Atlas/backend/.env.example Atlas/backend/.env
# ... repeat for other services
```

### 2. Start Services
```bash
# Terminal 1: Start all
pm2 start ecosystem.config.cjs
pm2 logs

# Terminal 2: Register OAuth clients
cd Gate && python register_internal_apps.py

# Terminal 3: Start frontend
cd "Control Center" && npm run dev
```

### 3. Login Test
- Open http://localhost:5173
- Click "Sign in with RM Gate"
- Login: `test@rmgate.local` / `password`
- Check localStorage: `localStorage.getItem('auth_token')`

### 4. Planet-specific Setup
1. **Frontend**
```bash
cd Planet
npm install
cp .env.example .env         # set VITE_GATE_URL and VITE_GATE_CLIENT_ID
npm run dev                   # runs on port 45006 by default
```
2. **Backend**
```bash
cd Planet/backend
python -m venv venv          # or use existing env
source venv/bin/activate
pip install -r ../requirements.txt
./start.sh                   # launches on port 46000
```
3. **Smoke test**
```bash
curl http://localhost:46000/health
# should return {"status":"ok","service":"planet"}
```
4. **Call protected API**
```bash
TOKEN=$(js -e "console.log(localStorage.getItem('auth_token'))")
ORG=$(js -e "console.log(JSON.parse(localStorage.getItem('auth_user')).org_id)")

curl -H "Authorization: Bearer $TOKEN" \
     -H "X-Org-Id: $ORG" \
     http://localhost:46000/api/orgs/$ORG/customers
```
(This will log an event on Redis channel `planet.activity`.)


---

## 🔑 Authentication Cheat Sheet

### Get Token (After Login)
```javascript
// Browser console
const token = localStorage.getItem('auth_token');
const user = JSON.parse(localStorage.getItem('auth_user'));
console.log(token, user.org_id);
```

### Decode Token (jwt.io)
```
1. Copy token from localStorage
2. Go to https://jwt.io
3. Paste in "Encoded" box
4. Check RS256 signature with Gate public key
```

### Call Protected API
```bash
TOKEN="eyJ..."  # From above
ORG_ID="org_123"

curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID"
```

### Verify Token at Service
```python
# FastAPI
from fastapi import Depends
from app.auth import get_current_user

@router.get("/projects")
async def list_projects(user: User = Depends(get_current_user)):
    # user is auto-populated from JWT
    return {"projects": [...]}
```

---

## 📡 Event Bus Cheat Sheet

### Publish an Event
```python
# FastAPI
from app.services.eventbus import publish_event

await publish_event('project.created', {
    'project_id': '123',
    'name': 'New Project',
    'created_by': user.id,
})
```

```javascript
// Node.js
const { publishEvent } = require('./eventbus');

await publishEvent('project.created', {
  projectId: '123',
  name: 'New Project',
  createdBy: userId,
});
```

### Consume Events
```python
# Python async
async def handle_project_event(event):
    if event['event_type'] == 'project.created':
        print(f"New project: {event['data']['name']}")

await event_consumer.subscribe('project.*', handle_project_event)
```

```javascript
// Node.js
const redis = require('redis');
const subscriber = redis.createClient();
await subscriber.connect();

await subscriber.pSubscribe('project.*', (message) => {
    const event = JSON.parse(message);
    console.log('Project event:', event.event_type);
});
```

### Monitor Events
```bash
# Terminal 1: Watch all events
redis-cli monitor

# Terminal 2: Trigger an event (create project)
curl -X POST http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID" \
  -d '{"name":"Test"}'

# Should see in Terminal 1:
# "PUBLISH" "project.created" "{...}"
```

---

## 🏢 Multi-Tenancy Cheat Sheet

### Enforce in Middleware
```python
# FastAPI
from fastapi import Header, HTTPException

async def verify_org(x_org_id: str = Header(None)):
    if not x_org_id:
        raise HTTPException(status_code=400, detail="X-Org-Id required")
    return x_org_id

@router.get("/projects")
async def list_projects(
    org_id: str = Depends(verify_org),
    user: User = Depends(get_current_user),
):
    # Both org_id and user.org_id must match
```

### Verify Access
```python
# Check user belongs to org
if user.org_id != request_org_id:
    raise HTTPException(status_code=403, detail="Unauthorized org")
```

### API Call with Org
```bash
# Always include header
curl http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: org_123"
```

---

## 🔍 Debugging Guide

### Check Token Expiry
```javascript
// Browser console
const token = localStorage.getItem('auth_token');
const parts = token.split('.');
const payload = JSON.parse(atob(parts[1]));
const exp = new Date(payload.exp * 1000);
console.log('Expires:', exp);
```

### Verify Public Key
```bash
# Check if Gate public key exists
ls -la Gate/authx/certs/public.pem

# Check if service has it
ls -la Atlas/backend/Gate/authx/certs/public.pem  # or via env
```

### Check Redis Connection
```bash
# From app directory
redis-cli ping
# Should output: PONG

# Check app can reach Redis
curl http://localhost:6379
redis-cli PUBSUB CHANNELS
```

### View Service Logs
```bash
# All services
pm2 logs

# Single service
pm2 logs atlas-backend

# Real-time with grep
pm2 logs | grep error
```

### Test API with Authentication
```bash
# Get token first
TOKEN=$(curl -s http://localhost:8000/oauth/token \
  -d '...' | jq -r '.access_token')

# Use in request
curl -v http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: org_123"
```

---

## 📝 Common Tasks

### Add New Endpoint with Auth
```python
from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter()

@router.post("/projects")
async def create_project(
    name: str,
    org_id: str = Header(..., alias="X-Org-Id"),
    user: User = Depends(get_current_user),
):
    # Verify org match
    if user.org_id != org_id:
        raise HTTPException(status_code=403)
    
    # Create project
    project = Project(name=name, org_id=org_id, created_by=user.id)
    db.add(project)
    
    # Publish event
    await publish_event('project.created', {
        'project_id': project.id,
        'name': name,
        'created_by': user.id,
    })
    
    return project
```

### Add Event Consumer
```python
# In service startup
async def init_app(app: FastAPI):
    await event_consumer.connect()
    
    async def handle_auth(event):
        if event['event_type'] == 'auth.login':
            user_id = event['data']['user_id']
            # Do something...
    
    await event_consumer.subscribe('auth.*', handle_auth)

# In main.py
app.add_event_handler("startup", init_app)
```

### Test with Real Token
```bash
# 1. Login in browser
# Get token from localStorage

# 2. Set environment variable
export TOKEN="eyJ..."
export ORG_ID="org_..."

# 3. Make request
curl -X GET http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: $ORG_ID" \
  -H "Content-Type: application/json"
```

---

## ⚠️ Common Mistakes

### ❌ Missing X-Org-Id Header
```bash
# Wrong
curl http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN"

# Right
curl http://localhost:8001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Org-Id: org_123"
```

### ❌ Invalid Bearer Format
```bash
# Wrong
-H "Authorization: $TOKEN"

# Right
-H "Authorization: Bearer $TOKEN"
```

### ❌ Forgot to Copy Public Key
```bash
# Check Gate public key is in service:
ls -la Gate/authx/certs/public.pem
echo $GATE_PUBLIC_KEY_PATH

# If missing
export GATE_PUBLIC_KEY_PATH=./Gate/authx/certs/public.pem
```

### ❌ Redis Not Running
```bash
# Check
redis-cli ping
# If error: Redis not running

# Start
redis-server --port 6379
```

---

## 📚 Full Documentation

For complete details, see:
- **[AUTH_SECURITY.md](AUTH_SECURITY.md)** - Full auth implementation
- **[EVENT_SCHEMA.md](EVENT_SCHEMA.md)** - All event types
- **[INTEGRATION_TESTING.md](INTEGRATION_TESTING.md)** - Test procedures
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What's implemented

---

## 🆘 Quick Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired? | Refresh token or re-login |
| 403 Forbidden | Org mismatch? | Check X-Org-Id matches token |
| 400 Bad Request | Missing header? | Add X-Org-Id header |
| Redis connection | `redis-cli ping` | Start Redis server |
| Event not publish | Check service logs | Verify Redis URL in .env |
| PKCE error | Clear session | localStorage.clear() |
| Can't login | Check Gate running | `ps aux \| grep gate` |

---

## 🚀 Performance Tips

### Reuse Connections
```javascript
const httpClient = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});
```

### Cache Tokens
```javascript
const token = localStorage.getItem('auth_token');
const user = JSON.parse(localStorage.getItem('auth_user'));
// Reuse across requests
```

### Batch Events
```python
# Instead of publishing 100 events
for item in items:
    await publish_event('item.created', item)  # ❌ Slow

# Batch them
await publish_event('items.batch_created', {
    'count': len(items),
    'items': items,  # ✅ Fast
})
```

### Monitor Performance
```bash
# Response time
time curl http://localhost:8001/api/projects -H "..."

# Redis latency
redis-cli --latency
```

---

**Last Updated:** 2026-03-01  
**For detailed info, see [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**
