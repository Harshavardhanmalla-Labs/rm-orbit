# 14 — FitterMe (Health & Wellness) — Comprehensive Checklist

> **App:** RM FitterMe — Health & Wellness Tracker
> **Stack:** Vanilla HTML/JS frontend (`FitterMe/backend/app/ui/index.html`, 1081 lines) served from Python/FastAPI backend
> **Design system:** orbit-tokens.css loaded, plus custom CSS variables (`--bg`, `--brand`, etc.)
> **Backend models:** Account, User, WorkoutLog, MealLog, Habit, HealthMetric, CoachFeedback, AnalyticsEvent, AuditEvent, ConsentRecord, PrivacyExportJob, RefreshToken, EmailVerificationToken, PasswordResetToken, LoginChallengeToken, EmailSuppression, EmailWebhookEventReceipt
> **Backend services:** AI Coach, AI Meal Planner, Analytics, Audit, Coach Calibration, Email Delivery, Email Suppression, Food Database, Metrics, Planner, Privacy, Scoring
> **Backend routes:** Auth routes, API v1 routes (workouts, meals, habits, health metrics, coach, analytics), AI routes, Food routes, Social routes
> **Auth:** Full auth system (registration, login, JWT + refresh tokens, email verification, password reset, login challenges, account lockout)
> **Status:** Most mature of the three — full backend with auth, AI services, monitoring stack (Prometheus, Grafana, Alertmanager)
> **Last synced with PER_APP_CHECKLIST.md:** 2026-04-06
>
> Legend: `[x]` = done · `[ ]` = todo · `[~]` = in progress · `[-]` = N/A / skipped

---

## 1. Project Setup & Configuration

### 1.1 Current Vanilla HTML/JS Setup
- [x] `FitterMe/backend/app/ui/index.html` — single-file SPA (1081 lines, served by backend)
- [x] `orbit-tokens.css` loaded in `<head>` via `/orbit-ui/orbit-tokens.css`
- [x] Dark mode bootstrap script in `<head>`
- [x] Custom CSS variables in `:root` (--bg, --bg-soft, --panel, --brand, --brand-2, etc.)
- [x] Custom font loading: Space Grotesk (headings) + IBM Plex Sans (body) via CDN
- [x] Background grid pattern (`.backgrid`)
- [x] Gradient background with brand colors
- [ ] Add `manifest.json` for PWA support
- [ ] Add `favicon.ico` and app icons (16, 32, 192, 512)
- [ ] Add Open Graph / social sharing meta tags
- [ ] Add `robots.txt`
- [ ] Add `apple-touch-icon.png`
- [ ] Add service worker for offline support / workout caching

### 1.2 Backend Setup
- [x] `FitterMe/backend/app/main.py` — FastAPI app with middleware stack
- [x] `FitterMe/backend/app/api/routes.py` — v1 API routes (comprehensive)
- [x] `FitterMe/backend/app/api/auth_routes.py` — authentication routes
- [x] `FitterMe/backend/app/api/ai_routes.py` — AI coach routes
- [x] `FitterMe/backend/app/api/food_routes.py` — food database routes
- [x] `FitterMe/backend/app/api/social_routes.py` — social/team routes
- [x] `FitterMe/backend/app/api/deps.py` — dependency injection (auth, profile)
- [x] `FitterMe/backend/app/core/config.py` — settings with validation
- [x] `FitterMe/backend/app/core/security.py` — JWT, password hashing
- [x] `FitterMe/backend/app/core/request_utils.py` — request utilities
- [x] `FitterMe/backend/app/db/session.py` — database session
- [x] `FitterMe/backend/app/db/init_db.py` — database initialization
- [x] `FitterMe/backend/app/models/entities.py` — 17 SQLAlchemy models
- [x] `FitterMe/backend/app/schemas/domain.py` — Pydantic schemas
- [x] `FitterMe/backend/app/services/ai_coach.py` — AI coach recommendations
- [x] `FitterMe/backend/app/services/ai_meal_planner.py` — AI meal planning
- [x] `FitterMe/backend/app/services/analytics.py` — analytics service
- [x] `FitterMe/backend/app/services/audit.py` — audit logging
- [x] `FitterMe/backend/app/services/coach_calibration.py` — coach model calibration
- [x] `FitterMe/backend/app/services/email_delivery.py` — email sending
- [x] `FitterMe/backend/app/services/email_suppression.py` — email bounce/complaint handling
- [x] `FitterMe/backend/app/services/email_webhook_security.py` — webhook signature validation
- [x] `FitterMe/backend/app/services/food_database.py` — food/nutrition lookup
- [x] `FitterMe/backend/app/services/metrics.py` — Prometheus metrics
- [x] `FitterMe/backend/app/services/planner.py` — workout/meal planner
- [x] `FitterMe/backend/app/services/privacy.py` — GDPR privacy service
- [x] `FitterMe/backend/app/services/scoring.py` — health scoring
- [x] `FitterMe/backend/app/workers/privacy_export_worker.py` — background export worker
- [x] `FitterMe/schema.sql` — PostgreSQL schema (200+ lines)
- [x] `FitterMe/backend/alembic/` — 18+ migration files
- [ ] Add `pyproject.toml` for modern Python packaging
- [ ] Add `Makefile` or `justfile` for common commands
- [ ] Add `pre-commit` hooks configuration

### 1.3 Testing Infrastructure
- [x] `FitterMe/backend/tests/conftest.py` — test configuration
- [x] `FitterMe/backend/tests/test_security.py` — security tests
- [x] `FitterMe/backend/tests/test_admin_privacy_exports.py` — admin privacy export tests
- [x] `FitterMe/backend/tests/test_email_suppression.py` — email suppression tests
- [x] `FitterMe/backend/tests/test_request_utils.py` — request utility tests
- [x] `FitterMe/backend/tests/test_config_validation.py` — config validation tests
- [x] `FitterMe/backend/tests/test_coach_feedback.py` — coach feedback tests
- [x] `FitterMe/backend/tests/test_privacy.py` — privacy tests
- [x] `FitterMe/backend/tests/test_v1_pagination.py` — pagination tests
- [x] `FitterMe/backend/tests/test_services.py` — service tests
- [x] `FitterMe/backend/tests/test_legal_hold.py` — legal hold tests
- [x] `FitterMe/backend/tests/test_analytics.py` — analytics tests
- [x] `FitterMe/backend/tests/test_auth_flow.py` — auth flow tests
- [x] `FitterMe/backend/tests/test_runtime.py` — runtime tests
- [x] `FitterMe/backend/tests/test_wearable_sync.py` — wearable sync tests
- [x] `FitterMe/backend/tests/test_ai_coach.py` — AI coach tests
- [ ] Test coverage report generation
- [ ] Test coverage threshold enforcement (>= 80%)
- [ ] Frontend test infrastructure

### 1.4 DevOps & Monitoring Infrastructure
- [x] `FitterMe/Dockerfile` — container image
- [x] `FitterMe/docker-compose.yml` — full stack compose
- [x] `FitterMe/deploy-to-server.sh` — deployment script
- [x] `FitterMe/ecosystem.config.js` — PM2 configuration
- [x] `FitterMe/nginx.conf.example` — Nginx reverse proxy
- [x] `FitterMe/ops/prometheus/prometheus.yml` — Prometheus config
- [x] `FitterMe/ops/prometheus/alerts.yml` — Prometheus alert rules
- [x] `FitterMe/ops/grafana/dashboards/rmfit-overview.json` — Grafana dashboard
- [x] `FitterMe/ops/grafana/provisioning/datasources/prometheus.yml` — Grafana datasource
- [x] `FitterMe/ops/grafana/provisioning/dashboards/default.yml` — Grafana dashboard provisioning
- [x] `FitterMe/ops/alertmanager/alertmanager.yml` — Alertmanager config
- [x] `FitterMe/ops/cloudflare/custom_waf_rules.template.json` — WAF rules
- [x] `FitterMe/ops/cloudflare/rate_limits.template.json` — rate limit config
- [x] `FitterMe/ops/systemd/rmfit-canary.service` — canary systemd service
- [x] `FitterMe/ops/systemd/rmfit-canary.timer` — canary timer
- [x] `FitterMe/scripts/production_canary.sh` — canary check script
- [x] `FitterMe/scripts/secret_scan.sh` — secret scanning
- [x] `FitterMe/scripts/smoke_check.sh` — smoke test
- [x] `FitterMe/scripts/deploy_production.sh` — production deploy
- [x] `FitterMe/scripts/restore_postgres.sh` — DB restore
- [x] `FitterMe/scripts/backup_postgres.sh` — DB backup
- [x] `FitterMe/scripts/alertmanager_test.sh` — alert test
- [x] `FitterMe/scripts/install_canary_systemd.sh` — canary install
- [x] `FitterMe/scripts/observability_check.sh` — observability check
- [x] `FitterMe/scripts/e2e_smoke.sh` — E2E smoke test
- [x] `FitterMe/scripts/cloudflare_policy_lint.sh` — Cloudflare policy lint
- [ ] Docker health check in Dockerfile
- [ ] `.dockerignore` optimization
- [ ] Container image size optimization
- [ ] Auto-scaling configuration

### 1.5 Documentation
- [x] `FitterMe/README.md` — project readme
- [x] `FitterMe/QUICK_START.md` — quick start guide
- [x] `FitterMe/PRODUCTION_DEPLOYMENT.md` — production deployment
- [x] `FitterMe/COMPETITIVE_ANALYSIS.md` — competitive analysis
- [x] `FitterMe/docs/ARCHITECTURE.md` — architecture doc
- [x] `FitterMe/docs/SECURITY.md` — security documentation
- [x] `FitterMe/docs/PRODUCTION_READINESS_UIUX_GAP_PLAN.md` — UI/UX gap plan
- [x] `FitterMe/docs/PRD.md` — product requirements
- [x] `FitterMe/docs/MVP_BACKLOG.md` — MVP backlog
- [x] `FitterMe/docs/DEPLOYMENT.md` — deployment guide
- [x] `FitterMe/docs/EDGE_ABUSE_PROTECTION.md` — abuse protection
- [x] `FitterMe/docs/OPERATIONS.md` — operations guide
- [x] `FitterMe/docs/DB_MIGRATIONS.md` — migration guide
- [x] `FitterMe/docs/API.md` — API documentation

### 1.6 React Migration Decision Path
- [ ] **DECISION:** Migrate to React 19 + TypeScript or enhance vanilla JS?
- [ ] If React: Create `FitterMe/frontend/` Vite + React 19 + TypeScript project
- [ ] If React: `package.json` with `@orbit-ui/react`, Tailwind, React Router, Zustand, Recharts, Lucide React
- [ ] If React: `tailwind.config.js` with orbit preset
- [ ] If React: `vite.config.ts` with proxy to backend API
- [ ] If React: `tsconfig.json` with strict mode
- [ ] If React: `index.html` with anti-FOUC + orbit-ui links
- [ ] If React: `main.tsx` with `ThemeProvider` wrapper
- [ ] If React: Gate OAuth PKCE auth flow (replace current auth UI)
- [ ] If React: ESLint + Prettier configuration
- [ ] If React: Vitest + React Testing Library setup
- [ ] If React: Storybook for component development
- [ ] If vanilla: Modularize single-file SPA into ES modules
- [ ] If vanilla: Add build step (esbuild/Vite) for bundling
- [ ] If vanilla: Add TypeScript via JSDoc type annotations
- [ ] If vanilla: Add unit tests with Vitest or Jest (JSDOM)
- [ ] If vanilla: Extract CSS into separate files
- [ ] If vanilla: Add CSS minification pipeline
- [ ] Parallel operation: keep both UIs while migrating
- [ ] Feature flag to toggle between old/new UI
- [ ] Migration completion criteria document

---

## 2. Design System Integration

### 2.1 Token Usage Audit
- [x] `orbit-tokens.css` loaded in `<head>`
- [x] Dark mode bootstrap script in `<head>`
- [ ] **ISSUE:** Custom CSS variables override orbit tokens extensively
- [ ] Replace `--bg: #07151b` with `var(--orbit-bg)` token
- [ ] Replace `--bg-soft: #10252f` with `var(--orbit-bg-soft)` token
- [ ] Replace `--panel: rgba(11, 33, 43, 0.88)` with `var(--orbit-surface)` token
- [ ] Replace `--panel-solid: #0b212b` with `var(--orbit-surface-solid)` token
- [ ] Replace `--panel-soft: #153543` with `var(--orbit-surface-soft)` token
- [ ] Replace `--card: #f3f6f4` with `var(--orbit-card)` token
- [ ] Replace `--ink: #0f2029` with `var(--orbit-text)` token
- [ ] Replace `--ink-soft: #5f6e76` with `var(--orbit-text-muted)` token
- [ ] Replace `--line: rgba(9, 29, 38, 0.16)` with `var(--orbit-border)` token
- [ ] Replace `--line-dark: rgba(195, 226, 231, 0.24)` with `var(--orbit-border-dark)` token
- [ ] Replace `--brand: #17ba90` with `var(--orbit-primary)` token
- [ ] Replace `--brand-2: #159bc8` with `var(--orbit-secondary)` token
- [ ] Replace `--focus: rgba(21, 155, 200, 0.34)` with `var(--orbit-focus)` token
- [ ] Replace `--warn: #ff7b5f` with `var(--orbit-warning)` token
- [ ] Replace `--ok: #5be293` with `var(--orbit-success)` token
- [ ] Replace `--amber: #ffbd59` with `var(--orbit-amber)` token
- [ ] Replace `--text-on-dark: #d8ebef` with `var(--orbit-text-on-dark)` token
- [ ] Replace `--text-dim: #8ea8b0` with `var(--orbit-text-dim)` token
- [ ] Remove all hardcoded hex colors from inline `<style>`
- [ ] Audit every `background`, `color`, `border-color` for hardcoded values

### 2.2 Typography Tokens
- [ ] **ISSUE:** Uses Space Grotesk + IBM Plex Sans instead of RM Forma
- [ ] Decide: keep custom fonts for FitterMe branding or align to orbit RM Forma
- [ ] If aligning: Replace Space Grotesk with RM Forma for headings
- [ ] If aligning: Replace IBM Plex Sans with RM Forma for body
- [ ] If keeping: Document font exception in design system guide
- [ ] Replace hardcoded font sizes with orbit tokens
- [ ] Replace hardcoded font weights with orbit tokens
- [ ] Replace hardcoded line heights with orbit tokens
- [ ] Replace hardcoded letter spacing with orbit tokens

### 2.3 Spacing & Layout Tokens
- [ ] Replace hardcoded padding values with orbit spacing tokens
- [ ] Replace hardcoded gap values with orbit spacing tokens
- [ ] Replace hardcoded margin values with orbit spacing tokens
- [ ] Replace hardcoded border-radius values with orbit radius tokens
- [ ] Replace hardcoded widths/heights with orbit sizing tokens

### 2.4 Shadow & Effect Tokens
- [ ] Replace hardcoded box-shadow values with orbit shadow tokens
- [ ] Replace backdrop-filter values with orbit glass tokens
- [ ] Replace hardcoded focus ring styles with orbit focus tokens

### 2.5 Motion & Animation Tokens
- [ ] Add orbit transition tokens for page transitions
- [ ] Add orbit transition tokens for modal open/close
- [ ] Add orbit transition tokens for workout timer animations
- [ ] Add orbit transition tokens for progress ring animations
- [ ] Add orbit transition tokens for chart animations
- [ ] Add orbit transition tokens for streak celebration animations
- [ ] Add orbit transition tokens for loading states

### 2.6 Component Replacements (orbit-ui equivalents)
- [ ] Replace custom button styles with orbit Button component
- [ ] Replace custom input styles with orbit Input component
- [ ] Replace custom select styles with orbit Select component
- [ ] Replace custom card styles with orbit Card component
- [ ] Replace custom table styles with orbit Table component
- [ ] Replace custom modal styles with orbit Modal/Dialog component
- [ ] Replace custom tooltip styles with orbit Tooltip component
- [ ] Replace custom badge/pill styles with orbit Badge component
- [ ] Replace custom progress bar with orbit ProgressBar component
- [ ] Replace custom progress ring with orbit ProgressRing component
- [ ] Replace custom tabs with orbit Tabs component
- [ ] Replace custom toast with orbit Toast component
- [ ] Replace custom form layouts with orbit Form components
- [ ] Replace custom navigation with orbit NavItem components
- [ ] Replace custom avatar with orbit Avatar component
- [ ] Replace custom stat cards with orbit StatCard component
- [ ] Replace custom toggle/switch with orbit Switch component
- [ ] Replace custom slider with orbit Slider component
- [ ] Replace custom date picker with orbit DatePicker component
- [ ] Replace custom number stepper with orbit NumberInput component

### 2.7 orbit-bar Integration
- [ ] **ISSUE:** orbit-bar.js is NOT loaded in FitterMe (uses orbit-tokens.css only)
- [ ] Add orbit-bar.js to FitterMe UI
- [ ] Configure orbit-bar to show FitterMe as active app
- [ ] Verify orbit-bar theme toggle integration
- [ ] Verify orbit-bar app switcher works
- [ ] Verify orbit-bar notifications integration
- [ ] Verify orbit-bar user menu integration

---

## 3. Dark Mode

### 3.1 Theme Infrastructure
- [x] Dark mode bootstrap script in `<head>` (checks localStorage + system preference)
- [x] `.dark` class toggled on `<html>` element
- [ ] Verify `orbit-tokens.css` provides both light and dark token values
- [ ] Add theme toggle button in FitterMe UI
- [ ] Persist theme preference to user profile (backend)
- [ ] Sync theme preference across tabs (BroadcastChannel)
- [ ] Respect `prefers-color-scheme` media query
- [ ] Add transition animation when switching themes
- [ ] Prevent FOUC on page load

### 3.2 Page/View Dark Mode Verification
- [ ] Login/Registration page — dark mode colors
- [ ] Email verification page — dark mode colors
- [ ] Password reset page — dark mode colors
- [ ] Dashboard / Daily OS view — dark mode colors
- [ ] Workout logging view — dark mode colors
- [ ] Workout history view — dark mode colors
- [ ] Workout plan view — dark mode colors
- [ ] Exercise library view — dark mode colors
- [ ] Meal tracking view — dark mode colors
- [ ] Meal logging form — dark mode colors
- [ ] Nutrition analysis view — dark mode colors
- [ ] Meal plan view — dark mode colors
- [ ] Food search view — dark mode colors
- [ ] Habit tracking view — dark mode colors
- [ ] Health metrics view (steps, heart rate, sleep, HRV) — dark mode colors
- [ ] Body measurements view — dark mode colors
- [ ] Progress charts view — dark mode colors
- [ ] Fitness goals view — dark mode colors
- [ ] Goal detail view — dark mode colors
- [ ] Streaks/achievements view — dark mode colors
- [ ] Health insights view — dark mode colors
- [ ] AI coach view — dark mode colors
- [ ] AI recommendations panel — dark mode colors
- [ ] Wearable integration settings — dark mode colors
- [ ] Team wellness challenges view — dark mode colors
- [ ] Social/team feed view — dark mode colors
- [ ] Admin dashboard — dark mode colors
- [ ] Privacy settings view — dark mode colors
- [ ] Consent management view — dark mode colors
- [ ] Account settings view — dark mode colors
- [ ] Profile settings view — dark mode colors
- [ ] Notification settings view — dark mode colors

### 3.3 Component Dark Mode Verification
- [ ] Buttons (primary, secondary, ghost, danger) — dark mode
- [ ] Input fields — dark mode backgrounds, borders, placeholder text
- [ ] Select dropdowns — dark mode
- [ ] Number inputs (weight, reps, sets) — dark mode
- [ ] Slider inputs — dark mode
- [ ] Toggle switches — dark mode
- [ ] Date pickers — dark mode
- [ ] Time pickers — dark mode
- [ ] Tables — dark mode headers, rows, alternate colors
- [ ] Stat cards (steps, calories, sleep, heart rate) — dark mode
- [ ] Progress rings (daily goals) — dark mode
- [ ] Progress bars — dark mode
- [ ] Navigation items — dark mode active/hover/inactive
- [ ] Modals/dialogs — dark mode overlay, background, text
- [ ] Tooltips — dark mode
- [ ] Badges (achievements, streaks) — dark mode
- [ ] Dropdown menus — dark mode
- [ ] Tabs — dark mode active/inactive
- [ ] Toast notifications — dark mode
- [ ] Cards — dark mode
- [ ] Charts (line, bar, area, pie) — dark mode colors and gridlines
- [ ] Calendar heatmap — dark mode
- [ ] Workout timer — dark mode
- [ ] Food search results — dark mode
- [ ] Nutrition macro bars — dark mode
- [ ] Loading spinners — dark mode
- [ ] Empty states — dark mode
- [ ] Error states — dark mode
- [ ] Skeleton loaders — dark mode
- [ ] Scrollbar styling — dark mode
- [ ] Avatar/profile picture — dark mode border
- [ ] Coach recommendation cards — dark mode
- [ ] Achievement badges — dark mode
- [ ] Streak counter — dark mode
- [ ] Water intake tracker — dark mode
- [ ] Heart rate display — dark mode
- [ ] Sleep score display — dark mode
- [ ] HRV display — dark mode

### 3.4 Light Mode Verification
- [ ] **ISSUE:** Current CSS appears dark-mode-first with custom dark variables
- [ ] Add light mode CSS variables
- [ ] All views listed in 3.2 — light mode verification
- [ ] All components listed in 3.3 — light mode verification
- [ ] Gradient backgrounds adapt to light mode
- [ ] Grid background pattern adapts to light mode
- [ ] Charts readable in light mode
- [ ] Health data colors (green/red/amber) work in light mode
- [ ] Background grid (`.backgrid`) adapts to light mode

---

## 4. Core Features (Exhaustive)

### 4.1 Authentication & Account Management
- [x] User registration (email + password)
- [x] User login (JWT access token + refresh token)
- [x] Refresh token rotation with family tracking
- [x] Email verification flow
- [x] Password reset flow (token-based)
- [x] Login challenge tokens (email OTP for suspicious logins)
- [x] Account lockout after failed attempts
- [x] Device fingerprint tracking on refresh tokens
- [x] Risk scoring on auth events
- [x] Session management (refresh token tracking)
- [x] Audit events for all auth actions
- [ ] Login UI form
- [ ] Registration UI form
- [ ] Email verification UI
- [ ] Password reset UI
- [ ] Login challenge UI (enter OTP code)
- [ ] Forgot password UI
- [ ] Account settings UI (change password, email)
- [ ] Session list UI (view/revoke sessions)
- [ ] Account deletion UI
- [ ] Social login (Google, Apple) — optional
- [ ] Biometric login (FaceID/TouchID) — mobile
- [ ] Remember me checkbox
- [ ] Terms of service acceptance

### 4.2 User Profile
- [x] User model: name, age, height_cm, weight_kg, goal, diet_type
- [x] Profile creation endpoint
- [x] Profile linked to Account (1:1)
- [ ] Profile setup wizard (onboarding)
- [ ] Profile edit form
- [ ] Profile photo upload
- [ ] Profile goal selection UI (weight loss, muscle gain, endurance, flexibility, general health)
- [ ] Profile diet type selection UI (balanced, keto, vegan, vegetarian, paleo, etc.)
- [ ] Profile activity level setting (sedentary, light, moderate, active, very active)
- [ ] Profile unit preference (metric/imperial)
- [ ] Profile privacy settings
- [ ] Profile data export (GDPR)
- [ ] Profile data deletion (GDPR)
- [ ] BMI calculation from height/weight
- [ ] BMR/TDEE calculation
- [ ] Target calorie calculation based on goal

### 4.3 Daily Health Tracking — Dashboard
- [x] Dashboard API endpoint (DashboardResponse schema)
- [ ] Dashboard UI layout
- [ ] Steps counter card with daily goal ring
- [ ] Calories consumed vs target card
- [ ] Water intake tracker (glasses/ml)
- [ ] Sleep duration and quality card
- [ ] Heart rate display (resting HR)
- [ ] HRV (heart rate variability) display
- [ ] Active minutes card
- [ ] Daily wellness score (composite)
- [ ] Daily greeting with motivational message
- [ ] Today's workout schedule
- [ ] Today's meal plan summary
- [ ] Habit checklist for the day
- [ ] Streak counter display
- [ ] Weekly progress mini-chart
- [ ] Quick-add buttons (workout, meal, water, weight)
- [ ] Date navigation (previous/next day)
- [ ] Auto-refresh for live wearable data

### 4.4 Workout Logging
- [x] WorkoutLog model: exercise_name, muscle_group, sets, reps, weight_kg, duration_min, completed
- [x] Workout log create endpoint
- [x] Workout log list endpoint (with pagination)
- [ ] Workout logging UI form
- [ ] Exercise name autocomplete from library
- [ ] Muscle group selector (chest, back, shoulders, arms, legs, core, cardio, full body)
- [ ] Sets/reps/weight input (stepper controls)
- [ ] Duration input (timer or manual)
- [ ] Workout timer with start/pause/stop
- [ ] Rest timer between sets (configurable)
- [ ] Workout complete toggle per exercise
- [ ] Add multiple exercises per workout session
- [ ] Workout session grouping (all exercises in one session)
- [ ] Workout template selection (use saved workout plan)
- [ ] Previous workout auto-fill (last time you did this exercise)
- [ ] Progressive overload suggestion (slightly more than last time)
- [ ] Quick-log mode (minimal fields)
- [ ] Detailed-log mode (all fields)
- [ ] Workout notes per exercise
- [ ] Workout RPE (Rate of Perceived Exertion) logging
- [ ] Workout mood rating
- [ ] Superset/circuit logging support
- [ ] Cardio workout logging (distance, time, pace, heart rate zones)
- [ ] Flexibility/mobility workout logging (stretch name, hold time)
- [ ] Workout photo (progress pic with workout)

### 4.5 Workout History
- [ ] Workout history list view
- [ ] Workout history calendar heatmap
- [ ] Workout history filter by date range
- [ ] Workout history filter by muscle group
- [ ] Workout history filter by exercise
- [ ] Workout detail view (all exercises in session)
- [ ] Workout edit (modify past workout)
- [ ] Workout delete with confirmation
- [ ] Workout volume chart (total weight lifted over time)
- [ ] Workout frequency chart (sessions per week)
- [ ] Personal records (PR) tracking per exercise
- [ ] PR celebration animation/badge
- [ ] Workout streak tracking
- [ ] Workout consistency score

### 4.6 Workout Plans
- [x] Workout plan generation (AI planner service)
- [x] WorkoutPlanRequest / WorkoutPlanResponse schemas
- [ ] Workout plan list view
- [ ] Workout plan create form (manual)
- [ ] Workout plan AI-generated (based on goals + history)
- [ ] Workout plan: name, description, duration (weeks), frequency (days/week)
- [ ] Workout plan day-by-day schedule
- [ ] Workout plan exercise list per day
- [ ] Workout plan progression (week over week)
- [ ] Workout plan active plan selection
- [ ] Workout plan start/stop tracking
- [ ] Workout plan progress (completed sessions / total)
- [ ] Workout plan sharing with team
- [ ] Workout plan templates (beginner, intermediate, advanced)
- [ ] Workout plan print/export

### 4.7 Exercise Library
- [ ] Exercise list view with search
- [ ] Exercise filter by muscle group
- [ ] Exercise filter by equipment (barbell, dumbbell, machine, bodyweight, bands, cable)
- [ ] Exercise filter by type (strength, cardio, flexibility, plyometric)
- [ ] Exercise detail view
- [ ] Exercise name and description
- [ ] Exercise muscle groups (primary, secondary)
- [ ] Exercise instructions (step-by-step)
- [ ] Exercise tips / form cues
- [ ] Exercise image/animation
- [ ] Exercise video link
- [ ] Exercise difficulty level (beginner, intermediate, advanced)
- [ ] Exercise equipment required
- [ ] Custom exercise creation
- [ ] Exercise favorites/bookmarks
- [ ] Exercise history (when you last did it, best weight/reps)

### 4.8 Meal Tracking
- [x] MealLog model: meal_name, calories, protein_g, carbs_g, fat_g
- [x] Meal log create endpoint
- [x] Meal log list endpoint
- [ ] Meal logging UI form
- [ ] Meal type selector: breakfast, lunch, dinner, snack, pre-workout, post-workout
- [ ] Food search (from food database service)
- [ ] Food search results display (name, calories, macros per serving)
- [ ] Serving size selector (grams, oz, cups, tablespoons, pieces)
- [ ] Multiple food items per meal
- [ ] Meal total calculation (sum of all items)
- [ ] Quick-add recent meals
- [ ] Favorite meals save/load
- [ ] Meal copy from previous day
- [ ] Barcode scanner for packaged food
- [ ] Meal photo (food picture)
- [ ] AI meal recognition from photo (future)
- [ ] Custom food creation (manual entry)
- [ ] Meal notes

### 4.9 Nutrition Analysis
- [x] Macro tracking: protein_g, carbs_g, fat_g, calories
- [ ] Daily macro progress bars
- [ ] Daily calorie progress ring
- [ ] Macro ratio pie chart (protein/carbs/fat %)
- [ ] Weekly nutrition summary
- [ ] Calorie trend chart (daily over time)
- [ ] Macro trend chart (daily over time)
- [ ] Micronutrient tracking (vitamins, minerals) — future
- [ ] Fiber intake tracking
- [ ] Sugar intake tracking
- [ ] Sodium intake tracking
- [ ] Water intake tracking
- [ ] Nutrition score (how well you hit targets)
- [ ] Calorie deficit/surplus indicator
- [ ] Protein target based on body weight
- [ ] Meal timing analysis (eating window)

### 4.10 AI Meal Planner
- [x] AI meal planner service (ai_meal_planner.py)
- [x] NutritionPlanRequest / NutritionPlanResponse schemas
- [ ] Meal plan generation UI
- [ ] Meal plan based on goals, diet type, calorie target
- [ ] Meal plan weekly view (7 days x meals)
- [ ] Meal plan daily view (all meals for today)
- [ ] Meal plan swap individual meals
- [ ] Meal plan regenerate single day
- [ ] Meal plan grocery list generation
- [ ] Meal plan dietary restriction support (allergies, intolerances)
- [ ] Meal plan cuisine preference
- [ ] Meal plan cooking time preference
- [ ] Meal plan budget consideration
- [ ] Meal plan print/export

### 4.11 Food Database
- [x] Food database service (food_database.py)
- [x] Food search routes (food_routes.py)
- [ ] Food search UI with real-time results
- [ ] Food search by name
- [ ] Food nutritional info display (per 100g and per serving)
- [ ] Food categories browsing
- [ ] Food common serving sizes
- [ ] USDA database integration
- [ ] Open Food Facts integration
- [ ] Custom food database entries
- [ ] Food brand search
- [ ] Food barcode lookup

### 4.12 Habit Tracking
- [x] Habit model: habit_type, status, target_value, date
- [x] Habit create endpoint
- [x] Habit list endpoint
- [ ] Habit list UI (today's habits)
- [ ] Habit check/uncheck toggle
- [ ] Habit types: water intake, vitamins, meditation, stretching, steps goal, sleep target, no sugar, no alcohol, journaling, reading, custom
- [ ] Habit creation form
- [ ] Habit deletion
- [ ] Habit streak tracking per habit
- [ ] Habit completion percentage per day
- [ ] Habit weekly view (7-day grid)
- [ ] Habit monthly view (calendar)
- [ ] Habit streak celebration
- [ ] Habit reminder notifications
- [ ] Habit reorder (priority)

### 4.13 Health Metrics
- [x] HealthMetric model: steps, resting_heart_rate, sleep_hours, hrv, source_provider, source_record_id
- [x] Health metric create endpoint
- [x] Wearable sync endpoint (WearableSyncRequest/Response)
- [x] Source provider tracking (manual, apple_health, google_fit, fitbit, etc.)
- [x] Deduplication via unique index (user_id, source_provider, source_record_id)
- [ ] Health metrics UI — steps card
- [ ] Health metrics UI — heart rate card
- [ ] Health metrics UI — sleep card
- [ ] Health metrics UI — HRV card
- [ ] Health metrics history chart (7-day, 30-day, 90-day)
- [ ] Health metrics trends analysis
- [ ] Health metrics anomaly alerts (unusual resting HR, poor sleep)
- [ ] Health metrics comparison (this week vs last week)
- [ ] Health metrics goals (daily step goal, sleep goal)
- [ ] Health metrics manual entry form
- [ ] Health metrics auto-sync from wearable (background)
- [ ] Health metrics body temperature tracking
- [ ] Health metrics blood pressure tracking
- [ ] Health metrics blood oxygen (SpO2) tracking
- [ ] Health metrics stress level tracking

### 4.14 Body Measurements
- [ ] Body measurements logging form
- [ ] Weight tracking (daily/weekly)
- [ ] Weight trend chart
- [ ] Weight moving average (7-day)
- [ ] Body fat percentage tracking
- [ ] Body fat trend chart
- [ ] Muscle mass tracking
- [ ] Waist circumference
- [ ] Hip circumference
- [ ] Chest circumference
- [ ] Arm circumference (left/right)
- [ ] Thigh circumference (left/right)
- [ ] Neck circumference
- [ ] BMI calculation and display
- [ ] Body measurement comparison (start vs current)
- [ ] Progress photos (before/after with body measurements)
- [ ] Photo overlay comparison tool

### 4.15 Fitness Goals
- [x] Goal management schemas (part of domain.py)
- [ ] Goal list view
- [ ] Goal create form
- [ ] Goal types: weight loss (target weight), muscle gain (target weight/body fat), running (distance/time), strength (target lift weight), flexibility, consistency (workout X days/week), custom
- [ ] Goal target value and deadline
- [ ] Goal progress tracking (auto-calculated from logs)
- [ ] Goal progress bar/ring
- [ ] Goal milestone markers
- [ ] Goal projected completion date
- [ ] Goal edit
- [ ] Goal complete celebration
- [ ] Goal delete/archive
- [ ] Goal difficulty adjustment (if ahead/behind)
- [ ] Goal sharing with team
- [ ] Goal accountability partner

### 4.16 Progress Charts
- [ ] Weight over time (line chart)
- [ ] Body fat over time (line chart)
- [ ] Workout volume over time (bar chart)
- [ ] Workout frequency over time (bar chart)
- [ ] Calorie intake over time (line chart)
- [ ] Macro distribution over time (stacked area chart)
- [ ] Steps over time (bar chart)
- [ ] Sleep quality over time (line chart)
- [ ] Heart rate resting over time (line chart)
- [ ] HRV over time (line chart)
- [ ] Exercise-specific progress (weight lifted for bench press, squat, deadlift)
- [ ] Personal record timeline
- [ ] Habit completion rate over time
- [ ] Wellness score over time
- [ ] Interactive chart tooltips
- [ ] Chart zoom and pan
- [ ] Chart date range selector
- [ ] Chart comparison overlay (two metrics)
- [ ] Chart export as image

### 4.17 Streaks & Achievements
- [ ] Workout streak (consecutive days with workout)
- [ ] Meal logging streak (consecutive days logged)
- [ ] Habit streak (consecutive days all habits completed)
- [ ] Step goal streak (consecutive days hitting step goal)
- [ ] Water intake streak
- [ ] Streak counter display on dashboard
- [ ] Streak history
- [ ] Achievement badges system
- [ ] Achievement: First workout logged
- [ ] Achievement: 7-day workout streak
- [ ] Achievement: 30-day workout streak
- [ ] Achievement: 100 workouts logged
- [ ] Achievement: First meal logged
- [ ] Achievement: 7-day meal logging streak
- [ ] Achievement: All macros hit for a day
- [ ] Achievement: Weight goal reached
- [ ] Achievement: New personal record
- [ ] Achievement: 10,000 steps
- [ ] Achievement: 8 hours sleep
- [ ] Achievement badge gallery view
- [ ] Achievement unlock animation
- [ ] Achievement share to social/team

### 4.18 Health Insights
- [x] Health scoring service (scoring.py)
- [ ] Daily wellness score breakdown
- [ ] Weekly health report
- [ ] Monthly health report
- [ ] Sleep quality analysis
- [ ] Recovery readiness score
- [ ] Overtraining risk assessment
- [ ] Nutrition quality assessment
- [ ] Hydration status assessment
- [ ] Stress level assessment (from HRV)
- [ ] Trend analysis (improving/declining/stable)
- [ ] Personalized insights (based on user data patterns)
- [ ] Comparison with healthy ranges
- [ ] Health risk alerts

### 4.19 AI Coach
- [x] AI coach service (ai_coach.py)
- [x] Coach model: readiness score, confidence, intensity recommendation
- [x] Coach calibration service (coach_calibration.py)
- [x] Coach feedback model (CoachFeedback entity)
- [x] Coach feedback create endpoint
- [x] CoachRecommendation schema
- [x] Model source and version tracking
- [ ] AI coach UI — today's recommendation card
- [ ] AI coach recommendation: workout intensity (rest/light/moderate/intense)
- [ ] AI coach recommendation: suggested exercises
- [ ] AI coach recommendation: nutrition adjustments
- [ ] AI coach recommendation: recovery suggestions
- [ ] AI coach feedback UI (was this helpful? too hard/too easy?)
- [ ] AI coach conversation mode (chat-based coaching)
- [ ] AI coach weekly planning suggestions
- [ ] AI coach goal adjustment recommendations
- [ ] AI coach insight explanations (why this recommendation)
- [ ] AI coach learning from user feedback
- [ ] AI coach confidence display
- [ ] AI coach model version display
- [ ] AI coach opt-in/opt-out setting

### 4.20 Wearable Integration
- [x] Wearable sync endpoint (WearableSyncRequest/Response)
- [x] Source provider tracking (manual, apple_health, google_fit, fitbit)
- [x] Deduplication of synced records
- [x] Source payload storage (raw data)
- [x] Risk score on device data
- [ ] Wearable settings UI — connect/disconnect device
- [ ] Apple Health integration setup
- [ ] Google Fit integration setup
- [ ] Fitbit integration setup
- [ ] Garmin integration setup
- [ ] Samsung Health integration setup
- [ ] Whoop integration setup
- [ ] Oura Ring integration setup
- [ ] Manual entry fallback when no wearable connected
- [ ] Wearable sync status indicator
- [ ] Wearable data sync frequency setting
- [ ] Wearable data conflict resolution (manual vs auto)
- [ ] Wearable connection status monitoring
- [ ] Wearable reconnection flow

### 4.21 Team Wellness Challenges
- [x] Social routes (social_routes.py)
- [ ] Team/challenge creation UI
- [ ] Challenge types: steps challenge, workout streak, weight loss %, consistency
- [ ] Challenge duration (1 week, 2 weeks, 1 month)
- [ ] Challenge participant list
- [ ] Challenge leaderboard
- [ ] Challenge progress tracking
- [ ] Challenge invite (by email/link)
- [ ] Challenge complete celebration
- [ ] Challenge history
- [ ] Team workout feed (see team members' activities)
- [ ] Team encouragement (likes/reactions on workouts)
- [ ] Team chat/messaging

### 4.22 Admin Dashboard
- [ ] Admin overview: total users, active users, new registrations
- [ ] Admin user management: list, search, disable, delete
- [ ] Admin user detail: profile, workouts, meals, auth events
- [ ] Admin email suppression management
- [ ] Admin privacy export jobs management
- [ ] Admin legal hold management
- [ ] Admin consent records view
- [ ] Admin audit log view
- [ ] Admin analytics dashboard
- [ ] Admin system health monitoring
- [ ] Admin feature flag management
- [ ] Admin rate limit configuration
- [ ] Admin broadcast notifications

### 4.23 Privacy & Consent
- [x] ConsentRecord model: consent_key, status, source, legal_basis
- [x] Privacy export job model (PrivacyExportJob)
- [x] Privacy export worker (background processing)
- [x] Privacy service (privacy.py)
- [x] Consent list endpoint
- [x] Consent update endpoint
- [x] Privacy export create endpoint
- [x] Privacy export status endpoint
- [x] Account deletion endpoint
- [x] Legal hold model and endpoints
- [ ] Consent management UI
- [ ] Privacy settings UI
- [ ] Data export request UI
- [ ] Data export download UI
- [ ] Account deletion UI with confirmation
- [ ] Cookie consent banner (if applicable)
- [ ] Privacy policy display
- [ ] Terms of service display
- [ ] Consent history view

---

## 5. API Integration

### 5.1 Backend API Endpoints (Existing)
- [x] Auth: `POST /auth/register` — user registration
- [x] Auth: `POST /auth/login` — login (JWT)
- [x] Auth: `POST /auth/refresh` — token refresh
- [x] Auth: `POST /auth/logout` — logout (revoke refresh token)
- [x] Auth: `POST /auth/verify-email` — email verification
- [x] Auth: `POST /auth/request-password-reset` — request password reset
- [x] Auth: `POST /auth/reset-password` — reset password
- [x] Auth: `POST /auth/login-challenge` — login challenge verification
- [x] v1: `GET /api/v1/dashboard` — daily dashboard
- [x] v1: `POST /api/v1/profile` — create profile
- [x] v1: `GET /api/v1/profile` — get profile
- [x] v1: `POST /api/v1/workouts` — log workout
- [x] v1: `GET /api/v1/workouts` — list workouts (paginated)
- [x] v1: `POST /api/v1/meals` — log meal
- [x] v1: `GET /api/v1/meals` — list meals
- [x] v1: `POST /api/v1/habits` — create habit
- [x] v1: `GET /api/v1/habits` — list habits
- [x] v1: `PATCH /api/v1/habits/{id}` — update habit
- [x] v1: `POST /api/v1/health-metrics` — log health metric
- [x] v1: `GET /api/v1/health-metrics` — list health metrics
- [x] v1: `POST /api/v1/wearable-sync` — sync wearable data
- [x] v1: `GET /api/v1/coach` — get AI coach recommendation
- [x] v1: `POST /api/v1/coach/feedback` — submit coach feedback
- [x] v1: `GET /api/v1/coach/calibration` — coach calibration data
- [x] v1: `POST /api/v1/workout-plan` — generate workout plan
- [x] v1: `POST /api/v1/nutrition-plan` — generate nutrition plan
- [x] v1: `POST /api/v1/analytics` — track analytics event
- [x] v1: `GET /api/v1/analytics` — list analytics events
- [x] v1: `GET /api/v1/retention` — user retention summary
- [x] v1: `GET /api/v1/consents` — list consents
- [x] v1: `POST /api/v1/consents` — update consent
- [x] v1: `POST /api/v1/privacy/export` — request data export
- [x] v1: `GET /api/v1/privacy/export` — list export jobs
- [x] v1: `DELETE /api/v1/account` — delete account
- [x] Admin: legal hold endpoints
- [x] Admin: email suppression endpoints
- [x] Admin: privacy export admin endpoints
- [x] Food: food search endpoints
- [x] Social: social/team endpoints
- [x] AI: AI-specific endpoints
- [x] `GET /health` — health check
- [x] `GET /ready` — readiness check
- [x] `GET /metrics` — Prometheus metrics

### 5.2 Frontend-Backend API Wiring
- [ ] Wire login form to `POST /auth/login`
- [ ] Wire registration form to `POST /auth/register`
- [ ] Wire email verification to `POST /auth/verify-email`
- [ ] Wire password reset flow
- [ ] Wire dashboard to `GET /api/v1/dashboard`
- [ ] Wire profile to `GET /api/v1/profile`
- [ ] Wire workout logging to `POST /api/v1/workouts`
- [ ] Wire workout list to `GET /api/v1/workouts`
- [ ] Wire meal logging to `POST /api/v1/meals`
- [ ] Wire meal list to `GET /api/v1/meals`
- [ ] Wire habit list to `GET /api/v1/habits`
- [ ] Wire habit toggle to `PATCH /api/v1/habits/{id}`
- [ ] Wire health metrics to `POST/GET /api/v1/health-metrics`
- [ ] Wire wearable sync to `POST /api/v1/wearable-sync`
- [ ] Wire AI coach to `GET /api/v1/coach`
- [ ] Wire coach feedback to `POST /api/v1/coach/feedback`
- [ ] Wire workout plan to `POST /api/v1/workout-plan`
- [ ] Wire nutrition plan to `POST /api/v1/nutrition-plan`
- [ ] Wire food search to food routes
- [ ] Wire consent management to consent endpoints
- [ ] Wire privacy export to privacy endpoints
- [ ] Wire account deletion to `DELETE /api/v1/account`
- [ ] Add API error handling with user-friendly messages
- [ ] Add API retry logic for transient failures
- [ ] Add JWT token storage and auto-refresh
- [ ] Add AbortController for request cancellation

### 5.3 External API Integrations
- [ ] Apple HealthKit API
- [ ] Google Fit API
- [ ] Fitbit Web API
- [ ] Garmin Connect API
- [ ] USDA FoodData Central API
- [ ] Open Food Facts API
- [ ] OpenAI/Claude API for AI coach (if using LLM)
- [ ] Email delivery service (SendGrid, AWS SES)

---

## 6. State Management

### 6.1 Current State (Vanilla JS)
- [ ] Audit current state management in index.html
- [ ] Identify all global state variables
- [ ] Identify all DOM manipulation patterns
- [ ] Identify all event listener registrations

### 6.2 State Architecture (if React migration)
- [ ] Zustand store for auth state (user, tokens)
- [ ] Zustand store for profile state
- [ ] Zustand store for workout state
- [ ] Zustand store for meal state
- [ ] Zustand store for habit state
- [ ] Zustand store for health metrics state
- [ ] Zustand store for goals state
- [ ] Zustand store for coach state
- [ ] Zustand store for wearable state
- [ ] Zustand store for UI state
- [ ] Zustand store for notification state
- [ ] React Query for server state management
- [ ] Optimistic updates for quick-logging
- [ ] Cache invalidation on data changes
- [ ] Offline queue for workout/meal logs

### 6.3 State Architecture (if vanilla JS enhancement)
- [ ] Event-driven state management (pub/sub)
- [ ] Centralized state store object
- [ ] DOM update on state changes
- [ ] LocalStorage for offline data caching
- [ ] SessionStorage for auth tokens
- [ ] IndexedDB for large datasets (workout history)

---

## 7. Performance

### 7.1 Frontend Performance
- [ ] Measure initial page load time (target < 2s)
- [ ] Measure LCP (< 2.5s)
- [ ] Measure CLS (< 0.1)
- [ ] Measure INP (< 200ms)
- [ ] Font loading optimization (Space Grotesk + IBM Plex Sans from CDN)
- [ ] Consider self-hosting fonts instead of CDN
- [ ] CSS optimization (remove unused CSS)
- [ ] JavaScript optimization (minify, tree-shake)
- [ ] Chart library lazy loading
- [ ] Image optimization (exercise images, food photos)
- [ ] Skeleton loading for dashboard cards
- [ ] Debounce food search input
- [ ] Virtualize long workout/meal history lists
- [ ] Progressive chart rendering
- [ ] Service worker caching for offline workout logging

### 7.2 Backend Performance
- [x] GZip middleware
- [x] Prometheus metrics for request timing
- [ ] Database query optimization
- [ ] Database connection pooling configuration
- [ ] Database index review (especially time-series queries)
- [ ] API response time monitoring (target < 200ms p95)
- [ ] API pagination for all list endpoints
- [ ] Redis caching for food database queries
- [ ] Redis caching for AI coach recommendations
- [ ] Background task processing for AI, exports
- [ ] Rate limiting per endpoint
- [ ] Database query timeout limits
- [ ] Slow query logging
- [ ] Batch wearable data sync

### 7.3 Real-Time Performance
- [ ] Workout timer accuracy
- [ ] Wearable data sync latency
- [ ] Dashboard auto-refresh efficiency
- [ ] SSE/WebSocket for live updates (if team features active)

---

## 8. Accessibility

### 8.1 WCAG 2.1 AA Compliance
- [ ] All interactive elements keyboard accessible
- [ ] Tab order logical
- [ ] Focus indicators visible
- [ ] Focus trap in modals
- [ ] Skip navigation link
- [ ] Landmark roles
- [ ] Heading hierarchy
- [ ] Alt text for exercise images
- [ ] ARIA labels for icon-only buttons
- [ ] ARIA labels for progress rings/bars
- [ ] ARIA live regions for timer updates
- [ ] ARIA live regions for real-time metrics
- [ ] Color contrast >= 4.5:1 for text
- [ ] Color contrast >= 3:1 for UI components
- [ ] Health status not conveyed by color alone (green/red must have icons/labels)
- [ ] Form inputs have labels
- [ ] Form errors linked to inputs
- [ ] Timer accessible to screen readers
- [ ] Charts have accessible data tables

### 8.2 Screen Reader Testing
- [ ] Test with NVDA
- [ ] Test with VoiceOver (macOS)
- [ ] Test with JAWS
- [ ] Test with TalkBack
- [ ] Verify workout timer announced
- [ ] Verify health metrics read correctly (units included)
- [ ] Verify progress percentages announced

### 8.3 Motion & Visual Preferences
- [ ] Respect `prefers-reduced-motion` (disable workout timer animations, chart transitions)
- [ ] Respect `prefers-contrast`
- [ ] Respect `prefers-color-scheme`
- [ ] Workout timer accessible without animations

---

## 9. Mobile & Responsive

### 9.1 Breakpoint System
- [ ] Mobile: 0-639px
- [ ] Tablet: 640-1023px
- [ ] Desktop: 1024-1279px
- [ ] Wide: 1280px+
- [ ] Test at each breakpoint

### 9.2 Layout Responsive Behavior
- [ ] Dashboard: single column on mobile
- [ ] Dashboard stat cards: 2-column on tablet, 1-column on mobile
- [ ] Workout logging form: full width on mobile
- [ ] Meal logging form: full width on mobile
- [ ] Charts: responsive sizing
- [ ] Navigation: bottom tab bar on mobile
- [ ] Exercise library: list view on mobile
- [ ] Calendar views: single day on mobile
- [ ] Progress photos: full-width on mobile
- [ ] Team leaderboard: simplified on mobile

### 9.3 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] Swipe to complete habits
- [ ] Swipe to delete workout/meal entries
- [ ] Pull to refresh dashboard
- [ ] Long press for exercise details
- [ ] Pinch to zoom on charts
- [ ] Touch-friendly stepper controls (sets, reps, weight)
- [ ] Touch-friendly timer controls

### 9.4 Mobile-Specific Features
- [ ] PWA installable (Add to Home Screen)
- [ ] Offline workout logging (sync when back online)
- [ ] Camera access for food photos, progress photos, receipt scanning
- [ ] Quick-log floating action button
- [ ] Haptic feedback on timer events (if supported)
- [ ] Wearable companion integration
- [ ] Motion sensors for rep counting (accelerometer) — future
- [ ] GPS for outdoor workout tracking (run/walk/bike) — future
- [ ] Widget for home screen (daily stats) — future
- [ ] Viewport height handling (100dvh)
- [ ] Safe area insets
- [ ] Input zoom prevention on iOS

---

## 10. Internationalization (i18n)

### 10.1 Infrastructure
- [ ] i18n library selection
- [ ] Translation file structure
- [ ] Default language: English
- [ ] Language detection
- [ ] Language switcher UI
- [ ] Language persistence

### 10.2 String Extraction
- [ ] Extract all UI strings from index.html
- [ ] Extract exercise names (common exercises)
- [ ] Extract muscle group names
- [ ] Extract food names / nutrition labels
- [ ] Extract habit type names
- [ ] Extract achievement names/descriptions
- [ ] Extract AI coach recommendation text
- [ ] Extract error messages
- [ ] Extract success messages
- [ ] Extract form labels
- [ ] Extract units (kg, lbs, cm, in, cal, kcal, ml, oz, etc.)

### 10.3 Locale Support
- [ ] English (en) — complete
- [ ] Spanish (es)
- [ ] French (fr)
- [ ] German (de)
- [ ] Japanese (ja)
- [ ] Chinese Simplified (zh-CN)
- [ ] Arabic (ar) — RTL
- [ ] Hindi (hi)
- [ ] Portuguese (pt-BR)
- [ ] Korean (ko)

### 10.4 Unit System
- [ ] Metric: kg, cm, ml, km, kcal
- [ ] Imperial: lbs, in/ft, fl oz, miles, cal
- [ ] User preference for unit system
- [ ] Auto-convert between systems
- [ ] Display correct unit labels throughout UI

### 10.5 Date/Time/Number Formatting
- [ ] Date formatting per locale
- [ ] Time formatting (12h/24h per locale)
- [ ] Number formatting (decimal separators)
- [ ] Weight formatting (1 decimal for kg, whole for lbs)
- [ ] Distance formatting
- [ ] Duration formatting (HH:MM:SS)

---

## 11. Security

### 11.1 Authentication Security
- [x] JWT access tokens (short-lived)
- [x] Refresh token rotation with family tracking
- [x] Password hashing (bcrypt via security.py)
- [x] Account lockout after failed login attempts
- [x] Login challenge tokens (email OTP)
- [x] Device fingerprint tracking
- [x] Risk scoring on auth events
- [x] Audit logging for all auth actions
- [x] Email verification flow
- [x] Password reset with expiring tokens
- [ ] Token storage: HttpOnly cookie for refresh token
- [ ] CSRF protection
- [ ] Rate limiting on auth endpoints
- [ ] Password complexity requirements UI
- [ ] Password breach detection (HaveIBeenPwned API)
- [ ] Concurrent session limit
- [ ] Session revocation on password change

### 11.2 Application Security
- [x] CORS middleware
- [x] GZip middleware
- [x] TrustedHost middleware
- [x] Request size limits
- [x] CSP headers (STRICT_CSP for API, UI_CSP for frontend)
- [x] Request ID tracking
- [x] IP address logging
- [x] User agent logging
- [ ] HSTS headers
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Referrer-Policy
- [ ] Permissions-Policy
- [ ] Subresource Integrity for CDN fonts

### 11.3 Data Security
- [ ] Health data encryption at rest
- [ ] Health data encryption in transit (TLS 1.2+)
- [ ] PII masking in logs
- [ ] Health data retention policy
- [ ] HIPAA compliance review (if applicable)
- [ ] Data minimization (only collect what's needed)
- [ ] Data anonymization for analytics
- [ ] Backup encryption
- [ ] Secret management for API keys

### 11.4 Privacy & Compliance
- [x] GDPR: Data export (privacy export worker)
- [x] GDPR: Right to deletion (account delete endpoint)
- [x] GDPR: Consent management (consent records)
- [x] Legal hold mechanism
- [x] Email suppression handling (bounces, complaints)
- [ ] GDPR: Data processing agreement
- [ ] GDPR: Privacy impact assessment
- [ ] CCPA compliance (if US users)
- [ ] Health data regulations (HIPAA, HITECH) — if applicable
- [ ] Cookie policy
- [ ] Data breach notification plan

### 11.5 Abuse Protection
- [x] Edge abuse protection documentation
- [x] Cloudflare WAF rules template
- [x] Cloudflare rate limit rules template
- [ ] API rate limiting implementation
- [ ] Bot detection
- [ ] Spam prevention (registration, feedback)
- [ ] Data scraping prevention
- [ ] Account enumeration prevention

### 11.6 Dependency Security
- [ ] Python dependency vulnerability scanning
- [ ] Automated dependency updates
- [ ] Lock file integrity verification
- [ ] Container image vulnerability scanning

---

## 12. Testing

### 12.1 Backend Unit Tests (Existing)
- [x] test_security.py — security function tests
- [x] test_admin_privacy_exports.py — admin privacy export tests
- [x] test_email_suppression.py — email suppression tests
- [x] test_request_utils.py — request utility tests
- [x] test_config_validation.py — config validation tests
- [x] test_coach_feedback.py — coach feedback tests
- [x] test_privacy.py — privacy tests
- [x] test_v1_pagination.py — pagination tests
- [x] test_services.py — service tests
- [x] test_legal_hold.py — legal hold tests
- [x] test_analytics.py — analytics tests
- [x] test_auth_flow.py — auth flow tests
- [x] test_runtime.py — runtime tests
- [x] test_wearable_sync.py — wearable sync tests
- [x] test_ai_coach.py — AI coach tests

### 12.2 Backend Unit Tests (To Add)
- [ ] Test: User registration — valid input
- [ ] Test: User registration — duplicate email
- [ ] Test: User registration — invalid email format
- [ ] Test: User registration — weak password
- [ ] Test: Login — valid credentials
- [ ] Test: Login — invalid password
- [ ] Test: Login — locked account
- [ ] Test: Login — unverified email
- [ ] Test: Token refresh — valid
- [ ] Test: Token refresh — expired
- [ ] Test: Token refresh — revoked (reuse detection)
- [ ] Test: Profile creation — valid
- [ ] Test: Profile creation — duplicate
- [ ] Test: Workout log — valid
- [ ] Test: Workout log — missing fields
- [ ] Test: Workout log — negative values
- [ ] Test: Meal log — valid
- [ ] Test: Meal log — negative calories
- [ ] Test: Habit — create valid
- [ ] Test: Habit — toggle status
- [ ] Test: Health metric — valid
- [ ] Test: Health metric — wearable sync deduplication
- [ ] Test: AI coach — recommendation generation
- [ ] Test: AI coach — feedback submission
- [ ] Test: Food search — valid query
- [ ] Test: Food search — empty results
- [ ] Test: Workout plan generation
- [ ] Test: Nutrition plan generation
- [ ] Test: Consent update
- [ ] Test: Privacy export creation
- [ ] Test: Account deletion — with legal hold (blocked)
- [ ] Test: Account deletion — without legal hold (success)
- [ ] Test: Analytics event tracking
- [ ] Test: Retention summary calculation

### 12.3 Frontend Unit Tests
- [ ] Test: Login form rendering
- [ ] Test: Login form validation
- [ ] Test: Registration form rendering
- [ ] Test: Dashboard card rendering
- [ ] Test: Workout form validation
- [ ] Test: Meal form validation
- [ ] Test: Habit toggle behavior
- [ ] Test: Health metric display
- [ ] Test: Chart data formatting
- [ ] Test: Progress ring calculation
- [ ] Test: Timer functionality
- [ ] Test: Theme toggle
- [ ] Test: Date formatting
- [ ] Test: Unit conversion
- [ ] Test: Empty state rendering
- [ ] Test: Error state rendering
- [ ] Test: Loading state rendering

### 12.4 End-to-End Tests
- [x] `scripts/e2e_smoke.sh` — E2E smoke test script
- [ ] E2E: Full registration flow
- [ ] E2E: Login and view dashboard
- [ ] E2E: Log workout
- [ ] E2E: Log meal
- [ ] E2E: Toggle habits
- [ ] E2E: View health metrics
- [ ] E2E: Get AI coach recommendation
- [ ] E2E: Generate workout plan
- [ ] E2E: Generate nutrition plan
- [ ] E2E: Search food
- [ ] E2E: Wearable sync
- [ ] E2E: View progress charts
- [ ] E2E: Update profile
- [ ] E2E: Change password
- [ ] E2E: Request data export
- [ ] E2E: Delete account
- [ ] E2E: Toggle dark mode
- [ ] E2E: Responsive layout (mobile)
- [ ] E2E: Keyboard navigation
- [ ] E2E test framework setup (Playwright)
- [ ] E2E test CI pipeline

### 12.5 Performance Tests
- [ ] Load test: Concurrent API requests
- [ ] Load test: Dashboard with many data points
- [ ] Load test: Wearable sync bulk data
- [ ] Load test: Food search concurrent queries
- [ ] Load test: AI coach concurrent requests
- [ ] Lighthouse CI for performance scoring
- [ ] Bundle size regression tests

### 12.6 Security Tests
- [ ] Security: Password hashing strength
- [ ] Security: JWT token validation
- [ ] Security: Refresh token rotation enforcement
- [ ] Security: Account lockout enforcement
- [ ] Security: Rate limiting verification
- [ ] Security: CORS enforcement
- [ ] Security: CSP enforcement
- [ ] Security: XSS prevention
- [ ] Security: SQL injection prevention
- [ ] Security: Sensitive data not in logs
- [ ] Penetration testing schedule

### 12.7 Visual Regression Tests
- [ ] Visual test: Dashboard
- [ ] Visual test: Workout log form
- [ ] Visual test: Meal log form
- [ ] Visual test: Health metrics cards
- [ ] Visual test: Progress charts
- [ ] Visual test: Dark mode
- [ ] Visual test: Light mode
- [ ] Visual test: Mobile layout
- [ ] Chromatic or Percy integration

---

## 13. Documentation

### 13.1 Code Documentation
- [x] `docs/ARCHITECTURE.md` — architecture overview
- [x] `docs/SECURITY.md` — security documentation
- [x] `docs/API.md` — API documentation
- [x] `docs/PRD.md` — product requirements
- [x] `docs/MVP_BACKLOG.md` — MVP backlog
- [x] `docs/DEPLOYMENT.md` — deployment guide
- [x] `docs/OPERATIONS.md` — operations guide
- [x] `docs/DB_MIGRATIONS.md` — migration guide
- [x] `docs/EDGE_ABUSE_PROTECTION.md` — abuse protection
- [x] `docs/PRODUCTION_READINESS_UIUX_GAP_PLAN.md` — UI/UX gap plan
- [ ] Backend: docstrings on all route handlers
- [ ] Backend: docstrings on all service functions
- [ ] Backend: docstrings on all model classes
- [ ] Frontend: JSDoc comments on all functions

### 13.2 API Documentation
- [x] FastAPI auto-generated OpenAPI docs
- [x] `docs/API.md` — manual API documentation
- [ ] API authentication guide (JWT flow)
- [ ] API rate limiting documentation
- [ ] API error codes reference
- [ ] API versioning strategy
- [ ] Postman/Insomnia collection
- [ ] API changelog

### 13.3 User Documentation
- [ ] Getting started guide (end user)
- [ ] Workout logging guide
- [ ] Meal tracking guide
- [ ] Understanding your health metrics guide
- [ ] AI coach guide
- [ ] Wearable setup guide (per device)
- [ ] Privacy and data guide
- [ ] FAQ
- [ ] Video tutorials

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [x] `scripts/secret_scan.sh` — secret scanning
- [x] `scripts/smoke_check.sh` — smoke tests
- [x] `scripts/cloudflare_policy_lint.sh` — policy lint
- [ ] GitHub Actions / GitLab CI workflow file
- [ ] Lint Python code (ruff/flake8)
- [ ] Type check Python code (mypy)
- [ ] Run all backend tests
- [ ] Test coverage enforcement
- [ ] Lint frontend code
- [ ] Run frontend tests
- [ ] Build frontend assets
- [ ] Docker image build
- [ ] Docker image push to registry
- [ ] Security scanning (Snyk/Trivy)
- [ ] Lighthouse CI scores

### 14.2 CD Pipeline
- [x] `scripts/deploy_production.sh` — production deploy script
- [x] `deploy-to-server.sh` — server deployment
- [x] `scripts/production_canary.sh` — canary deployment checks
- [x] `ops/systemd/rmfit-canary.service` — canary systemd service
- [ ] Staging environment auto-deploy
- [ ] Production deploy with manual approval
- [ ] Blue/green deployment
- [ ] Automated rollback on health check failure
- [ ] Database migration as part of deploy
- [ ] Health check verification post-deploy
- [ ] Smoke test post-deploy
- [ ] Deployment notification (Slack/email)

### 14.3 Environment Configuration
- [x] `.env.production.example` — production env template
- [x] `ecosystem.config.js` — PM2 configuration
- [x] `nginx.conf.example` — Nginx configuration
- [ ] Development environment setup docs
- [ ] Staging environment configuration
- [ ] Environment variable validation on startup (done in config.py)
- [ ] Secret management (Vault/AWS Secrets Manager)
- [ ] Feature flags system

### 14.4 Monitoring & Observability
- [x] Prometheus metrics endpoint (`/metrics`)
- [x] Prometheus configuration (`ops/prometheus/prometheus.yml`)
- [x] Prometheus alert rules (`ops/prometheus/alerts.yml`)
- [x] Grafana dashboard (`ops/grafana/dashboards/rmfit-overview.json`)
- [x] Grafana datasource provisioning
- [x] Alertmanager configuration
- [x] Request timing metrics (observe_request, REQUESTS_IN_PROGRESS)
- [x] Structured logging
- [x] Request ID (correlation ID) tracking
- [x] `scripts/observability_check.sh` — observability health check
- [ ] Error tracking (Sentry)
- [ ] Log aggregation (ELK/Loki)
- [ ] Custom business metrics (daily active users, workouts logged, etc.)
- [ ] Uptime monitoring (external)
- [ ] Database monitoring dashboards
- [ ] AI coach response time monitoring
- [ ] Wearable sync success rate monitoring

---

## 15. Backend

### 15.1 Database & Models
- [x] Account model — user accounts with auth
- [x] User model — user profiles with health data
- [x] WorkoutLog model — workout session entries
- [x] MealLog model — meal entries with macros
- [x] Habit model — daily habit tracking
- [x] HealthMetric model — health data from wearables/manual
- [x] CoachFeedback model — AI coach feedback loop
- [x] AnalyticsEvent model — user analytics
- [x] AuditEvent model — security audit trail
- [x] ConsentRecord model — GDPR consent tracking
- [x] PrivacyExportJob model — data export jobs
- [x] RefreshToken model — JWT refresh tokens
- [x] EmailVerificationToken model — email verification
- [x] PasswordResetToken model — password reset
- [x] LoginChallengeToken model — login challenges
- [x] EmailSuppression model — email bounce/complaint tracking
- [x] EmailWebhookEventReceipt model — webhook deduplication
- [x] 18+ Alembic migrations
- [x] `schema.sql` — full PostgreSQL schema
- [x] Database indexes for performance
- [x] Unique constraints for data integrity
- [ ] Database seed script for development
- [ ] Database backup automation (script exists)
- [ ] Read replica configuration
- [ ] Time-series data partitioning (health_metrics, workout_logs)
- [ ] Soft delete support
- [ ] Data archival policy (old analytics events)

### 15.2 API Architecture
- [x] FastAPI with versioned routes (/api/v1)
- [x] Pydantic v2 schemas for validation
- [x] SQLAlchemy ORM with relationships
- [x] Dependency injection (get_current_account, get_profile_for_account)
- [x] Pagination support
- [x] Request validation middleware
- [x] CORS, GZip, TrustedHost middleware
- [ ] API versioning (v2 planning)
- [ ] Cursor-based pagination (instead of offset)
- [ ] API rate limiting middleware
- [ ] Webhook delivery for wearable sync events
- [ ] OpenAPI spec customization
- [ ] GraphQL endpoint (optional, for flexible queries)

### 15.3 Services Architecture
- [x] AI Coach service — readiness scoring, intensity recommendation
- [x] AI Meal Planner service — nutrition plan generation
- [x] Analytics service — event tracking, retention analysis, cleanup
- [x] Audit service — security event logging
- [x] Coach Calibration service — model calibration
- [x] Email Delivery service — transactional emails
- [x] Email Suppression service — bounce/complaint handling
- [x] Email Webhook Security service — webhook signature validation
- [x] Food Database service — food lookup
- [x] Metrics service — Prometheus metrics
- [x] Planner service — workout/meal planning
- [x] Privacy service — GDPR compliance
- [x] Scoring service — health scoring
- [x] Privacy Export Worker — background job processing
- [ ] Notification service (in-app, push)
- [ ] Challenge/social service
- [ ] Achievement/gamification service
- [ ] Wearable data normalization service
- [ ] Scheduled job runner (token cleanup, analytics rollup)

### 15.4 Error Handling
- [x] Request validation error handler (RequestValidationError)
- [x] HTTP exception handler
- [x] RequestTooLargeError handler
- [x] JSON error response format
- [ ] Global unhandled exception handler
- [ ] Error alerting for critical failures
- [ ] Graceful degradation when AI service unavailable
- [ ] Database connection error recovery
- [ ] External API timeout handling

### 15.5 Scalability
- [ ] Horizontal scaling (stateless backend)
- [ ] Database connection pool tuning
- [ ] Redis caching for food database, coach recommendations
- [ ] Background job queue (Celery/ARQ) for AI, exports
- [ ] Load balancer configuration
- [ ] Auto-scaling rules
- [ ] CDN for static assets (exercise images, UI)
- [ ] Message queue for wearable sync events

---

## Appendix A: FitterMe Views & Pages Inventory

1. Login Page
2. Registration Page
3. Email Verification Page
4. Password Reset Request Page
5. Password Reset Page
6. Login Challenge (OTP) Page
7. Profile Setup Wizard
8. Dashboard / Daily OS
9. Workout Logging Form
10. Workout History List
11. Workout History Calendar Heatmap
12. Workout Detail View
13. Workout Plan List
14. Workout Plan Detail
15. Workout Plan Generator
16. Exercise Library
17. Exercise Detail
18. Meal Logging Form
19. Meal History List
20. Meal Detail
21. Nutrition Analysis View
22. Nutrition Plan Generator
23. Nutrition Plan View
24. Food Search
25. Food Detail
26. Habit Tracker (Daily)
27. Habit Tracker (Weekly)
28. Habit Manager
29. Health Metrics Dashboard
30. Health Metric History Chart
31. Body Measurements Form
32. Body Measurements History
33. Progress Photos Gallery
34. Progress Photo Comparison
35. Fitness Goals List
36. Goal Detail (Progress)
37. Goal Create/Edit Form
38. Progress Charts Overview
39. Exercise-Specific Progress
40. Streaks Dashboard
41. Achievements Gallery
42. Achievement Detail
43. Health Insights Report
44. AI Coach Recommendation Card
45. AI Coach Feedback Form
46. AI Coach Conversation (future)
47. Wearable Integration Settings
48. Wearable Sync Status
49. Team Wellness Challenges List
50. Challenge Detail / Leaderboard
51. Challenge Create Form
52. Team Activity Feed
53. Admin Dashboard
54. Admin User Management
55. Admin Email Suppressions
56. Admin Privacy Export Jobs
57. Admin Legal Holds
58. Admin Audit Log
59. Privacy Settings
60. Consent Management
61. Data Export Request
62. Account Settings
63. Profile Edit
64. Notification Settings
65. Error Page (404)
66. Error Page (500)
67. Maintenance Page
68. Loading/Splash Screen
69. Empty States (per section)

---

## Appendix B: React Migration Component Inventory

### Layout Components
- [ ] `AppLayout` — main layout shell
- [ ] `AuthLayout` — login/register layout
- [ ] `DashboardLayout` — dashboard grid
- [ ] `TopBar` — top navigation (or orbit-bar wrapper)
- [ ] `BottomNav` — mobile bottom navigation
- [ ] `Sidebar` — desktop sidebar navigation
- [ ] `PageHeader` — page title + breadcrumbs

### Auth Components
- [ ] `LoginForm` — email/password login
- [ ] `RegisterForm` — registration form
- [ ] `EmailVerificationPage` — verify email
- [ ] `PasswordResetForm` — reset password
- [ ] `LoginChallengeForm` — OTP input
- [ ] `ProfileSetupWizard` — onboarding wizard

### Dashboard Components
- [ ] `DailyDashboard` — main dashboard view
- [ ] `StepsCard` — steps with progress ring
- [ ] `CaloriesCard` — calories with progress ring
- [ ] `WaterIntakeCard` — water tracker
- [ ] `SleepCard` — sleep duration/quality
- [ ] `HeartRateCard` — resting HR
- [ ] `HRVCard` — heart rate variability
- [ ] `WellnessScore` — composite score
- [ ] `StreakCounter` — current streak display
- [ ] `TodaySchedule` — today's workout/meals
- [ ] `QuickAddBar` — quick-log buttons

### Workout Components
- [ ] `WorkoutLogger` — workout logging form
- [ ] `ExerciseInput` — exercise name + details
- [ ] `SetRepWeightInput` — sets/reps/weight stepper
- [ ] `WorkoutTimer` — start/pause/stop timer
- [ ] `RestTimer` — between-set rest timer
- [ ] `WorkoutHistory` — workout list with filtering
- [ ] `CalendarHeatmap` — workout frequency heatmap
- [ ] `ExerciseLibrary` — searchable exercise list
- [ ] `ExerciseCard` — exercise detail card
- [ ] `WorkoutPlan` — plan view
- [ ] `PlanGenerator` — AI plan generator

### Nutrition Components
- [ ] `MealLogger` — meal logging form
- [ ] `FoodSearch` — food search with results
- [ ] `FoodItem` — food item card
- [ ] `MacroProgressBars` — protein/carbs/fat bars
- [ ] `CalorieRing` — calorie progress ring
- [ ] `MealHistory` — meal list
- [ ] `NutritionPlan` — plan view
- [ ] `NutritionPlanGenerator` — AI nutrition planner
- [ ] `FoodDetail` — full nutritional info

### Health Components
- [ ] `HealthMetricsGrid` — metrics card grid
- [ ] `MetricHistoryChart` — line chart for any metric
- [ ] `BodyMeasurementForm` — measurement input
- [ ] `BodyMeasurementChart` — trend chart
- [ ] `ProgressPhotoGallery` — photo gallery
- [ ] `ProgressPhotoComparison` — before/after slider

### Goal & Achievement Components
- [ ] `GoalList` — goals list
- [ ] `GoalProgressCard` — goal progress display
- [ ] `GoalForm` — create/edit goal
- [ ] `AchievementGallery` — badge gallery
- [ ] `AchievementBadge` — individual badge
- [ ] `StreakDisplay` — streak visualization

### AI Coach Components
- [ ] `CoachCard` — today's recommendation
- [ ] `CoachFeedbackForm` — feedback input
- [ ] `CoachInsight` — insight explanation
- [ ] `CoachChat` — conversation mode (future)

### Chart Components
- [ ] `WeightChart` — weight over time
- [ ] `VolumeChart` — workout volume over time
- [ ] `CalorieChart` — calorie trend
- [ ] `MacroChart` — macro distribution
- [ ] `StepsChart` — steps over time
- [ ] `SleepChart` — sleep quality over time
- [ ] `HRChart` — heart rate over time
- [ ] `HRVChart` — HRV over time
- [ ] `ExerciseProgressChart` — exercise-specific progress
- [ ] `PRTimeline` — personal records timeline

### Admin Components
- [ ] `AdminDashboard` — admin overview
- [ ] `UserManagement` — user list/search
- [ ] `UserDetail` — user detail view
- [ ] `EmailSuppressionManager` — email suppression admin
- [ ] `PrivacyExportAdmin` — export job admin
- [ ] `LegalHoldManager` — legal hold admin
- [ ] `AuditLogViewer` — audit log with filtering

### Shared Components
- [ ] `DataTable` — reusable table
- [ ] `EmptyState` — empty state
- [ ] `ErrorBoundary` — error boundary
- [ ] `LoadingSkeleton` — skeleton loader
- [ ] `ConfirmDialog` — confirmation modal
- [ ] `Pagination` — pagination
- [ ] `FilterBar` — search + filter
- [ ] `DateRangePicker` — date range
- [ ] `NumberStepper` — increment/decrement input
- [ ] `ProgressRing` — circular progress
- [ ] `ProgressBar` — horizontal progress

### Hook Library
- [ ] `useAuth()` — authentication state + actions
- [ ] `useProfile()` — user profile
- [ ] `useWorkouts()` — workout CRUD
- [ ] `useMeals()` — meal CRUD
- [ ] `useHabits()` — habit CRUD
- [ ] `useHealthMetrics()` — health metrics
- [ ] `useGoals()` — goals CRUD
- [ ] `useCoach()` — AI coach
- [ ] `useWearable()` — wearable sync
- [ ] `useExerciseLibrary()` — exercise search
- [ ] `useFoodSearch()` — food search
- [ ] `useAnalytics()` — analytics tracking
- [ ] `useTimer()` — workout/rest timer
- [ ] `useTheme()` — theme toggle
- [ ] `useDebounce()` — debounce
- [ ] `useMediaQuery()` — responsive breakpoints
- [ ] `useOfflineQueue()` — offline data sync

---

## Appendix C: Detailed Test Scenarios

### C.1 Authentication Test Scenarios
- [ ] Scenario: Register with valid email and strong password
- [ ] Scenario: Register with existing email (expect 409 Conflict)
- [ ] Scenario: Register with invalid email format (expect 422)
- [ ] Scenario: Register with weak password (expect 422)
- [ ] Scenario: Register with password < 8 chars (expect 422)
- [ ] Scenario: Register with password missing uppercase
- [ ] Scenario: Register with password missing number
- [ ] Scenario: Login with correct credentials returns JWT + refresh token
- [ ] Scenario: Login with wrong password increments failed_login_attempts
- [ ] Scenario: Login with wrong password 5 times triggers account lockout
- [ ] Scenario: Login with locked account returns 403
- [ ] Scenario: Login with locked account after lockout expires succeeds
- [ ] Scenario: Login with unverified email returns appropriate error
- [ ] Scenario: Refresh token rotation — valid refresh returns new access + refresh
- [ ] Scenario: Refresh token rotation — used refresh (reuse detection) revokes family
- [ ] Scenario: Refresh token rotation — expired refresh returns 401
- [ ] Scenario: Logout revokes refresh token
- [ ] Scenario: Email verification with valid token verifies account
- [ ] Scenario: Email verification with expired token returns error
- [ ] Scenario: Email verification with already-used token returns error
- [ ] Scenario: Password reset request sends email (or creates token)
- [ ] Scenario: Password reset with valid token changes password
- [ ] Scenario: Password reset with expired token fails
- [ ] Scenario: Password reset with already-used token fails
- [ ] Scenario: Login challenge triggered on suspicious login
- [ ] Scenario: Login challenge with correct OTP succeeds
- [ ] Scenario: Login challenge with wrong OTP (3 attempts) fails
- [ ] Scenario: Login challenge with expired token fails
- [ ] Scenario: Device fingerprint change triggers higher risk score
- [ ] Scenario: New IP address triggers risk flag
- [ ] Scenario: Concurrent sessions from different devices

### C.2 User Profile Test Scenarios
- [ ] Scenario: Create profile with valid data
- [ ] Scenario: Create profile with negative age (expect 422)
- [ ] Scenario: Create profile with zero height (expect 422)
- [ ] Scenario: Create profile with negative weight (expect 422)
- [ ] Scenario: Create profile with empty name (expect 422)
- [ ] Scenario: Create profile when one already exists (expect 409)
- [ ] Scenario: Get profile returns correct data
- [ ] Scenario: Profile links to correct account
- [ ] Scenario: Update profile fields (height, weight, goal)
- [ ] Scenario: Profile with various goal types
- [ ] Scenario: Profile with various diet types

### C.3 Workout Logging Test Scenarios
- [ ] Scenario: Log workout with all fields
- [ ] Scenario: Log workout with minimum fields (exercise_name, muscle_group, sets, reps)
- [ ] Scenario: Log workout with zero weight_kg (bodyweight exercise)
- [ ] Scenario: Log workout with duration_min > 0
- [ ] Scenario: Log workout with completed=false (incomplete set)
- [ ] Scenario: Log workout with negative sets (expect 422)
- [ ] Scenario: Log workout with negative reps (expect 422)
- [ ] Scenario: Log workout with negative weight (expect 422)
- [ ] Scenario: Log workout with empty exercise_name (expect 422)
- [ ] Scenario: Log workout with empty muscle_group (expect 422)
- [ ] Scenario: List workouts returns user's workouts only
- [ ] Scenario: List workouts with pagination (page 1, page 2)
- [ ] Scenario: List workouts returns empty for new user
- [ ] Scenario: Workout logged_at defaults to current time
- [ ] Scenario: Log multiple workouts in one session
- [ ] Scenario: Workout volume calculation (sets * reps * weight)

### C.4 Meal Logging Test Scenarios
- [ ] Scenario: Log meal with all fields
- [ ] Scenario: Log meal with minimum fields (meal_name, calories, protein, carbs, fat)
- [ ] Scenario: Log meal with zero calories (expect 422 or allow)
- [ ] Scenario: Log meal with negative calories (expect 422)
- [ ] Scenario: Log meal with negative protein (expect 422)
- [ ] Scenario: Log meal with empty meal_name (expect 422)
- [ ] Scenario: List meals returns user's meals only
- [ ] Scenario: List meals with date filter
- [ ] Scenario: List meals returns empty for new user
- [ ] Scenario: Daily calorie total calculation
- [ ] Scenario: Daily macro total calculation
- [ ] Scenario: Meal logged_at defaults to current time

### C.5 Habit Tracking Test Scenarios
- [ ] Scenario: Create habit with valid data
- [ ] Scenario: Create habit with empty habit_type (expect 422)
- [ ] Scenario: Toggle habit status from false to true
- [ ] Scenario: Toggle habit status from true to false
- [ ] Scenario: List habits for today
- [ ] Scenario: List habits for specific date
- [ ] Scenario: Habit date defaults to today
- [ ] Scenario: Multiple habits for same date
- [ ] Scenario: Habit streak calculation (consecutive days all complete)
- [ ] Scenario: Habit completion percentage (completed / total for day)

### C.6 Health Metrics Test Scenarios
- [ ] Scenario: Log health metric with all fields
- [ ] Scenario: Log health metric with zero steps
- [ ] Scenario: Log health metric with zero heart rate (expect 422 or allow)
- [ ] Scenario: Log health metric with negative values (expect 422)
- [ ] Scenario: Log health metric from manual source
- [ ] Scenario: Log health metric from apple_health source
- [ ] Scenario: Log health metric from fitbit source
- [ ] Scenario: Wearable sync with valid data
- [ ] Scenario: Wearable sync deduplication (same source_record_id)
- [ ] Scenario: Wearable sync with new data creates new record
- [ ] Scenario: Wearable sync with unknown provider
- [ ] Scenario: List health metrics for user
- [ ] Scenario: List health metrics with date range
- [ ] Scenario: Health metric recorded_at vs synced_at distinction

### C.7 AI Coach Test Scenarios
- [ ] Scenario: Get recommendation for user with workout history
- [ ] Scenario: Get recommendation for user with no history (new user)
- [ ] Scenario: Get recommendation considers sleep hours
- [ ] Scenario: Get recommendation considers resting heart rate
- [ ] Scenario: Get recommendation considers HRV
- [ ] Scenario: Get recommendation considers recent workout intensity
- [ ] Scenario: Recommendation returns rest/light/moderate/intense
- [ ] Scenario: Recommendation includes readiness score
- [ ] Scenario: Recommendation includes confidence score
- [ ] Scenario: Submit positive coach feedback
- [ ] Scenario: Submit negative coach feedback
- [ ] Scenario: Submit feedback with perceived exertion
- [ ] Scenario: Submit feedback with completed_workout status
- [ ] Scenario: Coach calibration data returns correct model stats
- [ ] Scenario: Coach model version tracking
- [ ] Scenario: Coach handles insufficient data gracefully

### C.8 Food Database Test Scenarios
- [ ] Scenario: Search food by name (e.g., "chicken breast")
- [ ] Scenario: Search food with no results
- [ ] Scenario: Search food with special characters
- [ ] Scenario: Search food returns nutritional info (calories, protein, carbs, fat)
- [ ] Scenario: Search food returns serving sizes
- [ ] Scenario: Search food pagination (many results)
- [ ] Scenario: Food search performance (< 200ms response)

### C.9 Workout Plan Generation Test Scenarios
- [ ] Scenario: Generate plan for weight loss goal
- [ ] Scenario: Generate plan for muscle gain goal
- [ ] Scenario: Generate plan for endurance goal
- [ ] Scenario: Generate plan with 3 days/week frequency
- [ ] Scenario: Generate plan with 5 days/week frequency
- [ ] Scenario: Generate plan considers user profile (age, weight, goal)
- [ ] Scenario: Generated plan includes exercise names and sets/reps
- [ ] Scenario: Generated plan includes muscle group balance

### C.10 Privacy & Compliance Test Scenarios
- [ ] Scenario: Create privacy export job
- [ ] Scenario: Privacy export job status transitions (pending -> processing -> completed)
- [ ] Scenario: Privacy export includes all user data
- [ ] Scenario: Privacy export excludes other users' data
- [ ] Scenario: Privacy export download with nonce
- [ ] Scenario: Privacy export expiry
- [ ] Scenario: Privacy export retry on failure
- [ ] Scenario: Privacy export max retries exhausted
- [ ] Scenario: Account deletion removes all user data
- [ ] Scenario: Account deletion blocked by legal hold
- [ ] Scenario: Account deletion removes refresh tokens
- [ ] Scenario: Account deletion removes workout logs
- [ ] Scenario: Account deletion removes meal logs
- [ ] Scenario: Account deletion removes habits
- [ ] Scenario: Account deletion removes health metrics
- [ ] Scenario: Account deletion removes coach feedback
- [ ] Scenario: Account deletion removes analytics events
- [ ] Scenario: Account deletion removes consent records
- [ ] Scenario: Consent update — grant consent
- [ ] Scenario: Consent update — revoke consent
- [ ] Scenario: Consent list returns all consents for account
- [ ] Scenario: Legal hold prevents account deletion
- [ ] Scenario: Legal hold set by admin
- [ ] Scenario: Legal hold release by admin
- [ ] Scenario: Legal hold audit trail

### C.11 Email System Test Scenarios
- [ ] Scenario: Email delivery for verification
- [ ] Scenario: Email delivery for password reset
- [ ] Scenario: Email suppression on bounce
- [ ] Scenario: Email suppression on complaint
- [ ] Scenario: Email suppression prevents future sends
- [ ] Scenario: Email suppression release
- [ ] Scenario: Webhook event deduplication
- [ ] Scenario: Webhook signature validation
- [ ] Scenario: Webhook invalid signature rejection

---

## Appendix D: Detailed Responsive Design Specifications

### D.1 Mobile Layout (0-639px)
- [ ] Header: Logo + hamburger menu + notification bell
- [ ] Navigation: Bottom tab bar (Dashboard, Workouts, Nutrition, Health, More)
- [ ] Dashboard: Single column, scrollable cards
- [ ] Stat cards: 2-column grid (steps+cal, sleep+hr)
- [ ] Progress rings: Smaller size, centered
- [ ] Workout form: Full width, stacked fields
- [ ] Meal form: Full width, stacked fields
- [ ] Food search: Full width with inline results
- [ ] Charts: Full width, touch-optimized, minimal legends
- [ ] Habit list: Full width, checkbox + text
- [ ] Workout history: Card layout (not table)
- [ ] Meal history: Card layout (not table)
- [ ] Timer: Large display, large touch targets
- [ ] Modals: Full screen (slide up)
- [ ] Quick-add: Floating action button (bottom right)
- [ ] Camera: Full screen viewfinder for photos
- [ ] Exercise library: List view with expandable details

### D.2 Tablet Layout (640-1023px)
- [ ] Header: Full width with search
- [ ] Navigation: Collapsible left sidebar
- [ ] Dashboard: Two-column grid
- [ ] Stat cards: 3-column grid
- [ ] Charts: Two charts side by side
- [ ] Workout form: Two-column (exercise left, details right)
- [ ] Food search: Side panel results
- [ ] Timer: Medium display

### D.3 Desktop Layout (1024-1279px)
- [ ] Navigation: Fixed left sidebar (~220px)
- [ ] Dashboard: Multi-column dashboard grid
- [ ] Stat cards: 4-column grid
- [ ] Charts: Full size with legends and tooltips
- [ ] Workout form: Multi-column
- [ ] Exercise library: Grid with images
- [ ] Team challenges: Table view with leaderboard

### D.4 Wide Layout (1280px+)
- [ ] Content: Max-width 1440px centered
- [ ] Dashboard: Widget grid with more widgets visible
- [ ] Charts: Extra large, detailed
- [ ] Exercise library: Grid with large cards

---

## Appendix E: Health Data Models Specification

### E.1 Body Measurement Model (To Build)
- [ ] `id` — unique identifier
- [ ] `user_id` — user reference
- [ ] `weight_kg` — body weight
- [ ] `body_fat_pct` — body fat percentage
- [ ] `muscle_mass_kg` — skeletal muscle mass
- [ ] `waist_cm` — waist circumference
- [ ] `hip_cm` — hip circumference
- [ ] `chest_cm` — chest circumference
- [ ] `left_arm_cm` — left arm circumference
- [ ] `right_arm_cm` — right arm circumference
- [ ] `left_thigh_cm` — left thigh circumference
- [ ] `right_thigh_cm` — right thigh circumference
- [ ] `neck_cm` — neck circumference
- [ ] `bmi` — calculated BMI
- [ ] `notes` — user notes
- [ ] `photo_ids` — JSONB array of progress photo references
- [ ] `measured_at` — measurement date
- [ ] `created_at` — creation timestamp

### E.2 Exercise Library Model (To Build)
- [ ] `id` — unique identifier
- [ ] `name` — exercise name
- [ ] `description` — exercise description
- [ ] `instructions` — step-by-step text
- [ ] `tips` — form cues / tips
- [ ] `primary_muscles` — JSONB array of primary muscle groups
- [ ] `secondary_muscles` — JSONB array of secondary muscle groups
- [ ] `equipment` — enum: barbell, dumbbell, machine, bodyweight, bands, cable, kettlebell, none
- [ ] `type` — enum: strength, cardio, flexibility, plyometric, olympic
- [ ] `difficulty` — enum: beginner, intermediate, advanced
- [ ] `image_url` — exercise demonstration image
- [ ] `video_url` — exercise demonstration video (nullable)
- [ ] `is_custom` — boolean, user-created vs system
- [ ] `created_by` — user_id (for custom exercises)
- [ ] `created_at` — creation timestamp

### E.3 Fitness Goal Model (To Build)
- [ ] `id` — unique identifier
- [ ] `user_id` — user reference
- [ ] `name` — goal name
- [ ] `type` — enum: weight_loss, muscle_gain, running, strength, flexibility, consistency, custom
- [ ] `target_value` — target numeric value
- [ ] `target_unit` — unit for target (kg, lbs, km, min, days/week)
- [ ] `current_value` — current progress
- [ ] `start_value` — starting value
- [ ] `start_date` — goal start date
- [ ] `deadline` — target completion date
- [ ] `milestones` — JSONB array of milestone objects
- [ ] `priority` — int, priority ranking
- [ ] `is_completed` — boolean
- [ ] `completed_at` — completion timestamp
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### E.4 Achievement Model (To Build)
- [ ] `id` — unique identifier
- [ ] `user_id` — user reference
- [ ] `achievement_key` — enum key for achievement type
- [ ] `name` — display name
- [ ] `description` — achievement description
- [ ] `icon` — badge icon identifier
- [ ] `tier` — enum: bronze, silver, gold, platinum
- [ ] `unlocked_at` — when achievement was earned
- [ ] `progress` — numeric progress toward unlock
- [ ] `target` — numeric target for unlock
- [ ] `created_at` — creation timestamp

### E.5 Team Challenge Model (To Build)
- [ ] `id` — unique identifier
- [ ] `creator_user_id` — challenge creator
- [ ] `name` — challenge name
- [ ] `description` — challenge description
- [ ] `type` — enum: steps, workout_streak, weight_loss_pct, consistency
- [ ] `target_value` — challenge target
- [ ] `start_date` — challenge start
- [ ] `end_date` — challenge end
- [ ] `max_participants` — max team size
- [ ] `is_active` — boolean
- [ ] `created_at` — creation timestamp

### E.6 Challenge Participant Model (To Build)
- [ ] `id` — unique identifier
- [ ] `challenge_id` — challenge reference
- [ ] `user_id` — participant user
- [ ] `current_value` — participant progress
- [ ] `rank` — current leaderboard position
- [ ] `joined_at` — join timestamp
- [ ] `completed_at` — completion timestamp (nullable)

### E.7 Progress Photo Model (To Build)
- [ ] `id` — unique identifier
- [ ] `user_id` — user reference
- [ ] `image_path` — stored image path (encrypted storage)
- [ ] `thumbnail_path` — thumbnail for gallery
- [ ] `body_measurement_id` — linked measurement (nullable)
- [ ] `notes` — user notes
- [ ] `taken_at` — photo date
- [ ] `created_at` — creation timestamp

---

## Appendix F: Error State Inventory

### F.1 Network Errors
- [ ] Error state: No internet connection (offline banner)
- [ ] Error state: API request timeout
- [ ] Error state: Server 500 error
- [ ] Error state: Server 502/503 (backend down)
- [ ] Retry mechanism: Auto retry with exponential backoff
- [ ] Retry mechanism: Manual retry button
- [ ] Offline mode: Queue workout/meal logs for sync when online

### F.2 Validation Errors
- [ ] Error state: Required field empty
- [ ] Error state: Invalid number (negative where not allowed)
- [ ] Error state: Invalid date
- [ ] Error state: Exercise name too long
- [ ] Error state: Duplicate habit for same date
- [ ] Inline error messages under fields
- [ ] Form-level error summary
- [ ] Toast for server-side validation errors

### F.3 Auth Errors
- [ ] Error state: Session expired (401) — redirect to login
- [ ] Error state: Account locked — show lockout message with time
- [ ] Error state: Email not verified — show verification prompt
- [ ] Error state: Password too weak — show requirements
- [ ] Error state: Login challenge required — show OTP form

### F.4 Health Data Errors
- [ ] Error state: Wearable sync failed — show retry
- [ ] Error state: Wearable disconnected — show reconnect
- [ ] Error state: AI coach unavailable — show fallback recommendation
- [ ] Error state: Food search unavailable — show manual entry
- [ ] Error state: Photo upload failed — show retry
- [ ] Error state: Large file upload (> limit) — show size warning

---

## Appendix G: Loading State Inventory

### G.1 Page-Level Loading
- [ ] Loading state: Initial app load (splash with logo animation)
- [ ] Loading state: Dashboard loading (skeleton cards + rings)
- [ ] Loading state: Workout history loading (skeleton list)
- [ ] Loading state: Nutrition view loading (skeleton macro bars)

### G.2 Component-Level Loading
- [ ] Loading state: Stat cards (shimmer effect)
- [ ] Loading state: Progress rings (empty ring with shimmer)
- [ ] Loading state: Charts (skeleton chart area)
- [ ] Loading state: Food search results (skeleton list)
- [ ] Loading state: Exercise library (skeleton cards)
- [ ] Loading state: Workout plan generation (animated progress)
- [ ] Loading state: Nutrition plan generation (animated progress)
- [ ] Loading state: AI coach thinking (typing indicator)
- [ ] Loading state: Wearable syncing (sync icon animation)

### G.3 Action-Level Loading
- [ ] Loading state: Form submission (button spinner)
- [ ] Loading state: Workout timer starting (countdown 3-2-1)
- [ ] Loading state: Photo upload (progress bar)
- [ ] Loading state: Data export (progress percentage)
- [ ] Loading state: Barcode scanning (camera overlay)
- [ ] Loading state: Account deletion (multi-step progress)

---

## Appendix H: Notification Types Inventory

### H.1 Workout Notifications
- [ ] Notification: Workout reminder (scheduled time)
- [ ] Notification: Workout streak milestone (7, 14, 30, 60, 90, 365 days)
- [ ] Notification: Personal record set
- [ ] Notification: Workout plan day reminder
- [ ] Notification: Rest day recommendation

### H.2 Nutrition Notifications
- [ ] Notification: Meal logging reminder (breakfast, lunch, dinner)
- [ ] Notification: Calorie goal approaching
- [ ] Notification: Water intake reminder
- [ ] Notification: Macro imbalance alert (too much/little protein)

### H.3 Health Notifications
- [ ] Notification: Unusual resting heart rate detected
- [ ] Notification: Poor sleep quality detected
- [ ] Notification: Step goal achieved
- [ ] Notification: Wearable sync failed
- [ ] Notification: Recovery recommendation (rest day needed)

### H.4 Goal Notifications
- [ ] Notification: Goal milestone reached
- [ ] Notification: Goal deadline approaching
- [ ] Notification: Goal completed
- [ ] Notification: Goal behind schedule

### H.5 Social Notifications
- [ ] Notification: Challenge invitation
- [ ] Notification: Challenge started
- [ ] Notification: Challenge position change (leaderboard)
- [ ] Notification: Challenge ending soon
- [ ] Notification: Challenge completed
- [ ] Notification: Team member liked your workout
- [ ] Notification: Team member set a personal record

### H.6 Account Notifications
- [ ] Notification: Email verification reminder
- [ ] Notification: Password change confirmation
- [ ] Notification: New device login
- [ ] Notification: Account lockout alert
- [ ] Notification: Privacy export ready for download
- [ ] Notification: Data retention reminder

---

*Generated: 2026-04-06 | Total checkboxes: ~1200+ | Target: 2000+ lines*
