# 07 — Planet: CRM & Sales Platform — Comprehensive Checklist

> **App:** RM Orbit Planet
> **Stack:** React 19.2.3 · Vite 7.2.4 · Context-based navigation · Tailwind v4 · Zustand · FastAPI backend · SQLite
> **Frontend Pages:** Dashboard, Pipeline, Analytics, Predictions, Network, Reports, Settings, UserManagement, AuditLog
> **Frontend Components:** AppLauncher, Header, LoginPage, MetricCard, Sidebar
> **Backend Modules:** `main.py`, `config.py`, `database.py`, `eventbus.py`, `middleware/gate_auth.py`, `middleware/tenant_context.py`
> **Contexts:** AuditContext, AuthContext, NotificationContext
> **API Service:** `services/api.ts` (typed fetch wrappers for deals, pipeline, revenue, activities)
> **Last updated:** 2026-04-07

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration](#2-design-system-integration)
3. [Dark Mode](#3-dark-mode)
4. [Core Features](#4-core-features)
5. [API Integration](#5-api-integration)
6. [State Management](#6-state-management)
7. [Performance](#7-performance)
8. [Accessibility (WCAG 2.1 AA)](#8-accessibility-wcag-21-aa)
9. [Mobile & Responsive](#9-mobile--responsive)
10. [Internationalization](#10-internationalization)
11. [Security](#11-security)
12. [Testing](#12-testing)
13. [Documentation](#13-documentation)
14. [Deployment & CI/CD](#14-deployment--cicd)
15. [Backend](#15-backend)

---

## 1. Project Setup & Configuration

### 1.1 Frontend Project Structure
- [ ] Verify `package.json` has correct name (`@orbit/planet`)
- [ ] Verify React 19 is installed and configured
- [ ] Verify Vite is installed with correct plugins
- [ ] Verify Tailwind v4 is installed and configured
- [ ] Verify `@orbit-ui/react` is listed as a dependency
- [ ] Verify `lucide-react` is installed for icons
- [ ] Verify `recharts` is installed for charting
- [ ] Verify `zustand` is installed for state management
- [ ] Verify TypeScript is configured (`tsconfig.json`)
- [ ] Verify path aliases (`@/` mapping to `src/`) in `vite.config.ts`
- [ ] Verify ESLint is configured with consistent rules
- [ ] Verify Prettier is configured with consistent rules
- [ ] Verify `.env` / `.env.example` files exist
- [ ] Verify `VITE_API_BASE` environment variable is set
- [ ] Verify `VITE_PLANET_BACKEND` environment variable is set (default: `http://localhost:46000`)
- [ ] Add `.env.example` with all required variables documented
- [ ] Configure Vite proxy for `/api` to FastAPI backend
- [ ] Verify `index.html` has correct meta tags (charset, viewport)
- [ ] Verify `index.html` has Anti-FOUC script
- [ ] Verify `index.html` has correct title and favicon
- [ ] Remove any unused dependencies from `package.json`
- [ ] Verify all dev dependencies are correctly categorized
- [ ] Add `engines` field to `package.json` (Node >= 20)

### 1.2 Backend Project Structure
- [ ] Verify `requirements.txt` lists all Python dependencies
- [ ] Verify FastAPI is installed and configured
- [ ] Verify SQLite database file exists (`planet.db`)
- [ ] Verify Alembic is installed and configured for migrations
- [ ] Verify `alembic.ini` is configured with correct database URL
- [ ] Verify `app/config.py` has all required settings
- [ ] Verify `app/main.py` creates FastAPI app instance
- [ ] Verify `app/database.py` handles DB connection and queries
- [ ] Verify `app/eventbus.py` handles event publishing
- [ ] Verify `app/middleware/gate_auth.py` handles authentication
- [ ] Verify `app/middleware/tenant_context.py` handles org scoping
- [ ] Verify `tests/test_eventbus_contract.py` exists
- [ ] Verify `tests/test_gate_auth_claims.py` exists
- [ ] Verify `tests/test_tenant_context.py` exists
- [ ] Verify `start.sh` script works correctly
- [ ] Add `pyproject.toml` for Python project configuration
- [ ] Add `mypy.ini` for type checking
- [ ] Add `ruff.toml` for Python linting

### 1.3 Navigation Configuration
- [ ] Context-based navigation: Dashboard page
- [ ] Context-based navigation: Pipeline page
- [ ] Context-based navigation: Analytics page
- [ ] Context-based navigation: Predictions page
- [ ] Context-based navigation: Network page
- [ ] Context-based navigation: Reports page
- [ ] Context-based navigation: Settings page
- [ ] Context-based navigation: UserManagement page
- [ ] Context-based navigation: AuditLog page
- [ ] Navigation state persisted across page switches
- [ ] Deep linking support for all pages
- [ ] Browser back/forward navigation support
- [ ] URL-based routing (migrate from context-based to React Router)
- [ ] 404 handling for unknown routes
- [ ] Page transition animations
- [ ] All pages lazy-loaded with `React.lazy()`
- [ ] Suspense fallback with skeleton for each page
- [ ] Role-based page visibility (hide pages user cannot access)

---

## 2. Design System Integration

### 2.1 Token & Theme Setup
- [x] Anti-FOUC script in `index.html`
- [x] `ThemeProvider` wraps root component
- [x] Google Fonts removed
- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css";`
- [x] `index.html` — `orbit-tailwind-v4.css` loaded via `<link>` (Tailwind v4 app)
- [x] Remove all hardcoded hex color values from COLORS/STAGE_COLORS arrays
- [x] Replaced `COLORS` array in `Dashboard.tsx` with `CHART_COLORS` (orbit palette)
- [x] Replaced `COLORS` array in `Analytics.tsx` with `CHART_COLORS` (orbit palette)
- [x] Replaced `COLORS` array in `Network.tsx` with `CHART_COLORS` (orbit palette)
- [x] Replaced `COLORS` array in `Reports.tsx` with `CHART_COLORS` (orbit palette)
- [x] Replaced `STAGE_COLORS` in `Pipeline.tsx` with orbit palette values
- [x] Replace hardcoded `stageColors` in `api.ts` with orbit palette values (matching STAGE_COLORS)
- [x] Recharts chart tooltips use `var(--color-surface-base)` background (dark mode safe)
- [x] Recharts grid/axis lines use `var(--color-border-*)` and `var(--color-content-*)` CSS vars
- [x] Replaced all `Loader2 + animate-spin` loading states with `<Spinner>` from orbit-ui
- [x] Replaced all `border-slate-50` / `divide-slate-100` with `border-border-subtle` / `divide-border-subtle` (all pages + Header)
- [ ] Replace `bg-emerald-50 text-emerald-600` with orbit success tokens
- [ ] Replace `bg-blue-50 text-blue-600` with orbit primary tokens
- [ ] Replace `bg-indigo-50 text-indigo-600` with orbit primary tokens
- [ ] Replace `bg-amber-50 text-amber-600` with orbit warning tokens
- [ ] Replace `bg-red-50 text-red-500` with orbit danger tokens
- [ ] Replace all `bg-white` with `bg-surface-base`
- [ ] Replace all `bg-gray-*` with semantic surface tokens
- [ ] Replace all `text-gray-*` with semantic content tokens
- [ ] Replace all `border-gray-*` with `border-border-default` / `border-border-subtle`
- [ ] Replace `focus:ring-*` with `focus-ring` utility
- [x] `index.css` focus ring uses `var(--color-primary-500)` (was `#1d4ed8`)
- [x] `index.css` scrollbar colors use CSS vars (was hardcoded slate)
- [ ] Verify CSS custom properties used throughout all components

### 2.2 Replace Custom Components with @orbit-ui/react

#### Button
- [ ] Replace all CTA buttons in Dashboard with `<Button>`
- [ ] Replace "Add Deal" button in Pipeline with `<Button variant="primary">`
- [ ] Replace "Quick Actions" buttons in Dashboard with `<Button>`
- [ ] Replace filter/sort toggle buttons with `<Button variant="ghost">`
- [x] Replace "Kanban/List" view toggle with `<ButtonGroup>` (Pipeline.tsx)
- [ ] Replace Pipeline "Close Deal" buttons with `<Button variant="success">`
- [ ] Replace Pipeline "Lose Deal" buttons with `<Button variant="danger">`
- [ ] Replace Analytics export buttons with `<Button variant="outline">`
- [ ] Replace Reports "Generate" button with `<Button variant="primary">`
- [x] Replace Settings "Save/Cancel" buttons with `<Button variant="primary/secondary">` (Settings.tsx)
- [x] Replace Settings security "Update Password" and "Enable/Manage 2FA" buttons with `<Button>` (Settings.tsx)
- [x] Replace Settings integrations connect/configure buttons with `<Button>` (Settings.tsx)
- [x] Replace Contacts "Refresh" button with `<Button variant="secondary">` (Contacts.tsx)
- [x] Replace UserManagement "Add User" button with `<Button variant="primary" size="xs">` (UserManagement.tsx)
- [x] Replace UserManagement modal Cancel/Create buttons with `<Button>` (UserManagement.tsx)
- [x] Replace AuditLog Refresh/Export buttons with `<Button>` (AuditLog.tsx)
- [ ] Replace remaining icon-only action buttons with `<IconButton>`
- [ ] Replace all icon-only buttons with `<IconButton>`
- [ ] Replace LoginPage "Sign In" button with `<Button variant="primary" size="lg">`
- [ ] Ensure all buttons use consistent sizing

#### Input
- [ ] Replace all text inputs in Settings with `<Input>`
- [ ] Replace deal search input with `<Input prefix={<SearchIcon />}>`
- [ ] Replace contact search input with `<Input prefix={<SearchIcon />}>`
- [ ] Replace custom field inputs with `<Input>`
- [ ] Replace LoginPage email/password fields with `<Input>`
- [ ] Replace report builder parameter inputs with `<Input>`
- [ ] Replace deal form value input with `<Input type="number">`
- [ ] Replace deal form company input with `<Input>`
- [ ] Replace deal form name input with `<Input>`

#### Modal
- [ ] Replace deal creation dialog with `<Modal>`
- [ ] Replace deal detail dialog with `<Modal size="lg">`
- [ ] Replace deal delete confirmation with `<Modal>` (AlertDialog)
- [ ] Replace contact creation dialog with `<Modal>`
- [ ] Replace contact detail dialog with `<Modal size="lg">`
- [ ] Replace company creation dialog with `<Modal>`
- [ ] Replace import modal with `<Modal>`
- [ ] Replace export modal with `<Modal>`
- [ ] Replace settings confirmation with `<Modal>`
- [ ] Replace user invite dialog with `<Modal>`
- [ ] Replace role change confirmation with `<Modal>`

#### Badge
- [x] Replace deal stage badges in Pipeline list view with `<Badge>` (Pipeline.tsx)
- [x] Replace deal stage badges in Contacts table with `<Badge>` (Contacts.tsx)
- [x] Replace deal stage badges in Contacts drawer with `<Badge>` (Contacts.tsx)
- [x] Replace deal count badge in Contacts table with `<Badge color="primary">` (Contacts.tsx)
- [x] Replace user role badge in Settings profile with `<Badge>` (Settings.tsx)
- [x] Replace 2FA status badge in Settings security with `<Badge>` (Settings.tsx)
- [x] Replace session "Current" badge in Settings with `<Badge color="success">` (Settings.tsx)
- [x] Replace integration "Connected" badge in Settings with `<Badge color="success">` (Settings.tsx)
- [ ] Replace lead status badges with `<Badge>`
- [ ] Replace deal priority badges with `<Badge>`
- [ ] Replace probability percentage badges with `<Badge>`
- [ ] Replace win/loss indicators in Dashboard with `<Badge variant="success">` / `<Badge variant="danger">`
- [ ] Replace notification count badges with `<Badge>`
- [ ] Replace activity type indicators with `<Badge variant="subtle">`
- [ ] Replace region/industry labels in pipeline kanban with `<Badge>`
- [ ] Replace compliance status badges with `<Badge>`

#### Card
- [ ] Replace MetricCard component with `<Card>` from orbit-ui
- [ ] Replace KPI tiles on Dashboard with `<Card>`
- [ ] Replace Pipeline deal cards with `<Card interactive>`
- [ ] Replace top deals widget cards with `<Card>`
- [ ] Replace activity feed cards with `<Card>`
- [ ] Replace report summary cards with `<Card>`
- [ ] Replace integration cards with `<Card>`
- [ ] Replace analytics summary cards with `<Card>`
- [ ] Replace predictions result cards with `<Card>`

#### Table
- [ ] Replace contact list table with `<Table>` from orbit-ui
- [ ] Replace deal list view table with `<Table>`
- [ ] Replace activity log table with `<Table>`
- [ ] Replace report data table with `<Table>`
- [ ] Replace user management table with `<Table>`
- [ ] Replace audit log table with `<Table>`
- [ ] Add sortable headers to all tables
- [ ] Add row selection to contact/deal tables
- [ ] Add pagination to all tables
- [ ] Add sticky header to all tables
- [ ] Add empty state to all tables
- [ ] Add loading skeleton to all tables

#### Avatar
- [ ] Replace custom rep avatars in Pipeline with `<Avatar>`
- [ ] Replace custom contact profile pictures with `<Avatar>`
- [ ] Replace custom user avatars in header with `<Avatar>`
- [ ] Replace custom team member avatars with `<Avatar>`
- [ ] Replace activity feed user avatars with `<Avatar>`
- [ ] Replace deal card owner initials with `<Avatar>`
- [ ] Replace user management list avatars with `<Avatar>`
- [ ] Use `<AvatarGroup>` for multiple assigned reps

#### Tabs
- [ ] Replace record detail tabs (overview/activity/notes) with `<Tabs>`
- [ ] Replace Dashboard section tabs with `<Tabs>`
- [ ] Replace Analytics view tabs with `<Tabs>`
- [ ] Replace Reports view tabs with `<Tabs>`
- [x] Replace Settings section tabs with `<Tabs variant="pill">` (Settings.tsx)
- [ ] Replace contact detail tabs with `<Tabs>`
- [ ] Replace company detail tabs with `<Tabs>`

#### Switch
- [x] Replace custom toggle buttons in Settings Notifications with `<Switch>` (Settings.tsx)
- [x] Replace custom toggle buttons in Settings Appearance with `<Switch>` (Settings.tsx)
- [ ] Replace any other inline custom toggle controls with `<Switch>`

#### Dropdown
- [ ] Replace deal card action menu with `<Dropdown>`
- [ ] Replace contact action menu with `<Dropdown>`
- [ ] Replace sort-by selector with `<Dropdown>`
- [ ] Replace filter-by selector with `<Dropdown>`
- [ ] Replace stage selector in deal form with `<Dropdown>`
- [ ] Replace owner selector in deal form with `<Dropdown>`
- [ ] Replace region selector with `<Dropdown>`
- [ ] Replace industry selector with `<Dropdown>`
- [ ] Replace export format selector with `<Dropdown>`
- [ ] Replace chart type selector in Reports with `<Dropdown>`
- [ ] Replace time period selector with `<Dropdown>`
- [ ] Replace user role selector with `<Dropdown>`

#### Tooltip
- [ ] Add `<Tooltip>` to all icon-only buttons
- [ ] Add `<Tooltip>` to KPI cards (explain metric)
- [ ] Add `<Tooltip>` to chart data points
- [ ] Add `<Tooltip>` to pipeline stage headers
- [ ] Add `<Tooltip>` to truncated text elements
- [ ] Add `<Tooltip>` to sidebar navigation icons
- [ ] Add `<Tooltip>` to status indicators

#### Sidebar
- [ ] Replace custom `Sidebar.tsx` with `<Sidebar>` from orbit-ui
- [ ] Use `<SidebarItem>` for Dashboard navigation
- [ ] Use `<SidebarItem>` for Pipeline navigation
- [ ] Use `<SidebarItem>` for Analytics navigation
- [ ] Use `<SidebarItem>` for Predictions navigation
- [ ] Use `<SidebarItem>` for Network navigation
- [ ] Use `<SidebarItem>` for Reports navigation
- [ ] Use `<SidebarItem>` for Settings navigation
- [ ] Use `<SidebarItem>` for User Management navigation
- [ ] Use `<SidebarItem>` for Audit Log navigation
- [ ] Implement collapsible sidebar (icon-only mode)
- [ ] Sidebar sections: Main, Analytics, Admin
- [ ] Sidebar footer with user profile and settings
- [ ] Active page indicator in sidebar
- [ ] Badge counts on sidebar items (e.g., new leads count)

#### Skeleton
- [x] Dashboard full-page skeleton (KPI cards + charts)
- [x] Pipeline kanban skeleton (column headers + deal card placeholders)
- [x] Contacts table row-level skeleton (6 rows with circle + text)
- [x] Analytics charts skeleton (2-col + 3-col + 4-col grid)
- [x] Predictions skeleton (forecast chart + 2 charts + table)
- [x] Network skeleton (KPI row + map panel + rep list)
- [x] Reports skeleton (sidebar + main content area)
- [ ] Add `<Skeleton>` for Audit Log loading
- [ ] Add `<Skeleton>` for deal detail loading
- [ ] Add `<Skeleton>` for contact detail loading

#### Spinner
- [x] Replace all `<Loader2 animate-spin>` with `<Spinner>` from orbit-ui (all pages + LoginPage)
- [ ] Use `<Spinner>` for deal stage transition loading
- [ ] Use `<Spinner>` for data refresh indicator

#### EmptyState
- [ ] Add `<EmptyState>` for empty pipeline (no deals)
- [x] Add `<EmptyState>` for no contacts (`Contacts.tsx` table empty state)
- [ ] Add `<EmptyState>` for no search results in Pipeline/Dashboard
- [ ] Add `<EmptyState>` for no reports
- [ ] Add `<EmptyState>` for no activities
- [ ] Add `<EmptyState>` for no predictions available
- [ ] Add `<EmptyState>` for no network connections
- [ ] Add `<EmptyState>` for no audit log entries
- [ ] Add `<EmptyState>` for empty stage column

#### Alert
- [ ] Replace error messages with `<Alert variant="error">`
- [ ] Replace success messages with `<Alert variant="success">`
- [ ] Replace warning messages with `<Alert variant="warning">`
- [ ] Add `<Alert>` for deal close warning (large deal)
- [ ] Add `<Alert>` for quota attainment notification
- [ ] Add `<Alert>` for overdue activity reminder

#### DatePicker
- [ ] Add `<DatePicker>` for deal expected close date
- [ ] Add `<DatePicker>` for activity date filter
- [ ] Add `<DatePicker>` for report date range
- [ ] Add `<DatePicker>` for analytics period selection
- [ ] Add `<DatePicker>` for deal creation date filter
- [ ] Add `<DatePicker>` for forecast period

#### Progress
- [ ] Replace deal stage progress indicator with `<Progress>`
- [ ] Replace quota attainment bar with `<Progress>`
- [ ] Replace pipeline value progress with `<Progress>`
- [ ] Replace onboarding completion with `<Progress>`
- [ ] Replace import progress with `<Progress>`

#### FileUpload
- [ ] Add `<FileUpload>` for contact CSV import
- [ ] Add `<FileUpload>` for deal CSV import
- [ ] Add `<FileUpload>` for company CSV import
- [ ] Add `<FileUpload>` for contact photo upload
- [ ] Add `<FileUpload>` for attachment uploads

#### Breadcrumb
- [ ] Add `<Breadcrumb>` for deal detail navigation (Pipeline > Deal Name)
- [ ] Add `<Breadcrumb>` for contact detail navigation
- [ ] Add `<Breadcrumb>` for company detail navigation
- [ ] Add `<Breadcrumb>` for Settings sub-pages

#### Tag
- [ ] Add `<Tag>` for deal tags
- [ ] Add `<Tag>` for contact tags
- [ ] Add `<Tag>` for company tags
- [ ] Add `<Tag>` input for adding tags to records
- [ ] Add `<Tag>` for custom field values

---

## 3. Dark Mode

### 3.1 Dashboard Page
- [ ] Dashboard: KPI metric cards in dark mode
- [ ] Dashboard: KPI card icons and values in dark mode
- [ ] Dashboard: KPI comparison text (vs last period) in dark mode
- [ ] Dashboard: revenue chart (line) — axis, grid, data line, tooltip in dark mode
- [ ] Dashboard: pipeline funnel chart in dark mode
- [ ] Dashboard: pie chart (industry breakdown) colors in dark mode
- [ ] Dashboard: bar chart (weekly activities) in dark mode
- [ ] Dashboard: top performers leaderboard in dark mode
- [ ] Dashboard: recent activity feed in dark mode
- [ ] Dashboard: activity icon backgrounds in dark mode (`bg-emerald-50` etc.)
- [ ] Dashboard: quick actions panel in dark mode
- [ ] Dashboard: top deals section in dark mode
- [ ] Dashboard: loading spinner in dark mode
- [ ] Dashboard: section headers in dark mode
- [ ] Dashboard: card shadows in dark mode

### 3.2 Pipeline Page
- [ ] Pipeline: kanban column headers in dark mode
- [ ] Pipeline: kanban column backgrounds in dark mode
- [ ] Pipeline: stage value summaries in dark mode
- [ ] Pipeline: deal card background in dark mode
- [ ] Pipeline: deal card border on hover in dark mode
- [ ] Pipeline: deal card title text in dark mode
- [ ] Pipeline: deal card company text in dark mode
- [ ] Pipeline: deal card value text in dark mode
- [ ] Pipeline: deal card probability badge in dark mode
- [ ] Pipeline: deal card close date text in dark mode
- [ ] Pipeline: deal card owner avatar in dark mode
- [ ] Pipeline: drag-and-drop visual indicators in dark mode
- [ ] Pipeline: drag-over column highlight in dark mode
- [ ] Pipeline: list view table in dark mode
- [ ] Pipeline: list view table rows alternate coloring in dark mode
- [ ] Pipeline: filter/sort controls in dark mode
- [ ] Pipeline: view toggle (kanban/list) in dark mode
- [ ] Pipeline: region filter dropdown in dark mode
- [ ] Pipeline: empty column state in dark mode
- [ ] Pipeline: add deal button in dark mode

### 3.3 Analytics Page
- [ ] Analytics: chart backgrounds in dark mode
- [ ] Analytics: chart axis labels in dark mode
- [ ] Analytics: chart grid lines in dark mode
- [ ] Analytics: chart tooltips in dark mode
- [ ] Analytics: chart legends in dark mode
- [ ] Analytics: revenue trend line chart in dark mode
- [ ] Analytics: win/loss rate chart in dark mode
- [ ] Analytics: sales velocity chart in dark mode
- [ ] Analytics: activity breakdown chart in dark mode
- [ ] Analytics: deal size distribution in dark mode
- [ ] Analytics: rep performance comparison in dark mode
- [ ] Analytics: KPI summary cards in dark mode
- [ ] Analytics: date range selector in dark mode
- [ ] Analytics: filter controls in dark mode
- [ ] Analytics: export button in dark mode

### 3.4 Predictions Page
- [ ] Predictions: AI model results cards in dark mode
- [ ] Predictions: win probability scores in dark mode
- [ ] Predictions: churn risk indicators in dark mode
- [ ] Predictions: confidence levels in dark mode
- [ ] Predictions: deal recommendation cards in dark mode
- [ ] Predictions: forecast chart in dark mode
- [ ] Predictions: loading/processing state in dark mode
- [ ] Predictions: empty state in dark mode

### 3.5 Network Page
- [ ] Network: graph visualization background in dark mode
- [ ] Network: node colors in dark mode
- [ ] Network: edge/connection lines in dark mode
- [ ] Network: node labels in dark mode
- [ ] Network: hover tooltip on nodes in dark mode
- [ ] Network: selected node highlight in dark mode
- [ ] Network: legend in dark mode
- [ ] Network: zoom controls in dark mode
- [ ] Network: search/filter overlay in dark mode
- [ ] Network: detail panel on node click in dark mode

### 3.6 Reports Page
- [ ] Reports: report builder form in dark mode
- [ ] Reports: metric selector in dark mode
- [ ] Reports: dimension selector in dark mode
- [ ] Reports: chart type selector in dark mode
- [ ] Reports: generated chart in dark mode
- [ ] Reports: data table in dark mode
- [ ] Reports: saved reports list in dark mode
- [ ] Reports: report card in dark mode
- [ ] Reports: empty state in dark mode

### 3.7 Settings Page
- [ ] Settings: form sections in dark mode
- [ ] Settings: input fields in dark mode
- [ ] Settings: select dropdowns in dark mode
- [ ] Settings: toggle switches in dark mode
- [ ] Settings: section dividers in dark mode
- [ ] Settings: save/cancel buttons in dark mode
- [ ] Settings: tabs navigation in dark mode

### 3.8 UserManagement Page
- [ ] UserManagement: user table in dark mode
- [ ] UserManagement: user table row hover in dark mode
- [ ] UserManagement: role badges in dark mode
- [ ] UserManagement: status indicators (active/disabled) in dark mode
- [ ] UserManagement: invite form in dark mode
- [ ] UserManagement: action buttons in dark mode
- [ ] UserManagement: pagination in dark mode
- [ ] UserManagement: empty state in dark mode

### 3.9 AuditLog Page
- [ ] AuditLog: log table in dark mode
- [ ] AuditLog: log table row hover in dark mode
- [ ] AuditLog: action type badges in dark mode
- [ ] AuditLog: timestamp formatting in dark mode
- [ ] AuditLog: filter controls in dark mode
- [ ] AuditLog: search input in dark mode
- [ ] AuditLog: pagination in dark mode
- [ ] AuditLog: log detail expansion in dark mode
- [ ] AuditLog: metadata display in dark mode

### 3.10 Login Page
- [ ] LoginPage: background in dark mode
- [ ] LoginPage: form card in dark mode
- [ ] LoginPage: input fields in dark mode
- [ ] LoginPage: sign-in button in dark mode
- [ ] LoginPage: error messages in dark mode
- [ ] LoginPage: logo/branding in dark mode

### 3.11 Global Components
- [ ] Header: background in dark mode
- [ ] Header: user menu in dark mode
- [ ] Header: notification bell in dark mode
- [ ] Header: search bar in dark mode
- [ ] Sidebar: background in dark mode
- [ ] Sidebar: active item highlight in dark mode
- [ ] Sidebar: hover states in dark mode
- [ ] Sidebar: section dividers in dark mode
- [ ] AppLauncher: overlay in dark mode
- [ ] AppLauncher: app icons and labels in dark mode
- [ ] Notification toast: all variants in dark mode
- [ ] Confirmation dialogs in dark mode

### 3.12 Global Dark Mode Verification
- [ ] Verify color contrast ratios meet WCAG AA in dark mode (4.5:1)
- [ ] Verify all Recharts chart colors adapt to dark mode (CSS variables)
- [ ] Verify all focus rings are visible in dark mode
- [ ] Verify all scrollbar styles in dark mode
- [ ] Verify dark mode toggle persists across sessions
- [ ] Verify dark mode applies immediately without flash
- [ ] Test dark mode on all 9 pages simultaneously

---

## 4. Core Features

### 4.1 Dashboard
- [ ] KPI cards: total pipeline value
- [ ] KPI cards: total revenue closed (closed_won)
- [ ] KPI cards: active deals count
- [ ] KPI cards: average deal size
- [ ] KPI cards: win rate percentage
- [ ] KPI cards: period comparison (vs. last month / quarter)
- [ ] KPI cards: trend indicator (up/down arrow with color)
- [ ] Revenue chart: monthly trend line chart
- [ ] Revenue chart: target line overlay
- [ ] Revenue chart: tooltip with exact values
- [ ] Revenue chart: period selector (3M / 6M / 1Y / All)
- [ ] Pipeline funnel chart: deals per stage
- [ ] Pipeline funnel chart: value per stage
- [ ] Pipeline funnel chart: conversion rates between stages
- [ ] Industry breakdown: pie chart with percentages
- [ ] Weekly activities chart: stacked bar (calls, emails, meetings)
- [ ] Top performers leaderboard: rep name, deals won, revenue
- [ ] Top performers: time period filter
- [ ] Top deals: list of highest-value open deals
- [ ] Top deals: company, value, stage, probability, expected close
- [ ] Recent activity feed: last 10 activities
- [ ] Recent activity feed: icon per type (call, email, meeting, note, deal_update)
- [ ] Recent activity feed: timestamp with relative time ("2h ago")
- [ ] Recent activity feed: click to view detail
- [ ] Quick actions: "Add Contact" button
- [ ] Quick actions: "Add Deal" button
- [ ] Quick actions: "Log Activity" button
- [ ] Quick actions: "Schedule Meeting" button
- [ ] Dashboard: auto-refresh data (polling every 60s)
- [ ] Dashboard: manual refresh button
- [ ] Dashboard: date range filter
- [ ] Dashboard: loading state with skeletons

### 4.2 Pipeline Management

#### Pipeline — Kanban View
- [ ] Deal stages as kanban columns: Lead, Qualified, Proposal, Negotiation, Closed Won, Closed Lost
- [ ] Customizable stage columns (add/remove/rename stages)
- [ ] Stage column header: stage name, deal count, total value
- [ ] Deal card: company name
- [ ] Deal card: deal name
- [ ] Deal card: deal value (formatted currency)
- [ ] Deal card: probability percentage with color coding
- [ ] Deal card: expected close date
- [ ] Deal card: assigned rep avatar/initials
- [ ] Deal card: quick view button (eye icon)
- [ ] Deal card: drag handle for reordering
- [ ] Drag deals between stages (drag-and-drop)
- [ ] Drag deal: visual drop indicator on target column
- [ ] Drag deal: optimistic UI update (instant move, rollback on error)
- [ ] Drag deal: call `updateDeal` API on drop
- [ ] Deal stage automation: trigger actions on stage change
- [ ] Deal stage automation: send notification on stage change
- [ ] Deal stage automation: update probability on stage change
- [ ] Column WIP limits: visual warning when column exceeds limit
- [ ] Quick-add deal: "+" button in column header
- [ ] Quick-add deal: inline form (name, company, value)

#### Pipeline — List View
- [ ] Toggle between kanban and list view
- [ ] List view: table with all deals
- [ ] List view: columns — name, company, value, stage, probability, owner, expected_close, last_activity
- [ ] List view: sortable columns (click header to sort)
- [ ] List view: resizable columns
- [ ] List view: row click to open deal detail
- [ ] List view: row selection (checkboxes)
- [ ] List view: bulk actions (change stage, assign rep, delete)
- [ ] List view: inline editing (click cell to edit)
- [ ] List view: pagination (25/50/100 per page)

#### Pipeline — Filters
- [ ] Filter by stage (multi-select)
- [ ] Filter by rep/owner
- [ ] Filter by region
- [ ] Filter by industry
- [ ] Filter by date range (expected close)
- [ ] Filter by date range (created date)
- [ ] Filter by value range (min/max)
- [ ] Filter by probability range
- [ ] Filter by tag
- [ ] Active filter count badge
- [ ] Clear all filters button
- [ ] Save filter preset
- [ ] Load saved filter preset

#### Deal Detail
- [ ] Deal detail: overview tab — all deal fields displayed
- [ ] Deal detail: title (editable inline)
- [ ] Deal detail: company (editable, linked to company record)
- [ ] Deal detail: value (editable)
- [ ] Deal detail: stage (editable, dropdown)
- [ ] Deal detail: probability (editable, auto-set by stage or manual)
- [ ] Deal detail: expected close date (editable, date picker)
- [ ] Deal detail: owner/rep (editable, dropdown)
- [ ] Deal detail: industry (editable)
- [ ] Deal detail: region (editable)
- [ ] Deal detail: contact email (editable, linked to contact)
- [ ] Deal detail: notes (rich text editor)
- [ ] Deal detail: custom fields (text, number, dropdown, date)
- [ ] Deal detail: activity timeline tab
- [ ] Deal detail: timeline — calls, emails, meetings, notes, stage changes
- [ ] Deal detail: log new activity (call, email, meeting, note)
- [ ] Deal detail: linked tasks
- [ ] Deal detail: linked files/attachments
- [ ] Deal detail: linked contacts
- [ ] Deal detail: linked company
- [ ] Deal detail: deal age (days since creation)
- [ ] Deal detail: days in current stage
- [ ] Deal detail: stage progress bar
- [ ] Deal detail: close deal as Won (with reason)
- [ ] Deal detail: close deal as Lost (with reason/competitor)
- [ ] Deal detail: reopen closed deal
- [ ] Deal detail: delete deal (with confirmation)
- [ ] Deal detail: duplicate deal

#### Deal Creation
- [ ] Deal creation form: name (required)
- [ ] Deal creation form: company
- [ ] Deal creation form: value
- [ ] Deal creation form: stage (default: Lead)
- [ ] Deal creation form: probability
- [ ] Deal creation form: owner
- [ ] Deal creation form: expected close date
- [ ] Deal creation form: industry
- [ ] Deal creation form: region
- [ ] Deal creation form: contact email
- [ ] Deal creation form: notes
- [ ] Deal creation form: tags
- [ ] Deal creation form: validation errors
- [ ] Deal creation form: success notification
- [ ] Deal creation: auto-navigate to deal detail after creation

### 4.3 Contacts & Companies

#### Contact List
- [ ] Contact list: table view with all contacts
- [ ] Contact list: columns — name, email, phone, company, role, last activity
- [ ] Contact list: search by name/email/phone
- [ ] Contact list: filter by company
- [ ] Contact list: filter by tags
- [ ] Contact list: filter by last activity date
- [ ] Contact list: sort by name/company/last activity
- [ ] Contact list: pagination
- [ ] Contact list: row click to open detail
- [ ] Contact list: bulk select and actions
- [ ] Contact list: grid view alternative (contact cards)

#### Contact Detail
- [ ] Contact: name (first, last)
- [ ] Contact: email (primary, secondary)
- [ ] Contact: phone (mobile, work, home)
- [ ] Contact: company (linked)
- [ ] Contact: role/title
- [ ] Contact: department
- [ ] Contact: social links (LinkedIn, Twitter)
- [ ] Contact: address
- [ ] Contact: profile photo / avatar
- [ ] Contact: tags
- [ ] Contact: custom fields
- [ ] Contact: activity timeline (calls, emails, meetings)
- [ ] Contact: linked deals
- [ ] Contact: notes
- [ ] Contact: tasks
- [ ] Contact: last contacted date
- [ ] Contact: lead source
- [ ] Contact: lead score
- [ ] Contact: lifecycle stage (subscriber, lead, MQL, SQL, customer)
- [ ] Contact: edit all fields inline
- [ ] Contact: delete contact (with confirmation)

#### Contact Creation
- [ ] Contact creation form: first name, last name (required)
- [ ] Contact creation form: email
- [ ] Contact creation form: phone
- [ ] Contact creation form: company
- [ ] Contact creation form: role/title
- [ ] Contact creation form: tags
- [ ] Contact creation form: lead source
- [ ] Contact creation form: validation

#### Contact Import/Export
- [ ] Import contacts via CSV
- [ ] Import: column mapping UI
- [ ] Import: preview before confirming
- [ ] Import: duplicate detection
- [ ] Import: error handling (skip invalid rows)
- [ ] Import: progress indicator
- [ ] Export contacts to CSV
- [ ] Export contacts to vCard
- [ ] Duplicate detection: find and merge duplicates
- [ ] Duplicate detection: auto-suggest potential duplicates

#### Company Record
- [ ] Company: name
- [ ] Company: domain/website
- [ ] Company: industry
- [ ] Company: size (employee count range)
- [ ] Company: revenue range
- [ ] Company: address
- [ ] Company: phone
- [ ] Company: logo
- [ ] Company: linked contacts list
- [ ] Company: linked deals
- [ ] Company: activity timeline
- [ ] Company: notes
- [ ] Company: custom fields
- [ ] Company: creation form
- [ ] Company: edit form
- [ ] Company: delete (with confirmation)
- [ ] Company list: table view
- [ ] Company list: search and filter
- [ ] Company list: sort
- [ ] Company list: pagination

### 4.4 Activities
- [ ] Activity logging: phone call (duration, outcome, notes)
- [ ] Activity logging: email sent (subject, body preview)
- [ ] Activity logging: email received (tracked)
- [ ] Activity logging: meeting (date, attendees, outcome, notes)
- [ ] Activity logging: note (freeform text)
- [ ] Activity logging: task (title, due date, assigned to)
- [ ] Activity: link to deal
- [ ] Activity: link to contact
- [ ] Activity: link to company
- [ ] Activity: timestamp
- [ ] Activity: user who logged it
- [ ] Activity feed: filter by type (call/email/meeting/note/task)
- [ ] Activity feed: filter by date range
- [ ] Activity feed: filter by user
- [ ] Activity feed: search
- [ ] Activity feed: pagination
- [ ] Email tracking: open tracking (pixel)
- [ ] Email tracking: link click tracking
- [ ] Email tracking: notification on open/click
- [ ] Call logging: click-to-call integration
- [ ] Call logging: auto-log call from phone system

### 4.5 Analytics & Predictions

#### Revenue Analytics
- [ ] Revenue forecast: weighted pipeline sum by close month
- [ ] Revenue forecast: chart (bar chart with forecast vs actual)
- [ ] Revenue forecast: adjustable weights
- [ ] Revenue by month: trend line chart
- [ ] Revenue by rep: bar chart
- [ ] Revenue by industry: pie chart
- [ ] Revenue by region: map or bar chart
- [ ] Revenue target vs actual: comparison chart

#### Win/Loss Analytics
- [ ] Win rate: overall percentage
- [ ] Win rate: by stage (conversion rate per stage)
- [ ] Win rate: by rep
- [ ] Win rate: by industry
- [ ] Win rate: by deal size range
- [ ] Win rate: by lead source
- [ ] Win rate: trend over time
- [ ] Loss reasons: breakdown chart
- [ ] Loss reasons: competitor analysis
- [ ] Average days to close: by stage
- [ ] Average days to close: by rep

#### Sales Velocity
- [ ] Sales velocity metric: (# deals x avg value x win rate) / avg cycle days
- [ ] Sales velocity: trend chart
- [ ] Sales velocity: by rep comparison
- [ ] Time in stage: average days per stage
- [ ] Bottleneck identification: stages with longest average time

#### Quota & Targets
- [ ] Quota definition: per rep, per period (month/quarter)
- [ ] Quota attainment: percentage of quota achieved
- [ ] Quota attainment: progress bar per rep
- [ ] Quota attainment: team rollup
- [ ] Quota attainment: trend over periods

#### Activity Analytics
- [ ] Activity metrics: calls per rep (daily/weekly/monthly)
- [ ] Activity metrics: emails per rep
- [ ] Activity metrics: meetings per rep
- [ ] Activity metrics: activity-to-deal ratio
- [ ] Activity leaderboard

#### AI Predictions
- [ ] Deal win probability scores (ML model output)
- [ ] Deal win probability: factors contributing to score
- [ ] Deal win probability: recommendations to improve
- [ ] Churn risk indicators for existing customers
- [ ] Churn risk: contributing factors
- [ ] Churn risk: intervention recommendations
- [ ] Next best action suggestions
- [ ] Optimal contact timing predictions
- [ ] Deal scoring model configuration

#### Network Visualization
- [ ] Network graph: customer nodes
- [ ] Network graph: partner nodes
- [ ] Network graph: prospect nodes
- [ ] Network graph: relationship edges between entities
- [ ] Network graph: edge labels (relationship type)
- [ ] Network graph: node size based on deal value
- [ ] Network graph: node color based on stage/status
- [ ] Network graph: interactive dragging
- [ ] Network graph: zoom and pan
- [ ] Network graph: click to open record
- [ ] Network graph: search/filter nodes
- [ ] Network graph: cluster by industry/region
- [ ] Network graph: D3 or Cytoscape library integration

### 4.6 Reports

#### Report Builder
- [ ] Report builder: select metrics (revenue, deals, activities, etc.)
- [ ] Report builder: select dimensions (rep, stage, region, industry, time)
- [ ] Report builder: date range selection
- [ ] Report builder: filter conditions
- [ ] Report builder: group by options
- [ ] Report builder: preview before saving

#### Chart Types
- [ ] Chart: bar chart (vertical/horizontal)
- [ ] Chart: line chart
- [ ] Chart: pie/donut chart
- [ ] Chart: area chart
- [ ] Chart: scatter plot
- [ ] Chart: funnel chart
- [ ] Chart: data table view

#### Report Management
- [ ] Saved reports: save report configuration
- [ ] Saved reports: name and description
- [ ] Saved reports: library/list view
- [ ] Saved reports: edit saved report
- [ ] Saved reports: delete saved report
- [ ] Saved reports: duplicate saved report
- [ ] Scheduled reports: email delivery (daily/weekly/monthly)
- [ ] Scheduled reports: recipient list
- [ ] Report export: PDF download
- [ ] Report export: CSV download
- [ ] Report export: image download (PNG)
- [ ] Report sharing: share link with team

### 4.7 Sales Sequences & Automations

#### Sales Sequences
- [ ] Sequence builder: multi-step workflow (email, call, task, wait)
- [ ] Sequence builder: drag-and-drop step reordering
- [ ] Sequence builder: conditional branches (if opened -> next, else -> wait)
- [ ] Sequence enrollment: add contacts to sequence
- [ ] Sequence enrollment: bulk enrollment
- [ ] Sequence execution: auto-send emails on schedule
- [ ] Sequence execution: create tasks for manual steps
- [ ] Sequence analytics: open rate, reply rate, completion rate
- [ ] Sequence management: start/pause/stop sequences
- [ ] Sequence templates: pre-built sequences

#### Workflow Automations
- [ ] Automation trigger: deal stage change
- [ ] Automation trigger: deal value change
- [ ] Automation trigger: contact created
- [ ] Automation trigger: activity logged
- [ ] Automation trigger: deal inactivity (no activity for X days)
- [ ] Automation action: send email
- [ ] Automation action: create task
- [ ] Automation action: update field
- [ ] Automation action: assign owner
- [ ] Automation action: send notification
- [ ] Automation action: add to sequence
- [ ] Automation management: enable/disable automations
- [ ] Automation management: execution log

### 4.8 Territory Management
- [ ] Territory definition: by region
- [ ] Territory definition: by industry
- [ ] Territory definition: by account size
- [ ] Territory definition: by custom criteria
- [ ] Territory assignment: assign reps to territories
- [ ] Territory rules: auto-assign new leads to territory owner
- [ ] Territory performance: compare territories
- [ ] Territory map visualization

### 4.9 Lead Scoring
- [ ] Lead scoring rules: define criteria (email engagement, web activity, company size)
- [ ] Lead scoring: point-based model
- [ ] Lead scoring: auto-calculate on contact/deal update
- [ ] Lead scoring: score display on contact/deal card
- [ ] Lead scoring: high-score alerts
- [ ] Lead scoring: threshold for MQL/SQL transition
- [ ] Lead scoring: model configuration UI

### 4.10 User Management & RBAC

#### Roles & Permissions
- [ ] Roles: Super Admin — full access
- [ ] Roles: Admin — manage users, settings, data
- [ ] Roles: Manager — view team data, approve changes
- [ ] Roles: Sales Rep — own data, limited team visibility
- [ ] Roles: Read-only — view all, edit nothing
- [ ] Permission: page-level access control (`hasPermission` check)
- [ ] Permission: record-level access (own vs team vs all)
- [ ] Permission: action-level access (create, edit, delete, export)
- [ ] Permission: field-level access (hide sensitive fields)

#### User Management
- [ ] User invitation: invite by email
- [ ] User invitation: set role on invite
- [ ] User invitation: invitation email with link
- [ ] User activation: accept invitation flow
- [ ] User deactivation: disable user account
- [ ] User role change: admin changes user role
- [ ] User profile: edit own profile (name, photo, contact info)
- [ ] User list: table with name, email, role, status, last active
- [ ] User list: search and filter
- [ ] User list: pagination

### 4.11 Audit Log
- [ ] Audit log: all create operations logged
- [ ] Audit log: all update operations logged
- [ ] Audit log: all delete operations logged
- [ ] Audit log: actor (user who performed action)
- [ ] Audit log: timestamp
- [ ] Audit log: entity type and ID
- [ ] Audit log: action description
- [ ] Audit log: before/after values for updates
- [ ] Audit log: IP address of actor
- [ ] Audit log: searchable (by action, entity, user)
- [ ] Audit log: filterable by date range
- [ ] Audit log: filterable by action type
- [ ] Audit log: filterable by user
- [ ] Audit log: export to CSV
- [ ] Audit log: pagination
- [ ] Audit log: detail expansion (click row to see full metadata)

### 4.12 Settings
- [ ] Settings: workspace name and branding
- [ ] Settings: default currency
- [ ] Settings: default deal stages (add/remove/rename)
- [ ] Settings: deal probability defaults per stage
- [ ] Settings: fiscal year start month
- [ ] Settings: notification preferences
- [ ] Settings: email integration settings
- [ ] Settings: calendar integration settings
- [ ] Settings: API key management
- [ ] Settings: webhook configuration
- [ ] Settings: data retention policies
- [ ] Settings: import/export configuration
- [ ] Settings: custom fields definition
- [ ] Settings: custom field types (text, number, dropdown, date, checkbox)
- [ ] Settings: custom field assignment (deal, contact, company)
- [ ] Settings: lead scoring configuration
- [ ] Settings: territory configuration

### 4.13 Integrations
- [ ] Integration with RM Orbit Mail: email sync
- [ ] Integration with RM Orbit Mail: email tracking
- [ ] Integration with RM Orbit Calendar: meeting scheduling
- [ ] Integration with RM Orbit Calendar: activity sync
- [ ] Integration with RM Orbit Atlas: linked projects
- [ ] Integration with RM Orbit Connect: team messaging
- [ ] Integration with RM Orbit Capital Hub: revenue tracking
- [ ] Integration: Slack notifications
- [ ] Integration: webhook outgoing events
- [ ] Integration: Zapier/n8n connector

---

## 5. API Integration

### 5.1 Frontend API Layer
- [ ] Centralized API client (`services/api.ts`)
- [ ] All API calls use auth token from localStorage
- [ ] `Authorization: Bearer <token>` header on all requests
- [ ] `X-Org-Id` header on all requests
- [ ] `Content-Type: application/json` header on all requests
- [ ] 401 response: dispatch `unauthorized_access` event
- [ ] 401 response: redirect to login
- [ ] Error handling: parse backend error messages
- [ ] Error handling: show user-friendly error toasts
- [ ] Request timeout configuration
- [ ] Request retry logic with exponential backoff
- [ ] Request cancellation on component unmount (AbortController)
- [ ] Loading state management per request

### 5.2 Deal Endpoints
- [ ] `GET /api/deals` — list deals with pagination
- [ ] `GET /api/deals?stage=lead` — filter by stage
- [ ] `GET /api/deals/:id` — get single deal
- [ ] `POST /api/deals` — create deal
- [ ] `PUT /api/deals/:id` — update deal
- [ ] `DELETE /api/deals/:id` — delete deal
- [ ] `PUT /api/deals/:id/stage` — change deal stage
- [ ] `POST /api/deals/:id/close` — close deal (won/lost with reason)
- [ ] `POST /api/deals/:id/reopen` — reopen closed deal
- [ ] `POST /api/deals/:id/duplicate` — duplicate deal
- [x] Pagination on all list endpoints

### 5.3 Pipeline Endpoints
- [ ] `GET /api/pipeline` — pipeline stages with deal counts and values
- [ ] `GET /api/pipeline/summary` — pipeline summary metrics
- [ ] `PUT /api/pipeline/stages` — update stage definitions

### 5.4 Contact Endpoints
- [ ] `GET /api/contacts` — list contacts with pagination
- [ ] `GET /api/contacts/:id` — get single contact
- [ ] `POST /api/contacts` — create contact
- [ ] `PUT /api/contacts/:id` — update contact
- [ ] `DELETE /api/contacts/:id` — delete contact
- [ ] `GET /api/contacts/search?q=term` — search contacts
- [ ] `POST /api/contacts/import` — import contacts from CSV
- [ ] `GET /api/contacts/export` — export contacts to CSV
- [ ] `GET /api/contacts/:id/activities` — activities for contact
- [ ] `GET /api/contacts/:id/deals` — deals for contact

### 5.5 Company Endpoints
- [ ] `GET /api/companies` — list companies
- [ ] `GET /api/companies/:id` — get single company
- [ ] `POST /api/companies` — create company
- [ ] `PUT /api/companies/:id` — update company
- [ ] `DELETE /api/companies/:id` — delete company
- [ ] `GET /api/companies/:id/contacts` — contacts for company
- [ ] `GET /api/companies/:id/deals` — deals for company

### 5.6 Activity Endpoints
- [ ] `GET /api/activities` — list activities with pagination
- [ ] `GET /api/activities?limit=10` — recent activities
- [ ] `POST /api/activities` — log activity
- [ ] `PUT /api/activities/:id` — update activity
- [ ] `DELETE /api/activities/:id` — delete activity

### 5.7 Analytics Endpoints
- [ ] `GET /api/analytics/revenue` — revenue summary
- [ ] `GET /api/analytics/revenue/monthly` — monthly revenue breakdown
- [ ] `GET /api/analytics/pipeline` — pipeline analytics
- [ ] `GET /api/analytics/win-rate` — win/loss analytics
- [ ] `GET /api/analytics/velocity` — sales velocity metrics
- [ ] `GET /api/analytics/activities` — activity analytics
- [ ] `GET /api/analytics/reps` — per-rep performance

### 5.8 Prediction Endpoints
- [ ] `GET /api/predictions/deals` — deal win probability scores
- [ ] `GET /api/predictions/churn` — churn risk scores
- [ ] `GET /api/predictions/forecast` — revenue forecast
- [ ] `POST /api/predictions/refresh` — refresh predictions

### 5.9 Report Endpoints
- [ ] `GET /api/reports` — list saved reports
- [ ] `POST /api/reports` — create report
- [ ] `GET /api/reports/:id` — get report config and data
- [ ] `PUT /api/reports/:id` — update report
- [ ] `DELETE /api/reports/:id` — delete report
- [ ] `POST /api/reports/:id/export` — export report

### 5.10 User/Admin Endpoints
- [ ] `GET /api/users` — list users
- [ ] `POST /api/users/invite` — invite user
- [ ] `PUT /api/users/:id/role` — change user role
- [ ] `PUT /api/users/:id/disable` — disable user
- [ ] `GET /api/audit-logs` — list audit logs with pagination and filters

### 5.11 Real-time Updates
- [ ] EventBus SSE connection for real-time deal updates
- [ ] SSE: deal stage changes
- [ ] SSE: new deal created
- [ ] SSE: activity logged
- [ ] SSE: reconnection with exponential backoff
- [ ] `X-Org-Id` + Bearer token on all requests
- [ ] Search API: debounced (300ms) full-text search

---

## 6. State Management

### 6.1 Context Architecture
- [ ] `AuthContext`: user authentication state, token management
- [ ] `AuditContext`: audit logging context
- [ ] `NotificationContext`: notification/toast state

### 6.2 Zustand Store Architecture
- [ ] Create `useDealStore` — deals list, selection, filters
- [ ] Create `useContactStore` — contacts list, selection, filters
- [ ] Create `useCompanyStore` — companies list
- [ ] Create `useActivityStore` — activity log
- [ ] Create `usePipelineStore` — pipeline stages and configuration
- [ ] Create `useAnalyticsStore` — analytics data and computed metrics
- [ ] Create `useReportStore` — saved reports
- [ ] Create `useUIStore` — sidebar, modals, page state

### 6.3 Deal Store
- [ ] State: `deals[]`
- [ ] State: `selectedDealId`
- [ ] State: `loading`
- [ ] State: `error`
- [ ] State: `filters` (stage, rep, region, industry, value range)
- [ ] State: `sortBy` / `sortOrder`
- [ ] State: `viewMode` (kanban/list)
- [ ] Action: `fetchDeals()`
- [ ] Action: `createDeal(data)`
- [ ] Action: `updateDeal(id, data)`
- [ ] Action: `deleteDeal(id)`
- [ ] Action: `moveDealToStage(id, stage)`
- [ ] Action: `setFilter(field, value)`
- [ ] Action: `clearFilters()`
- [ ] Selector: `filteredDeals`
- [ ] Selector: `dealsByStage`

### 6.4 Contact Store
- [ ] State: `contacts[]`
- [ ] State: `selectedContactId`
- [ ] State: `loading`
- [ ] State: `searchQuery`
- [ ] Action: `fetchContacts()`
- [ ] Action: `createContact(data)`
- [ ] Action: `updateContact(id, data)`
- [ ] Action: `deleteContact(id)`
- [ ] Action: `searchContacts(query)`

### 6.5 State Persistence
- [ ] Persist pipeline view mode (kanban/list) to localStorage
- [ ] Persist filter selections to localStorage
- [ ] Persist sort preferences to localStorage
- [ ] Persist sidebar collapsed state to localStorage
- [ ] Persist theme preference to localStorage
- [ ] Persist active page to localStorage
- [ ] Persist selected dashboard time period to localStorage

---

## 7. Performance

### 7.1 Bundle & Loading
- [ ] All 9 pages lazy-loaded with `React.lazy()`
- [ ] Suspense fallback with skeleton for each page
- [ ] Bundle size audit: tree-shake unused Recharts modules
- [ ] Bundle analyzer: verify no duplicate dependencies
- [ ] Preload critical pages on idle (Dashboard, Pipeline)
- [ ] First meaningful paint < 1.5s on fast 3G
- [ ] Code splitting: separate vendor chunk

### 7.2 Data Performance
- [ ] Virtual scroll on contact/deal tables (1000+ records)
- [ ] Virtual scroll on audit log table
- [ ] Debounce search input (300ms)
- [ ] Debounce filter changes (200ms)
- [ ] Memoize chart computations (`useMemo`)
- [ ] Memoize filtered/sorted deal lists
- [ ] Memoize pipeline stage grouping
- [ ] Cache API responses (SWR pattern)
- [ ] Pagination: limit API queries to 100 records per page

### 7.3 Chart Performance
- [ ] Lazy load D3/Cytoscape for Network graph
- [ ] Lazy load Recharts modules per chart type
- [ ] Memoize chart data transformations
- [ ] Throttle chart resize recalculation
- [ ] Use CSS variables for chart colors (not JS-computed)

### 7.4 Network Performance
- [ ] Parallel API calls where possible (`Promise.allSettled`)
- [ ] Cancel previous search request on new input
- [ ] Optimistic updates for deal stage changes
- [ ] Stale-while-revalidate pattern for dashboard data
- [ ] Gzip/Brotli compression for API responses

### 7.5 Memory Management
- [ ] Clean up event listeners on unmount
- [ ] Clean up SSE/EventSource on unmount
- [ ] Limit audit log entries in memory (paginate)
- [ ] Garbage collect chart instances on unmount

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Global Accessibility
- [ ] Skip-to-main-content link at top of page
- [ ] Landmark regions: header, nav, main, aside
- [ ] Page titles update per active page
- [ ] Language attribute on `<html>` element
- [ ] Visible focus indicators on all interactive elements
- [ ] Focus indicators meet 3:1 contrast ratio
- [ ] No content relies solely on color to convey meaning
- [ ] Text resizable up to 200% without loss of content

### 8.2 Pipeline Accessibility
- [ ] Kanban board: keyboard navigation between columns (left/right arrow)
- [ ] Kanban board: keyboard navigation between deals within column (up/down arrow)
- [ ] Kanban board: keyboard move deal to different stage (Ctrl+Arrow)
- [ ] Kanban board: `role="list"` on columns, `role="listitem"` on deal cards
- [ ] Kanban board: `aria-label` on each column with stage name and count
- [ ] Drag-and-drop: keyboard alternative (cut/paste deal between stages)
- [ ] Drag-and-drop: `aria-live` region announcing drag state
- [ ] Deal card: all info accessible (not just visual)
- [ ] Stage colors: not the only indicator (also text labels)

### 8.3 Table Accessibility
- [ ] All tables: `<table>` with `<thead>`, `<tbody>`, `<th>`, `<td>`
- [ ] All tables: sortable column headers with `aria-sort`
- [ ] All tables: row selection with `aria-selected`
- [ ] All tables: pagination controls accessible
- [ ] All tables: empty state announced to screen readers

### 8.4 Chart Accessibility
- [ ] All charts: `aria-label` with description of data
- [ ] All charts: data table alternative (toggle)
- [ ] All charts: color-blind safe color palette
- [ ] All charts: pattern fills option (not just color)
- [ ] All charts: keyboard-navigable data points

### 8.5 Form Accessibility
- [ ] All form inputs have associated `<label>` elements
- [ ] All form inputs have visible labels
- [ ] Required fields marked with `aria-required="true"`
- [ ] Error messages linked to inputs with `aria-describedby`
- [ ] Form validation errors announced to screen readers
- [ ] Tab order is logical through all forms

### 8.6 Modal Accessibility
- [ ] All modals trap focus within modal
- [ ] All modals return focus to trigger on close
- [ ] All modals have `aria-modal="true"`
- [ ] All modals have `role="dialog"` or `role="alertdialog"`
- [ ] Close on Escape key

### 8.7 Screen Reader Testing
- [ ] Test with VoiceOver (macOS)
- [ ] Test with NVDA (Windows)
- [ ] Verify dynamic content updates are announced
- [ ] Verify heading structure is logical
- [ ] Verify link text is descriptive

---

## 9. Mobile & Responsive

### 9.1 Layout Responsiveness
- [ ] Mobile (< 640px): sidebar hidden, hamburger menu
- [ ] Mobile: bottom navigation for primary pages
- [ ] Tablet (640-1024px): collapsible sidebar (icon-only)
- [ ] Desktop (> 1024px): persistent sidebar
- [ ] KPI cards: stack vertically on mobile (1 column)
- [ ] KPI cards: 2 columns on tablet
- [ ] KPI cards: 4 columns on desktop
- [ ] Charts: full width on mobile
- [ ] Charts: responsive aspect ratio

### 9.2 Mobile Pipeline
- [ ] Mobile: kanban collapses to single-column with stage tabs
- [ ] Mobile: deal cards in list format per stage
- [ ] Mobile: swipe between stages
- [ ] Mobile: swipe on deal card for quick actions (edit, close, delete)
- [ ] Mobile: bottom sheet for deal detail
- [ ] Mobile: simplified deal card (name, value, stage)

### 9.3 Mobile Tables
- [ ] Mobile: horizontal scroll for wide tables
- [ ] Mobile: responsive table with hidden columns on small screens
- [ ] Mobile: card-based layout alternative to table rows
- [ ] Mobile: touch-friendly row selection

### 9.4 Mobile Forms
- [ ] Mobile: full-screen modal for forms
- [ ] Mobile: stacked form layout
- [ ] Mobile: native date picker integration
- [ ] Mobile: bottom sheet for dropdowns

### 9.5 Mobile Navigation
- [ ] Mobile: bottom tab bar for main sections
- [ ] Mobile: pull-to-refresh on lists
- [ ] Mobile: swipe back gesture
- [ ] Mobile: floating action button (FAB) for quick add

### 9.6 Responsive Testing
- [ ] Test on iPhone 14/15 (Safari)
- [ ] Test on Samsung Galaxy S23 (Chrome)
- [ ] Test on iPad Air (Safari)
- [ ] Test on iPad Pro (Safari)
- [ ] Test in Chrome DevTools responsive mode

---

## 10. Internationalization

### 10.1 i18n Framework Setup
- [ ] Install and configure i18n library (i18next or react-intl)
- [ ] Set up translation file structure
- [ ] Wrap app in i18n provider
- [ ] Configure default locale (English)
- [ ] Configure locale detection from browser
- [ ] Add language switcher in settings

### 10.2 UI String Extraction
- [ ] Extract all Dashboard UI strings
- [ ] Extract all Pipeline UI strings
- [ ] Extract all Analytics UI strings
- [ ] Extract all Predictions UI strings
- [ ] Extract all Network UI strings
- [ ] Extract all Reports UI strings
- [ ] Extract all Settings UI strings
- [ ] Extract all UserManagement UI strings
- [ ] Extract all AuditLog UI strings
- [ ] Extract all modal/dialog strings
- [ ] Extract all error messages
- [ ] Extract all success messages
- [ ] Extract all tooltip texts
- [ ] Extract all empty state messages
- [ ] Extract all placeholder texts

### 10.3 RTL Support
- [ ] Support `dir="rtl"` attribute
- [ ] Mirror layout for RTL languages
- [ ] Test with Arabic locale
- [ ] Test with Hebrew locale

### 10.4 Date, Number & Currency Formatting
- [ ] Use `Intl.DateTimeFormat` for all date displays
- [ ] Use `Intl.NumberFormat` for all number displays
- [ ] Currency formatting: configurable currency (USD, EUR, GBP, INR, etc.)
- [ ] Currency formatting: symbol position (prefix/suffix)
- [ ] Currency formatting: decimal separator (`.` vs `,`)
- [ ] Relative time formatting ("2 hours ago", "yesterday")
- [ ] Deal values: locale-aware currency formatting
- [ ] Revenue: locale-aware currency formatting
- [ ] Quota: locale-aware currency formatting

---

## 11. Security

### 11.1 Authentication & Authorization
- [ ] All API requests include JWT Bearer token
- [ ] JWT token validation on backend (Gate SSO)
- [ ] JWT token expiration handling
- [ ] 401 response: redirect to login
- [ ] Role-based page access enforcement
- [ ] Record-level access control (own data vs team vs all)
- [ ] Action-level access control (create, edit, delete, export)
- [ ] API rate limiting per user
- [ ] Session timeout with warning
- [ ] Multi-factor authentication for admin actions

### 11.2 Data Protection
- [ ] XSS prevention: sanitize all user inputs
- [ ] CSRF protection on state-changing requests
- [ ] Input validation: all form fields (client-side + server-side)
- [ ] Input validation: deal value range limits
- [ ] Input validation: email format validation
- [ ] Input validation: phone number format validation
- [ ] Content Security Policy headers
- [ ] No sensitive data in localStorage (only tokens)
- [ ] Clear sensitive data on logout
- [ ] Encrypt sensitive fields at rest (API keys, passwords)

### 11.3 Org Isolation
- [ ] All API queries scoped to org_id
- [ ] `X-Org-Id` header validated on backend
- [ ] Tenant context middleware enforces org isolation
- [ ] Cross-org data access prevented
- [ ] Database queries always include org_id filter

### 11.4 Audit Trail
- [ ] All CRUD operations logged to audit trail
- [ ] Audit records: immutable append-only storage
- [ ] Audit records: retention policy (configurable)
- [ ] Audit records: export capability
- [ ] Admin actions: elevated logging

---

## 12. Testing

### 12.1 Unit Tests — Frontend

#### Component Tests
- [ ] Unit test: MetricCard rendering with values
- [ ] Unit test: MetricCard with trend indicator
- [ ] Unit test: DealCard rendering with all fields
- [ ] Unit test: DealCard probability color coding
- [ ] Unit test: Sidebar navigation active state
- [ ] Unit test: Header user menu
- [ ] Unit test: LoginPage form validation
- [ ] Unit test: Pipeline kanban column rendering
- [ ] Unit test: Pipeline list view rendering

#### Logic Tests
- [ ] Unit test: deal filter logic (by stage)
- [ ] Unit test: deal filter logic (by region)
- [ ] Unit test: deal filter logic (by value range)
- [ ] Unit test: deal sorting logic (by value, date, name)
- [ ] Unit test: currency formatting (`formatCurrency`)
- [ ] Unit test: pipeline value calculation
- [ ] Unit test: win rate calculation
- [ ] Unit test: sales velocity calculation
- [ ] Unit test: activity grouping by day
- [ ] Unit test: industry breakdown calculation
- [ ] Unit test: monthly revenue calculation

#### API Layer Tests
- [ ] Unit test: `apiFetch` with success response
- [ ] Unit test: `apiFetch` with error response
- [ ] Unit test: `apiFetch` with 401 (dispatches event)
- [ ] Unit test: `getHeaders` returns correct auth headers
- [ ] Unit test: `fetchDeals` with stage filter
- [ ] Unit test: `createDeal` with valid data
- [ ] Unit test: `updateDeal` with partial data
- [ ] Unit test: `deleteDeal`
- [ ] Unit test: `fetchPipeline`
- [ ] Unit test: `fetchRevenueSummary`
- [ ] Unit test: `fetchActivities` with limit

#### Zustand Store Tests
- [ ] Unit test: deal store — fetch and set deals
- [ ] Unit test: deal store — create deal
- [ ] Unit test: deal store — update deal stage
- [ ] Unit test: deal store — delete deal
- [ ] Unit test: deal store — filter deals
- [ ] Unit test: contact store — CRUD operations
- [ ] Unit test: UI store — sidebar toggle

### 12.2 Integration Tests
- [ ] Integration: login -> dashboard loads with data
- [ ] Integration: dashboard -> click pipeline -> navigate
- [ ] Integration: pipeline -> drag deal -> API call -> verify
- [ ] Integration: pipeline -> add deal -> appears in stage
- [ ] Integration: pipeline -> filter by region -> verify
- [ ] Integration: analytics -> date range change -> charts update
- [ ] Integration: reports -> create report -> save -> reload -> verify
- [ ] Integration: settings -> update -> save -> reload -> verify
- [ ] Integration: user management -> invite user -> verify

### 12.3 E2E Tests (Playwright)
- [ ] E2E: login flow (email + password)
- [ ] E2E: dashboard loads with KPIs and charts
- [ ] E2E: navigate to Pipeline via sidebar
- [ ] E2E: create new deal in Pipeline
- [ ] E2E: drag deal between stages
- [ ] E2E: open deal detail and edit fields
- [ ] E2E: close deal as won
- [ ] E2E: close deal as lost
- [ ] E2E: search for deal by name
- [ ] E2E: filter pipeline by region
- [ ] E2E: toggle kanban/list view
- [ ] E2E: navigate to Analytics
- [ ] E2E: analytics date range filter
- [ ] E2E: navigate to Reports and create report
- [ ] E2E: export report as PDF
- [ ] E2E: navigate to Settings and update
- [ ] E2E: user management — invite user
- [ ] E2E: audit log — view and filter entries
- [ ] E2E: dark mode toggle
- [ ] E2E: mobile viewport — responsive layout

### 12.4 Visual Regression Tests
- [ ] Visual: Dashboard (light mode)
- [ ] Visual: Dashboard (dark mode)
- [ ] Visual: Pipeline kanban (light mode)
- [ ] Visual: Pipeline kanban (dark mode)
- [ ] Visual: Pipeline list view (light mode)
- [ ] Visual: Pipeline list view (dark mode)
- [ ] Visual: Analytics charts (light mode)
- [ ] Visual: Analytics charts (dark mode)
- [ ] Visual: Deal detail modal
- [ ] Visual: Network graph
- [ ] Visual: Login page
- [ ] Visual: Empty states (all variants)
- [ ] Visual: Mobile layouts

### 12.5 Unit Tests — Backend
- [ ] Unit test: deal CRUD operations
- [ ] Unit test: deal validation (required fields)
- [ ] Unit test: pipeline aggregation queries
- [ ] Unit test: revenue summary calculation
- [ ] Unit test: activity logging
- [ ] Unit test: Gate auth token verification
- [ ] Unit test: Gate auth claims parsing
- [ ] Unit test: tenant context extraction
- [ ] Unit test: tenant context isolation
- [ ] Unit test: eventbus event publishing
- [ ] Unit test: eventbus event format

### 12.6 Integration Tests — Backend
- [ ] Integration: POST /deals -> GET /deals -> verify
- [ ] Integration: PUT /deals/:id -> GET -> verify update
- [ ] Integration: DELETE /deals/:id -> GET -> verify 404
- [ ] Integration: GET /pipeline -> verify stage aggregation
- [ ] Integration: GET /analytics/revenue -> verify calculation
- [ ] Integration: auth middleware rejects invalid tokens
- [ ] Integration: tenant isolation (org A can't access org B data)
- [ ] Integration: pagination on all list endpoints

### 12.7 Performance Tests
- [ ] Performance: dashboard load time with 1000 deals
- [ ] Performance: pipeline render time with 500 deals
- [ ] Performance: contact table with 5000 contacts
- [ ] Performance: bundle size < 500KB gzipped
- [ ] Performance: LCP < 2.5s
- [ ] Performance: FID < 100ms
- [ ] Performance: CLS < 0.1

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] JSDoc comments on all exported functions
- [ ] JSDoc comments on all React components (props interface)
- [ ] JSDoc comments on all context providers
- [ ] JSDoc comments on all utility functions
- [ ] JSDoc comments on all API service functions
- [ ] Python docstrings on all FastAPI endpoints
- [ ] Python docstrings on all service functions
- [ ] Python docstrings on all middleware functions
- [ ] Inline comments for complex business logic

### 13.2 API Documentation
- [ ] OpenAPI/Swagger auto-generated from FastAPI
- [ ] API documentation accessible at `/docs`
- [ ] All endpoints documented with request/response schemas
- [ ] All endpoints documented with example payloads
- [ ] Error response schemas documented
- [ ] Authentication requirements documented
- [ ] Rate limiting documented

### 13.3 User Documentation
- [ ] Getting started guide for Planet CRM
- [ ] Pipeline management guide
- [ ] Contact management guide
- [ ] Analytics interpretation guide
- [ ] Report builder guide
- [ ] Admin guide (users, roles, settings)
- [ ] Keyboard shortcuts reference

### 13.4 Developer Documentation
- [ ] README with setup instructions
- [ ] Architecture overview
- [ ] Data model diagram
- [ ] State management architecture
- [ ] API integration guide
- [ ] Contributing guidelines
- [ ] Environment variables reference

---

## 14. Deployment & CI/CD

### 14.1 Frontend Build
- [ ] Production build succeeds (`vite build`)
- [ ] No TypeScript errors in build
- [ ] No ESLint warnings in build
- [ ] Source maps generated
- [ ] Build output optimized (minified, tree-shaken)
- [ ] Assets hashed for cache busting
- [ ] Environment variables injected at build time

### 14.2 Backend Build
- [ ] Python dependencies installable
- [ ] Database migrations run successfully
- [ ] Health endpoint responds (`GET /health`)
- [ ] All tests pass in CI
- [ ] Database seeding works (`seed_demo_data`)

### 14.3 CI Pipeline
- [ ] GitHub Actions workflow for frontend
- [ ] GitHub Actions workflow for backend
- [ ] Frontend: lint, type check, unit test, build
- [ ] Backend: lint, type check, unit test, integration test
- [ ] Code coverage report generation
- [ ] Code coverage threshold (>80%)
- [ ] Bundle size check
- [ ] Dependency vulnerability scan
- [ ] PR preview deployments

### 14.4 Deployment
- [ ] Docker image for frontend
- [ ] Docker image for backend
- [ ] Docker Compose for local development
- [ ] Kubernetes manifests for production
- [ ] Health check endpoint for load balancer
- [ ] Graceful shutdown handling
- [ ] Environment-specific configuration
- [ ] Database migration on deployment
- [ ] Zero-downtime deployment

### 14.5 Monitoring
- [ ] Application error tracking (Sentry)
- [ ] API response time monitoring
- [ ] Database query performance monitoring
- [ ] Frontend Core Web Vitals monitoring
- [ ] Uptime monitoring and alerting
- [ ] Log aggregation (structured JSON logs)

---

## 15. Backend

### 15.1 Database Schema
- [ ] `deals` table: id, org_id, name, company, value, stage, probability, owner, expected_close, industry, region, contact_email, notes, created, updated
- [ ] `contacts` table: id, org_id, first_name, last_name, email, phone, company_id, role, department, tags, lead_source, lead_score, lifecycle_stage, created, updated
- [ ] `companies` table: id, org_id, name, domain, industry, size, revenue_range, address, phone, created, updated
- [ ] `activities` table: id, org_id, type, title, description, timestamp, user_id, user_name, deal_id, contact_id, company_id
- [ ] `reports` table: id, org_id, name, description, config, chart_type, created_by, created, updated
- [ ] `users` table: id, org_id, email, name, role, status, last_active, created
- [ ] `audit_logs` table: id, org_id, actor, action, entity_type, entity_id, metadata, timestamp, ip_address
- [ ] `custom_fields` table: id, org_id, entity_type, name, field_type, options, required
- [ ] `tags` table: id, org_id, name, color
- [ ] `deal_tags` table: deal_id, tag_id
- [ ] `contact_tags` table: contact_id, tag_id
- [ ] `pipeline_stages` table: id, org_id, name, order, default_probability, color
- [ ] `sequences` table: id, org_id, name, steps, status, created
- [ ] `automations` table: id, org_id, name, trigger, actions, enabled, created
- [ ] `territories` table: id, org_id, name, criteria, assigned_users
- [ ] Run initial migration successfully

### 15.2 API Endpoints Implementation
- [ ] `GET /health` — health check
- [ ] `GET /api/deals` — list deals with pagination and filters
- [ ] `GET /api/deals/:id` — get deal detail
- [ ] `POST /api/deals` — create deal
- [ ] `PUT /api/deals/:id` — update deal
- [ ] `DELETE /api/deals/:id` — delete deal
- [ ] `GET /api/pipeline` — pipeline summary
- [ ] `GET /api/analytics/revenue` — revenue summary
- [ ] `GET /api/analytics/pipeline` — pipeline analytics
- [ ] `GET /api/analytics/velocity` — sales velocity
- [ ] `GET /api/activities` — list activities
- [ ] `POST /api/activities` — log activity
- [ ] `GET /api/contacts` — list contacts
- [ ] `POST /api/contacts` — create contact
- [ ] `PUT /api/contacts/:id` — update contact
- [ ] `DELETE /api/contacts/:id` — delete contact
- [ ] `GET /api/companies` — list companies
- [ ] `POST /api/companies` — create company
- [ ] `GET /api/reports` — list reports
- [ ] `POST /api/reports` — create report
- [ ] `GET /api/users` — list users
- [ ] `POST /api/users/invite` — invite user
- [ ] `GET /api/audit-logs` — list audit logs
- [ ] `GET /api/predictions/deals` — deal predictions

### 15.3 Authentication & Middleware
- [ ] Gate auth middleware (`gate_auth.py`)
- [ ] `get_current_user` dependency: verify JWT and extract user
- [ ] Tenant context middleware (`tenant_context.py`)
- [ ] Org scoping on all queries
- [ ] CORS middleware configured
- [ ] Request logging middleware
- [ ] Rate limiting middleware

### 15.4 EventBus Integration
- [ ] `log_planet_activity` function implemented
- [ ] Event: `deal.created`
- [ ] Event: `deal.updated`
- [ ] Event: `deal.stage_changed`
- [ ] Event: `deal.closed_won`
- [ ] Event: `deal.closed_lost`
- [ ] Event: `contact.created`
- [ ] Event: `contact.updated`
- [ ] Event: `activity.logged`
- [ ] Events include org_id, user_id, timestamp, entity data
- [ ] EventBus contract tests pass

### 15.5 Demo Data & Seeding
- [ ] `seed_demo_data(org_id)` function
- [ ] Demo deals across all stages
- [ ] Demo contacts with various companies
- [ ] Demo companies with industries
- [ ] Demo activities (calls, emails, meetings)
- [ ] Demo data idempotent (won't duplicate on re-run)

### 15.6 Database Performance
- [ ] Indexes on frequently queried columns (org_id, stage, owner)
- [ ] Pagination on all list queries (limit/offset)
- [ ] Connection pooling configured
- [ ] Query optimization for analytics aggregations
- [ ] Database backup strategy

### 15.7 Background Tasks
- [ ] Scheduled: refresh AI predictions
- [ ] Scheduled: calculate lead scores
- [ ] Scheduled: activity reminder emails
- [ ] Scheduled: report email delivery
- [ ] Async: eventbus publishing
- [ ] Async: email tracking processing

---

_End of Planet Checklist — Total items: 2000+_
