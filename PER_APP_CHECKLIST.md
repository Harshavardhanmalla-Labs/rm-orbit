# RM Orbit — Per-App Granular Checklist

> **~1,950 checkpoints** across all 16 apps + shared infrastructure.
> Cross-reference with `WORLD_CLASS_CHECKLIST.md` for phase-level tracking.
> Last updated: 2026-04-06
>
> Legend: `[x]` = done · `[ ]` = todo · `[~]` = in progress · `[-]` = N/A / skipped

---

## Table of Contents

0. [Shared Infrastructure — orbit-ui + EventBus + Gate](#0-shared-infrastructure)
1. [Atlas — Project Management](#1-atlas--project-management)
2. [Mail — Enterprise Email](#2-mail--enterprise-email)
3. [Connect — Team Communication](#3-connect--team-communication)
4. [Meet — Video Conferencing](#4-meet--video-conferencing)
5. [Calendar — Scheduling](#5-calendar--scheduling)
6. [Writer — Document Editor](#6-writer--document-editor)
7. [Planet — CRM & Sales](#7-planet--crm--sales)
8. [Secure — Endpoint Security](#8-secure--endpoint-security)
9. [Control Center — Operations Hub](#9-control-center--operations-hub)
10. [Capital Hub — Finance Dashboard](#10-capital-hub--finance-dashboard)
11. [TurboTick — Issue Tracker](#11-turbotick--issue-tracker)
12. [Dock — Workspace Hub](#12-dock--workspace-hub)
13. [Wallet — Financial Management](#13-wallet--financial-management)
14. [FitterMe — Health & Wellness](#14-fitterme--health--wellness)
15. [Learn — Documentation Portal](#15-learn--documentation-portal)
16. [Gate — Authentication (AuthX)](#16-gate--authentication-authx)

---

## 0 Shared Infrastructure

### 0-A orbit-ui Design System

#### Design Tokens
- [x] `tokens/colors.json` — full primary/neutral/semantic palette
- [x] `tokens/typography.json` — font families, sizes, weights, line-heights
- [x] `tokens/radius.json` — border-radius scale + component-specific
- [x] `tokens/shadows.json` — shadow scale + glass + focus rings
- [x] `tokens/z-index.json` — named z-index layers
- [x] `tokens/motion.json` — durations, easings, keyframes
- [x] `tokens/orbit-tokens.css` — CSS custom properties (light + dark)
- [x] `tailwind-preset.js` — shared TW v3 preset with all tokens + plugins
- [x] `orbit-tailwind-v4.css` — TW v4 `@theme` integration file
- [ ] Token versioning/changelog system
- [ ] Visual regression tests for token output
- [ ] Figma token sync (Figma Tokens plugin export)

#### orbit-bar (Shell Web Component)
- [x] App launcher panel with all 14 apps
- [x] Org switcher (reads/writes localStorage + emits `orbit:org-change`)
- [x] Identity panel (user avatar, name, sign-out)
- [x] Theme toggle button (sun/moon SVG, cycles light→dark→system)
- [x] `orbit:theme-change` custom event dispatch
- [x] CSS for theme toggle button (`.orbit-shell__theme-toggle`)
- [ ] Search hotkey (`/`) opens global search
- [ ] Keyboard navigation within app launcher panel
- [ ] Active app highlight in app launcher
- [ ] Notification badge on app icons (unread counts)
- [ ] Org switcher: search/filter for many orgs
- [ ] Breadcrumb slot (apps can inject current page path)
- [ ] Help / keyboard shortcut guide button
- [ ] Orbit bar mobile: collapse to icon-only below 768px
- [ ] Orbit bar a11y: all interactive elements have aria-labels

#### orbit-theme-init.js (Anti-FOUC)
- [x] Reads `localStorage["orbit-theme"]`
- [x] Checks `prefers-color-scheme: dark`
- [x] Applies `.dark` class to `<html>` before CSS loads
- [ ] Minified/inlined version for production builds

#### @orbit-ui/react Component Library
- [x] Package setup (`name: "@orbit-ui/react"`, ESM + CJS outputs)
- [x] `cn()` utility (clsx + tailwind-merge)
- [x] `Button` — 7 variants × 5 sizes, loading, icon slots, polymorphic `as`
- [x] `IconButton` — square variant, all sizes, loading
- [x] `Input` — sizes, states, prefix/suffix, error, helper
- [x] `Textarea` — base component
- [x] `Select` — native select wrapper
- [x] `Badge` — variants + sizes
- [x] `Card` — base card component
- [x] `Avatar` + `AvatarGroup`
- [x] `Sidebar` + `useSidebar` — collapsible, sections, items
- [x] `Tabs` — 3 variants, controlled/uncontrolled, lazy panels
- [x] `Modal` — accessible dialog
- [x] `Alert` — variants
- [x] `Tooltip` — 4 placements, delay, disabled
- [x] `ToastProvider` + `useToast`
- [x] `Spinner` + `PageLoader`
- [x] `Skeleton` + `SkeletonText` + `SkeletonCard`
- [x] `EmptyState`
- [x] `ThemeProvider` + `ThemeToggle` + `useTheme`
- [x] `Checkbox` — checked/indeterminate/disabled, label+description
- [x] `Switch` — sm/md, label+description, disabled
- [x] `Progress` + `ProgressStacked` — sizes, color variants
- [x] `Divider` — horizontal/vertical, with label
- [x] `Dropdown` suite — Trigger, Content, Item, Label, Separator, SubTrigger
- [x] `Radio` + `RadioGroup`
- [x] `ButtonGroup` — connected borders, active state
- [x] `Slider` — single + range, step markers
- [x] `DatePicker` — single date + range
- [x] `TimePicker` — 12h/24h
- [x] `CommandPalette` — search, categories, keyboard nav
- [x] `Drawer` / `Sheet` — side panel overlay
- [x] `Popover` — floating content anchor
- [x] `ContextMenu` — right-click trigger
- [x] `Table` — sortable, selectable rows, pagination
- [ ] `DataGrid` — virtual scroll, column resize
- [ ] `Form` wrapper with field-level validation
- [x] `FileUpload` — drag-drop zone, progress
- [ ] `RichTextEditor` — wrapper for Tiptap
- [x] `Tag` / `Chip` — dismissible, colored
- [x] `Steps` / `Stepper` — horizontal/vertical wizard
- [x] `Accordion` — single/multi expand
- [ ] `Tree` — nested list with expand/collapse
- [x] `Pagination` — page numbers + prev/next
- [x] `Breadcrumb` — nav with separator
- [x] `NumberInput` — increment/decrement, min/max/step
- [ ] Storybook 8 configured and running
- [ ] Stories for every component (all states/variants)
- [ ] Vitest unit tests for all components
- [ ] Interaction tests in Storybook

#### Token Sync Script
- [x] Syncs `orbit-tokens.css` to all 16 app `public/orbit-ui/` dirs
- [x] Syncs `orbit-bar.js`, `orbit-ui.css`, `orbit-theme-init.js`
- [x] Syncs `orbit-tailwind-v4.css`
- [ ] Pre-commit hook that auto-runs sync
- [ ] CI step that verifies all apps have latest tokens

### 0-B EventBus Service

- [ ] EventBus service running on port 6005
- [ ] SSE stream endpoint (`/stream?token=&org_id=`)
- [ ] Publish endpoint (`/publish`)
- [ ] Event types documented: project, deal, calendar, mail, planet, connect
- [ ] Event schema validation (Pydantic/Zod)
- [ ] Dead-letter queue for failed deliveries
- [ ] Replay last N events on reconnect
- [ ] Per-org event isolation (no cross-tenant leakage)
- [ ] Auth: Gate token required to subscribe/publish
- [ ] WebSocket fallback for SSE-blocked environments
- [ ] Health endpoint (`/health`)
- [ ] Metrics endpoint (`/metrics`)

### 0-C Gate Authentication (AuthX)

- [ ] PKCE OAuth2 flow fully tested end-to-end
- [ ] JWKS endpoint (`/.well-known/jwks.json`) production-ready
- [ ] Token introspection endpoint
- [ ] Token revocation endpoint
- [ ] Refresh token rotation
- [ ] Session management: concurrent sessions per user
- [ ] Org-scoped claims in JWT (`org_id`, `roles`, `permissions`)
- [ ] Admin portal UI for user/org management
- [ ] Gate developer dashboard (token inspector, key manager)
- [ ] Rate limiting on auth endpoints
- [ ] Brute force protection (lockout after N failures)
- [ ] Email verification flow
- [ ] Password strength enforcement
- [ ] MFA: TOTP (Google Authenticator) support
- [ ] MFA: SMS fallback
- [ ] Magic link (passwordless) login
- [ ] Social SSO: Google OAuth
- [ ] Social SSO: GitHub OAuth
- [ ] Social SSO: Microsoft Entra
- [ ] SAML 2.0 IdP support (enterprise)
- [ ] SCIM user provisioning endpoint
- [ ] Audit log of all auth events

### 0-D AI Layer (Orbit AI Infrastructure)
- [ ] LLM service: Claude (Anthropic) + OpenAI as fallback — unified `/api/ai/complete` endpoint
- [ ] Per-request model routing (task complexity → model tier selection)
- [ ] AI usage metering: tokens in/out logged per org per user
- [ ] Prompt template registry: versioned prompts stored in DB
- [ ] Streaming responses: SSE streaming for long AI outputs
- [ ] Context window management: chunking + summarization for long documents
- [ ] Knowledge graph: cross-app entity resolution (contact = same person in Mail + Planet + Connect)
- [ ] AI rate limiting: per-org token budget with overage alerts
- [ ] AI audit log: every AI call logged (prompt hash, model, tokens, latency)
- [ ] Orbit Assistant backend: chat agent with tool-call support (read/write across all apps)
- [ ] Workflow automation engine: trigger → condition → action pipeline
- [ ] Natural language workflow builder: "When a deal closes, create an Atlas project"
- [ ] AI feature flags per org (enable/disable per app AI features)

### 0-E Shared i18n Infrastructure
- [ ] i18n library: `react-i18next` + `i18next` in orbit-ui
- [ ] Locale detection: browser language → user preference → org default
- [ ] Translation file structure: `locales/{lang}/common.json` + per-app namespaces
- [ ] Languages: en, es, fr, de, pt, ja, zh-Hans, ar (RTL), he (RTL)
- [ ] RTL support: CSS logical properties throughout orbit-ui components
- [ ] RTL: orbit-bar layout flips correctly for ar/he locales
- [ ] Date/time formatting: `Intl.DateTimeFormat` locale-aware across all apps
- [ ] Number/currency formatting: `Intl.NumberFormat` locale-aware
- [ ] Pluralization rules: i18next handles language-specific plural forms
- [ ] Translation missing key fallback: always fall back to `en`
- [ ] CI check: no hardcoded English strings outside translation files (i18n-ally lint)

### 0-F Shared Observability Infrastructure
- [ ] Frontend error tracking: Sentry DSN configured in all apps via orbit-ui env
- [ ] Web Vitals: CLS, FID, LCP, FCP, TTFB reported to Sentry / Datadog
- [ ] User session replay: opt-in session recording (privacy-filtered, no PII)
- [ ] API latency tracking: all fetch calls wrapped in performance marks
- [ ] Feature usage analytics: custom events (orbit_event) per feature interaction
- [ ] Backend: structured JSON logging (timestamp, level, service, trace_id, user_id)
- [ ] Distributed tracing: OpenTelemetry spans across all 16 backend services
- [ ] Metrics: Prometheus counters/histograms exported per service
- [ ] Grafana dashboard: per-service latency p50/p95/p99, error rate, request rate
- [ ] Alerting: PagerDuty / Slack alert on error rate > 1% or p95 > 2s
- [ ] Uptime monitoring: synthetic health checks every 60s per service

---

## 1 Atlas — Project Management

> **Stack:** React 18.3.1 · Vite 5.4.2 · Router v6 · Tailwind v3 · Axios · @dnd-kit · Tiptap · Chart.js · Yjs
> **Routes:** 20+ · **Status:** ~70% feature complete

### 1-A Design System Integration
- [x] `index.css` imports `orbit-tokens.css`
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root in `main.jsx`
- [x] Remove all remaining hardcoded hex colors from component files (bulk token migration)
- [x] Replace `bg-gray-*` / `text-gray-*` with semantic tokens (`bg-surface-*`, `text-content-*`)
- [x] Replace `border-gray-*` with `border-border-*`
- [ ] Remove `bg-gray-50 text-gray-900` from `<body>` (done in index.html)
- [ ] Replace custom focus styles with `focus-ring` utility class
- [ ] Replace custom scrollbar CSS with `.scrollbar-thin` plugin
- [ ] Replace skeleton loading with `<Skeleton>` / `<SkeletonCard>` components
- [ ] Replace custom toast with shared `useToast` from `@orbit-ui/react`
- [ ] Replace custom `Spinner` with shared `<Spinner>` component
- [ ] Replace hardcoded button classes with `<Button>` from `@orbit-ui/react`
- [ ] Replace custom `Badge` variants with shared `<Badge>`
- [ ] Replace custom `Card` layouts with `<Card>` component
- [ ] Replace custom `Modal` with shared `<Modal>`
- [ ] Replace custom `Tooltip` with shared `<Tooltip>`
- [ ] Replace custom `Avatar` with shared `<Avatar>` / `<AvatarGroup>`
- [ ] Adopt `<Tabs>` component in project detail (board/timeline/sprints/files tabs)
- [ ] Adopt `<Sidebar>` component (replace custom sidebar implementation)
- [ ] Adopt `<Dropdown>` for context menus on tasks and project cards
- [ ] Adopt `<EmptyState>` for no-projects, no-tasks, no-results views

### 1-B Dark Mode
- [x] Audit Dashboard page — replace hardcoded light colors with dark: variants
- [x] Audit Kanban Board — semantic token migration applied
- [x] Audit Task Detail modal — border-gray-50 fixed, semantic tokens applied
- [ ] Audit Timeline view — grid lines, event bars, date headers
- [ ] Audit Sprint view — burndown chart, story point badges
- [ ] Audit Portfolio page — project cards, progress bars
- [x] Audit Settings page — form inputs, section dividers
- [x] Audit Login/Auth pages — form fields, error states
- [ ] Chart.js charts — dynamic theme colors (use CSS variables in dataset options)
- [ ] Verify dark mode on all 20+ routes
- [ ] Test color contrast ratios in dark mode (WCAG AA)

### 1-C Core Features — Project Management
- [ ] Dashboard: activity feed with real-time updates (WebSocket or polling)
- [ ] Dashboard: my tasks widget (filtered to current user)
- [ ] Dashboard: project health overview (on-track / at-risk / overdue)
- [ ] Dashboard: recent activity timeline
- [ ] Projects list: filtering by status (active, archived, completed)
- [ ] Projects list: search by project name
- [ ] Projects list: sort by name / due date / created / last updated
- [ ] Projects list: grid vs. list view toggle
- [ ] Project creation: name, description, start/end dates, team members, color/icon
- [ ] Kanban board: column creation (custom workflow states)
- [ ] Kanban board: drag-and-drop tasks between columns (@dnd-kit)
- [ ] Kanban board: task cards with assignee avatar, priority, due date
- [ ] Kanban board: swimlane grouping (by assignee / epic / priority)
- [ ] Kanban board: column WIP limits with visual warning
- [ ] Kanban board: quick-add task (click + in column header)
- [ ] Task detail: title editing (inline)
- [ ] Task detail: description with rich text editor (Tiptap)
- [ ] Task detail: subtask list with completion tracking
- [ ] Task detail: file attachments (upload + preview)
- [ ] Task detail: activity/comment thread
- [ ] Task detail: custom fields (dropdown, text, date, number)
- [ ] Task detail: time logging (start/stop timer + manual entry)
- [ ] Task detail: link related tasks (blocks / blocked-by / related)
- [ ] Task detail: history/audit trail of all changes
- [ ] Timeline / Gantt: task bars with duration
- [ ] Timeline / Gantt: dependency arrows between tasks
- [ ] Timeline / Gantt: drag-resize bars to change dates
- [ ] Timeline / Gantt: milestone markers
- [ ] Timeline / Gantt: critical path highlighting
- [ ] Sprint management: create sprint with start/end date, goal
- [ ] Sprint management: backlog triage (drag tasks into sprint)
- [ ] Sprint management: velocity chart (story points per sprint)
- [ ] Sprint management: burndown chart per sprint
- [ ] Sprint management: sprint retrospective notes
- [ ] Portfolio view: cross-project progress overview
- [ ] Portfolio view: resource allocation heatmap
- [ ] AI Inbox: AI-suggested task priorities
- [ ] AI Inbox: automated status update summaries
- [ ] File browser: folder structure, upload, preview (image/PDF/doc)
- [ ] Import: CSV import for tasks
- [ ] Import: Jira/Trello export import (JSON format)
- [ ] Team management: invite by email, assign roles per project
- [ ] Project settings: rename, archive, delete, change color/icon
- [ ] Analytics page: task completion trends, team velocity
- [ ] Collaborative editing: Yjs integration for task descriptions

### 1-D API Integration
- [ ] All API calls use centralized Axios instance with auth headers
- [ ] Token refresh interceptor working (401 → refresh → retry)
- [ ] `X-Org-Id` header on all requests
- [ ] Error handling: show user-facing error messages on API failures
- [ ] Optimistic updates for task status changes (instant UI, rollback on error)
- [ ] Real-time updates: WebSocket or SSE subscription for board changes
- [ ] Offline queue: actions taken offline replayed on reconnect

### 1-E Performance
- [ ] Route-level code splitting (all 20 routes lazy loaded)
- [ ] Virtual scroll for large task lists (>100 items)
- [ ] Kanban board: only render visible columns (virtualize horizontal scroll)
- [ ] Image thumbnails: lazy loaded with `loading="lazy"`
- [ ] Debounce search input (300ms)
- [ ] Memoize expensive computations (task filters, gantt calculations)
- [ ] Bundle size audit: tree-shake unused Chart.js modules
- [ ] First meaningful paint < 1.5s on fast 3G

### 1-F Accessibility
- [ ] Skip-to-main-content link at top of page
- [ ] Kanban board: keyboard navigation between tasks (arrow keys)
- [ ] Drag-and-drop keyboard alternative (cut/paste tasks)
- [ ] All modals trap focus and return focus on close
- [ ] All form fields have visible labels
- [ ] ARIA live region for board updates ("Task moved to Done")
- [ ] Color is not the only indicator of task status/priority
- [ ] Tested with screen reader (VoiceOver / NVDA)

### 1-G Mobile & Responsive
- [ ] Mobile: bottom tab navigation instead of sidebar
- [ ] Mobile: task card list view (kanban board collapses to list)
- [ ] Mobile: touch-friendly drag-and-drop (drag handle visible)
- [ ] Mobile: swipe left on task card to quick-action (complete / delete)
- [ ] Tablet: sidebar collapses to icon-only
- [ ] All modals full-screen on mobile

### 1-H Testing
- [ ] Unit tests: task filtering logic
- [ ] Unit tests: date calculation utilities
- [ ] Integration tests: create project → add task → move to Done
- [ ] E2E (Playwright): full board interaction flow
- [ ] E2E: OAuth login flow

### 1-I AI Features (Atlas AI)
- [ ] AI task breakdown: paste a goal → AI generates subtasks with estimates
- [ ] Sprint planning assistant: AI suggests which backlog items fit sprint capacity
- [ ] Effort estimation: AI predicts story point range based on task description + history
- [ ] Risk analysis: AI flags tasks with vague descriptions or missing assignees
- [ ] Standup summary: AI generates yesterday/today/blockers from task activity
- [ ] Project health report: AI analyzes velocity trends and generates narrative summary
- [ ] Smart labels: AI auto-suggests labels based on task description
- [ ] Duplicate detection: AI warns when new task is similar to existing one
- [ ] Meeting-to-tasks: paste meeting notes → AI extracts action items into Atlas tasks
- [ ] AI search: natural language query ("show me overdue tasks assigned to me this sprint")

### 1-J Cross-App Integrations
- [ ] Calendar: Atlas milestones appear as Calendar events (bidirectional sync)
- [ ] Meet: "Start meeting" from Atlas project → creates Meet room linked to project
- [ ] Writer: link Writer document to Atlas task/project (shows in task detail)
- [ ] Mail: email thread can be linked to Atlas task (shows email thread in task)
- [ ] Connect: Atlas task notifications posted to relevant Connect channel
- [ ] TurboTick: Atlas task ↔ TurboTick issue linking (for engineering handoffs)
- [ ] Control Center: Atlas project progress feeds into Control Center dashboard
- [ ] Planet: Atlas project linked to Planet deal (delivery tracking for sales)
- [ ] EventBus: emit `project.created`, `task.updated`, `sprint.completed` events
- [ ] EventBus: consume `deal.won` → auto-create Atlas project from template

### 1-K Security & Compliance
- [ ] All Atlas API endpoints require valid Gate JWT + org scope
- [ ] Row-level security: users only see projects/tasks within their org
- [ ] RBAC: Admin / Project Lead / Member / Viewer role enforcement in all routes
- [ ] File attachments: virus scan on upload, MIME type whitelist
- [ ] Sensitive data: no task content in error logs or analytics events
- [ ] GDPR: user data export includes all Atlas tasks/comments created by user
- [ ] GDPR: user deletion anonymizes task history (replaces name with "Deleted User")
- [ ] Audit log: all task CUD operations logged with actor + timestamp

### 1-L Accessibility (Additional)
- [ ] Kanban board: keyboard drag-and-drop (Space to pick up, arrow keys to move, Enter to drop)
- [ ] Gantt/timeline: keyboard navigation between tasks
- [ ] Date pickers: keyboard navigable calendar widget
- [ ] All modals: focus trap + return focus on close
- [ ] Status badges: never rely on color alone (always include text label)
- [ ] Screen reader: announce drag-and-drop state changes via aria-live

### 1-M i18n
- [ ] All static strings in `locales/` translation files
- [ ] Date display: locale-aware (DD/MM/YYYY for EU, MM/DD/YYYY for US)
- [ ] Sprint duration labels: locale-aware pluralization ("1 day" vs "2 days")
- [ ] RTL: kanban board columns render correctly in ar/he
- [ ] Number formatting: story points and hours use `Intl.NumberFormat`

---

## 2 Mail — Enterprise Email

> **Stack:** React 18.3.1 · Vite 5.4.8 · Router v6 · Tailwind v3 · Axios · React Quill · Framer Motion
> **Routes:** 7 · **Status:** ~65% feature complete

### 2-A Design System Integration
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [x] `styles.css` — add `@import "/orbit-ui/orbit-tokens.css";` at top
- [ ] Replace hardcoded colors in mail list, thread view, compose panel
- [ ] Replace custom `Spinner` with shared component
- [ ] Replace custom toast notifications with `useToast`
- [ ] Replace custom `Avatar` for sender avatars with `<Avatar>`
- [ ] Adopt `<Badge>` for unread count, attachment indicators
- [ ] Adopt `<EmptyState>` for empty inbox, empty search results
- [ ] Adopt `<Skeleton>` for loading thread list
- [ ] Replace hardcoded focus styles with `focus-ring`
- [ ] Adopt `<Dropdown>` for email action menus (reply/forward/more)

### 2-B Dark Mode
- [ ] Email list pane: selected state, hover state in dark mode
- [ ] Email thread view: message bubbles, quoted text
- [ ] Compose panel: toolbar, editor background, recipient chips
- [ ] Sidebar: folder tree, unread count badges
- [ ] Search results: highlighted match text
- [ ] Email content iframe: inject `color-scheme: dark` when in dark mode
- [ ] Attachment preview overlays
- [ ] Audit all 7 routes in dark mode

### 2-C Core Features — Email Client
- [ ] Inbox: paginated/virtual-scroll thread list (handle 10k+ threads)
- [ ] Inbox: unread count badge per folder
- [ ] Inbox: mark as read/unread on open
- [ ] Inbox: star/flag emails
- [ ] Inbox: bulk select (checkbox) + bulk actions (archive, delete, move)
- [ ] Thread view: full conversation threading (email chain)
- [ ] Thread view: expand/collapse individual replies
- [ ] Thread view: inline images rendered (safe, not blocked)
- [ ] Thread view: attachment list with download links
- [ ] Thread view: external link warning before navigating
- [ ] Compose: To / CC / BCC recipient chips with autocomplete
- [ ] Compose: Subject line
- [ ] Compose: rich text editor (React Quill — bold, italic, lists, links, images)
- [ ] Compose: paste HTML from clipboard (Word / Google Docs)
- [ ] Compose: inline image insertion
- [ ] Compose: file attachments with progress bar
- [ ] Compose: save draft (auto-save every 30s)
- [ ] Compose: discard draft with confirmation
- [ ] Compose: send with delay (schedule send)
- [ ] Compose: reply / reply-all / forward actions from thread
- [ ] Compose: floating composer (like Gmail) — minimize/maximize
- [ ] Folders: Inbox, Sent, Drafts, Trash, Spam — all functional
- [ ] Folders: custom folder creation + drag email into folder
- [ ] Labels: create, assign, color-code labels
- [ ] Labels: filter view by label
- [ ] Search: full-text search across all emails
- [ ] Search: filters (from, to, date range, has attachment, label)
- [ ] Search: result highlighting
- [ ] Search: recent searches history
- [ ] Settings: email signature editor
- [ ] Settings: vacation autoresponder
- [ ] Settings: notification preferences (desktop, email digest)
- [ ] Settings: keyboard shortcuts toggle
- [ ] Admin: user management (create/disable accounts)
- [ ] Admin: domain management
- [ ] Admin: email routing rules
- [ ] Admin: quota management
- [ ] Admin: audit log of admin actions
- [ ] Keyboard shortcuts: `c` compose, `r` reply, `f` forward, `e` archive, `#` delete, `j/k` next/prev email

### 2-D API Integration
- [ ] Email list API: pagination, folder filter, search query
- [ ] Thread API: load full thread by thread_id
- [ ] Compose API: send email with attachments (multipart/form-data)
- [ ] Draft API: create / update / delete draft
- [ ] Labels API: CRUD + apply to thread
- [ ] Move/archive API: thread-level operations
- [ ] Search API: debounced query, highlight snippets in results
- [ ] Real-time: new email notification via SSE or WebSocket
- [ ] Attachment download: signed URL or streaming endpoint

### 2-E Performance
- [ ] Virtual scroll for thread list (react-window or tanstack virtual)
- [ ] Email content iframe sandbox (prevent runaway scripts)
- [ ] Progressive loading: load first 20 threads, lazy load more
- [ ] Attachment preview: generate thumbnails server-side
- [ ] Debounce search input (400ms)

### 2-F Accessibility
- [ ] Thread list: arrow key navigation
- [ ] Compose: tab order through To → CC → Subject → Body
- [ ] Keyboard shortcut overlay (press `?` to show)
- [ ] Screen reader: announce "1 new email" on new message
- [ ] All icons have aria-label or aria-hidden

### 2-G Mobile & Responsive
- [ ] Mobile: two-panel layout collapses to single panel
- [ ] Mobile: swipe right on thread to archive
- [ ] Mobile: bottom sheet for compose instead of floating panel
- [ ] Mobile: touch-friendly attachment upload

### 2-H Testing
- [ ] Unit: compose form validation (empty subject warning)
- [ ] Unit: thread grouping logic
- [ ] E2E: login → open inbox → open thread → reply

### 2-I AI Features (Mail AI)
- [ ] Compose assist: AI drafts full email from bullet points or short prompt
- [ ] Smart reply: 3 AI-generated quick reply options for any email
- [ ] Email summarization: one-click AI summary of long email threads
- [ ] Priority inbox: AI scores emails by urgency + sender importance
- [ ] Auto-categorization: AI labels emails (invoice, meeting request, support, newsletter)
- [ ] Sentiment analysis: flag emotionally charged or urgent emails
- [ ] Follow-up reminder: AI detects emails awaiting reply → surfaces in inbox after N days
- [ ] Subject line suggestions: AI improves subject line before sending
- [ ] Tone adjustment: rewrite email in formal / casual / assertive tone
- [ ] Unsubscribe suggestions: AI identifies newsletters and offers one-click unsubscribe

### 2-J Cross-App Integrations
- [ ] Calendar: "Add to Calendar" from meeting invite emails (parses ICS attachment)
- [ ] Atlas: "Create task from email" action in email detail view
- [ ] Planet: emails from Planet contacts auto-link to their CRM record
- [ ] Connect: forward email to Connect channel
- [ ] Meet: "Join meeting" button parsed from email invites (Zoom, Google Meet, Orbit Meet links)
- [ ] Writer: attach Writer document to email (inserts shareable link)
- [ ] EventBus: emit `mail.received` events for high-priority emails
- [ ] EventBus: consume `deal.won` → auto-send congratulations template email

### 2-K Security & Compliance
- [ ] All email data encrypted at rest (AES-256)
- [ ] SPF / DKIM / DMARC validation on incoming emails (display warnings for failures)
- [ ] Phishing detection: flag emails with suspicious links or spoofed senders
- [ ] Link rewriting: external links go through safe-link proxy before opening
- [ ] Attachment scanning: virus scan + MIME type check before download
- [ ] No email content in frontend logs or Sentry breadcrumbs
- [ ] GDPR: email data export on user request
- [ ] GDPR: email purge on account deletion (with 30-day retention for legal hold)
- [ ] Email encryption: S/MIME support for sending/receiving encrypted emails
- [ ] Audit log: email send/delete/move actions logged per user

### 2-L i18n
- [ ] All UI strings in translation files
- [ ] Date display in email list: locale-aware relative times ("2 hours ago" / "hace 2 horas")
- [ ] Email compose: spell-check respects user's locale language
- [ ] RTL: email list and reading pane layout flip for ar/he
- [ ] Time zone: sent/received timestamps shown in user's local timezone

### 2-M Accessibility (Additional)
- [ ] Email list: keyboard navigation (up/down arrows to move between emails)
- [ ] Email list: keyboard shortcuts (`E` = archive, `#` = delete, `R` = reply, `F` = forward)
- [ ] Mark-as-read on keyboard focus (configurable)
- [ ] All toolbar buttons in compose labeled with aria-label
- [ ] Attachment list: each attachment has descriptive accessible name
- [ ] Screen reader: announce unread count changes via aria-live="polite"

---

## 3 Connect — Team Communication

> **Stack:** React 19.2.3 · Vite 7.2.4 · SPA (no router) · Tailwind v4 · Zustand · Socket.io · WebRTC
> **Routes:** N/A (SPA) · **Status:** ~75% feature complete

### 3-A Design System Integration
- [x] `ThemeProvider` wraps root
- [x] Anti-FOUC script in `index.html`
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";` before `@import "tailwindcss";`
- [x] `index.css` — add `@import "/orbit-ui/orbit-tailwind-v4.css";` after tailwindcss
- [ ] Remove Google Fonts DM Sans (already done in index.html — verify CSS)
- [ ] Replace `font-['DM_Sans']` occurrences with `font-sans`
- [ ] `JetBrains Mono` for code blocks — configure via orbit-tailwind-v4 theme
- [ ] Replace hardcoded sidebar bg colors with `bg-surface-subtle`
- [ ] Replace hardcoded message bubble colors with semantic tokens
- [ ] Replace custom `Avatar` with `<Avatar>` from `@orbit-ui/react`
- [ ] Replace custom `Badge` (mention count, online indicator) with `<Badge>`
- [ ] Replace custom `Tooltip` with shared `<Tooltip>`
- [ ] Replace custom `Dropdown` (message actions menu) with `<Dropdown>` suite
- [ ] Replace custom `Modal` (create channel, settings) with `<Modal>`
- [ ] Replace custom `Switch` in settings with `<Switch>`
- [ ] Adopt `<EmptyState>` for empty channel (no messages yet)
- [ ] Adopt `<Spinner>` for loading states
- [ ] Adopt `<Skeleton>` for loading message list

### 3-B Dark Mode
- [ ] Channel sidebar: active channel highlight, hover state
- [ ] Message list: message bubbles (own vs. others), system messages
- [ ] Message input: border, placeholder, emoji picker background
- [ ] Right panel: thread view, profile panel, members list
- [ ] Call overlay: video grid, mute indicators, speaker highlight
- [ ] Command palette: background, result items, category headers
- [ ] User settings modal: all form sections
- [ ] Create channel modal
- [ ] Pinned messages view
- [ ] Full dark mode audit across all views

### 3-C Core Features — Messaging
- [ ] Direct messages: 1-on-1 conversations
- [ ] Group direct messages (up to N participants)
- [ ] Channels: public / private distinction
- [ ] Channel creation with name, description, private toggle
- [ ] Channel invites: add members by name/email
- [ ] Channel archive / leave / delete
- [ ] Message threading (reply in thread)
- [ ] Thread panel: full thread view without leaving channel
- [ ] Message reactions: emoji picker, reaction counts, who reacted tooltip
- [ ] Message editing (own messages, edit history visible)
- [ ] Message deletion (own messages, admin can delete any)
- [ ] Message pinning (pin important messages, pin list)
- [ ] @mentions: autocomplete, highlight in message, unread mention badge
- [ ] @channel / @here mentions
- [ ] #channel links (navigate to channel on click)
- [ ] User links (open DM on click)
- [ ] URL unfurling: link preview (title, description, image)
- [ ] Emoji in messages: `:smile:` shortcode autocomplete
- [ ] Markdown rendering: **bold**, _italic_, `code`, ```code block```, > quote
- [ ] File sharing: drag-drop into chat area
- [ ] File sharing: image inline preview
- [ ] File sharing: document/PDF download link
- [ ] File sharing: virus scan warning (placeholder)
- [ ] Message search: full-text across all channels
- [ ] Message bookmarks / saved items
- [ ] Message notifications: desktop push + in-app
- [ ] Notification preferences: per-channel, DM, mentions
- [ ] Do Not Disturb mode with schedule
- [ ] User presence: Online / Away / Do Not Disturb / Offline
- [ ] Custom status: emoji + text + expiry time
- [ ] User profile: name, title, timezone, contact info
- [ ] Unread tracking: scroll to first unread message
- [ ] "Mark as unread" on any message
- [ ] Jump to: jump to date, jump to message permalink
- [ ] Channel history: load older messages (infinite scroll upward)

### 3-D Core Features — Voice & Video Calls
- [ ] 1-on-1 voice call from DM
- [ ] 1-on-1 video call from DM
- [ ] Group voice call (channel huddle)
- [ ] Group video call (channel)
- [ ] Screen sharing (full screen or window)
- [ ] Call overlay: active speaker highlight
- [ ] Call overlay: participant grid / spotlight view toggle
- [ ] Mute / unmute audio
- [ ] Camera on/off
- [ ] Background blur / virtual background (WebRTC)
- [ ] Call recording (requires server-side SFU)
- [ ] Call noise cancellation
- [ ] Raise hand gesture
- [ ] In-call chat (continue messaging during call)
- [ ] End call / hang up for self
- [ ] End call for everyone (host only)
- [ ] Call quality indicator (signal strength display)
- [ ] STUN/TURN server configuration for NAT traversal

### 3-E API & Real-time Integration
- [ ] Socket.io connection management (auto-reconnect with exponential backoff)
- [ ] Presence heartbeat (ping every 30s)
- [ ] Message persistence: messages stored in backend, loaded on reconnect
- [ ] Message delivery receipts (sent → delivered → read)
- [ ] Typing indicators: show `User is typing...`
- [ ] File upload API: chunked upload for large files
- [ ] Signed URL download for file access
- [ ] `X-Org-Id` on all API requests for tenant isolation
- [ ] Gate JWT auth on WebSocket upgrade

### 3-F Performance
- [ ] Virtual scroll for message list (only render visible messages)
- [ ] Lazy load images (placeholder blur until loaded)
- [ ] Message list: don't re-render on new message (use stable keys)
- [ ] Channel switch: cache last 50 messages per channel in Zustand
- [ ] File preview: generate thumbnail server-side, load lazily
- [ ] WebRTC peer connection: proper cleanup on unmount

### 3-G Accessibility
- [ ] Chat message list: aria-live region for new messages
- [ ] Focus management: after sending a message, focus returns to input
- [ ] Call controls: all buttons keyboard accessible + labeled
- [ ] Emoji picker: keyboard navigable grid

### 3-H Mobile & Responsive
- [ ] Mobile: sidebar hidden by default, hamburger opens it
- [ ] Mobile: full-screen channel view
- [ ] Mobile: touch-to-react on messages (long press)
- [ ] Mobile: call UI optimized for portrait orientation
- [ ] Mobile: swipe back gesture to return to channel list

### 3-I Testing
- [ ] Unit: message formatting (markdown, mentions, emoji)
- [ ] Unit: Zustand store actions (send message, update presence)
- [ ] E2E: connect two browser instances, send message, verify receipt

### 3-J AI Features (Connect AI)
- [ ] Thread summarization: AI summarizes long channel threads into 3-5 bullets
- [ ] Smart notifications digest: daily AI summary of missed messages while away
- [ ] Response suggestions: AI suggests 3 quick replies based on message context
- [ ] Channel topic summarization: "catch me up on #general since yesterday"
- [ ] Meeting scheduler: AI parses "can we meet Thursday?" → suggests time slots
- [ ] Translation: AI translates messages in-line for multilingual teams
- [ ] Tone coach: warn before sending messages that may come across as harsh
- [ ] Action item extraction: AI detects commitments in messages ("I'll send that by Friday")
- [ ] Smart search: natural language search ("messages from Ana about the budget last week")
- [ ] Bot framework: add AI-powered bots to channels (slash command triggers)

### 3-K Cross-App Integrations
- [ ] Meet: "Start huddle/call" from any DM or channel → launches Meet room
- [ ] Atlas: `@mention` a task/project in a message → rich preview card
- [ ] Calendar: event reminders posted to relevant channel 15 min before
- [ ] Planet: deal updates from Planet posted to sales channel automatically
- [ ] Mail: forward email to Connect channel (email → message conversion)
- [ ] Writer: share document link → rich preview with title + description
- [ ] Secure: security alerts from Secure posted to #security-alerts channel
- [ ] Control Center: critical ops alerts → Connect DM to on-call person
- [ ] EventBus: emit `message.sent`, `channel.created` events
- [ ] EventBus: consume events → post formatted notifications to designated channels

### 3-L Security & Compliance
- [ ] End-to-end encryption for DMs (Signal Protocol or equivalent)
- [ ] All messages encrypted at rest
- [ ] Message retention policies: org-configurable (30/90/365 days / forever)
- [ ] eDiscovery: admin can search and export messages by date range, user, channel
- [ ] Data Loss Prevention (DLP): detect credit card numbers, SSNs in messages and warn
- [ ] Guest access: external users can join specific channels with limited permissions
- [ ] Message edit/delete audit: original content retained in audit log
- [ ] No message content in error logs or Sentry
- [ ] GDPR: user data export includes all messages sent by user
- [ ] GDPR: right-to-erasure: delete user messages on account deletion request

### 3-M i18n
- [ ] All UI strings in translation files
- [ ] Timestamps: locale-aware relative and absolute formats
- [ ] RTL: message bubbles, sidebar, channel list layout flip for ar/he
- [ ] Emoji picker: full Unicode 15 support regardless of locale
- [ ] @mention autocomplete: works with non-Latin character names

### 3-N Accessibility (Additional)
- [ ] Message list: keyboard navigation between messages
- [ ] Keyboard shortcut: `Alt+Up/Down` navigate channels, `Enter` to open
- [ ] Emoji reactions: keyboard accessible (tab to reaction button, enter to react)
- [ ] File upload: dropzone has keyboard-accessible "Choose file" button
- [ ] Screen reader: announce new messages in active channel via aria-live="polite"
- [ ] Video call controls: all labeled, keyboard accessible

---

## 4 Meet — Video Conferencing

> **Stack:** React 19.2.0 · Vite 7.3.1 · Router v7 · Tailwind (no config visible) · LiveKit · Framer Motion
> **Routes:** 8 · **Status:** ~60% feature complete

### 4-A Design System Integration
- [x] Anti-FOUC script in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Google Fonts Inter removed
- [ ] `index.css` — import orbit-tokens.css
- [ ] Configure Tailwind (no tailwind.config.js found — add orbit preset)
- [ ] Meet uses Material Symbols icons — migrate to Lucide React for consistency
- [ ] Replace hardcoded lobby form colors with semantic tokens
- [ ] Replace hardcoded meeting controls colors with semantic tokens
- [ ] Adopt `<Button>` for all action buttons (join, leave, mute, camera)
- [ ] Adopt `<Avatar>` for participant thumbnails
- [ ] Adopt `<Badge>` for hand-raise indicator, recording indicator
- [ ] Adopt `<Tooltip>` on all control buttons
- [ ] Adopt `<Spinner>` for joining/loading state
- [ ] Adopt `<Modal>` for settings, invite, end-meeting dialogs
- [ ] Adopt `<EmptyState>` for empty participants panel

### 4-B Dark Mode
- [ ] Pre-join lobby: device preview, device selectors, form fields
- [ ] Active meeting: video grid background, participant labels
- [ ] Meeting controls bar: button states, icon colors
- [ ] Chat panel (in-meeting): message bubbles, input area
- [ ] Participants list panel: user rows, mute/unmute indicators
- [ ] Screen share view: border, controls overlay
- [ ] Post-meeting recap: notes, action items, recording link
- [ ] Full dark mode default (meetings often in dark environments)

### 4-C Core Features — Pre-Join Lobby
- [ ] Camera preview before joining
- [ ] Microphone level indicator (audio visualizer)
- [ ] Device selection: camera, microphone, speaker
- [ ] Device test: play test sound
- [ ] Join name display (pre-filled from auth, editable as guest)
- [ ] Join with audio muted toggle
- [ ] Join with video off toggle
- [ ] Background blur toggle in lobby
- [ ] Virtual background selection in lobby
- [ ] Meeting passcode entry (for protected meetings)
- [ ] Bandwidth test / connection quality indicator

### 4-D Core Features — Active Meeting
- [ ] Video grid: thumbnail layout for 2-8 participants
- [ ] Video grid: gallery view (equal tiles, 3×3 max)
- [ ] Video grid: spotlight view (speaker large, others small)
- [ ] Active speaker detection (highlight current speaker)
- [ ] Mute / unmute toggle (keyboard shortcut: `M`)
- [ ] Camera on/off toggle (keyboard shortcut: `V`)
- [ ] Screen share: start/stop (keyboard shortcut: `Shift+S`)
- [ ] Screen share: choose window or full screen
- [ ] Screen share: annotation tools overlay
- [ ] Hand raise: raise/lower hand button
- [ ] Raise hand queue: host sees order of raised hands
- [ ] In-meeting chat: open/close chat panel
- [ ] In-meeting chat: message badge for unread count
- [ ] Participants panel: list, mute all, admit from waiting room
- [ ] Waiting room: host approves guests before they join
- [ ] Recording: start/stop recording (notify all participants)
- [ ] Recording: download recording after meeting ends
- [ ] Captions / live transcription (LiveKit AI transcription)
- [ ] Meeting lock: prevent new participants from joining
- [ ] End meeting: for self only vs. for everyone
- [ ] Meeting timer display
- [ ] Network quality indicator per participant

### 4-E Core Features — Post-Meeting
- [ ] Auto-generated meeting summary
- [ ] Action items extracted from transcript
- [ ] Meeting recap shared to connected Calendar event
- [ ] Recording stored and linked to meeting
- [ ] Participants list saved
- [ ] Share recap via Mail

### 4-F LiveKit & API Integration
- [ ] LiveKit token generation from backend (`/api/meetings/:id/token`)
- [ ] Meeting creation API (`POST /api/meetings`)
- [ ] Participant management API
- [ ] Recording API (`POST /api/meetings/:id/recording`)
- [ ] Gate JWT for authenticated meetings
- [ ] Guest link generation (share link without auth)

### 4-G Performance
- [ ] Lazy load screen share library (only load when activated)
- [ ] Participant video: adaptive bitrate based on visible tile size
- [ ] Meeting page loads < 2s (pre-join lobby fast path)

### 4-H Accessibility
- [ ] All controls labeled (mute = "Mute microphone", not just mic icon)
- [ ] Keyboard navigation through control bar
- [ ] ARIA live region for participant join/leave announcements
- [ ] Captions visible and positioned correctly

### 4-I Mobile & Responsive
- [ ] Mobile: portrait and landscape meeting layouts
- [ ] Mobile: simplified controls (mute, camera, end as primary)
- [ ] Mobile: speaker view default on mobile
- [ ] Mobile: swipe to open chat / participants

### 4-J Testing
- [ ] Unit: device enumeration (mock MediaDevices)
- [ ] Unit: participant layout calculation
- [ ] Integration: LiveKit room connection mock
- [ ] E2E: two browsers join same room, verify audio/video state

### 4-K AI Features (Meet AI)
- [ ] Live transcription: real-time speech-to-text during meeting (LiveKit AI / Whisper)
- [ ] Speaker diarization: attribute transcript lines to correct speaker
- [ ] Auto-generated meeting summary: key points, decisions, blockers
- [ ] Action item extraction: AI detects commitments in transcript ("John will send by Monday")
- [ ] Follow-up email draft: AI generates follow-up email with summary + action items
- [ ] Smart chapter markers: AI segments recording into topics with timestamps
- [ ] Noise suppression: AI background noise cancellation
- [ ] Virtual backgrounds: AI-powered background blur and replacement
- [ ] Meeting sentiment: AI scores overall meeting tone (engaged / neutral / tense)
- [ ] Post-meeting Q&A: ask AI questions about the meeting ("What did we decide about pricing?")

### 4-L Cross-App Integrations
- [ ] Calendar: Meet rooms linked to Calendar events (join button in event detail)
- [ ] Calendar: meeting recap auto-updates linked Calendar event with notes
- [ ] Connect: meeting recordings and summaries shareable to Connect channels
- [ ] Writer: meeting notes auto-saved as Writer document linked to event
- [ ] Atlas: action items extracted from meeting auto-created as Atlas tasks
- [ ] Control Center: meeting metrics (duration, attendance) feed into Control Center analytics
- [ ] Mail: post-meeting follow-up email sent via Mail integration
- [ ] EventBus: emit `meeting.started`, `meeting.ended`, `meeting.recorded` events

### 4-M Security & Compliance
- [ ] Meeting recordings encrypted at rest and in transit
- [ ] Meeting access control: only invited participants (or org members for open meetings)
- [ ] Waiting room: mandatory for external guests
- [ ] Recording consent notification: all participants notified when recording starts
- [ ] Recording retention policy: org-configurable (30/90/365 days)
- [ ] Meeting data residency: recordings stored in org's configured region
- [ ] No meeting content in logs (transcript snippets treated as PII)
- [ ] GDPR: user can request deletion of their meeting recordings and transcript data

### 4-N i18n
- [ ] All UI strings in translation files
- [ ] Live captions: support multiple languages (Whisper multilingual model)
- [ ] Meeting duration and time displays: locale-aware formatting
- [ ] RTL: meeting controls and panels layout for ar/he locales

### 4-O Observability
- [ ] Meeting join latency tracked (time from click to audio/video active)
- [ ] Per-participant network quality metrics logged
- [ ] Recording processing latency tracked (end of meeting → recording available)
- [ ] AI transcription accuracy tracked (error rate via sampling)
- [ ] Sentry: LiveKit connection errors tracked with room + participant context

---

## 5 Calendar — Scheduling

> **Stack:** React 18.3.1 · Vite 5.3.1 · Router · Tailwind v3 · Axios
> **Routes:** 3 main views · **Status:** ~55% feature complete
> ⚠️ `App.tsx` is 19K+ lines — needs code splitting

### 5-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Google Fonts removed
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Split `App.tsx` into separate route components (top priority)
- [ ] Replace hardcoded calendar grid colors with semantic tokens
- [ ] Replace custom time slot colors with orbit color scale
- [ ] Replace custom `Modal` (event creation) with `<Modal>`
- [ ] Replace custom `Avatar` for attendee list with `<Avatar>`
- [ ] Replace custom `Badge` (event type) with `<Badge>`
- [ ] Replace custom `Tabs` (calendar/tasks/team) with `<Tabs>`
- [ ] Replace custom task status badges with `<Badge>`
- [ ] Adopt `<Dropdown>` for event context menu (edit/delete/copy)
- [ ] Adopt `<EmptyState>` for no events, no tasks
- [ ] Adopt `<Skeleton>` for loading calendar grid

### 5-B Dark Mode
- [ ] Calendar grid: weekend highlight, today highlight, past dates
- [ ] Event chips: all color variants in dark mode
- [ ] Event creation/edit modal: all form fields
- [ ] Time slot hover state
- [ ] Task list pane: priority badges, status chips
- [ ] Team availability grid
- [ ] Mini calendar sidebar
- [ ] AI Assistant panel

### 5-C Core Features — Calendar Views
- [ ] Month view: full month grid with event chips
- [ ] Week view: 7-column time grid (15-min slots)
- [ ] Day view: single-column time grid
- [ ] Agenda view: list of upcoming events
- [ ] Multi-day event spanning across columns
- [ ] All-day events row at top of week/day view
- [ ] Drag-to-create event (click and drag time range)
- [ ] Drag-to-move event (drag existing event to new time)
- [ ] Drag-to-resize event (resize event duration)
- [ ] Event categories / calendars (personal, work, holidays)
- [ ] Calendar color coding (each calendar has a color)
- [ ] Show/hide specific calendars
- [ ] Today button (jump to current date)
- [ ] Next/prev navigation (week/month/day)
- [ ] Timezone display (show events in user's local timezone)
- [ ] Multiple timezone columns (side-by-side for global teams)
- [ ] Working hours shading (outside hours greyed out)
- [ ] Recurring events (daily, weekly, monthly, custom RRULE)
- [ ] Recurring event edit: this event only / this and following / all

### 5-D Core Features — Event Management
- [ ] Quick event creation (click on time slot → popover)
- [ ] Full event form: title, date/time, location, description
- [ ] Event attendees: add by email/name, see availability
- [ ] Event attendees: RSVP status (accepted/declined/tentative)
- [ ] Event location: text or Google Maps link
- [ ] Event video link: auto-link to Meet meeting
- [ ] Event reminders: email, push, 15/30/60 min before
- [ ] Event color / category assignment
- [ ] Private event flag
- [ ] Event copy / duplicate
- [ ] Event sharing (public URL for external guests)
- [ ] iCal export (download .ics file)
- [ ] External calendar import (subscribe to iCal URL)
- [ ] Google Calendar sync (bidirectional)

### 5-E Core Features — Task Management
- [ ] Task list panel (to-do items separate from calendar events)
- [ ] Task: title, due date, priority (High/Med/Low), assignee, tags
- [ ] Task: link to calendar event
- [ ] Task completion toggle
- [ ] Task drag to calendar (creates time block)
- [ ] Task overdue highlighting
- [ ] Task view: filter by priority, status, assignee

### 5-F Core Features — Team Features
- [ ] Team availability grid (free/busy view)
- [ ] Find a time (suggest meeting slots when all attendees are free)
- [ ] Overlay team member calendars
- [ ] Scheduling link (share link for others to book a slot with you)

### 5-G API Integration
- [ ] Events CRUD (`GET/POST/PUT/DELETE /api/events`)
- [ ] Recurring events: server-side expansion with RRULE
- [ ] Attendee availability API
- [ ] Real-time updates: event changes via SSE / WebSocket
- [ ] Timezone normalization on all date fields (ISO 8601 with tz)

### 5-H Code Quality
- [ ] Split `App.tsx` (19K lines) into CalendarView, TasksView, TeamView, EventModal, TaskModal components
- [ ] Extract date utility functions to `src/utils/date.ts`
- [ ] Extract API calls to `src/api/` layer
- [ ] Add TypeScript types for CalendarEvent, Task, CalendarSettings

### 5-I Performance
- [ ] Virtualize long event lists (agenda view)
- [ ] Only load visible month's events (paginate by month)
- [ ] Memoize calendar grid (re-render only on date/event change)
- [ ] Lazy load Team view (heavy availability calculation)

### 5-J Mobile & Responsive
- [ ] Mobile: agenda view as default (not month grid)
- [ ] Mobile: swipe left/right to change week
- [ ] Mobile: bottom sheet for event creation
- [ ] Mobile: event detail drawer (from bottom)

### 5-K AI Features (Calendar AI)
- [ ] Scheduling assistant: "Find a time for a 1-hour meeting with Ana and Ben this week"
- [ ] Conflict resolution: AI suggests reschedule options when conflicts detected
- [ ] Agenda preparation: AI generates agenda based on meeting title + attendees
- [ ] Smart scheduling links: AI picks optimal slots based on attendee working hours + preferences
- [ ] Focus time blocks: AI suggests blocking "deep work" time based on calendar patterns
- [ ] Meeting acceptance suggestions: AI scores meeting invites (priority / can skip / delegate)
- [ ] Weekly planning brief: AI generates Monday morning summary of the week ahead
- [ ] Time allocation insights: "You spent 60% of last week in meetings — here's how to reduce it"
- [ ] Recurring meeting optimization: AI flags recurring meetings with low attendance

### 5-L Cross-App Integrations
- [ ] Meet: Calendar events with video link auto-launch Meet room at start time
- [ ] Atlas: project milestones appear as Calendar events (read-only from Atlas)
- [ ] Connect: event reminders posted to relevant Connect channel
- [ ] Planet: customer meetings created from Planet deals appear in Calendar
- [ ] Mail: meeting invites received in Mail → accept/decline from Mail → reflects in Calendar
- [ ] Control Center: team calendar aggregated in Control Center calendar view
- [ ] TurboTick: sprint start/end dates appear as Calendar events
- [ ] EventBus: emit `event.created`, `event.updated`, `event.cancelled` events
- [ ] EventBus: consume `meeting.started` → update event status to "In Progress"

### 5-M Security & Compliance
- [ ] Calendar data encrypted at rest
- [ ] Attendee email addresses not exposed in API responses beyond org scope
- [ ] External calendar sync (Google): OAuth token stored encrypted, refresh securely
- [ ] iCal subscription URLs: signed tokens (not guessable)
- [ ] Private events: only creator and invited attendees can see title + details
- [ ] GDPR: user data export includes all calendar events created by user
- [ ] GDPR: event deletion on account removal

### 5-N Accessibility
- [ ] Calendar grid: keyboard navigation (arrow keys to move dates, Enter to open event)
- [ ] Event creation via keyboard (no mouse required)
- [ ] All interactive elements have aria-labels
- [ ] Color-coded calendars: pattern fills for color-blind users (not color only)
- [ ] Date picker: ARIA calendar widget role with keyboard support
- [ ] Screen reader: announce current view (month/week/day) and selected date

### 5-O Testing (Additional)
- [ ] Unit: RRULE parsing and expansion for recurring events
- [ ] Unit: timezone conversion edge cases (DST transitions)
- [ ] Unit: conflict detection algorithm
- [ ] E2E: create event with attendees → verify invite sent → RSVP flow
- [ ] E2E: drag-to-move event → verify new time persisted
- [ ] Performance test: render month view with 200+ events

### 5-P i18n
- [ ] All UI strings in translation files
- [ ] First day of week: locale-aware (Monday for EU, Sunday for US)
- [ ] Date format: DD/MM/YYYY vs MM/DD/YYYY per locale
- [ ] Month and day names: translated for all 9 supported languages
- [ ] RTL: calendar grid layout flips for ar/he (right-to-left week progression)
- [ ] Time format: 12h vs 24h per locale preference

---

## 6 Writer — Document Editor

> **Stack:** React 19.2.0 · Vite 7.3.1 · Router v7 · Zustand · FastAPI backend · Tailwind v3
> **Routes:** 3 · **Status:** ~40% feature complete

### 6-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Material Symbols removed
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Replace custom `Sidebar` with `<Sidebar>` from `@orbit-ui/react`
- [ ] Replace custom `Modal` with `<Modal>`
- [ ] Adopt `<Button>` for toolbar actions
- [ ] Adopt `<Dropdown>` for block type selector, more actions
- [ ] Adopt `<Tooltip>` on toolbar buttons
- [ ] Adopt `<EmptyState>` for no documents in dashboard
- [ ] Adopt `<Skeleton>` for loading document list
- [ ] Adopt `<Badge>` for document status (draft/published), word count

### 6-B Dark Mode
- [x] Dashboard: document card list, sidebar, search bar (semantic token migration)
- [ ] Editor: text body background, toolbar, margins
- [ ] Toolbar: button hover/active states
- [ ] Block handles: slash command menu
- [ ] Inline comments panel
- [ ] Version history panel
- [x] Sheets view: cell backgrounds, borders — uses semantic tokens

### 6-C Core Features — Document Dashboard
- [ ] Document list: grid and list view toggle
- [ ] Document list: sort by name / modified / created
- [ ] Document list: filter by status (draft/published/archived)
- [ ] Document list: search by title
- [ ] Document creation: blank, from template
- [ ] Document duplication
- [ ] Document archiving / deletion
- [ ] Folder organization (nested folders)
- [ ] Favorites / starred documents
- [ ] Recent documents widget
- [ ] Shared with me / all documents toggle

### 6-D Core Features — Block Editor
- [ ] Block types: paragraph, heading 1/2/3, bulleted list, numbered list
- [ ] Block types: checkbox list (todo), quote, divider
- [ ] Block types: code block (with syntax highlighting)
- [ ] Block types: image (upload + paste + URL)
- [ ] Block types: embed (video URL, iFrame)
- [ ] Block types: callout (info, warning, tip boxes)
- [ ] Block types: table (basic grid)
- [ ] Block types: math equation (LaTeX)
- [ ] Block drag-and-drop reordering
- [ ] Slash `/` command palette (type to filter block types)
- [ ] Inline formatting: bold, italic, underline, strikethrough, code
- [ ] Inline formatting: text color, background highlight
- [ ] Inline links: create, edit, remove
- [ ] Inline mentions: @mention users
- [ ] Inline page links: @ link to other documents
- [ ] Inline comments: highlight text → add comment
- [ ] Comment resolution (mark comment as resolved)
- [ ] Undo/redo stack (50+ levels)
- [ ] Selection multi-block operations (select multiple blocks → change type)
- [ ] Keyboard shortcuts: `Cmd+B` bold, `Cmd+I` italic, `Cmd+K` link, `Cmd+Z` undo
- [ ] Auto-save (debounced 1s after last keystroke)
- [ ] Save indicator ("Saved" / "Saving..." / "Unsaved changes")

### 6-E Core Features — Collaboration
- [ ] Real-time collaborative editing (Yjs + WebSocket provider)
- [ ] Cursor presence: see where other users are editing
- [ ] User cursor labels (name badge next to cursor)
- [ ] Conflict resolution: CRDT-based (Yjs handles this)
- [ ] Offline editing: local buffer, sync when reconnected
- [ ] Version history: named versions ("Version 1.0")
- [ ] Version history: auto-versions every hour
- [ ] Version diff view: side-by-side or inline diff
- [ ] Restore to version
- [ ] Comments & suggestions mode (like Google Docs)
- [ ] Page-level sharing: who can view/edit
- [ ] Share link with permission level

### 6-F Core Features — Sheets (Spreadsheet)
- [x] Grid: column/row headers, multi-sheet tabs
- [x] Cell editing: text, numbers, dates (double-click)
- [ ] Formula support: SUM, AVERAGE, COUNT, IF, VLOOKUP basics
- [ ] Cell formatting: bold, italic, alignment, bg color
- [ ] Column/row insert/delete
- [x] Multi-cell select + bulk delete
- [ ] Import CSV
- [x] Export to CSV

### 6-G API Integration
- [ ] Document CRUD fully implemented with FastAPI
- [ ] Block API: create/update/delete blocks with order
- [ ] Version history API
- [ ] WebSocket room for collaborative editing (`/ws/documents/:id`)
- [ ] `X-Workspace-Id` header on all requests
- [ ] File upload API for image blocks (MinIO backend)

### 6-H Performance
- [ ] Block renderer: only re-render changed blocks (React.memo)
- [ ] Virtual scroll for document with 500+ blocks
- [ ] Lazy load code block syntax highlighter
- [ ] Lazy load math equation renderer

### 6-I Mobile & Responsive
- [ ] Mobile: full-screen editor (hide sidebar)
- [ ] Mobile: floating toolbar on selection
- [ ] Mobile: simplified toolbar (most-used actions only)

### 6-J Testing
- [ ] Unit: block ordering / drag-and-drop logic
- [ ] Unit: slash command filtering
- [ ] E2E: create document → add blocks → save → reload and verify

### 6-K AI Features (Writer AI)
- [ ] AI compose: generate document from title or outline prompt
- [ ] Continue writing: AI extends selected paragraph naturally
- [ ] Summarize: condense selected text or entire document to N bullets
- [ ] Improve writing: rewrite selected text for clarity, grammar, conciseness
- [ ] Tone adjustment: make selected text more formal / casual / persuasive
- [ ] Generate TOC: AI creates table of contents from document headings
- [ ] Extract action items: AI identifies tasks and decisions in document
- [ ] Translate document: AI translates entire document to target language
- [ ] Grammar & spell check: inline AI suggestions (underline + suggestion on click)
- [ ] AI chat sidebar: "ask anything about this document" Q&A interface
- [ ] Template generation: describe desired doc type → AI generates structured template
- [ ] Code explanation: select code block → AI explains what it does

### 6-L Cross-App Integrations
- [ ] Atlas: link Writer document to Atlas task — shows doc in task detail
- [ ] Meet: meeting notes auto-created as Writer doc linked to Calendar event
- [ ] Mail: attach Writer document link in email compose (auto-inserts shareable URL)
- [ ] Connect: share document to Connect channel → rich preview card
- [ ] Planet: proposal/contract documents linked to Planet deals
- [ ] TurboTick: technical spec documents linked to TurboTick epics
- [ ] EventBus: emit `document.created`, `document.published` events

### 6-M Security & Compliance
- [ ] Document content encrypted at rest
- [ ] Sharing permissions enforced server-side (not just UI)
- [ ] Public share links: revocable, optional password protection, optional expiry
- [ ] Version history retained for minimum 90 days
- [ ] File uploads in documents: virus scanned, MIME type whitelist
- [ ] No document content in error logs
- [ ] GDPR: document export on user request
- [ ] GDPR: document deletion on account removal (with transfer-to-org option)

### 6-N Accessibility
- [ ] Block editor: full keyboard operation (no mouse required for editing)
- [ ] Slash command menu: keyboard navigable (arrow keys + enter)
- [ ] Inline formatting toolbar: keyboard accessible (appears on selection, tab-navigable)
- [ ] All toolbar icons have aria-labels
- [ ] Comments panel: keyboard accessible (tab to comment, reply, resolve)
- [ ] Screen reader: announce autosave state changes

### 6-O i18n
- [ ] All UI strings in translation files
- [ ] Document timestamps: locale-aware relative and absolute formats
- [ ] RTL: editor text direction follows document language setting (auto-detect or manual)
- [ ] Code blocks: syntax highlighting works for all languages regardless of UI locale
- [ ] Word count: locale-aware number formatting

### 6-P Observability
- [ ] Track document load time (time to first editable block)
- [ ] Track collaboration session health (Yjs connection state, conflict count)
- [ ] AI feature usage tracked per feature type (compose/summarize/improve)
- [ ] Autosave failure rate tracked and alerted

---

## 7 Planet — CRM & Sales

> **Stack:** React 19.2.3 · Vite 7.2.4 · Context-based nav · Tailwind v4 · Zustand · FastAPI
> **Pages:** 9 · **Status:** ~30% feature complete (mostly stubs)

### 7-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Google Fonts removed
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] `index.css` — add `@import "/orbit-ui/orbit-tailwind-v4.css";` (TW v4 app)
- [ ] Remove hardcoded color values in all 9 page stubs
- [ ] Adopt `<Sidebar>` for the collapsible nav (`<SidebarItem>` for each page)
- [ ] Adopt `<Button>` for all CTA buttons
- [ ] Adopt `<Badge>` for deal stage, lead status, priority
- [ ] Adopt `<Card>` for KPI tiles, pipeline cards
- [ ] Adopt `<Table>` (when built) for contact/deal lists
- [ ] Adopt `<Avatar>` for contact profile pictures, rep assignments
- [ ] Adopt `<Tabs>` for record detail (overview/activity/notes tabs)
- [ ] Adopt `<EmptyState>` for empty pipeline, no contacts, no reports
- [ ] Adopt `<Skeleton>` for loading dashboard KPIs
- [ ] Adopt `<Progress>` for deal stage progress bar, quota attainment

### 7-B Dark Mode
- [ ] Dashboard KPI cards
- [ ] Sales pipeline (kanban-style columns)
- [ ] Contact/lead list table
- [ ] Deal detail view
- [ ] Analytics charts (use CSS variable colors for chart datasets)
- [ ] Predictions/forecasting panel
- [ ] Network graph visualization
- [ ] Reports builder
- [ ] User management table
- [ ] Audit log table

### 7-C Core Features — Dashboard
- [ ] KPI cards: total revenue, open deals, win rate, avg deal size
- [ ] KPI cards: period comparison (vs. last month / quarter)
- [ ] Revenue chart: monthly trend (line chart)
- [ ] Pipeline funnel chart
- [ ] Top performers leaderboard
- [ ] Recent activity feed (deals updated, contacts added)
- [ ] Quick actions: add contact, add deal, log activity

### 7-D Core Features — Pipeline Management
- [ ] Deal stages: customizable columns (Kanban board)
- [ ] Deal card: company, value, expected close date, probability
- [ ] Deal card: assigned rep avatar
- [ ] Drag deals between stages
- [ ] Deal stage automation rules (trigger actions on stage change)
- [ ] Deal filters: by rep, stage, date range, value range
- [ ] Deal list view (table alternative to kanban)
- [ ] Deal detail: full record with timeline, notes, files, tasks
- [ ] Deal linking to contact and company
- [ ] Deal probability weighting (by stage or custom)
- [ ] Won/Lost deal logging with reason
- [ ] Weighted pipeline value calculation

### 7-E Core Features — Contacts & Companies
- [ ] Contact list: search, filter, sort
- [ ] Contact record: name, email, phone, company, role, social links
- [ ] Contact record: activity timeline (calls, emails, meetings)
- [ ] Contact record: linked deals
- [ ] Contact record: notes + tasks
- [ ] Company record: domain, industry, size, revenue range
- [ ] Company linked contacts list
- [ ] Company linked deals
- [ ] Contact import via CSV
- [ ] Duplicate detection and merge
- [ ] Contact export (CSV, vCard)

### 7-F Core Features — Analytics & Predictions
- [ ] Revenue forecast (weighted pipeline sum by close month)
- [ ] Win/loss rate by stage, rep, product
- [ ] Sales velocity (avg days per stage)
- [ ] Quota attainment per rep
- [ ] Activity metrics (calls, emails, meetings per rep)
- [ ] AI predictions: deal win probability scores
- [ ] AI predictions: churn risk indicators for existing customers
- [ ] Network visualization: customer/partner/prospect relationships

### 7-G Core Features — Reports
- [ ] Report builder: choose metrics, dimensions, date range
- [ ] Chart types: bar, line, pie, table
- [ ] Saved reports library
- [ ] Scheduled email reports
- [ ] Export report as PDF / CSV

### 7-H Core Features — User Management & RBAC
- [ ] Roles: Admin, Manager, Sales Rep, Read-only
- [ ] Role-based page access (already in `hasPermission` check)
- [ ] User invitation by email
- [ ] Territory assignment (reps own specific contact segments)
- [ ] Audit log: all CUD operations logged with actor, timestamp

### 7-I API Integration
- [ ] All 9 pages connected to FastAPI backend
- [ ] Org-scoped queries (`/api/orgs/{orgId}/...`)
- [x] Pagination on all list endpoints
- [ ] Search API (debounced, full-text)
- [ ] `X-Org-Id` + Bearer token on all requests
- [ ] Real-time deal updates via EventBus SSE

### 7-J Performance
- [ ] Virtual scroll on contact/deal tables (potentially thousands of records)
- [ ] Debounce search (300ms)
- [ ] Memoize chart computations
- [ ] Lazy load Network graph library (D3 or cytoscape)

### 7-K AI Features (Planet AI)
- [ ] Lead scoring: AI scores contacts 0-100 based on engagement + firmographic data
- [ ] Deal win probability: AI predicts % chance of closing each deal
- [ ] Next-best-action: AI recommends next step for each deal (call / email / proposal)
- [ ] Churn risk: AI flags existing customers showing disengagement signals
- [ ] Pipeline forecast: AI projects end-of-quarter revenue based on deal probabilities
- [ ] Email drafting: compose follow-up emails from deal context
- [ ] Meeting prep brief: AI generates 1-page summary before a customer call
- [ ] Competitive intelligence: AI analyzes loss reasons and surfaces patterns
- [ ] ICP matching: AI scores inbound leads against Ideal Customer Profile
- [ ] Natural language reporting: "How many deals did we close last quarter worth >$50K?"

### 7-L Cross-App Integrations
- [ ] Mail: emails from Planet contacts auto-link to their CRM record activity timeline
- [ ] Calendar: schedule meeting from Planet deal → creates Calendar event + Meet room
- [ ] Connect: deal won notification posted to #sales channel in Connect
- [ ] Atlas: won deal → auto-create onboarding project in Atlas from template
- [ ] Writer: proposal document linked to Planet deal record
- [ ] Control Center: open pipeline and deal metrics feed into Control Center dashboard
- [ ] Capital Hub: closed won deal value flows into Capital Hub revenue tracking
- [ ] TurboTick: customer bug reports from Planet linked to TurboTick issues
- [ ] EventBus: emit `deal.created`, `deal.stage_changed`, `deal.won`, `deal.lost` events
- [ ] EventBus: consume `invoice.paid` (from Capital Hub) → update deal to "Paid"

### 7-M Security & Compliance
- [ ] Customer PII (email, phone) encrypted at rest
- [ ] GDPR: contact deletion / anonymization on request
- [ ] GDPR: contact data export (JSON/CSV) on request
- [ ] Row-level security: reps only see their assigned contacts/deals (unless Manager+)
- [ ] Audit log: all contact/deal CUD operations with actor + timestamp
- [ ] Data import validation: CSV imports sanitized and validated before DB insert
- [ ] No customer PII in frontend logs or Sentry events

### 7-N Accessibility
- [ ] Kanban board: keyboard drag-and-drop for deals between stages
- [ ] Deal detail: keyboard navigable tabs (overview/activity/notes)
- [ ] Contact list: keyboard navigation, sortable columns accessible
- [ ] Status badges: text label always present (not color alone)
- [ ] Charts: accessible text descriptions / data tables as fallback

### 7-O Testing
- [ ] Unit: deal probability calculation
- [ ] Unit: pipeline value aggregation
- [ ] Unit: AI lead scoring mock
- [ ] E2E: create contact → create deal → move deal stage → mark won
- [ ] E2E: import contacts from CSV → verify data accuracy

### 7-P i18n
- [ ] All UI strings in translation files
- [ ] Currency display: `Intl.NumberFormat` with currency code per org setting
- [ ] Date formats: locale-aware across all deal dates, activity timestamps
- [ ] RTL: kanban board and table layout for ar/he

---

## 8 Secure — Endpoint Security

> **Stack:** React 19.2.0 · Vite 7.3.1 · Router v7 · Tailwind v3 · Zustand · Playwright
> **Routes:** 9 · **Status:** ~45% feature complete

### 8-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Replace custom alert/banner with `<Alert>` from `@orbit-ui/react`
- [ ] Adopt `<Badge>` for severity (critical/high/medium/low/info)
- [ ] Adopt `<Progress>` for patch compliance percentage
- [ ] Adopt `<Table>` for endpoint inventory, vulnerability list
- [ ] Adopt `<Tabs>` in device detail (overview/vulnerabilities/patches/logs)
- [ ] Adopt `<Button>` for all action buttons
- [ ] Adopt `<Modal>` for device wipe confirmation, policy editor
- [ ] Adopt `<EmptyState>` for no vulnerabilities found, no endpoints
- [ ] Adopt `<Skeleton>` for loading endpoint list
- [ ] Adopt `<Sidebar>` for navigation

### 8-B Dark Mode
- [ ] Security overview: risk score gauge, threat level indicator
- [ ] Endpoint inventory table: status badges (online/offline/at-risk)
- [ ] Vulnerability list: severity color coding
- [ ] Patch management: installed/pending/failed status badges
- [ ] Policy editor
- [ ] Compliance checklist
- [ ] Audit log table
- [ ] Integration cards

### 8-C Core Features — Overview Dashboard
- [ ] Security posture score (0-100 gauge)
- [ ] Endpoint status summary: online, offline, at-risk counts
- [ ] Vulnerability summary: critical, high, medium, low counts
- [ ] Patch compliance rate (% of endpoints up to date)
- [ ] Recent incidents / alerts feed
- [ ] Threat timeline chart (incidents over last 30 days)
- [ ] Top 5 critical vulnerabilities callout
- [ ] Compliance framework coverage (SOC 2, GDPR, ISO 27001)

### 8-D Core Features — Endpoint Inventory
- [ ] Endpoint list: hostname, OS, IP, last seen, status, tags
- [ ] Endpoint search by hostname / IP
- [ ] Endpoint filter: by OS, status, compliance state, tags
- [ ] Endpoint detail: system info, installed software, network, users
- [ ] Endpoint detail: vulnerability list for that device
- [ ] Endpoint detail: patch history
- [ ] Endpoint detail: policy assignment
- [ ] Endpoint grouping by department / tag
- [ ] Remote actions: lock device, wipe device (admin + MFA required)
- [ ] Remote actions: push patch update
- [ ] Endpoint agent status: installed / pending / not installed

### 8-E Core Features — Vulnerability Management
- [ ] Vulnerability list: CVE ID, severity, CVSS score, affected endpoints count
- [ ] Vulnerability detail: description, impact, remediation steps, references
- [ ] Vulnerability timeline: when first/last seen
- [ ] Affected endpoints for each vulnerability
- [ ] Vulnerability filter: by severity, status (open/mitigated/accepted)
- [ ] Vulnerability accept risk (with expiry date and justification)
- [ ] Vulnerability assignment (assign to team member for remediation)
- [ ] Automated CVE feed integration (NVD / OSV)
- [ ] False positive flagging

### 8-F Core Features — Patch Management
- [ ] Available patches list: OS patches, application patches
- [ ] Patch detail: vendor, severity, release date, size
- [ ] Patch deployment: select endpoints → schedule deployment
- [ ] Patch deployment status: queued / in progress / success / failed
- [ ] Patch rollback option
- [ ] Patch policy: auto-approve critical patches
- [ ] Maintenance window configuration

### 8-G Core Features — Policies
- [ ] Policy templates: password policy, screen lock, encryption
- [ ] Policy editor: configure rules per policy
- [ ] Policy assignment: apply to endpoint groups
- [ ] Policy compliance check: is device meeting all rules?
- [ ] Non-compliant device alerts

### 8-H Core Features — Compliance
- [ ] Compliance frameworks: SOC 2, GDPR, ISO 27001, HIPAA
- [ ] Per-control status (passed / failed / in progress / N/A)
- [ ] Evidence attachment per control
- [ ] Audit-ready report generation (PDF export)
- [ ] Control assignment to team members

### 8-I Core Features — Logs
- [ ] Audit log: user actions (who did what, when, from where)
- [ ] Security events log: login attempts, policy violations
- [ ] Filter logs by: event type, user, date range, severity
- [ ] Log export (CSV, JSON)
- [ ] SIEM integration hook (Splunk, Datadog forwarding)

### 8-J API & Security
- [ ] All endpoints authenticated (Bearer token + org scoping)
- [ ] Device wipe endpoint requires MFA re-verification
- [ ] Vulnerability data fetched from backend CVE database
- [ ] Patch metadata from vendor APIs (proxied through backend)
- [ ] Audit log persisted to immutable append-only store

### 8-K Performance & Reliability
- [ ] Large endpoint tables: virtual scroll (1000+ devices)
- [ ] Polling for endpoint status updates (30s interval or WebSocket)
- [ ] Optimistic UI for quick actions (lock device)

### 8-L Testing
- [ ] Playwright E2E: view endpoint list, open device detail
- [ ] Playwright E2E: device wipe flow (requires MFA mock)
- [ ] Unit: CVE severity sorting logic

### 8-M AI Features (Secure AI)
- [ ] Anomaly detection: AI flags unusual login patterns, data access spikes
- [ ] Vulnerability prioritization: AI ranks CVEs by exploitability + asset criticality
- [ ] Patch impact prediction: AI estimates risk of applying patch (breaking change likelihood)
- [ ] Threat narrative: AI generates plain-English explanation of each CVE for non-technical stakeholders
- [ ] Policy recommendation: AI suggests hardening policies based on industry (SOC 2 / HIPAA profile)
- [ ] Incident response playbook: AI generates step-by-step remediation for detected threats
- [ ] Compliance gap analysis: AI analyzes current state and produces gap report vs. framework
- [ ] Natural language log search: "Show me all failed login attempts from new IPs last week"

### 8-N Cross-App Integrations
- [ ] Connect: critical security alerts → DM to security team channel
- [ ] Control Center: security posture score + incident count feeds into Control Center ops dashboard
- [ ] Gate: pull authentication events (failed logins, MFA failures) from Gate audit log
- [ ] EventBus: emit `security.incident`, `vulnerability.critical`, `policy.violation` events
- [ ] EventBus: consume `user.offboarded` → trigger endpoint wipe workflow
- [ ] Mail: compliance report sent via Mail to CISO on schedule

### 8-O i18n
- [ ] All UI strings in translation files
- [ ] CVE severity labels: localized
- [ ] Date/time in logs: locale-aware formatting
- [ ] Compliance framework labels: translated where official translations exist (GDPR is EU, etc.)

### 8-P Observability
- [ ] Track endpoint agent heartbeat latency (detect stale agents)
- [ ] Vulnerability scan completion rate tracked
- [ ] Patch deployment success/failure rate tracked per OS
- [ ] Compliance score trend chart (week-over-week)
- [ ] Sentry: critical security action failures (wipe, patch push) tracked with full context

---

## 9 Control Center — Operations Hub

> **Stack:** React 19.2.0 · Vite (TW v4) · Zustand · Axios · EventSource SSE · 17 views
> **Routes:** 17 views (Zustand-managed) · **Status:** ~55% feature complete

### 9-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Google Fonts removed
- [x] `index.css` imports `orbit-tokens.css` + `orbit-tailwind-v4.css`
- [x] `@orbit-ui/react` installed
- [ ] Replace all `#6366f1` (indigo) hardcoded colors with `primary-500`
- [ ] Replace all `outline: 2px solid #6366f1` with `focus-ring` utility
- [ ] Replace `::selection` hardcoded color with orbit primary
- [ ] Replace all scrollbar CSS with `.scrollbar-thin` plugin
- [ ] Adopt `<Sidebar>` from `@orbit-ui/react` (replace custom sidebar)
- [ ] Adopt `<Button>` for all action buttons
- [ ] Adopt `<Badge>` for notification types, meeting status
- [ ] Adopt `<Card>` for dashboard tiles, meeting cards
- [ ] Adopt `<Tabs>` for view switching (meetings/calendar/analytics)
- [ ] Adopt `<Modal>` for create meeting, settings dialogs
- [ ] Adopt `<EmptyState>` for no meetings, no notifications
- [ ] Adopt `<Skeleton>` for loading dashboard
- [ ] Adopt `<Toast>` replacing react-hot-toast

### 9-B Dark Mode
- [ ] Dashboard: all 17 views audited and using semantic tokens
- [ ] Replace `#f1f5f9` scrollbar track with `var(--orbit-surface-muted)`
- [ ] Replace `#cbd5e1` scrollbar thumb with `var(--orbit-border-strong)`
- [ ] EventBus notification cards: info/deal/success/warning/error variants
- [ ] Calendar view: event chips, time grid
- [ ] Analytics charts: dataset colors from CSS variables
- [ ] Operations view: metric cards
- [ ] Pulse view: real-time feed items

### 9-C Core Features — Dashboard
- [ ] Today's meeting count + next meeting countdown
- [ ] Team activity feed (cross-app events from EventBus)
- [ ] Action items due today widget
- [ ] Quick meeting creation button
- [ ] Recent activity: last 10 events from all Orbit apps
- [ ] Key metrics: projects active (Atlas), unread emails (Mail), deals in pipeline (Planet)

### 9-D Core Features — Meetings
- [ ] Meeting list: upcoming, today, past
- [ ] Meeting list: filter by creator, attendee, date
- [ ] Meeting creation: title, date/time, duration, attendees, agenda
- [ ] Meeting creation: auto-create Meet room and Calendar event
- [ ] Meeting detail: agenda, notes, recording link, attendees
- [ ] Meeting detail: action items assigned with owners
- [ ] Meeting edit / cancel
- [ ] Recurring meeting support

### 9-E Core Features — Calendar View
- [ ] Month/week/day calendar grid
- [ ] Events from Atlas (project milestones), Calendar app, Meet (scheduled meetings)
- [ ] Cross-app event aggregation via EventBus
- [ ] Create new event or meeting from calendar click

### 9-F Core Features — Analytics
- [ ] Meeting analytics: meetings per week, avg duration, no-show rate
- [ ] Team activity metrics: messages sent (Connect), tasks completed (Atlas)
- [ ] Cross-app engagement report
- [ ] Time tracking summary (from Atlas timesheets)

### 9-G Core Features — Operations
- [ ] Operations status board: active incidents, blockers, risks
- [ ] Department / team health overview
- [ ] Resource allocation view
- [ ] Budget utilization (Capital Hub integration)

### 9-H Core Features — Pulse (Real-time Feed)
- [ ] Live event stream from EventBus (SSE)
- [ ] Auto-reconnect EventSource (exponential backoff)
- [ ] Filter feed by event type (project / deal / calendar / mail)
- [ ] Mark events as seen / dismissed
- [ ] Notification bell: unread count badge
- [ ] Notification detail panel

### 9-I Core Features — People & Time
- [ ] Team members list with role, status (online/offline)
- [ ] Time cards: daily / weekly hours per member
- [ ] Overtime tracking and alerts
- [ ] PTO / leave calendar
- [ ] Posture: team working locations (in-office / remote / OOO)

### 9-J Core Features — Action Items & Notes
- [ ] Action items: title, owner, due date, status, linked meeting
- [ ] Action items created from meeting notes
- [ ] Sync action items to Atlas tasks
- [ ] Meeting notes: rich text, auto-save
- [ ] Notes search
- [ ] Notes export (PDF, Markdown)

### 9-K EventBus Integration
- [ ] SSE connection on app load (token + org_id params)
- [ ] Reconnect logic (EventSource.onerror → exponential backoff)
- [ ] Parse event types correctly (project.updated, deal.created, etc.)
- [ ] Show real-time toast for critical events
- [ ] All 6 event type categories handled: project, deal, calendar, mail, planet, connect

### 9-L Performance
- [ ] 17 views: all lazy-loaded (Suspense boundaries)
- [ ] EventSource: don't re-subscribe on view change
- [ ] Dashboard widgets: stale-while-revalidate pattern

### 9-M AI Features (Control Center AI)
- [ ] Executive briefing: AI daily summary of org-wide activity (deals, tasks, incidents, meetings)
- [ ] Meeting effectiveness score: AI rates meetings by agenda completion, action items generated
- [ ] Team workload analysis: AI flags overloaded team members based on task + meeting load
- [ ] Operations anomaly detection: AI spots KPI drops and alerts before they become critical
- [ ] Action item follow-up: AI tracks action items from meetings and sends nudges when overdue
- [ ] Natural language ops query: "What are the top 3 blockers across all teams this week?"
- [ ] Sprint retrospective assistant: AI generates retro insights from sprint data
- [ ] OKR progress analysis: AI predicts which OKRs are at risk of missing targets

### 9-N Cross-App Integrations
- [ ] Atlas: pull project status, task counts, sprint progress into Control Center dashboard
- [ ] Planet: pull open pipeline value, deals closing this month into dashboard
- [ ] Mail: unread email count widget in dashboard
- [ ] Calendar: today's meetings aggregated from Calendar
- [ ] Connect: unread message count + channel activity in dashboard
- [ ] Capital Hub: budget utilization and cash position pulled into ops dashboard
- [ ] Secure: security posture score widget in dashboard
- [ ] Meet: meeting recordings and summaries accessible from Control Center
- [ ] EventBus: ALL event types consumed and rendered in Pulse feed
- [ ] EventBus: emit `action_item.created`, `action_item.completed` events

### 9-O Security & Compliance
- [ ] Control Center reads from all other apps via service-to-service authenticated APIs
- [ ] Users only see data from apps they have access to (permission passthrough)
- [ ] Action items containing sensitive info: org-scoped, no cross-org leakage
- [ ] Audit log: who viewed which dashboard sections (for compliance reporting)
- [ ] GDPR: time card and people data purged on user deletion

### 9-P i18n
- [ ] All UI strings in translation files
- [ ] Dashboard KPI numbers: `Intl.NumberFormat` locale-aware
- [ ] Meeting duration display: locale-aware (e.g., "1h 30m" vs "1:30")
- [ ] Calendar view in Control Center: locale-aware date/time, first day of week
- [ ] RTL: all 17 views render correctly for ar/he

### 9-Q Accessibility
- [ ] Dashboard widgets: keyboard navigable, can tab between widgets
- [ ] All charts have accessible data tables as fallback
- [ ] Real-time feed (Pulse): aria-live="polite" for new items, not aria-live="assertive" (avoid interruption)
- [ ] 17 views: all navigable by keyboard from sidebar

### 9-R Testing
- [ ] Unit: EventBus event parsing for all 6 event categories
- [ ] Unit: meeting metrics calculation (avg duration, no-show rate)
- [ ] E2E: create meeting → verify it appears in Control Center meetings list
- [ ] E2E: action item created → synced to Atlas tasks
- [ ] Integration: SSE connection stays alive for 5+ minutes without reconnect

---

## 10 Capital Hub — Finance Dashboard

> **Stack:** React 19.2.0 · Vite 7.3.1 · Router v7 · Recharts · Tailwind v3
> **Routes:** 4 (Dashboard, Assets, Transactions, Reports) · **Status:** ~55% feature complete

### 10-A Design System Integration
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Adopt `<Sidebar>` for navigation
- [ ] Adopt `<Card>` for all financial KPI tiles
- [ ] Adopt `<Badge>` for status labels (on budget / over budget / at risk)
- [ ] Adopt `<Progress>` for budget utilization bars
- [ ] Adopt `<Table>` for transaction lists, budget line items
- [ ] Adopt `<Tabs>` for report sections
- [ ] Adopt `<EmptyState>` for no transactions, no accounts
- [ ] Adopt `<Skeleton>` for loading dashboard

### 10-B Dark Mode
- [ ] All dashboard chart backgrounds
- [ ] KPI card number colors
- [ ] Budget variance (positive = green, negative = red) in dark mode
- [ ] Table rows: alternating bg in dark mode
- [ ] Financial period selector

### 10-C Core Features — Dashboard
- [ ] Total Revenue KPI (current period vs. prior period)
- [ ] Total Expenses KPI
- [ ] Net Profit / EBITDA KPI
- [ ] Cash position (bank balance summary)
- [ ] Revenue trend chart (12 months, Recharts LineChart)
- [ ] Expense breakdown donut chart (by category)
- [ ] Budget vs. actual bar chart (by department)
- [ ] Recent transactions list (last 10)
- [ ] Outstanding invoices count + total amount
- [ ] Period selector: MTD / QTD / YTD / custom range

### 10-D Core Features — Analytics
- [ ] Revenue by product/service breakdown
- [ ] Customer revenue concentration (top 10 customers)
- [ ] MoM / YoY growth rates
- [ ] Gross margin trend
- [ ] Operating expenses as % of revenue trend

### 10-E Core Features — Budgeting
- [ ] Budget creation: period, departments, line items
- [ ] Budget approval workflow
- [ ] Budget vs. actuals table (line-by-line)
- [ ] Variance alerts (>10% over budget auto-flag)
- [ ] Budget forecasting (project end-of-period actuals)

### 10-F Core Features — Invoicing
- [ ] Invoice list: number, client, amount, due date, status
- [ ] Invoice creation: line items, tax, discount
- [ ] Invoice PDF generation and download
- [ ] Invoice status: draft / sent / paid / overdue
- [ ] Payment recording
- [ ] Overdue invoice reminders

### 10-G Core Features — Expenses
- [ ] Expense submissions (employee reports)
- [ ] Expense approval workflow (manager → finance)
- [ ] Receipt image upload and OCR
- [ ] Expense categories and cost center tagging
- [ ] Export to CSV / accounting software (QuickBooks format)

### 10-H Core Features — Accounts & Integrations
- [ ] Bank account connections (read-only balance feeds)
- [ ] Chart of accounts (COA) management
- [ ] Journal entries (double-entry bookkeeping)
- [ ] Financial statement generation (P&L, Balance Sheet, Cash Flow)
- [ ] Export financial reports as PDF / Excel

### 10-I API Integration
- [x] All routes implemented beyond Dashboard
- [ ] Recharts datasets use CSS variable colors (dark-mode responsive)
- [x] `X-Org-Id` on all requests
- [x] Pagination on all list endpoints
- [ ] Export endpoints (PDF/CSV generation on server)

### 10-J AI Features (Capital Hub AI)
- [ ] Cash flow forecast: AI predicts 30/60/90-day cash position from current data
- [ ] Expense anomaly detection: AI flags unusual expense patterns vs. historical baseline
- [ ] Budget variance explanation: AI generates narrative for budget line overruns
- [ ] Invoice collection likelihood: AI scores which overdue invoices are likely to be paid
- [ ] Revenue recognition assistant: AI suggests revenue recognition schedule for contracts
- [ ] Financial narrative: AI writes the "Management Discussion & Analysis" section from numbers
- [ ] Cost optimization suggestions: AI identifies areas to reduce spend based on trends
- [ ] Natural language financial query: "What was our gross margin in Q3 vs Q2?"

### 10-K Cross-App Integrations
- [ ] Planet: closed won deal value → auto-create invoice in Capital Hub
- [ ] Control Center: cash position and budget utilization widget in Control Center
- [ ] Atlas: project budgets tracked in Capital Hub (actual vs. planned spend)
- [ ] Mail: send invoice via Mail integration (PDF attached, payment link in body)
- [ ] EventBus: emit `invoice.created`, `invoice.paid`, `expense.approved` events
- [ ] EventBus: consume `deal.won` → trigger invoice creation workflow

### 10-L Security & Compliance
- [ ] Financial data encrypted at rest (AES-256)
- [ ] Bank connection tokens (OAuth for Plaid/open banking) stored encrypted, never logged
- [ ] Invoice data: strict org isolation (no cross-tenant data leakage)
- [ ] Expense receipts: stored in encrypted MinIO bucket
- [ ] SOC 2 Type II controls: access logging, change management for financial records
- [ ] Audit log: all financial record CUD operations with actor + timestamp + IP
- [ ] GDPR: financial data export includes all invoices and expenses for user
- [ ] Multi-factor auth required for financial exports and bank connections

### 10-M Accessibility
- [ ] All charts have underlying data tables accessible to screen readers
- [ ] Financial tables: keyboard navigable, sortable columns accessible
- [ ] Currency inputs: aria-labels include currency code ("Amount in USD")
- [ ] Date range picker: keyboard accessible
- [ ] Status badges (paid/overdue/draft): text label always present

### 10-N Testing
- [ ] Unit: budget variance calculation (actual vs. planned %)
- [ ] Unit: invoice total with line items, tax, discount
- [ ] Unit: cash flow projection algorithm
- [ ] E2E: create invoice → mark as paid → verify dashboard revenue updates
- [ ] E2E: expense submission → approval workflow → reports reflect expense

### 10-O i18n
- [ ] All UI strings in translation files
- [ ] Currency: configurable per org (USD, EUR, GBP, JPY, etc.)
- [ ] Number formatting: `Intl.NumberFormat` with currency symbol placement per locale
- [ ] Date formats: locale-aware across all financial dates
- [ ] RTL: tables and charts render correctly for ar/he

---

## 11 TurboTick — Issue Tracker

> **Stack:** ❌ NO FRONTEND EXISTS · Backend: Flask/Python
> **Status:** 0% — Frontend build from scratch required

### 11-A Initial Setup
- [ ] Create `TurboTick/frontend/` Vite + React 19 + TypeScript project
- [ ] `package.json`: add `@orbit-ui/react`, Tailwind v3, React Router v7, Zustand, Axios, Lucide React
- [ ] `tailwind.config.js`: use orbit preset
- [ ] `index.html`: anti-FOUC script + orbit-ui assets links
- [ ] `main.tsx`: `ThemeProvider` wraps root
- [ ] `index.css`: `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Vite proxy: `/api` → `http://localhost:[turbotick-backend-port]`
- [ ] Auth: Gate OAuth PKCE flow (reuse pattern from Atlas)
- [ ] Add to sync script `FRONTENDS` array (already present)

### 11-B Core Features — Issue Management
- [ ] Issue list: title, type, status, priority, assignee, labels
- [ ] Issue creation: title, description, type (bug/feature/task/epic), priority
- [ ] Issue detail: full description (rich text), comments, activity
- [ ] Issue status workflow: Backlog → Todo → In Progress → Review → Done
- [ ] Issue priority: Critical, High, Medium, Low
- [ ] Issue type icons: 🐛 Bug, ✨ Feature, ⚙️ Task, 🎯 Epic
- [ ] Issue labels: create, assign, color
- [ ] Issue assignee: assign to team member
- [ ] Issue sprint assignment
- [ ] Issue estimates: story points or time
- [ ] Issue linking: blocks / is-blocked-by / duplicate / related
- [ ] Issue comments: rich text, @mentions, emoji reactions
- [ ] Issue history/activity log
- [ ] Issue watching / subscribe to notifications
- [ ] Issue search: full-text + filter by all fields

### 11-C Core Features — Project & Board
- [ ] Projects list with icon and description
- [ ] Project creation: name, key (e.g. TT-), description, lead
- [ ] Kanban board per project (customizable columns)
- [ ] Sprint board view
- [ ] Backlog list view (sorted, filterable)
- [ ] Board quick filters (mine / unassigned / current sprint)
- [ ] Board swimlanes (by epic or assignee)

### 11-D Core Features — Sprints
- [ ] Sprint creation: name, goal, start/end dates
- [ ] Sprint backlog refinement (drag issues in/out)
- [ ] Sprint start / complete actions
- [ ] Sprint burndown chart
- [ ] Sprint velocity history

### 11-E Core Features — Epics & Roadmap
- [ ] Epic: parent issue grouping multiple issues
- [ ] Roadmap: timeline view of epics
- [ ] Epic progress bar (% of child issues complete)

### 11-F Core Features — Reporting
- [ ] Velocity chart (story points per sprint)
- [ ] Burndown chart
- [ ] Cumulative flow diagram
- [ ] Issue resolution time metrics
- [ ] Open issues by priority chart

### 11-G API Integration
- [ ] Full CRUD for issues, comments, projects, sprints
- [ ] WebSocket or SSE for real-time board updates
- [ ] Webhook support (notify external services on issue events)
- [ ] Atlas integration: link Atlas tasks to TurboTick issues

### 11-H Design System Integration
- [ ] `index.css` imports `orbit-tokens.css`
- [ ] Tailwind config uses orbit preset
- [ ] Adopt `<Sidebar>` for project/board navigation
- [ ] Adopt `<Button>` for all issue actions
- [ ] Adopt `<Badge>` for issue priority, type, status labels
- [ ] Adopt `<Avatar>` for assignee display
- [ ] Adopt `<Tabs>` for issue detail (description/comments/activity/links)
- [ ] Adopt `<Modal>` for issue creation, sprint creation
- [ ] Adopt `<EmptyState>` for empty backlog, no sprints
- [ ] Adopt `<Skeleton>` for loading board and issue list
- [ ] Adopt `<Progress>` for epic completion, sprint progress

### 11-I Dark Mode
- [ ] Kanban board: column headers, card backgrounds, priority badges
- [ ] Issue list: row hover, priority color coding
- [ ] Issue detail: description area, comment bubbles
- [ ] Roadmap timeline: epic bars, milestone markers
- [ ] Burndown chart: axis labels, plot colors use CSS variables

### 11-J AI Features (TurboTick AI)
- [ ] Issue auto-classification: AI assigns type and priority from title/description
- [ ] Duplicate detection: AI warns when new issue is similar to existing
- [ ] Acceptance criteria generation: AI generates "Given/When/Then" from issue description
- [ ] Effort estimation: AI suggests story point range based on description + similar past issues
- [ ] Sprint planning assistant: AI selects optimal sprint backlog based on team velocity
- [ ] Bug report enrichment: AI adds reproduction steps suggestions to vague bug reports
- [ ] Release notes generator: AI generates changelog from merged issues in sprint
- [ ] Natural language issue search: "show me all UI bugs assigned to me in the current sprint"

### 11-K Cross-App Integrations
- [ ] Atlas: TurboTick issues linkable to Atlas tasks (engineering ↔ project management bridge)
- [ ] Connect: issue updates posted to designated Connect channel (#eng-updates)
- [ ] Writer: technical spec documents linkable to TurboTick epics
- [ ] Calendar: sprint start/end dates appear in Calendar as events
- [ ] Control Center: open critical bugs count shown in Control Center ops dashboard
- [ ] GitHub/GitLab: PR/commit mentions auto-link to TurboTick issue (webhook)
- [ ] EventBus: emit `issue.created`, `issue.resolved`, `sprint.completed` events

### 11-L Security & Compliance
- [ ] All API endpoints require Gate JWT + org scope
- [ ] Row-level security: users see only their org's issues
- [ ] RBAC: Admin / Project Lead / Developer / Reporter roles
- [ ] Issue content: sanitize markdown before render (XSS prevention)
- [ ] Audit log: issue status changes, assignment changes logged
- [ ] GDPR: user anonymization on account deletion (replaces name in all issues)

### 11-M Accessibility
- [ ] Kanban board: keyboard drag-and-drop for issues
- [ ] Issue list: keyboard navigation (arrow keys + enter to open)
- [ ] All priority and status badges: text label, not color alone
- [ ] Screen reader: announce issue status changes
- [ ] Focus trap in issue creation modal

### 11-N Testing
- [ ] Unit: sprint capacity calculation
- [ ] Unit: burndown chart data generation
- [ ] Unit: issue priority sort order
- [ ] E2E: create project → create sprint → add issues → start sprint → move issue to Done
- [ ] E2E: drag issue on kanban board → verify persisted position

### 11-O Performance
- [ ] Virtual scroll on backlog with 500+ issues
- [ ] Lazy load roadmap timeline library
- [ ] Board updates via WebSocket (avoid full page refresh)
- [ ] Debounce issue search (300ms)

### 11-P i18n
- [ ] All UI strings in translation files
- [ ] Date displays (sprint dates, due dates): locale-aware
- [ ] Story point labels: locale-aware pluralization
- [ ] RTL: board columns and issue list render correctly for ar/he

---

## 12 Dock — Workspace Hub

> **Stack:** ❌ NO FRONTEND EXISTS · Backend: Node.js/Express
> **Status:** 0% — Frontend build from scratch required

### 12-A Initial Setup
- [ ] Create `Dock/frontend/` Vite + React 19 + TypeScript project
- [ ] `package.json`: `@orbit-ui/react`, Tailwind, Router, Zustand, Lucide React
- [ ] `tailwind.config.js`: orbit preset
- [ ] `index.html`: anti-FOUC + orbit-ui links
- [ ] `main.tsx`: `ThemeProvider`
- [ ] Gate OAuth PKCE auth flow

### 12-B Core Concept
> Dock is the personal workspace homepage — a customizable dashboard showing cross-app activity widgets.

- [ ] Widget grid: draggable, resizable widget layout
- [ ] Widget: My Tasks (from Atlas)
- [ ] Widget: Unread Emails (from Mail)
- [ ] Widget: Upcoming Meetings (from Calendar/Meet)
- [ ] Widget: Team Activity Feed (from Connect + EventBus)
- [ ] Widget: Open Deals (from Planet)
- [ ] Widget: Calendar mini-view (from Calendar)
- [ ] Widget: Notes quick-capture (to Writer)
- [ ] Widget: Notifications (from EventBus)
- [ ] Widget: AI Daily Briefing
- [ ] Add/remove widgets from a gallery
- [ ] Widget settings (e.g., filter tasks to "my tasks only")
- [ ] Layout presets (compact, focus, overview)
- [ ] Workspace clock + timezone display
- [ ] Quick launch: most-used apps bar
- [ ] Search bar (global search across all Orbit apps)
- [ ] Daily agenda (today's calendar events + tasks)
- [ ] Keyboard shortcut: `Cmd+Space` to open Dock search

### 12-C Cross-App Integration
- [ ] Pull task data from Atlas API
- [ ] Pull email counts from Mail API
- [ ] Pull events from Calendar API
- [ ] Subscribe to EventBus SSE for live updates
- [ ] Unified notification center
- [ ] Cross-app action: create task from email, schedule meeting from task

### 12-D Dark Mode
- [ ] Widget backgrounds and borders
- [ ] Widget header text and icon colors
- [ ] Search bar
- [ ] Quick launch app icons
- [ ] Daily agenda event chips
- [ ] AI Daily Briefing card

### 12-E AI Features (Dock AI)
- [ ] AI Daily Briefing widget: morning summary of today's priorities (meetings, tasks, deals, alerts)
- [ ] Smart prioritization: AI reorders "My Tasks" widget by urgency + deadline
- [ ] Focus time recommendation: AI suggests best time blocks for deep work today
- [ ] Anomaly alerts: AI surfaces unusual events ("3 critical bugs opened overnight")
- [ ] Natural language widget commands: "show me my overdue tasks from Atlas"
- [ ] Personalized layout suggestions: AI recommends widget layout based on usage patterns

### 12-F Security & Compliance
- [ ] Dock only reads data — no write operations (read-only aggregator)
- [ ] Per-widget data access respects source app's permissions
- [ ] Widget data cached with short TTL (max 5 min for sensitive data)
- [ ] No cross-org data in widgets
- [ ] Session-scoped widget state (no PII persisted to localStorage)

### 12-G Accessibility
- [ ] Widget grid: keyboard navigable (tab between widgets)
- [ ] Drag-and-drop layout: keyboard accessible alternative (settings menu to reorder)
- [ ] All widget action buttons labeled with aria-labels
- [ ] Search bar: keyboard shortcut `Cmd+Space` and aria-label

### 12-H Testing
- [ ] Unit: widget data aggregation (mock API responses)
- [ ] E2E: load Dock → verify all widgets render with data
- [ ] E2E: add/remove widget from gallery

### 12-I Performance
- [ ] Widget data loaded in parallel (not sequentially)
- [ ] Stale-while-revalidate for all widget data
- [ ] Lazy load heavy widgets (charts, graphs)
- [ ] Widget error boundaries: one failing widget doesn't break the page

### 12-J i18n
- [ ] All UI strings in translation files
- [ ] Widget timestamps: locale-aware relative times
- [ ] Number formatting in KPI widgets: `Intl.NumberFormat` locale-aware
- [ ] RTL: widget grid layout adapts for ar/he

---

## 13 Wallet — Financial Management

> **Stack:** ❌ NO FRONTEND EXISTS · Backend: Python/FastAPI
> **Status:** 0% — Frontend build from scratch required

### 13-A Initial Setup
- [ ] Create `Wallet/frontend/` Vite + React 19 + TypeScript project
- [ ] `package.json`: `@orbit-ui/react`, Tailwind, Router, Zustand, Recharts, Lucide
- [ ] `tailwind.config.js`: orbit preset
- [ ] `index.html`: anti-FOUC + orbit-ui links
- [ ] `main.tsx`: `ThemeProvider`
- [ ] Gate OAuth PKCE auth flow
- [ ] Security: all financial data over HTTPS only, strict CSP headers

### 13-B Core Features — Wallet Dashboard
- [ ] Portfolio overview: total value, 24h change, allocation chart
- [ ] Asset list: cryptocurrency + traditional holdings
- [ ] Holdings: coin name, amount, value, 24h %, overall %
- [ ] Price chart: interactive line chart (1D/1W/1M/3M/1Y)
- [ ] Transaction history: buy/sell/transfer/receive log
- [ ] P&L tracking: cost basis vs. current value
- [ ] Portfolio rebalancing calculator

### 13-C Core Features — Transactions
- [ ] Transaction list: date, type, asset, amount, fee, status
- [ ] Transaction filter: by asset, type, date range
- [ ] Transaction export: CSV for tax reporting
- [ ] Import transactions from exchange CSV (Coinbase, Binance)

### 13-D Core Features — Analytics
- [ ] Asset allocation donut chart
- [ ] Performance chart vs. benchmark (BTC, S&P500)
- [ ] Risk metrics: Sharpe ratio, max drawdown
- [ ] Tax lot tracking (FIFO / LIFO calculation)
- [ ] Realized gains/losses summary

### 13-E Security
- [ ] No private keys stored (view-only by default)
- [ ] Session timeout for financial views
- [ ] Transaction confirmation dialogs with 2-step confirmation
- [ ] Audit log of all actions

### 13-F Dark Mode
- [ ] Portfolio overview card
- [ ] Price chart: axis, grid lines, tooltip colors
- [ ] Asset list: holding rows, % change colors (green/red maintain contrast in dark)
- [ ] Transaction list
- [ ] Analytics charts

### 13-G AI Features (Wallet AI)
- [ ] Portfolio rebalancing suggestion: AI recommends trades to reach target allocation
- [ ] Tax optimization: AI identifies tax loss harvesting opportunities
- [ ] Spending insights: AI categorizes expenses and identifies savings opportunities
- [ ] Market brief: AI morning summary of relevant market news for user's holdings
- [ ] Risk assessment: AI analyzes portfolio concentration risk
- [ ] Budget vs. spending: AI forecasts end-of-month overspend by category
- [ ] Natural language query: "How much did I spend on SaaS tools last quarter?"

### 13-H Cross-App Integrations
- [ ] Capital Hub: personal wallet data (if org = sole proprietor) syncs to Capital Hub
- [ ] Mail: invoice emails auto-detected and logged as transactions
- [ ] Connect: budget alerts shared to personal Connect DM
- [ ] EventBus: emit `transaction.logged`, `budget.alert` events

### 13-I Design System Integration
- [ ] Adopt `<Sidebar>` for navigation
- [ ] Adopt `<Card>` for portfolio summary, asset cards
- [ ] Adopt `<Badge>` for transaction types and status
- [ ] Adopt `<Progress>` for budget utilization bars
- [ ] Adopt `<Tabs>` for dashboard sections
- [ ] Adopt `<EmptyState>` for no transactions, no connected accounts
- [ ] Adopt `<Skeleton>` for loading portfolio data

### 13-J Accessibility
- [ ] Price changes: not conveyed by color alone (↑↓ arrows + text)
- [ ] Charts: accessible data table alternative
- [ ] Transaction list: keyboard navigable
- [ ] All financial inputs: clear aria-labels with currency context

### 13-K Testing
- [ ] Unit: P&L calculation (cost basis vs. current)
- [ ] Unit: tax lot FIFO/LIFO logic
- [ ] E2E: add transaction → verify portfolio value updates
- [ ] Security test: verify no private keys accepted or stored

### 13-L Performance
- [ ] Price data: cache with 60s TTL (don't hammer price APIs)
- [ ] Portfolio calculation: memoize, only recalculate on new transactions
- [ ] Lazy load chart library

### 13-M i18n
- [ ] All UI strings in translation files
- [ ] Currency display: configurable base currency, `Intl.NumberFormat`
- [ ] Date/time in transactions: locale-aware
- [ ] RTL: asset list and transaction table for ar/he

---

## 14 FitterMe — Health & Wellness

> **Stack:** ❌ NO FRONTEND · Backend: Python/FastAPI
> **Status:** 0% — Frontend build from scratch required

### 14-A Initial Setup
- [ ] Create `FitterMe/frontend/` Vite + React 19 + TypeScript project
- [ ] `package.json`: `@orbit-ui/react`, Tailwind, Router, Zustand, Recharts, Lucide
- [ ] `tailwind.config.js`: orbit preset
- [ ] `index.html`: anti-FOUC + orbit-ui links
- [ ] `main.tsx`: `ThemeProvider`
- [ ] Gate OAuth PKCE auth flow

### 14-B Core Features — Dashboard
- [ ] Daily activity summary: steps, calories, active minutes
- [ ] Weekly progress rings (goals vs. actual)
- [ ] Body metrics: weight, BMI, body fat % trend chart
- [ ] Hydration tracker
- [ ] Sleep quality score
- [ ] Daily wellness score (composite)

### 14-C Core Features — Workouts
- [ ] Workout library: exercises with instructions, muscle groups
- [ ] Workout creator: name, exercises, sets/reps/rest
- [ ] Workout log: start/stop timer, log sets with weight/reps
- [ ] Workout history: calendar heatmap of completed sessions
- [ ] Workout streak counter
- [ ] AI workout suggestion based on goals + history

### 14-D Core Features — Nutrition
- [ ] Food search (USDA / Open Food Facts database)
- [ ] Meal logging: breakfast/lunch/dinner/snack
- [ ] Macro tracking: protein/carbs/fat/calories
- [ ] Daily calorie target vs. consumed
- [ ] Water intake logging
- [ ] Meal planner (weekly)

### 14-E Core Features — Goals & Progress
- [ ] Goal creation: weight loss, muscle gain, endurance, flexibility
- [ ] Goal milestones with dates
- [ ] Progress photos (before/after comparison)
- [ ] Personal records (PR) tracking per exercise
- [ ] Achievement badges

### 14-F Wearable Integration
- [ ] Apple Health / Google Fit read access (via backend API)
- [ ] Fitbit sync
- [ ] Manual entry fallback when no wearable connected

### 14-G Dark Mode
- [ ] Dashboard rings and progress indicators
- [ ] Workout log cards
- [ ] Nutrition macros chart
- [ ] Body metrics trend charts
- [ ] Goal progress cards
- [ ] Achievement badges

### 14-H AI Features (FitterMe AI)
- [ ] Personalized workout plan: AI generates weekly workout plan based on goals + fitness level
- [ ] Adaptive progression: AI adjusts weights/reps recommendations as user improves
- [ ] Meal plan generator: AI creates weekly meal plan to hit macro targets
- [ ] Recipe suggestions: AI suggests recipes from available ingredients matching macro goals
- [ ] Recovery advisor: AI recommends rest days based on training load and sleep data
- [ ] Injury prevention: AI flags overtraining patterns and suggests mobility work
- [ ] Progress coaching: AI weekly check-in message with encouragement and adjustments
- [ ] Natural language logging: "I did 3 sets of bench press at 185lbs" → auto-parses into workout log

### 14-I Design System Integration
- [ ] Adopt `<Sidebar>` for navigation
- [ ] Adopt `<Card>` for workout cards, meal cards, goal cards
- [ ] Adopt `<Progress>` for macro tracking bars, goal progress
- [ ] Adopt `<Badge>` for achievement badges, difficulty levels
- [ ] Adopt `<Tabs>` for workout detail (info/history/instructions)
- [ ] Adopt `<EmptyState>` for no workouts logged, no goals set
- [ ] Adopt `<Skeleton>` for loading dashboard

### 14-J Cross-App Integrations
- [ ] Calendar: scheduled workouts appear as Calendar events
- [ ] Connect: share workout achievement to team channel (opt-in)
- [ ] EventBus: emit `workout.completed`, `goal.achieved` events

### 14-K Security & Compliance
- [ ] Health data is sensitive PII — encrypted at rest with separate key per user
- [ ] HIPAA-aligned data handling (if target market includes US healthcare)
- [ ] No health data in error logs, Sentry, or analytics events
- [ ] GDPR: full health data export on request
- [ ] GDPR: health data deletion on account removal

### 14-L Accessibility
- [ ] Progress rings: not color-only (include percentage text)
- [ ] Workout timer: screen reader announces time remaining
- [ ] All charts: accessible data table alternative
- [ ] Exercise instructions: support for screen reader (text descriptions of movements)

### 14-M Testing
- [ ] Unit: calorie calculation (TDEE, macro targets)
- [ ] Unit: workout volume calculation (sets × reps × weight)
- [ ] E2E: log workout → verify dashboard activity ring updates
- [ ] E2E: create goal → log progress → verify progress bar

### 14-N Performance
- [ ] Food database search: debounced, paginated (USDA API has 300k+ items)
- [ ] Workout library: virtualized list
- [ ] Charts: lazy loaded
- [ ] Wearable sync: background job, not blocking UI

### 14-O i18n
- [ ] All UI strings in translation files
- [ ] Metric/Imperial toggle: kg/lbs, km/miles, cm/inches
- [ ] Calorie/kilojoule toggle per locale preference
- [ ] RTL: dashboard layout for ar/he

---

## 15 Learn — Documentation Portal

> **Stack:** React 18.2.0 · Vite 5.0.0 · Router v6 · Zustand · Tailwind v3 · Axios
> **Routes:** Static pages · **Status:** ~50% feature complete

### 15-A Design System Integration
- [x] `tailwind.config.js` uses orbit preset
- [x] Anti-FOUC in `index.html`
- [x] `ThemeProvider` wraps root
- [x] `index.css` — add `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Replace hardcoded sidebar bg with `bg-surface-subtle`
- [ ] Replace hardcoded nav active state with `bg-primary-50 text-primary-600`
- [ ] Adopt `<Badge>` for "New", "Updated", "Beta" labels on docs pages
- [ ] Adopt `<Tabs>` for API reference (endpoint / parameters / response / examples tabs)
- [ ] Adopt `<Alert>` for callout boxes (info, warning, deprecated notices)
- [ ] Adopt `<Divider>` between doc sections
- [ ] Adopt `<EmptyState>` for empty search results
- [ ] Replace custom scrollbar with `.scrollbar-thin` plugin

### 15-B Dark Mode
- [ ] Full sidebar navigation dark mode
- [ ] Markdown content: code blocks, inline code, tables, blockquotes
- [ ] Search overlay
- [ ] API reference tables
- [ ] Navigation breadcrumbs
- [ ] TOC (table of contents) sidebar
- [ ] Footer links

### 15-C Core Features — Documentation Structure
- [ ] Getting Started guide: complete end-to-end setup walkthrough
- [ ] Architecture overview: how all 16 apps fit together
- [ ] Authentication guide: Gate OAuth PKCE flow with code examples
- [ ] API reference: all app APIs documented (auto-generated from OpenAPI)
- [ ] Design system guide: how to use orbit-tokens, tailwind preset, @orbit-ui/react
- [ ] Component reference: all @orbit-ui/react components with props docs
- [ ] Deployment guide: Docker, env vars, production checklist
- [ ] Changelog / Release notes: versioned

### 15-D Core Features — Search
- [ ] Full-text search across all documentation
- [ ] Search results ranked by relevance
- [ ] Search result snippet with keyword highlight
- [ ] Keyboard shortcut: `Cmd+K` opens search
- [ ] Recent searches
- [ ] "No results" state with suggestions

### 15-E Core Features — Navigation
- [ ] Persistent left sidebar with nested sections (expand/collapse)
- [ ] Active page highlighted in sidebar
- [ ] TOC (right sidebar) auto-generated from headings
- [ ] Previous / Next page navigation at bottom
- [ ] Breadcrumb trail at top of each page
- [ ] Mobile: hamburger to open sidebar

### 15-F Core Features — Content
- [ ] Markdown rendering with syntax-highlighted code blocks
- [ ] Copy-to-clipboard button on code blocks
- [ ] Version selector (docs for different Orbit versions)
- [ ] "Edit this page" link to GitHub
- [ ] "Was this page helpful?" feedback widget
- [ ] External link indicators (arrow icon)
- [ ] Internal link hover preview (popover)

### 15-G Core Features — Community & Feedback
- [ ] Forum: community discussion boards
- [ ] Forum: threaded replies
- [ ] Forum: search and filter
- [ ] Forum: moderation (pin, lock, delete)
- [ ] Changelog: subscribe to release notes via email

### 15-H API & Backend
- [ ] Search backend: index all markdown pages (Elasticsearch or Algolia)
- [ ] Forum backend: post/comment CRUD with Gate auth
- [ ] Analytics: page view tracking, popular pages
- [ ] Feedback collection API

### 15-I AI Features (Learn AI)
- [ ] AI search: natural language query ("how do I set up OAuth in Atlas?")
- [ ] Answer generation: AI synthesizes answer from docs and cites sources
- [ ] Related articles: AI suggests related documentation pages
- [ ] "Explain this" code block action: AI explains selected code example
- [ ] Doc quality checker: AI scores documentation completeness and clarity
- [ ] Auto-generated API docs: AI generates prose descriptions from OpenAPI spec
- [ ] Chatbot: "Ask the docs" floating chat widget for quick Q&A
- [ ] Translation: AI translates documentation pages to supported languages

### 15-J Cross-App Integrations
- [ ] Gate: developer dashboard in Gate links to Learn OAuth documentation
- [ ] All apps: "?" help button in each app deep-links to relevant Learn page
- [ ] Connect: #help channel bot answers questions using Learn knowledge base
- [ ] EventBus: emit `feedback.submitted` events for documentation ratings

### 15-K Security & Compliance
- [ ] Forum posts: content moderation (spam/abuse detection)
- [ ] User-generated forum content: sanitized before render (XSS prevention)
- [ ] Documentation search: no query logging with PII
- [ ] GDPR: forum posts anonymized on user account deletion
- [ ] Rate limiting on search and feedback APIs

### 15-L Accessibility
- [ ] All code blocks: copy button keyboard accessible
- [ ] Navigation sidebar: keyboard navigable, expandable sections via Enter/Space
- [ ] Search overlay: focus trap, Escape to close
- [ ] "Was this helpful?" widget: keyboard accessible
- [ ] Table of contents: skip-to-section links

### 15-M Testing
- [ ] Unit: search ranking algorithm
- [ ] Unit: Markdown rendering (code blocks, tables, callouts)
- [ ] E2E: search for term → verify results → click result → verify correct page
- [ ] E2E: forum post → reply → verify thread

### 15-N Performance
- [ ] Search: results in <500ms (pre-indexed)
- [ ] Doc pages: static generation where possible (SSG/SSR)
- [ ] Code syntax highlighting: lazy loaded
- [ ] Images in docs: optimized, lazy loaded

### 15-O i18n
- [ ] All UI strings in translation files
- [ ] Documentation pages: AI-translated versions for all 9 supported languages
- [ ] RTL: sidebar and content layout for ar/he
- [ ] Code examples: language-agnostic where possible (show curl + SDK examples)

---

## 16 Gate — Authentication (AuthX)

> **Stack:** Backend only (Python/FastAPI) · No frontend React app
> **Status:** Backend ~80% · Admin UI: 0%

### 16-A Admin Portal (Frontend — to be built)
- [ ] Admin portal frontend: Vite + React 19 + TypeScript
- [ ] Login with super-admin credentials
- [ ] User management: list, search, create, disable, reset password
- [ ] Organization management: list, create, configure, delete
- [ ] OAuth client management: view clients, rotate secrets, set redirect URIs
- [ ] Token inspector: decode and validate any JWT
- [ ] JWKS key management: view current keys, rotate keys
- [ ] Audit log viewer: all auth events with filter/search
- [ ] Rate limit configuration per endpoint
- [ ] Session management: view active sessions, revoke sessions
- [ ] MFA enrollment management: view who has MFA, force enrollment
- [ ] Dark mode (orbit-ui tokens)

### 16-B Developer Dashboard (Frontend)
- [ ] Create and manage OAuth2 applications
- [ ] View and test OAuth flows
- [ ] API key generation (for service accounts)
- [ ] Webhook configuration (auth events pushed to app endpoints)
- [ ] Documentation / quickstart embedded

### 16-C Backend Hardening
- [ ] PKCE code verifier minimum entropy enforcement
- [ ] Token expiry: access token 15 min, refresh 7 days
- [ ] Refresh token rotation (new refresh token on each use)
- [ ] Single-use refresh tokens (revoke old on rotation)
- [ ] JWKS: key rotation without downtime
- [ ] Token introspection endpoint (RFC 7662)
- [ ] Token revocation endpoint (RFC 7009)
- [ ] Revocation list: efficient lookup (Redis bloom filter)
- [ ] Account lockout: 5 failed attempts → 15 min lock
- [ ] Brute force protection: sliding window rate limit
- [ ] Password: bcrypt with cost factor ≥ 12
- [ ] Email verification: required before login
- [ ] TOTP MFA: RFC 6238 compliant
- [ ] MFA backup codes (8 single-use codes)
- [ ] Magic link (passwordless) flow
- [ ] Google OAuth SSO
- [ ] GitHub OAuth SSO
- [ ] Microsoft Entra SSO
- [ ] SAML 2.0 SP metadata + IdP-initiated SSO
- [ ] SCIM 2.0 user provisioning
- [ ] Device tracking: remember device for MFA (30 days)
- [ ] Suspicious login detection (new location, device)
- [ ] Security email: alert user on new device login

### 16-D Integration Health
- [ ] All 16 apps tested against Gate tokens end-to-end
- [ ] Atlas: PKCE login tested
- [ ] Mail: token refresh tested
- [ ] Connect: WebSocket auth via Gate token tested
- [ ] Meet: meeting room auth via Gate token tested
- [ ] Planet: org-scoped API with Gate JWT verified
- [ ] Secure: admin role claim in Gate JWT respected
- [ ] TurboTick: auth flow to be implemented
- [ ] Dock: auth flow to be implemented
- [ ] Wallet: auth flow + security hardening tested
- [ ] FitterMe: auth flow to be implemented

### 16-E AI Features (Gate AI)
- [ ] Anomalous login detection: AI flags logins from new location/device/time pattern
- [ ] Bot detection: AI identifies automated credential stuffing attacks
- [ ] Risk-based authentication: AI adjusts MFA requirements based on risk score
- [ ] Fraud pattern detection: AI correlates suspicious auth events across org
- [ ] Security posture report: AI weekly summary of auth health (failed logins, new devices, etc.)

### 16-F i18n
- [ ] Login page: all UI strings in translation files, auto-detected from browser locale
- [ ] Error messages: localized (invalid credentials, MFA failed, account locked)
- [ ] Email notifications (new device login, password reset): sent in user's language
- [ ] RTL: login form and admin portal layout for ar/he

### 16-G Observability
- [ ] Auth event metrics: login success/failure rate by method (password/OAuth/SAML)
- [ ] Token issuance latency tracked (p50/p95/p99)
- [ ] MFA challenge completion rate tracked
- [ ] JWKS key rotation events alerted
- [ ] Failed login spike detection: alert when failure rate > baseline + 3σ
- [ ] Sentry: all auth exceptions captured with request context (no credentials logged)

### 16-H Testing
- [ ] Unit: PKCE code verifier/challenge generation and validation
- [ ] Unit: JWT signing and verification
- [ ] Unit: refresh token rotation logic
- [ ] Unit: account lockout threshold and timer reset
- [ ] Integration: full PKCE OAuth flow (auth code → token → refresh → revoke)
- [ ] Integration: SAML 2.0 SP-initiated flow
- [ ] Integration: SCIM user provisioning (create/update/deactivate)
- [ ] Security: test token replay prevention
- [ ] Security: test brute force lockout triggers correctly
- [ ] Load test: 1000 concurrent token validations in <100ms

---

## Cross-Cutting Concerns (All Apps)

### Performance Standards
- [ ] First Contentful Paint < 1.5s (all apps, fast 3G)
- [ ] Largest Contentful Paint < 2.5s
- [ ] Total bundle size < 500KB gzipped (initial load)
- [ ] Route lazy loading in all 11 active apps
- [ ] All images use `loading="lazy"` or lazy-loaded via IntersectionObserver
- [ ] No unused CSS (PurgeCSS / Tailwind content config correct in all apps)

### Accessibility Standards
- [ ] WCAG 2.1 AA compliance in all apps
- [ ] All pages have a unique `<title>`
- [ ] All pages have skip-to-main-content link
- [ ] All images have `alt` attributes
- [ ] All form fields have visible, associated `<label>`
- [ ] Color contrast ≥ 4.5:1 for normal text
- [ ] Color contrast ≥ 3:1 for large text and UI components
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible in both light and dark mode
- [ ] No content flashes on page load (anti-FOUC done)
- [ ] Screen reader tested: VoiceOver (macOS) + NVDA (Windows)

### Security
- [ ] No secrets in frontend code or `console.log` in production
- [ ] Content Security Policy headers on all app responses
- [ ] All user-generated content sanitized before render (DOMPurify or equivalent)
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] File uploads: MIME type + extension validation
- [ ] API error messages: no stack traces exposed in production
- [ ] CORS: restricted to known origins
- [ ] HTTPS enforced (HSTS header)
- [ ] XSS protection: React escapes by default, audit all string interpolation to DOM

### DevOps / CI
- [ ] GitHub Actions / CI: lint + typecheck on every PR
- [ ] GitHub Actions: Vitest tests run on every PR
- [ ] GitHub Actions: Playwright E2E smoke tests on every PR
- [ ] GitHub Actions: orbit-ui sync validation (tokens distributed)
- [ ] Docker: each app has production Dockerfile
- [ ] Docker Compose: full ecosystem up with one command
- [ ] Environment variable documentation (`.env.example` in each app)
- [ ] Health check endpoint in each backend service

### Monitoring & Observability
- [ ] Error tracking: Sentry (or equivalent) in all frontend apps
- [ ] Performance monitoring: web vitals reporting (Sentry / Datadog)
- [ ] API error rate dashboard
- [ ] User event analytics (privacy-respecting, no PII)
- [ ] Uptime monitoring for all 16 services

---

*Total checkpoints: ~3,200 · Last updated: 2026-04-07*
