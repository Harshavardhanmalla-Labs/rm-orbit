# 10 -- Capital Hub (Finance Dashboard) -- Comprehensive Checklist

> **App:** Capital Hub -- Finance Dashboard (Asset Management + Financial Analytics)
> **Stack:** React 19.2.0 | Vite 7.3.1 | React Router v7 | Recharts | Tailwind v3 | @orbit-ui/react
> **Architecture:** SPA with React Router (4 routes: Dashboard, Assets, Transactions, Reports)
> **Ports:** Frontend localhost:45010 | Backend localhost:45013
> **Backend:** Python FastAPI + SQLAlchemy + PostgreSQL (Alembic migrations)
> **Last updated:** 2026-04-06
>
> Legend: `[x]` = done | `[ ]` = todo | `[~]` = in progress | `[-]` = N/A / skipped

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

### 1.1 Frontend Toolchain
- [x] Vite 7.3.1 initialized with React 19 template
- [x] TypeScript configured (`tsconfig.json`)
- [ ] TypeScript strict mode enabled (`"strict": true`)
- [ ] TypeScript `noUncheckedIndexedAccess` enabled
- [ ] TypeScript `exactOptionalPropertyTypes` enabled
- [x] Tailwind CSS v3 installed and configured
- [ ] Tailwind CSS purge paths verified for production builds
- [ ] PostCSS config validated
- [x] React Router v7 installed and configured
- [x] Recharts installed for charting
- [x] ESLint configured
- [ ] ESLint rule: no-unused-vars (error level)
- [ ] ESLint rule: no-explicit-any (error level)
- [ ] ESLint rule: react-hooks/exhaustive-deps (error level)
- [ ] ESLint rule: import/order (auto-sort imports)
- [ ] ESLint rule: no-console (warn in dev, error in prod)
- [x] Prettier configured
- [ ] Prettier + ESLint integration (eslint-config-prettier)
- [ ] Husky pre-commit hook running lint + format
- [ ] lint-staged configured for staged files only

### 1.2 Frontend Dependencies
- [x] `react` 19.2.0 installed
- [x] `react-dom` 19.2.0 installed
- [x] `react-router-dom` v7 installed
- [x] `recharts` installed
- [x] `lucide-react` installed
- [x] `@orbit-ui/react` installed
- [ ] `clsx` installed (used by cn utility)
- [ ] `tailwind-merge` installed (used by cn utility)
- [ ] All dependencies pinned to exact versions
- [ ] `package-lock.json` committed and up to date
- [ ] No unused dependencies (run `depcheck`)
- [ ] No known vulnerabilities (`npm audit`)
- [ ] `date-fns` installed for date formatting
- [ ] `zustand` or `@tanstack/react-query` for state management

### 1.3 Frontend Project Structure
- [x] `src/App.tsx` -- root with Router and ThemeProvider
- [x] `src/main.tsx` -- entry point
- [x] `src/index.css` -- global styles
- [x] `src/App.css` -- app-specific styles
- [x] `src/utils/cn.ts` -- className utility
- [x] `src/services/api.ts` -- API service with typed methods
- [x] `src/components/Layout.tsx` -- layout with sidebar and outlet
- [x] `src/pages/Dashboard.tsx` -- dashboard page
- [x] `src/pages/Assets.tsx` -- assets page
- [x] `src/pages/Transactions.tsx` -- transactions page
- [x] `src/pages/Reports.tsx` -- reports page
- [ ] `src/hooks/` directory created
- [ ] `src/hooks/usePortfolio.ts` -- portfolio data hook
- [ ] `src/hooks/useAssets.ts` -- assets data hook
- [ ] `src/hooks/useTransactions.ts` -- transactions data hook
- [ ] `src/hooks/useReports.ts` -- reports data hook
- [ ] `src/hooks/useDebounce.ts` -- debounce utility hook
- [ ] `src/hooks/useMediaQuery.ts` -- responsive breakpoint hook
- [ ] `src/types/` directory created
- [ ] `src/types/index.ts` -- centralized type definitions (currently in api.ts)
- [ ] `src/constants/` directory created
- [ ] `src/constants/config.ts` -- API URLs, feature flags
- [ ] `src/constants/categories.ts` -- asset categories, statuses
- [ ] `src/store/` directory for state management (if Zustand adopted)

### 1.4 Index HTML & Shell
- [x] Anti-FOUC script in `index.html`
- [x] `orbit-tokens.css` linked in `index.html`
- [x] `orbit-bar.js` loaded (deferred)
- [x] `orbit-ui.css` linked
- [x] `orbit-theme-init.js` loaded
- [ ] `<meta name="description">` set for Capital Hub
- [ ] `<meta name="theme-color">` set (light + dark)
- [ ] Favicon set to Capital Hub icon
- [ ] Apple touch icon configured
- [ ] Open Graph meta tags for link previews
- [ ] CSP meta tag (Content-Security-Policy)
- [ ] `<noscript>` fallback message

### 1.5 Backend Toolchain
- [x] Python FastAPI backend initialized
- [x] SQLAlchemy ORM configured
- [x] Alembic migrations configured
- [x] Initial migration: accounts table
- [x] Hardening migration: indexes and constraints
- [x] Gate auth integration (`gate_auth.py`)
- [x] Routes module (`routes.py`)
- [x] Database module (`database.py`)
- [x] Models module (`models.py`)
- [ ] `.env.example` with all required variables
- [ ] Requirements.txt up to date
- [ ] Python 3.10+ version pinned
- [ ] Virtual environment documented
- [ ] Backend start script (`start-backend.sh`) documented

### 1.6 Node Extension
- [x] Node extension module exists (`node-extension/`)
- [x] Org middleware (`org-middleware.js`)
- [x] Tenant context (`tenant-context.js`)
- [x] Service test (`capitalhub-service.test.js`)
- [ ] Node extension: Socket.IO integration documented
- [ ] Node extension: CORS configured
- [ ] Node extension: error handling middleware

---

## 2. Design System Integration

### 2.1 Token Integration
- [x] `index.css` imports `orbit-tokens.css`
- [x] `ThemeProvider` from `@orbit-ui/react` wraps root in App.tsx
- [x] `ThemeToggle` from `@orbit-ui/react` used in sidebar
- [ ] `tailwind.config.js` uses orbit tailwind preset
- [ ] Remove all remaining hardcoded hex colors from components
- [ ] Replace all `#6366f1` (indigo) with `primary-500`
- [ ] Replace all `#4f46e5` with `primary-600`
- [ ] Replace all `#818cf8` with `primary-400`
- [ ] Replace all `#3b82f6` (blue) with `info-500` or `primary-500`
- [ ] Replace all `#10b981` (emerald) with `success-500`
- [ ] Replace all `#ef4444` (red) with `danger-500`
- [ ] Replace all `#f59e0b` (amber) with `warning-500`
- [ ] Replace all `#8b5cf6` (violet) with `purple-500`
- [ ] Replace all `#06b6d4` (cyan) with `info-400`
- [ ] Replace all `#1e293b` with `content-primary` or `neutral-800`
- [ ] Replace all `#475569` with `content-secondary` or `neutral-600`
- [ ] Replace all `#64748b` with `content-muted` or `neutral-500`
- [ ] Replace all `#94a3b8` with `neutral-400`
- [ ] Replace all `#cbd5e1` with `border-default`
- [ ] Replace all `#e2e8f0` with `border-subtle`
- [ ] Replace all `#f1f5f9` with `surface-muted`
- [ ] Replace all `#f8fafc` with `surface-base`
- [ ] Replace all `#ffffff` / `#fff` backgrounds with `surface-base`
- [ ] Verify all `bg-slate-*` classes replaced with semantic tokens
- [ ] Verify all `text-slate-*` classes replaced with semantic tokens
- [ ] Verify all `border-slate-*` classes replaced with semantic tokens
- [ ] Font family uses `var(--orbit-font-family)` or orbit preset
- [ ] All focus styles use `focus-ring` utility class
- [ ] All scrollbar CSS uses `.scrollbar-thin` plugin

### 2.2 Adopt Sidebar Component
- [ ] Replace custom sidebar in `Layout.tsx` with `<Sidebar>` + `useSidebar` from `@orbit-ui/react`
- [ ] Sidebar: collapsible toggle (expanded/collapsed)
- [ ] Sidebar: section grouping (Navigation, System)
- [ ] Sidebar: active item highlight via route matching
- [ ] Sidebar: Dashboard nav item with icon
- [ ] Sidebar: Assets nav item with icon
- [ ] Sidebar: Transactions nav item with icon
- [ ] Sidebar: Reports nav item with icon
- [ ] Sidebar: Help nav item at bottom
- [ ] Sidebar: Sign out button at bottom
- [ ] Sidebar: Theme toggle at bottom
- [ ] Sidebar: Brand/logo section at top
- [ ] Sidebar: responsive behavior (mobile slide-in, desktop persistent)
- [ ] Sidebar: mobile close button
- [ ] Sidebar: backdrop overlay on mobile
- [ ] Remove custom sidebar CSS from Layout.tsx

### 2.3 Adopt Card Component
- [ ] Adopt `<Card>` from `@orbit-ui/react` for all card layouts
- [ ] Dashboard: Total Asset Value KPI card
- [ ] Dashboard: Depreciated Value KPI card
- [ ] Dashboard: Monthly Burn KPI card
- [ ] Dashboard: Compliance Risk KPI card
- [ ] Dashboard: Asset Value Trend chart container card
- [ ] Dashboard: Category Breakdown card
- [ ] Dashboard: Depreciation by Category card
- [ ] Dashboard: Recent Transactions card
- [ ] Dashboard: Portfolio Summary card
- [ ] Assets: individual asset cards in grid view
- [ ] Assets: asset detail card
- [ ] Assets: asset creation form card
- [ ] Assets: asset edit form card
- [ ] Assets: asset filter panel card
- [ ] Transactions: transaction list card
- [ ] Transactions: transaction detail card
- [ ] Transactions: transaction filter panel card
- [ ] Transactions: transaction summary card
- [ ] Reports: report list card
- [ ] Reports: report detail card
- [ ] Reports: report generation card
- [ ] Reports: portfolio report card
- [ ] Reports: depreciation report card
- [ ] Reports: compliance report card
- [ ] Reports: transactions report card

### 2.4 Adopt Badge Component
- [ ] Adopt `<Badge>` from `@orbit-ui/react`
- [ ] Dashboard: compliance risk badge (Low/Medium/High)
- [ ] Dashboard: asset value change badge (positive/negative)
- [ ] Dashboard: transaction status badges
- [ ] Assets: asset status badges (active, review, disposed, maintenance)
- [ ] Assets: asset category badges (hardware, software, real_estate, vehicle, furniture, other)
- [ ] Transactions: transaction type badges (acquisition, disposal, depreciation, maintenance, insurance)
- [ ] Transactions: transaction status badges (completed, pending, review)
- [ ] Reports: report type badges (portfolio, depreciation, compliance, transactions)
- [ ] Reports: report status badges (ready, generating)
- [ ] Replace all custom badge classes in `api.ts` statusColors with `<Badge>` variants
- [ ] Replace all custom badge classes in `api.ts` transactionTypeColors with `<Badge>` variants

### 2.5 Adopt Button Component
- [ ] Adopt `<Button>` from `@orbit-ui/react` for all action buttons
- [ ] Dashboard: "Add Asset" button uses `<Button variant="primary">`
- [ ] Dashboard: "View All Assets" uses `<Button variant="ghost">`
- [ ] Dashboard: "View All Transactions" uses `<Button variant="ghost">`
- [ ] Dashboard: period selector buttons use `<Button variant="outline">`
- [ ] Dashboard: filter button uses `<Button variant="ghost">`
- [ ] Dashboard: more options button uses `<IconButton>`
- [ ] Assets: "Add Asset" button uses `<Button variant="primary">`
- [ ] Assets: "Edit Asset" button uses `<Button variant="outline">`
- [ ] Assets: "Delete Asset" button uses `<Button variant="danger">`
- [ ] Assets: "Export" button uses `<Button variant="outline">`
- [ ] Assets: filter/sort toggle buttons use `<Button variant="ghost">`
- [ ] Assets: view mode toggle (grid/list) uses `<IconButton>`
- [ ] Transactions: "Add Transaction" button uses `<Button variant="primary">`
- [ ] Transactions: "Export" button uses `<Button variant="outline">`
- [ ] Transactions: filter buttons use `<Button variant="ghost">`
- [ ] Reports: "Generate Report" button uses `<Button variant="primary">`
- [ ] Reports: "Download" button uses `<Button variant="outline">`
- [ ] Reports: "Share" button uses `<Button variant="ghost">`
- [ ] Layout: mobile menu toggle uses `<IconButton>`
- [ ] Layout: sign out button uses `<Button variant="ghost">`
- [ ] All button `loading` states use `<Button loading>` prop
- [ ] All button `disabled` states use `<Button disabled>` prop

### 2.6 Adopt Table Component
- [ ] Adopt `<Table>` from `@orbit-ui/react`
- [ ] Assets: asset list table (sortable by name, category, status, value)
- [ ] Assets: asset list table row selection (checkbox)
- [ ] Assets: asset list table pagination
- [ ] Transactions: transaction list table (sortable by date, type, amount, status)
- [ ] Transactions: transaction list table row selection
- [ ] Transactions: transaction list table pagination
- [ ] Reports: budget vs actuals table
- [ ] Reports: depreciation schedule table
- [ ] Reports: journal entries table
- [ ] Reports: chart of accounts table
- [ ] Dashboard: recent transactions table

### 2.7 Adopt Progress Component
- [ ] Adopt `<Progress>` from `@orbit-ui/react`
- [ ] Dashboard: budget utilization progress bars
- [ ] Dashboard: depreciation progress bars by category
- [ ] Dashboard: compliance score progress
- [ ] Assets: depreciation percentage progress per asset
- [ ] Reports: budget vs actual progress bars by department
- [ ] Reports: budget vs actual progress bars by line item

### 2.8 Adopt Tabs Component
- [ ] Adopt `<Tabs>` from `@orbit-ui/react`
- [ ] Reports: tab switching between Portfolio / Depreciation / Compliance / Transactions
- [ ] Assets: tab switching between All / Hardware / Software / Real Estate / Vehicles / Furniture
- [ ] Dashboard: tab switching between Overview / Analytics / Budget
- [ ] Transactions: tab switching between All / Acquisitions / Disposals / Depreciation / Maintenance

### 2.9 Adopt EmptyState Component
- [ ] Adopt `<EmptyState>` from `@orbit-ui/react`
- [ ] Dashboard: no data available
- [ ] Assets: no assets found
- [ ] Assets: no search results
- [ ] Assets: no assets in selected category
- [ ] Transactions: no transactions found
- [ ] Transactions: no transactions in date range
- [ ] Transactions: no search results
- [ ] Reports: no reports generated
- [ ] Reports: report data unavailable

### 2.10 Adopt Skeleton Component
- [ ] Adopt `<Skeleton>` / `<SkeletonCard>` / `<SkeletonText>` from `@orbit-ui/react`
- [ ] Dashboard: KPI cards skeleton
- [ ] Dashboard: chart skeleton
- [ ] Dashboard: category breakdown skeleton
- [ ] Dashboard: recent transactions skeleton
- [ ] Dashboard: replace "Loading Dashboard..." text with skeleton
- [ ] Assets: asset list skeleton
- [ ] Assets: asset grid skeleton
- [ ] Assets: asset detail skeleton
- [ ] Transactions: transaction list skeleton
- [ ] Transactions: transaction summary skeleton
- [ ] Reports: report list skeleton
- [ ] Reports: report content skeleton

### 2.11 Adopt Modal Component
- [ ] Adopt `<Modal>` from `@orbit-ui/react`
- [ ] Assets: create asset modal
- [ ] Assets: edit asset modal
- [ ] Assets: delete asset confirmation modal
- [ ] Assets: asset detail modal (or use drawer)
- [ ] Transactions: create transaction modal
- [ ] Transactions: transaction detail modal
- [ ] Reports: generate report modal (type + period selection)
- [ ] Reports: share report modal
- [ ] Settings: confirmation modals

### 2.12 Adopt Tooltip Component
- [ ] Adopt `<Tooltip>` from `@orbit-ui/react`
- [ ] Dashboard: KPI card info tooltips
- [ ] Dashboard: chart data point tooltips (override Recharts defaults)
- [ ] Dashboard: category breakdown tooltips
- [ ] Dashboard: depreciation bar tooltips
- [ ] Assets: asset status tooltip
- [ ] Assets: depreciation percentage tooltip
- [ ] Transactions: transaction amount tooltip (full precision)
- [ ] Sidebar: collapsed nav item tooltips
- [ ] Reports: report generation info tooltip

### 2.13 Adopt Input Component
- [ ] Adopt `<Input>` from `@orbit-ui/react`
- [ ] Assets: search input field
- [ ] Assets: asset name input (create/edit)
- [ ] Assets: serial number input
- [ ] Assets: location input
- [ ] Assets: notes input
- [ ] Assets: purchase value input
- [ ] Assets: current value input
- [ ] Transactions: search input
- [ ] Transactions: amount input
- [ ] Transactions: description input
- [ ] Reports: period input
- [ ] Reports: custom date range inputs

### 2.14 Adopt Select Component
- [ ] Adopt `<Select>` from `@orbit-ui/react`
- [ ] Assets: category filter select
- [ ] Assets: status filter select
- [ ] Assets: asset category select (create/edit)
- [ ] Assets: asset status select (create/edit)
- [ ] Transactions: type filter select
- [ ] Transactions: status filter select
- [ ] Reports: report type select
- [ ] Reports: period select (MTD, QTD, YTD, custom)
- [ ] Dashboard: period selector (MTD, QTD, YTD, custom)

### 2.15 Adopt Spinner / PageLoader Component
- [ ] Replace custom PageLoader in App.tsx with `<Spinner>` or `<PageLoader>` from `@orbit-ui/react`
- [ ] Dashboard: data loading spinner
- [ ] Assets: list loading spinner
- [ ] Transactions: list loading spinner
- [ ] Reports: report generation spinner
- [ ] Reports: report loading spinner

### 2.16 Adopt Dropdown Component
- [ ] Adopt `<Dropdown>` from `@orbit-ui/react`
- [ ] Dashboard: more options dropdown per section
- [ ] Assets: asset action dropdown (edit, delete, archive)
- [ ] Transactions: transaction action dropdown
- [ ] Reports: report action dropdown (download, share, delete)
- [ ] Header: user profile dropdown

### 2.17 Adopt DatePicker Component
- [ ] Adopt `<DatePicker>` from `@orbit-ui/react`
- [ ] Assets: purchase date picker (create/edit)
- [ ] Transactions: date range picker (filter)
- [ ] Transactions: transaction date picker (create)
- [ ] Reports: report period date picker
- [ ] Dashboard: custom period date range picker

### 2.18 Adopt Pagination Component
- [ ] Adopt `<Pagination>` from `@orbit-ui/react`
- [ ] Assets: paginated asset list
- [ ] Transactions: paginated transaction list
- [ ] Reports: paginated report list

### 2.19 Adopt Breadcrumb Component
- [ ] Adopt `<Breadcrumb>` from `@orbit-ui/react`
- [ ] Assets: Dashboard > Assets
- [ ] Assets: Dashboard > Assets > [Asset Name]
- [ ] Transactions: Dashboard > Transactions
- [ ] Reports: Dashboard > Reports
- [ ] Reports: Dashboard > Reports > [Report Name]

### 2.20 Adopt Alert Component
- [ ] Adopt `<Alert>` from `@orbit-ui/react`
- [ ] Dashboard: budget overrun alert
- [ ] Dashboard: compliance risk alert
- [ ] Assets: asset requiring maintenance alert
- [ ] Assets: asset near full depreciation alert
- [ ] Transactions: pending approval alert
- [ ] Reports: report generation failed alert
- [ ] App: offline mode alert (replace custom banner)

### 2.21 Adopt Drawer / Sheet Component
- [ ] Adopt `<Drawer>` from `@orbit-ui/react`
- [ ] Assets: asset detail side drawer
- [ ] Transactions: transaction detail side drawer
- [ ] Reports: report preview side drawer
- [ ] Dashboard: detailed KPI breakdown drawer

### 2.22 Adopt Tag / Chip Component
- [ ] Adopt `<Tag>` from `@orbit-ui/react`
- [ ] Assets: asset tags display
- [ ] Assets: asset tag input/management (create/edit)
- [ ] Transactions: category tags
- [ ] Reports: report filter tags

### 2.23 Adopt Switch Component
- [ ] Adopt `<Switch>` from `@orbit-ui/react`
- [ ] Settings: notification toggles
- [ ] Settings: auto-depreciation toggle
- [ ] Settings: compliance alerts toggle
- [ ] Assets: active/inactive toggle per asset

### 2.24 Adopt Checkbox Component
- [ ] Adopt `<Checkbox>` from `@orbit-ui/react`
- [ ] Assets: bulk selection checkboxes
- [ ] Transactions: bulk selection checkboxes
- [ ] Reports: report content section checkboxes
- [ ] Settings: preference checkboxes

### 2.25 Adopt NumberInput Component
- [ ] Adopt `<NumberInput>` from `@orbit-ui/react`
- [ ] Assets: purchase value input
- [ ] Assets: current value input
- [ ] Assets: depreciation percentage input
- [ ] Transactions: amount input
- [ ] Reports: budget amount inputs

### 2.26 Adopt Divider Component
- [ ] Adopt `<Divider>` from `@orbit-ui/react`
- [ ] Layout: sidebar section dividers
- [ ] Dashboard: section dividers
- [ ] Assets: detail section dividers
- [ ] Reports: section dividers

### 2.27 Adopt Accordion Component
- [ ] Adopt `<Accordion>` from `@orbit-ui/react`
- [ ] Assets: asset detail expandable sections
- [ ] Reports: report sections
- [ ] Settings: collapsible settings groups

### 2.28 Adopt CommandPalette Component
- [ ] Adopt `<CommandPalette>` from `@orbit-ui/react`
- [ ] Global: Cmd+K / Ctrl+K opens command palette
- [ ] Command: navigate to Dashboard
- [ ] Command: navigate to Assets
- [ ] Command: navigate to Transactions
- [ ] Command: navigate to Reports
- [ ] Command: create new asset
- [ ] Command: search assets
- [ ] Command: search transactions
- [ ] Command: toggle theme
- [ ] Command: generate report

### 2.29 Adopt Popover Component
- [ ] Adopt `<Popover>` from `@orbit-ui/react`
- [ ] Dashboard: KPI detail popovers
- [ ] Dashboard: chart interaction popovers
- [ ] Assets: quick asset info popover
- [ ] Transactions: quick transaction info popover

### 2.30 Adopt Steps / Stepper Component
- [ ] Adopt `<Steps>` from `@orbit-ui/react`
- [ ] Assets: multi-step asset creation wizard
- [ ] Reports: multi-step report generation wizard
- [ ] Transactions: transaction approval workflow steps

### 2.31 Adopt FileUpload Component
- [ ] Adopt `<FileUpload>` from `@orbit-ui/react`
- [ ] Assets: import CSV file upload
- [ ] Transactions: import CSV file upload
- [ ] Reports: upload supporting documents
- [ ] Expenses: receipt image upload

### 2.32 Adopt Radio / RadioGroup Component
- [ ] Adopt `<Radio>` / `<RadioGroup>` from `@orbit-ui/react`
- [ ] Reports: report type selection (radio group)
- [ ] Reports: report format selection (PDF/CSV/Excel)
- [ ] Assets: depreciation method selection
- [ ] Settings: default view selection
- [ ] Settings: currency display preference

### 2.33 Adopt Textarea Component
- [ ] Adopt `<Textarea>` from `@orbit-ui/react`
- [ ] Assets: notes field (create/edit)
- [ ] Transactions: description field (create/edit)
- [ ] Reports: custom notes field
- [ ] Transactions: metadata notes

### 2.34 Replace All Hardcoded Inline Styles
- [ ] Dashboard: remove all inline `style={{}}` attributes
- [ ] Assets: remove all inline styles
- [ ] Transactions: remove all inline styles
- [ ] Reports: remove all inline styles
- [ ] Layout: remove all inline styles
- [ ] Replace inline color values with Tailwind classes
- [ ] Replace inline spacing with Tailwind classes
- [ ] Replace inline font sizes with Tailwind classes

### 2.35 Icon Consistency
- [ ] All icons use Lucide React exclusively (no mixing icon sets)
- [ ] Icon sizes consistent: sm=16px, md=18px, lg=20px, xl=24px
- [ ] Icon colors use semantic token classes
- [ ] No inline icon SVGs (use component imports)
- [ ] All decorative icons have `aria-hidden="true"`
- [ ] All functional icons have `aria-label`

---

## 3. Dark Mode

### 3.1 Global Dark Mode
- [ ] `<html>` element gets `.dark` class correctly via orbit-theme-init
- [x] `ThemeProvider` initializes dark mode from localStorage
- [x] `ThemeToggle` in sidebar works correctly
- [ ] Theme persists across page reloads
- [ ] System preference detection (`prefers-color-scheme: dark`)
- [ ] No FOUC on page load
- [ ] CSS custom properties switch correctly in dark mode

### 3.2 Dashboard Page -- Dark Mode
- [ ] Page background color (`bg-surface-muted` or equivalent)
- [ ] KPI card: Total Asset Value -- background, text, trend indicator
- [ ] KPI card: Depreciated Value -- background, text, trend indicator
- [ ] KPI card: Monthly Burn -- background, text, trend indicator
- [ ] KPI card: Compliance Risk -- background, text, risk badge
- [ ] KPI card borders
- [ ] KPI card shadows
- [ ] KPI card icon backgrounds (Calendar, Plus, TrendingUp, TrendingDown, etc.)
- [ ] KPI card icon colors
- [ ] Asset Value Trend chart: background
- [ ] Asset Value Trend chart: area fill gradient
- [ ] Asset Value Trend chart: stroke color
- [ ] Asset Value Trend chart: axis label colors
- [ ] Asset Value Trend chart: grid line colors
- [ ] Asset Value Trend chart: tooltip background
- [ ] Asset Value Trend chart: tooltip text
- [ ] Asset Value Trend chart: tooltip border
- [ ] Category Breakdown section: backgrounds
- [ ] Category Breakdown: bar colors per category
- [ ] Category Breakdown: label text colors
- [ ] Category Breakdown: value text colors
- [ ] Category Breakdown: percentage text colors
- [ ] Depreciation by Category: progress bar backgrounds
- [ ] Depreciation by Category: progress bar fill colors
- [ ] Depreciation by Category: category labels
- [ ] Depreciation by Category: value labels
- [ ] Recent Transactions section: background
- [ ] Recent Transactions: row backgrounds
- [ ] Recent Transactions: row hover states
- [ ] Recent Transactions: icon backgrounds (`bg-blue-100`, `bg-purple-100`, `bg-indigo-100`)
- [ ] Recent Transactions: icon colors
- [ ] Recent Transactions: name text color
- [ ] Recent Transactions: category text color
- [ ] Recent Transactions: date text color
- [ ] Recent Transactions: status badge colors
- [ ] Recent Transactions: value text colors (positive green, negative red)
- [ ] Header section: title and subtitle colors
- [ ] Period selector button active/inactive states
- [ ] Filter button colors
- [ ] Loading state text color (`text-slate-500` -> semantic)

### 3.3 Assets Page -- Dark Mode
- [ ] Page background
- [ ] Page header: title and description
- [ ] Search input: background, border, placeholder, text
- [ ] Category filter select: background, border, options
- [ ] Status filter select: background, border, options
- [ ] View toggle buttons (grid/list): active/inactive states
- [ ] "Add Asset" button
- [ ] Asset grid cards: background
- [ ] Asset grid cards: border
- [ ] Asset grid cards: hover state
- [ ] Asset grid cards: shadow
- [ ] Asset grid cards: name text color
- [ ] Asset grid cards: category text color
- [ ] Asset grid cards: status badge colors
- [ ] Asset grid cards: value text color
- [ ] Asset grid cards: depreciation progress bar
- [ ] Asset grid cards: serial number text color
- [ ] Asset grid cards: location text color
- [ ] Asset grid cards: tags display
- [ ] Asset grid cards: action buttons
- [ ] Asset list table: header background
- [ ] Asset list table: header text color
- [ ] Asset list table: row backgrounds (alternating)
- [ ] Asset list table: row hover state
- [ ] Asset list table: cell text colors
- [ ] Asset list table: border colors
- [ ] Asset list table: sort indicator
- [ ] Asset list table: pagination controls
- [ ] Asset detail view: background
- [ ] Asset detail view: field labels
- [ ] Asset detail view: field values
- [ ] Asset detail view: action buttons
- [ ] Empty state: icon and text colors
- [ ] "No results" state: text colors

### 3.4 Transactions Page -- Dark Mode
- [ ] Page background
- [ ] Page header: title and description
- [ ] Search input: background, border, placeholder, text
- [ ] Type filter select: background, border, options
- [ ] Status filter select: background, border, options
- [ ] Date range picker: background, border, calendar popup
- [ ] "Add Transaction" button
- [ ] Transaction list table: header background
- [ ] Transaction list table: header text color
- [ ] Transaction list table: row backgrounds (alternating)
- [ ] Transaction list table: row hover state
- [ ] Transaction list table: cell text colors
- [ ] Transaction list table: border colors
- [ ] Transaction list table: type badge colors (acquisition, disposal, depreciation, maintenance, insurance)
- [ ] Transaction list table: status badge colors (completed, pending, review)
- [ ] Transaction list table: amount colors (positive green, negative red)
- [ ] Transaction list table: date text colors
- [ ] Transaction list table: description text colors
- [ ] Transaction list table: asset name link colors
- [ ] Transaction list table: sort indicator
- [ ] Transaction list table: pagination controls
- [ ] Transaction summary card: background
- [ ] Transaction summary card: total amount
- [ ] Transaction summary card: by type breakdown
- [ ] Transaction detail view: background
- [ ] Transaction detail view: field labels
- [ ] Transaction detail view: field values
- [ ] Empty state: icon and text colors
- [ ] Export button

### 3.5 Reports Page -- Dark Mode
- [ ] Page background
- [ ] Page header: title and description
- [ ] "Generate Report" button
- [ ] Report type selection cards: background
- [ ] Report type selection cards: border
- [ ] Report type selection cards: hover state
- [ ] Report type selection cards: icon colors
- [ ] Report type selection cards: text colors
- [ ] Report list: card backgrounds
- [ ] Report list: card borders
- [ ] Report list: report title text
- [ ] Report list: report type badge
- [ ] Report list: report date text
- [ ] Report list: report status badge (ready/generating)
- [ ] Report list: action buttons (download, share, delete)
- [ ] Report viewer: background
- [ ] Report viewer: table headers
- [ ] Report viewer: table rows
- [ ] Report viewer: chart backgrounds
- [ ] Report viewer: chart colors
- [ ] Report viewer: text colors
- [ ] Portfolio report: value displays
- [ ] Depreciation report: schedule table
- [ ] Compliance report: status indicators
- [ ] Transactions report: summary table
- [ ] Empty state: icon and text colors

### 3.6 Layout -- Dark Mode
- [ ] Sidebar background (`bg-surface-base`)
- [ ] Sidebar border right (`border-border-default`)
- [ ] Sidebar brand icon background
- [ ] Sidebar brand text colors (`text-content-primary`, `text-content-muted`)
- [ ] Sidebar nav item text colors (active/inactive)
- [ ] Sidebar nav item active background (`bg-primary-50` / `dark:bg-primary-950/30`)
- [ ] Sidebar nav item hover background (`bg-surface-muted`)
- [ ] Sidebar bottom section border (`border-border-subtle`)
- [ ] Sidebar theme toggle area
- [ ] Sidebar help link colors
- [ ] Sidebar sign out button colors
- [ ] Mobile header: background
- [ ] Mobile header: border bottom
- [ ] Mobile header: text colors
- [ ] Mobile header: hamburger icon color
- [ ] Mobile backdrop overlay color
- [ ] Offline banner: dark mode styling

### 3.7 Recharts Dark Mode
- [ ] All Recharts charts use CSS variable colors (not hardcoded)
- [ ] AreaChart: gradient fill uses dark-mode-aware colors
- [ ] AreaChart: stroke uses dark-mode-aware colors
- [ ] XAxis: tick label color from CSS variable
- [ ] YAxis: tick label color from CSS variable
- [ ] Tooltip: background from CSS variable
- [ ] Tooltip: text from CSS variable
- [ ] Tooltip: border from CSS variable
- [ ] CartesianGrid: stroke from CSS variable
- [ ] ResponsiveContainer: background transparent
- [ ] Legend: text color from CSS variable
- [ ] Bar colors per category use CSS variables
- [ ] Line colors per dataset use CSS variables
- [ ] Pie/Donut segment colors use CSS variables

### 3.8 Scrollbar Dark Mode
- [ ] All scrollbar track colors use `var(--orbit-surface-muted)`
- [ ] All scrollbar thumb colors use `var(--orbit-border-strong)`
- [ ] Scrollbar thumb hover color
- [ ] Scrollbar in all scrollable containers (tables, lists, main content)

---

## 4. Core Features

### 4.1 Dashboard -- Portfolio Overview
- [ ] Total Asset Value KPI card
- [ ] Total Asset Value: displays formatted currency
- [ ] Total Asset Value: trend indicator (percentage change 30d)
- [ ] Total Asset Value: trend direction arrow (up/down)
- [ ] Total Asset Value: trend color (green for positive, red for negative)
- [ ] Depreciated Value KPI card
- [ ] Depreciated Value: displays formatted currency
- [ ] Depreciated Value: trend indicator
- [ ] Monthly Burn KPI card
- [ ] Monthly Burn: displays formatted currency
- [ ] Monthly Burn: trend indicator
- [ ] Compliance Risk KPI card
- [ ] Compliance Risk: displays risk level (Low/Medium/High)
- [ ] Compliance Risk: issues count
- [ ] Compliance Risk: color coding by level
- [ ] Period selector: MTD (month-to-date)
- [ ] Period selector: QTD (quarter-to-date)
- [ ] Period selector: YTD (year-to-date)
- [ ] Period selector: Custom date range
- [ ] Period selector: changes refresh all dashboard data

### 4.2 Dashboard -- Charts
- [ ] Asset Value Trend chart (Recharts AreaChart)
- [ ] Asset Value Trend: 10-12 months of data
- [ ] Asset Value Trend: monthly data points
- [ ] Asset Value Trend: gradient fill area
- [ ] Asset Value Trend: smooth curve (monotone)
- [ ] Asset Value Trend: responsive sizing
- [ ] Asset Value Trend: tooltip with month and value
- [ ] Asset Value Trend: X-axis with month labels
- [ ] Asset Value Trend: Y-axis with currency values
- [ ] Category Breakdown chart/bars
- [ ] Category Breakdown: bar per category
- [ ] Category Breakdown: percentage of total
- [ ] Category Breakdown: asset count per category
- [ ] Category Breakdown: total value per category
- [ ] Category Breakdown: color coding per category
- [ ] Depreciation by Category bars
- [ ] Depreciation by Category: progress bar per category
- [ ] Depreciation by Category: value label
- [ ] Depreciation by Category: percentage width
- [ ] Depreciation by Category: color coding
- [ ] Revenue trend chart (12 months, Recharts LineChart)
- [ ] Expense breakdown donut chart (by category)
- [ ] Budget vs. actual bar chart (by department)

### 4.3 Dashboard -- Recent Activity
- [ ] Recent Transactions list (last 10)
- [ ] Recent Transactions: asset name
- [ ] Recent Transactions: category
- [ ] Recent Transactions: date
- [ ] Recent Transactions: status badge
- [ ] Recent Transactions: value (positive/negative formatting)
- [ ] Recent Transactions: icon per category
- [ ] Recent Transactions: click to view transaction detail
- [ ] "View All" link to Transactions page
- [ ] Outstanding invoices count and total amount
- [ ] Cash position summary (bank balance)

### 4.4 Asset Management
- [ ] Asset list view (grid layout)
- [ ] Asset list view (table layout)
- [ ] Asset list: toggle between grid and table view
- [ ] Asset list: search by name
- [ ] Asset list: search by serial number
- [ ] Asset list: filter by category (hardware, software, real_estate, vehicle, furniture, other)
- [ ] Asset list: filter by status (active, review, disposed, maintenance)
- [ ] Asset list: sort by name (A-Z, Z-A)
- [ ] Asset list: sort by value (high-low, low-high)
- [ ] Asset list: sort by purchase date (newest, oldest)
- [ ] Asset list: sort by depreciation percentage
- [ ] Asset list: sort by status
- [ ] Asset list: pagination
- [ ] Asset list: items per page selector
- [ ] Asset list: total count display
- [ ] Asset card: name
- [ ] Asset card: category badge
- [ ] Asset card: status badge
- [ ] Asset card: current value (formatted currency)
- [ ] Asset card: purchase value (formatted currency)
- [ ] Asset card: depreciation percentage (progress bar)
- [ ] Asset card: purchase date
- [ ] Asset card: location
- [ ] Asset card: serial number
- [ ] Asset card: tags
- [ ] Asset card: action menu (edit, delete, change status)
- [ ] Asset card: click to view detail
- [ ] Asset creation form: name (required)
- [ ] Asset creation form: category select (required)
- [ ] Asset creation form: status select (default: active)
- [ ] Asset creation form: purchase value (required, number)
- [ ] Asset creation form: current value (required, number)
- [ ] Asset creation form: depreciation percentage (number, 0-100)
- [ ] Asset creation form: purchase date (date picker)
- [ ] Asset creation form: location (optional)
- [ ] Asset creation form: serial number (optional)
- [ ] Asset creation form: notes (optional, textarea)
- [ ] Asset creation form: tags (optional, multi-input)
- [ ] Asset creation form: validation messages
- [ ] Asset creation form: submit creates asset and shows in list
- [ ] Asset creation form: cancel returns to list
- [ ] Asset edit form: pre-populated fields
- [ ] Asset edit form: save updates asset
- [ ] Asset edit form: cancel discards changes
- [ ] Asset deletion: confirmation dialog
- [ ] Asset deletion: removes from list
- [ ] Asset detail view: all asset fields displayed
- [ ] Asset detail view: transaction history for this asset
- [ ] Asset detail view: depreciation schedule
- [ ] Asset detail view: edit button
- [ ] Asset detail view: delete button
- [ ] Asset detail view: change status button
- [ ] Bulk actions: select multiple assets
- [ ] Bulk actions: delete selected
- [ ] Bulk actions: change status of selected
- [ ] Bulk actions: export selected
- [ ] Export assets: CSV format
- [ ] Export assets: PDF format
- [ ] Import assets: CSV upload
- [ ] Asset loading state
- [ ] Asset error state
- [ ] Asset empty state

### 4.5 Transactions
- [ ] Transaction list view (table)
- [ ] Transaction list: all transactions
- [ ] Transaction list: filter by type (acquisition, disposal, depreciation, maintenance, insurance)
- [ ] Transaction list: filter by status (completed, pending, review)
- [ ] Transaction list: filter by date range
- [ ] Transaction list: filter by asset
- [ ] Transaction list: filter by category
- [ ] Transaction list: search by description
- [ ] Transaction list: sort by date (newest, oldest)
- [ ] Transaction list: sort by amount (high-low, low-high)
- [ ] Transaction list: sort by type
- [ ] Transaction list: sort by status
- [ ] Transaction list: pagination
- [ ] Transaction list: items per page selector
- [ ] Transaction list: total count display
- [ ] Transaction row: date
- [ ] Transaction row: description
- [ ] Transaction row: type badge
- [ ] Transaction row: status badge
- [ ] Transaction row: amount (formatted, colored)
- [ ] Transaction row: asset name (link to asset)
- [ ] Transaction row: category
- [ ] Transaction row: action menu
- [ ] Transaction creation: description (required)
- [ ] Transaction creation: amount (required, positive number)
- [ ] Transaction creation: debit account select
- [ ] Transaction creation: credit account select
- [ ] Transaction creation: idempotency key (optional)
- [ ] Transaction creation: metadata (optional, JSON)
- [ ] Transaction creation: validation
- [ ] Transaction creation: submit
- [ ] Transaction creation: success/error handling
- [ ] Transaction detail view: all fields
- [ ] Transaction detail view: linked asset
- [ ] Transaction detail view: account details
- [ ] Transaction summary: total amount by type
- [ ] Transaction summary: count by type
- [ ] Transaction summary: monthly comparison
- [ ] Export transactions: CSV format
- [ ] Export transactions: PDF format
- [ ] Transaction loading state
- [ ] Transaction error state
- [ ] Transaction empty state

### 4.6 Reports
- [ ] Report list view
- [ ] Report list: all generated reports
- [ ] Report list: filter by type (portfolio, depreciation, compliance, transactions)
- [ ] Report list: filter by status (ready, generating)
- [ ] Report list: sort by date (newest, oldest)
- [ ] Report list: report title
- [ ] Report list: report type badge
- [ ] Report list: report date
- [ ] Report list: report period
- [ ] Report list: report status badge
- [ ] Report list: download action
- [ ] Report list: share action
- [ ] Report list: delete action
- [ ] Report generation: select report type
- [ ] Report generation: select period (MTD, QTD, YTD, custom range)
- [ ] Report generation: additional options per type
- [ ] Report generation: generate button
- [ ] Report generation: loading state during generation
- [ ] Report generation: success notification
- [ ] Report generation: error handling
- [ ] Portfolio report: total asset value summary
- [ ] Portfolio report: value by category breakdown
- [ ] Portfolio report: value trend chart
- [ ] Portfolio report: top assets by value
- [ ] Portfolio report: asset count summary
- [ ] Depreciation report: depreciation schedule table
- [ ] Depreciation report: depreciation by category chart
- [ ] Depreciation report: monthly depreciation trend
- [ ] Depreciation report: fully depreciated assets list
- [ ] Depreciation report: upcoming full depreciation alerts
- [ ] Compliance report: compliance score
- [ ] Compliance report: compliance issues list
- [ ] Compliance report: regulatory requirements checklist
- [ ] Compliance report: audit trail
- [ ] Compliance report: risk assessment
- [ ] Transactions report: transaction summary table
- [ ] Transactions report: transaction volume chart
- [ ] Transactions report: transaction by type breakdown
- [ ] Transactions report: large transaction alerts
- [ ] Download report as PDF
- [ ] Download report as CSV/Excel
- [ ] Share report via email
- [ ] Report loading state
- [ ] Report error state
- [ ] Report empty state

### 4.7 Budget Tracking
- [ ] Budget creation: period (monthly, quarterly, annual)
- [ ] Budget creation: departments / cost centers
- [ ] Budget creation: line items with amounts
- [ ] Budget approval workflow
- [ ] Budget vs. actuals table (line-by-line comparison)
- [ ] Budget variance calculation
- [ ] Budget variance alerts (>10% over budget auto-flag)
- [ ] Budget forecasting (project end-of-period actuals)
- [ ] Budget utilization progress bars by department
- [ ] Budget summary dashboard widget

### 4.8 Depreciation
- [ ] Auto-depreciation calculation (straight-line method)
- [ ] Depreciation schedule per asset
- [ ] Monthly depreciation run (batch process)
- [ ] Depreciation adjustment entries
- [ ] Accumulated depreciation tracking
- [ ] Book value calculation
- [ ] Depreciation method selection (straight-line, declining balance, units-of-production)
- [ ] Useful life configuration per asset category
- [ ] Salvage value configuration
- [ ] Depreciation report generation

### 4.9 Compliance
- [ ] Compliance score calculation
- [ ] Compliance checks: asset valuation current
- [ ] Compliance checks: depreciation schedules up to date
- [ ] Compliance checks: all assets have required fields
- [ ] Compliance checks: disposal documentation complete
- [ ] Compliance checks: insurance coverage current
- [ ] Compliance alerts: score drops below threshold
- [ ] Compliance alerts: missing documentation
- [ ] Audit trail: all asset changes logged
- [ ] Audit trail: all transaction changes logged
- [ ] Regulatory requirements checklist

### 4.10 Financial KPIs
- [ ] Total asset value (real-time)
- [ ] Total depreciation (cumulative)
- [ ] Monthly burn rate
- [ ] Compliance score (percentage)
- [ ] Asset value change (30-day)
- [ ] Asset count by category
- [ ] Asset count by status
- [ ] Average asset age
- [ ] Average depreciation rate
- [ ] Total maintenance costs (MTD)
- [ ] Total acquisition costs (MTD)
- [ ] Total disposal proceeds (MTD)
- [ ] Return on assets (ROA)

### 4.11 Invoicing
- [ ] Invoice list: number, client, amount, due date, status
- [ ] Invoice creation: line items, tax, discount
- [ ] Invoice PDF generation and download
- [ ] Invoice status: draft / sent / paid / overdue
- [ ] Payment recording
- [ ] Overdue invoice reminders
- [ ] Invoice template customization
- [ ] Invoice numbering (auto-increment)

### 4.12 Expenses
- [ ] Expense submissions (employee reports)
- [ ] Expense approval workflow (manager -> finance)
- [ ] Receipt image upload and OCR
- [ ] Expense categories and cost center tagging
- [ ] Export to CSV / accounting software (QuickBooks format)
- [ ] Expense limits and policies
- [ ] Recurring expense tracking

### 4.13 Accounts & Chart of Accounts
- [ ] Chart of accounts (COA) management
- [ ] Account types: asset, liability, equity, revenue, expense
- [ ] Account creation: name, type, parent account
- [ ] Account hierarchy (parent/child)
- [ ] Account balance display
- [ ] Journal entries (double-entry bookkeeping)
- [ ] Journal entry: debit account, credit account, amount, description
- [ ] Journal entry: validation (debits = credits)
- [ ] Trial balance report
- [ ] Financial statements: Profit & Loss (Income Statement)
- [ ] Financial statements: Balance Sheet
- [ ] Financial statements: Cash Flow Statement
- [ ] Export financial reports as PDF
- [ ] Export financial reports as Excel

### 4.14 Bank Account Connections
- [ ] Bank account list (read-only balance feeds)
- [ ] Bank account: connection status
- [ ] Bank account: last sync timestamp
- [ ] Bank account: current balance
- [ ] Bank account: transaction history
- [ ] Bank reconciliation (match bank transactions to journal entries)
- [ ] Multi-currency support

### 4.15 CSV / PDF Export
- [ ] Export assets list as CSV
- [ ] Export assets list with selected columns only
- [ ] Export assets list with current filters applied
- [ ] Export transactions list as CSV
- [ ] Export transactions list with date range filter
- [ ] Export reports as PDF
- [ ] Export portfolio summary as PDF
- [ ] Export depreciation schedule as PDF
- [ ] Export compliance report as PDF
- [ ] Export budget vs actuals as PDF
- [ ] Export financial statements as PDF
- [ ] Export financial statements as Excel
- [ ] PDF: company branding / letterhead
- [ ] PDF: page numbers and timestamps
- [ ] PDF: table of contents for multi-page reports
- [ ] CSV: proper escaping of commas and quotes
- [ ] CSV: UTF-8 encoding with BOM
- [ ] Download progress indicator
- [ ] Server-side generation for large exports (avoid browser timeout)

### 4.16 Notifications & Alerts
- [ ] Budget overrun alert (expense exceeds budget)
- [ ] Large transaction alert (transaction above threshold)
- [ ] Asset maintenance due alert
- [ ] Asset warranty expiry alert
- [ ] Insurance renewal alert
- [ ] Compliance score drop alert
- [ ] Monthly depreciation reminder
- [ ] Quarterly report due reminder
- [ ] Stale asset review alert (no update in 12 months)
- [ ] Alert delivery: in-app notification
- [ ] Alert delivery: email notification
- [ ] Alert preferences: configurable per alert type
- [ ] Alert history log
- [ ] Alert dismissal / acknowledgment

### 4.17 Settings Page
- [ ] Settings page/view (new route: /settings)
- [ ] Organization settings: company name, fiscal year start
- [ ] Organization settings: default currency
- [ ] Organization settings: number format preference
- [ ] Asset settings: default depreciation method
- [ ] Asset settings: default useful life by category
- [ ] Asset settings: auto-depreciation toggle
- [ ] Alert settings: budget overrun threshold (%)
- [ ] Alert settings: large transaction threshold ($)
- [ ] Alert settings: email notification toggles
- [ ] Display settings: default dashboard period
- [ ] Display settings: default list page size
- [ ] Display settings: compact/comfortable density
- [ ] Export settings: default format (CSV/PDF)
- [ ] Export settings: include company branding toggle
- [ ] Save settings confirmation
- [ ] Reset to defaults option

---

## 5. API Integration

### 5.1 API Service Configuration
- [x] API service module created (`src/services/api.ts`)
- [x] Base URL configurable via `VITE_CAPITAL_BACKEND` env variable
- [x] API path configurable via `VITE_API_BASE` env variable
- [x] Authorization header from localStorage token
- [x] X-Org-Id header from localStorage
- [x] 401 handler dispatches `unauthorized_access` event
- [ ] Request timeout configuration
- [ ] Retry logic for failed requests
- [ ] Request cancellation on component unmount
- [ ] Request deduplication
- [ ] Error normalization (consistent error shape)

### 5.2 Portfolio API
- [x] `fetchPortfolioSummary()` -- GET `/capital/portfolio/summary`
- [ ] Portfolio summary: total_asset_value populated from real data
- [ ] Portfolio summary: total_depreciation populated
- [ ] Portfolio summary: monthly_burn populated
- [ ] Portfolio summary: compliance_score populated
- [ ] Portfolio summary: value_change_30d populated
- [ ] Portfolio summary: category_breakdown populated
- [ ] Portfolio summary: monthly_values populated

### 5.3 Assets API
- [x] `fetchAssets(filters?)` -- GET `/capital/assets`
- [x] `fetchAsset(id)` -- GET `/capital/assets/:id`
- [x] `createAsset(data)` -- POST `/capital/assets`
- [x] `updateAsset(id, data)` -- PUT `/capital/assets/:id`
- [x] `deleteAsset(id)` -- DELETE `/capital/assets/:id`
- [ ] Assets: category filter query param
- [ ] Assets: status filter query param
- [ ] Assets: search query param
- [ ] Assets: pagination query params (page, limit)
- [ ] Assets: sort query params (sort_by, sort_order)
- [ ] Assets: bulk delete endpoint
- [ ] Assets: bulk status update endpoint
- [ ] Assets: export endpoint (CSV)
- [ ] Assets: import endpoint (CSV upload)

### 5.4 Transactions API
- [x] `fetchTransactions(filters?)` -- GET `/capital/transactions`
- [ ] Transactions: asset_id filter
- [ ] Transactions: type filter
- [ ] Transactions: date range filter (from, to)
- [ ] Transactions: limit parameter
- [ ] Transactions: pagination (page, limit)
- [ ] Transactions: sort params
- [ ] Transactions: create endpoint used from frontend
- [ ] Transactions: export endpoint (CSV)

### 5.5 Reports API
- [x] `fetchReports()` -- GET `/capital/reports`
- [x] `generateReport(type, period)` -- POST `/capital/reports`
- [ ] Reports: download endpoint (PDF)
- [ ] Reports: download endpoint (CSV/Excel)
- [ ] Reports: delete endpoint
- [ ] Reports: share endpoint

### 5.6 Accounts API
- [ ] GET `/capital/accounts` -- list accounts
- [ ] POST `/capital/accounts` -- create account
- [ ] PUT `/capital/accounts/:id` -- update account
- [ ] DELETE `/capital/accounts/:id` -- delete account
- [ ] GET `/capital/accounts/:id/transactions` -- account transactions

### 5.7 Additional API Endpoints
- [ ] GET `/capital/budget` -- budget data
- [ ] POST `/capital/budget` -- create budget
- [ ] GET `/capital/compliance/score` -- compliance score
- [ ] GET `/capital/compliance/issues` -- compliance issues
- [ ] GET `/capital/kpis` -- financial KPIs
- [ ] GET `/capital/depreciation/schedule` -- depreciation schedule
- [ ] POST `/capital/depreciation/run` -- run depreciation batch

### 5.8 API Headers & Auth
- [x] X-Org-Id on all requests
- [x] Authorization Bearer token on all requests
- [x] Pagination on all list endpoints (backend supports)
- [ ] X-Request-Id on all requests
- [ ] X-Workspace-Id on applicable requests
- [ ] Export endpoints (PDF/CSV generation on server)
- [ ] Recharts datasets use CSS variable colors (dark-mode responsive)

### 5.9 EventBus Integration
- [ ] Publish events on asset created
- [ ] Publish events on asset updated
- [ ] Publish events on asset disposed
- [ ] Publish events on large transaction created
- [ ] Publish events on budget overage
- [ ] Publish events on compliance score change
- [ ] Consume events from other Orbit apps
- [ ] Real-time dashboard updates via EventBus

---

## 6. State Management

### 6.1 Current State Approach
- [ ] Decide on state management approach (Zustand, React Query, or local state)
- [ ] Currently: local state with useState in each page component
- [ ] Dashboard: `data` state holds all dashboard data
- [ ] Dashboard: `loading` state
- [ ] Dashboard: mock data fallback on API failure
- [ ] Remove mock data fallback in production

### 6.2 Zustand Store (if adopted)
- [ ] Create `src/store/useCapitalStore.ts`
- [ ] Store: portfolio summary state
- [ ] Store: assets list state
- [ ] Store: transactions list state
- [ ] Store: reports list state
- [ ] Store: filters state (per page)
- [ ] Store: loading states per section
- [ ] Store: error states per section
- [ ] Store: selected asset state
- [ ] Store: selected transaction state
- [ ] Store: UI state (sidebar, view mode)
- [ ] Store: persist preferences (view mode, filters)
- [ ] Store: fetchPortfolioSummary action
- [ ] Store: fetchAssets action
- [ ] Store: createAsset action
- [ ] Store: updateAsset action
- [ ] Store: deleteAsset action
- [ ] Store: fetchTransactions action
- [ ] Store: fetchReports action
- [ ] Store: generateReport action

### 6.3 React Query (alternative)
- [ ] Install `@tanstack/react-query`
- [ ] Configure QueryClient with defaults
- [ ] Cache time configuration
- [ ] Stale time configuration
- [ ] Retry configuration
- [ ] Portfolio summary query hook
- [ ] Assets list query hook (with filter params)
- [ ] Asset detail query hook
- [ ] Transactions list query hook
- [ ] Reports list query hook
- [ ] Asset create mutation
- [ ] Asset update mutation
- [ ] Asset delete mutation
- [ ] Transaction create mutation
- [ ] Report generate mutation
- [ ] Optimistic updates for mutations
- [ ] Cache invalidation on mutations

### 6.4 Derived State
- [ ] Total asset value calculation
- [ ] Asset count by category
- [ ] Asset count by status
- [ ] Total depreciation calculation
- [ ] Transaction total by type
- [ ] Transaction total by status
- [ ] Budget variance calculation
- [ ] Compliance score calculation

---

## 7. Performance

### 7.1 Code Splitting & Lazy Loading
- [x] All 4 page components lazy-loaded with `React.lazy()`
- [x] Dashboard lazy-loaded
- [x] Assets lazy-loaded
- [x] Transactions lazy-loaded
- [x] Reports lazy-loaded
- [x] `<Suspense>` wrapping Routes with fallback
- [ ] Suspense fallback shows `<Skeleton>` instead of spinner
- [ ] Layout component not lazy-loaded (always needed)

### 7.2 Bundle Optimization
- [ ] Vite code splitting configured
- [ ] Vendor chunk: react, react-dom, react-router-dom
- [ ] Vendor chunk: recharts (large dependency)
- [ ] Vendor chunk: @orbit-ui/react
- [ ] Vendor chunk: lucide-react (tree-shaken)
- [ ] Bundle size analyzed with `vite-plugin-visualizer`
- [ ] Total bundle size < 500KB gzipped
- [ ] Recharts tree-shaken (only import used chart components)
- [ ] No duplicate dependencies
- [ ] Tree-shaking verified

### 7.3 Runtime Performance
- [ ] Dashboard data: stale-while-revalidate caching
- [ ] Asset list: virtual scrolling for >100 items
- [ ] Transaction list: virtual scrolling for >100 items
- [ ] Search: debounced input (300ms)
- [ ] Filter changes: debounced API calls
- [ ] Charts: memoized with React.memo
- [ ] Charts: responsive without re-render on window resize (use container)
- [ ] API calls: deduplicated concurrent requests
- [ ] Images: lazy loading
- [ ] Memoized expensive computations (currency formatting, sorting)
- [ ] React.memo on pure components (KPI cards, table rows)
- [ ] useMemo for derived state
- [ ] useCallback for event handlers
- [ ] No unnecessary re-renders (React DevTools Profiler)

### 7.4 Network Performance
- [ ] API response caching
- [ ] Conditional requests (ETag/If-None-Match)
- [ ] Request batching (portfolio + assets + transactions in parallel)
- [ ] Prefetch adjacent pages (hover on pagination)
- [ ] Offline support: cache last-fetched data
- [ ] Service worker for asset caching
- [ ] Compression: gzip/brotli on responses

### 7.5 Rendering Performance
- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] First Input Delay < 100ms
- [ ] Time to Interactive < 3.5s
- [ ] Lighthouse performance score > 90

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Keyboard Navigation
- [ ] All interactive elements focusable with Tab
- [ ] Focus order follows visual order
- [ ] Focus visible indicator on all interactive elements
- [ ] Skip to main content link
- [ ] Escape key closes modals and dropdowns
- [ ] Enter/Space activates buttons and links
- [ ] Arrow keys navigate within menus, tabs, table rows
- [ ] Sidebar navigation keyboard accessible
- [ ] Table row keyboard navigation
- [ ] Table column sort via keyboard
- [ ] Modal trap focus within modal
- [ ] Dropdown menu keyboard navigation
- [ ] Date picker keyboard navigation
- [ ] Asset card keyboard activation
- [ ] Chart keyboard navigation (data points)
- [ ] Pagination keyboard navigation
- [ ] Keyboard shortcut: Cmd+K for command palette

### 8.2 Screen Reader Support
- [ ] All images have alt text
- [ ] All icons have aria-labels or aria-hidden
- [ ] All form inputs have associated labels
- [ ] All form inputs have aria-describedby for errors
- [ ] Sidebar navigation uses `<nav>` with aria-label
- [ ] Main content area uses `<main>` landmark
- [ ] Header uses `<header>` landmark
- [ ] Sidebar uses `<aside>` landmark
- [ ] Modals have aria-modal="true" and role="dialog"
- [ ] Modals have aria-labelledby pointing to title
- [ ] Tables have `<caption>` or aria-label
- [ ] Table headers use `<th>` with scope attribute
- [ ] Sort direction announced via aria-sort
- [ ] Loading states announced with aria-live="polite"
- [ ] Dynamic content updates via aria-live regions
- [ ] Currency values announced correctly
- [ ] Chart data available in text/table form for screen readers
- [ ] Page title updates on route change
- [ ] Breadcrumbs use `<nav>` with aria-label="Breadcrumb"

### 8.3 Color & Contrast
- [ ] All text meets 4.5:1 contrast ratio
- [ ] All large text meets 3:1 contrast ratio
- [ ] All interactive elements meet 3:1 contrast
- [ ] Status colors not solely reliant on color (icons/text added)
- [ ] Asset status badges readable in both themes
- [ ] Transaction type badges readable in both themes
- [ ] Chart data distinguishable without color (patterns/labels)
- [ ] Positive/negative values distinguishable without color (use + / - prefix)
- [ ] Focus ring visible against all backgrounds
- [ ] Error messages not solely indicated by red

### 8.4 Forms & Inputs
- [ ] All form fields have visible labels
- [ ] Required fields indicated (asterisk + text, not just color)
- [ ] Error messages displayed adjacent to field
- [ ] Error messages descriptive
- [ ] Form submission errors summarized
- [ ] Autocomplete attributes on inputs
- [ ] Input type attributes correct (number, text, date)
- [ ] Placeholder text not used as sole label
- [ ] Number inputs have proper step, min, max

### 8.5 Motion & Animation
- [ ] `prefers-reduced-motion` respected
- [ ] Chart animations can be disabled
- [ ] Page transition animations respect preference
- [ ] No flashing content
- [ ] Skeleton loading respects motion preference

### 8.6 Responsive Accessibility
- [ ] Content readable at 200% zoom
- [ ] Content readable at 400% zoom
- [ ] No horizontal scroll at 320px viewport
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Tap target spacing minimum 8px

### 8.7 Data Table Accessibility
- [ ] Asset table: column headers announced by screen reader
- [ ] Asset table: sort state announced (aria-sort)
- [ ] Asset table: row selection announced
- [ ] Asset table: pagination controls have aria-labels
- [ ] Transaction table: column headers announced
- [ ] Transaction table: sort state announced
- [ ] Transaction table: currency values announced correctly
- [ ] Transaction table: positive/negative amounts distinguished by text (not just color)
- [ ] Report tables: all headers and data cells properly associated
- [ ] Empty table state: "No data" announced
- [ ] Table loading state: "Loading" announced (aria-busy)

### 8.8 Chart Accessibility
- [ ] All charts have aria-label describing the data
- [ ] All charts have text alternative (data table view)
- [ ] Recharts tooltip accessible via keyboard
- [ ] Chart legend items focusable and togglable
- [ ] Chart data downloadable as CSV (screen reader friendly alternative)
- [ ] High contrast mode: charts remain readable
- [ ] Color blind mode: chart colors distinguishable (use patterns)

### 8.9 Financial Data Accessibility
- [ ] Currency values formatted consistently ($X,XXX.XX)
- [ ] Currency values have correct aria-label ("forty two thousand five hundred dollars")
- [ ] Percentage values have % announced
- [ ] Negative values clearly announced as negative
- [ ] Date values announced in full format
- [ ] KPI trend direction announced (up/down by X percent)

---

## 9. Mobile & Responsive

### 9.1 Breakpoint Strategy
- [ ] Mobile: 0-639px (sm)
- [ ] Tablet: 640-1023px (md/lg)
- [ ] Desktop: 1024px+ (lg)
- [ ] All breakpoints tested

### 9.2 Layout Responsive Behavior
- [x] Sidebar: hidden on mobile, overlay on toggle (lg:hidden / lg:flex)
- [x] Mobile header with hamburger menu
- [x] Sidebar close button on mobile
- [x] Mobile backdrop overlay
- [ ] Main content: full width on mobile
- [ ] Main content: padding adjusts per breakpoint
- [ ] Dashboard: KPI cards stack to 2-column on tablet, 1-column on mobile
- [ ] Dashboard: charts full width on mobile
- [ ] Dashboard: recent transactions card full width on mobile
- [ ] Assets: grid to 2-column on tablet, 1-column on mobile
- [ ] Assets: switch to list view on mobile automatically
- [ ] Transactions: horizontal scroll on table for mobile
- [ ] Transactions: card view alternative on mobile
- [ ] Reports: single column on mobile
- [ ] Reports: chart responsive sizing
- [ ] All modals full-screen on mobile
- [ ] All drawers full-width on mobile

### 9.3 Touch Interactions
- [ ] Touch-friendly button sizes (minimum 44px)
- [ ] Swipe to reveal actions on mobile (asset cards, transaction rows)
- [ ] Pull to refresh (mobile)
- [ ] Touch-friendly dropdowns
- [ ] Touch-friendly date pickers
- [ ] Touch-friendly number inputs
- [ ] No hover-only interactions

### 9.4 Mobile-Specific Features
- [ ] Mobile: bottom navigation bar (optional)
- [ ] Mobile: floating action button for add asset
- [ ] Mobile: compact KPI cards
- [ ] Mobile: collapsible chart sections
- [ ] Mobile: simplified table views (priority columns only)

---

## 10. Internationalization

### 10.1 i18n Framework
- [ ] i18n library installed (react-i18next or similar)
- [ ] i18n provider wrapping app
- [ ] Default language: English (en)
- [ ] Language detection from browser
- [ ] Language persistence in localStorage
- [ ] Language selector in UI

### 10.2 String Extraction
- [ ] All user-facing strings extracted to translation files
- [ ] Dashboard strings extracted
- [ ] Assets strings extracted
- [ ] Transactions strings extracted
- [ ] Reports strings extracted
- [ ] Layout strings extracted
- [ ] Error messages extracted
- [ ] Empty state messages extracted
- [ ] Validation messages extracted
- [ ] Category labels extracted (currently in api.ts: categoryLabels)
- [ ] Status labels extracted (currently in api.ts: statusLabels)
- [ ] Transaction type labels extracted

### 10.3 Date & Number Formatting
- [ ] Dates formatted with locale-aware formatter
- [ ] Currency formatted with locale-aware formatter
- [ ] Currently: hardcoded USD (`formatCurrency` in api.ts)
- [ ] Currency: configurable per org (not just USD)
- [ ] Numbers formatted with locale-aware grouping
- [ ] Percentages formatted with locale-aware formatter
- [ ] Relative time formatting
- [ ] Large number abbreviation locale-aware (K, M, B)

### 10.4 RTL Support
- [ ] Layout supports RTL languages
- [ ] Sidebar position mirrors in RTL
- [ ] Chart axes mirror for RTL
- [ ] Table column order adjusts for RTL
- [ ] Text alignment adjusts for RTL
- [ ] Padding/margin adjusted for RTL (logical properties)

---

## 11. Security

### 11.1 Authentication
- [x] Token read from localStorage (auth_token, access_token, gate_access_token)
- [x] Authorization Bearer header on API requests
- [x] 401 response triggers `unauthorized_access` event
- [ ] Sign out clears all tokens (Layout.tsx signOut function)
- [ ] Token refresh on near-expiry
- [ ] Auto-logout on token expiry
- [ ] CSRF protection
- [ ] Secure cookie flags consideration

### 11.2 Authorization
- [ ] Role-based access control
- [ ] Admin-only features gated (e.g., account management)
- [ ] Org isolation verified (X-Org-Id)
- [ ] Server-side authorization for all mutations

### 11.3 Data Protection
- [ ] No sensitive data in URL parameters
- [ ] No sensitive data logged to console
- [ ] Financial data encrypted in transit (HTTPS)
- [ ] Financial data encrypted at rest (database)
- [ ] Org isolation: X-Org-Id on all requests
- [ ] No cross-tenant data leakage
- [ ] Audit trail for all financial operations

### 11.4 Input Validation
- [ ] All form inputs validated on client
- [ ] All form inputs validated on server
- [ ] Amount fields: numeric only, positive values
- [ ] Amount fields: max value limit
- [ ] Description fields: max length limit
- [ ] XSS prevention: sanitize user input
- [ ] SQL injection prevention (parameterized queries on backend)
- [ ] Idempotency keys on financial transactions

### 11.5 Network Security
- [ ] HTTPS enforced
- [ ] Content-Security-Policy header
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Strict-Transport-Security header
- [ ] CORS configured to specific origins only

### 11.6 Dependency Security
- [ ] `npm audit` clean (frontend)
- [ ] `pip audit` clean (backend)
- [ ] No known vulnerable dependencies
- [ ] Lock files committed
- [ ] Dependabot or Renovate configured

---

## 12. Testing

### 12.1 Frontend Unit Tests
- [ ] API service: fetchPortfolioSummary
- [ ] API service: fetchAssets (with filters)
- [ ] API service: fetchAsset
- [ ] API service: createAsset
- [ ] API service: updateAsset
- [ ] API service: deleteAsset
- [ ] API service: fetchTransactions (with filters)
- [ ] API service: fetchReports
- [ ] API service: generateReport
- [ ] API service: formatCurrency
- [ ] API service: getHeaders (token/org extraction)
- [ ] API service: error handling (401, 403, 500)
- [ ] Utils: cn() utility
- [ ] Types: type validation tests

### 12.2 Frontend Component Tests
- [ ] Layout: renders sidebar and main content
- [ ] Layout: sidebar navigation active states
- [ ] Layout: mobile menu toggle
- [ ] Layout: sign out function
- [ ] Dashboard: renders KPI cards
- [ ] Dashboard: renders chart
- [ ] Dashboard: renders category breakdown
- [ ] Dashboard: renders recent transactions
- [ ] Dashboard: loading state
- [ ] Dashboard: error state (mock data fallback)
- [ ] Dashboard: empty state
- [ ] Assets: renders asset list (grid)
- [ ] Assets: renders asset list (table)
- [ ] Assets: filter by category
- [ ] Assets: filter by status
- [ ] Assets: search by name
- [ ] Assets: sort functionality
- [ ] Assets: create asset form
- [ ] Assets: edit asset form
- [ ] Assets: delete confirmation
- [ ] Assets: loading state
- [ ] Assets: empty state
- [ ] Transactions: renders transaction table
- [ ] Transactions: filter by type
- [ ] Transactions: filter by date range
- [ ] Transactions: sort functionality
- [ ] Transactions: loading state
- [ ] Transactions: empty state
- [ ] Reports: renders report list
- [ ] Reports: generate report form
- [ ] Reports: report type selection
- [ ] Reports: loading state
- [ ] Reports: empty state

### 12.3 Frontend Integration Tests
- [ ] Navigation: click sidebar links -> correct page renders
- [ ] Dashboard: load page -> fetch portfolio data -> render
- [ ] Assets: load page -> fetch assets -> render list
- [ ] Assets: create asset -> appears in list
- [ ] Assets: edit asset -> changes reflected
- [ ] Assets: delete asset -> removed from list
- [ ] Transactions: load page -> fetch transactions -> render
- [ ] Reports: generate report -> appears in list
- [ ] Theme toggle -> all pages render correctly in both themes
- [ ] Offline mode -> banner shown, app still functional with cached data

### 12.4 Backend Unit Tests
- [x] Backend test file exists (`tests/test_api.py`)
- [ ] Test: create account
- [ ] Test: list accounts
- [ ] Test: create transaction
- [ ] Test: list transactions
- [ ] Test: transaction amount validation (positive only)
- [ ] Test: idempotency key deduplication
- [ ] Test: org isolation (different org_ids)
- [ ] Test: unauthorized access (no token)
- [ ] Test: invalid token
- [ ] Test: portfolio summary calculation
- [ ] Test: asset CRUD operations
- [ ] Test: transaction filter by date range
- [ ] Test: transaction filter by type
- [ ] Test: pagination
- [ ] Test: internal token validation
- [ ] Test: event emission

### 12.5 Backend Integration Tests
- [ ] Full CRUD flow: create account -> create transaction -> verify balances
- [ ] Double-entry bookkeeping: debit + credit balances correct
- [ ] Concurrent transaction handling
- [ ] Database migration up/down
- [ ] Gate auth integration test
- [ ] EventBus publish integration test

### 12.6 End-to-End Tests
- [ ] E2E framework configured (Playwright or Cypress)
- [ ] E2E: dashboard loads with data
- [ ] E2E: navigate to Assets page
- [ ] E2E: create new asset
- [ ] E2E: edit asset
- [ ] E2E: delete asset
- [ ] E2E: navigate to Transactions page
- [ ] E2E: filter transactions
- [ ] E2E: navigate to Reports page
- [ ] E2E: generate report
- [ ] E2E: dark mode toggle
- [ ] E2E: mobile responsive layout

### 12.7 Visual Regression Tests
- [ ] Dashboard: light mode screenshot
- [ ] Dashboard: dark mode screenshot
- [ ] Assets: light mode screenshot
- [ ] Assets: dark mode screenshot
- [ ] Transactions: light mode screenshot
- [ ] Transactions: dark mode screenshot
- [ ] Reports: light mode screenshot
- [ ] Reports: dark mode screenshot
- [ ] All pages at mobile, tablet, desktop breakpoints

### 12.8 Test Coverage
- [ ] Frontend unit test coverage > 80%
- [ ] Frontend component test coverage > 70%
- [ ] Backend unit test coverage > 80%
- [ ] CI pipeline runs all tests on PR
- [ ] Test results reported in PR comments

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] All TypeScript interfaces documented with JSDoc
- [ ] API service functions documented with JSDoc
- [ ] All custom hooks documented with JSDoc
- [ ] All utility functions documented with JSDoc
- [ ] Component prop documentation
- [ ] Complex business logic commented
- [ ] Backend: all API routes documented with docstrings
- [ ] Backend: model fields documented
- [ ] Backend: Pydantic schemas documented

### 13.2 Developer Documentation
- [ ] README.md: project overview
- [ ] README.md: tech stack
- [ ] README.md: setup instructions (frontend + backend)
- [ ] README.md: environment variables
- [ ] README.md: folder structure
- [ ] README.md: available scripts
- [ ] README.md: API documentation
- [ ] CONTRIBUTING.md: coding standards
- [ ] CONTRIBUTING.md: PR process
- [ ] CHANGELOG.md: version history
- [ ] Architecture decision records (ADRs)

### 13.3 API Documentation
- [ ] All API endpoints documented (method, URL, params, response)
- [ ] API error codes documented
- [ ] API authentication documented
- [ ] API rate limits documented
- [ ] OpenAPI/Swagger spec generated (FastAPI auto-generates)
- [ ] Postman/Insomnia collection exported

### 13.4 User Documentation
- [ ] Feature guide: dashboard overview
- [ ] Feature guide: asset management
- [ ] Feature guide: transactions
- [ ] Feature guide: reports
- [ ] Feature guide: budgeting
- [ ] Keyboard shortcuts reference
- [ ] FAQ document

---

## 14. Deployment & CI/CD

### 14.1 Frontend Build
- [ ] Production build succeeds (`vite build`)
- [ ] Build output optimized
- [ ] Source maps generated
- [ ] Environment variables validated at build time
- [ ] Cache busting via file hashing
- [ ] Asset size limits configured

### 14.2 Docker
- [x] Dockerfile exists at root
- [ ] Dockerfile: multi-stage build (frontend + backend)
- [ ] Dockerfile: Node build stage for frontend
- [ ] Dockerfile: Python stage for backend
- [ ] Dockerfile: Nginx serve stage for frontend assets
- [ ] Dockerfile: health check configured
- [ ] Docker compose entry
- [ ] Docker compose: port mapping (frontend 45010, backend 45013)
- [ ] Docker compose: volume mounts
- [ ] Docker compose: environment variables
- [ ] `.dockerignore` configured

### 14.3 CI Pipeline
- [ ] GitHub Actions workflow configured
- [ ] CI: install frontend dependencies
- [ ] CI: install backend dependencies
- [ ] CI: frontend lint check
- [ ] CI: frontend type check
- [ ] CI: frontend unit tests
- [ ] CI: frontend build
- [ ] CI: backend lint check (flake8/ruff)
- [ ] CI: backend type check (mypy)
- [ ] CI: backend unit tests (pytest)
- [ ] CI: E2E tests
- [ ] CI: security audit
- [ ] CI: bundle size check
- [ ] CI: deploy preview on PR

### 14.4 Deployment
- [ ] Staging environment configured
- [ ] Production environment configured
- [ ] Deployment script / pipeline
- [ ] Database migration on deploy
- [ ] Rollback procedure documented
- [ ] Zero-downtime deployment
- [ ] Health check endpoint (backend)
- [ ] Error monitoring (Sentry)
- [ ] Performance monitoring
- [ ] Log aggregation

### 14.5 Environment Management
- [x] `.env.example` exists (backend)
- [ ] Frontend: `.env.example` with all variables
- [ ] Frontend: `VITE_API_BASE`
- [ ] Frontend: `VITE_CAPITAL_BACKEND`
- [ ] Frontend: `VITE_GATE_URL`
- [ ] Backend: all env vars documented
- [ ] Secrets not committed to git
- [ ] `.gitignore` includes all env files

---

## 15. Backend

### 15.1 API Server (FastAPI)
- [x] FastAPI application initialized
- [x] Routes module with APIRouter
- [x] Internal router for service-to-service calls
- [x] CORS configured (needs verification for production)
- [ ] Request logging middleware
- [ ] Error handling middleware (structured error responses)
- [ ] Health check endpoint (`GET /health`)
- [ ] Metrics endpoint (`GET /metrics`)
- [ ] API versioning (`/api/v1/`)
- [ ] Rate limiting middleware
- [ ] Request ID middleware

### 15.2 Database (SQLAlchemy + Alembic)
- [x] SQLAlchemy models defined (Account, Transaction)
- [x] Alembic configured
- [x] Initial migration: accounts and transactions tables
- [x] Hardening migration: indexes and constraints
- [x] Account model: id, org_id, name, type, balance, metadata_json, timestamps
- [x] Transaction model: id, org_id, description, amount, debit/credit accounts, idempotency_key, timestamps
- [x] Indexes: org_id + type, org_id + transacted_at, org_id + idempotency_key (unique)
- [x] Constraint: amount > 0
- [ ] Asset model: separate from accounts (or mapped to account type)
- [ ] Budget model
- [ ] Budget line item model
- [ ] Invoice model
- [ ] Expense model
- [ ] Depreciation schedule model
- [ ] Audit log model
- [ ] Database connection pooling configured
- [ ] Database backup strategy documented

### 15.3 Auth (Gate Integration)
- [x] Gate auth module (`gate_auth.py`)
- [x] Actor class for request context
- [ ] Token validation middleware
- [ ] Org isolation in all queries
- [ ] Role-based authorization on endpoints
- [ ] Admin-only endpoint protection

### 15.4 API Endpoints
- [x] Account CRUD endpoints
- [x] Transaction CRUD endpoints
- [x] Internal asset sync endpoint
- [ ] Portfolio summary endpoint (aggregate calculations)
- [ ] Asset CRUD endpoints (frontend-facing, separate from accounts)
- [ ] Asset search endpoint
- [ ] Asset bulk operations endpoints
- [ ] Depreciation calculation endpoint
- [ ] Depreciation batch run endpoint
- [ ] Budget CRUD endpoints
- [ ] Budget vs actuals endpoint
- [ ] Compliance score endpoint
- [ ] Compliance issues endpoint
- [ ] Financial KPIs endpoint
- [ ] Report generation endpoint (portfolio)
- [ ] Report generation endpoint (depreciation)
- [ ] Report generation endpoint (compliance)
- [ ] Report generation endpoint (transactions)
- [ ] Report download endpoint (PDF)
- [ ] Report download endpoint (CSV/Excel)
- [ ] Export endpoints (assets CSV, transactions CSV)
- [ ] Import endpoint (assets CSV upload)

### 15.5 Business Logic
- [ ] Double-entry bookkeeping validation
- [ ] Balance calculation (sum of debits - sum of credits)
- [ ] Depreciation calculation (straight-line)
- [ ] Depreciation calculation (declining balance)
- [ ] Compliance score calculation logic
- [ ] Budget variance calculation
- [ ] Currency conversion (if multi-currency)
- [ ] Idempotency enforcement on transactions
- [ ] Transaction reversal logic

### 15.6 EventBus Integration
- [x] Event emission function (`_emit_finance_event`)
- [x] Event sink URL configurable
- [x] Internal token for event sink
- [ ] Publish: asset.created event
- [ ] Publish: asset.updated event
- [ ] Publish: asset.disposed event
- [ ] Publish: transaction.created event
- [ ] Publish: budget.overage event
- [ ] Publish: compliance.alert event
- [ ] Consume: device.detected from Secure (asset auto-creation)
- [ ] Consume: budget.request from Control Center
- [ ] Event schema validation
- [ ] Dead letter queue for failed events
- [ ] Event replay capability

### 15.7 Backend Testing
- [x] Test file exists (`tests/test_api.py`)
- [ ] Test database configuration (SQLite for tests)
- [ ] Test fixtures and factories
- [ ] Unit tests: account operations
- [ ] Unit tests: transaction operations
- [ ] Unit tests: balance calculations
- [ ] Unit tests: depreciation calculations
- [ ] Unit tests: compliance scoring
- [ ] Integration tests: full CRUD flows
- [ ] Integration tests: double-entry validation
- [ ] Integration tests: idempotency enforcement
- [ ] Integration tests: org isolation
- [ ] Integration tests: auth middleware
- [ ] Test coverage > 80%
- [ ] CI runs backend tests

### 15.8 Node Extension
- [x] Org middleware (`org-middleware.js`)
- [x] Tenant context (`tenant-context.js`)
- [x] Service test (`capitalhub-service.test.js`)
- [ ] Socket.IO real-time updates
- [ ] Event forwarding to frontend
- [ ] Error handling
- [ ] Reconnection logic
- [ ] Test coverage for node extension

### 15.9 Backend Data Integrity
- [ ] Double-entry bookkeeping: every transaction has debit + credit
- [ ] Transaction amount constraint: always positive
- [ ] Account balance auto-recalculation on transaction
- [ ] Idempotency key unique constraint enforced
- [ ] Cascading deletes: account deletion handles transactions
- [ ] Orphan prevention: transaction references valid accounts
- [ ] Org_id never null on any record
- [ ] Concurrent transaction handling (row-level locking)
- [ ] Database backup before destructive operations
- [ ] Data export for audit purposes
- [ ] Archival strategy for old transactions
- [ ] Soft delete for accounts (mark inactive, don't remove)
- [ ] Soft delete for transactions (reversals, not deletions)
- [ ] Audit log: who created/modified each record
- [ ] Audit log: timestamp of each modification
- [ ] Audit log: before/after values for changes

### 15.10 Backend API Error Handling
- [ ] Consistent error response format: `{ "detail": "...", "code": "..." }`
- [ ] 400 Bad Request: invalid input data
- [ ] 401 Unauthorized: missing or invalid token
- [ ] 403 Forbidden: insufficient permissions
- [ ] 404 Not Found: resource does not exist
- [ ] 409 Conflict: idempotency key conflict
- [ ] 422 Unprocessable Entity: validation error with field details
- [ ] 429 Too Many Requests: rate limit exceeded
- [ ] 500 Internal Server Error: unexpected failures
- [ ] Error logging with request context (request_id, org_id)
- [ ] Error monitoring integration (Sentry)
- [ ] Error response includes request_id for debugging
- [ ] Validation errors return field-level detail
- [ ] Database errors mapped to appropriate HTTP codes
- [ ] External service errors (Gate, EventBus) handled gracefully

### 15.11 Backend Caching
- [ ] Cache: portfolio summary (TTL 60s)
- [ ] Cache: asset list (invalidate on CRUD)
- [ ] Cache: transaction list (invalidate on CRUD)
- [ ] Cache: dashboard KPIs (TTL 30s)
- [ ] Cache: compliance score (TTL 300s)
- [ ] Cache strategy: Redis or in-memory
- [ ] Cache invalidation on write operations
- [ ] Cache key includes org_id (tenant isolation)
- [ ] Cache headers on API responses (ETag, Cache-Control)

### 15.12 Backend Background Tasks
- [ ] Depreciation batch run (scheduled monthly)
- [ ] SLA/compliance score recalculation (scheduled daily)
- [ ] Stale asset alerts (assets not reviewed in 12 months)
- [ ] Report generation (async background task)
- [ ] Event publishing (async, non-blocking)
- [ ] Cleanup: expired export files
- [ ] Cleanup: orphaned attachments
- [ ] Health check: database connectivity
- [ ] Health check: Redis connectivity (if used)
- [ ] Health check: Gate service reachability

---

## Summary

| Section | Total Items | Done | Remaining |
|---------|------------|------|-----------|
| 1. Project Setup | 56 | 27 | 29 |
| 2. Design System | 196 | 4 | 192 |
| 3. Dark Mode | 128 | 2 | 126 |
| 4. Core Features | 267 | 0 | 267 |
| 5. API Integration | 60 | 14 | 46 |
| 6. State Management | 42 | 0 | 42 |
| 7. Performance | 38 | 6 | 32 |
| 8. Accessibility | 54 | 0 | 54 |
| 9. Mobile & Responsive | 28 | 4 | 24 |
| 10. Internationalization | 24 | 0 | 24 |
| 11. Security | 27 | 3 | 24 |
| 12. Testing | 74 | 1 | 73 |
| 13. Documentation | 24 | 0 | 24 |
| 14. Deployment & CI/CD | 32 | 2 | 30 |
| 15. Backend | 68 | 18 | 50 |
| **TOTAL** | **1118** | **81** | **1037** |
