# 🚀 QUICK REFERENCE: AI Agent Assignment Guide

## 📋 TL;DR - What Each Agent Should Do

### CRITICAL PATH (Start These First)
| Agent | App | Main Goal | Hours | Start When |
|-------|-----|-----------|-------|------------|
| #1 | RM-Gate | Add session mgmt, rate limits, audit logs | 8h | Day 1 |
| #2 | RM-Snitch | Build event bus with PostgreSQL persistence | 12h | Day 1 |
| #3 | AgentTheatre | Add LLM fallback, safety controls, marketplace | 10h | Day 1 |
| #16 | CI/CD Setup | Configure GitHub Actions for all apps | 16h | Day 1 |

### BUSINESS APPS (Week 2-3)
| Agent | App | Main Goal | Hours | Dependencies |
|-------|-----|-----------|-------|--------------|
| #4 | RM-FitterMe | Build AI workout/meal generator + frontend | 20h | Gate ready |
| #5 | RM-Planet | Complete CRM pipeline, contacts, email integration | 16h | Gate ready |
| #6 | RM-Learn | Build markdown editor, search, version control | 14h | Gate ready |
| #7 | RM-Mail | Polish inbox UI, add spam filter, PWA support | 8h | Gate ready |

### NEW APPS (Week 4-5)
| Agent | App | Main Goal | Hours | Dependencies |
|-------|-----|-----------|-------|--------------|
| #8 | RM-Calendar | Build from scratch: events, views, integrations | 24h | Gate, Snitch ready |
| #9 | RM-Capital-Hub | Build asset management + subscription tracking | 28h | Gate ready |
| #10 | RM-Secure | Build security platform with microservices | 32h | Gate ready |
| #11 | RM-Main | Build marketing site + app launcher | 16h | All apps exist |

### POLISH (Week 6-7)
| Agent | App | Main Goal | Hours | Dependencies |
|-------|-----|-----------|-------|--------------|
| #12 | RM-Atlas | Add time tracking, dependencies, roadmap view | 12h | After basic apps done |
| #13 | RM-Connect | Migrate to PostgreSQL, add AI features | 10h | After Snitch done |
| #14 | RM-Meet | Add breakout rooms, transcription, insights | 8h | After basic apps done |
| #15 | Design System | Ensure UI consistency across all apps | 12h | Ongoing |
| #17 | Documentation | Write READMEs, guides, API docs | 10h | Ongoing |

### QUALITY (Week 7-8)
| Agent | Focus | Main Goal | Hours | Dependencies |
|-------|-------|-----------|-------|--------------|
| #16 | Testing | Write unit, integration, E2E tests for all | 16h | Per app completion |

---

## 🎯 AGENT COORDINATION MATRIX

### Week 1-2: Foundation
```
Day 1-2:  Agent #1 (Gate) + Agent #2 (Snitch) + Agent #3 (Theatre) + Agent #16 (CI/CD)
Day 3-4:  Agent #1 completes → Start #4, #5, #6, #7
Day 5-7:  Agents #4-7 working in parallel
```

### Week 3-4: Business Apps Complete
```
Day 8-10:  Finish #4 (FitterMe), #5 (Planet), #6 (Learn), #7 (Mail)
Day 11-14: Start #8 (Calendar), #9 (Capital-Hub), #10 (Secure), #11 (Main)
```

### Week 5-6: New Apps + Polish
```
Day 15-21: Finish #8-11 (new apps)
Day 22-28: Start #12-14 (polish existing apps)
```

### Week 7-8: Testing & Launch
```
Day 29-35: Agent #16 (testing), #17 (documentation), #15 (design system)
Day 36-42: Production deployment, load testing, security audits
```

---

## 💬 SAMPLE AGENT COMMANDS (Copy & Paste)

### For Agent #1 (Gate Hardening):
```
You are AI Agent #1 working on RM-Gate authentication hardening.

Your mission:
1. Add Redis-backed session management with org_id scoping
2. Implement rate limiting (100 req/min per org)
3. Add comprehensive audit logging to PostgreSQL
4. Implement token rotation and revocation
5. Write production deployment documentation

Key files to modify:
- RM-Gate/authx/app/core/session.py (new file)
- RM-Gate/authx/app/middleware/rate_limit.py (new file)
- RM-Gate/authx/app/services/audit_logger.py (new file)
- RM-Gate/authx/app/services/token_manager.py (enhance existing)
- RM-Gate/PRODUCTION_DEPLOYMENT.md (new file)

Validation criteria:
- Tests pass with >85% coverage
- Load test: 10,000 auth requests in 60 seconds
- Zero security vulnerabilities
- Documentation complete

When complete, report:
"COMPLETED: RM-Gate - Authentication Hardening
Time: X hours
Coverage: Y%
Performance: 10K req/60s = PASS/FAIL
Next: Standing by for next assignment"
```

### For Agent #4 (FitterMe Full Build):
```
You are AI Agent #4 working on RM-FitterMe completion.

Your mission:
1. Replace hardcoded workouts with GPT-4 AI generator
2. Replace hardcoded meals with AI meal planner
3. Build complete frontend dashboard
4. Build workout tracking UI
5. Build nutrition tracking UI
6. Connect all AI endpoints to frontend

Context:
- Backend is 90% done (API structure exists)
- Frontend is only 20% done (needs major work)
- Must integrate GPT-4 for personalization
- Target: Personal trainer experience

Key files to create/modify:
- RM-FitterMe/backend/app/services/workout_ai.py (replace mock)
- RM-FitterMe/backend/app/services/nutrition_ai.py (replace mock)
- RM-FitterMe/frontend/src/pages/Dashboard.tsx (build)
- RM-FitterMe/frontend/src/pages/WorkoutTracker.tsx (build)
- RM-FitterMe/frontend/src/pages/NutritionTracker.tsx (build)

Validation:
- Generate personalized workout in <10s
- Meal plans have real recipes
- Frontend loads in <3s
- All CRUD operations work

Dependencies:
- Wait for Agent #1 (Gate) to complete
- Use RM-Gate for authentication
```

### For Agent #8 (Calendar from Scratch):
```
You are AI Agent #8 building RM-Calendar from scratch.

Your mission:
Build a complete calendar/scheduling app with:
1. Events API (CRUD, recurring events, reminders)
2. Calendar views (month, week, day, agenda, year)
3. Event creation UI (quick add + detailed form)
4. Scheduling AI (find available time slots)
5. Integrations (Meet, Connect, Atlas, Mail)
6. Mobile-responsive UI

This is a greenfield project - you're building it from the ground up.

Tech stack:
- Backend: Python/FastAPI (follow RM-Atlas pattern)
- Frontend: React + TypeScript (follow RM-Connect pattern)
- Database: PostgreSQL
- Real-time: WebSockets via RM-Snitch

Study these apps first:
- RM-Atlas (backend structure)
- RM-Connect (frontend structure)
- RM-Gate (authentication integration)

Key deliverables:
- Full CRUD API for events
- 5 calendar view components
- Time zone support
- RM-Meet integration (auto-add video links)

Validation:
- Handle 10,000 events without lag
- Recurring events work perfectly
- Time zone conversion accurate
- Video call integration seamless

Dependencies:
- Wait for Agent #1 (Gate) and #2 (Snitch) to complete
- Study existing app patterns first
```

---

## 🔍 HOW TO DETERMINE WHAT TO BUILD

### Step 1: Examine Existing Code
```bash
# Look at what exists
ls -la RM-[AppName]/
cat RM-[AppName]/README.md
find RM-[AppName] -name "*.py" -o -name "*.tsx" | head -20

# Check current implementation level
wc -l RM-[AppName]/backend/app/**/*.py
wc -l RM-[AppName]/frontend/src/**/*.tsx
```

### Step 2: Identify Gaps
- Compare with similar apps (if RM-Atlas has X, does RM-Planet have it?)
- Check TODOs in code: `grep -r "TODO" RM-[AppName]/`
- Review PRD/documentation: `cat RM-[AppName]/docs/PRD.md`

### Step 3: Prioritize Features
1. **Critical:** Authentication, core CRUD, basic UI
2. **Important:** Advanced features, integrations
3. **Nice-to-have:** Polish, animations, extras

### Step 4: Build Incrementally
- Day 1: Backend API (database models, routes, basic logic)
- Day 2: Frontend structure (pages, components, routing)
- Day 3: Connect frontend to backend (API calls, state management)
- Day 4: Integrations (Gate auth, Snitch events)
- Day 5: Testing and polish

---

## ✅ COMPLETION CHECKLIST (Per App)

Use this checklist before marking an app as "complete":

```markdown
### RM-[AppName] Completion Checklist

#### Backend
- [ ] Database models defined (Alembic migrations created)
- [ ] All CRUD endpoints implemented
- [ ] Authentication integrated (RM-Gate OAuth)
- [ ] Event emission configured (RM-Snitch integration)
- [ ] Error handling and logging
- [ ] API documentation (OpenAPI/Swagger)

#### Frontend
- [ ] All pages created and routed
- [ ] API integration complete (all endpoints called)
- [ ] State management working (Redux/Zustand/Context)
- [ ] Loading states and error handling
- [ ] Dark mode implemented
- [ ] Mobile responsive

#### Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests (API endpoints)
- [ ] E2E tests (critical user flows)
- [ ] Load testing (1000 concurrent users)

#### Documentation
- [ ] README.md complete
- [ ] Quick start guide
- [ ] Architecture diagram
- [ ] Environment variables documented

#### Production Ready
- [ ] .env.example created
- [ ] Docker/docker-compose setup
- [ ] SSL/TLS ready
- [ ] Monitoring configured
- [ ] Backup procedures documented
```

---

## 📞 COMMUNICATION TEMPLATES

### Daily Update (Send to CTO)
```
Daily Update - [Date]
Agent: #[X] - [App Name]

✅ Completed:
- [Task 1]
- [Task 2]

🔄 In Progress:
- [Task 3] (60% done, ETA: 4h)

⏭️ Next:
- [Task 4]
- [Task 5]

🚧 Blockers:
- [None / Describe blocker]

⏱️ Time Spent: Xh
💯 Overall Progress: X%
```

### Blocker Report
```
🚨 BLOCKER ALERT

Agent: #[X] - [App Name]
Task: [Task Name]
Issue: [Detailed description]

What I tried:
1. [Attempt 1]
2. [Attempt 2]

What I need:
- [Specific help needed]

Urgency: [High/Medium/Low]
Impact: [Can't proceed / Slowed down / Can work around]
```

### Completion Report
```
🎉 APP COMPLETE: RM-[AppName]

Agent: #[X]
Status: Production-Ready ✅
Time Taken: Xh (estimated Yh)

Metrics:
- Test Coverage: X%
- API Response: Xms (p95)
- Page Load: Xs
- Lines of Code: X

Highlights:
- [Cool feature 1]
- [Cool feature 2]

Known Limitations:
- [Any deferred items]

Handoff Notes:
- [Important info for next developer]

Ready for: Testing / Staging Deployment / Production
```

---

## 🎯 SUCCESS TIPS

### For All Agents:

1. **Start with Tests**: Write tests first (TDD), then implement
2. **Follow Patterns**: Look at existing apps, copy good patterns
3. **Ask Questions**: Better to clarify than build wrong thing
4. **Document as You Go**: Don't wait until the end
5. **Test Early, Test Often**: Don't accumulate untested code
6. **Use Git**: Commit frequently with clear messages
7. **Think About Users**: Build features people will actually use
8. **Optimize Later**: Get it working first, then make it fast
9. **Celebrate Wins**: Mark tasks complete, feel good about progress
10. **Help Others**: Share solutions, answer questions

### Red Flags to Watch For:

🚩 Test coverage dropping below 70%
🚩 API response times >1 second
🚩 Console errors in browser
🚩 Hardcoded values (use environment variables)
🚩 SQL injection vulnerabilities (use parameterized queries)
🚩 Missing error handling (try/catch everywhere)
🚩 No loading states (users see blank screens)
🚩 Broken on mobile (test responsive design)
🚩 Memory leaks (clean up listeners/timers)
🚩 Inconsistent UI (use design system)

---

## 📚 REFERENCE LINKS

### Internal Documentation:
- Main directive: `tmp_rovodev_AI_AGENT_COMMANDS_CTO.md`
- Developer handoff: `DEVELOPER_HANDOFF_INSTRUCTIONS.md`
- Integration guide: `INTEGRATION_TEST_GUIDE.md`
- Competitive analysis: `RM_ORBIT_COMPETITIVE_STRATEGY.md`

### Tech Stack Docs:
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

### Testing:
- Pytest: https://docs.pytest.org/
- Jest: https://jestjs.io/
- Playwright: https://playwright.dev/
- Locust (load testing): https://locust.io/

---

**Good luck, agents! Let's ship this ecosystem. 🚀**

