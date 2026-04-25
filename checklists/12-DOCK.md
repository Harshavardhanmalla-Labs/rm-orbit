# 12 — Dock (Workspace Hub) — Comprehensive Checklist

> **App:** RM Dock — Workspace Hub / Dashboard
> **Stack:** Vanilla HTML/JS frontend (`Dock/frontend/index.html`, 1076 lines) + Python/FastAPI backend (`Dock/backend/`)
> **Design system:** orbit-tokens.css, orbit-ui.css, orbit-bar.js (already integrated in HTML)
> **Backend models:** DockApp, License, Assignment, DockRequest, DockPackage, DockAuditEvent, BudgetPolicy, ProcurementConfig
> **Backend routes:** Full CRUD for apps, licenses, assignments, requests, budget policies, procurement configs, audit events
> **Auth:** Hybrid mode (Gate OIDC Bearer + header fallback), role-based (admin/manager/member)
> **Status:** Frontend exists as vanilla HTML SPA; backend is fully database-backed with Alembic migrations
> **Last synced with PER_APP_CHECKLIST.md:** 2026-04-06
>
> Legend: `[x]` = done · `[ ]` = todo · `[~]` = in progress · `[-]` = N/A / skipped

---

## 1. Project Setup & Configuration

### 1.1 Current Vanilla HTML/JS Setup
- [x] `Dock/frontend/index.html` — single-file SPA (1076 lines)
- [x] `Dock/frontend/public/orbit-ui/orbit-tokens.css` — design tokens
- [x] `Dock/frontend/public/orbit-ui/orbit-ui.css` — component styles
- [x] `Dock/frontend/public/orbit-ui/orbit-bar.js` — top navigation bar
- [x] `Dock/frontend/public/orbit-ui/orbit-theme-init.js` — dark mode bootstrap
- [x] `Dock/frontend/public/orbit-ui/orbit-tailwind-v4.css` — Tailwind v4 theme
- [x] `Dock/frontend/public/fonts/RMForma-Regular.woff2` — brand font
- [x] `Dock/frontend/public/fonts/RMForma-SemiBold.woff2` — brand font
- [x] `Dock/frontend/public/fonts/RMForma-Bold.woff2` — brand font
- [x] `Dock/frontend/public/fonts/RM-Samplet-Regular.ttf` — brand font
- [ ] Add `manifest.json` for PWA support
- [ ] Add `favicon.ico` and app icons (16, 32, 192, 512)
- [ ] Add Open Graph / social sharing meta tags
- [ ] Add `robots.txt`
- [ ] Add `sitemap.xml` (if public pages exist)
- [ ] Configure Content Security Policy headers
- [ ] Add `apple-touch-icon.png`
- [ ] Add service worker registration for offline support

### 1.2 Backend Setup
- [x] `Dock/backend/app/main.py` — FastAPI app with SPA serving
- [x] `Dock/backend/app/routes.py` — Full API router
- [x] `Dock/backend/app/models.py` — SQLAlchemy models (8 models)
- [x] `Dock/backend/app/database.py` — DB session factory
- [x] `Dock/backend/alembic.ini` — Alembic configuration
- [x] `Dock/backend/alembic/versions/f5f164f1d072_init_dock.py` — initial migration
- [x] `Dock/backend/alembic/versions/37fec8f797a3_add_budget_and_procurement_policies.py` — budget migration
- [x] `Dock/backend/requirements.txt` — Python dependencies
- [x] `Dock/backend/.env.example` — environment variable template
- [x] `Dock/backend/tests/test_api.py` — API tests
- [x] `Dock/backend/tests/test_secure_sync_helpers.py` — Secure bridge tests
- [ ] Add `pyproject.toml` for modern Python packaging
- [ ] Add `Makefile` or `justfile` for common commands
- [ ] Add `.flake8` / `ruff.toml` linting configuration
- [ ] Add `mypy.ini` for type checking
- [ ] Add `pre-commit` hooks configuration
- [ ] Add `docker-compose.yml` for local development
- [ ] Add `docker-compose.test.yml` for CI testing
- [ ] Add health check endpoint with DB connectivity check

### 1.3 Docker & Deployment
- [x] `Dock/Dockerfile` — container image
- [x] `Dock/start-backend.sh` — backend start script
- [x] `Dock/start-frontend.sh` — frontend start script
- [ ] Multi-stage Docker build (build frontend + serve from backend)
- [ ] Docker health check in Dockerfile
- [ ] `.dockerignore` to exclude unnecessary files
- [ ] Docker Compose for full local stack (app + DB + Redis)
- [ ] Production Dockerfile with non-root user
- [ ] Container image size optimization (< 200MB)
- [ ] Environment-specific Docker Compose overrides

### 1.4 React Migration Decision Path
- [ ] **DECISION:** Migrate to React 19 + TypeScript or enhance vanilla JS?
- [ ] If React: Create `Dock/frontend-react/` Vite + React 19 + TypeScript project
- [ ] If React: `package.json` with `@orbit-ui/react`, Tailwind, React Router, Zustand, Lucide React
- [ ] If React: `tailwind.config.js` with orbit preset
- [ ] If React: `vite.config.ts` with proxy to backend API
- [ ] If React: `tsconfig.json` with strict mode
- [ ] If React: `index.html` with anti-FOUC + orbit-ui links
- [ ] If React: `main.tsx` with `ThemeProvider` wrapper
- [ ] If React: ESLint + Prettier configuration
- [ ] If React: Vitest + React Testing Library setup
- [ ] If React: Storybook for component development
- [ ] If vanilla: Modularize single-file SPA into ES modules
- [ ] If vanilla: Add build step (esbuild/Vite) for bundling
- [ ] If vanilla: Add TypeScript via JSDoc type annotations
- [ ] If vanilla: Add unit tests with Vitest or Jest (JSDOM)
- [ ] If vanilla: Extract CSS into separate files
- [ ] If vanilla: Add CSS minification pipeline
- [ ] If vanilla: Add JavaScript minification pipeline
- [ ] Parallel operation: keep both UIs while migrating
- [ ] Feature flag to toggle between old/new UI
- [ ] Migration completion criteria document

---

## 2. Design System Integration

### 2.1 Token Usage Audit
- [x] `orbit-tokens.css` loaded in `<head>`
- [x] Dark mode bootstrap script in `<head>` (localStorage + system preference)
- [ ] **ISSUE:** Custom CSS variables (`--bg`, `--bg-soft`, `--card`, etc.) override orbit tokens
- [ ] Replace `--bg: #07131a` with `var(--orbit-bg)` or equivalent token
- [ ] Replace `--bg-soft: #0d1f2a` with `var(--orbit-bg-soft)` token
- [ ] Replace `--card: #132431` with `var(--orbit-surface)` token
- [ ] Replace `--card-alt: #183243` with `var(--orbit-surface-alt)` token
- [ ] Replace `--text: #e4f8ff` with `var(--orbit-text)` token
- [ ] Replace `--muted: #8db6c7` with `var(--orbit-text-muted)` token
- [ ] Replace `--border: #2b4a5a` with `var(--orbit-border)` token
- [ ] Replace `--brand-a: #0ea5e9` with `var(--orbit-primary)` token
- [ ] Replace `--brand-b: #14b8a6` with `var(--orbit-secondary)` token
- [ ] Replace `--ok: #22c55e` with `var(--orbit-success)` token
- [ ] Replace `--warn: #f59e0b` with `var(--orbit-warning)` token
- [ ] Replace `--danger: #ef4444` with `var(--orbit-danger)` token
- [ ] Remove all hardcoded hex colors from inline `<style>`
- [ ] Audit every `background`, `color`, `border-color` for hardcoded values
- [ ] Replace hardcoded `#2d6278`, `#184055`, `#18374a` stat card colors with tokens
- [ ] Replace hardcoded `#2f657c`, `#173546` active nav colors with tokens
- [ ] Replace hardcoded `#32677f` side-note border with token
- [ ] Replace hardcoded `#275062` table border with token
- [ ] Replace hardcoded `rgba(...)` badge/overlay colors with token-based variants
- [ ] Replace hardcoded gradient backgrounds with token-based gradients

### 2.2 Typography Tokens
- [x] Font-family set to "RM Forma" with fallback
- [ ] Replace hardcoded `font-size: 15px` (brand h1) with `var(--orbit-text-sm)`
- [ ] Replace hardcoded `font-size: 11px` (brand p) with `var(--orbit-text-xs)`
- [ ] Replace hardcoded `font-size: 14px` (section head h2) with orbit token
- [ ] Replace hardcoded `font-size: 18px` (stat b) with orbit token
- [ ] Replace hardcoded `font-size: 12px` (table) with orbit token
- [ ] Replace hardcoded `letter-spacing: 0.02em` with orbit token
- [ ] Replace hardcoded `line-height: 1.5` with orbit token
- [ ] Use orbit font-weight tokens for `font-weight: 700` occurrences

### 2.3 Spacing & Layout Tokens
- [ ] Replace hardcoded `height: 66px` top bar with orbit token
- [ ] Replace hardcoded `padding: 0 14px` with orbit spacing
- [ ] Replace hardcoded `gap: 10px`, `gap: 8px`, `gap: 12px` with orbit spacing tokens
- [ ] Replace hardcoded `border-radius: 9px`, `10px`, `14px` with orbit radius tokens
- [ ] Replace hardcoded `margin-bottom: 7px` with orbit spacing
- [ ] Replace hardcoded `padding: 10px`, `8px`, `12px` with orbit spacing
- [ ] Replace `min-height: calc(100vh - 92px)` with CSS var or utility

### 2.4 Shadow & Effect Tokens
- [ ] Replace hardcoded `box-shadow: 0 10px 30px rgba(20, 184, 166, 0.28)` with orbit shadow
- [ ] Replace `backdrop-filter: blur(14px)` with orbit glass token
- [ ] Replace hardcoded focus ring styles with orbit focus token

### 2.5 Motion & Animation Tokens
- [ ] Add orbit transition tokens for hover states
- [ ] Add orbit transition tokens for modal open/close
- [ ] Add orbit transition tokens for sidebar collapse
- [ ] Add orbit transition tokens for tab switching
- [ ] Add loading skeleton animations using orbit motion tokens

### 2.6 Component Replacements (orbit-ui equivalents)
- [ ] Replace custom `.button` class with orbit Button component
- [ ] Replace custom `.button.primary` with orbit Button variant="primary"
- [ ] Replace custom `.button.warn` with orbit Button variant="warning"
- [ ] Replace custom `.button.danger` with orbit Button variant="danger"
- [ ] Replace custom `.input` class with orbit Input component
- [ ] Replace custom `.select` class with orbit Select component
- [ ] Replace custom `.textarea` class with orbit Textarea component
- [ ] Replace custom table styling with orbit Table component
- [ ] Replace custom `.stat` cards with orbit StatCard component
- [ ] Replace custom `.nav-item` with orbit NavItem component
- [ ] Replace custom `.side-note` with orbit Callout component
- [ ] Replace custom modal styling with orbit Modal/Dialog component
- [ ] Replace custom tooltip with orbit Tooltip component
- [ ] Replace custom badge/pill styling with orbit Badge component
- [ ] Replace custom dropdown with orbit DropdownMenu component
- [ ] Replace custom tabs with orbit Tabs component
- [ ] Replace custom toast/notification with orbit Toast component
- [ ] Replace custom card layout with orbit Card component
- [ ] Replace custom search input with orbit SearchInput component
- [ ] Replace custom avatar with orbit Avatar component

### 2.7 orbit-bar Integration
- [x] `orbit-bar.js` loaded with `defer`
- [ ] Verify orbit-bar renders correctly in all views
- [ ] Verify orbit-bar app switcher shows Dock as active
- [ ] Verify orbit-bar theme toggle syncs with Dock theme
- [ ] Verify orbit-bar notifications integration
- [ ] Verify orbit-bar user menu integration
- [ ] Verify orbit-bar search integration with Dock global search

---

## 3. Dark Mode

### 3.1 Theme Infrastructure
- [x] Dark mode bootstrap script in `<head>` (checks localStorage + system preference)
- [x] `.dark` class toggled on `<html>` element
- [ ] Verify `orbit-tokens.css` provides both light and dark token values
- [ ] Add theme toggle button in UI (beyond orbit-bar)
- [ ] Persist theme preference to user profile (backend)
- [ ] Sync theme preference across tabs (BroadcastChannel)
- [ ] Respect `prefers-color-scheme` media query for auto mode
- [ ] Add transition animation when switching themes
- [ ] Prevent flash of unstyled content (FOUC) on page load

### 3.2 Page/View Dark Mode Verification
- [ ] Top navigation bar — dark mode colors
- [ ] Sidebar navigation — dark mode colors
- [ ] Workspace main content area — dark mode colors
- [ ] Context panel (right sidebar) — dark mode colors
- [ ] App Catalog view — dark mode colors
- [ ] Licenses view — dark mode colors
- [ ] Assignments view — dark mode colors
- [ ] Requests view — dark mode colors
- [ ] Packages view — dark mode colors
- [ ] Audit Log view — dark mode colors
- [ ] Budget & Compliance view — dark mode colors
- [ ] Settings view — dark mode colors
- [ ] Dashboard/Overview view — dark mode colors
- [ ] Search results view — dark mode colors
- [ ] Quick actions menu — dark mode colors
- [ ] Notifications panel — dark mode colors
- [ ] User profile/preferences — dark mode colors

### 3.3 Component Dark Mode Verification
- [ ] Buttons (primary, secondary, warn, danger) — dark mode
- [ ] Input fields — dark mode backgrounds, borders, placeholder text
- [ ] Select dropdowns — dark mode
- [ ] Textarea — dark mode
- [ ] Tables — dark mode headers, rows, alternate row colors
- [ ] Stat cards — dark mode backgrounds, borders, text
- [ ] Navigation items — dark mode active/hover/inactive states
- [ ] Side notes / callouts — dark mode
- [ ] Modals/dialogs — dark mode overlay, background, text
- [ ] Tooltips — dark mode
- [ ] Badges/pills — dark mode
- [ ] Dropdown menus — dark mode
- [ ] Tabs — dark mode active/inactive
- [ ] Toast notifications — dark mode
- [ ] Cards — dark mode
- [ ] Search input — dark mode
- [ ] Avatar — dark mode
- [ ] Loading spinners — dark mode
- [ ] Empty states — dark mode
- [ ] Error states — dark mode
- [ ] Skeleton loaders — dark mode
- [ ] Scrollbar styling — dark mode
- [ ] Context menus — dark mode
- [ ] Breadcrumbs — dark mode
- [ ] Pagination — dark mode
- [ ] Progress bars — dark mode

### 3.4 Light Mode Verification
- [ ] **ISSUE:** Current CSS is dark-only (hardcoded dark colors in `:root`)
- [ ] Add light mode CSS variables
- [ ] Top navigation bar — light mode colors
- [ ] Sidebar navigation — light mode colors
- [ ] Workspace main content area — light mode colors
- [ ] Context panel — light mode colors
- [ ] All views listed in 3.2 — light mode
- [ ] All components listed in 3.3 — light mode
- [ ] Gradient backgrounds adapt to light mode
- [ ] Backdrop blur effects adapt to light mode
- [ ] Box shadows adapt to light mode

---

## 4. Core Features (Exhaustive)

### 4.1 Workspace Overview / Dashboard
- [ ] Dashboard layout: grid-based widget system
- [ ] Dashboard greeting: personalized "Good morning, [name]"
- [ ] Dashboard date/time display
- [ ] Dashboard quick stats row (total apps, active licenses, pending requests, active users)
- [ ] Dashboard recent activity feed
- [ ] Dashboard quick actions panel
- [ ] Dashboard system health indicators
- [ ] Dashboard org-level overview metrics
- [ ] Dashboard customizable widget grid
- [ ] Dashboard drag-and-drop widget repositioning
- [ ] Dashboard widget resize handles
- [ ] Dashboard widget add/remove gallery
- [ ] Dashboard widget settings per widget
- [ ] Dashboard layout presets (compact, focus, overview)
- [ ] Dashboard layout save/restore
- [ ] Dashboard layout per-user persistence
- [ ] Dashboard auto-refresh interval setting
- [ ] Dashboard manual refresh button

### 4.2 App Launcher / App Catalog
- [x] App catalog CRUD (backend: DockApp model)
- [x] App listing with name, vendor, description, URL
- [x] App license model field (per_user, etc.)
- [x] App integrations list (JSONB)
- [x] App advertised/hidden toggle
- [x] Create new app entry
- [x] Update app entry
- [x] Delete app entry
- [ ] App catalog card grid view
- [ ] App catalog list view toggle
- [ ] App catalog search/filter
- [ ] App catalog category filtering
- [ ] App catalog vendor filtering
- [ ] App catalog sort (name, date, vendor)
- [ ] App icon/logo upload
- [ ] App icon/logo display
- [ ] App detail modal/page
- [ ] App launch button (opens URL)
- [ ] App quick-launch favorites bar
- [ ] App recently used sorting
- [ ] App usage frequency tracking
- [ ] Most used apps pinned to top
- [ ] App catalog empty state

### 4.3 License Management
- [x] License CRUD (backend: License model)
- [x] License seats_purchased / seats_assigned tracking
- [x] License currency and total_cost
- [x] License renewal_date
- [x] License status (active, pending_finance_approval)
- [ ] License list view with search/filter
- [ ] License detail view
- [ ] License create form with validation
- [ ] License edit form
- [ ] License renewal reminder notifications
- [ ] License utilization chart (assigned vs purchased seats)
- [ ] License cost summary by vendor
- [ ] License cost summary by department
- [ ] License expiry calendar view
- [ ] License bulk import (CSV)
- [ ] License export (CSV/PDF)
- [ ] License cost trend chart
- [ ] License auto-renewal toggle
- [ ] License approval workflow integration

### 4.4 App Assignment Management
- [x] Assignment CRUD (backend: Assignment model)
- [x] Assignment user_id and access_level
- [x] Assignment status (active, revoked)
- [x] Assignment audit trail (assigned_by)
- [ ] Assignment list view with search/filter
- [ ] Assignment detail view
- [ ] Assignment create form (assign app to user)
- [ ] Assignment bulk assign (multiple users)
- [ ] Assignment revoke action with confirmation
- [ ] Assignment access level change
- [ ] Assignment history per user
- [ ] Assignment history per app
- [ ] Self-service assignment request flow
- [ ] Assignment notification to assigned user
- [ ] Assignment notification to admin on bulk operations

### 4.5 Request Management / Procurement
- [x] Request CRUD (backend: DockRequest model)
- [x] Request status workflow (pending, under_review, approved, rejected, provisioned)
- [x] Request reason and business justification
- [x] Request requested_seats
- [x] Request review_notes and reviewer_user_id
- [x] Request automation_ticket_id (TurboTick integration)
- [x] Request automation_status and automation_hint
- [ ] Request list view with search/filter/status tabs
- [ ] Request detail view
- [ ] Request create form with validation
- [ ] Request approval workflow UI
- [ ] Request approval email notifications
- [ ] Request rejection with reason
- [ ] Request auto-provisioning flow
- [ ] Request linked_app_id post-approval
- [ ] Request timeline/history view
- [ ] Request comments/discussion thread
- [ ] Request SLA tracking (time to approval)
- [ ] Request dashboard for managers
- [ ] Request bulk approval/rejection

### 4.6 Package Management
- [x] Package model (backend: DockPackage)
- [x] Package name, description, version, s3_key, size_bytes, checksum
- [ ] Package list view
- [ ] Package upload UI
- [ ] Package version history
- [ ] Package download link
- [ ] Package checksum verification
- [ ] Package auto-update mechanism
- [ ] Package rollback capability
- [ ] Package dependency tracking
- [ ] Package deployment status per app

### 4.7 Budget & Compliance
- [x] BudgetPolicy model (backend: monthly_limit, currency, alert_threshold_pct, department_id)
- [x] ProcurementConfig model (backend: require_manager_approval, auto_approve_threshold)
- [ ] Budget policy list view
- [ ] Budget policy create/edit form
- [ ] Budget policy per-department configuration
- [ ] Budget utilization chart (spent vs limit)
- [ ] Budget alert threshold notifications
- [ ] Budget overspend blocking or warning
- [ ] Procurement config admin UI
- [ ] Procurement auto-approve threshold UI
- [ ] Procurement manager approval toggle UI
- [ ] Compliance dashboard
- [ ] Compliance report generation
- [ ] Compliance policy violations list
- [ ] Budget forecast chart

### 4.8 Audit Log
- [x] AuditEvent model (backend: event_type, org_id, user_id, role, resource_type, resource_id, request_id, metadata_json)
- [x] Audit logging in all CRUD operations
- [ ] Audit log list view with filtering
- [ ] Audit log search by event type
- [ ] Audit log search by user
- [ ] Audit log search by resource
- [ ] Audit log search by date range
- [ ] Audit log detail view
- [ ] Audit log export (CSV/JSON)
- [ ] Audit log retention policy
- [ ] Audit log real-time streaming (SSE/WebSocket)
- [ ] Audit log anomaly detection alerts

### 4.9 Quick Actions
- [ ] Quick action: Create new app entry
- [ ] Quick action: Assign app to user
- [ ] Quick action: Submit procurement request
- [ ] Quick action: Approve pending request
- [ ] Quick action: View audit log
- [ ] Quick action: Generate report
- [ ] Quick action: Search across all data
- [ ] Quick action: Open app catalog
- [ ] Quick action: View budget status
- [ ] Quick actions panel in dashboard
- [ ] Quick actions keyboard shortcut (Cmd+K / Ctrl+K)
- [ ] Quick actions command palette

### 4.10 Recent Activity Feed
- [ ] Activity feed showing latest audit events
- [ ] Activity feed filtering by event type
- [ ] Activity feed real-time updates (SSE)
- [ ] Activity feed user avatars
- [ ] Activity feed time-relative timestamps ("2 min ago")
- [ ] Activity feed grouped by date
- [ ] Activity feed load more / infinite scroll
- [ ] Activity feed empty state

### 4.11 Bookmarks / Favorites
- [ ] Favorite apps pinning
- [ ] Favorite apps reorder (drag and drop)
- [ ] Favorite apps quick-access bar
- [ ] Favorite apps per-user persistence
- [ ] Favorite views/pages bookmarking
- [ ] Recently visited pages list

### 4.12 Widgets
- [ ] Widget: Clock with timezone display
- [ ] Widget: Weather (location-based)
- [ ] Widget: Quick notes capture
- [ ] Widget: Task list (local or from Atlas)
- [ ] Widget: Calendar preview (from Calendar app)
- [ ] Widget: Unread emails count (from Mail app)
- [ ] Widget: Upcoming meetings (from Meet/Calendar)
- [ ] Widget: Team activity feed (from Connect + EventBus)
- [ ] Widget: Open deals (from Planet CRM)
- [ ] Widget: AI Daily Briefing
- [ ] Widget: Notifications center
- [ ] Widget: App usage statistics
- [ ] Widget: Budget summary
- [ ] Widget: License utilization
- [ ] Widget: System health status
- [ ] Widget gallery for adding/removing widgets
- [ ] Widget drag-and-drop placement
- [ ] Widget resize capability
- [ ] Widget settings per instance
- [ ] Widget refresh interval per widget
- [ ] Widget loading states
- [ ] Widget error states with retry

### 4.13 Workspace Settings
- [ ] Workspace name and description
- [ ] Workspace branding (logo, colors)
- [ ] Workspace default landing page
- [ ] Workspace default widget layout
- [ ] Workspace notification preferences
- [ ] Workspace timezone setting
- [ ] Workspace language setting
- [ ] Workspace data retention policy
- [ ] Workspace audit log retention

### 4.14 Organization Management
- [ ] Org info display (name, plan, members)
- [ ] Org member list
- [ ] Org member roles (admin, manager, member)
- [ ] Org member invite
- [ ] Org member remove
- [ ] Org settings page
- [ ] Org billing overview link
- [ ] Org departments management
- [ ] Org teams management

### 4.15 User Preferences
- [ ] User display name
- [ ] User avatar
- [ ] User timezone preference
- [ ] User language preference
- [ ] User notification preferences (email, push, in-app)
- [ ] User dashboard layout preference
- [ ] User theme preference (light/dark/auto)
- [ ] User keyboard shortcut customization
- [ ] User session management (view active sessions)
- [ ] User connected apps/integrations

### 4.16 Global Search
- [ ] Search bar in top navigation
- [ ] Search across apps catalog
- [ ] Search across licenses
- [ ] Search across assignments
- [ ] Search across requests
- [ ] Search across audit logs
- [ ] Search across packages
- [ ] Search results grouped by category
- [ ] Search results highlighting
- [ ] Search recent queries history
- [ ] Search keyboard shortcut (Cmd+Space or Cmd+K)
- [ ] Search suggestions/autocomplete
- [ ] Cross-app search (Atlas tasks, Mail, Calendar, etc.)

### 4.17 Notifications Hub
- [ ] In-app notification bell icon with unread count
- [ ] Notification dropdown panel
- [ ] Notification types: request approved/rejected, license expiring, budget alert
- [ ] Notification mark as read/unread
- [ ] Notification mark all as read
- [ ] Notification click-through to related resource
- [ ] Notification preferences per type
- [ ] Notification real-time delivery (SSE/WebSocket)
- [ ] Notification sound toggle
- [ ] Push notification support (if PWA)
- [ ] Email notification digest (daily/weekly)

### 4.18 File Manager
- [ ] File manager view for package artifacts
- [ ] File upload drag-and-drop
- [ ] File download with checksum verification
- [ ] File version history
- [ ] File size display
- [ ] File type icons
- [ ] File search
- [ ] File preview (images, PDFs)
- [ ] File delete with confirmation
- [ ] File bulk operations

### 4.19 Keyboard Shortcuts
- [ ] `Cmd+K` / `Ctrl+K` — command palette
- [ ] `Cmd+Space` — global search
- [ ] `/` — focus search from anywhere
- [ ] `Cmd+N` — new app / new request
- [ ] `Cmd+,` — open settings
- [ ] `?` — show keyboard shortcuts help
- [ ] `Esc` — close modal/panel
- [ ] `Tab` / `Shift+Tab` — navigate between sections
- [ ] Arrow keys — navigate lists
- [ ] `Enter` — select/open item
- [ ] `Cmd+Shift+D` — toggle dark mode
- [ ] Keyboard shortcut help modal
- [ ] Keyboard shortcut customization

---

## 5. API Integration

### 5.1 Backend API Endpoints (Existing)
- [x] `GET /api/dock/apps` — list apps
- [x] `POST /api/dock/apps` — create app
- [x] `PATCH /api/dock/apps/{id}` — update app
- [x] `DELETE /api/dock/apps/{id}` — delete app
- [x] `GET /api/dock/licenses` — list licenses
- [x] `POST /api/dock/licenses` — create license
- [x] `GET /api/dock/assignments` — list assignments
- [x] `POST /api/dock/assignments` — create assignment
- [x] `PATCH /api/dock/assignments/{id}` — update assignment
- [x] `GET /api/dock/requests` — list requests
- [x] `POST /api/dock/requests` — create request
- [x] `PATCH /api/dock/requests/{id}` — update request
- [x] `GET /api/dock/audit` — list audit events
- [x] `GET /api/dock/budget-policies` — list budget policies
- [x] `POST /api/dock/budget-policies` — create budget policy
- [x] `GET /api/dock/procurement-config` — get procurement config
- [x] `PUT /api/dock/procurement-config` — upsert procurement config
- [x] `GET /health` — health check

### 5.2 Frontend-Backend API Wiring
- [ ] Wire app catalog list to `GET /api/dock/apps`
- [ ] Wire app create form to `POST /api/dock/apps`
- [ ] Wire app update form to `PATCH /api/dock/apps/{id}`
- [ ] Wire app delete action to `DELETE /api/dock/apps/{id}`
- [ ] Wire license list to `GET /api/dock/licenses`
- [ ] Wire license create form to `POST /api/dock/licenses`
- [ ] Wire assignment list to `GET /api/dock/assignments`
- [ ] Wire assignment create to `POST /api/dock/assignments`
- [ ] Wire assignment update to `PATCH /api/dock/assignments/{id}`
- [ ] Wire request list to `GET /api/dock/requests`
- [ ] Wire request create form to `POST /api/dock/requests`
- [ ] Wire request approval to `PATCH /api/dock/requests/{id}`
- [ ] Wire audit log list to `GET /api/dock/audit`
- [ ] Wire budget policy list to `GET /api/dock/budget-policies`
- [ ] Wire budget policy create to `POST /api/dock/budget-policies`
- [ ] Wire procurement config to `GET/PUT /api/dock/procurement-config`
- [ ] Add API error handling with user-friendly messages
- [ ] Add API retry logic for transient failures
- [ ] Add API request timeout handling
- [ ] Add API response caching where appropriate

### 5.3 Cross-App API Integration
- [ ] Pull task data from Atlas API
- [ ] Pull email counts from Mail API
- [ ] Pull events from Calendar API
- [ ] Pull deal data from Planet CRM API
- [ ] Subscribe to EventBus SSE for live updates
- [ ] Unified notification center from EventBus
- [ ] Cross-app action: create task from email
- [ ] Cross-app action: schedule meeting from task
- [ ] TurboTick integration for request automation
- [ ] Gate OIDC integration for authentication
- [ ] Secure bridge integration for assignment sync

### 5.4 Authentication & Authorization
- [x] Gate OIDC Bearer token validation (backend)
- [x] Header-based auth fallback (X-Org-Id, X-User-Id, X-User-Role)
- [x] Hybrid auth mode (Gate + headers)
- [x] Role-based access control (admin, manager, member)
- [ ] Frontend token storage (localStorage/sessionStorage)
- [ ] Frontend token refresh flow
- [ ] Frontend auth state management
- [ ] Frontend login redirect to Gate
- [ ] Frontend logout flow
- [ ] Frontend session timeout handling
- [ ] Frontend unauthorized error handling (401 redirect)
- [ ] Frontend forbidden error handling (403 message)
- [ ] RBAC enforcement in UI (hide admin-only features for members)

### 5.5 API Client Layer
- [ ] Centralized fetch/axios wrapper
- [ ] Request interceptor for auth headers
- [ ] Response interceptor for error handling
- [ ] API client type definitions
- [ ] API client request/response logging (dev mode)
- [ ] API client request deduplication
- [ ] API client request cancellation (AbortController)
- [ ] OpenAPI spec generation from backend
- [ ] API client code generation from OpenAPI spec

---

## 6. State Management

### 6.1 Current State (Vanilla JS)
- [ ] Audit current state management approach in index.html
- [ ] Identify all global state variables
- [ ] Identify all DOM manipulation patterns
- [ ] Identify all event listener registrations

### 6.2 State Architecture (if React migration)
- [ ] Zustand store for app catalog state
- [ ] Zustand store for license state
- [ ] Zustand store for assignment state
- [ ] Zustand store for request state
- [ ] Zustand store for audit log state
- [ ] Zustand store for budget/compliance state
- [ ] Zustand store for user/auth state
- [ ] Zustand store for UI state (sidebar open, active tab, etc.)
- [ ] Zustand store for notification state
- [ ] Zustand store for search state
- [ ] Zustand store for widget layout state
- [ ] Zustand middleware for localStorage persistence
- [ ] Zustand middleware for devtools
- [ ] React Query / TanStack Query for server state
- [ ] Query key naming conventions
- [ ] Optimistic updates for mutations
- [ ] Cache invalidation strategy

### 6.3 State Architecture (if vanilla JS enhancement)
- [ ] Create event-driven state management (pub/sub)
- [ ] Centralized state store object
- [ ] State change listeners for DOM updates
- [ ] LocalStorage persistence for user preferences
- [ ] SessionStorage for session-specific state
- [ ] URL state (hash routing or query params)

---

## 7. Performance

### 7.1 Frontend Performance
- [ ] Measure initial page load time (target < 2s)
- [ ] Measure Time to First Byte (TTFB)
- [ ] Measure First Contentful Paint (FCP)
- [ ] Measure Largest Contentful Paint (LCP < 2.5s)
- [ ] Measure Cumulative Layout Shift (CLS < 0.1)
- [ ] Measure First Input Delay (FID < 100ms)
- [ ] Measure Interaction to Next Paint (INP < 200ms)
- [ ] Bundle size audit (if build step added)
- [ ] Code splitting / lazy loading for views
- [ ] Image optimization (WebP, lazy loading)
- [ ] Font loading optimization (font-display: swap)
- [ ] CSS optimization (remove unused CSS)
- [ ] JavaScript optimization (minify, tree-shake)
- [ ] Gzip/Brotli compression
- [ ] CDN for static assets
- [ ] Browser caching headers (Cache-Control, ETag)
- [ ] Preload critical resources
- [ ] Prefetch likely next pages
- [ ] Reduce DOM size (target < 1500 nodes)
- [ ] Debounce search input
- [ ] Virtualize long lists (audit log, app catalog)
- [ ] Skeleton loading screens
- [ ] Progressive image loading

### 7.2 Backend Performance
- [ ] Database query optimization (N+1 query detection)
- [ ] Database connection pooling configuration
- [ ] Database index analysis
- [ ] API response time monitoring (target < 200ms p95)
- [ ] API pagination for list endpoints
- [ ] API response compression
- [ ] Redis caching for frequently accessed data
- [ ] Background task processing (Celery/ARQ)
- [ ] Rate limiting per endpoint
- [ ] Request payload size limits
- [ ] Database query timeout limits
- [ ] Slow query logging

### 7.3 Real-Time Performance
- [ ] SSE connection management
- [ ] WebSocket connection pooling (if used)
- [ ] Event debouncing/throttling
- [ ] Reconnection logic with exponential backoff

---

## 8. Accessibility

### 8.1 WCAG 2.1 AA Compliance
- [ ] All interactive elements keyboard accessible
- [ ] Tab order is logical and follows visual order
- [ ] Focus indicators visible on all interactive elements
- [ ] Focus trap in modals/dialogs
- [ ] Skip navigation link
- [ ] Landmark roles (header, nav, main, aside, footer)
- [ ] Heading hierarchy (h1 > h2 > h3, no skips)
- [ ] Alt text for all images
- [ ] ARIA labels for icon-only buttons
- [ ] ARIA labels for custom controls
- [ ] ARIA live regions for dynamic content
- [ ] ARIA expanded/collapsed states for accordions
- [ ] ARIA selected states for tabs
- [ ] ARIA sort states for table columns
- [ ] Color contrast ratio >= 4.5:1 for text
- [ ] Color contrast ratio >= 3:1 for large text
- [ ] Color contrast ratio >= 3:1 for UI components
- [ ] Information not conveyed by color alone
- [ ] Form inputs have associated labels
- [ ] Form error messages linked to inputs (aria-describedby)
- [ ] Required fields indicated (aria-required)
- [ ] Error states announced to screen readers
- [ ] Success messages announced to screen readers
- [ ] Loading states announced to screen readers

### 8.2 Screen Reader Testing
- [ ] Test with NVDA on Windows
- [ ] Test with VoiceOver on macOS
- [ ] Test with JAWS on Windows
- [ ] Test with TalkBack on Android
- [ ] Test with VoiceOver on iOS/iPadOS
- [ ] Verify all page titles are descriptive
- [ ] Verify all links have descriptive text
- [ ] Verify all buttons have descriptive text
- [ ] Verify data tables are properly structured (th, scope)

### 8.3 Motion & Visual Preferences
- [ ] Respect `prefers-reduced-motion`
- [ ] Respect `prefers-contrast`
- [ ] Respect `prefers-color-scheme`
- [ ] No auto-playing animations without user control
- [ ] No content that flashes more than 3 times per second

---

## 9. Mobile & Responsive

### 9.1 Breakpoint System
- [ ] Mobile: 0-639px (sm)
- [ ] Tablet: 640-1023px (md)
- [ ] Desktop: 1024-1279px (lg)
- [ ] Wide: 1280px+ (xl)
- [ ] Test at each breakpoint

### 9.2 Layout Responsive Behavior
- [ ] Top navigation: hamburger menu on mobile
- [ ] Sidebar: collapsible drawer on mobile/tablet
- [ ] Three-column layout: stack on mobile, two columns on tablet
- [ ] Context panel: bottom sheet or collapsible on mobile
- [ ] Stat cards: 2-column on tablet, 1-column on mobile
- [ ] Table: horizontal scroll or card layout on mobile
- [ ] Toolbar: stack controls vertically on mobile
- [ ] Modal: full-screen on mobile
- [ ] Widget grid: single column on mobile

### 9.3 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] Swipe to dismiss notifications
- [ ] Pull to refresh
- [ ] Long press for context menu
- [ ] Pinch to zoom on charts/widgets
- [ ] Touch-friendly drag and drop (widget reorder)

### 9.4 Mobile-Specific Features
- [ ] PWA installable (Add to Home Screen)
- [ ] Offline indicator banner
- [ ] Mobile-optimized navigation (bottom tabs)
- [ ] Mobile-optimized quick actions
- [ ] Viewport height handling (100dvh)
- [ ] Safe area insets (notch/rounded corners)
- [ ] Input zoom prevention on iOS (font-size >= 16px)
- [ ] Virtual keyboard handling

---

## 10. Internationalization (i18n)

### 10.1 Infrastructure
- [ ] i18n library selection (i18next, or vanilla approach)
- [ ] Translation file structure (`/locales/en.json`, etc.)
- [ ] Default language: English (en)
- [ ] Language detection from browser/user preference
- [ ] Language switcher UI
- [ ] Language persistence (localStorage + user profile)

### 10.2 String Extraction
- [ ] Extract all UI strings from index.html
- [ ] Extract button labels
- [ ] Extract navigation labels
- [ ] Extract form labels and placeholders
- [ ] Extract error messages
- [ ] Extract success messages
- [ ] Extract empty state messages
- [ ] Extract tooltip text
- [ ] Extract ARIA labels
- [ ] Extract date/time format strings
- [ ] Extract number format strings
- [ ] Extract currency format strings

### 10.3 Locale Support
- [ ] English (en) — complete
- [ ] Spanish (es) — translation
- [ ] French (fr) — translation
- [ ] German (de) — translation
- [ ] Japanese (ja) — translation
- [ ] Chinese Simplified (zh-CN) — translation
- [ ] Arabic (ar) — RTL support
- [ ] Hindi (hi) — translation

### 10.4 RTL Support
- [ ] CSS logical properties (margin-inline-start, etc.)
- [ ] RTL layout testing
- [ ] Bidirectional text handling
- [ ] Icon mirroring for directional icons

### 10.5 Date/Time/Number Formatting
- [ ] Date formatting per locale (Intl.DateTimeFormat)
- [ ] Time formatting per locale
- [ ] Number formatting per locale (Intl.NumberFormat)
- [ ] Currency formatting per locale
- [ ] Relative time formatting ("2 hours ago")
- [ ] Timezone display per user preference

---

## 11. Security

### 11.1 Authentication Security
- [x] Gate OIDC Bearer token validation
- [x] Token forwarding to backend
- [ ] Token storage: HttpOnly cookie preferred over localStorage
- [ ] CSRF protection (SameSite cookies or CSRF tokens)
- [ ] Session timeout and auto-logout
- [ ] Concurrent session detection
- [ ] Brute force protection (rate limiting on login)
- [ ] Account lockout after failed attempts

### 11.2 Authorization Security
- [x] Role-based access control (admin/manager/member)
- [x] Org-scoped data isolation
- [ ] Frontend route guards
- [ ] Backend permission checks on every endpoint
- [ ] Principle of least privilege enforcement
- [ ] Admin-only endpoint protection
- [ ] Cross-org data access prevention

### 11.3 Input Security
- [ ] Input sanitization (XSS prevention)
- [ ] Output encoding (HTML entity encoding)
- [ ] SQL injection prevention (parameterized queries — handled by SQLAlchemy)
- [ ] SSRF prevention (validate URLs in DockApp.url)
- [ ] File upload validation (type, size, content)
- [ ] Content-Type validation on API requests
- [ ] Request body size limits

### 11.4 Network Security
- [ ] HTTPS enforcement
- [ ] HSTS headers
- [ ] Content Security Policy (CSP) headers
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] X-XSS-Protection header
- [ ] Referrer-Policy header
- [ ] Permissions-Policy header
- [ ] CORS configuration (restrict origins)
- [ ] Subresource Integrity (SRI) for CDN resources

### 11.5 Data Security
- [ ] Sensitive data encryption at rest
- [ ] Sensitive data encryption in transit (TLS 1.2+)
- [ ] PII masking in logs
- [ ] Audit log tamper protection
- [ ] Database encryption (PostgreSQL TDE or application-level)
- [ ] Backup encryption
- [ ] Secret management (no hardcoded secrets)

### 11.6 Dependency Security
- [ ] Python dependency vulnerability scanning (pip-audit)
- [ ] JavaScript dependency vulnerability scanning (npm audit)
- [ ] Automated dependency updates (Dependabot/Renovate)
- [ ] Lock file integrity verification
- [ ] Supply chain security (package provenance)

---

## 12. Testing

### 12.1 Backend Unit Tests
- [x] `tests/test_api.py` — API endpoint tests
- [x] `tests/test_secure_sync_helpers.py` — Secure bridge helper tests
- [ ] Test: Create DockApp — valid input
- [ ] Test: Create DockApp — duplicate name
- [ ] Test: Create DockApp — invalid input (empty name)
- [ ] Test: Update DockApp — valid input
- [ ] Test: Update DockApp — non-existent ID
- [ ] Test: Delete DockApp — existing
- [ ] Test: Delete DockApp — non-existent
- [ ] Test: List DockApps — empty
- [ ] Test: List DockApps — with data
- [ ] Test: List DockApps — org isolation
- [ ] Test: Create License — valid input
- [ ] Test: Create License — invalid app_id
- [ ] Test: Create License — zero seats
- [ ] Test: List Licenses — by org
- [ ] Test: Create Assignment — valid input
- [ ] Test: Create Assignment — duplicate user+app
- [ ] Test: Update Assignment — revoke
- [ ] Test: List Assignments — by org
- [ ] Test: List Assignments — by user
- [ ] Test: Create Request — valid input
- [ ] Test: Create Request — missing reason
- [ ] Test: Update Request — approve
- [ ] Test: Update Request — reject
- [ ] Test: Update Request — invalid status transition
- [ ] Test: List Requests — by status
- [ ] Test: Create BudgetPolicy — valid input
- [ ] Test: Create BudgetPolicy — negative limit
- [ ] Test: Upsert ProcurementConfig — create
- [ ] Test: Upsert ProcurementConfig — update
- [ ] Test: Audit events — logged on create
- [ ] Test: Audit events — logged on update
- [ ] Test: Audit events — logged on delete
- [ ] Test: Audit events — list by org
- [ ] Test: Audit events — list by event type
- [ ] Test: Auth — Gate Bearer token validation
- [ ] Test: Auth — header fallback
- [ ] Test: Auth — missing auth
- [ ] Test: Auth — invalid token
- [ ] Test: Auth — role normalization
- [ ] Test: RBAC — admin can create apps
- [ ] Test: RBAC — member cannot delete apps
- [ ] Test: RBAC — manager can approve requests
- [ ] Test: Health endpoint returns 200

### 12.2 Backend Integration Tests
- [ ] Test: Full request lifecycle (create -> review -> approve -> provision)
- [ ] Test: License and assignment flow (create license -> assign user)
- [ ] Test: Budget enforcement (request exceeds budget)
- [ ] Test: TurboTick automation trigger
- [ ] Test: Secure bridge sync
- [ ] Test: Database migration up/down
- [ ] Test: API with real PostgreSQL (docker-compose)

### 12.3 Frontend Unit Tests
- [ ] Test: App catalog rendering
- [ ] Test: App search filtering
- [ ] Test: License form validation
- [ ] Test: Assignment form validation
- [ ] Test: Request form validation
- [ ] Test: Theme toggle
- [ ] Test: Navigation state
- [ ] Test: Quick actions menu
- [ ] Test: Notification rendering
- [ ] Test: Date/time formatting
- [ ] Test: Currency formatting
- [ ] Test: Empty state rendering
- [ ] Test: Error state rendering
- [ ] Test: Loading state rendering

### 12.4 End-to-End Tests
- [ ] E2E: Login flow
- [ ] E2E: Browse app catalog
- [ ] E2E: Create new app
- [ ] E2E: Assign app to user
- [ ] E2E: Submit procurement request
- [ ] E2E: Approve procurement request
- [ ] E2E: View audit log
- [ ] E2E: Configure budget policy
- [ ] E2E: Search across apps
- [ ] E2E: Toggle dark mode
- [ ] E2E: Responsive layout (mobile viewport)
- [ ] E2E: Keyboard navigation
- [ ] E2E test framework setup (Playwright)
- [ ] E2E test CI pipeline

### 12.5 Performance Tests
- [ ] Load test: Concurrent API requests
- [ ] Load test: Large app catalog (1000+ apps)
- [ ] Load test: Large audit log (100K+ events)
- [ ] Lighthouse CI for performance scoring
- [ ] Bundle size regression tests

### 12.6 Visual Regression Tests
- [ ] Visual test: Dashboard view
- [ ] Visual test: App catalog view
- [ ] Visual test: License list view
- [ ] Visual test: Audit log view
- [ ] Visual test: Dark mode
- [ ] Visual test: Light mode
- [ ] Visual test: Mobile layout
- [ ] Chromatic or Percy integration

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] Backend: docstrings on all route handlers
- [ ] Backend: docstrings on all model classes
- [ ] Backend: docstrings on all utility functions
- [ ] Backend: README.md with setup instructions
- [ ] Frontend: JSDoc comments on all functions
- [ ] Frontend: README.md with setup instructions
- [ ] Architecture decision records (ADRs)
- [ ] Data model diagram
- [ ] API flow diagrams

### 13.2 API Documentation
- [x] FastAPI auto-generated OpenAPI docs (`/docs`)
- [ ] API authentication guide
- [ ] API rate limiting documentation
- [ ] API error codes reference
- [ ] API versioning strategy documentation
- [ ] Postman/Insomnia collection
- [ ] API changelog

### 13.3 User Documentation
- [ ] Getting started guide
- [ ] App catalog management guide
- [ ] License management guide
- [ ] Procurement request guide
- [ ] Budget policy configuration guide
- [ ] Audit log usage guide
- [ ] Keyboard shortcuts reference
- [ ] FAQ
- [ ] Video tutorials / walkthroughs

### 13.4 Operations Documentation
- [ ] Deployment guide
- [ ] Environment variables reference
- [ ] Database migration guide
- [ ] Monitoring and alerting guide
- [ ] Incident response runbook
- [ ] Backup and recovery guide
- [ ] Scaling guide

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [ ] GitHub Actions / GitLab CI workflow
- [ ] Lint Python code (ruff/flake8)
- [ ] Type check Python code (mypy)
- [ ] Run backend unit tests
- [ ] Run backend integration tests
- [ ] Lint frontend code (ESLint if React)
- [ ] Run frontend tests
- [ ] Build frontend assets
- [ ] Docker image build
- [ ] Docker image push to registry
- [ ] Security scanning (Snyk/Trivy)
- [ ] License compliance check
- [ ] Lighthouse CI scores

### 14.2 CD Pipeline
- [ ] Staging environment auto-deploy on merge
- [ ] Production deploy with manual approval
- [ ] Blue/green deployment strategy
- [ ] Canary deployment option
- [ ] Rollback automation
- [ ] Database migration as part of deploy
- [ ] Health check verification post-deploy
- [ ] Smoke test suite post-deploy
- [ ] Deployment notification (Slack/email)

### 14.3 Environment Configuration
- [ ] Development environment setup docs
- [ ] Staging environment configuration
- [ ] Production environment configuration
- [ ] Environment variable validation on startup
- [ ] Secret management (Vault/AWS Secrets Manager)
- [ ] Feature flags system

### 14.4 Monitoring & Observability
- [ ] Application performance monitoring (APM)
- [ ] Error tracking (Sentry)
- [ ] Structured logging (JSON format)
- [ ] Request tracing (correlation IDs)
- [ ] Metrics endpoint (Prometheus)
- [ ] Grafana dashboards
- [ ] Alerting rules (PagerDuty/OpsGenie)
- [ ] Uptime monitoring
- [ ] Database monitoring
- [ ] Log aggregation (ELK/Loki)

---

## 15. Backend

### 15.1 Database & Models
- [x] DockApp model — app catalog entries
- [x] License model — seat-based licenses
- [x] Assignment model — user-to-app assignments
- [x] DockRequest model — procurement requests with workflow
- [x] DockPackage model — software packages with S3 storage
- [x] DockAuditEvent model — full audit trail
- [x] BudgetPolicy model — department budget limits
- [x] ProcurementConfig model — org-level procurement settings
- [x] Alembic migrations for all models
- [ ] Database seed script for development
- [ ] Database indexes review and optimization
- [ ] Database foreign key constraints audit
- [ ] Database NOT NULL constraints audit
- [ ] Database default values audit
- [ ] Soft delete support (is_deleted flag)
- [ ] Updated_at auto-update trigger
- [ ] Database backup automation
- [ ] Database point-in-time recovery
- [ ] Read replica configuration (if needed)

### 15.2 API Architecture
- [x] FastAPI router with prefix `/api/dock`
- [x] Pydantic request/response models
- [x] SQLAlchemy ORM for database access
- [x] Dependency injection for auth (get_actor_dependency)
- [x] Dependency injection for database sessions
- [ ] API versioning (v1, v2)
- [ ] API pagination (cursor-based)
- [ ] API sorting (field + direction)
- [ ] API filtering (query params)
- [ ] API field selection (sparse fieldsets)
- [ ] API bulk operations
- [ ] API rate limiting middleware
- [ ] API request validation (Pydantic v2)
- [ ] API response serialization consistency
- [ ] API error response format standardization
- [ ] Background task queue (Celery/ARQ)
- [ ] Webhook delivery for external integrations
- [ ] OpenAPI spec customization

### 15.3 Authentication & Authorization (Backend)
- [x] Gate OIDC userinfo validation
- [x] Header-based auth (X-Org-Id, X-User-Id, X-User-Role)
- [x] Hybrid auth mode
- [x] Role-based access (admin, manager, member)
- [x] Org-scoped data queries
- [ ] Token refresh mechanism
- [ ] Token revocation check
- [ ] Permission matrix documentation
- [ ] Scope-based authorization (beyond roles)
- [ ] API key support for service-to-service calls
- [ ] IP whitelisting for admin endpoints
- [ ] Rate limiting per user/org

### 15.4 Cross-Service Communication
- [x] TurboTick integration (automation ticket creation)
- [x] Secure bridge integration (assignment sync)
- [x] Gate OIDC integration (token validation)
- [x] Event sink URL configuration (EventBus)
- [ ] EventBus event publishing
- [ ] Service mesh configuration
- [ ] Circuit breaker for external service calls
- [ ] Retry with exponential backoff
- [ ] Request timeout configuration
- [ ] Service discovery
- [ ] Health check dependencies on external services

### 15.5 Error Handling
- [ ] Global exception handler
- [ ] Structured error responses
- [ ] Error logging with context
- [ ] Error alerting for critical failures
- [ ] Graceful degradation when external services are down
- [ ] Database connection error recovery
- [ ] Transient error retry logic

### 15.6 Logging & Monitoring
- [ ] Structured JSON logging
- [ ] Request/response logging (sanitized)
- [ ] Slow query logging
- [ ] Error rate monitoring
- [ ] Prometheus metrics endpoint
- [ ] Custom business metrics (requests per day, approvals, etc.)
- [ ] Correlation ID propagation
- [ ] Log levels configurable per module
- [ ] Log rotation configuration

### 15.7 Data Integrity & Validation
- [x] Pydantic models with field validation (min/max length, ge/le)
- [x] Request status enum validation
- [x] Role enum validation
- [ ] Database constraint enforcement
- [ ] Data migration scripts for schema changes
- [ ] Data validation on import
- [ ] Orphan record cleanup
- [ ] Data consistency checks (scheduled)

### 15.8 Scalability
- [ ] Horizontal scaling support (stateless backend)
- [ ] Database connection pool tuning
- [ ] Caching layer (Redis)
- [ ] CDN for static assets
- [ ] API response caching with invalidation
- [ ] Background job processing
- [ ] Queue-based event processing
- [ ] Load balancer configuration
- [ ] Auto-scaling rules

---

## Appendix A: Dock-Specific Views & Pages Inventory

The following is a comprehensive list of every distinct view/page in Dock, used for cross-referencing dark mode, responsive, accessibility, and testing checklists:

1. Dashboard / Home
2. App Catalog (grid view)
3. App Catalog (list view)
4. App Detail Modal
5. App Create/Edit Form
6. License List
7. License Detail
8. License Create Form
9. Assignment List
10. Assignment Create Form
11. Assignment Detail
12. Request List (with status tabs)
13. Request Detail
14. Request Create Form
15. Request Approval Form
16. Package List
17. Package Upload
18. Package Detail
19. Audit Log List
20. Audit Log Detail
21. Budget Policy List
22. Budget Policy Create/Edit
23. Procurement Config
24. Compliance Dashboard
25. Settings — Workspace
26. Settings — Organization
27. Settings — User Preferences
28. Settings — Notifications
29. Global Search Results
30. Notification Panel
31. Widget Gallery
32. Widget Settings
33. Keyboard Shortcuts Help
34. Error Page (404)
35. Error Page (500)
36. Maintenance Page
37. Loading/Splash Screen
38. Empty States (per section)

---

## Appendix B: React Migration Component Inventory

If migrating to React, the following components would need to be created:

### Layout Components
- [ ] `AppLayout` — main layout shell
- [ ] `TopBar` — top navigation
- [ ] `Sidebar` — left navigation
- [ ] `ContextPanel` — right panel
- [ ] `PageHeader` — page title + breadcrumbs
- [ ] `PageContent` — main content area

### Feature Components
- [ ] `DashboardGrid` — widget grid layout
- [ ] `WidgetCard` — individual widget wrapper
- [ ] `AppCatalogGrid` — app card grid
- [ ] `AppCard` — individual app card
- [ ] `AppDetailModal` — app detail modal
- [ ] `LicenseTable` — license list table
- [ ] `AssignmentTable` — assignment list table
- [ ] `RequestList` — request list with status tabs
- [ ] `RequestDetailPanel` — request detail view
- [ ] `AuditLogTable` — audit log with filtering
- [ ] `BudgetChart` — budget utilization chart
- [ ] `SearchOverlay` — global search overlay
- [ ] `NotificationPanel` — notification dropdown
- [ ] `QuickActionsMenu` — command palette

### Form Components
- [ ] `AppForm` — create/edit app
- [ ] `LicenseForm` — create license
- [ ] `AssignmentForm` — assign app to user
- [ ] `RequestForm` — create procurement request
- [ ] `BudgetPolicyForm` — create/edit budget policy
- [ ] `ProcurementConfigForm` — procurement settings

### Shared Components
- [ ] `DataTable` — reusable sortable/filterable table
- [ ] `StatusBadge` — status pill component
- [ ] `EmptyState` — empty state illustration + text
- [ ] `ErrorBoundary` — React error boundary
- [ ] `LoadingSkeleton` — skeleton loader
- [ ] `ConfirmDialog` — confirmation modal
- [ ] `Pagination` — pagination controls
- [ ] `FilterBar` — search + filter controls

### Hook Library
- [ ] `useApps()` — app catalog CRUD
- [ ] `useLicenses()` — license CRUD
- [ ] `useAssignments()` — assignment CRUD
- [ ] `useRequests()` — request CRUD
- [ ] `useAuditLog()` — audit log queries
- [ ] `useBudgetPolicies()` — budget CRUD
- [ ] `useProcurementConfig()` — procurement config
- [ ] `useAuth()` — authentication state
- [ ] `useSearch()` — global search
- [ ] `useNotifications()` — notification state
- [ ] `useTheme()` — theme toggle
- [ ] `useKeyboardShortcuts()` — keyboard shortcut registration
- [ ] `useWidgetLayout()` — widget grid state
- [ ] `useDebounce()` — debounce utility
- [ ] `useMediaQuery()` — responsive breakpoint detection

---

## Appendix C: Detailed Test Scenarios

### C.1 App Catalog Test Scenarios
- [ ] Scenario: Admin creates app with all fields populated
- [ ] Scenario: Admin creates app with only required fields
- [ ] Scenario: Admin creates app with empty name (expect 422)
- [ ] Scenario: Admin creates app with name exactly 2 chars (boundary)
- [ ] Scenario: Admin creates app with name exactly 200 chars (boundary)
- [ ] Scenario: Admin creates app with name 201 chars (expect 422)
- [ ] Scenario: Admin creates app with description 2000 chars (boundary)
- [ ] Scenario: Admin creates app with description 2001 chars (expect 422)
- [ ] Scenario: Admin creates app with URL 4000 chars (boundary)
- [ ] Scenario: Admin creates app with URL 4001 chars (expect 422)
- [ ] Scenario: Admin creates app with invalid license_model
- [ ] Scenario: Admin creates app with empty integrations list
- [ ] Scenario: Admin creates app with populated integrations list
- [ ] Scenario: Admin updates app name only
- [ ] Scenario: Admin updates app vendor only
- [ ] Scenario: Admin updates app all fields
- [ ] Scenario: Admin updates non-existent app (expect 404)
- [ ] Scenario: Admin deletes existing app
- [ ] Scenario: Admin deletes non-existent app (expect 404)
- [ ] Scenario: Admin deletes app with active licenses (expect error or cascade)
- [ ] Scenario: Admin deletes app with active assignments (expect error or cascade)
- [ ] Scenario: Member creates app (expect 403 or allowed depending on policy)
- [ ] Scenario: Manager creates app (expect allowed)
- [ ] Scenario: List apps returns only current org apps
- [ ] Scenario: List apps from empty org (expect empty list)
- [ ] Scenario: List apps with 100+ entries (pagination)
- [ ] Scenario: Search apps by name substring
- [ ] Scenario: Filter apps by vendor
- [ ] Scenario: Filter apps by advertised status
- [ ] Scenario: Sort apps by name ascending
- [ ] Scenario: Sort apps by created_at descending

### C.2 License Management Test Scenarios
- [ ] Scenario: Admin creates license with valid app_id
- [ ] Scenario: Admin creates license with non-existent app_id (expect 404)
- [ ] Scenario: Admin creates license with 1 seat (boundary)
- [ ] Scenario: Admin creates license with 100000 seats (boundary)
- [ ] Scenario: Admin creates license with 100001 seats (expect 422)
- [ ] Scenario: Admin creates license with 0 seats (expect 422)
- [ ] Scenario: Admin creates license with negative cost (expect 422)
- [ ] Scenario: Admin creates license with various currencies (USD, EUR, GBP)
- [ ] Scenario: Admin creates license with renewal_date
- [ ] Scenario: List licenses returns only current org
- [ ] Scenario: License seats_assigned does not exceed seats_purchased
- [ ] Scenario: License status transitions (active -> pending_finance_approval)

### C.3 Assignment Management Test Scenarios
- [ ] Scenario: Admin assigns app to user
- [ ] Scenario: Admin assigns app to user with access_level "admin"
- [ ] Scenario: Admin assigns app to user with access_level "user"
- [ ] Scenario: Admin assigns app that user already has (expect conflict)
- [ ] Scenario: Admin assigns app with no available license seats (expect error)
- [ ] Scenario: Admin revokes assignment
- [ ] Scenario: Admin changes access_level on existing assignment
- [ ] Scenario: List assignments by org
- [ ] Scenario: List assignments by user_id
- [ ] Scenario: List assignments by app_id
- [ ] Scenario: Member cannot assign apps (expect 403)
- [ ] Scenario: Manager can assign apps within team
- [ ] Scenario: Assignment increments license seats_assigned
- [ ] Scenario: Revocation decrements license seats_assigned

### C.4 Request Workflow Test Scenarios
- [ ] Scenario: Member creates request with all fields
- [ ] Scenario: Member creates request with minimum fields
- [ ] Scenario: Member creates request with reason < 3 chars (expect 422)
- [ ] Scenario: Member creates request with 1 seat
- [ ] Scenario: Member creates request with 100000 seats
- [ ] Scenario: Manager reviews request (changes to under_review)
- [ ] Scenario: Manager approves request
- [ ] Scenario: Manager rejects request with notes
- [ ] Scenario: Admin provisions approved request
- [ ] Scenario: Invalid status transition (pending -> provisioned, skip approved)
- [ ] Scenario: Request auto-triggers TurboTick automation
- [ ] Scenario: Request with budget exceeding policy limit
- [ ] Scenario: List requests filtered by status
- [ ] Scenario: List requests filtered by requester
- [ ] Scenario: Request SLA tracking (time from creation to resolution)
- [ ] Scenario: Bulk approve multiple requests

### C.5 Budget & Compliance Test Scenarios
- [ ] Scenario: Create budget policy with all fields
- [ ] Scenario: Create budget policy with department_id
- [ ] Scenario: Create budget policy with 0 monthly_limit
- [ ] Scenario: Create budget policy with negative monthly_limit (expect 422)
- [ ] Scenario: Create budget policy with alert_threshold 0%
- [ ] Scenario: Create budget policy with alert_threshold 100%
- [ ] Scenario: Create budget policy with alert_threshold 101% (expect 422)
- [ ] Scenario: Upsert procurement config (create new)
- [ ] Scenario: Upsert procurement config (update existing)
- [ ] Scenario: Procurement config require_manager_approval true
- [ ] Scenario: Procurement config auto_approve_threshold
- [ ] Scenario: Request approved bypasses manager if under auto_approve_threshold
- [ ] Scenario: Request requires manager approval if over threshold
- [ ] Scenario: Budget alert triggered when spending reaches threshold

### C.6 Audit Log Test Scenarios
- [ ] Scenario: Audit event created on app create
- [ ] Scenario: Audit event created on app update
- [ ] Scenario: Audit event created on app delete
- [ ] Scenario: Audit event created on license create
- [ ] Scenario: Audit event created on assignment create
- [ ] Scenario: Audit event created on assignment revoke
- [ ] Scenario: Audit event created on request create
- [ ] Scenario: Audit event created on request status change
- [ ] Scenario: Audit event contains correct org_id
- [ ] Scenario: Audit event contains correct user_id
- [ ] Scenario: Audit event contains correct role
- [ ] Scenario: Audit event contains correct resource_type
- [ ] Scenario: Audit event contains correct resource_id
- [ ] Scenario: Audit event metadata_json populated
- [ ] Scenario: List audit events by org
- [ ] Scenario: List audit events by event_type
- [ ] Scenario: List audit events by user_id
- [ ] Scenario: List audit events by date range
- [ ] Scenario: Audit events org isolation (cannot see other org events)

### C.7 Authentication Test Scenarios
- [ ] Scenario: Valid Bearer token returns correct actor
- [ ] Scenario: Expired Bearer token returns 401
- [ ] Scenario: Invalid Bearer token returns 401
- [ ] Scenario: Missing Bearer token with gate-only mode returns 401
- [ ] Scenario: Header-based auth with all headers returns actor
- [ ] Scenario: Header-based auth missing X-Org-Id returns 400
- [ ] Scenario: Header-based auth missing X-User-Id returns 400
- [ ] Scenario: Header-based auth invalid X-User-Role returns 400
- [ ] Scenario: Hybrid mode prefers Bearer when present
- [ ] Scenario: Hybrid mode falls back to headers when no Bearer
- [ ] Scenario: Gate userinfo returns org_role correctly mapped
- [ ] Scenario: Gate userinfo returns roles array correctly mapped
- [ ] Scenario: Gate userinfo missing subject returns 502
- [ ] Scenario: Gate userinfo missing org_id returns 403
- [ ] Scenario: Gate service unavailable returns 502

---

## Appendix D: Detailed Responsive Design Specifications

### D.1 Mobile Layout (0-639px)
- [ ] Header: Logo + hamburger menu, search icon, notification icon
- [ ] Navigation: Full-screen slide-out drawer from left
- [ ] Navigation: Close on outside tap
- [ ] Navigation: Close on route change
- [ ] Content: Single column, full width
- [ ] Stat cards: Single column stack
- [ ] Table: Horizontal scroll with shadow indicator
- [ ] Table: Alternative card view for small data sets
- [ ] Toolbar: Stacked vertically (search full-width, filters below)
- [ ] Modals: Full screen (bottom sheet style)
- [ ] Context panel: Hidden by default, accessible via button
- [ ] Toast notifications: Bottom center, full width
- [ ] Floating action button: Bottom right for quick actions
- [ ] Footer: Sticky bottom navigation (if applicable)

### D.2 Tablet Layout (640-1023px)
- [ ] Header: Full width with search bar
- [ ] Navigation: Collapsible sidebar (icon-only mode)
- [ ] Navigation: Expand on hover or click
- [ ] Content: Two columns (content + context panel)
- [ ] Stat cards: Two-column grid
- [ ] Table: Full width with horizontal scroll if needed
- [ ] Toolbar: Single row with condensed controls
- [ ] Modals: Centered with max-width 600px
- [ ] Context panel: Collapsible right panel

### D.3 Desktop Layout (1024-1279px)
- [ ] Header: Full width with search bar and actions
- [ ] Navigation: Fixed sidebar (icon + text, ~220px)
- [ ] Content: Three columns (sidebar + content + context)
- [ ] Stat cards: Four-column grid
- [ ] Table: Full width with all columns visible
- [ ] Toolbar: Single row with all controls
- [ ] Modals: Centered with max-width 720px
- [ ] Context panel: Always visible (~350px)

### D.4 Wide Layout (1280px+)
- [ ] Content: Max-width container (1440px) centered
- [ ] Stat cards: Four or more columns
- [ ] Table: Comfortable spacing, all columns visible
- [ ] Sidebar: Fixed width
- [ ] Context panel: Wider (~400px)

---

## Appendix E: Keyboard Shortcut Specification

### E.1 Global Shortcuts
- [ ] `Cmd/Ctrl + K` — Open command palette / quick search
- [ ] `Cmd/Ctrl + /` — Toggle sidebar
- [ ] `Cmd/Ctrl + Shift + D` — Toggle dark mode
- [ ] `Cmd/Ctrl + ,` — Open settings
- [ ] `Escape` — Close current modal/panel/overlay
- [ ] `?` — Show keyboard shortcuts help (when no input focused)

### E.2 Navigation Shortcuts
- [ ] `G then H` — Go to Home/Dashboard
- [ ] `G then A` — Go to App Catalog
- [ ] `G then L` — Go to Licenses
- [ ] `G then S` — Go to Assignments
- [ ] `G then R` — Go to Requests
- [ ] `G then P` — Go to Packages
- [ ] `G then U` — Go to Audit Log
- [ ] `G then B` — Go to Budget & Compliance
- [ ] `G then T` — Go to Settings

### E.3 Action Shortcuts
- [ ] `N then A` — New App
- [ ] `N then R` — New Request
- [ ] `N then L` — New License
- [ ] `Cmd/Ctrl + Enter` — Submit current form
- [ ] `Cmd/Ctrl + Shift + A` — Approve selected request
- [ ] `Cmd/Ctrl + Shift + R` — Reject selected request

### E.4 Table Navigation
- [ ] `J` / `Down Arrow` — Move to next row
- [ ] `K` / `Up Arrow` — Move to previous row
- [ ] `Enter` — Open selected row detail
- [ ] `Space` — Toggle row selection
- [ ] `Cmd/Ctrl + A` — Select all rows
- [ ] `Delete` / `Backspace` — Delete selected (with confirmation)

---

## Appendix F: Error State Inventory

### F.1 Network Errors
- [ ] Error state: No internet connection
- [ ] Error state: API request timeout
- [ ] Error state: Server 500 error
- [ ] Error state: Server 502/503 (backend down)
- [ ] Error state: CORS error
- [ ] Retry mechanism: Automatic retry with exponential backoff
- [ ] Retry mechanism: Manual retry button
- [ ] Offline banner with reconnection detection

### F.2 Validation Errors
- [ ] Error state: Required field empty
- [ ] Error state: Field too short (min length)
- [ ] Error state: Field too long (max length)
- [ ] Error state: Invalid email format
- [ ] Error state: Invalid URL format
- [ ] Error state: Number out of range
- [ ] Error state: Duplicate entry
- [ ] Inline error messages under fields
- [ ] Form-level error summary

### F.3 Authorization Errors
- [ ] Error state: Session expired (401) — redirect to login
- [ ] Error state: Forbidden (403) — permission denied message
- [ ] Error state: Org not found — org selection required
- [ ] Error state: Account disabled — contact admin message

### F.4 Data Errors
- [ ] Error state: Record not found (404)
- [ ] Error state: Conflict (409) — stale data warning
- [ ] Error state: Data integrity violation
- [ ] Error state: Empty search results
- [ ] Error state: Empty list (with create CTA)

---

## Appendix G: Loading State Inventory

### G.1 Page-Level Loading
- [ ] Loading state: Initial app load (splash screen)
- [ ] Loading state: Page navigation (skeleton screen)
- [ ] Loading state: Data fetching (skeleton cards/rows)

### G.2 Component-Level Loading
- [ ] Loading state: Table rows (skeleton rows)
- [ ] Loading state: Stat cards (skeleton cards)
- [ ] Loading state: Charts (skeleton charts)
- [ ] Loading state: Search results (skeleton list)
- [ ] Loading state: Context panel (skeleton content)
- [ ] Loading state: Modal content (skeleton form)

### G.3 Action-Level Loading
- [ ] Loading state: Form submission (button spinner)
- [ ] Loading state: Delete operation (confirmation + spinner)
- [ ] Loading state: Export generation (progress indicator)
- [ ] Loading state: Bulk operation (progress bar)
- [ ] Loading state: File upload (progress bar)

---

---

## Appendix H: Notification Types Inventory

### H.1 Procurement Notifications
- [ ] Notification: New procurement request submitted (to managers)
- [ ] Notification: Request status changed (to requester)
- [ ] Notification: Request approved (to requester)
- [ ] Notification: Request rejected (to requester, with reason)
- [ ] Notification: Request provisioned (to requester, app ready to use)
- [ ] Notification: Request SLA warning (approaching deadline, to reviewer)
- [ ] Notification: Request SLA breached (to admin)
- [ ] Notification: Request needs review (to assigned reviewer)
- [ ] Notification: Bulk approval summary (to admin)

### H.2 License Notifications
- [ ] Notification: License renewal approaching (30 days, 14 days, 7 days, 1 day)
- [ ] Notification: License expired
- [ ] Notification: License seats almost full (> 90% utilized)
- [ ] Notification: License seats exhausted (100% utilized)
- [ ] Notification: New license purchased (to team)
- [ ] Notification: License cost changed
- [ ] Notification: License downgraded/upgraded

### H.3 Assignment Notifications
- [ ] Notification: App assigned to you (to user)
- [ ] Notification: App access revoked (to user)
- [ ] Notification: Access level changed (to user)
- [ ] Notification: Bulk assignment completed (to admin)
- [ ] Notification: Assignment sync with Secure failed (to admin)

### H.4 Budget Notifications
- [ ] Notification: Budget threshold reached (alert_threshold_pct)
- [ ] Notification: Budget exceeded (100%)
- [ ] Notification: Monthly budget report ready
- [ ] Notification: New budget policy created (to affected managers)
- [ ] Notification: Budget policy changed (to affected managers)
- [ ] Notification: Quarterly budget review reminder

### H.5 System Notifications
- [ ] Notification: System maintenance scheduled
- [ ] Notification: New Dock feature available
- [ ] Notification: API deprecation warning
- [ ] Notification: Cross-app integration error (EventBus down, etc.)
- [ ] Notification: Security event (unusual login, password change)
- [ ] Notification: Package update available

### H.6 Widget Notifications
- [ ] Notification: Widget data source unavailable
- [ ] Notification: Widget refresh failed
- [ ] Notification: New widgets available in gallery

---

## Appendix I: Cross-App Integration Specifications

### I.1 Atlas (Project Management) Integration
- [ ] Pull task count for dashboard widget
- [ ] Pull assigned tasks for "My Tasks" widget
- [ ] Pull project list for quick navigation
- [ ] Deep link to specific task
- [ ] Create task from Dock (quick action)
- [ ] Task status change events via EventBus
- [ ] Task assignment events via EventBus

### I.2 Mail Integration
- [ ] Pull unread email count for widget
- [ ] Pull recent emails for preview widget
- [ ] Deep link to specific email
- [ ] Compose email from Dock (quick action)
- [ ] New email notification via EventBus

### I.3 Calendar Integration
- [ ] Pull today's events for "Daily Agenda" widget
- [ ] Pull upcoming meetings for "Meetings" widget
- [ ] Deep link to specific event
- [ ] Create event from Dock (quick action)
- [ ] Event reminder notification via EventBus
- [ ] Calendar mini-view widget

### I.4 Meet Integration
- [ ] Pull upcoming meetings for "Meetings" widget
- [ ] Join meeting button in widget
- [ ] Meeting start notification

### I.5 Connect Integration
- [ ] Pull team activity for "Team Feed" widget
- [ ] Pull unread messages count
- [ ] Pull recent DMs preview
- [ ] Deep link to channel/DM

### I.6 Planet CRM Integration
- [ ] Pull open deals count for "Deals" widget
- [ ] Pull deal pipeline overview
- [ ] Deal stage change events via EventBus

### I.7 TurboTick Integration
- [x] Automation ticket creation from requests
- [ ] Issue status tracking in requests
- [ ] Issue assignment sync
- [ ] Issue resolution notification

### I.8 Secure Integration
- [x] Assignment sync via Secure bridge
- [ ] Security compliance status widget
- [ ] Endpoint health overview widget
- [ ] Security alerts via EventBus

### I.9 Capital Hub Integration
- [ ] Finance overview widget
- [ ] Budget status from Capital Hub
- [ ] Invoice pending count
- [ ] Financial reports deep link

### I.10 Writer Integration
- [ ] Quick note capture widget (saves to Writer)
- [ ] Recent documents widget
- [ ] Document search integration

### I.11 EventBus Integration
- [ ] SSE subscription for real-time updates
- [ ] Event filtering by type
- [ ] Event routing to appropriate widget
- [ ] Connection health monitoring
- [ ] Reconnection with exponential backoff
- [ ] Event deduplication
- [ ] Event ordering guarantees

---

## Appendix J: Data Migration Specifications

### J.1 If Migrating Backend (Node.js to Python)
> Note: PER_APP_CHECKLIST.md says backend is Node.js/Express, but actual codebase is Python/FastAPI

- [x] Backend is already Python/FastAPI (no migration needed)
- [ ] Document the actual stack in PER_APP_CHECKLIST.md (correct from Node.js to Python)

### J.2 Frontend Data Migration (Vanilla to React)
- [ ] Map current DOM state to React state
- [ ] Map current event handlers to React event handlers
- [ ] Map current API calls to React Query hooks
- [ ] Map current CSS classes to Tailwind/orbit utilities
- [ ] Map current animations to Framer Motion or CSS transitions
- [ ] Verify all features work identically after migration
- [ ] Performance comparison (vanilla vs React bundle size)
- [ ] Accessibility comparison (ensure no regressions)

### J.3 Database Schema Evolution
- [ ] Review current Alembic migrations for completeness
- [ ] Plan new migrations for missing features (widgets, preferences, bookmarks)
- [ ] Widget layout table (user_id, widget_type, position, size, config)
- [ ] User preferences table (user_id, key, value)
- [ ] Bookmarks table (user_id, resource_type, resource_id, title)
- [ ] Notification table (user_id, type, title, body, read, created_at)
- [ ] Search history table (user_id, query, result_count, searched_at)

---

## Appendix K: Monitoring & Alerting Specifications

### K.1 Application Metrics
- [ ] Metric: HTTP request count by endpoint and status
- [ ] Metric: HTTP request latency (p50, p95, p99) by endpoint
- [ ] Metric: HTTP request body size
- [ ] Metric: Active connections count
- [ ] Metric: Error rate (4xx, 5xx) by endpoint
- [ ] Metric: Database query latency (p50, p95, p99)
- [ ] Metric: Database connection pool utilization
- [ ] Metric: Cache hit/miss ratio (if Redis)
- [ ] Metric: Background job queue depth
- [ ] Metric: Background job processing time

### K.2 Business Metrics
- [ ] Metric: Active users per day/week/month
- [ ] Metric: Apps created per day
- [ ] Metric: Requests submitted per day
- [ ] Metric: Requests approved per day
- [ ] Metric: Average request resolution time
- [ ] Metric: License utilization percentage
- [ ] Metric: Budget utilization percentage
- [ ] Metric: Top requested apps
- [ ] Metric: Widget usage by type

### K.3 Alert Rules
- [ ] Alert: Error rate > 5% for 5 minutes
- [ ] Alert: p95 latency > 2s for 5 minutes
- [ ] Alert: Database connection pool > 80% for 5 minutes
- [ ] Alert: Disk usage > 85%
- [ ] Alert: Memory usage > 85%
- [ ] Alert: CPU usage > 80% for 10 minutes
- [ ] Alert: Health check failure for 1 minute
- [ ] Alert: Zero traffic for 10 minutes (unexpected)
- [ ] Alert: Auth failure spike (> 50 in 5 minutes)
- [ ] Alert: External service (Gate, TurboTick) down for 2 minutes

---

---

## Appendix L: Data Model Specifications for Missing Features

### L.1 Widget Layout Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — user who owns this layout
- [ ] `widget_type` — enum: clock, weather, notes, tasks, calendar, emails, meetings, activity, deals, ai_briefing, notifications, app_usage, budget, licenses, system_health
- [ ] `position_x` — grid column position
- [ ] `position_y` — grid row position
- [ ] `width` — widget width in grid units
- [ ] `height` — widget height in grid units
- [ ] `config` — JSONB widget-specific settings
- [ ] `is_visible` — boolean, show/hide
- [ ] `sort_order` — display order
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### L.2 User Preference Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — user reference
- [ ] `key` — preference key (theme, language, timezone, sidebar_collapsed, etc.)
- [ ] `value` — preference value (JSONB for flexibility)
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### L.3 Bookmark Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — user reference
- [ ] `resource_type` — enum: app, view, link, external
- [ ] `resource_id` — reference to bookmarked item (nullable)
- [ ] `title` — display title
- [ ] `url` — direct URL (for external bookmarks)
- [ ] `icon` — display icon
- [ ] `sort_order` — display order
- [ ] `created_at` — creation timestamp

### L.4 Notification Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — recipient user
- [ ] `type` — notification type enum
- [ ] `title` — notification title
- [ ] `body` — notification body text
- [ ] `resource_type` — related resource type (nullable)
- [ ] `resource_id` — related resource ID (nullable)
- [ ] `action_url` — click-through URL
- [ ] `is_read` — boolean
- [ ] `read_at` — timestamp when read
- [ ] `is_dismissed` — boolean
- [ ] `dismissed_at` — timestamp when dismissed
- [ ] `priority` — enum: low, normal, high, urgent
- [ ] `created_at` — creation timestamp
- [ ] `expires_at` — auto-dismiss timestamp (nullable)

### L.5 Search Index Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `resource_type` — indexed resource type
- [ ] `resource_id` — indexed resource ID
- [ ] `title` — searchable title text
- [ ] `body` — searchable body text
- [ ] `metadata` — JSONB additional indexed fields
- [ ] `last_indexed_at` — last reindex timestamp
- [ ] Full-text search index on title + body
- [ ] Trigram index for fuzzy matching
- [ ] Auto-reindex on resource update

### L.6 Quick Action Model (To Build)
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — user reference (nullable for org-wide actions)
- [ ] `name` — action display name
- [ ] `description` — action description
- [ ] `icon` — display icon
- [ ] `action_type` — enum: navigate, create, api_call, external_link
- [ ] `action_config` — JSONB action parameters
- [ ] `keyboard_shortcut` — keyboard shortcut (nullable)
- [ ] `usage_count` — times used (for sorting by frequency)
- [ ] `is_system` — boolean, system-provided vs user-created
- [ ] `sort_order` — display order
- [ ] `created_at` — creation timestamp

---

## Appendix M: API Endpoint Design for Missing Features

### M.1 Widget Layout API
- [ ] `GET /api/dock/widgets` — get user's widget layout
- [ ] `POST /api/dock/widgets` — add widget
- [ ] `PATCH /api/dock/widgets/{id}` — update widget position/config
- [ ] `DELETE /api/dock/widgets/{id}` — remove widget
- [ ] `PUT /api/dock/widgets/layout` — bulk update layout
- [ ] `GET /api/dock/widgets/gallery` — available widget types
- [ ] `POST /api/dock/widgets/reset` — reset to default layout

### M.2 User Preferences API
- [ ] `GET /api/dock/preferences` — get all preferences
- [ ] `GET /api/dock/preferences/{key}` — get specific preference
- [ ] `PUT /api/dock/preferences/{key}` — set preference
- [ ] `DELETE /api/dock/preferences/{key}` — reset to default

### M.3 Bookmarks API
- [ ] `GET /api/dock/bookmarks` — get user's bookmarks
- [ ] `POST /api/dock/bookmarks` — add bookmark
- [ ] `PATCH /api/dock/bookmarks/{id}` — update bookmark
- [ ] `DELETE /api/dock/bookmarks/{id}` — remove bookmark
- [ ] `PUT /api/dock/bookmarks/reorder` — reorder bookmarks

### M.4 Notifications API
- [ ] `GET /api/dock/notifications` — get notifications (paginated)
- [ ] `GET /api/dock/notifications/unread-count` — unread count
- [ ] `PATCH /api/dock/notifications/{id}/read` — mark as read
- [ ] `POST /api/dock/notifications/mark-all-read` — mark all read
- [ ] `DELETE /api/dock/notifications/{id}` — dismiss notification
- [ ] `GET /api/dock/notifications/stream` — SSE for real-time

### M.5 Search API
- [ ] `GET /api/dock/search?q=term` — global search
- [ ] `GET /api/dock/search/suggestions?q=term` — autocomplete
- [ ] `GET /api/dock/search/recent` — recent searches
- [ ] `DELETE /api/dock/search/recent` — clear recent searches

### M.6 Widget Data Proxy API
- [ ] `GET /api/dock/widgets/data/tasks` — proxy to Atlas for tasks
- [ ] `GET /api/dock/widgets/data/emails` — proxy to Mail for emails
- [ ] `GET /api/dock/widgets/data/events` — proxy to Calendar for events
- [ ] `GET /api/dock/widgets/data/meetings` — proxy to Meet for meetings
- [ ] `GET /api/dock/widgets/data/deals` — proxy to Planet for deals
- [ ] `GET /api/dock/widgets/data/activity` — proxy to EventBus for activity
- [ ] Widget data caching (5-minute TTL)
- [ ] Widget data error handling (stale data on failure)

---

---

## Appendix N: Accessibility Testing Checklist (Per View)

### N.1 Dashboard View Accessibility
- [ ] Keyboard: Tab through all widget cards
- [ ] Keyboard: Enter/Space to interact with widget
- [ ] Screen reader: Widget titles announced
- [ ] Screen reader: Widget content described
- [ ] Screen reader: "X of Y widgets" count announced
- [ ] Focus: Widget card has visible focus ring
- [ ] Contrast: All widget text meets 4.5:1

### N.2 App Catalog View Accessibility
- [ ] Keyboard: Navigate app cards with arrow keys
- [ ] Keyboard: Enter to open app detail
- [ ] Screen reader: App name, vendor, description announced
- [ ] Screen reader: App status (advertised/hidden) announced
- [ ] Focus: App card has visible focus ring
- [ ] Contrast: All text meets requirements

### N.3 Table Views Accessibility (Licenses, Assignments, Requests, Audit)
- [ ] Keyboard: Tab into table, arrow keys between cells
- [ ] Keyboard: Enter to open row detail
- [ ] Screen reader: Table headers announced per column
- [ ] Screen reader: Sort direction announced
- [ ] Screen reader: Row count announced
- [ ] Screen reader: Pagination state announced
- [ ] Focus: Current cell has visible focus ring
- [ ] Contrast: All cell text meets requirements

---

*Generated: 2026-04-06 | Total checkboxes: ~1340+ | Target: 2000+ lines*
