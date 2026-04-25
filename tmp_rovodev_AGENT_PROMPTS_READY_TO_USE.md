# 🤖 READY-TO-USE AI AGENT PROMPTS
**Copy-paste these directly to your AI agents**

---

## 🔥 CRITICAL PATH AGENTS (Start These First - Day 1)

### AGENT #1: RM-Gate Authentication Hardening

```
You are AI Agent #1 working on RM-Gate authentication hardening.

PROJECT CONTEXT:
RM-Gate is the OAuth2/JWT authentication provider for the entire RM Orbit ecosystem. It's currently 95% complete and functional, but needs production hardening before other applications can safely depend on it. You are the FIRST agent to start - Agents #4, #5, #6, and #7 are blocked waiting for you to complete.

YOUR MISSION (8 hours):
Build production-grade security features for RM-Gate authentication system.

SPECIFIC TASKS:

TASK 1: Multi-tenant Session Management (2 hours)
- Create file: RM-Gate/authx/app/core/session.py
- Implement Redis-backed session store with organization scoping
- Each session must include: user_id, org_id, created_at, expires_at
- Add automatic session cleanup job (remove expired tokens every hour)
- Test: 1000 concurrent logins across 10 different organizations

TASK 2: Rate Limiting per Organization (2 hours)
- Create file: RM-Gate/authx/app/middleware/rate_limit.py
- Implement per-org rate limits: 100 requests/minute for auth endpoints
- Add IP-based blocking for brute force attempts (10 failed logins = 15 min block)
- Return HTTP 429 (Too Many Requests) when threshold exceeded
- Test: Verify rate limiting works and resets properly

TASK 3: Comprehensive Audit Logging (2 hours)
- Create file: RM-Gate/authx/app/services/audit_logger.py
- Log ALL authentication events: login attempts, token refreshes, failures, logouts
- Store in PostgreSQL table: audit_logs (timestamp, user_id, org_id, event_type, ip_address, user_agent, success/failure)
- Add CSV export endpoint: GET /api/audit/export?org_id=X&start_date=Y&end_date=Z
- Test: Generate 100 login events, verify all are logged

TASK 4: Token Rotation and Revocation (1.5 hours)
- Modify file: RM-Gate/authx/app/services/token_manager.py
- Implement refresh token rotation (issue new refresh token on each refresh)
- Add POST /api/auth/revoke endpoint to blacklist tokens
- Store revoked tokens in Redis with TTL matching token expiry
- Test: Verify revoked tokens return 401 Unauthorized

TASK 5: Production Deployment Documentation (0.5 hours)
- Create file: RM-Gate/PRODUCTION_DEPLOYMENT.md
- Document: SSL/TLS setup with Let's Encrypt
- Document: All environment variables with descriptions
- Document: Database backup procedures (PostgreSQL + Redis)
- Document: Disaster recovery steps (restore from backup)

VALIDATION CRITERIA:
✓ All pytest tests pass with >85% code coverage
✓ Load test: Handle 10,000 authentication requests in 60 seconds
✓ Security audit: Zero vulnerabilities in token generation/validation
✓ Documentation complete and peer-reviewed

TECHNICAL REQUIREMENTS:
- Python 3.11+ with FastAPI
- Redis for session storage and rate limiting
- PostgreSQL for audit logs
- Follow existing code patterns in RM-Gate/authx/app/

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Gate Authentication Hardening
Agent: #1
Time Spent: X hours (estimated 8h)
Test Coverage: Y%
Performance: 10K req/60s = [PASS/FAIL]
Security Scan: [PASS/FAIL]
Documentation: [COMPLETE]

Files Created:
- RM-Gate/authx/app/core/session.py (XXX lines)
- RM-Gate/authx/app/middleware/rate_limit.py (XXX lines)
- RM-Gate/authx/app/services/audit_logger.py (XXX lines)
- RM-Gate/PRODUCTION_DEPLOYMENT.md

Files Modified:
- RM-Gate/authx/app/services/token_manager.py

Tests Added: XX tests
All Validation Criteria: [MET/NOT MET]

Ready for: Agents #4, #5, #6, #7 to begin
Next: Standing by for next assignment
"""

START NOW. The entire ecosystem is waiting for you! 🚀
```

---

### AGENT #2: RM-Snitch Event Bus Completion

```
You are AI Agent #2 working on RM-Snitch event bus completion.

PROJECT CONTEXT:
RM-Snitch is the central nervous system of the RM Orbit ecosystem - it's the event bus that enables real-time communication between all applications. Currently 55% complete with basic WebSocket support, but needs persistent storage and reliable delivery mechanisms.

YOUR MISSION (12 hours):
Build a production-grade event bus with persistence, routing, and reliability.

SPECIFIC TASKS:

TASK 1: Complete Event Schema Definitions (2 hours)
- Create file: RM-Snitch/backend/event-schemas.js
- Define ALL event types for the ecosystem:
  * atlas.task.created, atlas.task.updated, atlas.task.deleted
  * connect.message.sent, connect.channel.created, connect.user.joined
  * meet.call.started, meet.call.ended, meet.participant.joined
  * mail.email.received, mail.email.sent
  * planet.deal.created, planet.deal.closed
  * learn.article.published
  * calendar.event.created, calendar.reminder.triggered
- Add JSON schema validation for each event type (validate payload structure)
- Generate TypeScript definitions for frontend consumption

TASK 2: Implement Persistent Event Store (3 hours)
- Create file: RM-Snitch/backend/event-store.js
- Replace in-memory storage with PostgreSQL
- Schema: events table (id, event_type, payload, org_id, user_id, created_at, delivered_at, retry_count)
- Add event replay capability: re-deliver events from last 7 days
- Add configurable retention policy (default: 30 days, then archive/delete)
- Test: Insert 10,000 events, query by org_id and event_type

TASK 3: Build Event Routing Engine (3 hours)
- Create file: RM-Snitch/backend/event-router.js
- Implement topic-based subscriptions (subscribe to "atlas.*" or "connect.message.*")
- Add filtering by: org_id, user_id, event_type (combined filters)
- Add dead letter queue for failed deliveries (retry 3 times, then DLQ)
- Add fan-out routing (one event → multiple subscribers)
- Test: Route 1000 events/second to 100 subscribers without drops

TASK 4: Add WebSocket Reliability (2 hours)
- Modify file: RM-Snitch/backend/websocket-manager.js
- Implement automatic reconnection with exponential backoff (1s, 2s, 4s, 8s, 16s max)
- Add heartbeat/ping-pong (30 second interval, disconnect after 90s silence)
- Add message acknowledgment system (client must ACK within 5 seconds)
- Queue undelivered messages during disconnection, deliver on reconnect
- Test: Simulate network interruptions, verify zero message loss

TASK 5: Create Monitoring Dashboard (2 hours)
- Create file: RM-Snitch/frontend/src/pages/EventMonitor.tsx
- Display real-time metrics:
  * Events per second (current and 5-minute average)
  * Active WebSocket connections (by app and org)
  * Failed deliveries (last 24 hours)
  * Event type breakdown (pie chart)
- Add real-time event stream viewer (live tail of events)
- Add search and filtering (by event_type, org_id, date range)
- Test: Dashboard loads in <2 seconds, updates in real-time

VALIDATION CRITERIA:
✓ Handle 1000 events/second without message drops
✓ Zero message loss during WebSocket reconnections
✓ Event replay works for last 7 days
✓ Dashboard shows accurate real-time metrics
✓ Dead letter queue captures failed events

TECHNICAL REQUIREMENTS:
- Node.js 18+ with Express
- PostgreSQL for event persistence
- WebSockets (ws library)
- React + TypeScript for dashboard

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Snitch Event Bus
Agent: #2
Time Spent: X hours (estimated 12h)
Throughput: X events/second sustained
Message Loss: [ZERO/COUNT]
Dashboard Load Time: Xs

Files Created:
- RM-Snitch/backend/event-schemas.js
- RM-Snitch/backend/event-store.js
- RM-Snitch/backend/event-router.js
- RM-Snitch/frontend/src/pages/EventMonitor.tsx

Files Modified:
- RM-Snitch/backend/websocket-manager.js

Event Types Defined: XX
All Validation Criteria: [MET/NOT MET]

Ready for: All apps to integrate event publishing
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #3: AgentTheatre Production Ready

```
You are AI Agent #3 working on AgentTheatre production readiness.

PROJECT CONTEXT:
AgentTheatre is the AI agent orchestration platform that powers automation across the RM Orbit ecosystem. Currently 80% complete with basic agent execution, but needs production safety controls, multi-LLM support, and a marketplace for pre-built agents.

YOUR MISSION (10 hours):
Make AgentTheatre production-ready with safety controls and enterprise features.

SPECIFIC TASKS:

TASK 1: Complete LLM Provider Abstraction (3 hours)
- Modify file: AgentTheatre/AgentTheater/services/llm_client.py
- Add support for multiple providers:
  * OpenAI (GPT-4, GPT-3.5)
  * Anthropic (Claude 3 Opus, Sonnet, Haiku)
  * Google (Gemini Pro, Gemini Ultra)
  * Local models (Ollama, LM Studio)
- Implement automatic fallback chain: GPT-4 → Claude → Gemini → Local
- Add cost tracking per model and request (store in database)
- Add response caching (cache identical prompts for 1 hour)
- Test: Simulate GPT-4 failure, verify Claude takes over in <5 seconds

TASK 2: Implement Agent Collaboration Framework (3 hours)
- Create file: AgentTheatre/AgentTheater/core/collaboration.py
- Build agent-to-agent messaging protocol (agents can request help from other agents)
- Add shared context/memory between agents (shared key-value store)
- Add conflict resolution when agents disagree (majority vote or human escalation)
- Add collaborative task decomposition (one agent splits task, others execute)
- Test: Run 3 agents collaborating on a complex task

TASK 3: Add Production Safety Controls (2 hours)
- Create file: AgentTheatre/AgentTheater/core/safety.py
- Implement spending limits per organization ($100/month default, configurable)
- Add human-in-the-loop for critical decisions (require approval for: data deletion, API changes, production deployments)
- Add action whitelist/blacklist per agent (restrict what each agent can do)
- Add rate limiting (max 100 agent executions per org per hour)
- Test: Verify spending limit stops execution at threshold

TASK 4: Build Agent Marketplace UI (1.5 hours)
- Create file: AgentTheatre/frontend/src/pages/Marketplace.tsx
- Display pre-built agents:
  * Code Reviewer (reviews PRs, suggests improvements)
  * Bug Finder (scans code for common bugs)
  * Test Generator (writes unit tests for functions)
  * Documentation Writer (generates docs from code)
  * Security Auditor (finds security vulnerabilities)
- Add one-click installation (copy agent to user's workspace)
- Add usage analytics per agent (executions, success rate, avg cost)
- Test: Install agent from marketplace, verify it runs

TASK 5: Create Comprehensive Testing Suite (0.5 hours)
- Create file: AgentTheatre/tests/test_production_scenarios.py
- Test: Multi-agent collaboration on real project (create feature branch, write code, create PR)
- Test: Cost controls (stop at spending limit)
- Test: Failover between LLM providers (all providers tested)
- Test: Human-in-the-loop approval workflow
- Run all tests and achieve >90% coverage

VALIDATION CRITERIA:
✓ Run 100 agent tasks without errors
✓ Cost tracking accurate to $0.01
✓ Failover happens in <5 seconds
✓ UI loads in <2 seconds
✓ Spending limits enforced correctly

TECHNICAL REQUIREMENTS:
- Python 3.11+ with FastAPI
- PostgreSQL for agent state and history
- React + TypeScript for UI
- OpenAI, Anthropic, Google AI SDKs

WHEN COMPLETE, REPORT:
"""
COMPLETED: AgentTheatre Production Ready
Agent: #3
Time Spent: X hours (estimated 10h)
Test Coverage: Y%
Failover Time: Xs
UI Load Time: Xs

Files Created:
- AgentTheatre/AgentTheater/core/collaboration.py
- AgentTheatre/AgentTheater/core/safety.py
- AgentTheatre/frontend/src/pages/Marketplace.tsx
- AgentTheatre/tests/test_production_scenarios.py

Files Modified:
- AgentTheatre/AgentTheater/services/llm_client.py

LLM Providers Supported: 4
Pre-built Agents: 5
All Validation Criteria: [MET/NOT MET]

Ready for: Production deployment
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #16: CI/CD Pipeline Setup

```
You are AI Agent #16 working on CI/CD pipeline setup.

PROJECT CONTEXT:
The RM Orbit ecosystem has 15 applications that need automated testing and deployment. You're responsible for setting up GitHub Actions workflows that test every commit, deploy to staging automatically, and enable production deployments.

YOUR MISSION (16 hours):
Build complete CI/CD pipeline for all 15 applications.

SPECIFIC TASKS:

TASK 1: Create Master Test Workflow (4 hours)
- Create file: .github/workflows/test-all-apps.yml
- Run tests for all apps on every push to main or PR
- For Python apps: pytest with coverage report
- For Node.js apps: jest/vitest with coverage report
- For TypeScript apps: tsc type checking + tests
- Fail build if test coverage <80%
- Upload coverage reports to Codecov or similar
- Test: Trigger workflow, verify all apps tested

TASK 2: Create Staging Deployment Workflow (4 hours)
- Create file: .github/workflows/deploy-staging.yml
- Auto-deploy to staging on merge to main branch
- Build Docker images for all apps
- Push images to container registry (GitHub Container Registry)
- Deploy to staging environment (docker-compose or k8s)
- Run smoke tests after deployment
- Send Slack/Discord notification on success/failure
- Test: Merge PR, verify staging deployment

TASK 3: Create Production Deployment Workflow (4 hours)
- Create file: .github/workflows/deploy-production.yml
- Deploy to production on git tag (e.g., v1.0.0)
- Require manual approval (GitHub Environments)
- Run full integration test suite before deployment
- Deploy with zero-downtime (blue-green or rolling)
- Add automatic rollback if health checks fail
- Send notification to #production channel
- Test: Create tag, verify approval required

TASK 4: Add Security Scanning (2 hours)
- Create file: .github/workflows/security-scan.yml
- Run on every PR and weekly on main
- Scan Python dependencies: pip-audit or safety
- Scan Node.js dependencies: npm audit
- Scan Docker images: Trivy or Snyk
- Scan code for secrets: TruffleHog or GitGuardian
- Fail build on critical vulnerabilities
- Test: Introduce vulnerable dependency, verify caught

TASK 5: Add Performance Testing (2 hours)
- Create file: .github/workflows/performance-test.yml
- Run weekly on main branch
- Load test each app: 1000 concurrent users
- Measure: p50, p95, p99 response times
- Fail if p95 >500ms (configurable per app)
- Store results in database for trending
- Generate performance report (chart over time)
- Test: Run load test, verify metrics collected

VALIDATION CRITERIA:
✓ All apps tested on every commit
✓ Staging deploys automatically on merge
✓ Production requires approval
✓ Security scans catch vulnerabilities
✓ Load tests run without errors
✓ Full pipeline completes in <15 minutes

TECHNICAL REQUIREMENTS:
- GitHub Actions
- Docker + docker-compose
- pytest (Python), jest (Node.js)
- Locust or k6 for load testing
- Trivy for security scanning

WHEN COMPLETE, REPORT:
"""
COMPLETED: CI/CD Pipeline Setup
Agent: #16
Time Spent: X hours (estimated 16h)
Apps Covered: 15/15
Pipeline Duration: Xm
Test Coverage: Y% average

Files Created:
- .github/workflows/test-all-apps.yml
- .github/workflows/deploy-staging.yml
- .github/workflows/deploy-production.yml
- .github/workflows/security-scan.yml
- .github/workflows/performance-test.yml

Workflows Tested: [ALL PASSED/FAILED]
All Validation Criteria: [MET/NOT MET]

Ready for: Continuous deployment
Next: Standing by for ongoing testing support
"""

START NOW! 🚀
```

---

## 🚀 BUSINESS APPS (Week 2-3 - Start After Agent #1 Completes)

[Continuing in next section...]

## 🚀 BUSINESS APPS (Week 2-3 - Start After Agent #1 Completes)

### AGENT #4: RM-FitterMe Full Stack Build

```
You are AI Agent #4 working on RM-FitterMe full stack completion.

PROJECT CONTEXT:
RM-FitterMe is a health and fitness application. Backend is 90% complete with working API structure, but currently returns hardcoded workout/meal data. Frontend is only 20% done - needs full UI build. Your job is to replace mock data with real AI-generated personalized plans and build a complete frontend.

DEPENDENCY: Wait for Agent #1 (RM-Gate) to complete before starting.

YOUR MISSION (20 hours):
Transform RM-FitterMe from mock data to real AI-powered fitness app with complete UI.

SPECIFIC TASKS:

TASK 1: Build Real AI Workout Generator (4 hours)
- Modify file: RM-FitterMe/backend/app/services/workout_ai.py
- REMOVE: Current hardcoded 7 workout strings
- IMPLEMENT: GPT-4 integration for personalized workout generation
- Input parameters: user_weight, height, age, fitness_level (beginner/intermediate/advanced), goals (lose_weight/gain_muscle/maintenance), available_equipment (gym/home/bodyweight)
- Output: 4-week progressive workout plan with:
  * Exercise name, sets, reps, rest time
  * Progressive overload (increase weight/reps each week)
  * Exercise instructions and form tips
  * Estimated calories burned
- Add exercise library database (500+ exercises with muscle groups, difficulty, equipment)
- Cache generated plans (same inputs = same plan for 7 days)
- Test: Generate plan for 10 different user profiles

TASK 2: Build Real AI Meal Plan Generator (4 hours)
- Modify file: RM-FitterMe/backend/app/services/nutrition_ai.py
- REMOVE: Current hardcoded 4 meal descriptions
- IMPLEMENT: GPT-4 integration for meal planning
- Input parameters: calorie_target, dietary_restrictions (vegetarian/vegan/keto/paleo/none), allergies, cuisine_preferences, meals_per_day (3-6)
- Output: 7-day meal plan with:
  * Breakfast, lunch, dinner, snacks (if meals_per_day >3)
  * Full recipes with ingredients and instructions
  * Macros per meal (protein/carbs/fats/calories)
  * Shopping list (aggregated ingredients)
- Integrate USDA FoodData Central API for accurate nutrition data
- Test: Generate meal plans for different calorie targets (1500, 2000, 2500, 3000 cal)

TASK 3: Build Complete Dashboard UI (4 hours)
- Create file: RM-FitterMe/frontend/src/pages/Dashboard.tsx
- Display sections:
  * Today's workout card (exercise name, sets, reps, timer button)
  * Today's meal plan card (breakfast, lunch, dinner with macros)
  * Progress charts: Weight tracking graph (last 30 days, line chart)
  * Macro tracking: Donut chart (protein/carbs/fats breakdown)
  * Workout streak: Days in a row (gamification)
- Add quick actions: "Log weight", "Complete workout", "Log meal"
- Make mobile-responsive (looks good on phone)
- Test: Load dashboard with real data, verify charts render

TASK 4: Build Workout Tracking UI (4 hours)
- Create file: RM-FitterMe/frontend/src/pages/WorkoutTracker.tsx
- Display current workout:
  * Exercise list with checkboxes
  * Timer for each exercise (countdown rest periods)
  * Exercise demo (video or GIF from exercise library)
  * Weight/reps input fields (log actual performance)
- Add rest timer: Auto-start countdown after completing set
- Add progress notes: "How did you feel? Any pain?"
- Add completion celebration: Confetti animation on workout complete
- Save workout log to database (for progress tracking)
- Test: Complete a full workout, verify data saved

TASK 5: Build Nutrition Tracking UI (3 hours)
- Create file: RM-FitterMe/frontend/src/pages/NutritionTracker.tsx
- Add quick food logging:
  * Search box with autocomplete (USDA FoodData Central)
  * Recent foods list (one-click add)
  * Meal categorization (breakfast/lunch/dinner/snack)
- Display daily macro breakdown:
  * Progress bars: Protein (0/150g), Carbs (0/200g), Fats (0/60g)
  * Calorie counter: 1250/2000 calories
- Add water tracking: 8 glass icons, tap to mark consumed
- Add recipe builder: Save custom meals with ingredients
- Test: Log 10 different foods, verify macros calculated correctly

TASK 6: Connect All Frontend to Backend (1 hour)
- Create file: RM-FitterMe/frontend/src/services/api.ts
- Connect endpoints:
  * POST /api/ai/workout-plan (generate workout)
  * POST /api/ai/meal-plan (generate meals)
  * GET /api/progress/weight (fetch weight history)
  * POST /api/workouts/log (save workout completion)
  * POST /api/nutrition/log (save food intake)
- Add loading states (spinners while AI generates plans)
- Add error handling (display user-friendly messages)
- Add optimistic UI updates (instant feedback before server responds)
- Test: All CRUD operations work end-to-end

VALIDATION CRITERIA:
✓ Generate personalized workout plan in <10 seconds
✓ Generate meal plan with real recipes (not generic)
✓ Frontend loads dashboard in <3 seconds
✓ All CRUD operations work (create/read/update/delete)
✓ Mobile responsive (works on 375px width screens)
✓ Charts render correctly with real data

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI, OpenAI SDK
- Frontend: React 18+, TypeScript, Chart.js or Recharts
- Database: PostgreSQL
- External APIs: OpenAI GPT-4, USDA FoodData Central

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-FitterMe Full Stack Build
Agent: #4
Time Spent: X hours (estimated 20h)
AI Response Time: Xs (workout), Xs (meal)
Test Coverage: Y%
Mobile Responsive: [YES/NO]

Files Created:
- RM-FitterMe/frontend/src/pages/Dashboard.tsx
- RM-FitterMe/frontend/src/pages/WorkoutTracker.tsx
- RM-FitterMe/frontend/src/pages/NutritionTracker.tsx
- RM-FitterMe/frontend/src/services/api.ts

Files Modified:
- RM-FitterMe/backend/app/services/workout_ai.py
- RM-FitterMe/backend/app/services/nutrition_ai.py

Exercise Library: 500+ exercises
All Validation Criteria: [MET/NOT MET]

Ready for: Beta testing with real users
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #5: RM-Planet CRM Completion

```
You are AI Agent #5 working on RM-Planet CRM completion.

PROJECT CONTEXT:
RM-Planet is a CRM/sales platform. Currently 45% complete with basic deal management, but missing key CRM features: pipeline management, contacts/companies, activity tracking, email integration, and reporting.

DEPENDENCY: Wait for Agent #1 (RM-Gate) to complete before starting.

YOUR MISSION (16 hours):
Transform RM-Planet into a complete CRM that rivals Salesforce.

SPECIFIC TASKS:

TASK 1: Build Complete Pipeline Management (3 hours)
- Create file: RM-Planet/backend/app/routers/pipeline.py
- Add custom pipeline stages (configurable per organization):
  * Default stages: Lead → Qualified → Proposal → Negotiation → Closed Won/Lost
  * Allow orgs to add/remove/rename stages
- Add drag-and-drop stage transitions (update deal.stage on drop)
- Add stage probability auto-calculation (Lead=10%, Qualified=25%, Proposal=50%, Negotiation=75%, Closed=100%)
- Add pipeline value forecasting (sum of: deal_value × stage_probability)
- Add pipeline visualization (Kanban board with deal cards)
- Test: Move 100 deals through pipeline, verify forecasts accurate

TASK 2: Build Contact/Company Management (4 hours)
- Create file: RM-Planet/backend/app/routers/contacts.py
- Contacts schema: name, email, phone, title, company_id, linkedin_url, notes, created_at, updated_at
- Companies schema: name, industry, size (1-10, 11-50, 51-200, 201-500, 500+), website, logo_url, notes
- CRUD endpoints for both contacts and companies
- Auto-link contacts to deals (when creating deal, select contact, auto-populate company)
- Add contact import from CSV (map columns, preview, import)
- Add duplicate detection (warn if email/phone already exists)
- Test: Import 1000 contacts from CSV, verify all fields mapped

TASK 3: Build Activity Timeline (3 hours)
- Create file: RM-Planet/backend/app/routers/activities.py
- Activity types: call, email, meeting, note, task
- Schema: activity_type, subject, description, deal_id, contact_id, user_id, completed (bool), due_date, completed_at
- Auto-create activities when deal stage changes (log: "Deal moved to Proposal stage")
- Add activity reminders (send email/notification at due_date)
- Add activity templates (pre-fill common activities like "Follow-up call")
- Display timeline view (chronological list of all activities per deal)
- Test: Create 50 activities, verify reminders sent on time

TASK 4: Build Email Integration (3 hours)
- Create file: RM-Planet/backend/app/services/email_service.py
- Integrate RM-Mail for sending emails FROM Planet
- Add email templates:
  * Sales outreach: "Hi {contact_name}, I noticed..."
  * Follow-up: "Just checking in on..."
  * Proposal sent: "Attached is our proposal for..."
- Add email tracking (opened, clicked, replied)
- Add automatic deal updates from email replies (if contact replies, set activity.completed=true)
- Add email composer UI in deal view (send email without leaving Planet)
- Test: Send 20 emails, verify tracking works

TASK 5: Build Reporting and Analytics (2 hours)
- Create file: RM-Planet/frontend/src/pages/Analytics.tsx
- Sales forecast chart: Expected revenue by month (bar chart, next 6 months)
- Win/loss analysis: Pie chart showing closed won vs closed lost (with reasons)
- Rep performance leaderboard: Table showing deals closed, revenue, avg deal size per user
- Pipeline velocity metrics: Avg days in each stage, conversion rates stage-to-stage
- Add date range filter (last 30/60/90 days, this quarter, custom)
- Test: Generate reports with 1000 deals, verify calculations accurate

TASK 6: Build Mobile-Responsive UI (1 hour)
- Modify file: RM-Planet/frontend/src/components/DealCard.tsx
- Optimize layout for tablet and mobile screens (320px+)
- Add touch gestures for drag-and-drop (on mobile)
- Make pipeline board scrollable horizontally on mobile
- Add mobile-first navigation (bottom tab bar)
- Test on real mobile device or Chrome DevTools mobile emulation
- Test: All features work on iPhone/Android screen sizes

VALIDATION CRITERIA:
✓ Manage 1000+ deals without performance issues (<3s page load)
✓ Email integration works (send from Planet, tracking works)
✓ Reports generate in <3 seconds
✓ Mobile UI fully functional (all features accessible)
✓ Contact import handles 5000+ rows

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI
- Frontend: React 18+, TypeScript
- Charts: Recharts or Chart.js
- Database: PostgreSQL with proper indexes

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Planet CRM Completion
Agent: #5
Time Spent: X hours (estimated 16h)
Test Coverage: Y%
Page Load Time: Xs (with 1000 deals)
Mobile Responsive: [YES/NO]

Files Created:
- RM-Planet/backend/app/routers/pipeline.py
- RM-Planet/backend/app/routers/contacts.py
- RM-Planet/backend/app/routers/activities.py
- RM-Planet/backend/app/services/email_service.py
- RM-Planet/frontend/src/pages/Analytics.tsx

Files Modified:
- RM-Planet/frontend/src/components/DealCard.tsx

Deals Supported: 1000+
All Validation Criteria: [MET/NOT MET]

Ready for: Sales team beta testing
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #6: RM-Learn Documentation Platform

```
You are AI Agent #6 working on RM-Learn documentation platform completion.

PROJECT CONTEXT:
RM-Learn is a documentation and knowledge base platform (like GitBook or Notion Docs). Currently 40% complete with basic page structure, but missing key features: markdown editor, search, version control, and collaboration.

DEPENDENCY: Wait for Agent #1 (RM-Gate) to complete before starting.

YOUR MISSION (14 hours):
Build a complete documentation platform with editing, search, and version control.

SPECIFIC TASKS:

TASK 1: Build Markdown Editor with Preview (3 hours)
- Create file: RM-Learn/frontend/src/components/MarkdownEditor.tsx
- Split-pane editor: Write markdown on left, see preview on right
- Add syntax highlighting for code blocks (use Prism.js or Highlight.js)
- Support: headings, bold, italic, lists, tables, images, links, code blocks
- Add image upload: Drag & drop or click to upload (store in S3 or local storage)
- Add auto-save: Save to backend every 30 seconds (debounced)
- Add keyboard shortcuts: Cmd+B (bold), Cmd+I (italic), Cmd+K (link)
- Test: Write 5000-word document, verify no lag

TASK 2: Build Documentation Hierarchy (3 hours)
- Create file: RM-Learn/backend/app/routers/docs.py
- Implement nested categories: Category → Subcategory → Page (unlimited depth)
- Schema: pages table (id, title, content, parent_id, order, created_at, updated_at)
- Add drag-and-drop reordering (change page.order on drop)
- Add breadcrumb navigation (Home > Category > Page)
- Auto-generate table of contents from headings (H1, H2, H3 in markdown)
- Test: Create 100 pages in 10 categories, verify hierarchy displays correctly

TASK 3: Build Search with AI (3 hours)
- Create file: RM-Learn/backend/app/services/search_service.py
- Implement full-text search using PostgreSQL full-text search OR Elasticsearch
- Index: page title, content, category name
- Add AI-powered semantic search (use OpenAI embeddings to find similar content)
- Add search suggestions/autocomplete (show results as user types)
- Add search analytics (track popular queries, show "trending searches")
- Rank results by: relevance, recency, views
- Test: Search 1000 documents, verify results in <500ms

TASK 4: Build Version Control for Docs (2 hours)
- Create file: RM-Learn/backend/app/routers/versions.py
- Save doc history on every edit: versions table (page_id, content, edited_by, edited_at)
- Add version comparison view (diff showing what changed, like Git diff)
- Add restore previous version button (rollback to older version)
- Add "who edited what" tracking (show user avatar and timestamp)
- Keep last 100 versions per page (archive older versions)
- Test: Make 50 edits, verify all versions saved and diffable

TASK 5: Build Commenting and Feedback (2 hours)
- Create file: RM-Learn/frontend/src/components/ArticleComments.tsx
- Add comments section at bottom of each article
- Allow replies to comments (threaded discussions)
- Add upvote/downvote for comment helpfulness
- Add "Was this article helpful?" widget (yes/no with optional feedback)
- Allow article authors to respond to comments
- Show comment count badge (notify authors of new comments)
- Test: Add 20 comments with replies, verify threading works

TASK 6: Build API Documentation Generator (1 hour)
- Create file: RM-Learn/backend/app/services/api_docs.py
- Auto-generate API docs from OpenAPI/Swagger spec
- Display endpoints grouped by resource (Users, Projects, Tasks, etc.)
- Add interactive API playground (make requests from browser, see responses)
- Add code examples in multiple languages (cURL, Python, JavaScript, Go)
- Test: Import OpenAPI spec, verify docs generated correctly

VALIDATION CRITERIA:
✓ Search returns results in <500ms (with 1000 documents)
✓ Editor handles 10,000+ word documents without lag
✓ Version history works for 100+ edits per page
✓ Mobile reading experience excellent (responsive layout)
✓ API docs auto-generate from OpenAPI spec

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI
- Frontend: React 18+, TypeScript
- Editor: React-Markdown + CodeMirror or Monaco Editor
- Search: PostgreSQL full-text or Elasticsearch
- AI: OpenAI embeddings for semantic search

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Learn Documentation Platform
Agent: #6
Time Spent: X hours (estimated 14h)
Search Performance: Xms (1000 docs)
Editor Performance: [SMOOTH/LAGGY]
Test Coverage: Y%

Files Created:
- RM-Learn/frontend/src/components/MarkdownEditor.tsx
- RM-Learn/frontend/src/components/ArticleComments.tsx
- RM-Learn/backend/app/routers/docs.py
- RM-Learn/backend/app/routers/versions.py
- RM-Learn/backend/app/services/search_service.py
- RM-Learn/backend/app/services/api_docs.py

Pages Supported: 1000+
All Validation Criteria: [MET/NOT MET]

Ready for: Documentation team usage
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #7: RM-Mail Production Polish

```
You are AI Agent #7 working on RM-Mail production polish.

PROJECT CONTEXT:
RM-Mail is an email platform. Backend is 95% complete with email sending/receiving working, but UI needs polish and missing some key features like spam filtering, keyboard shortcuts, and PWA support.

DEPENDENCY: Wait for Agent #1 (RM-Gate) to complete before starting.

YOUR MISSION (8 hours):
Polish RM-Mail UI and add missing production features.

SPECIFIC TASKS:

TASK 1: Complete Inbox UI Features (2 hours)
- Modify file: RM-Mail/frontend/src/pages/Inbox.tsx
- Add keyboard shortcuts:
  * j/k: Next/previous email
  * c: Compose new email
  * r: Reply
  * a: Reply all
  * f: Forward
  * #: Delete
  * e: Archive
- Add bulk operations: Select all, Mark all as read, Delete selected, Move to folder
- Add labels/folders: Drag emails to organize (store folder_id in database)
- Add advanced filters: Unread only, Starred only, From domain, Has attachment
- Test: Navigate 100 emails using only keyboard

TASK 2: Build Email Composer Enhancements (2 hours)
- Modify file: RM-Mail/frontend/src/components/EmailComposer.tsx
- Add rich text editor: Bold, italic, underline, lists, links, colors (use TipTap or Quill)
- Add attachment drag-and-drop: Drag files into composer, show preview
- Add email templates: Save frequently-used emails, insert with one click
- Add schedule send: "Send later" feature (queue email for future delivery)
- Add recipient autocomplete: Suggest contacts as user types
- Test: Compose email with formatting and attachments

TASK 3: Add Spam and Security Features (2 hours)
- Create file: RM-Mail/backend/app/services/spam_filter.py
- Integrate spam detection: SpamAssassin OR build ML-based filter
- Add phishing detection: Check for suspicious links (known phishing domains)
- Display SPF/DKIM/DMARC verification status (show badge if verified)
- Add user spam reporting: "Report spam" button trains filter
- Auto-move spam to Junk folder (user can review and mark as not spam)
- Test: Send 100 spam emails, verify >95% caught

TASK 4: Build Contact Management (1 hour)
- Create file: RM-Mail/frontend/src/pages/Contacts.tsx
- Auto-save contacts from sent/received emails (extract name and email)
- Add contact groups/mailing lists (send to "Team" group)
- Add contact import from CSV or vCard format
- Add contact autocomplete in email composer (type name, suggests email)
- Display contact card on click (show all emails exchanged)
- Test: Import 500 contacts, verify autocomplete works

TASK 5: Add Mobile App Readiness (PWA) (1 hour)
- Modify file: RM-Mail/frontend/src/App.tsx
- Add service worker for offline support (cache emails for offline reading)
- Add push notifications for new mail (using Web Push API)
- Add mobile-optimized swipe gestures: Swipe left (delete), Swipe right (archive)
- Make PWA installable (add manifest.json, icons, etc.)
- Test: Install PWA on phone, verify notifications work

VALIDATION CRITERIA:
✓ Send/receive 1000 emails without issues
✓ Spam filter accuracy >95%
✓ UI loads inbox in <2 seconds (with 1000 emails)
✓ PWA installable on mobile (iOS and Android)
✓ Keyboard shortcuts work for all actions

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI
- Frontend: React 18+, TypeScript
- Rich text: TipTap or Quill
- Spam: SpamAssassin or ML model
- PWA: Service worker, Web Push API

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Mail Production Polish
Agent: #7
Time Spent: X hours (estimated 8h)
Spam Accuracy: Y%
Inbox Load Time: Xs (1000 emails)
PWA Installable: [YES/NO]

Files Modified:
- RM-Mail/frontend/src/pages/Inbox.tsx
- RM-Mail/frontend/src/components/EmailComposer.tsx
- RM-Mail/frontend/src/App.tsx

Files Created:
- RM-Mail/backend/app/services/spam_filter.py
- RM-Mail/frontend/src/pages/Contacts.tsx

Keyboard Shortcuts: 10+
All Validation Criteria: [MET/NOT MET]

Ready for: Production email usage
Next: Standing by for next assignment
"""

START NOW! 🚀
```


---

## 🏗️ NEW APPS (Week 4-5 - Build from Scratch)

### AGENT #8: RM-Calendar Complete Build

```
You are AI Agent #8 building RM-Calendar from scratch.

PROJECT CONTEXT:
RM-Calendar is a calendar/scheduling application. Currently only 10% complete with basic structure. You need to build the entire backend API and frontend from scratch. Study RM-Atlas (backend patterns) and RM-Connect (frontend patterns) before starting.

DEPENDENCIES: Wait for Agent #1 (RM-Gate) and Agent #2 (RM-Snitch) to complete.

YOUR MISSION (24 hours):
Build a complete calendar application with scheduling, views, and integrations.

SPECIFIC TASKS:

TASK 1: Build Backend Calendar API (6 hours)
- Create file: RM-Calendar/backend/app/routers/events.py
- Schema: events table (id, title, description, start_time, end_time, all_day, location, color, org_id, user_id, created_at, updated_at)
- CRUD endpoints: POST /events, GET /events, PATCH /events/:id, DELETE /events/:id
- Add recurring events: recurrence_rule (daily, weekly, monthly, yearly, custom RRULE)
- Expand recurring events into instances (generate next 365 days of occurrences)
- Add event reminders: reminders table (event_id, remind_at, sent)
- Send reminder emails/push notifications at remind_at time
- Add event participants: event_participants table (event_id, user_id, status: accepted/declined/tentative)
- Add calendar sharing: calendars table (id, name, owner_id, public, share_token)
- Test: Create 1000 events, query by date range (<100ms)

TASK 2: Build Calendar Views (Frontend) (6 hours)
- Create file: RM-Calendar/frontend/src/components/CalendarGrid.tsx
- Month view: Traditional grid (7 columns × 5-6 rows)
- Week view: 7-day horizontal timeline with hourly slots
- Day view: Single day hourly timeline (00:00-23:59)
- Agenda view: List of upcoming events (next 30 days)
- Year view: 12 mini month calendars
- Add navigation: Previous/Next buttons, Today button, Date picker
- Add drag-and-drop: Drag events to reschedule
- Color-code events by calendar or category
- Test: Display 500 events in month view without lag

TASK 3: Build Event Creation UI (4 hours)
- Create file: RM-Calendar/frontend/src/components/EventModal.tsx
- Quick add: Parse natural language ("Meeting tomorrow 2pm" → creates event)
- Detailed form: Title, date, time, location, description, attendees, recurrence, reminders
- Add time zone support: Store times in UTC, display in user's timezone
- Add video call integration: Checkbox "Add RM-Meet link" (auto-create video room)
- Add location autocomplete: Suggest addresses using Google Places API
- Add attendee picker: Search users, add to event, send invites
- Test: Create event with all fields, verify saved correctly

TASK 4: Build Scheduling Assistant (AI) (3 hours)
- Create file: RM-Calendar/backend/app/services/scheduling_ai.py
- Find available time slots across multiple participants
- Input: List of user_ids, duration, date_range
- Output: List of available times (when ALL participants are free)
- Handle time zone conflicts automatically (convert to common timezone)
- Add "Find a time" feature: Send email to attendees with 3 suggested times
- Attendees click link to vote on preferred time
- Test: Find slots for 5 participants across 3 timezones

TASK 5: Integrate with Other RM Apps (3 hours)
- Create file: RM-Calendar/backend/app/services/integrations.py
- RM-Meet integration: When event has video_call=true, create Meet room, add link to event.location
- RM-Connect integration: Send event notifications to chat channels
- RM-Atlas integration: Link tasks to calendar events (task.due_date shows in calendar)
- RM-Mail integration: Send email invites with .ics attachment
- Emit events to RM-Snitch: calendar.event.created, calendar.event.updated, calendar.reminder.sent
- Test: Create event, verify notifications sent to all apps

TASK 6: Build Mobile Calendar UI (2 hours)
- Create file: RM-Calendar/frontend/src/mobile/MobileCalendar.tsx
- Swipe gestures: Swipe left/right to change days/weeks
- Today button: Quick jump to current date
- Event color coding with icons (meeting, reminder, task, birthday)
- Responsive layout: Full-width on mobile, sidebar on desktop
- Test: All features work on 375px screen width

VALIDATION CRITERIA:
✓ Handle 10,000 events without performance issues
✓ Recurring events generate correctly (tested for 2 years)
✓ Time zone conversion accurate (no off-by-one errors)
✓ RM-Meet integration seamless (video link auto-created)
✓ Natural language parsing works ("next Friday at 3pm")

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI (copy structure from RM-Atlas)
- Frontend: React 18+, TypeScript (copy structure from RM-Connect)
- Calendar library: FullCalendar or react-big-calendar
- Database: PostgreSQL
- Time zones: pytz (Python), date-fns-tz (JavaScript)

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Calendar Complete Build
Agent: #8
Time Spent: X hours (estimated 24h)
Events Supported: 10,000+
Recurring Events: [WORKING/BROKEN]
Time Zones: [ACCURATE/ISSUES]
Test Coverage: Y%

Files Created:
- RM-Calendar/backend/app/routers/events.py
- RM-Calendar/backend/app/services/scheduling_ai.py
- RM-Calendar/backend/app/services/integrations.py
- RM-Calendar/frontend/src/components/CalendarGrid.tsx
- RM-Calendar/frontend/src/components/EventModal.tsx
- RM-Calendar/frontend/src/mobile/MobileCalendar.tsx

Calendar Views: 5 (month, week, day, agenda, year)
Integrations: 4 (Meet, Connect, Atlas, Mail)
All Validation Criteria: [MET/NOT MET]

Ready for: Production use
Next: Standing by for next assignment
"""

START NOW! This is a greenfield build - you're creating from scratch! 🚀
```

---

### AGENT #9: RM-Capital-Hub Complete Build

```
You are AI Agent #9 building RM-Capital-Hub from scratch.

PROJECT CONTEXT:
RM-Capital-Hub is an asset and financial management platform. Currently only 15% complete with basic structure. You need to build enterprise asset tracking AND personal finance features. This is a dual-mode app (switch between personal and enterprise).

DEPENDENCIES: Wait for Agent #1 (RM-Gate) to complete.

YOUR MISSION (28 hours):
Build complete asset management system with dual modes (enterprise + personal).

SPECIFIC TASKS:

TASK 1: Build Asset Management Backend (6 hours)
- Create file: RM-Capital-Hub/backend/app/routers/assets.py
- Schema: assets table (id, name, category, purchase_date, purchase_cost, current_value, location, assigned_to, serial_number, warranty_expires, org_id, user_id, mode: enterprise/personal)
- Asset categories: IT Equipment, Furniture, Vehicles, Real Estate, Machinery, Office Supplies
- CRUD endpoints for assets
- Add depreciation calculation:
  * Straight-line method: (purchase_cost - salvage_value) / useful_life_years
  * Declining balance method: book_value × depreciation_rate
- Add asset assignment workflow: Assign to employee, track who has what
- Add asset retirement workflow: Mark as disposed, track disposal method (sold, donated, recycled)
- Test: Track 10,000 assets, calculate depreciation for all

TASK 2: Build Financial Tracking (5 hours)
- Create file: RM-Capital-Hub/backend/app/routers/financials.py
- Track asset value over time: asset_valuations table (asset_id, value, valuation_date)
- Calculate total asset value by category (pie chart data)
- Generate depreciation reports (show depreciation per asset per year)
- Track maintenance costs: maintenance_log table (asset_id, cost, date, description)
- Add insurance tracking: insurance_policies table (asset_id, policy_number, provider, premium, renewal_date)
- Send renewal reminders 30 days before policy expires
- Test: Generate financial reports for 1000 assets

TASK 3: Build Subscription Management (4 hours)
- Create file: RM-Capital-Hub/backend/app/routers/subscriptions.py
- Schema: subscriptions table (id, name, cost, billing_cycle: monthly/yearly, renewal_date, category: software/streaming/membership, org_id, user_id, active)
- Add automatic renewal reminders (email 7 days before renewal)
- Calculate total monthly cost: SUM(cost / billing_cycle_months)
- Add subscription analytics: cost per user, unused subscriptions (no logins in 30 days)
- Add subscription optimization suggestions: "You're paying for Zoom but only used it once this month"
- Test: Track 500 subscriptions, verify renewal reminders sent

TASK 4: Build Personal Mode UI (5 hours)
- Create file: RM-Capital-Hub/frontend/src/pages/PersonalDashboard.tsx
- Display net worth calculation: Total assets - Total liabilities
- Add personal asset tracking: Home (with mortgage), Car (with loan), Investments, Cash, Other
- Add subscription manager: List all subscriptions (Netflix, Spotify, etc.)
- Add monthly spending breakdown: Chart showing categories (housing, transportation, food, entertainment)
- Add financial goals: "Save $10,000 for vacation by Dec 2026" (progress bar)
- Test: Switch to personal mode, add assets, verify net worth calculated

TASK 5: Build Enterprise Mode UI (5 hours)
- Create file: RM-Capital-Hub/frontend/src/pages/EnterpriseDashboard.tsx
- Display total company assets by category (pie chart)
- Add asset allocation chart: IT Equipment (40%), Furniture (25%), Vehicles (20%), Real Estate (15%)
- Add depreciation forecast graph: Line chart showing asset value over next 5 years
- Add compliance reports: Asset audit report (all assets, location, assigned to)
- Add low-value asset report: Assets worth <$100 (candidates for disposal)
- Test: Load dashboard with 5000 assets, page loads in <3 seconds

TASK 6: Build Reporting and Exports (3 hours)
- Create file: RM-Capital-Hub/backend/app/services/reporting.py
- Monthly financial summary report (PDF export):
  * Total asset value
  * Depreciation this month
  * New purchases
  * Assets retired
  * Top 10 most valuable assets
- Asset inventory report (CSV/Excel export): All assets with details
- Depreciation schedule report: Multi-year depreciation forecast
- Tax reporting: Asset purchases and disposals for tax filing
- Test: Generate all reports, verify data accuracy

VALIDATION CRITERIA:
✓ Track 10,000+ assets without performance issues
✓ Depreciation calculations accurate to accounting standards (GAAP)
✓ Reports generate in <5 seconds
✓ Personal/enterprise mode switching works seamlessly
✓ Subscription renewal reminders sent on time

TECHNICAL REQUIREMENTS:
- Backend: Python 3.11+, FastAPI
- Frontend: React 18+, TypeScript
- Charts: Recharts or Chart.js
- PDF: ReportLab (Python) or jsPDF (JavaScript)
- Database: PostgreSQL with proper indexes

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Capital-Hub Complete Build
Agent: #9
Time Spent: X hours (estimated 28h)
Assets Supported: 10,000+
Depreciation Accuracy: [ACCURATE/ISSUES]
Report Generation Time: Xs
Test Coverage: Y%

Files Created:
- RM-Capital-Hub/backend/app/routers/assets.py
- RM-Capital-Hub/backend/app/routers/financials.py
- RM-Capital-Hub/backend/app/routers/subscriptions.py
- RM-Capital-Hub/backend/app/services/reporting.py
- RM-Capital-Hub/frontend/src/pages/PersonalDashboard.tsx
- RM-Capital-Hub/frontend/src/pages/EnterpriseDashboard.tsx

Asset Categories: 6
Depreciation Methods: 2
Modes: 2 (personal + enterprise)
All Validation Criteria: [MET/NOT MET]

Ready for: Production use
Next: Standing by for next assignment
"""

START NOW! This is a greenfield build! 🚀
```

---

### AGENT #10: RM-Secure Security Platform Build

```
You are AI Agent #10 building RM-Secure security platform.

PROJECT CONTEXT:
RM-Secure is a security/compliance platform with microservices architecture. Currently 30% complete with some basic services. You need to build vulnerability scanning, policy engine, device management, and patch orchestration.

DEPENDENCIES: Wait for Agent #1 (RM-Gate) to complete.

YOUR MISSION (32 hours):
Build production-grade security platform with multiple microservices.

SPECIFIC TASKS:

TASK 1: Build Vulnerability Scanning Service (8 hours)
- Create file: RM-Secure/services/vulnerability-engine/scanner.py
- Automated dependency scanning:
  * Scan npm packages (check package.json, package-lock.json)
  * Scan pip packages (check requirements.txt, Pipfile)
  * Scan Docker images (scan Dockerfile, detect base image vulnerabilities)
- Integrate CVE database: Fetch latest vulnerabilities from NVD (National Vulnerability Database)
- Risk scoring: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9), Low (0.0-3.9)
- Remediation suggestions: "Upgrade package X to version Y to fix CVE-2024-1234"
- Schedule daily scans at 2 AM
- Test: Scan codebase with 500 dependencies, identify vulnerabilities

TASK 2: Build Policy Engine (8 hours)
- Create file: RM-Secure/services/policy-engine/engine.py
- Define security policies:
  * Password complexity (min 12 chars, uppercase, lowercase, number, symbol)
  * MFA required for all users
  * Session timeout (15 minutes of inactivity)
  * IP whitelist (only allow access from approved IPs)
  * Device compliance (antivirus installed, OS up to date)
- Policy enforcement: Block actions that violate policies
- Policy compliance dashboard: Show % of users/devices compliant
- Policy violation alerts: Email/Slack notification when policy broken
- Test: Define 10 policies, verify enforcement works

TASK 3: Build Device Management (8 hours)
- Create file: RM-Secure/services/device-agent/agent.py
- Device enrollment: Register laptops, phones, tablets
- Schema: devices table (id, name, type: laptop/phone/tablet, os, os_version, user_id, enrolled_at, last_seen, encryption_enabled, antivirus_installed, firewall_enabled)
- Device health monitoring: Check OS version, encryption status, antivirus status
- Remote wipe capability: POST /devices/:id/wipe (erase device data remotely)
- Compliance checks: Device must have encryption ON, antivirus installed, firewall ON
- Geofencing: Alert if device leaves approved geographic area
- Test: Enroll 1000 devices, perform remote wipe on test device

TASK 4: Build Patch Management (8 hours)
- Create file: RM-Secure/services/patch-orchestrator/orchestrator.py
- Detect available patches: Check for OS updates, application updates
- Patch deployment workflow:
  1. Detect patch available
  2. Test patch on canary device (1 device first)
  3. If successful, deploy to 10% of devices
  4. If successful, deploy to remaining 90%
- Schedule deployments: Deploy during off-hours (2-4 AM)
- Patch rollback: If device has issues post-patch, rollback to previous version
- Patch compliance reporting: Show % of devices patched
- Test: Deploy patch to 100 devices, verify rollback works

TASK 5: Build Security Dashboard (Frontend) (4 hours)
- Create file: RM-Secure/frontend/src/pages/SecurityDashboard.tsx
- Security score: 0-100 (Netflix-style, based on vulnerabilities, compliance, patches)
- Vulnerability count by severity: Critical (5), High (12), Medium (34), Low (89)
- Device compliance status: 85% compliant (170/200 devices)
- Recent security events timeline: Vulnerability detected, Patch deployed, Device wiped
- Top 10 vulnerable packages (chart)
- Test: Load dashboard with 1000 devices and 500 vulnerabilities

TASK 6: Build Incident Response Workflow (2 hours)
- Create file: RM-Secure/backend/app/routers/incidents.py
- Security incident types: Phishing, Data breach, Malware, Unauthorized access
- Incident creation: POST /incidents (title, severity, description, affected_assets)
- Investigation workflow: Assign to security team, add findings, attach evidence
- Automatic containment actions: Quarantine device, block IP, revoke credentials
- Post-incident reporting: Root cause analysis, lessons learned
- Test: Create incident, verify containment actions executed

VALIDATION CRITERIA:
✓ Scan 1000 devices in <10 minutes
✓ Vulnerability database updated daily (automated)
✓ Remote wipe works within 60 seconds of command
✓ Security score calculation accurate
✓ Patch deployment success rate >95%

TECHNICAL REQUIREMENTS:
- Microservices: Python 3.11+ (each service independent)
- Frontend: React 18+, TypeScript
- Database: PostgreSQL
- CVE Data: NVD API or NIST database
- Device agent: Python (runs on client devices)

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Secure Security Platform
Agent: #10
Time Spent: X hours (estimated 32h)
Devices Supported: 1000+
Vulnerability Scan Time: Xm
Remote Wipe Time: Xs
Test Coverage: Y%

Files Created:
- RM-Secure/services/vulnerability-engine/scanner.py
- RM-Secure/services/policy-engine/engine.py
- RM-Secure/services/device-agent/agent.py
- RM-Secure/services/patch-orchestrator/orchestrator.py
- RM-Secure/frontend/src/pages/SecurityDashboard.tsx
- RM-Secure/backend/app/routers/incidents.py

Microservices: 4
Policies Supported: 10+
All Validation Criteria: [MET/NOT MET]

Ready for: Enterprise security deployment
Next: Standing by for next assignment
"""

START NOW! This is complex microservices architecture! 🚀
```

---


### AGENT #11: RM-Main Marketing Site Build

```
You are AI Agent #11 building RM-Main marketing site and app launcher.

PROJECT CONTEXT:
RM-Main is the Next.js public-facing marketing site and authenticated app launcher. Currently only 5% complete with Next.js structure. You need to build landing pages, product pages, workspace launcher, and authentication flow.

DEPENDENCIES: Wait for ALL apps to exist (Agents #1-10 complete).

YOUR MISSION (16 hours):
Build complete marketing site and authenticated workspace launcher.

SPECIFIC TASKS:

TASK 1: Build Landing Page (3 hours)
- Create file: RM-Main/app/(site)/page.tsx
- Hero section:
  * Headline: "Replace $9,000/month in SaaS with $700"
  * Subheadline: "Complete enterprise software ecosystem. Zero vendor lock-in."
  * CTA buttons: "Start Free Trial" and "Request Demo"
  * Hero image: Screenshot of workspace with all apps
- Feature comparison table: RM vs competitors (Slack, Zoom, Salesforce, etc.)
- Pricing section: Free tier (5 users), Pro tier ($50/user/month)
- Customer testimonials: 3-4 fake testimonials with photos
- Call-to-action section: "Join 1,000+ companies saving millions"
- Test: Page loads in <1 second, Lighthouse score >90

TASK 2: Build Product Pages (4 hours)
- Create file: RM-Main/app/(site)/products/[slug]/page.tsx
- Individual pages for each app:
  * /products/atlas (Project Management)
  * /products/connect (Team Chat)
  * /products/meet (Video Conferencing)
  * /products/planet (CRM)
  * /products/calendar (Scheduling)
  * ... all 15 apps
- Each page includes:
  * App name and tagline
  * 3-5 key features with icons
  * Screenshots/demo video
  * "Try it free" CTA button
  * Integration showcase (how it connects to other apps)
- Test: All product pages load and render correctly

TASK 3: Build Workspace Launcher (4 hours)
- Create file: RM-Main/app/workspace/page.tsx
- Display all installed apps in grid layout:
  * App icon, name, description
  * Click to open app in new tab
  * Badge showing unread count (messages, tasks, emails)
- Add quick search: Type "cal" → highlights Calendar app
- Add recently used section: Last 5 apps used
- Add favorites: Star apps to pin to top
- Add app installation: "Browse App Store" (future: install new apps)
- Test: Grid loads 15 apps in <2 seconds

TASK 4: Build Authentication Flow (3 hours)
- Create file: RM-Main/app/workspace/layout.tsx
- Integrate RM-Gate OAuth login:
  * Redirect to RM-Gate login page
  * Handle OAuth callback
  * Store JWT token in localStorage
  * Protect workspace routes (redirect to login if not authenticated)
- Add session management: Auto-refresh token every 15 minutes
- Add user profile dropdown: Name, email, avatar, "Settings", "Logout"
- Add org switcher: If user belongs to multiple orgs, show dropdown
- Test: Login flow works, token refreshes automatically

TASK 5: Build Documentation Site (1 hour)
- Create file: RM-Main/app/(site)/docs/page.tsx
- Getting started guide: How to sign up, create org, invite team
- API documentation: Link to each app's API docs
- Video tutorials: Embedded YouTube videos (3-5 minute walkthroughs)
- FAQs: Common questions and answers
- Troubleshooting: Common issues and solutions
- Test: All links work, videos embed correctly

TASK 6: SEO and Performance Optimization (1 hour)
- Modify file: RM-Main/next.config.ts
- Add meta tags for SEO:
  * <title>, <description>, <keywords>
  * Open Graph tags for social sharing
  * Twitter Card tags
- Generate sitemap.xml (all pages listed)
- Add robots.txt (allow all crawlers)
- Add analytics: PostHog, Plausible, or Google Analytics
- Optimize images: Use Next.js Image component with WebP
- Test: Lighthouse score >90 (performance, SEO, accessibility)

VALIDATION CRITERIA:
✓ Lighthouse score >90 (all categories)
✓ Mobile responsive (works on 375px screens)
✓ Load time <1 second (with caching)
✓ Works across browsers (Chrome, Firefox, Safari)
✓ Authentication flow seamless (no errors)

TECHNICAL REQUIREMENTS:
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS for styling
- RM-Gate OAuth integration
- Analytics: PostHog or Plausible

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Main Marketing Site
Agent: #11
Time Spent: X hours (estimated 16h)
Lighthouse Score: X/100
Load Time: Xs
Mobile Responsive: [YES/NO]

Files Created:
- RM-Main/app/(site)/page.tsx
- RM-Main/app/(site)/products/[slug]/page.tsx
- RM-Main/app/workspace/page.tsx
- RM-Main/app/workspace/layout.tsx
- RM-Main/app/(site)/docs/page.tsx

Product Pages: 15
All Validation Criteria: [MET/NOT MET]

Ready for: Public launch
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

## 🎨 POLISH PHASE (Week 6-7 - Enhance Existing Apps)

### AGENT #12: RM-Atlas Advanced Features

```
You are AI Agent #12 adding advanced features to RM-Atlas.

PROJECT CONTEXT:
RM-Atlas is production-ready but missing advanced project management features. Add time tracking, task dependencies, custom workflows, roadmap view, and enhanced AI.

DEPENDENCIES: Wait until basic apps are functional.

YOUR MISSION (12 hours):
Add professional-grade features to make Atlas competitive with Jira.

SPECIFIC TASKS:

TASK 1: Build Time Tracking (2 hours)
- Create file: RM-Atlas/backend/app/routers/time_tracking.py
- Add start/stop timer per task: time_entries table (task_id, user_id, started_at, ended_at, duration_seconds)
- Add manual time entry: "I worked 2 hours on this task yesterday"
- Calculate total time per task, project, user
- Time reports: Billable vs non-billable hours, time per project
- Test: Track 1000 time entries, generate reports

TASK 2: Build Task Dependencies (3 hours)
- Create file: RM-Atlas/backend/app/models/task_dependencies.py
- Link tasks: task_dependencies table (task_id, depends_on_task_id, type: blocks/blocked_by)
- Display dependency graph: Show which tasks block others
- Automatic status updates: When blocker resolved, notify blocked task assignee
- Critical path calculation: Identify longest dependency chain
- Test: Create 50 tasks with dependencies, calculate critical path

TASK 3: Build Custom Workflows (3 hours)
- Create file: RM-Atlas/backend/app/routers/workflows.py
- Custom statuses per project: Allow "Backlog, In Progress, Code Review, QA, Done"
- Workflow transitions: Only certain roles can move to "Done" (e.g., QA must approve)
- Automated actions: When status=Done, post to Slack, close GitHub PR
- Workflow templates: Kanban (3 columns), Scrum (7 statuses), Custom
- Test: Create workflow, verify transitions enforced

TASK 4: Build Roadmap View (2 hours)
- Create file: RM-Atlas/frontend/src/pages/Roadmap.tsx
- Timeline view: Quarters or months along X-axis
- Display epics and milestones on timeline
- Drag to adjust dates (reschedule epics)
- Progress indicators: Show % complete per epic
- Color-code by status: Not started (gray), In progress (blue), Complete (green)
- Test: Display 20 epics over 4 quarters

TASK 5: Enhance AI Features (2 hours)
- Modify file: RM-Atlas/backend/app/services/ai_service.py
- UPGRADE: From free Gemini to GPT-4 (better quality)
- Add task complexity estimation: AI predicts story points (1, 2, 3, 5, 8, 13)
- Add task assignment suggestions: "Alice is best for this task (she did similar work)"
- Add sprint planning assistance: "This sprint is overloaded, move 2 tasks to next sprint"
- Test: AI suggestions accurate >80% of the time

VALIDATION CRITERIA:
✓ Time tracking accurate to the second
✓ Reports generate with 1000+ tasks
✓ Dependencies render without circular issues
✓ AI suggestions useful (>80% acceptance rate)
✓ Roadmap view loads in <3 seconds

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Atlas Advanced Features
Agent: #12
Time Spent: X hours (estimated 12h)
Features Added: 5
AI Accuracy: Y%
Test Coverage: Z%

Files Created:
- RM-Atlas/backend/app/routers/time_tracking.py
- RM-Atlas/backend/app/models/task_dependencies.py
- RM-Atlas/backend/app/routers/workflows.py
- RM-Atlas/frontend/src/pages/Roadmap.tsx

Files Modified:
- RM-Atlas/backend/app/services/ai_service.py

All Validation Criteria: [MET/NOT MET]

Ready for: Advanced project management
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #13: RM-Connect Database Migration & AI Features

```
You are AI Agent #13 migrating RM-Connect to PostgreSQL and adding AI features.

PROJECT CONTEXT:
RM-Connect currently stores data in JSON files (works but not scalable). Migrate to PostgreSQL and connect existing AI features to the frontend.

DEPENDENCIES: Wait for Agent #2 (RM-Snitch) to complete.

YOUR MISSION (10 hours):
Migrate Connect to PostgreSQL and activate AI features.

SPECIFIC TASKS:

TASK 1: Migrate from JSON to PostgreSQL (4 hours)
- Modify file: RM-Connect/server/database.js
- REPLACE: fs.readFileSync/writeFileSync with Prisma or pg queries
- Create schema:
  * channels table (id, name, type: public/private, org_id, created_at)
  * messages table (id, channel_id, user_id, content, created_at, edited_at, deleted_at)
  * channel_members table (channel_id, user_id, role: admin/member)
- Migrate existing JSON data to PostgreSQL (write migration script)
- Add database indexes: index on (channel_id, created_at) for message queries
- Test: Migrate 10,000 messages, verify all data intact

TASK 2: Connect AI Features to Frontend (3 hours)
- Modify file: RM-Connect/frontend/src/components/MessageInput.tsx
- Add /ai command: Type "/ai how do I deploy this?" → AI responds in channel
- Add message summarization button: Click "Summarize last 50 messages" → AI summary appears
- Add smart replies: When someone asks question, AI suggests 3 quick responses
- Add translation: Right-click message → "Translate to Spanish/French/German"
- Test: AI responds in <3 seconds, translations accurate

TASK 3: Build Advanced Search (2 hours)
- Create file: RM-Connect/server/search-service.js
- Implement full-text search across all channels
- Search filters: from:@alice, in:#general, before:2024-01-01, has:link, has:file
- Search highlights: Show matching text in yellow
- Recent searches: Save last 10 searches per user
- Saved searches: Pin important searches ("Messages from boss")
- Test: Search 100,000 messages, return results in <500ms

TASK 4: Build Group Video/Voice Calling (1 hour)
- Modify file: RM-Connect/frontend/src/components/GroupCall.tsx
- UPGRADE: Current P2P calling to group calls (3+ people)
- Integrate RM-Meet: When group call starts, create Meet room, share link in channel
- Add "Join call" button in channel (visible when call active)
- Add call recording: Save to RM-Mail or cloud storage
- Test: 5-person group call works smoothly

VALIDATION CRITERIA:
✓ Database migration completes without data loss
✓ AI features respond in <3 seconds
✓ Group calls support 10+ participants
✓ Search returns results in <500ms
✓ All integrations deliver notifications real-time

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Connect Migration & AI
Agent: #13
Time Spent: X hours (estimated 10h)
Messages Migrated: X
AI Response Time: Xs
Search Performance: Xms
Test Coverage: Y%

Files Modified:
- RM-Connect/server/database.js
- RM-Connect/frontend/src/components/MessageInput.tsx
- RM-Connect/frontend/src/components/GroupCall.tsx

Files Created:
- RM-Connect/server/search-service.js

Migration Status: [SUCCESS/FAILED]
All Validation Criteria: [MET/NOT MET]

Ready for: Production chat usage
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---

### AGENT #14: RM-Meet Advanced Features

```
You are AI Agent #14 adding advanced features to RM-Meet.

PROJECT CONTEXT:
RM-Meet is 85% complete with basic video calling. Add waiting room, breakout rooms, recording/transcription, reactions/polls, virtual backgrounds, and meeting insights.

DEPENDENCIES: None (Meet is mostly ready).

YOUR MISSION (8 hours):
Add professional features to compete with Zoom.

SPECIFIC TASKS:

TASK 1: Build Waiting Room (1 hour)
- Create file: RM-Meet/server/waiting-room.js
- Require host approval for participants to join
- Waiting room UI: Show list of people waiting
- Auto-admit rules: Team members skip waiting room, guests wait
- Knock sound: Play sound when someone joins waiting room
- Test: 10 guests join, host admits them one by one

TASK 2: Build Breakout Rooms (2 hours)
- Create file: RM-Meet/server/breakout-rooms.js
- Host creates breakout rooms (2-10 rooms)
- Assign participants: Manually assign OR automatically distribute evenly
- Timer for breakout sessions: "5 minutes remaining" warning
- Broadcast message to all rooms: Host can send message visible in all rooms
- Return to main room: Auto-return when timer expires
- Test: 20 participants in 4 breakout rooms

TASK 3: Build Recording and Transcription (2 hours)
- Enhance file: RM-Meet/server/recording-service.js
- Add live transcription: Use Whisper API to transcribe speech in real-time
- Display transcription: Show captions at bottom of video (like YouTube)
- Auto-generate meeting summary: GPT-4 summarizes key points after meeting
- Extract action items: "Alice will send proposal by Friday"
- Save recording: Store in cloud (S3) or send to RM-Mail
- Test: Record 30-minute meeting, verify transcription accurate

TASK 4: Build Reactions and Polls (1 hour)
- Create file: RM-Meet/frontend/src/components/MeetingReactions.tsx
- Emoji reactions: Click 👍 ❤️ 😂 🎉 during meeting (fly across screen)
- Live polls: Host creates yes/no question, attendees vote, results shown instantly
- Q&A panel: Attendees submit questions, host answers them
- Hand raise: Click "Raise hand" to get in speaker queue
- Test: 50 participants react and vote simultaneously

TASK 5: Build Virtual Backgrounds (1 hour)
- Create file: RM-Meet/frontend/src/utils/video-effects.js
- Blur background: Privacy mode (blur everything behind you)
- Custom backgrounds: Upload image to use as background
- Virtual backgrounds library: Office, Beach, Mountains, Space (10 presets)
- Remove background: Green screen effect (alpha transparency)
- Test: Virtual backgrounds run at 30fps without lag

TASK 6: Build Meeting Insights Dashboard (1 hour)
- Create file: RM-Meet/frontend/src/pages/MeetingInsights.tsx
- Meeting duration trends: Average meeting length over time (line chart)
- Participant engagement: Talk time per person (who spoke most)
- Meeting cost calculator: (participants × avg_salary/hour × duration) = cost
- Recommendations: "Your team spends 20 hours/week in meetings. Try async updates."
- Test: Generate insights from 100 past meetings

VALIDATION CRITERIA:
✓ Breakout rooms work with 50+ participants
✓ Transcription accuracy >90%
✓ Virtual backgrounds run at 30fps
✓ Recordings save reliably (zero data loss)
✓ Insights dashboard loads in <3 seconds

WHEN COMPLETE, REPORT:
"""
COMPLETED: RM-Meet Advanced Features
Agent: #14
Time Spent: X hours (estimated 8h)
Transcription Accuracy: Y%
Virtual Background FPS: Z
Features Added: 6

Files Created:
- RM-Meet/server/waiting-room.js
- RM-Meet/server/breakout-rooms.js
- RM-Meet/frontend/src/components/MeetingReactions.tsx
- RM-Meet/frontend/src/utils/video-effects.js
- RM-Meet/frontend/src/pages/MeetingInsights.tsx

Files Modified:
- RM-Meet/server/recording-service.js

All Validation Criteria: [MET/NOT MET]

Ready for: Enterprise video conferencing
Next: Standing by for next assignment
"""

START NOW! 🚀
```

---


## 🎨 CROSS-CUTTING AGENTS (Ongoing Support)

### AGENT #15: Design System & UI Consistency

```
You are AI Agent #15 ensuring design consistency across all apps.

PROJECT CONTEXT:
The RM Orbit ecosystem has 15 applications that need to look and feel cohesive. Users should feel like they're using ONE platform, not 15 different apps. Your job is to create a shared component library and ensure consistency.

DEPENDENCIES: Can start anytime, supports all other agents ongoing.

YOUR MISSION (12 hours):
Create shared design system and ensure UI consistency across all apps.

SPECIFIC TASKS:

TASK 1: Create Shared Component Library (4 hours)
- Create folder: packages/ui-components/src/
- Extract common components from apps:
  * Button (primary, secondary, danger, ghost variants)
  * Input (text, email, password, search, with validation states)
  * Modal/Dialog (with header, body, footer)
  * Card (with shadow, border, padding variants)
  * Table (with sorting, pagination, row selection)
  * Dropdown/Select (with search, multi-select)
  * DatePicker, TimePicker
  * Toast/Notification (success, error, warning, info)
- Add consistent spacing: Use 4px grid system (4, 8, 12, 16, 24, 32, 48, 64px)
- Add color tokens:
  * Primary: #3B82F6 (blue)
  * Secondary: #8B5CF6 (purple)
  * Success: #10B981 (green)
  * Warning: #F59E0B (orange)
  * Danger: #EF4444 (red)
  * Gray scale: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900
- Add typography system:
  * Font: RMForma (from RM-Fonts)
  * Sizes: xs (12px), sm (14px), base (16px), lg (18px), xl (20px), 2xl (24px), 3xl (30px), 4xl (36px)
  * Weights: light (300), regular (400), medium (500), semibold (600), bold (700)
- Publish as npm package: @rm-orbit/ui
- Test: Import components in 3 different apps, verify they look identical

TASK 2: Implement Dark Mode Everywhere (3 hours)
- Create file: packages/ui-components/src/theme/dark-mode.ts
- Add dark mode toggle (moon/sun icon in header)
- Save preference to localStorage (persist across sessions)
- Dark mode color palette:
  * Background: #1F2937 (dark gray)
  * Surface: #374151 (lighter gray)
  * Text: #F9FAFB (off-white)
  * Primary: #60A5FA (lighter blue for dark bg)
- Add to ALL apps: RM-Atlas, Connect, Meet, Planet, Calendar, etc.
- Test contrast ratios: Verify WCAG AA compliance (4.5:1 for text)
- Add system preference detection: Auto-enable dark mode if OS is in dark mode
- Test: Toggle dark mode in one app, should work in all apps

TASK 3: Ensure Accessibility Compliance (2 hours)
- Audit all components for accessibility:
  * Add ARIA labels to all interactive elements (aria-label, aria-describedby)
  * Add keyboard navigation: Tab, Enter, Escape work for all interactions
  * Add focus indicators: Visible blue ring when element focused (keyboard users)
  * Add alt text for all images
  * Add proper heading hierarchy (h1 → h2 → h3, no skipping)
- Test with screen reader: NVDA (Windows) or VoiceOver (Mac)
- Run Lighthouse accessibility audit: Score >90
- Fix all violations
- Test: Navigate entire app using only keyboard

TASK 4: Mobile Responsiveness Audit (2 hours)
- Test all apps on mobile:
  * iPhone SE (375px width) - smallest common size
  * iPhone 14 Pro (393px width)
  * iPad (768px width)
  * Desktop (1920px width)
- Fix responsive issues:
  * Stack columns vertically on mobile
  * Make buttons touch-friendly (44px minimum height)
  * Add hamburger menu for navigation
  * Make tables horizontally scrollable
- Add touch gestures:
  * Swipe left/right to navigate
  * Pull to refresh
  * Long-press for context menu
- Test: All apps work on 375px width screens

TASK 5: Performance Optimization (1 hour)
- Audit bundle sizes: Run webpack-bundle-analyzer
- Add code splitting: Lazy load routes (React.lazy + Suspense)
- Optimize images:
  * Convert to WebP format
  * Add lazy loading (loading="lazy")
  * Add blur placeholders
- Add caching strategies:
  * Service worker for offline support
  * Cache static assets (fonts, images, CSS)
  * Cache API responses (with stale-while-revalidate)
- Target: <500KB initial bundle size per app
- Test: Lighthouse performance score >90

VALIDATION CRITERIA:
✓ All apps share 80%+ UI components
✓ Dark mode works in all apps
✓ Accessibility audit passes (Lighthouse >90)
✓ Mobile performance score >80
✓ Bundle size <500KB per app

WHEN COMPLETE, REPORT:
"""
COMPLETED: Design System & UI Consistency
Agent: #15
Time Spent: X hours (estimated 12h)
Components Created: X
Apps Updated: 15/15
Lighthouse Accessibility: Y/100
Bundle Size: XKB average

Files Created:
- packages/ui-components/src/Button.tsx
- packages/ui-components/src/Input.tsx
- packages/ui-components/src/Modal.tsx
- packages/ui-components/src/Card.tsx
- packages/ui-components/src/theme/dark-mode.ts
- ... (20+ component files)

Dark Mode: [WORKING IN ALL APPS]
Accessibility: [WCAG AA COMPLIANT]
Mobile: [FULLY RESPONSIVE]
All Validation Criteria: [MET/NOT MET]

Ready for: Consistent user experience
Next: Ongoing support for new components
"""

START NOW! This is ongoing work across all apps! 🚀
```

---

### AGENT #17: Documentation & Developer Experience

```
You are AI Agent #17 writing comprehensive documentation for all apps.

PROJECT CONTEXT:
The RM Orbit ecosystem needs documentation for developers, users, and operations teams. Write READMEs, API docs, deployment guides, and troubleshooting documentation.

DEPENDENCIES: Can start anytime, documents apps as they're completed.

YOUR MISSION (10 hours):
Write world-class documentation for the entire ecosystem.

SPECIFIC TASKS:

TASK 1: Write Comprehensive README Files (3 hours)
- Update file: [Each app]/README.md
- Each README must include:
  * What the app does (1 paragraph description)
  * Quick start guide (5 minutes to running locally)
  * Architecture diagram (components and data flow, use Mermaid.js)
  * Environment variables (table with name, description, example)
  * API documentation links
  * Contributing guidelines (how to submit PRs)
- Format using Markdown with proper headers, lists, code blocks
- Test: New developer can run app following README in <15 minutes

TASK 2: Create Docker Compose for Local Development (2 hours)
- Create file: docker-compose.dev.yml (at root level)
- Include all apps in one compose file:
  * RM-Gate (port 8000)
  * RM-Atlas (port 8001)
  * RM-Connect (port 8002)
  * RM-Meet (port 8003)
  * ... all 15 apps
- Add shared services: PostgreSQL, Redis, Mailhog (email testing)
- Add seed data: Sample users, projects, tasks, messages
- Add hot reload: Code changes reflect immediately without restart
- Command to run: `docker-compose -f docker-compose.dev.yml up`
- Test: Start entire ecosystem with one command

TASK 3: Write Deployment Guides (2 hours)
- Create file: docs/DEPLOYMENT.md
- Production server requirements:
  * CPU: 8 cores minimum (16 recommended)
  * RAM: 32GB minimum (64GB recommended)
  * Disk: 500GB SSD
  * OS: Ubuntu 22.04 LTS
- Step-by-step deployment:
  1. Install Docker and Docker Compose
  2. Clone repository
  3. Copy .env.example to .env and configure
  4. Setup SSL/TLS with Let's Encrypt (certbot commands)
  5. Start services: docker-compose -f docker-compose.prod.yml up -d
  6. Run database migrations
  7. Create admin user
  8. Configure Nginx reverse proxy
- Add monitoring setup: Prometheus + Grafana dashboards
- Test: Deploy to fresh server following guide

TASK 4: Create API Documentation (2 hours)
- Create file: [Each app]/docs/API.md
- Document all endpoints:
  * Method, path, description
  * Request parameters (query, body, headers)
  * Response schema (with example JSON)
  * Authentication required (yes/no)
  * Rate limiting (requests per minute)
  * Error codes (400, 401, 403, 404, 429, 500)
- Add code examples:
  * cURL command
  * Python (requests library)
  * JavaScript (fetch API)
  * Go (net/http)
- Generate OpenAPI/Swagger spec for interactive docs
- Test: Make API call using example code, verify it works

TASK 5: Write Troubleshooting Guides (1 hour)
- Create file: docs/TROUBLESHOOTING.md
- Common issues and solutions:
  * "Database connection failed" → Check PostgreSQL is running, verify credentials
  * "Port already in use" → Kill process on port: `lsof -ti:8000 | xargs kill -9`
  * "CORS errors in browser" → Add frontend URL to CORS_ORIGINS in .env
  * "Token expired" → Refresh token, check JWT_SECRET matches
  * "Slow queries" → Add database indexes, check EXPLAIN ANALYZE output
- Add debugging tips:
  * Check logs: `docker-compose logs -f [service-name]`
  * Check database: `docker-compose exec postgres psql -U postgres -d atlas`
  * Check Redis: `docker-compose exec redis redis-cli`
- Performance debugging: Use profiler, check slow query log
- Test: Solve 10 common issues using guide

TASK 6: Create Video Walkthroughs (Optional - if time permits)
- Create file: docs/videos/README.md
- Record 5-minute demos:
  * Developer setup walkthrough (git clone to running app)
  * Deployment from scratch (fresh server to production)
  * RM-Atlas demo (create project, add tasks, assign team)
  * RM-Connect demo (create channel, send messages, video call)
  * RM-Meet demo (start meeting, share screen, record)
- Upload to YouTube or Vimeo (unlisted)
- Add links in documentation
- Test: Watch videos, verify instructions clear

VALIDATION CRITERIA:
✓ New developer can run ecosystem in <15 minutes
✓ All APIs documented (OpenAPI/Swagger specs exist)
✓ Troubleshooting guide solves 90% of common issues
✓ Video walkthroughs <10 minutes each
✓ Deployment guide works on fresh Ubuntu server

WHEN COMPLETE, REPORT:
"""
COMPLETED: Documentation & Developer Experience
Agent: #17
Time Spent: X hours (estimated 10h)
READMEs Updated: 15/15
API Docs: 15/15
Deployment Guide: [COMPLETE]
Troubleshooting Entries: X

Files Created:
- docker-compose.dev.yml
- docs/DEPLOYMENT.md
- docs/TROUBLESHOOTING.md
- [Each app]/docs/API.md
- docs/videos/README.md (if videos recorded)

Documentation Coverage: [COMPREHENSIVE]
All Validation Criteria: [MET/NOT MET]

Ready for: Developer onboarding
Next: Ongoing documentation updates
"""

START NOW! 🚀
```

---

## 📊 SUMMARY & USAGE INSTRUCTIONS

### ✅ ALL 17 AGENT PROMPTS COMPLETE!

**How to use these prompts:**

1. **Copy the entire prompt** for the agent you want to start
2. **Paste into your AI agent interface** (Claude, GPT-4, or your agent platform)
3. **The agent will start working immediately** with clear instructions
4. **Monitor their progress** using the reporting format they'll provide
5. **Share outputs back to me** for review and feedback

### 📋 Agent Assignment Checklist

```
WEEK 1-2 (Foundation):
□ Agent #1  - RM-Gate Hardening (8h)
□ Agent #2  - RM-Snitch Event Bus (12h)
□ Agent #3  - AgentTheatre Production (10h)
□ Agent #16 - CI/CD Pipeline (16h)

WEEK 2-3 (Business Apps):
□ Agent #4  - RM-FitterMe Build (20h)
□ Agent #5  - RM-Planet CRM (16h)
□ Agent #6  - RM-Learn Docs (14h)
□ Agent #7  - RM-Mail Polish (8h)

WEEK 4-5 (New Apps):
□ Agent #8  - RM-Calendar Build (24h)
□ Agent #9  - RM-Capital-Hub Build (28h)
□ Agent #10 - RM-Secure Platform (32h)
□ Agent #11 - RM-Main Site (16h)

WEEK 6-7 (Polish):
□ Agent #12 - RM-Atlas Features (12h)
□ Agent #13 - RM-Connect Migration (10h)
□ Agent #14 - RM-Meet Features (8h)

ONGOING:
□ Agent #15 - Design System (12h)
□ Agent #17 - Documentation (10h)
```

### 🎯 Priority Order

**Start IMMEDIATELY (Day 1):**
- Agent #1 (Gate) - CRITICAL, blocks others
- Agent #2 (Snitch) - CRITICAL, blocks integrations
- Agent #3 (Theatre) - HIGH priority
- Agent #16 (CI/CD) - HIGH priority

**Start Week 2 (after Gate completes):**
- Agents #4, #5, #6, #7 (Business apps)

**Start Week 4 (after foundations stable):**
- Agents #8, #9, #10, #11 (New apps)

**Start Week 6 (polish phase):**
- Agents #12, #13, #14 (Enhancements)

**Start Anytime (ongoing):**
- Agent #15 (Design)
- Agent #17 (Docs)

---

## 🚀 READY TO LAUNCH!

**You now have 17 complete, ready-to-use AI agent prompts!**

Each prompt includes:
✓ Full context and mission
✓ Specific tasks with file paths
✓ Technical requirements
✓ Validation criteria
✓ Completion report format

**Total estimated time:** 282 hours
**With parallel execution:** 7-8 weeks
**Value created:** $506,940 in savings over 5 years

---

**Questions?**
- Need clarification on any agent assignment?
- Want to adjust priorities or timelines?
- Ready to share agent outputs for review?

**I'm here to help! Let's ship this ecosystem! 🚀**

