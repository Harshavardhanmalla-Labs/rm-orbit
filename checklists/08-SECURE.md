# 08 — RM Orbit Secure: Endpoint Security Platform

> **Standalone Checklist** -- Comprehensive feature, component, test, and deployment tracker
> **Comparable to:** CrowdStrike Falcon / SentinelOne Singularity / Microsoft Defender for Endpoint
> **Stack:** React 19.2.0 | Vite 7.3.1 | React Router v7 | Tailwind v3 | Zustand 5 | @orbit-ui/react | Playwright 1.58
> **Frontend port:** 45012 | **Backend port:** 8000 (FastAPI) / 6034 (Node extension) / 6004 (Docker)
> **Routes:** 9 (Overview, Endpoints, Vulnerabilities, Patches, Policies, Compliance, Logs, Integrations, WipeDevice)
> **Last updated:** 2026-04-06
>
> Legend: `[x]` = done | `[ ]` = todo | `[~]` = in progress | `[-]` = N/A / skipped

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration](#2-design-system-integration)
3. [Dark Mode](#3-dark-mode)
4. [Core Features](#4-core-features)
   - 4A. Overview / Dashboard
   - 4B. Endpoints
   - 4C. Vulnerabilities
   - 4D. Patches
   - 4E. Policies
   - 4F. Compliance
   - 4G. Deployment Logs
   - 4H. Integrations
   - 4I. Wipe Device Wizard
   - 4J. Threat Detection
   - 4K. Incident Response
   - 4L. Alerting & Notifications
   - 4M. Reports & Analytics
5. [API Integration](#5-api-integration)
6. [State Management](#6-state-management)
7. [Performance](#7-performance)
8. [Accessibility (WCAG 2.1 AA)](#8-accessibility-wcag-21-aa)
9. [Mobile & Responsive](#9-mobile--responsive)
10. [Internationalization](#10-internationalization)
11. [Security (The App Itself)](#11-security-the-app-itself)
12. [Testing](#12-testing)
13. [Documentation](#13-documentation)
14. [Deployment & CI/CD](#14-deployment--cicd)
15. [Backend](#15-backend)

---

## 1. Project Setup & Configuration

### 1.1 Package & Dependencies

- [x] `package.json` exists with `"type": "module"`
- [x] React 19.2.0 installed as dependency
- [x] React DOM 19.2.0 installed as dependency
- [x] React Router DOM v7.13.1 installed
- [x] `@orbit-ui/react` linked via `file:../../orbit-ui/react`
- [x] `lucide-react` v0.576.0 installed for iconography
- [x] `zustand` v5.0.11 installed for state management
- [x] `clsx` v2.1.1 installed for class composition
- [x] `tailwind-merge` v3.5.0 installed for TW class dedup
- [x] `date-fns` v4.1.0 installed for date formatting
- [ ] Pin all dependency versions (remove ^ ranges for production lockdown)
- [ ] Add `@tanstack/react-query` for server-state caching
- [ ] Add `react-hook-form` + `zod` for form validation
- [ ] Add `recharts` or `chart.js` for dashboard visualizations
- [ ] Add `react-virtuoso` or `@tanstack/react-virtual` for virtual scrolling
- [ ] Add `i18next` + `react-i18next` for internationalization
- [ ] Add `@sentry/react` for error tracking
- [ ] Add `msw` (Mock Service Worker) for API mocking in dev/test
- [ ] Add `@testing-library/react` + `@testing-library/jest-dom` for unit tests
- [ ] Add `vitest` for unit test runner
- [ ] Add `@axe-core/playwright` for accessibility testing in E2E
- [ ] Add `eslint-plugin-jsx-a11y` for accessibility linting
- [ ] Audit all dependencies for known CVEs (`npm audit`)
- [ ] Add `husky` + `lint-staged` for pre-commit hooks
- [ ] Add `prettier` for consistent formatting
- [ ] Add `@types/node` version aligned with Node LTS

### 1.2 Dev Dependencies

- [x] `@eslint/js` v9.39.1
- [x] `@playwright/test` v1.58.2
- [x] `@types/react` v19.2.7
- [x] `@types/react-dom` v19.2.3
- [x] `@vitejs/plugin-react` v5.1.1
- [x] `autoprefixer` v10.4.27
- [x] `eslint` v9.39.1
- [x] `eslint-plugin-react-hooks` v7.0.1
- [x] `eslint-plugin-react-refresh` v0.4.24
- [x] `globals` v16.5.0
- [x] `postcss` v8.5.8
- [x] `tailwindcss` v3.4.19
- [x] `typescript` v5.9.3
- [x] `typescript-eslint` v8.48.0
- [x] `vite` v7.3.1
- [ ] Add `@types/jest` or `@types/vitest` for test type support
- [ ] Add `eslint-plugin-import` for import ordering
- [ ] Add `@typescript-eslint/eslint-plugin` strict rules enabled
- [ ] Add `postcss-nesting` for CSS nesting support

### 1.3 Scripts

- [x] `dev` script (`vite`)
- [x] `build` script (`tsc -b && vite build`)
- [x] `lint` script (`eslint .`)
- [x] `preview` script (`vite preview`)
- [x] `test:e2e` script (`npm run build && playwright test`)
- [x] `test:e2e:ci` script (`playwright test`)
- [ ] Add `test:unit` script for vitest
- [ ] Add `test:unit:coverage` script with coverage thresholds
- [ ] Add `format` script for prettier
- [ ] Add `format:check` script for CI
- [ ] Add `typecheck` script (`tsc --noEmit`)
- [ ] Add `lint:fix` script (`eslint . --fix`)
- [ ] Add `storybook` script
- [ ] Add `build-storybook` script
- [ ] Add `analyze` script for bundle analysis (rollup-plugin-visualizer)
- [ ] Add `clean` script to remove dist/node_modules/.cache

### 1.4 Vite Configuration

- [x] `vite.config.ts` exists
- [x] React plugin configured (`@vitejs/plugin-react`)
- [x] Path alias `@` -> `./src`
- [x] Dev server port 45012 with `strictPort: true`
- [x] Host set to `0.0.0.0` for network access
- [x] Allowed hosts include `secure.freedomlabs.in`, `*.freedomlabs.in`, `localhost`
- [x] API proxy: `/api` -> `http://localhost:8000`
- [ ] Add WebSocket proxy for `/api/v1/ws` -> `ws://localhost:8000`
- [ ] Add `build.rollupOptions.output.manualChunks` for vendor splitting
- [ ] Add `build.sourcemap` for production debugging
- [ ] Add `define` for build-time constants (app version, build hash)
- [ ] Add `css.modules` configuration if CSS modules used
- [ ] Add environment variable validation plugin
- [ ] Add `build.target` set to modern browsers only
- [ ] Add `optimizeDeps.include` for pre-bundling critical deps
- [ ] Add `server.hmr` configuration for reliable HMR
- [ ] Add GZIP/Brotli compression plugin for production build

### 1.5 TypeScript Configuration

- [x] `tsconfig.json` exists (project references)
- [x] `tsconfig.app.json` exists (app source config)
- [x] `tsconfig.node.json` exists (node/vite config)
- [ ] Enable `strict: true` in tsconfig.app.json
- [ ] Enable `noUnusedLocals: true`
- [ ] Enable `noUnusedParameters: true`
- [ ] Enable `noUncheckedIndexedAccess: true`
- [ ] Enable `exactOptionalPropertyTypes: true`
- [ ] Verify `moduleResolution` is set to `bundler`
- [ ] Verify `target` is set to `ES2022` or newer
- [ ] Add path aliases in tsconfig matching Vite aliases

### 1.6 ESLint Configuration

- [x] `eslint.config.js` exists (flat config)
- [ ] Enable `@typescript-eslint/strict` ruleset
- [ ] Enable `@typescript-eslint/no-explicit-any` as error
- [ ] Enable `react-hooks/exhaustive-deps` as error
- [ ] Enable `jsx-a11y/recommended` ruleset
- [ ] Enable `import/order` for consistent imports
- [ ] Configure `no-console` as warning (allow console.error/warn)
- [ ] Add `.eslintignore` or config-level ignores for dist/node_modules

### 1.7 PostCSS Configuration

- [x] `postcss.config.js` exists
- [x] Tailwind CSS plugin configured
- [x] Autoprefixer plugin configured
- [ ] Add `postcss-import` for CSS @import resolution
- [ ] Add `cssnano` for production CSS minification

### 1.8 Environment Variables

- [x] `.env.example` exists at project root
- [x] `VITE_SECURE_BEARER_TOKEN` env var supported in secureApi.ts
- [x] `VITE_SECURE_TENANT_ID` env var supported in secureApi.ts
- [ ] Create `.env.example` in frontend directory
- [ ] Add `VITE_API_BASE_URL` env var for configurable API endpoint
- [ ] Add `VITE_WS_BASE_URL` env var for configurable WebSocket endpoint
- [ ] Add `VITE_SENTRY_DSN` env var for error reporting
- [ ] Add `VITE_APP_VERSION` env var injected at build time
- [ ] Add `VITE_ENABLE_MOCK_API` env var for MSW toggle
- [ ] Add env var validation at app startup (fail fast on missing vars)
- [ ] Document all env vars with descriptions in .env.example

### 1.9 Docker

- [x] Multi-stage `Dockerfile` (frontend builder + Python backend)
- [x] `docker-compose.dev.yml` with postgres, redis, secure-service, workers
- [x] `docker-compose.prod.yml` exists
- [x] Postgres 16 service configured
- [x] Redis 7 service configured
- [x] Health check on secure-service (`/healthz`)
- [x] Patch dispatcher worker service
- [x] Patch worker (Celery) service
- [x] Policy worker service
- [x] Vulnerability engine scheduler service
- [ ] Add `.dockerignore` to exclude node_modules, .git, etc.
- [ ] Add frontend-only Dockerfile for dev (no Python)
- [ ] Add nginx service for production frontend serving
- [ ] Add resource limits (memory, CPU) to all services
- [ ] Add restart policies (`unless-stopped`)
- [ ] Add named networks for service isolation
- [ ] Add Docker Compose profiles (dev, test, prod)
- [ ] Add volume for Redis persistence
- [ ] Add pgAdmin or Adminer service for dev DB inspection
- [ ] Optimize Python image size (multi-stage with slim base)
- [ ] Pin all Docker image versions (no `latest` tags)

---

## 2. Design System Integration

### 2.1 Token & Theme Foundation

- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css"`
- [x] `tailwind.config.js` uses `orbitPreset` from `../../orbit-ui/tailwind-preset.js`
- [x] `darkMode: "class"` set in Tailwind config
- [x] `ThemeProvider` wraps root in `main.tsx`
- [x] `ThemeToggle` rendered in Layout header
- [x] Anti-FOUC via `orbit-theme-init.js` in `index.html`
- [ ] Remove Google Fonts import (`JetBrains Mono`) from `index.css` -- use local font or orbit token
- [ ] Remove custom CSS variables in `:root` (`--secure-bg-1`, `--secure-bg-2`, `--secure-bg-3`, `--secure-panel`, `--secure-border`, `--secure-shadow`) and replace with orbit tokens
- [ ] Remove hardcoded `body` background-color and background-image in index.css -- use orbit surface tokens
- [ ] Remove hardcoded `color: #0f172a` on body -- use `text-content-primary`
- [ ] Remove `* { @apply border-slate-200; }` global rule -- use per-component border tokens
- [ ] Remove leftover `App.css` (Vite boilerplate with `.logo`, `.card`, `.read-the-docs`)
- [ ] Replace all `text-slate-900` with `text-content-primary`
- [ ] Replace all `text-slate-700` with `text-content-secondary`
- [ ] Replace all `text-slate-600` with `text-content-secondary`
- [ ] Replace all `text-slate-500` with `text-content-muted`
- [ ] Replace all `text-slate-400` with `text-content-muted`
- [ ] Replace all `text-slate-300` with `text-content-muted`
- [ ] Replace all `text-slate-200` with orbit token equivalent
- [ ] Replace all `text-slate-100` with orbit token equivalent
- [ ] Replace all `bg-slate-50` with `bg-surface-muted`
- [ ] Replace all `bg-slate-100` with `bg-surface-muted`
- [ ] Replace all `bg-slate-200` with orbit token equivalent
- [ ] Replace all `bg-slate-900` (code blocks) with `bg-surface-invert`
- [ ] Replace all `bg-slate-950` (sidebar) with orbit dark surface token
- [ ] Replace all `border-slate-200` with `border-border-default`
- [ ] Replace all `border-slate-100` with `border-border-subtle`
- [ ] Replace all `border-slate-300` with `border-border-default`
- [ ] Replace all `border-slate-700` with `border-border-strong`
- [ ] Replace `bg-red-50`, `bg-red-100`, `text-red-700` severity badges with orbit semantic danger tokens
- [ ] Replace `bg-amber-50`, `bg-amber-100`, `text-amber-700` severity badges with orbit semantic warning tokens
- [ ] Replace `bg-emerald-50`, `bg-emerald-100`, `text-emerald-700` badges with orbit semantic success tokens
- [ ] Replace `bg-orange-100`, `text-orange-700` badges with orbit semantic tokens
- [ ] Replace all `bg-emerald-600` button colors with `bg-primary-600`
- [ ] Replace all `hover:bg-emerald-700` with `hover:bg-primary-700`
- [ ] Replace `bg-indigo-600` on Atlas remediation button with orbit primary
- [ ] Replace `focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100` with orbit `focus-ring` utility
- [ ] Remove `.secure-panel` custom CSS class -- use `<Card>` component
- [ ] Remove `.secure-panel-muted` custom CSS class -- use `<Card variant="muted">`
- [ ] Remove `.secure-input` custom CSS class -- use `<Input>` component
- [ ] Remove `.secure-select` custom CSS class -- use `<Select>` component
- [ ] Remove `.secure-btn-primary` custom CSS class -- use `<Button variant="primary">`
- [ ] Remove `.secure-btn-secondary` custom CSS class -- use `<Button variant="secondary">`
- [ ] Remove `.secure-btn-warning` custom CSS class -- use `<Button variant="warning">`
- [ ] Remove `.secure-btn-danger` custom CSS class -- use `<Button variant="danger">`
- [ ] Remove `.secure-btn-ghost` custom CSS class -- use `<Button variant="ghost">`
- [ ] Remove `.secure-chip-*` custom CSS classes -- use `<Badge>` component
- [ ] Remove `.secure-list-item` / `.secure-list-item-active` custom CSS -- use orbit list pattern
- [ ] Remove `.secure-table-*` custom CSS classes -- use `<Table>` component
- [ ] Remove `.secure-kpi` custom CSS class -- use `<Card>` with KPI layout
- [ ] Remove `.secure-title` custom CSS class -- use orbit typography tokens
- [ ] Remove `.secure-shell::before` grid overlay CSS -- replace with orbit pattern or remove

### 2.2 Replace Custom Components with @orbit-ui/react

#### Button Replacements

- [ ] Replace `.secure-btn-primary` in Overview (Refresh button) with `<Button>`
- [ ] Replace `.secure-btn-ghost` in Overview (Quick Action CTAs) with `<Button variant="ghost">`
- [ ] Replace `.secure-btn-ghost` in Endpoints (Previous/Next pagination) with `<Button variant="ghost">`
- [ ] Replace `.secure-btn-secondary` in Endpoints (Lock Device) with `<Button variant="secondary">`
- [ ] Replace `.secure-btn-danger` in Endpoints (Start Wipe Wizard) with `<Button variant="danger">`
- [ ] Replace `.secure-btn-primary` in Patches (Create Patch Job) with `<Button>`
- [ ] Replace `.secure-btn-primary` in Policies (Save Policy) with `<Button>`
- [ ] Replace `.secure-btn-secondary` in Policies (Run Simulation) with `<Button variant="secondary">`
- [ ] Replace `.secure-btn-warning` in Policies (Resolve Conflict) with `<Button variant="warning">`
- [ ] Replace `.secure-btn-primary` in Integrations (Evaluate Gate) with `<Button>`
- [ ] Replace `bg-indigo-600` button in Integrations (Create Atlas Task) with `<Button>`
- [ ] Replace `.secure-btn-secondary` in Integrations (Sync Device) with `<Button variant="secondary">`
- [ ] Replace `.secure-btn-primary` in WipeDevice (Continue buttons) with `<Button>`
- [ ] Replace `.secure-btn-danger` in WipeDevice (Authorize Remote Wipe) with `<Button variant="danger">`
- [ ] Replace `.secure-btn-ghost` in WipeDevice (Back buttons) with `<Button variant="ghost">`
- [ ] Replace sidebar mobile close button with `<IconButton>`
- [ ] Replace sidebar mobile open button with `<IconButton>`

#### Input Replacements

- [ ] Replace `.secure-input` in Endpoints (search) with `<Input>`
- [ ] Replace `.secure-input` in Endpoints (command reason) with `<Input>`
- [ ] Replace `.secure-input` in Vulnerabilities (severity select) with `<Select>`
- [ ] Replace `.secure-input` in Vulnerabilities (status select) with `<Select>`
- [ ] Replace `.secure-input` in Patches (scope select) with `<Select>`
- [ ] Replace `.secure-input` in Patches (version input) with `<Input>`
- [ ] Replace `.secure-input` in Patches (software name input) with `<Input>`
- [ ] Replace `.secure-input` in Patches (scheduled time input) with `<DatePicker>` or `<Input type="datetime-local">`
- [ ] Replace `.secure-input` in Patches (status filter select) with `<Select>`
- [ ] Replace `.secure-input` in Policies (name input) with `<Input>`
- [ ] Replace `.secure-input` in Policies (type select) with `<Select>`
- [ ] Replace `.secure-input` in Policies (severity input) with `<Input>`
- [ ] Replace `.secure-input` in Policies (simulate type select) with `<Select>`
- [ ] Replace `.secure-input` in Policies (min risk score input) with `<NumberInput>`
- [ ] Replace `.secure-input` in Policies (preferred policy ID input) with `<Input>`
- [ ] Replace `.secure-input` in Policies (superseded IDs input) with `<Input>`
- [ ] Replace `.secure-input` in Compliance (status filter input) with `<Input>`
- [ ] Replace `.secure-input` in Logs (action filter input) with `<Input>`
- [ ] Replace `.secure-input` in Integrations (threshold input) with `<NumberInput>`
- [ ] Replace `.secure-input` in Integrations (device select) with `<Select>`
- [ ] Replace `.secure-input` in Integrations (title input) with `<Input>`
- [ ] Replace `.secure-input` in Integrations (severity input) with `<Input>`
- [ ] Replace `.secure-input` in Integrations (entity ID input) with `<Input>`
- [ ] Replace `.secure-input` in Integrations (ownership select) with `<Select>`
- [ ] Replace `.secure-input` in WipeDevice (serial confirm input) with `<Input>`
- [ ] Replace `.secure-input` in WipeDevice (MFA code input) with `<Input>`
- [ ] Replace `.secure-input` in WipeDevice (schedule datetime input) with `<Input>`
- [ ] Replace `.secure-input` in WipeDevice (justification textarea) with `<Textarea>`
- [ ] Replace `.secure-select` in WipeDevice (wipe mode select) with `<Select>`
- [ ] Replace Overview preset `<select>` with `<Select>` from orbit-ui
- [ ] Replace TableDensityControl `<select>` with `<Select>` from orbit-ui

#### Badge Replacements

- [ ] Replace `.secure-chip-positive` in Layout header with `<Badge variant="success">`
- [ ] Replace `.secure-chip-neutral` in Layout header with `<Badge>`
- [ ] Replace `riskClass()` colored spans in Overview table with `<Badge>` severity variants
- [ ] Replace `riskClass()` colored spans in Endpoints list with `<Badge>` severity variants
- [ ] Replace `severityTone()` spans in Vulnerabilities table with `<Badge>` severity variants
- [ ] Replace `severityTone()` spans in Vulnerabilities mobile cards with `<Badge>` severity variants
- [ ] Replace `.secure-chip-neutral` in Patches table (status) with `<Badge>`
- [ ] Replace `.secure-chip-warning` in Policies table (severity) with `<Badge variant="warning">`
- [ ] Replace `.secure-chip-neutral` in Compliance (violation status) with `<Badge>`
- [ ] Replace `socketBadgeClass()` spans in Endpoints (WS status) with `<Badge>`
- [ ] Replace `socketBadgeClass()` spans in Patches (WS status) with `<Badge>`
- [ ] Replace `getRiskTone()` spans in Overview mobile cards with `<Badge>`

#### Card Replacements

- [ ] Replace `.secure-panel` in Overview (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Overview (metric cards) with `<Card>`
- [ ] Replace `.secure-panel` in Overview (quick action cards) with `<Card>`
- [ ] Replace `.secure-panel` in Overview (fleet snapshot section) with `<Card>`
- [ ] Replace `.secure-panel` in Endpoints (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Endpoints (device inventory) with `<Card>`
- [ ] Replace `.secure-panel` in Endpoints (endpoint detail) with `<Card>`
- [ ] Replace `.secure-panel` in Vulnerabilities (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Vulnerabilities (KPI cards) with `<Card>`
- [ ] Replace `.secure-panel` in Vulnerabilities (CVE findings section) with `<Card>`
- [ ] Replace `.secure-panel` in Patches (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Patches (create deployment) with `<Card>`
- [ ] Replace `.secure-panel` in Patches (selected job) with `<Card>`
- [ ] Replace `.secure-panel` in Patches (job list section) with `<Card>`
- [ ] Replace `.secure-panel` in Policies (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Policies (create policy form) with `<Card>`
- [ ] Replace `.secure-panel` in Policies (simulate policy form) with `<Card>`
- [ ] Replace `.secure-panel` in Policies (existing policies table) with `<Card>`
- [ ] Replace `.secure-panel` in Policies (resolve conflict form) with `<Card>`
- [ ] Replace `.secure-panel` in Compliance (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Compliance (KPI cards) with `<Card>`
- [ ] Replace `.secure-panel` in Compliance (violations table) with `<Card>`
- [ ] Replace `.secure-panel` in Logs (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Logs (audit events list) with `<Card>`
- [ ] Replace `.secure-panel` in Logs (event detail) with `<Card>`
- [ ] Replace `.secure-panel` in Integrations (header section) with `<Card>`
- [ ] Replace `.secure-panel` in Integrations (Gate evaluation card) with `<Card>`
- [ ] Replace `.secure-panel` in Integrations (Atlas remediation card) with `<Card>`
- [ ] Replace `.secure-panel` in Integrations (Capital Hub sync card) with `<Card>`
- [ ] Replace `.secure-panel` in Integrations (result section) with `<Card>`
- [ ] Replace `.secure-panel` in WipeDevice (header section) with `<Card>`
- [ ] Replace `.secure-panel` in WipeDevice (wizard section) with `<Card>`
- [ ] Replace `.secure-panel-muted` mobile cards in Overview with `<Card variant="muted">`
- [ ] Replace `.secure-panel-muted` mobile cards in Vulnerabilities with `<Card variant="muted">`
- [ ] Replace `.secure-panel-muted` mobile cards in Patches with `<Card variant="muted">`
- [ ] Replace `.secure-panel-muted` mobile cards in Policies with `<Card variant="muted">`
- [ ] Replace `.secure-panel-muted` mobile cards in Compliance with `<Card variant="muted">`

#### Table Replacements

- [ ] Replace custom `<table>` in Overview (fleet snapshot) with `<Table>` from orbit-ui
- [ ] Replace custom `<table>` in Vulnerabilities (CVE findings) with `<Table>`
- [ ] Replace custom `<table>` in Patches (patch jobs) with `<Table>`
- [ ] Replace custom `<table>` in Policies (existing policies) with `<Table>`
- [ ] Replace custom `<table>` in Compliance (policy violations) with `<Table>`

#### Modal Replacements

- [ ] Add `<Modal>` for device wipe confirmation (pre-wizard check)
- [ ] Add `<Modal>` for policy delete confirmation
- [ ] Add `<Modal>` for patch job cancellation
- [ ] Add `<Modal>` for endpoint retire confirmation
- [ ] Add `<Modal>` for lock device confirmation
- [ ] Add `<Modal>` for vulnerability detail view
- [ ] Add `<Modal>` for CVE detail overlay
- [ ] Add `<Modal>` for audit log detail overlay (replace inline detail)

#### Sidebar Replacement

- [ ] Replace custom sidebar `<aside>` in Layout.tsx with `<Sidebar>` from orbit-ui
- [ ] Replace custom mobile sidebar toggle with `useSidebar()` hook
- [ ] Replace custom nav item active state logic with `<Sidebar.Item>` active prop
- [ ] Replace custom sidebar header with `<Sidebar.Header>`
- [ ] Replace custom sidebar footer with `<Sidebar.Footer>`
- [ ] Replace custom mobile overlay with Sidebar's built-in mobile drawer

#### EmptyState / Loading / Error Replacements

- [ ] Replace custom `EmptyState` component in StateViews.tsx with `<EmptyState>` from orbit-ui
- [ ] Replace custom `LoadingState` component with `<Spinner>` + text or `<PageLoader>`
- [ ] Replace custom `ErrorState` component with `<Alert variant="error">`
- [ ] Replace custom `KpiSkeletonGrid` with `<SkeletonCard>` grid
- [ ] Replace custom `TableSkeleton` with `<Skeleton>` rows

#### Additional Component Adoptions

- [ ] Adopt `<Tabs>` in Endpoint detail view (Overview / Vulnerabilities / Telemetry / Violations / Actions)
- [ ] Adopt `<Tabs>` in Overview for preset switching (SecOps / IT Ops / Compliance)
- [ ] Adopt `<Tooltip>` for risk score explanations
- [ ] Adopt `<Tooltip>` for compliance status explanations
- [ ] Adopt `<Tooltip>` for truncated CVE descriptions
- [ ] Adopt `<Tooltip>` for WS connection status
- [ ] Adopt `<Avatar>` for user identity in Layout header (replace custom `SU` circle)
- [ ] Adopt `<Progress>` for patch compliance percentage in Overview
- [ ] Adopt `<Progress>` for compliance posture percentage
- [ ] Adopt `<Progress>` for vulnerability remediation progress
- [ ] Adopt `<Skeleton>` for Logs page loading state
- [ ] Adopt `<Skeleton>` for Integrations page loading state
- [ ] Adopt `<Spinner>` for form submission states
- [ ] Adopt `<Alert>` for offline banner (replace custom red banner in App.tsx)
- [ ] Adopt `<Alert>` for top risk CVE banner in Vulnerabilities
- [ ] Adopt `<Alert>` for simulation result in Policies
- [ ] Adopt `<Alert>` for conflict resolution result in Policies
- [ ] Adopt `<DatePicker>` for patch scheduling
- [ ] Adopt `<DatePicker>` for vulnerability due dates
- [ ] Adopt `<DatePicker>` for audit log date range filtering
- [ ] Adopt `<Pagination>` for Endpoints page pagination (replace custom Previous/Next)
- [ ] Adopt `<Pagination>` for Vulnerabilities list
- [ ] Adopt `<Pagination>` for Patch jobs list
- [ ] Adopt `<Pagination>` for Audit log list
- [ ] Adopt `<Steps>` / `<Stepper>` in WipeDevice wizard (replace custom step buttons)
- [ ] Adopt `<Breadcrumb>` in Layout header for navigation path
- [ ] Adopt `<Dropdown>` for user menu in Layout header
- [ ] Adopt `<Dropdown>` for bulk actions on endpoint list
- [ ] Adopt `<Drawer>` / `<Sheet>` for endpoint detail panel (replace inline)
- [ ] Adopt `<Checkbox>` from orbit-ui in WipeDevice step 1 (replace native checkboxes)
- [ ] Adopt `<Switch>` for crypto erase toggle in WipeDevice step 2
- [ ] Adopt `<Switch>` for auto-patching toggle
- [ ] Adopt `<Tag>` / `<Chip>` for endpoint tags display
- [ ] Adopt `<Tag>` / `<Chip>` for vulnerability affected packages
- [ ] Adopt `<Accordion>` for policy config sections
- [ ] Adopt `<Accordion>` for compliance framework details
- [ ] Adopt `<CommandPalette>` for global search across endpoints/CVEs/policies
- [ ] Adopt `<Toast>` / `useToast()` for action confirmations (lock, wipe, create)
- [ ] Adopt `<Divider>` for section separation in detail views
- [ ] Adopt `<Radio>` / `<RadioGroup>` for wipe mode selection (replace select)
- [ ] Adopt `<ButtonGroup>` for table density toggle (replace select dropdown)
- [ ] Adopt `<Popover>` for inline help/context on KPI cards

### 2.3 ModuleShell Component

- [ ] Evaluate whether `ModuleShell.tsx` is still used (appears unused in routing)
- [ ] If unused, remove `ModuleShell.tsx`
- [ ] If used, migrate to orbit-ui components

---

## 3. Dark Mode

### 3.1 Global / Shell

- [ ] Body background: replace hardcoded gradient with dark-mode-aware orbit surface tokens
- [ ] Sidebar gradient (`from-slate-950 via-slate-900 to-slate-800`): verify dark mode appearance
- [ ] Sidebar border (`border-slate-700/70`): use `border-border-default` token
- [ ] Header bar (`bg-surface-base/75`): verify dark mode transparency
- [ ] Offline banner (`bg-red-500`): verify dark mode contrast
- [ ] Suspense fallback (`bg-slate-50`): replace with `bg-surface-base`
- [ ] Mobile sidebar overlay (`bg-slate-950/45`): use orbit overlay token
- [ ] Scrollbar styling: add dark mode scrollbar colors
- [ ] `.secure-shell::before` grid pattern: verify dark mode visibility

### 3.2 Overview / Dashboard Page

- [ ] Page title (`text-slate-900`): use `text-content-primary`
- [ ] Page subtitle (`text-slate-600`): use `text-content-secondary`
- [ ] Preset label (`text-slate-500`): use `text-content-muted`
- [ ] Metric card labels (`text-slate-500`): dark mode audit
- [ ] Metric card values (`text-slate-900`): dark mode audit
- [ ] Metric card subtexts (`text-slate-500`): dark mode audit
- [ ] Quick action titles (`text-slate-900`): dark mode audit
- [ ] Quick action descriptions (`text-slate-600`): dark mode audit
- [ ] Fleet snapshot table header (`text-slate-500`): dark mode audit
- [ ] Fleet snapshot table cells (`text-slate-700`, `text-slate-600`): dark mode audit
- [ ] Risk tone badges (red/amber/emerald backgrounds): verify dark mode contrast
- [ ] Compliance status text in table: dark mode audit
- [ ] Preset select dropdown: dark mode styling
- [ ] Mobile card backgrounds (`bg-surface-base`): verify dark mode

### 3.3 Endpoints Page

- [ ] Page title (`text-slate-900`): dark mode audit
- [ ] Search input: dark mode styling
- [ ] Device inventory heading: dark mode audit
- [ ] Device list items: dark mode hover/active states
- [ ] Device hostname text (`text-slate-900`): dark mode audit
- [ ] Device metadata text (`text-slate-500`): dark mode audit
- [ ] Risk score badges: dark mode contrast
- [ ] Pagination buttons: dark mode styling
- [ ] Endpoint detail panel: dark mode audit
- [ ] Detail info card (`bg-slate-50 border-slate-200`): dark mode tokens
- [ ] Telemetry gauge cards (`bg-slate-50`): dark mode tokens
- [ ] Open vulnerabilities / violations cards: dark mode borders
- [ ] Remote actions section: dark mode borders and text
- [ ] Command reason input: dark mode styling
- [ ] Lock/Wipe buttons: dark mode hover states
- [ ] Command status/error messages: dark mode text contrast
- [ ] WS status badge: dark mode contrast
- [ ] Last event timestamp text: dark mode audit

### 3.4 Vulnerabilities Page

- [ ] Page title and subtitle: dark mode audit
- [ ] Severity filter select: dark mode styling
- [ ] Status filter select: dark mode styling
- [ ] KPI cards (unique CVEs, affected endpoints, exploitable): dark mode audit
- [ ] Top risk banner (`bg-red-50 border-red-200 text-red-900`): dark mode semantic tokens
- [ ] CVE table header row: dark mode audit
- [ ] CVE table body cells: dark mode text colors
- [ ] Severity badges in table: dark mode contrast
- [ ] CVE description truncated text: dark mode audit
- [ ] Mobile CVE cards: dark mode backgrounds and borders
- [ ] Mobile card metadata chips (`bg-surface-base`): verify dark mode
- [ ] Table density control: dark mode styling

### 3.5 Patches Page

- [ ] Page title and subtitle: dark mode audit
- [ ] WS status badge: dark mode contrast
- [ ] Create deployment form: dark mode inputs and labels
- [ ] Scope select: dark mode styling
- [ ] Version input: dark mode styling
- [ ] Software name input: dark mode styling
- [ ] Scheduled time input: dark mode styling
- [ ] Create button: dark mode hover
- [ ] Selected job detail panel: dark mode text
- [ ] Patch jobs table header: dark mode audit
- [ ] Patch jobs table rows: dark mode audit
- [ ] Selected row highlight (`bg-emerald-50`): dark mode equivalent
- [ ] Hover row state (`hover:bg-slate-50`): dark mode equivalent
- [ ] Status filter select: dark mode styling
- [ ] Mobile patch job cards: dark mode audit
- [ ] Table density control: dark mode styling

### 3.6 Policies Page

- [ ] Page title and subtitle: dark mode audit
- [ ] Create policy form card: dark mode styling
- [ ] Simulate policy form card: dark mode styling
- [ ] Simulation result card (`bg-slate-50 border-slate-200`): dark mode tokens
- [ ] Existing policies table: dark mode audit
- [ ] Policy list mobile cards: dark mode audit
- [ ] Resolve conflict form: dark mode styling
- [ ] Conflict result card (`bg-amber-50 border-amber-200`): dark mode tokens
- [ ] All input fields in forms: dark mode styling
- [ ] All select dropdowns: dark mode styling

### 3.7 Compliance Page

- [ ] Page title and subtitle: dark mode audit
- [ ] KPI cards (total devices, non-compliant %, non-compliant count): dark mode audit
- [ ] Violation table header: dark mode audit
- [ ] Violation table cells: dark mode text
- [ ] Mobile violation cards: dark mode audit
- [ ] Status filter input: dark mode styling
- [ ] Table density control: dark mode styling

### 3.8 Deployment Logs Page

- [ ] Page title and subtitle: dark mode audit
- [ ] Audit events list panel: dark mode audit
- [ ] List item hover/active states: dark mode tokens
- [ ] Action filter input: dark mode styling
- [ ] Event detail panel: dark mode audit
- [ ] Metadata JSON `<pre>` block (`bg-slate-900 text-slate-100`): verify dark mode
- [ ] Detail field labels: dark mode audit
- [ ] Detail field values: dark mode audit

### 3.9 Integrations Page

- [ ] Page title and subtitle: dark mode audit
- [ ] Gate access evaluation card: dark mode audit
- [ ] Atlas remediation card: dark mode audit
- [ ] Capital Hub sync card: dark mode audit
- [ ] All form labels: dark mode text
- [ ] All input fields: dark mode styling
- [ ] All select dropdowns: dark mode styling
- [ ] All submit buttons: dark mode hover states
- [ ] Integration result JSON `<pre>` block: dark mode verification
- [ ] Empty state for no result: dark mode audit

### 3.10 Wipe Device Wizard Page

- [ ] Page title (`text-slate-900`): dark mode audit
- [ ] "Critical Action" label (`text-red-700`): dark mode contrast
- [ ] Back to Endpoints link: dark mode styling
- [ ] Step indicator buttons: dark mode active/inactive states
- [ ] Step 1 warning banner (`bg-amber-50 border-amber-200`): dark mode tokens
- [ ] Step 1 checkbox labels with borders: dark mode styling
- [ ] Step 2 wipe mode select: dark mode styling
- [ ] Step 2 schedule input: dark mode styling
- [ ] Step 2 crypto erase checkbox: dark mode styling
- [ ] Step 2 justification textarea: dark mode styling
- [ ] Step 3 final warning banner (`bg-red-50 border-red-200`): dark mode tokens
- [ ] Step 3 serial confirm input: dark mode styling
- [ ] Step 3 MFA code input: dark mode styling
- [ ] Success message banner (`bg-emerald-50 border-emerald-200`): dark mode tokens
- [ ] Error message banner (`bg-red-50 border-red-200`): dark mode tokens
- [ ] Post-wipe info card (`bg-slate-50 border-slate-200`): dark mode tokens

### 3.11 Shared Components Dark Mode

- [ ] `LoadingState` component: dark mode text and border
- [ ] `EmptyState` component: dark mode text and border
- [ ] `ErrorState` component: dark mode red tones
- [ ] `KpiSkeletonGrid` pulse colors: dark mode skeleton tones
- [ ] `TableSkeleton` pulse colors: dark mode skeleton tones
- [ ] `TableDensityControl` select: dark mode styling
- [ ] `ModuleShell` design sources/API lists (`bg-slate-50`): dark mode tokens

---

## 4. Core Features

### 4A. Overview / Dashboard

#### 4A.1 Security Posture Score

- [ ] Security posture score (0-100 gauge) visual component
- [ ] Gauge color changes by risk level (green/amber/red)
- [ ] Gauge animated transition on data load
- [ ] Gauge tooltip showing breakdown factors
- [ ] Gauge dark mode styling

#### 4A.2 Persona Presets

- [x] SecOps preset with threat-focused metrics
- [x] IT Ops preset with fleet health metrics
- [x] Compliance preset with audit-focused metrics
- [x] Preset persistence to localStorage
- [x] Preset sync to server via UI preferences API
- [x] Preset hydration from server on load
- [ ] Preset selection via orbit-ui `<Tabs>` or `<ButtonGroup>`
- [ ] Keyboard shortcut to cycle presets (1/2/3)

#### 4A.3 KPI Metric Cards

- [x] Managed Endpoints count (SecOps + IT Ops)
- [x] Average Risk score (SecOps + Compliance)
- [x] High-Risk Devices count (SecOps, risk >= 80)
- [x] Non-Compliant Devices count (SecOps + Compliance)
- [x] Seen In Last 24h count (IT Ops)
- [x] Encrypted Devices count (IT Ops)
- [x] Firewall Enabled count (IT Ops)
- [x] Compliant Devices count (Compliance)
- [x] KPI skeleton loading state
- [ ] KPI trend indicators (up/down arrow with % change)
- [ ] KPI sparkline charts (last 7 days trend)
- [ ] KPI click-through to relevant detail page
- [ ] KPI refresh animation on data update

#### 4A.4 Quick Actions

- [x] SecOps: Investigate CVE Exposure -> /vulnerabilities
- [x] SecOps: Drill Into High-Risk Endpoints -> /endpoints
- [x] SecOps: Launch Emergency Patching -> /patches
- [x] IT Ops: Inspect Fleet Health -> /endpoints
- [x] IT Ops: Schedule Patch Window -> /patches
- [x] IT Ops: Sync Device Lifecycle -> /integrations
- [x] Compliance: Run Compliance Review -> /compliance
- [x] Compliance: Simulate Policy Impact -> /policies
- [x] Compliance: Collect Audit Evidence -> /logs
- [ ] Quick action icons per card
- [ ] Quick action keyboard shortcuts

#### 4A.5 Fleet Snapshot Table

- [x] First 8 endpoints displayed
- [x] Hostname column
- [x] OS column (type + version)
- [x] Risk score column with color badge
- [x] Compliance status column
- [x] Last seen column (formatted date)
- [x] Table density control (compact/comfortable)
- [x] Table density persistence
- [x] Mobile card layout for small screens
- [x] Empty state when no endpoints
- [ ] Click row to navigate to endpoint detail
- [ ] Sort columns (hostname, risk, compliance, last seen)
- [ ] "View All" link to /endpoints
- [ ] Virtual scrolling for large fleet snapshots

#### 4A.6 Dashboard Charts (Not Yet Implemented)

- [ ] Threat timeline chart (incidents over last 30 days)
- [ ] Vulnerability severity distribution pie/donut chart
- [ ] Endpoint status distribution chart (online/offline/at-risk)
- [ ] Patch compliance trend chart (7/30/90 days)
- [ ] Top 5 critical vulnerabilities callout
- [ ] Risk score distribution histogram
- [ ] Compliance framework coverage chart (SOC2/GDPR/ISO 27001)
- [ ] Recent alerts / incidents feed widget
- [ ] Active threat map / timeline visualization
- [ ] Endpoint enrollment trend chart

### 4B. Endpoints

#### 4B.1 Device Inventory List

- [x] Device list with hostname, OS, serial, compliance, risk, last seen
- [x] Device search by hostname, serial number, OS type
- [x] Pagination (page/pageSize) with Previous/Next controls
- [x] Total device count displayed
- [x] Selected device highlight state
- [x] Auto-select first device on load
- [x] Preserve selection on page change if device still in list
- [x] Loading state for device list
- [x] Empty state for no matches
- [x] Error state for API failure
- [ ] Filter by OS type dropdown
- [ ] Filter by compliance status (green/yellow/red)
- [ ] Filter by risk score range (slider)
- [ ] Filter by enrollment date range
- [ ] Filter by device type
- [ ] Filter by tags
- [ ] Sort by hostname (A-Z / Z-A)
- [ ] Sort by risk score (highest first)
- [ ] Sort by last seen (most recent)
- [ ] Sort by compliance status
- [ ] Bulk selection with checkboxes
- [ ] Bulk actions: lock, tag, assign group, export
- [ ] Export endpoints to CSV
- [ ] Export endpoints to JSON
- [ ] Virtual scrolling for 1000+ devices
- [ ] Device status indicator (online/offline/isolated dot)
- [ ] Last heartbeat relative time ("2 min ago")

#### 4B.2 Endpoint Detail View

- [x] Hostname and serial number display
- [x] Encryption status (Yes/No)
- [x] Firewall status (On/Off)
- [x] Compliance status
- [x] Risk score
- [x] Open vulnerabilities count
- [x] Policy violations count
- [ ] Full system info panel (CPU, RAM, disk, model, manufacturer)
- [ ] Installed software inventory list
- [ ] Network interfaces (IP, MAC, SSID)
- [ ] Logged-in users
- [ ] Agent version and status
- [ ] Agent last check-in time
- [ ] Enrollment date
- [ ] Device owner / assigned user
- [ ] Device group / department
- [ ] Tags management (add/remove tags)
- [ ] Patch history timeline
- [ ] Policy assignment list
- [ ] Risk score breakdown (what contributes to score)
- [ ] Activity timeline (recent events for this device)

#### 4B.3 Telemetry

- [x] Latest telemetry sample (CPU, RAM, Disk usage)
- [x] Real-time telemetry updates via WebSocket
- [x] Telemetry collection buffer (last 50 samples)
- [ ] CPU usage trend chart (line graph over time)
- [ ] RAM usage trend chart
- [ ] Disk usage trend chart
- [ ] Running services list
- [ ] Network throughput metrics
- [ ] Process list (top processes by CPU/memory)
- [ ] Telemetry collection interval indicator
- [ ] Telemetry data export

#### 4B.4 WebSocket (Real-time)

- [x] WebSocket connection to `/api/v1/ws/patch/{tenantId}`
- [x] Connection state tracking (offline/connecting/online/error)
- [x] Auto-reconnect on close (3s delay)
- [x] Ping/keep-alive every 25 seconds
- [x] Parse incoming JSON events
- [x] Update device `last_seen` on heartbeat/telemetry events
- [x] Inject real-time telemetry into selected device view
- [x] Display WS state badge (color-coded)
- [x] Display last event timestamp
- [ ] Exponential backoff for reconnections
- [ ] Max reconnection attempts with user notification
- [ ] Connection quality indicator
- [ ] Event rate display (events/sec)
- [ ] WebSocket auth token refresh on expiry
- [ ] Graceful degradation to polling when WS unavailable

#### 4B.5 Remote Actions

- [x] Lock device command (POST to API)
- [x] Lock device role-gated (admin + soc_analyst only)
- [x] Command reason input (optional, max 400 chars)
- [x] Command busy/success/error states
- [x] Link to Wipe Device wizard (admin only)
- [x] Read-only message for insufficient role
- [ ] Restart device command
- [ ] Isolate device command (network isolation)
- [ ] Un-isolate device command
- [ ] Push config update command
- [ ] Run scan command (trigger vulnerability scan)
- [ ] Collect diagnostics command
- [ ] Uninstall agent command
- [ ] Remote shell (future feature)
- [ ] Command history for this device
- [ ] Command confirmation modal before execution
- [ ] Command audit trail logging

#### 4B.6 Endpoint Groups & Tags

- [ ] Create endpoint groups
- [ ] Assign endpoints to groups
- [ ] Group-based policy assignment
- [ ] Group-based patch deployment targeting
- [ ] Tag management (create, delete, rename tags)
- [ ] Filter by tag in endpoint list
- [ ] Bulk tag assignment
- [ ] Auto-tagging rules based on OS, risk, compliance

### 4C. Vulnerabilities

#### 4C.1 Vulnerability List

- [x] CVE ID column
- [x] Severity column with color-coded badge
- [x] CVSS score column
- [x] Affected devices count
- [x] Exploitable devices count
- [x] Patchable devices count
- [x] Open findings count
- [x] Published date column
- [x] Description (truncated with line-clamp)
- [x] Filter by severity (critical/high/medium/low)
- [x] Filter by status (open/remediated/ignored)
- [x] Table density control
- [x] Mobile card layout
- [x] Empty state for no results
- [x] Loading skeleton
- [ ] Search by CVE ID
- [ ] Search by description keyword
- [ ] Sort by severity
- [ ] Sort by CVSS score
- [ ] Sort by affected endpoints count
- [ ] Sort by published date
- [ ] Pagination with page size control
- [ ] Export vulnerability list to CSV
- [ ] Export vulnerability list to JSON
- [ ] Export vulnerability list to PDF
- [ ] Virtual scrolling for large result sets

#### 4C.2 KPI Summary Cards

- [x] Unique CVEs count
- [x] Affected endpoints count
- [x] Exploitable findings count
- [x] KPI skeleton loading
- [ ] Remediated in last 7 days count
- [ ] New in last 7 days count
- [ ] Average time to remediate metric
- [ ] EPSS (Exploit Prediction Scoring System) integration

#### 4C.3 Top Risk Banner

- [x] Highest current risk CVE highlighted
- [x] Max risk score displayed
- [ ] Link to CVE detail view
- [ ] Link to affected endpoints list
- [ ] Link to NVD/MITRE page

#### 4C.4 Vulnerability Detail View (Not Yet Implemented)

- [ ] CVE detail modal/drawer
- [ ] Full CVE description
- [ ] CVSS vector string breakdown
- [ ] Impact analysis (confidentiality, integrity, availability)
- [ ] Remediation steps
- [ ] External references (NVD, vendor advisories)
- [ ] Affected endpoints list for this CVE
- [ ] Exploit availability status
- [ ] Patch availability status
- [ ] Risk accept workflow (with expiry date and justification)
- [ ] Assignment to team member for remediation
- [ ] False positive flagging
- [ ] CVE timeline (first seen, last seen, status changes)
- [ ] Related CVEs

#### 4C.5 Vulnerability Analytics (Not Yet Implemented)

- [ ] Vulnerability trend chart (open/closed over time)
- [ ] Severity distribution chart
- [ ] Mean time to remediate (MTTR) chart
- [ ] Top affected packages/software
- [ ] Top affected endpoints
- [ ] Aging report (unresolved vulnerabilities by age)
- [ ] SLA compliance tracking (remediation within defined windows)

#### 4C.6 CVE Feed Integration

- [ ] Automated CVE feed from NVD API
- [ ] CVE feed from OSV (Open Source Vulnerabilities)
- [ ] CVE matching against installed software inventory
- [ ] New CVE notification alerts
- [ ] CVE enrichment with EPSS scores
- [ ] CVE enrichment with KEV (Known Exploited Vulnerabilities) catalog

### 4D. Patches

#### 4D.1 Patch Job Creation

- [x] Target scope selector (all/group/device)
- [x] Software name input
- [x] Version input
- [x] Scheduled time input (datetime-local)
- [x] Tenant ID detection and display
- [x] Create patch job API call
- [x] Form reset after successful creation
- [x] Auto-refresh job list after creation
- [x] Error handling for missing tenant ID
- [x] Error handling for missing schedule time
- [ ] Group selector when scope is "group"
- [ ] Device selector when scope is "device"
- [ ] Patch selection from available patches catalog
- [ ] Maintenance window awareness (warn if outside window)
- [ ] Pre-deployment validation checks
- [ ] Approval workflow for critical patches
- [ ] Patch job notes/description field
- [ ] Rollback plan specification
- [ ] Max failure threshold before auto-rollback

#### 4D.2 Patch Job List

- [x] Job ID column
- [x] Software name column
- [x] Version column
- [x] Target scope column
- [x] Status column (pending/queued/dispatched/acknowledged/success/failed/rolled_back)
- [x] Scheduled time column
- [x] Status filter dropdown
- [x] Table density control
- [x] Click to select job
- [x] Selected row highlight
- [x] Mobile card layout
- [x] Empty state
- [x] Loading skeleton
- [ ] Sort by scheduled time
- [ ] Sort by status
- [ ] Sort by software name
- [ ] Pagination
- [ ] Bulk cancel patch jobs
- [ ] Export patch jobs to CSV
- [ ] Job progress indicator (endpoints patched / total)

#### 4D.3 Patch Job Detail

- [x] Job ID display
- [x] Software name display
- [x] Version display
- [x] Scope display
- [x] Status display
- [x] Scheduled time (formatted)
- [x] Executed time (formatted, or "Not yet")
- [x] Detail hydration via API on selection
- [ ] Per-endpoint patch status breakdown
- [ ] Failure reasons for failed endpoints
- [ ] Retry failed endpoints button
- [ ] Cancel job button
- [ ] Rollback button for completed jobs
- [ ] Patch job timeline (created -> queued -> dispatched -> success/failed)
- [ ] Execution log / output viewer
- [ ] Duration metric (time from dispatch to completion)

#### 4D.4 Real-time Patch Updates

- [x] WebSocket connection for patch events
- [x] Auto-refresh job list on WS events
- [x] WS state badge display
- [x] Last event timestamp
- [x] Auto-reconnect on disconnect
- [ ] Per-job live status updates without full refresh
- [ ] Push notifications for job completion/failure
- [ ] Progress bar animation during deployment

#### 4D.5 Patch Management Features (Not Yet Implemented)

- [ ] Available patches catalog (OS + application patches)
- [ ] Patch detail view (vendor, severity, release date, size, changelog)
- [ ] Patch rollback mechanism (revert to previous version)
- [ ] Patch compliance dashboard (% of fleet up to date)
- [ ] Patch approval workflow (request -> review -> approve -> deploy)
- [ ] Patch groups (group endpoints for phased rollout)
- [ ] Auto-patching rules (auto-deploy critical patches)
- [ ] Maintenance window configuration
- [ ] Patch exclusion rules (skip certain endpoints/software)
- [ ] Patch testing/staging environment support
- [ ] Patch deployment history per endpoint
- [ ] Patch supersedence tracking

### 4E. Policies

#### 4E.1 Policy Creation

- [x] Policy name input
- [x] Policy type selector (encryption/password/firewall/software)
- [x] Policy severity input
- [x] Config object for software type (minimum_risk_score)
- [x] Create policy API call
- [x] Form reset after creation
- [x] Auto-refresh policy list after creation
- [ ] Policy description/notes field
- [ ] Policy template library (pre-configured common policies)
- [ ] Policy versioning (track changes over time)
- [ ] Policy effective date / expiry date
- [ ] Policy condition builder (visual rule editor)
- [ ] Policy target groups selector
- [ ] Policy priority/order configuration
- [ ] Import policy from JSON/YAML
- [ ] Clone existing policy

#### 4E.2 Policy List

- [x] Policy ID column
- [x] Policy name column
- [x] Policy type column
- [x] Policy severity column
- [x] Table density control
- [x] Mobile card layout
- [x] Empty state
- [x] Loading skeleton
- [ ] Policy status column (active/draft/disabled)
- [ ] Assigned groups/endpoints count column
- [ ] Compliance rate column (% of assigned endpoints compliant)
- [ ] Last evaluated time column
- [ ] Sort by name
- [ ] Sort by type
- [ ] Sort by severity
- [ ] Filter by type
- [ ] Filter by status
- [ ] Search by name
- [ ] Pagination
- [ ] Edit policy action
- [ ] Delete policy action (with confirmation)
- [ ] Enable/disable policy toggle
- [ ] Duplicate policy action
- [ ] Export policies to JSON

#### 4E.3 Policy Simulation

- [x] Simulation type selector
- [x] Config for software type (minimum risk score)
- [x] Simulation result display (policy type, scanned devices, affected devices)
- [x] Run simulation API call
- [ ] Simulation result: list of affected device IDs/hostnames
- [ ] Simulation comparison (before vs. after)
- [ ] Simulation dry-run for deployment planning
- [ ] Simulation history (past simulation runs)
- [ ] Simulation export to PDF

#### 4E.4 Policy Conflict Resolution

- [x] Preferred policy ID input
- [x] Superseded policy IDs input (comma-separated)
- [x] Resolve conflict API call
- [x] Conflict result display (status, preferred, superseded)
- [ ] Visual conflict detection (auto-detect overlapping policies)
- [ ] Conflict resolution wizard (step-by-step)
- [ ] Conflict resolution audit trail

#### 4E.5 Policy Features (Not Yet Implemented)

- [ ] Policy editor with JSON/YAML config editing
- [ ] Policy enforcement status dashboard
- [ ] Policy assignment to endpoint groups
- [ ] Policy compliance history chart
- [ ] Non-compliant device alerts per policy
- [ ] Policy exception management (exempt specific endpoints)
- [ ] Policy approval workflow
- [ ] Policy import/export in bulk
- [ ] Policy change audit log
- [ ] Policy rollback to previous version

### 4F. Compliance

#### 4F.1 Compliance Summary KPIs

- [x] Total devices count
- [x] Non-compliant percentage
- [x] Non-compliant devices count (calculated)
- [x] KPI loading state (dots)
- [ ] Compliant devices count
- [ ] Compliance trend chart (30-day)
- [ ] Compliance score (0-100)
- [ ] Most violated policy
- [ ] Endpoints with most violations

#### 4F.2 Policy Violations Table

- [x] Violation ID column
- [x] Device hostname column
- [x] Device ID column
- [x] Policy name column
- [x] Status column
- [x] Detected at column (formatted timestamp)
- [x] Status filter input
- [x] Table density control
- [x] Mobile card layout
- [x] Empty state
- [x] Loading skeleton
- [ ] Severity column
- [ ] Remediated at column
- [ ] Time to remediate column
- [ ] Sort by detection date
- [ ] Sort by severity
- [ ] Sort by policy name
- [ ] Filter by policy type
- [ ] Filter by device hostname
- [ ] Filter by date range
- [ ] Pagination with page size control
- [ ] Export violations to CSV
- [ ] Export violations to JSON
- [ ] Bulk acknowledge violations
- [ ] Bulk dismiss violations

#### 4F.3 Compliance Frameworks (Not Yet Implemented)

- [ ] SOC 2 Type II framework mapping
- [ ] ISO 27001 control mapping
- [ ] HIPAA Security Rule mapping
- [ ] PCI DSS v4.0 mapping
- [ ] GDPR Article 32 mapping
- [ ] NIST CSF 2.0 mapping
- [ ] CIS Benchmarks mapping
- [ ] Per-control status (passed/failed/in progress/N/A)
- [ ] Per-control evidence attachment
- [ ] Per-control owner assignment
- [ ] Per-control notes and comments
- [ ] Framework selector UI
- [ ] Framework progress bar (% controls met)
- [ ] Control requirement detail view

#### 4F.4 Compliance Reporting (Not Yet Implemented)

- [ ] Audit-ready report generation
- [ ] PDF export of compliance posture
- [ ] Executive summary report
- [ ] Gap analysis report
- [ ] Evidence collection workflow
- [ ] Scheduled compliance reports (weekly/monthly)
- [ ] Report template customization
- [ ] Report sharing (email, link)
- [ ] Historical compliance snapshots (point-in-time)

### 4G. Deployment Logs

#### 4G.1 Audit Event List

- [x] Audit log list with action, actor, entity, timestamp
- [x] Action filter input
- [x] Click to select event
- [x] Selected event highlight
- [x] Loading state
- [x] Empty state
- [x] Error state
- [x] Scrollable list (max-height 560px)
- [x] Fetch up to 150 events per page
- [ ] Filter by actor (user who performed action)
- [ ] Filter by entity type
- [ ] Filter by date range
- [ ] Filter by severity/importance
- [ ] Search across all log fields
- [ ] Sort by timestamp (ascending/descending)
- [ ] Pagination with page size control
- [ ] Auto-refresh / live streaming of new events
- [ ] Export logs to CSV
- [ ] Export logs to JSON
- [ ] Export logs to Syslog format
- [ ] Bulk selection and export
- [ ] Log retention policy indicator

#### 4G.2 Event Detail Panel

- [x] Event ID display
- [x] Actor display
- [x] Action display
- [x] Entity type and ID display
- [x] Timestamp display (formatted)
- [x] Metadata JSON viewer (syntax-highlighted)
- [x] Detail hydration via API on selection
- [ ] Metadata field search/filter
- [ ] Copy metadata to clipboard
- [ ] Link to related entity (device, policy, patch job)
- [ ] Previous/next event navigation
- [ ] Diff view for configuration changes

#### 4G.3 Log Features (Not Yet Implemented)

- [ ] Real-time log streaming via WebSocket/SSE
- [ ] Log level indicators (info/warning/error/critical)
- [ ] Log correlation (group related events by trace ID)
- [ ] SIEM forwarding configuration (Splunk, Datadog, Elastic)
- [ ] Log search with query syntax (field:value, AND/OR)
- [ ] Saved searches / bookmarks
- [ ] Log alerting rules (notify on specific patterns)
- [ ] Log retention configuration
- [ ] Immutable append-only log verification
- [ ] Log integrity hash chain verification

### 4H. Integrations

#### 4H.1 Gate Access Evaluation

- [x] Device selector dropdown
- [x] Threshold input (optional, numeric)
- [x] Evaluate API call
- [x] Result display (device_id, threshold, device_healthy, decision, reasons)
- [ ] Evaluation history for selected device
- [ ] Batch evaluation for multiple devices
- [ ] Auto-evaluate on device risk change
- [ ] Access policy configuration

#### 4H.2 Atlas Remediation

- [x] Title input
- [x] Severity input
- [x] Entity ID input
- [x] Create Atlas task API call
- [x] Result display
- [ ] Auto-populate entity ID from selected vulnerability
- [ ] Link back to Atlas task after creation
- [ ] Bulk remediation task creation from vulnerability list
- [ ] Remediation template selection

#### 4H.3 Capital Hub Sync

- [x] Device selector (reused from Gate)
- [x] Ownership selector (corporate/personal/contractor)
- [x] Sync API call
- [x] Result display
- [ ] Bulk device sync
- [ ] Sync status tracking
- [ ] Auto-sync on enrollment/retirement
- [ ] Cost tracking per device

#### 4H.4 Integration Result Display

- [x] JSON result viewer (syntax-highlighted)
- [x] Empty state when no result
- [ ] Result history (last N integration calls)
- [ ] Copy result to clipboard
- [ ] Download result as JSON file

#### 4H.5 Integrations (Not Yet Implemented)

- [ ] SIEM integration (Splunk, Datadog, Elastic Security)
- [ ] Ticketing integration (Jira, ServiceNow, TurboTick)
- [ ] Notification channels (Slack, Teams, email, SMS, PagerDuty)
- [ ] API key management (create, revoke, rotate)
- [ ] Webhook management (configure outbound webhooks)
- [ ] Connect (Orbit) integration for security alerts in chat
- [ ] Mail (Orbit) integration for compliance report delivery
- [ ] Calendar (Orbit) integration for maintenance windows
- [ ] SSO/SAML provider integration configuration
- [ ] CMDB integration for asset management
- [ ] EDR/XDR data feed integration
- [ ] Cloud provider integrations (AWS, Azure, GCP)
- [ ] Integration health monitoring dashboard
- [ ] Integration event log

### 4I. Wipe Device Wizard

#### 4I.1 Step 1: Verify Prerequisites

- [x] Device hostname and serial number display
- [x] Admin role check (redirects non-admins)
- [x] Backup confirmation checkbox
- [x] Notification confirmation checkbox
- [x] Recovery/legal approval checkbox
- [x] All three checkboxes required to proceed
- [x] Warning banner for destructive action
- [x] Continue to Options button (disabled until all checked)
- [ ] Link to backup policy documentation
- [ ] Link to incident response playbook
- [ ] Automatic backup status check from device

#### 4I.2 Step 2: Wipe Options

- [x] Wipe mode selector (immediate/scheduled)
- [x] Schedule datetime input (disabled for immediate mode)
- [x] Cryptographic erase toggle
- [x] Justification textarea (min 8 chars)
- [x] Back button to step 1
- [x] Continue to Authorization button (disabled until valid)
- [ ] Estimated wipe duration display
- [ ] Impact summary (data that will be lost)
- [ ] Notification preview (who will be notified)

#### 4I.3 Step 3: Authorize

- [x] Serial number confirmation input (must match device serial)
- [x] MFA code input (min 6 chars)
- [x] Serial mismatch error display
- [x] Invalid MFA error display
- [x] Wipe API call with reason, serial confirmation, MFA token
- [x] Success state with command queued message
- [x] Error state with failure message
- [x] Submitting/busy state
- [x] Navigate back to Endpoints after success
- [x] Final warning banner (irreversible action)
- [ ] MFA code auto-focus
- [ ] MFA code masked input
- [ ] Countdown timer after authorization (grace period to cancel)
- [ ] Wipe receipt/confirmation download

#### 4I.4 Wipe Wizard Navigation

- [x] Step indicator buttons (1/2/3) with active styling
- [x] Step buttons disabled until prerequisites met
- [x] Click step buttons to navigate between completed steps
- [x] Back to Endpoints link
- [ ] Replace step buttons with orbit-ui `<Steps>` / `<Stepper>`
- [ ] Progress indicator showing completion percentage
- [ ] Unsaved changes warning on navigation away

### 4J. Threat Detection (Not Yet Implemented)

- [ ] Real-time threat alert feed
- [ ] Alert severity levels (critical/high/medium/low/info)
- [ ] Alert detail view (source, description, affected endpoints, IOCs)
- [ ] IOC matching engine (indicators of compromise)
- [ ] Behavioral analysis alerts (anomalous process execution)
- [ ] File integrity monitoring alerts
- [ ] Malware detection alerts
- [ ] Quarantine action (isolate suspicious files)
- [ ] Quarantine review and release workflow
- [ ] Investigation workspace (pivot from alert to endpoint data)
- [ ] Threat intelligence feed integration
- [ ] MITRE ATT&CK mapping for detected threats
- [ ] Kill chain visualization
- [ ] Alert correlation (group related alerts)
- [ ] False positive management
- [ ] Threat hunting query interface
- [ ] Custom detection rules editor
- [ ] Machine learning anomaly detection configuration

### 4K. Incident Response (Not Yet Implemented)

- [ ] Incident creation from threat alert
- [ ] Incident severity classification
- [ ] Incident timeline view (chronological events)
- [ ] Incident containment actions (isolate, block, quarantine)
- [ ] Evidence collection workflow (screenshots, logs, artifacts)
- [ ] Playbook library (pre-defined response procedures)
- [ ] Playbook execution tracker (step-by-step checklist)
- [ ] Incident assignment to team members
- [ ] Incident communication log
- [ ] Incident status tracking (open/investigating/contained/resolved/closed)
- [ ] Post-mortem / lessons learned template
- [ ] Root cause analysis documentation
- [ ] Incident metrics (MTTD, MTTC, MTTR)
- [ ] Incident report generation (PDF)
- [ ] Regulatory notification tracker (breach notification requirements)
- [ ] Evidence chain of custody log

### 4L. Alerting & Notifications (Not Yet Implemented)

- [ ] Alert rule creation (condition -> threshold -> action)
- [ ] Alert channels (email, Slack, webhook, PagerDuty, SMS)
- [ ] Alert escalation policies (if not acknowledged in X minutes, escalate)
- [ ] Alert suppression rules (don't alert during maintenance windows)
- [ ] Alert deduplication (group identical alerts)
- [ ] Alert acknowledgement workflow
- [ ] Alert snooze/mute for specific duration
- [ ] Alert history and analytics
- [ ] On-call schedule integration
- [ ] Alert routing rules (by severity, by team, by endpoint group)
- [ ] Custom alert templates
- [ ] Alert testing (send test notification)

### 4M. Reports & Analytics (Not Yet Implemented)

- [ ] Executive security summary report
- [ ] Compliance posture report
- [ ] Vulnerability management report
- [ ] Patch compliance report
- [ ] Incident summary report
- [ ] Endpoint inventory report
- [ ] Risk trend analysis report
- [ ] Scheduled report delivery (daily/weekly/monthly)
- [ ] Ad-hoc report builder (select metrics, date range, filters)
- [ ] Report template library
- [ ] Report export formats (PDF, CSV, Excel, HTML)
- [ ] Report sharing (email, link with expiry)
- [ ] Dashboard widgets for custom report views
- [ ] Year-over-year comparison charts
- [ ] Board-level security metrics summary
- [ ] Benchmark comparison (vs industry averages)

---

## 5. API Integration

### 5.1 Auth & Request Infrastructure

- [x] `secureRequest()` generic fetch wrapper
- [x] Bearer token from env or localStorage (multi-source fallback)
- [x] Tenant ID from env, localStorage, JWT claims, or user objects
- [x] `Authorization` header on all requests
- [x] `X-Tenant-ID` header on all requests
- [x] Error parsing from API responses (detail, error, status fallback)
- [x] Content-Type: application/json for request bodies
- [x] Accept: application/json header
- [x] Query string builder with null/empty filtering
- [ ] Token refresh / rotation handling
- [ ] 401 interceptor (redirect to login or refresh token)
- [ ] 403 interceptor (show permission denied message)
- [ ] 429 interceptor (rate limit handling with retry)
- [ ] Request retry with exponential backoff for 5xx errors
- [ ] Request timeout configuration
- [ ] Request cancellation via AbortController
- [ ] Request deduplication (prevent duplicate concurrent requests)
- [ ] Global error handler for network failures
- [ ] API versioning awareness (handle version mismatches)

### 5.2 Device Endpoints

- [x] `GET /api/v1/devices` -- list devices (paginated)
- [x] `GET /api/v1/devices/:id` -- get single device
- [x] `GET /api/v1/devices/:id/telemetry` -- device telemetry (paginated)
- [x] `GET /api/v1/devices/:id/vulnerabilities` -- device vulnerabilities
- [x] `GET /api/v1/devices/:id/violations` -- device policy violations
- [x] `POST /api/v1/devices/:id/lock` -- lock device command
- [x] `POST /api/v1/devices/:id/wipe` -- wipe device command (MFA required)
- [ ] `POST /api/v1/devices` -- enroll new device
- [ ] `PATCH /api/v1/devices/:id` -- update device metadata
- [ ] `DELETE /api/v1/devices/:id` -- retire/decommission device
- [ ] `POST /api/v1/devices/:id/isolate` -- network isolation
- [ ] `POST /api/v1/devices/:id/unisolate` -- remove isolation
- [ ] `POST /api/v1/devices/:id/scan` -- trigger on-demand scan
- [ ] `GET /api/v1/devices/:id/software` -- installed software list
- [ ] `GET /api/v1/devices/:id/network` -- network interfaces
- [ ] `GET /api/v1/devices/:id/history` -- device event history
- [ ] `POST /api/v1/devices/bulk/lock` -- bulk lock
- [ ] `POST /api/v1/devices/bulk/tag` -- bulk tag assignment

### 5.3 Risk & Compliance Endpoints

- [x] `GET /api/v1/risk/dashboard` -- risk dashboard data
- [x] `GET /api/v1/compliance/summary` -- compliance summary
- [ ] `GET /api/v1/risk/trend` -- risk trend over time
- [ ] `GET /api/v1/risk/top-cves` -- top CVEs by risk
- [ ] `GET /api/v1/compliance/frameworks` -- available compliance frameworks
- [ ] `GET /api/v1/compliance/frameworks/:id/controls` -- controls for framework
- [ ] `PUT /api/v1/compliance/frameworks/:id/controls/:controlId` -- update control status
- [ ] `POST /api/v1/compliance/frameworks/:id/report` -- generate compliance report
- [ ] `GET /api/v1/compliance/evidence` -- evidence library

### 5.4 Vulnerability Endpoints

- [x] `GET /api/v1/vulnerabilities` -- list vulnerabilities (paginated, filtered)
- [ ] `GET /api/v1/vulnerabilities/:id` -- vulnerability detail
- [ ] `PATCH /api/v1/vulnerabilities/:id` -- update vulnerability status
- [ ] `POST /api/v1/vulnerabilities/:id/accept-risk` -- accept risk
- [ ] `POST /api/v1/vulnerabilities/:id/assign` -- assign to team member
- [ ] `POST /api/v1/vulnerabilities/:id/false-positive` -- flag as false positive
- [ ] `GET /api/v1/vulnerabilities/stats` -- vulnerability statistics
- [ ] `GET /api/v1/vulnerabilities/trend` -- vulnerability trend data

### 5.5 Patch Endpoints

- [x] `GET /api/v1/patch` -- list patch jobs (paginated, filtered)
- [x] `POST /api/v1/patch` -- create patch job
- [x] `GET /api/v1/patch/:id` -- get patch job detail
- [x] `WS /api/v1/ws/patch/:tenantId` -- patch event WebSocket
- [ ] `PATCH /api/v1/patch/:id` -- update patch job
- [ ] `POST /api/v1/patch/:id/cancel` -- cancel patch job
- [ ] `POST /api/v1/patch/:id/retry` -- retry failed patch job
- [ ] `POST /api/v1/patch/:id/rollback` -- rollback patch job
- [ ] `GET /api/v1/patch/available` -- list available patches
- [ ] `GET /api/v1/patch/compliance` -- patch compliance statistics
- [ ] `GET /api/v1/patch/windows` -- maintenance windows

### 5.6 Policy Endpoints

- [x] `GET /api/v1/policies` -- list policies (paginated)
- [x] `POST /api/v1/policies` -- create policy
- [x] `POST /api/v1/policies/simulate` -- simulate policy
- [x] `POST /api/v1/policies/resolve-conflict` -- resolve policy conflict
- [x] `GET /api/v1/policies/violations` -- list policy violations (paginated, filtered)
- [ ] `GET /api/v1/policies/:id` -- get policy detail
- [ ] `PATCH /api/v1/policies/:id` -- update policy
- [ ] `DELETE /api/v1/policies/:id` -- delete policy
- [ ] `POST /api/v1/policies/:id/enable` -- enable policy
- [ ] `POST /api/v1/policies/:id/disable` -- disable policy
- [ ] `GET /api/v1/policies/:id/compliance` -- policy compliance stats
- [ ] `GET /api/v1/policies/:id/history` -- policy version history

### 5.7 Audit Log Endpoints

- [x] `GET /api/v1/audit` -- list audit logs (paginated, filtered by action)
- [x] `GET /api/v1/audit/:id` -- get audit log detail
- [ ] `GET /api/v1/audit/export` -- export audit logs
- [ ] `GET /api/v1/audit/stats` -- audit log statistics
- [ ] `POST /api/v1/audit/search` -- advanced audit log search

### 5.8 Integration Endpoints

- [x] `POST /api/v1/integrations/gate/device-access-evaluate` -- Gate access evaluation
- [x] `POST /api/v1/integrations/atlas/remediation` -- Atlas remediation creation
- [x] `POST /api/v1/integrations/capital-hub/device-sync` -- Capital Hub device sync
- [ ] `GET /api/v1/integrations` -- list configured integrations
- [ ] `POST /api/v1/integrations/siem/configure` -- configure SIEM forwarding
- [ ] `POST /api/v1/integrations/ticketing/configure` -- configure ticketing
- [ ] `POST /api/v1/integrations/notifications/configure` -- configure notification channels
- [ ] `GET /api/v1/integrations/webhooks` -- list webhooks
- [ ] `POST /api/v1/integrations/webhooks` -- create webhook
- [ ] `DELETE /api/v1/integrations/webhooks/:id` -- delete webhook
- [ ] `GET /api/v1/integrations/api-keys` -- list API keys
- [ ] `POST /api/v1/integrations/api-keys` -- create API key
- [ ] `DELETE /api/v1/integrations/api-keys/:id` -- revoke API key

### 5.9 UI Preferences Endpoints

- [x] `GET /api/v1/ui/preferences` -- fetch user UI preferences
- [x] `PUT /api/v1/ui/preferences` -- update user UI preferences
- [ ] `DELETE /api/v1/ui/preferences` -- reset to defaults

### 5.10 Additional API Endpoints Needed

- [ ] `GET /api/v1/health` -- API health check
- [ ] `GET /api/v1/version` -- API version info
- [ ] `GET /api/v1/agents/status` -- agent fleet status summary
- [ ] `POST /api/v1/agents/enroll` -- agent enrollment
- [ ] `GET /api/v1/reports` -- list available reports
- [ ] `POST /api/v1/reports` -- generate report
- [ ] `GET /api/v1/alerts` -- list alerts
- [ ] `POST /api/v1/alerts/rules` -- create alert rule
- [ ] `GET /api/v1/threats` -- list detected threats
- [ ] `POST /api/v1/incidents` -- create incident
- [ ] `GET /api/v1/incidents` -- list incidents
- [ ] `GET /api/v1/dashboard/widgets` -- dashboard widget data

---

## 6. State Management

### 6.1 Current State Approach

- [x] Local `useState` per page component
- [x] Zustand dependency installed (v5.0.11)
- [x] Custom hooks for persisted preferences (`usePersistedOverviewPreset`, `usePersistedTableDensity`)
- [x] localStorage + server sync for UI preferences
- [x] Module-level caching for remote preferences (`cachedPreferences`)
- [x] Lazy bootstrap promise for server preferences
- [ ] Extract device list state into Zustand store
- [ ] Extract vulnerability list state into Zustand store
- [ ] Extract patch job state into Zustand store
- [ ] Extract policy state into Zustand store
- [ ] Extract compliance state into Zustand store
- [ ] Extract audit log state into Zustand store
- [ ] Extract integration state into Zustand store
- [ ] Create auth store (token, tenant, roles, user)
- [ ] Create WebSocket connection store (state, reconnect, events)
- [ ] Create notification/toast store

### 6.2 Server State Caching

- [ ] Implement React Query or SWR for server state
- [ ] Configure stale time per endpoint (devices: 30s, vulnerabilities: 60s)
- [ ] Configure cache time per endpoint
- [ ] Implement optimistic updates for remote commands
- [ ] Implement query invalidation on mutations
- [ ] Implement prefetching for navigated-to pages
- [ ] Implement infinite scroll queries for long lists
- [ ] Background refetching on window focus
- [ ] Retry configuration per query type
- [ ] Deduplication of concurrent identical requests

### 6.3 Form State

- [ ] Implement react-hook-form for Patches creation form
- [ ] Implement react-hook-form for Policies creation form
- [ ] Implement react-hook-form for Policy simulation form
- [ ] Implement react-hook-form for Conflict resolution form
- [ ] Implement react-hook-form for WipeDevice wizard
- [ ] Implement react-hook-form for Integration forms
- [ ] Add Zod validation schemas for all forms
- [ ] Add inline field-level validation errors
- [ ] Add form dirty state tracking
- [ ] Add unsaved changes warning on navigation

### 6.4 URL State

- [ ] Sync active tab/filter state with URL query parameters
- [ ] Sync search queries with URL
- [ ] Sync pagination with URL parameters
- [ ] Sync sort order with URL parameters
- [ ] Deep linking to specific endpoint detail
- [ ] Deep linking to specific vulnerability
- [ ] Deep linking to specific patch job
- [ ] Deep linking to specific audit log entry
- [ ] Browser back/forward navigation for filter changes

---

## 7. Performance

### 7.1 Code Splitting & Lazy Loading

- [x] Route-based lazy loading for all 9 pages
- [x] Suspense boundary with loading fallback
- [ ] Lazy load chart/visualization components
- [ ] Lazy load modal/drawer components
- [ ] Lazy load PDF generation library
- [ ] Analyze bundle size with rollup-plugin-visualizer
- [ ] Set bundle size budget (< 200KB initial JS)
- [ ] Tree-shake unused Lucide icons (import only used icons)
- [ ] Verify dead code elimination in production build

### 7.2 Rendering Performance

- [ ] Memoize expensive list rendering with `React.memo()`
- [ ] Memoize callback props with `useCallback()`
- [ ] Memoize computed values with `useMemo()`
- [x] `useMemo` for filteredDevices in Endpoints
- [x] `useMemo` for selectedDevice in Endpoints
- [x] `useMemo` for latestTelemetry in Endpoints
- [x] `useMemo` for metricCards in Overview
- [x] `useMemo` for quickActions in Overview
- [x] `useMemo` for totalAffected/totalExploitable in Vulnerabilities
- [ ] Virtual scrolling for endpoint list (1000+ items)
- [ ] Virtual scrolling for vulnerability list
- [ ] Virtual scrolling for audit log list
- [ ] Virtual scrolling for patch job list
- [ ] Debounce search input (300ms)
- [ ] Throttle WebSocket state updates (batch per animation frame)
- [ ] Use `startTransition` for non-urgent state updates
- [ ] Profile with React DevTools Profiler
- [ ] Eliminate unnecessary re-renders

### 7.3 Network Performance

- [ ] API response compression (gzip/brotli)
- [ ] Request deduplication for concurrent fetches
- [ ] Prefetch data for likely next navigation
- [ ] Cache API responses in service worker
- [ ] Implement ETags / conditional requests
- [ ] Paginate large lists server-side (already done for some)
- [ ] Reduce payload size (select only needed fields)
- [ ] WebSocket message batching
- [ ] Implement connection pooling

### 7.4 Asset Performance

- [ ] Optimize production bundle (minification, tree-shaking)
- [ ] Configure Brotli compression for static assets
- [ ] Set proper cache headers for static assets
- [ ] Preload critical CSS
- [ ] Inline critical CSS for above-the-fold content
- [ ] Optimize font loading (font-display: swap)
- [ ] Remove unused CSS (PurgeCSS via Tailwind)
- [ ] Image optimization (SVGs, lazy load images)
- [ ] Service worker for offline-first PWA support

### 7.5 Metrics & Monitoring

- [ ] Core Web Vitals tracking (LCP, FID/INP, CLS)
- [ ] Performance monitoring integration (Sentry Performance)
- [ ] Custom timing marks for page transitions
- [ ] API latency tracking and alerting
- [ ] Bundle size tracking in CI (fail on regression)
- [ ] Lighthouse CI integration (target score 90+)

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Global / Shell

- [ ] All interactive elements have visible focus indicators
- [ ] Focus trap in mobile sidebar when open
- [ ] `aria-label` on mobile sidebar toggle button
- [ ] `aria-label` on mobile sidebar close button
- [ ] `aria-expanded` on mobile sidebar toggle
- [ ] Skip navigation link to main content
- [ ] Semantic HTML structure (`<nav>`, `<main>`, `<header>`, `<aside>`)
- [x] `<main>` tag used for content area
- [x] `<header>` tag used for top bar
- [x] `<aside>` tag used for sidebar
- [x] `<nav>` tag used for sidebar navigation
- [ ] `role="navigation"` with `aria-label` on sidebar nav
- [ ] Page title updates on route change (via `document.title`)
- [ ] Announce route changes to screen readers (live region)
- [ ] Color contrast ratio >= 4.5:1 for all text
- [ ] Color contrast ratio >= 3:1 for large text
- [ ] Color is not the only indicator (add icons/patterns to status badges)

### 8.2 Overview Page

- [ ] Heading hierarchy (h1 for page title, h2 for sections)
- [ ] KPI cards: announce value changes to screen readers
- [ ] Preset selector: accessible label
- [ ] Quick action cards: semantic article elements
- [ ] Fleet snapshot table: proper `<th scope="col">` headers
- [ ] Fleet snapshot table: `aria-sort` on sortable columns
- [ ] Table density control: accessible label
- [ ] Risk score badges: text alternative (not color-only)

### 8.3 Endpoints Page

- [ ] Search input: proper label (visible or `aria-label`)
- [ ] Device list items: `role="listbox"` and `role="option"` or equivalent
- [x] Device list items: `aria-pressed` for selection state
- [ ] Keyboard navigation through device list (arrow keys)
- [ ] Endpoint detail: `aria-live="polite"` for dynamic content
- [ ] Telemetry values: accessible formatting
- [ ] Remote action buttons: descriptive `aria-label`s
- [ ] Command reason input: `<label>` properly associated
- [x] Command reason input: `htmlFor` and `id` set
- [ ] Pagination buttons: `aria-label="Previous page"` / `"Next page"`
- [ ] WS status badge: `aria-live="polite"` for status changes

### 8.4 Vulnerabilities Page

- [ ] Severity filter select: proper label
- [ ] Status filter select: proper label
- [ ] CVE table: proper `<th>` headers with scope
- [ ] Severity badges: include text label (not color-only)
- [ ] Top risk banner: `role="alert"` or `aria-live`
- [ ] Table density control: accessible label
- [ ] Mobile cards: semantic article elements with heading

### 8.5 Patches Page

- [ ] Create deployment form: all inputs properly labeled
- [ ] Scope select: accessible label
- [ ] Version input: accessible label
- [ ] Software name input: accessible label
- [ ] Scheduled time input: accessible label
- [ ] Create button: descriptive text
- [ ] Patch jobs table: proper headers
- [ ] Selected job row: `aria-selected` attribute
- [ ] WS status badge: `aria-live`
- [ ] Status filter select: accessible label

### 8.6 Policies Page

- [ ] Create policy form: all inputs labeled
- [ ] Simulate policy form: all inputs labeled
- [ ] Resolve conflict form: all inputs labeled
- [ ] Policies table: proper headers
- [ ] Simulation result: `aria-live` for dynamic content
- [ ] Conflict result: `aria-live` for dynamic content
- [ ] Error messages: `role="alert"`

### 8.7 Compliance Page

- [ ] KPI values: accessible to screen readers
- [ ] Violations table: proper headers with scope
- [ ] Status filter: accessible label
- [ ] Table density control: accessible label
- [ ] Loading states: `aria-busy="true"` on container

### 8.8 Deployment Logs Page

- [ ] Action filter input: accessible label
- [ ] Audit event list: keyboard navigable
- [x] Audit events: `aria-pressed` for selection
- [ ] Metadata JSON viewer: accessible (code block with label)
- [ ] Detail panel: `aria-live` for content changes

### 8.9 Integrations Page

- [ ] All form inputs: properly labeled
- [ ] Device selectors: accessible labels
- [ ] Result JSON viewer: accessible code block
- [ ] Error messages: `role="alert"`

### 8.10 Wipe Device Wizard

- [ ] Step indicators: `aria-current="step"` for active step
- [ ] Checkboxes: proper `<label>` associations
- [ ] Form inputs: all properly labeled
- [ ] Warning banners: `role="alert"`
- [ ] Success/error messages: `role="alert"` or `aria-live`
- [ ] MFA input: do not use `type="password"` (codes are often shared verbally)
- [ ] Focus management: auto-focus first input in each step
- [ ] Keyboard: Enter to proceed, Escape to go back

### 8.11 Shared Components

- [ ] `LoadingState`: `role="status"` with `aria-live="polite"`
- [ ] `EmptyState`: descriptive message for screen readers
- [ ] `ErrorState`: `role="alert"` with `aria-live="assertive"`
- [ ] `KpiSkeletonGrid`: `aria-busy="true"` and `aria-label="Loading"`
- [ ] `TableSkeleton`: `aria-busy="true"` and `aria-label="Loading"`
- [x] `TableDensityControl`: `aria-label="Table density"` on select

### 8.12 Testing

- [ ] Run axe-core on every page in Playwright tests
- [ ] Run axe-core in dark mode on every page
- [ ] Manual screen reader testing (NVDA or VoiceOver)
- [ ] Keyboard-only navigation testing (all pages)
- [ ] High contrast mode testing
- [ ] Reduced motion testing (`prefers-reduced-motion`)
- [ ] Zoom 200% testing (no content loss)
- [ ] Touch target size >= 44x44px for mobile

---

## 9. Mobile & Responsive

### 9.1 Layout

- [x] Sidebar hidden on mobile (< lg breakpoint)
- [x] Mobile sidebar toggle button in header
- [x] Mobile sidebar overlay with backdrop
- [x] Mobile sidebar close on link click
- [x] Mobile sidebar close on backdrop click
- [x] Content area full width on mobile
- [ ] Bottom navigation bar for mobile (alternative to sidebar)
- [ ] Swipe gesture to open/close sidebar
- [ ] Responsive header: collapse actions on small screens

### 9.2 Overview Page

- [x] KPI cards: 1 col on mobile, 2 col on md, 4 col on xl
- [x] Quick actions: 1 col on mobile, 3 col on md
- [x] Mobile card layout for fleet snapshot
- [x] Desktop table hidden on mobile (`hidden md:block`)
- [ ] Preset selector: full width on mobile
- [ ] Refresh button: full width on mobile

### 9.3 Endpoints Page

- [x] Grid: stacked on mobile, 2-col on lg
- [x] Search input: full width on mobile
- [ ] Detail panel: bottom sheet on mobile instead of side panel
- [ ] Device list items: touch-friendly tap targets
- [ ] Pagination: simplified for mobile

### 9.4 Vulnerabilities Page

- [x] Mobile card layout for CVE list
- [x] Desktop table hidden on mobile
- [x] Filter selects: 2-col grid on mobile
- [ ] Filter selects: full width on very small screens (< 375px)
- [ ] KPI cards: responsive grid

### 9.5 Patches Page

- [x] Mobile card layout for patch jobs
- [x] Desktop table hidden on mobile
- [x] Grid: stacked on mobile, 2-col on lg
- [ ] Create form: full width on mobile
- [ ] Status filter: full width on mobile

### 9.6 Policies Page

- [x] Grid: stacked on mobile, 2-col on lg
- [x] Mobile card layout for policy list
- [ ] Form inputs: full width on mobile
- [ ] Simulation/conflict forms: stacked on mobile

### 9.7 Compliance Page

- [x] KPI cards: responsive grid (1/3 col)
- [x] Mobile card layout for violations
- [x] Desktop table hidden on mobile
- [ ] Filter input: full width on mobile

### 9.8 Deployment Logs Page

- [x] Grid: stacked on mobile, 2-col on lg
- [ ] Event list: touch-friendly items
- [ ] Detail panel: bottom sheet on mobile
- [ ] JSON viewer: horizontal scroll on mobile

### 9.9 Integrations Page

- [x] Grid: 1 col on mobile, 3 col on lg
- [ ] Form cards: full width on mobile
- [ ] Result JSON viewer: horizontal scroll on mobile

### 9.10 Wipe Device Wizard

- [x] Step buttons: responsive grid (3 col on sm)
- [x] Form inputs: full width
- [ ] Wizard: full screen on mobile
- [ ] Step navigation: swipe gestures

### 9.11 Touch & Interaction

- [ ] All buttons: minimum 44x44px touch target
- [ ] All interactive list items: minimum 44px height
- [ ] No hover-only interactions (all hover states have tap equivalents)
- [ ] Pull-to-refresh for data refresh
- [ ] Haptic feedback for destructive actions (native mobile)
- [ ] Landscape orientation support

---

## 10. Internationalization

### 10.1 Framework Setup

- [ ] Install and configure `i18next` + `react-i18next`
- [ ] Create `locales/` directory structure
- [ ] Create English (en) translation file
- [ ] Configure language detection (browser, localStorage, URL)
- [ ] Add language switcher UI component
- [ ] Configure fallback language (English)
- [ ] Lazy load locale files per language

### 10.2 String Extraction

- [ ] Extract all hardcoded strings from Overview page
- [ ] Extract all hardcoded strings from Endpoints page
- [ ] Extract all hardcoded strings from Vulnerabilities page
- [ ] Extract all hardcoded strings from Patches page
- [ ] Extract all hardcoded strings from Policies page
- [ ] Extract all hardcoded strings from Compliance page
- [ ] Extract all hardcoded strings from Logs page
- [ ] Extract all hardcoded strings from Integrations page
- [ ] Extract all hardcoded strings from WipeDevice page
- [ ] Extract all hardcoded strings from Layout component
- [ ] Extract all hardcoded strings from StateViews components
- [ ] Extract all hardcoded strings from TableDensityControl
- [ ] Extract all hardcoded strings from App.tsx (offline banner, loading)
- [ ] Extract all error messages from secureApi.ts

### 10.3 Number & Date Formatting

- [ ] Use `Intl.NumberFormat` for all numeric displays
- [ ] Use `Intl.DateTimeFormat` for all date displays
- [ ] Replace `.toLocaleString()` / `.toLocaleDateString()` with i18n-aware formatters
- [ ] Format percentages with locale-aware number formatting
- [ ] Format CVSS scores with locale-aware decimal handling
- [ ] Handle RTL text direction for RTL languages

### 10.4 Additional Locales

- [ ] Spanish (es) translation file
- [ ] French (fr) translation file
- [ ] German (de) translation file
- [ ] Japanese (ja) translation file
- [ ] Chinese Simplified (zh-CN) translation file
- [ ] Portuguese (pt-BR) translation file
- [ ] Korean (ko) translation file
- [ ] Arabic (ar) translation file (RTL support)

---

## 11. Security (The App Itself)

### 11.1 Authentication & Authorization

- [x] Bearer token required for all API requests
- [x] Token sourced from env var or localStorage (multiple fallback keys)
- [x] JWT claim parsing for roles and tenant ID
- [x] Role-based UI gating (canLock, canWipe)
- [x] Admin-only access for wipe device page
- [x] MFA required for device wipe
- [x] Serial confirmation required for device wipe
- [ ] Token expiry detection and auto-refresh
- [ ] Logout functionality (clear tokens)
- [ ] Session timeout (auto-logout after inactivity)
- [ ] CSRF protection (if using cookies)
- [ ] Prevent token leakage in URL parameters
- [ ] Clear tokens from memory on logout
- [ ] Secure token storage (consider HttpOnly cookies vs localStorage)

### 11.2 Input Validation & Sanitization

- [ ] Validate all form inputs client-side before submission
- [ ] Sanitize user input before display (prevent XSS)
- [ ] Validate email formats where applicable
- [ ] Validate numeric inputs (min/max/step)
- [ ] Validate date inputs (future dates for scheduling)
- [ ] Validate JSON input in metadata fields
- [ ] Prevent SQL injection in search fields (server-side, but also validate client)
- [ ] Validate file uploads (if added later)
- [ ] Content Security Policy (CSP) headers configured
- [ ] Subresource Integrity (SRI) for CDN assets

### 11.3 Data Protection

- [ ] Sensitive data (tokens, MFA codes) not logged to console
- [ ] Sensitive data not persisted to localStorage unnecessarily
- [ ] API responses with PII handled appropriately
- [ ] No sensitive data in URL query parameters
- [ ] Clipboard access (copy to clipboard) requires user action
- [ ] Metadata JSON viewer: sanitize before rendering
- [ ] Error messages: don't leak internal server details

### 11.4 Network Security

- [ ] All API calls over HTTPS in production
- [ ] WebSocket over WSS in production
- [x] CORS allowed origins configured in env
- [ ] API rate limiting awareness in UI
- [ ] Certificate pinning for agent communication
- [x] mTLS configuration for agent certificates (env vars present)
- [ ] No mixed content (HTTP resources on HTTPS page)

### 11.5 Dependency Security

- [ ] Regular `npm audit` (zero critical/high vulnerabilities)
- [ ] Dependabot or Renovate configured for automated updates
- [ ] Lock file committed and up to date
- [x] `package-lock.json` exists
- [ ] No deprecated dependencies
- [ ] Verify integrity of `@orbit-ui/react` local dependency
- [ ] Supply chain security (verify package checksums)

---

## 12. Testing

### 12.1 Unit Tests (Per Feature)

#### Overview Page

- [ ] `getRiskTone()` returns correct class for score >= 80
- [ ] `getRiskTone()` returns correct class for score >= 60
- [ ] `getRiskTone()` returns correct class for score < 60
- [ ] SecOps preset metric cards computed correctly
- [ ] IT Ops preset metric cards computed correctly
- [ ] Compliance preset metric cards computed correctly
- [ ] Quick actions change by preset
- [ ] Non-compliant count calculation from percentage
- [ ] High-risk device count filter (>= 80)
- [ ] Encrypted device count calculation
- [ ] Firewall enabled count calculation
- [ ] Seen within 24h calculation
- [ ] Snapshot limited to first 8 devices

#### Endpoints Page

- [ ] `riskClass()` returns correct class for each threshold
- [ ] `socketBadgeClass()` returns correct class per state
- [ ] Device search filter by hostname
- [ ] Device search filter by serial number
- [ ] Device search filter by OS type
- [ ] Device search case-insensitive
- [ ] Latest telemetry sorting (most recent first)
- [ ] Filtered devices empty when no match
- [ ] Role detection: canLock for admin
- [ ] Role detection: canLock for soc_analyst
- [ ] Role detection: canWipe for admin only
- [ ] Role detection: read-only for other roles
- [ ] Pagination: totalPages calculation

#### Vulnerabilities Page

- [ ] `severityTone()` returns correct class for critical
- [ ] `severityTone()` returns correct class for high
- [ ] `severityTone()` returns correct class for medium
- [ ] `severityTone()` returns correct class for low
- [ ] Total affected endpoints aggregation
- [ ] Total exploitable findings aggregation
- [ ] Top risk vulnerability sorting (highest max_risk_score)

#### Patches Page

- [ ] `socketBadgeClass()` helper
- [ ] Patch job creation payload construction
- [ ] Status filter application
- [ ] Selected job preservation on list refresh
- [ ] Schedule time validation

#### Policies Page

- [ ] Policy creation payload construction
- [ ] Simulation payload construction with config
- [ ] Conflict resolution: preferred policy ID validation (positive number)
- [ ] Conflict resolution: superseded IDs parsing (comma-separated)
- [ ] Form reset after successful creation

#### Compliance Page

- [ ] Non-compliant count calculation from summary
- [ ] Status filter application
- [ ] Loading/error state handling

#### Logs Page

- [ ] Action filter application
- [ ] Selected log preservation on filter change
- [ ] Detail hydration on selection change

#### Integrations Page

- [ ] Device options mapping from device list
- [ ] Gate evaluation payload with optional threshold
- [ ] Atlas remediation payload construction
- [ ] Capital Hub sync payload construction

#### WipeDevice Page

- [ ] Step 1: all checkboxes required validation
- [ ] Step 2: reason minimum 8 chars validation
- [ ] Step 2: scheduled mode requires scheduledAt
- [ ] Step 3: serial confirmation match validation
- [ ] Step 3: MFA code minimum 6 chars validation
- [ ] Wipe payload construction (reason summary concatenation)
- [ ] Admin role check

#### secureApi.ts

- [ ] `getSecureAuthContext()` reads from env vars
- [ ] `getSecureAuthContext()` reads from localStorage fallbacks
- [ ] `getSecureAuthContext()` decodes JWT claims
- [ ] `getSecureAuthContext()` extracts tenant from multiple sources
- [ ] `getSecureAuthContext()` extracts roles from claims and user objects
- [ ] `getPatchWebSocketUrl()` generates correct WS URL
- [ ] `getPatchWebSocketUrl()` uses wss for https
- [ ] `toQueryString()` filters null/undefined/empty values
- [ ] `parseError()` extracts detail string
- [ ] `parseError()` extracts error string
- [ ] `parseError()` falls back to status code
- [ ] `secureRequest()` throws on missing token
- [ ] `secureRequest()` throws on missing tenant
- [ ] `secureRequest()` sets correct headers
- [ ] `secureRequest()` sends JSON body for POST/PUT

#### uiPrefs.ts

- [ ] `normalizePreset()` returns valid preset for valid input
- [ ] `normalizePreset()` defaults to 'secops' for invalid input
- [ ] `normalizeDensity()` returns valid density for valid input
- [ ] `normalizeDensity()` defaults to 'comfortable' for invalid input
- [ ] localStorage read/write error handling
- [ ] Remote preference hydration
- [ ] Remote preference sync on change
- [ ] Deduplication of sync (lastSyncedRef)

### 12.2 Integration Tests

- [ ] Overview page renders with mocked API data
- [ ] Endpoints page loads device list from API
- [ ] Endpoints page shows detail on device click
- [ ] Vulnerabilities page filters by severity
- [ ] Vulnerabilities page filters by status
- [ ] Patches page creates a new patch job
- [ ] Patches page shows job detail on click
- [ ] Policies page creates a new policy
- [ ] Policies page runs simulation
- [ ] Policies page resolves conflict
- [ ] Compliance page loads summary and violations
- [ ] Logs page loads and filters audit events
- [ ] Integrations page runs Gate evaluation
- [ ] Integrations page creates Atlas remediation
- [ ] Integrations page syncs Capital Hub
- [ ] WipeDevice wizard completes all 3 steps
- [ ] WebSocket connection lifecycle (connect, message, close, reconnect)
- [ ] Offline banner appears when navigator.onLine is false
- [ ] ThemeToggle switches theme correctly
- [ ] Route navigation between all pages
- [ ] 404/unknown routes redirect to overview

### 12.3 E2E Tests (Playwright)

- [x] Playwright configured with `playwright.config.ts`
- [x] Test directory set to `./e2e`
- [x] Chromium project configured
- [x] Web server command for preview mode
- [x] CI retries (2 retries in CI)
- [x] Trace on first retry
- [ ] E2E: Navigate to Overview and verify KPI cards render
- [ ] E2E: Switch persona preset (SecOps -> IT Ops -> Compliance)
- [ ] E2E: Navigate to Endpoints and verify device list
- [ ] E2E: Search for device by hostname
- [ ] E2E: Click device and verify detail panel
- [ ] E2E: Navigate to Vulnerabilities and verify CVE table
- [ ] E2E: Filter vulnerabilities by severity
- [ ] E2E: Filter vulnerabilities by status
- [ ] E2E: Navigate to Patches and create a patch job
- [ ] E2E: Verify created patch appears in list
- [ ] E2E: Navigate to Policies and create a policy
- [ ] E2E: Run policy simulation
- [ ] E2E: Navigate to Compliance and verify summary cards
- [ ] E2E: Navigate to Logs and verify audit events
- [ ] E2E: Filter logs by action
- [ ] E2E: Click log and verify detail panel
- [ ] E2E: Navigate to Integrations and run Gate evaluation
- [ ] E2E: Device wipe wizard: complete step 1 prerequisites
- [ ] E2E: Device wipe wizard: configure step 2 options
- [ ] E2E: Device wipe wizard: authorize step 3 (mock MFA)
- [ ] E2E: Verify sidebar navigation highlights active route
- [ ] E2E: Verify mobile sidebar toggle
- [ ] E2E: Verify theme toggle (light -> dark)
- [ ] E2E: Verify table density control persistence
- [ ] E2E: Verify offline banner appears when offline
- [ ] E2E: Add Firefox project
- [ ] E2E: Add Safari/WebKit project
- [ ] E2E: Add mobile viewport project (iPhone 14)
- [ ] E2E: Add tablet viewport project (iPad)
- [ ] E2E: Screenshot comparison tests for each page
- [ ] E2E: Dark mode screenshot comparisons

### 12.4 Visual Regression Tests

- [ ] Visual snapshot: Overview page (light mode)
- [ ] Visual snapshot: Overview page (dark mode)
- [ ] Visual snapshot: Endpoints page (light mode)
- [ ] Visual snapshot: Endpoints page (dark mode)
- [ ] Visual snapshot: Vulnerabilities page (light mode)
- [ ] Visual snapshot: Vulnerabilities page (dark mode)
- [ ] Visual snapshot: Patches page (light mode)
- [ ] Visual snapshot: Patches page (dark mode)
- [ ] Visual snapshot: Policies page (light mode)
- [ ] Visual snapshot: Policies page (dark mode)
- [ ] Visual snapshot: Compliance page (light mode)
- [ ] Visual snapshot: Compliance page (dark mode)
- [ ] Visual snapshot: Logs page (light mode)
- [ ] Visual snapshot: Logs page (dark mode)
- [ ] Visual snapshot: Integrations page (light mode)
- [ ] Visual snapshot: Integrations page (dark mode)
- [ ] Visual snapshot: WipeDevice wizard step 1
- [ ] Visual snapshot: WipeDevice wizard step 2
- [ ] Visual snapshot: WipeDevice wizard step 3
- [ ] Visual snapshot: Mobile viewport all pages
- [ ] Visual snapshot: Empty states all pages
- [ ] Visual snapshot: Error states all pages
- [ ] Visual snapshot: Loading/skeleton states all pages

### 12.5 Component Tests (Storybook)

- [ ] Storybook configured for Secure app
- [ ] Story: LoadingState component
- [ ] Story: EmptyState component
- [ ] Story: ErrorState component
- [ ] Story: KpiSkeletonGrid component
- [ ] Story: TableSkeleton component
- [ ] Story: TableDensityControl component
- [ ] Story: ModuleShell component
- [ ] Story: Layout with mock content
- [ ] Story: Risk badge variants (high/medium/low)
- [ ] Story: Severity badge variants (critical/high/medium/low)
- [ ] Story: Socket state badge variants
- [ ] Story: WipeDevice step indicators

---

## 13. Documentation

### 13.1 Code Documentation

- [ ] JSDoc comments on all exported functions in secureApi.ts
- [ ] JSDoc comments on all exported types/interfaces
- [ ] JSDoc comments on all custom hooks (uiPrefs.ts)
- [ ] JSDoc comments on all shared components
- [ ] JSDoc comments on all page components
- [ ] Inline comments for complex business logic
- [ ] README for frontend directory (setup, development, architecture)
- [ ] README for node-extension directory

### 13.2 API Documentation

- [ ] OpenAPI/Swagger spec for all backend endpoints
- [ ] API endpoint documentation with request/response examples
- [ ] WebSocket protocol documentation (event types, payloads)
- [ ] Authentication flow documentation
- [ ] Error code reference documentation
- [ ] Rate limiting documentation

### 13.3 Architecture Documentation

- [ ] Architecture decision records (ADRs)
- [ ] Data flow diagram (frontend -> API -> DB)
- [ ] Component hierarchy diagram
- [ ] State management documentation
- [ ] WebSocket event flow diagram
- [ ] Multi-tenant architecture documentation
- [ ] Agent communication protocol documentation
- [ ] Deployment architecture diagram

### 13.4 User Documentation

- [ ] User guide: Overview dashboard usage
- [ ] User guide: Endpoint management
- [ ] User guide: Vulnerability management
- [ ] User guide: Patch management
- [ ] User guide: Policy management
- [ ] User guide: Compliance tracking
- [ ] User guide: Audit log usage
- [ ] User guide: Integration configuration
- [ ] User guide: Device wipe procedure
- [ ] Admin guide: Role and permission management
- [ ] Admin guide: Agent deployment
- [ ] Admin guide: Integration setup

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline

- [ ] GitHub Actions workflow for CI
- [ ] Step: Install dependencies (`npm ci`)
- [ ] Step: TypeScript type check (`tsc --noEmit`)
- [ ] Step: ESLint lint check
- [ ] Step: Prettier format check
- [ ] Step: Unit tests with coverage
- [ ] Step: Build production bundle
- [ ] Step: Bundle size check (fail on regression)
- [ ] Step: Playwright E2E tests
- [ ] Step: Accessibility audit (axe-core)
- [ ] Step: Visual regression tests
- [ ] Step: Security audit (`npm audit`)
- [ ] Step: Docker image build test
- [ ] Step: Upload test reports as artifacts
- [ ] Branch protection: require CI pass before merge
- [ ] Branch protection: require PR review

### 14.2 CD Pipeline

- [ ] Automated deployment to staging on merge to develop
- [ ] Automated deployment to production on merge to main
- [ ] Blue-green deployment strategy
- [ ] Canary deployment support
- [ ] Rollback automation on health check failure
- [ ] Environment-specific configuration (staging vs production)
- [ ] Database migration automation (Alembic)
- [ ] Static asset CDN deployment
- [ ] Cache invalidation on deploy
- [ ] Deployment notification (Slack, email)

### 14.3 Infrastructure

- [ ] Production Dockerfile optimized (multi-stage, minimal layers)
- [ ] Production Docker Compose or Kubernetes manifests
- [ ] TLS/SSL certificate management
- [ ] Load balancer configuration
- [ ] Auto-scaling configuration
- [ ] Database backup automation
- [ ] Redis backup/persistence configuration
- [ ] Log aggregation (ELK/Loki/CloudWatch)
- [ ] Monitoring dashboards (Grafana/Datadog)
- [ ] Alerting for service health (PagerDuty/OpsGenie)
- [ ] Disaster recovery plan
- [ ] Uptime monitoring (external health checks)

### 14.4 Environment Management

- [ ] Development environment documentation
- [ ] Staging environment matching production config
- [ ] Production environment hardened (no debug, no source maps)
- [ ] Secrets management (Vault/AWS Secrets Manager)
- [ ] Environment variable injection at runtime (not baked into image)
- [ ] Feature flags for gradual rollout

---

## 15. Backend

### 15.1 Python/FastAPI Backend (services/secure-service)

#### Core API

- [ ] FastAPI application entry point (`app/main.py`)
- [ ] Health check endpoint (`/healthz`)
- [ ] CORS middleware configured
- [ ] JWT/JWKS authentication middleware
- [ ] Tenant isolation middleware
- [ ] Request logging middleware
- [ ] Error handling middleware (structured error responses)
- [ ] API versioning (`/api/v1/`)
- [ ] Rate limiting middleware
- [ ] Request ID tracking (X-Request-ID header)

#### Device Endpoints

- [ ] `GET /api/v1/devices` -- list devices with pagination, filtering, sorting
- [ ] `GET /api/v1/devices/{id}` -- get device detail
- [ ] `POST /api/v1/devices` -- register/enroll device
- [ ] `PATCH /api/v1/devices/{id}` -- update device
- [ ] `DELETE /api/v1/devices/{id}` -- decommission device
- [ ] `GET /api/v1/devices/{id}/telemetry` -- device telemetry
- [ ] `GET /api/v1/devices/{id}/vulnerabilities` -- device vulnerabilities
- [ ] `GET /api/v1/devices/{id}/violations` -- device policy violations
- [ ] `POST /api/v1/devices/{id}/lock` -- lock command
- [ ] `POST /api/v1/devices/{id}/wipe` -- wipe command (MFA verified)
- [ ] `POST /api/v1/devices/{id}/isolate` -- network isolation
- [ ] `POST /api/v1/devices/{id}/scan` -- trigger scan

#### Vulnerability Endpoints

- [ ] `GET /api/v1/vulnerabilities` -- list with filtering
- [ ] `GET /api/v1/vulnerabilities/{id}` -- detail
- [ ] `PATCH /api/v1/vulnerabilities/{id}` -- update status
- [ ] `POST /api/v1/vulnerabilities/{id}/accept-risk` -- accept risk
- [ ] `GET /api/v1/vulnerabilities/stats` -- statistics

#### Patch Endpoints

- [ ] `GET /api/v1/patch` -- list patch jobs
- [ ] `POST /api/v1/patch` -- create patch job
- [ ] `GET /api/v1/patch/{id}` -- patch job detail
- [ ] `POST /api/v1/patch/{id}/cancel` -- cancel job
- [ ] `POST /api/v1/patch/{id}/rollback` -- rollback job
- [ ] `WS /api/v1/ws/patch/{tenant_id}` -- WebSocket for patch events

#### Policy Endpoints

- [ ] `GET /api/v1/policies` -- list policies
- [ ] `POST /api/v1/policies` -- create policy
- [ ] `GET /api/v1/policies/{id}` -- policy detail
- [ ] `PATCH /api/v1/policies/{id}` -- update policy
- [ ] `DELETE /api/v1/policies/{id}` -- delete policy
- [ ] `POST /api/v1/policies/simulate` -- simulate
- [ ] `POST /api/v1/policies/resolve-conflict` -- resolve conflict
- [ ] `GET /api/v1/policies/violations` -- list violations

#### Compliance Endpoints

- [ ] `GET /api/v1/compliance/summary` -- summary stats
- [ ] `GET /api/v1/compliance/frameworks` -- list frameworks
- [ ] `GET /api/v1/compliance/frameworks/{id}/controls` -- framework controls
- [ ] `POST /api/v1/compliance/report` -- generate report

#### Risk & Dashboard Endpoints

- [ ] `GET /api/v1/risk/dashboard` -- risk dashboard data
- [ ] `GET /api/v1/risk/trend` -- risk trend
- [ ] `GET /api/v1/risk/top-cves` -- top CVEs

#### Audit Log Endpoints

- [ ] `GET /api/v1/audit` -- list audit logs
- [ ] `GET /api/v1/audit/{id}` -- audit detail
- [ ] `GET /api/v1/audit/export` -- export logs

#### Integration Endpoints

- [ ] `POST /api/v1/integrations/gate/device-access-evaluate`
- [ ] `POST /api/v1/integrations/atlas/remediation`
- [ ] `POST /api/v1/integrations/capital-hub/device-sync`

#### UI Preference Endpoints

- [ ] `GET /api/v1/ui/preferences` -- get preferences
- [ ] `PUT /api/v1/ui/preferences` -- update preferences

### 15.2 Database Schema

- [ ] `tenants` table (id, name, settings, created_at)
- [ ] `users` table (id, tenant_id, email, roles, created_at)
- [ ] `devices` table (id, tenant_id, hostname, os_type, os_version, serial_number, device_type, enrolled_at, last_seen, compliance_status, risk_score, is_encrypted, firewall_enabled, agent_version, tags, metadata)
- [ ] `device_telemetry` table (id, tenant_id, device_id, cpu_usage, ram_usage, disk_usage, running_services, collected_at)
- [ ] `vulnerabilities` table (id, cve_id, severity, cvss_score, description, published_date, references, remediation)
- [ ] `device_vulnerabilities` table (id, tenant_id, device_id, vulnerability_id, exploit_available, risk_score, patch_available, status, detected_at, remediated_at)
- [ ] `patch_jobs` table (id, tenant_id, target_scope, software_name, version, status, scheduled_at, executed_at, created_by, rollback_job_id)
- [ ] `patch_job_devices` table (id, patch_job_id, device_id, status, started_at, completed_at, error_message)
- [ ] `policies` table (id, tenant_id, name, type, config, severity, status, version, created_at, updated_at)
- [ ] `policy_violations` table (id, tenant_id, device_id, policy_id, status, detected_at, remediated_at)
- [ ] `compliance_frameworks` table (id, name, version, description)
- [ ] `compliance_controls` table (id, framework_id, control_id, title, description, category)
- [ ] `tenant_compliance` table (id, tenant_id, framework_id, control_id, status, evidence, notes, assigned_to, updated_at)
- [ ] `audit_logs` table (id, tenant_id, actor, action, entity_type, entity_id, metadata, timestamp) -- append-only
- [ ] `ui_preferences` table (id, subject, tenant_id, preferences, updated_at)
- [ ] `integration_configs` table (id, tenant_id, type, config, status, created_at)
- [ ] `alerts` table (id, tenant_id, severity, title, description, source, status, created_at, acknowledged_at)
- [ ] `incidents` table (id, tenant_id, severity, title, status, created_at, resolved_at, assigned_to)
- [ ] Database indexes on tenant_id for all tenant-scoped tables
- [ ] Database indexes on frequently filtered columns (status, severity, device_id)
- [ ] Foreign key constraints for referential integrity
- [ ] Alembic migration scripts for all schema changes
- [ ] Seed data scripts for development/testing

### 15.3 Node Extension Backend (node-extension/)

- [x] Express.js application (`secure-service.js`)
- [x] In-memory store per org (endpoints, findings)
- [x] Auth middleware (Gate token verification)
- [x] Org middleware (organization context extraction)
- [x] Tenant context middleware (org + user resolution)
- [x] Event envelope builder for Redis pub/sub
- [x] Health endpoint (`/health`)
- [x] Overview endpoint (`/overview`)
- [x] Endpoints CRUD (`GET /endpoints`, `POST /endpoints`, `GET /endpoints/:id`, `PATCH /endpoints/:id`)
- [x] Endpoint vulnerabilities (`GET /endpoints/:id/vulnerabilities`, `POST /endpoints/:id/vulnerabilities`)
- [x] Vulnerabilities listing with filtering (`GET /vulnerabilities`)
- [x] Vulnerability update (`PATCH /vulnerabilities/:findingId`)
- [x] Scan results ingestion (`POST /scan-results`)
- [x] Redis event publisher
- [x] Noop event publisher fallback
- [x] Input validation for endpoints (hostname, status, criticality)
- [x] Input validation for findings (title, severity, status, CVSS, dates)
- [x] Endpoint summary with finding counts
- [x] Org-isolated data storage
- [ ] Replace in-memory store with database persistence
- [ ] Add patch job endpoints
- [ ] Add policy endpoints
- [ ] Add compliance endpoints
- [ ] Add audit log endpoints
- [ ] Add integration endpoints
- [ ] Add WebSocket endpoint for real-time events
- [ ] Add rate limiting
- [ ] Add request validation with Joi or Zod
- [ ] Add structured logging
- [ ] Add health check with dependency status (Redis, DB)
- [ ] Add graceful shutdown handling
- [ ] Add unit tests for all endpoints
- [ ] Add integration tests with supertest

### 15.4 Background Workers

- [x] Patch dispatcher worker (docker-compose service)
- [x] Patch worker (Celery-based)
- [x] Policy evaluation worker (configurable interval and batch size)
- [x] Vulnerability sync scheduler (configurable sync hours)
- [ ] Agent heartbeat processor
- [ ] Telemetry data aggregator/compressor
- [ ] Compliance scoring engine
- [ ] Risk score calculator
- [ ] Alert rule evaluator
- [ ] Audit log archiver
- [ ] Report generator worker
- [ ] CVE feed sync worker (NVD/OSV)
- [ ] Dead letter queue processor
- [ ] Worker health monitoring
- [ ] Worker retry policies
- [ ] Worker logging and metrics

### 15.5 Agent Communication

- [x] mTLS configuration (agent cert, key, CA cert in env)
- [x] Backend URL for agent communication
- [x] Enrollment signature in env
- [ ] Agent enrollment protocol (register new device)
- [ ] Agent heartbeat protocol (periodic check-in)
- [ ] Agent telemetry collection protocol
- [ ] Agent command dispatch protocol (lock, wipe, scan)
- [ ] Agent command acknowledgement protocol
- [ ] Agent update/upgrade protocol
- [ ] Agent certificate rotation
- [ ] Agent connectivity status tracking
- [ ] Agent version tracking and minimum version enforcement

### 15.6 Telemetry Pipeline

- [x] Redis pub/sub for event distribution
- [x] Event envelope format with metadata (source, event_type, org_id, user_id, timestamp)
- [x] Global channel for cross-org events
- [ ] Event schema validation
- [ ] Event retention policy
- [ ] Event replay capability
- [ ] Time-series telemetry storage (TimescaleDB or InfluxDB)
- [ ] Telemetry aggregation (hourly, daily rollups)
- [ ] Telemetry alerting thresholds
- [ ] Telemetry data export API
- [ ] Event correlation engine
- [ ] Real-time event streaming to frontend via WebSocket/SSE

### 15.7 Security Hardening

- [ ] Database connection encryption (SSL/TLS)
- [ ] Redis connection encryption
- [ ] Secrets management (no plaintext secrets in config)
- [ ] API input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] Output encoding (prevent XSS in API responses)
- [ ] Audit log integrity verification (hash chain)
- [ ] Tenant data isolation verification tests
- [ ] Penetration testing
- [ ] Dependency vulnerability scanning (backend)
- [ ] Container security scanning
- [ ] Network policy enforcement between services

---

## Summary Statistics

| Section | Total Items | Done | Todo | In Progress |
|---------|------------|------|------|-------------|
| 1. Project Setup | ~85 | ~35 | ~50 | 0 |
| 2. Design System | ~175 | ~8 | ~167 | 0 |
| 3. Dark Mode | ~110 | 0 | ~110 | 0 |
| 4. Core Features | ~375 | ~115 | ~260 | 0 |
| 5. API Integration | ~100 | ~25 | ~75 | 0 |
| 6. State Management | ~40 | ~5 | ~35 | 0 |
| 7. Performance | ~50 | ~7 | ~43 | 0 |
| 8. Accessibility | ~80 | ~6 | ~74 | 0 |
| 9. Mobile & Responsive | ~55 | ~25 | ~30 | 0 |
| 10. Internationalization | ~35 | 0 | ~35 | 0 |
| 11. Security | ~35 | ~10 | ~25 | 0 |
| 12. Testing | ~180 | ~7 | ~173 | 0 |
| 13. Documentation | ~40 | 0 | ~40 | 0 |
| 14. Deployment & CI/CD | ~45 | 0 | ~45 | 0 |
| 15. Backend | ~170 | ~30 | ~140 | 0 |
| **TOTAL** | **~1,575** | **~273** | **~1,302** | **0** |

> Estimated completion: ~18%
> Critical path: Design system migration -> Dark mode -> Core features -> Testing -> Deployment
