# 13 — Wallet (Financial Management) — Comprehensive Checklist

> **App:** RM Wallet — Financial Management (Secrets/Credentials Vault + Personal/Team Finance)
> **Stack:** Vanilla HTML/JS frontend (`Wallet/frontend/index.html`, 1266 lines) + Python/FastAPI backend (`Wallet/backend/`)
> **Design system:** orbit-tokens.css, orbit-ui.css, orbit-bar.js (already integrated in HTML)
> **Backend models:** Vault, Secret, AuditLog, SharedInfo — encrypted secrets management
> **Backend routes:** CRUD for secrets with Fernet encryption, reveal with decryption
> **Auth:** Header-based (X-Org-Id) + Gate auth (gate_auth.py exists)
> **Status:** Frontend exists as vanilla HTML SPA; backend is database-backed with encrypted secret storage
> **Last synced with PER_APP_CHECKLIST.md:** 2026-04-06
>
> Legend: `[x]` = done · `[ ]` = todo · `[~]` = in progress · `[-]` = N/A / skipped

---

## 1. Project Setup & Configuration

### 1.1 Current Vanilla HTML/JS Setup
- [x] `Wallet/frontend/index.html` — single-file SPA (1266 lines)
- [x] `Wallet/frontend/public/orbit-ui/orbit-tokens.css` — design tokens
- [x] `Wallet/frontend/public/orbit-ui/orbit-ui.css` — component styles
- [x] `Wallet/frontend/public/orbit-ui/orbit-bar.js` — top navigation bar
- [x] `Wallet/frontend/public/orbit-ui/orbit-theme-init.js` — dark mode bootstrap
- [x] `Wallet/frontend/public/orbit-ui/orbit-tailwind-v4.css` — Tailwind v4 theme
- [x] `Wallet/frontend/public/fonts/RMForma-Regular.woff2` — brand font
- [x] `Wallet/frontend/public/fonts/RMForma-SemiBold.woff2` — brand font
- [x] `Wallet/frontend/public/fonts/RMForma-Bold.woff2` — brand font
- [x] `Wallet/frontend/public/fonts/RM-Samplet-Regular.ttf` — brand font
- [ ] Add `manifest.json` for PWA support
- [ ] Add `favicon.ico` and app icons (16, 32, 192, 512)
- [ ] Add Open Graph / social sharing meta tags
- [ ] Add `robots.txt`
- [ ] Configure Content Security Policy headers
- [ ] Add `apple-touch-icon.png`
- [ ] Add service worker registration for offline support

### 1.2 Backend Setup
- [x] `Wallet/backend/app/main.py` — FastAPI app
- [x] `Wallet/backend/app/routes.py` — API router (secrets CRUD + reveal)
- [x] `Wallet/backend/app/models.py` — SQLAlchemy models (Vault, Secret, AuditLog, SharedInfo)
- [x] `Wallet/backend/app/database.py` — DB session factory
- [x] `Wallet/backend/app/gate_auth.py` — Gate authentication module
- [x] `Wallet/backend/alembic.ini` — Alembic configuration
- [x] `Wallet/backend/alembic/versions/1c7e78015c1e_init_wallet.py` — initial migration
- [x] `Wallet/backend/alembic/versions/7f02f6d6f91f_wallet_postgres_hardening.py` — hardening migration
- [x] `Wallet/backend/requirements.txt` — Python dependencies
- [x] `Wallet/backend/.env.example` — environment variable template
- [x] `Wallet/backend/tests/test_api.py` — API tests
- [x] `Wallet/backend/app/wallet_shared_info.json` — shared info seed data
- [ ] Add `pyproject.toml` for modern Python packaging
- [ ] Add `Makefile` or `justfile` for common commands
- [ ] Add `.flake8` / `ruff.toml` linting configuration
- [ ] Add `mypy.ini` for type checking
- [ ] Add `pre-commit` hooks configuration
- [ ] Add `docker-compose.yml` for local development
- [ ] Add `docker-compose.test.yml` for CI testing
- [ ] Add health check endpoint with DB connectivity check
- [ ] Add security headers middleware

### 1.3 Docker & Deployment
- [x] `Wallet/Dockerfile` — container image
- [x] `Wallet/start-backend.sh` — backend start script
- [x] `Wallet/start-frontend.sh` — frontend start script
- [ ] Multi-stage Docker build (build frontend + serve from backend)
- [ ] Docker health check in Dockerfile
- [ ] `.dockerignore` to exclude unnecessary files
- [ ] Docker Compose for full local stack (app + DB + Redis)
- [ ] Production Dockerfile with non-root user
- [ ] Container image size optimization (< 200MB)
- [ ] Environment-specific Docker Compose overrides

### 1.4 React Migration Decision Path
- [ ] **DECISION:** Migrate to React 19 + TypeScript or enhance vanilla JS?
- [ ] If React: Create `Wallet/frontend-react/` Vite + React 19 + TypeScript project
- [ ] If React: `package.json` with `@orbit-ui/react`, Tailwind, React Router, Zustand, Recharts, Lucide React
- [ ] If React: `tailwind.config.js` with orbit preset
- [ ] If React: `vite.config.ts` with proxy to backend API
- [ ] If React: `tsconfig.json` with strict mode
- [ ] If React: `index.html` with anti-FOUC + orbit-ui links
- [ ] If React: `main.tsx` with `ThemeProvider` wrapper
- [ ] If React: Gate OAuth PKCE auth flow
- [ ] If React: ESLint + Prettier configuration
- [ ] If React: Vitest + React Testing Library setup
- [ ] If React: Storybook for component development
- [ ] If React: Security — all financial data over HTTPS only, strict CSP headers
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
- [ ] Replace `--bg: #071026` with `var(--orbit-bg)` or equivalent token
- [ ] Replace `--bg-soft: #0d1734` with `var(--orbit-bg-soft)` token
- [ ] Replace `--card: #111c3d` with `var(--orbit-surface)` token
- [ ] Replace `--card-alt: #17264c` with `var(--orbit-surface-alt)` token
- [ ] Replace `--text: #e7edff` with `var(--orbit-text)` token
- [ ] Replace `--muted: #98a9d2` with `var(--orbit-text-muted)` token
- [ ] Replace `--border: #2a3f6a` with `var(--orbit-border)` token
- [ ] Replace `--brand-a: #2563eb` with `var(--orbit-primary)` token
- [ ] Replace `--brand-b: #7c3aed` with `var(--orbit-secondary)` token
- [ ] Replace `--ok: #22c55e` with `var(--orbit-success)` token
- [ ] Replace `--warn: #f59e0b` with `var(--orbit-warning)` token
- [ ] Replace `--danger: #ef4444` with `var(--orbit-danger)` token
- [ ] Remove all hardcoded hex colors from inline `<style>`
- [ ] Audit every `background`, `color`, `border-color` for hardcoded values
- [ ] Replace hardcoded `#334f84`, `#162751` stat card colors with tokens
- [ ] Replace hardcoded `#375898`, `#15234b` active nav colors with tokens
- [ ] Replace hardcoded `#3b578e` side-note border with token
- [ ] Replace hardcoded `#233660` table border with token
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
- [ ] Replace hardcoded `box-shadow: 0 10px 30px rgba(37, 99, 235, 0.45)` with orbit shadow
- [ ] Replace `backdrop-filter: blur(14px)` with orbit glass token
- [ ] Replace hardcoded focus ring styles with orbit focus token

### 2.5 Motion & Animation Tokens
- [ ] Add orbit transition tokens for hover states
- [ ] Add orbit transition tokens for modal open/close
- [ ] Add orbit transition tokens for sidebar collapse
- [ ] Add orbit transition tokens for tab switching
- [ ] Add loading skeleton animations using orbit motion tokens
- [ ] Add orbit transition tokens for secret reveal/hide animation
- [ ] Add orbit transition tokens for transaction row highlights

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
- [ ] Replace custom password input (reveal toggle) with orbit PasswordInput

### 2.7 orbit-bar Integration
- [x] `orbit-bar.js` loaded with `defer`
- [ ] Verify orbit-bar renders correctly in all views
- [ ] Verify orbit-bar app switcher shows Wallet as active
- [ ] Verify orbit-bar theme toggle syncs with Wallet theme
- [ ] Verify orbit-bar notifications integration
- [ ] Verify orbit-bar user menu integration

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
- [ ] Secrets/Credentials list view — dark mode colors
- [ ] Secret detail/reveal view — dark mode colors
- [ ] Vault list view — dark mode colors
- [ ] Vault detail view — dark mode colors
- [ ] Transaction tracking view — dark mode colors
- [ ] Account management view — dark mode colors
- [ ] Budget overview view — dark mode colors
- [ ] Spending categories view — dark mode colors
- [ ] Income tracking view — dark mode colors
- [ ] Bill reminders view — dark mode colors
- [ ] Financial goals view — dark mode colors
- [ ] Reports/Analytics view — dark mode colors
- [ ] Receipt scanning view — dark mode colors
- [ ] Investment tracking view — dark mode colors
- [ ] Tax tracking view — dark mode colors
- [ ] Settings view — dark mode colors
- [ ] Audit log view — dark mode colors
- [ ] Export view — dark mode colors
- [ ] Shared info view — dark mode colors

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
- [ ] Password/secret reveal input — dark mode
- [ ] Loading spinners — dark mode
- [ ] Empty states — dark mode
- [ ] Error states — dark mode
- [ ] Skeleton loaders — dark mode
- [ ] Scrollbar styling — dark mode
- [ ] Charts/graphs — dark mode colors
- [ ] Progress bars — dark mode
- [ ] Currency display — dark mode
- [ ] Date pickers — dark mode
- [ ] Number inputs — dark mode
- [ ] Toggle switches — dark mode
- [ ] Confirmation dialogs — dark mode

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
- [ ] Financial data remains readable in light mode
- [ ] Positive/negative value colors work in light mode

---

## 4. Core Features (Exhaustive)

### 4.1 Secrets / Credentials Vault (Existing Backend)
- [x] Secret CRUD (backend: create, list, delete)
- [x] Secret encryption with Fernet (AES-128-CBC)
- [x] Secret reveal endpoint with decryption
- [x] Secret model: name, description, encrypted_value, iv_material
- [x] Secret model: secret_type, project, tags, shares
- [x] Secret model: rotation_interval_days, last_rotated_at, expires_at
- [x] Secret model: owner_user_id, org_id
- [x] Org-scoped secret isolation (X-Org-Id header)
- [ ] Secret update endpoint (change value, re-encrypt)
- [ ] Secret rotation flow (generate new value, archive old)
- [ ] Secret rotation reminders/notifications
- [ ] Secret expiry warnings
- [ ] Secret sharing (add/remove share recipients)
- [ ] Secret sharing access log
- [ ] Secret search by name/project/tags
- [ ] Secret filter by type (api_key, password, token, etc.)
- [ ] Secret filter by project
- [ ] Secret bulk import (CSV/JSON)
- [ ] Secret bulk export (encrypted archive)
- [ ] Secret copy-to-clipboard with auto-clear timer
- [ ] Secret reveal audit logging
- [ ] Secret access history per secret
- [ ] Secret version history (previous values, encrypted)
- [ ] Secret tags management
- [ ] Secret notes/description editing
- [ ] Secret type categorization (api_key, password, ssh_key, certificate, etc.)

### 4.2 Vault Management (Existing Backend)
- [x] Vault model: name, description, owner_team, org_id
- [x] Vault-Secret relationship (vault_id FK)
- [ ] Vault CRUD endpoints
- [ ] Vault list view
- [ ] Vault detail view (secrets within vault)
- [ ] Vault create form
- [ ] Vault update form
- [ ] Vault delete with cascade warning
- [ ] Vault sharing with teams
- [ ] Vault access control (who can view/edit)
- [ ] Vault default vault for new secrets
- [ ] Vault search/filter
- [ ] Vault icon/color customization

### 4.3 Shared Info (Existing Backend)
- [x] SharedInfo model: category, title, value, environment, owner_team, notes, tags, source
- [x] Org-scoped and global (*) shared info
- [x] `wallet_shared_info.json` seed data
- [ ] Shared info list view
- [ ] Shared info create form
- [ ] Shared info update form
- [ ] Shared info delete
- [ ] Shared info filter by category
- [ ] Shared info filter by environment (dev, staging, prod)
- [ ] Shared info filter by team
- [ ] Shared info search
- [ ] Shared info import/export

### 4.4 Audit Log (Existing Backend)
- [x] AuditLog model: user_id, role, action, resource_type, resource_id, ip_address, metadata_json
- [x] Org-scoped audit isolation
- [ ] Audit log list view with filtering
- [ ] Audit log search by action
- [ ] Audit log search by user
- [ ] Audit log search by resource
- [ ] Audit log search by date range
- [ ] Audit log search by IP address
- [ ] Audit log detail view
- [ ] Audit log export (CSV/JSON)
- [ ] Audit log retention policy
- [ ] Audit log tamper detection

### 4.5 Transaction Tracking (Financial Feature — To Build)
- [ ] Transaction list view
- [ ] Transaction create form (manual entry)
- [ ] Transaction fields: date, description, amount, currency, category, account
- [ ] Transaction type: income, expense, transfer
- [ ] Transaction status: cleared, pending, reconciled
- [ ] Transaction search/filter
- [ ] Transaction filter by date range
- [ ] Transaction filter by category
- [ ] Transaction filter by account
- [ ] Transaction filter by amount range
- [ ] Transaction filter by type (income/expense/transfer)
- [ ] Transaction sort by date, amount, category
- [ ] Transaction edit
- [ ] Transaction delete with confirmation
- [ ] Transaction bulk categorization
- [ ] Transaction bulk delete
- [ ] Transaction split (one transaction into multiple categories)
- [ ] Transaction recurring setup
- [ ] Transaction notes/memo field
- [ ] Transaction attachment (receipt photo)
- [ ] Transaction location/merchant tagging
- [ ] Transaction import from CSV
- [ ] Transaction import from bank (OFX/QFX)
- [ ] Transaction import from credit card statement
- [ ] Transaction export CSV
- [ ] Transaction export PDF statement
- [ ] Transaction duplicate detection
- [ ] Transaction auto-categorization (rule-based)
- [ ] Transaction auto-categorization (AI-based)

### 4.6 Account Management (Financial Feature — To Build)
- [ ] Account list view (all financial accounts)
- [ ] Account types: bank checking, bank savings, credit card, crypto wallet, cash, investment
- [ ] Account create form
- [ ] Account detail view
- [ ] Account balance display
- [ ] Account balance history chart
- [ ] Account currency setting
- [ ] Account institution/bank name
- [ ] Account last-4 digits for identification
- [ ] Account color/icon customization
- [ ] Account archive (hide without deleting)
- [ ] Account delete with transaction handling
- [ ] Account reconciliation tool
- [ ] Account balance auto-sync (API integration)
- [ ] Account net worth calculation (sum all accounts)
- [ ] Account interest rate tracking (savings, credit)
- [ ] Account credit limit tracking (credit cards)
- [ ] Account payment due date (credit cards, loans)

### 4.7 Budget Management (Financial Feature — To Build)
- [ ] Budget overview dashboard
- [ ] Budget create form (name, amount, period, categories)
- [ ] Budget period: weekly, bi-weekly, monthly, quarterly, yearly
- [ ] Budget by category (food, transport, entertainment, etc.)
- [ ] Budget by account
- [ ] Budget progress bar (spent vs budget)
- [ ] Budget remaining amount display
- [ ] Budget daily spending average
- [ ] Budget projected end-of-period total
- [ ] Budget vs actual comparison chart
- [ ] Budget trend over time (month-over-month)
- [ ] Budget rollover (carry unused to next period)
- [ ] Budget alerts: approaching limit (80%, 90%, 100%)
- [ ] Budget alerts: over budget notification
- [ ] Budget edit
- [ ] Budget delete
- [ ] Budget templates (common budget presets)
- [ ] Budget sharing with team members
- [ ] Budget approval workflow (team budgets)
- [ ] Zero-based budget mode (every dollar assigned)
- [ ] Envelope budgeting mode

### 4.8 Spending Categories (Financial Feature — To Build)
- [ ] Category list view
- [ ] Default categories: Food & Dining, Transportation, Housing, Utilities, Entertainment, Shopping, Health, Education, Travel, Insurance, Subscriptions, Gifts, Personal Care, Savings, Investments
- [ ] Custom category creation
- [ ] Category edit (name, icon, color)
- [ ] Category delete (reassign transactions)
- [ ] Category hierarchy (parent/child categories)
- [ ] Category spending summary (total per category)
- [ ] Category spending chart (pie/donut)
- [ ] Category spending trend (line chart over time)
- [ ] Category auto-assign rules (merchant -> category mapping)
- [ ] Category budget assignment
- [ ] Category icon library
- [ ] Category merge tool

### 4.9 Income Tracking (Financial Feature — To Build)
- [ ] Income list view
- [ ] Income sources: salary, freelance, investments, rental, side business, other
- [ ] Income create form
- [ ] Income recurring setup (weekly, bi-weekly, monthly)
- [ ] Income vs expense summary
- [ ] Income trend chart
- [ ] Income by source breakdown
- [ ] Income tax withholding tracking
- [ ] Income gross vs net tracking
- [ ] Income year-over-year comparison
- [ ] Income projections

### 4.10 Bill Reminders (Financial Feature — To Build)
- [ ] Bill list view
- [ ] Bill create form (name, amount, due date, frequency, account)
- [ ] Bill frequency: one-time, weekly, monthly, quarterly, annually
- [ ] Bill due date reminders (1 day, 3 days, 1 week before)
- [ ] Bill reminder delivery: in-app, email, push notification
- [ ] Bill paid/unpaid status toggle
- [ ] Bill auto-pay indicator
- [ ] Bill payment history
- [ ] Bill amount change tracking
- [ ] Bill late payment tracking
- [ ] Bill calendar view
- [ ] Bill upcoming this week/month summary
- [ ] Bill total monthly recurring expenses
- [ ] Bill categories

### 4.11 Financial Goals (Financial Feature — To Build)
- [ ] Goal list view
- [ ] Goal create form (name, target amount, deadline, category)
- [ ] Goal types: emergency fund, vacation, down payment, debt payoff, retirement, custom
- [ ] Goal progress bar
- [ ] Goal current amount tracking
- [ ] Goal contribution schedule (auto-save)
- [ ] Goal milestone markers
- [ ] Goal projected completion date
- [ ] Goal priority ranking
- [ ] Goal celebrate completion (animation/badge)
- [ ] Goal edit
- [ ] Goal delete/archive
- [ ] Goal monthly contribution recommendation
- [ ] Goal linked to specific account
- [ ] Goal sharing with partner/team

### 4.12 Reports & Analytics (Financial Feature — To Build)
- [ ] Dashboard overview: net worth, monthly spending, monthly income, savings rate
- [ ] Spending by category report (pie chart)
- [ ] Spending by merchant report
- [ ] Spending trend report (line chart, monthly)
- [ ] Income vs expense report (bar chart)
- [ ] Net worth over time report (area chart)
- [ ] Cash flow report (waterfall chart)
- [ ] Budget vs actual report (comparison bars)
- [ ] Account balance history report
- [ ] Monthly financial summary report
- [ ] Yearly financial summary report
- [ ] Custom date range reports
- [ ] Report export to PDF
- [ ] Report export to CSV
- [ ] Report email delivery (scheduled)
- [ ] Report comparison (month vs month, year vs year)
- [ ] Financial health score (composite metric)
- [ ] Savings rate calculation
- [ ] Debt-to-income ratio
- [ ] Expense ratio by category

### 4.13 Receipt Scanning (Financial Feature — To Build)
- [ ] Receipt photo capture (camera)
- [ ] Receipt image upload
- [ ] Receipt OCR processing (extract amount, date, merchant)
- [ ] Receipt auto-create transaction from OCR
- [ ] Receipt manual review/correction
- [ ] Receipt attachment to existing transaction
- [ ] Receipt storage (image persistence)
- [ ] Receipt gallery view
- [ ] Receipt search by merchant/date
- [ ] Receipt bulk scanning mode

### 4.14 Multi-Currency Support (Financial Feature — To Build)
- [ ] Currency list (ISO 4217 codes)
- [ ] Default/home currency setting
- [ ] Transaction currency field
- [ ] Account currency field
- [ ] Exchange rate lookup (real-time API)
- [ ] Historical exchange rates
- [ ] Currency conversion calculator
- [ ] Multi-currency portfolio view (converted to home currency)
- [ ] Currency formatting per locale
- [ ] Forex gain/loss tracking
- [ ] Currency symbols display
- [ ] Cryptocurrency support (BTC, ETH, etc.)
- [ ] Cryptocurrency price feeds

### 4.15 Investment Tracking (Financial Feature — To Build)
- [ ] Portfolio overview: total value, 24h change, allocation chart
- [ ] Asset list: cryptocurrency + traditional holdings
- [ ] Holdings: name, amount, value, 24h %, overall %
- [ ] Price chart: interactive line chart (1D/1W/1M/3M/1Y)
- [ ] Transaction history: buy/sell/transfer/receive log
- [ ] P&L tracking: cost basis vs. current value
- [ ] Portfolio rebalancing calculator
- [ ] Asset allocation donut chart
- [ ] Performance chart vs. benchmark (BTC, S&P500)
- [ ] Risk metrics: Sharpe ratio, max drawdown
- [ ] Tax lot tracking (FIFO / LIFO calculation)
- [ ] Realized gains/losses summary
- [ ] Dividend tracking
- [ ] Stock split handling
- [ ] Investment account types: brokerage, IRA, 401k, crypto exchange
- [ ] Import transactions from exchange CSV (Coinbase, Binance, Robinhood)

### 4.16 Tax Tracking (Financial Feature — To Build)
- [ ] Tax year overview
- [ ] Income summary by source
- [ ] Deductible expenses tracking
- [ ] Capital gains/losses summary
- [ ] Tax bracket estimation
- [ ] Estimated tax liability
- [ ] Tax payment tracking (quarterly estimates)
- [ ] Tax document storage (W-2, 1099, etc.)
- [ ] Tax export for CPA/accountant
- [ ] Tax category tagging on transactions
- [ ] Charitable donation tracking
- [ ] Business expense tracking
- [ ] Mileage tracking (business use)
- [ ] Home office deduction calculator
- [ ] Tax-loss harvesting suggestions

### 4.17 Recurring Transactions (Financial Feature — To Build)
- [ ] Recurring transaction list view
- [ ] Recurring transaction create form
- [ ] Frequency: daily, weekly, bi-weekly, monthly, quarterly, annually
- [ ] Auto-post on schedule
- [ ] Skip/defer individual occurrence
- [ ] Recurring transaction edit (future only or all)
- [ ] Recurring transaction delete/cancel
- [ ] Recurring transaction amount change tracking
- [ ] Subscription detection (auto-identify recurring charges)
- [ ] Subscription cost summary
- [ ] Subscription cancellation reminders

### 4.18 Payment Methods (Financial Feature — To Build)
- [ ] Payment method list
- [ ] Payment method types: debit card, credit card, bank transfer, cash, digital wallet
- [ ] Payment method add/edit form
- [ ] Payment method default setting
- [ ] Payment method last-4 digits display
- [ ] Payment method expiry tracking
- [ ] Payment method linked account
- [ ] Payment method usage statistics

### 4.19 Credit Score Tracking (Financial Feature — To Build)
- [ ] Credit score display
- [ ] Credit score history chart
- [ ] Credit score factors breakdown
- [ ] Credit score alerts (significant changes)
- [ ] Credit report summary
- [ ] Credit utilization tracking
- [ ] Credit account list
- [ ] Credit score improvement tips

### 4.20 Export & Integration (Financial Feature — To Build)
- [ ] Export transactions to CSV
- [ ] Export transactions to PDF
- [ ] Export transactions to OFX/QFX
- [ ] Export budget report to PDF
- [ ] Export tax summary to PDF
- [ ] Integration with accounting software (QuickBooks, Xero)
- [ ] Integration with tax software (TurboTax)
- [ ] API access for external tools
- [ ] Webhook notifications for transactions

---

## 5. API Integration

### 5.1 Backend API Endpoints (Existing)
- [x] `GET /api/wallet/` — list secrets
- [x] `POST /api/wallet/` — create secret (with encryption)
- [x] `GET /api/wallet/{secret_id}/reveal` — reveal secret (with decryption)
- [x] `DELETE /api/wallet/{secret_id}` — delete secret
- [ ] `PATCH /api/wallet/{secret_id}` — update secret
- [ ] `GET /api/wallet/vaults` — list vaults
- [ ] `POST /api/wallet/vaults` — create vault
- [ ] `PATCH /api/wallet/vaults/{id}` — update vault
- [ ] `DELETE /api/wallet/vaults/{id}` — delete vault
- [ ] `GET /api/wallet/shared-info` — list shared info
- [ ] `POST /api/wallet/shared-info` — create shared info
- [ ] `GET /api/wallet/audit` — list audit log
- [ ] `GET /health` — health check

### 5.2 Financial API Endpoints (To Build)
- [ ] `GET /api/wallet/transactions` — list transactions
- [ ] `POST /api/wallet/transactions` — create transaction
- [ ] `PATCH /api/wallet/transactions/{id}` — update transaction
- [ ] `DELETE /api/wallet/transactions/{id}` — delete transaction
- [ ] `GET /api/wallet/accounts` — list financial accounts
- [ ] `POST /api/wallet/accounts` — create account
- [ ] `PATCH /api/wallet/accounts/{id}` — update account
- [ ] `DELETE /api/wallet/accounts/{id}` — delete account
- [ ] `GET /api/wallet/budgets` — list budgets
- [ ] `POST /api/wallet/budgets` — create budget
- [ ] `PATCH /api/wallet/budgets/{id}` — update budget
- [ ] `DELETE /api/wallet/budgets/{id}` — delete budget
- [ ] `GET /api/wallet/categories` — list categories
- [ ] `POST /api/wallet/categories` — create category
- [ ] `GET /api/wallet/bills` — list bills
- [ ] `POST /api/wallet/bills` — create bill
- [ ] `GET /api/wallet/goals` — list goals
- [ ] `POST /api/wallet/goals` — create goal
- [ ] `GET /api/wallet/reports/spending` — spending report
- [ ] `GET /api/wallet/reports/income` — income report
- [ ] `GET /api/wallet/reports/net-worth` — net worth report
- [ ] `GET /api/wallet/reports/cash-flow` — cash flow report
- [ ] `POST /api/wallet/receipts/scan` — OCR receipt scan
- [ ] `GET /api/wallet/recurring` — list recurring transactions
- [ ] `POST /api/wallet/export` — export data

### 5.3 Frontend-Backend API Wiring
- [ ] Wire secret list to `GET /api/wallet/`
- [ ] Wire secret create to `POST /api/wallet/`
- [ ] Wire secret reveal to `GET /api/wallet/{id}/reveal`
- [ ] Wire secret delete to `DELETE /api/wallet/{id}`
- [ ] Wire all financial endpoints as they are built
- [ ] Add API error handling with user-friendly messages
- [ ] Add API retry logic for transient failures
- [ ] Add API request timeout handling
- [ ] Add API response caching where appropriate

### 5.4 External API Integrations
- [ ] Bank data aggregation API (Plaid, Yodlee)
- [ ] Exchange rate API (Open Exchange Rates, Fixer.io)
- [ ] Cryptocurrency price API (CoinGecko, CoinMarketCap)
- [ ] Stock market data API (Alpha Vantage, Yahoo Finance)
- [ ] OCR API for receipt scanning (Tesseract, Google Vision)
- [ ] Credit score API
- [ ] Tax calculation API

### 5.5 Authentication & Authorization
- [x] Org-scoped data isolation (X-Org-Id header)
- [x] Gate auth module exists (gate_auth.py)
- [ ] Frontend token storage (HttpOnly cookie preferred)
- [ ] Frontend token refresh flow
- [ ] Frontend auth state management
- [ ] Frontend login redirect to Gate
- [ ] Frontend logout flow
- [ ] Frontend session timeout handling
- [ ] RBAC enforcement in UI
- [ ] Financial data access audit logging
- [ ] Two-factor authentication for sensitive operations
- [ ] Re-authentication for secret reveals
- [ ] Session timeout for financial views (shorter than standard)

---

## 6. State Management

### 6.1 Current State (Vanilla JS)
- [ ] Audit current state management approach in index.html
- [ ] Identify all global state variables
- [ ] Identify all DOM manipulation patterns
- [ ] Identify all event listener registrations

### 6.2 State Architecture (if React migration)
- [ ] Zustand store for secrets state
- [ ] Zustand store for vaults state
- [ ] Zustand store for shared info state
- [ ] Zustand store for transactions state
- [ ] Zustand store for accounts state
- [ ] Zustand store for budgets state
- [ ] Zustand store for categories state
- [ ] Zustand store for bills state
- [ ] Zustand store for goals state
- [ ] Zustand store for reports state
- [ ] Zustand store for user/auth state
- [ ] Zustand store for UI state (sidebar, active tab, etc.)
- [ ] Zustand store for notification state
- [ ] Zustand middleware for localStorage persistence
- [ ] React Query / TanStack Query for server state
- [ ] Optimistic updates for mutations
- [ ] Cache invalidation strategy
- [ ] Sensitive data: clear from state on logout/timeout

### 6.3 State Architecture (if vanilla JS enhancement)
- [ ] Create event-driven state management (pub/sub)
- [ ] Centralized state store object
- [ ] State change listeners for DOM updates
- [ ] LocalStorage persistence for preferences (NOT financial data)
- [ ] SessionStorage for session-specific state
- [ ] Clear sensitive state on tab close

---

## 7. Performance

### 7.1 Frontend Performance
- [ ] Measure initial page load time (target < 2s)
- [ ] Measure Time to First Byte (TTFB)
- [ ] Measure First Contentful Paint (FCP)
- [ ] Measure Largest Contentful Paint (LCP < 2.5s)
- [ ] Measure Cumulative Layout Shift (CLS < 0.1)
- [ ] Measure Interaction to Next Paint (INP < 200ms)
- [ ] Bundle size audit (if build step added)
- [ ] Code splitting / lazy loading for views
- [ ] Chart library lazy loading (only load when needed)
- [ ] Image optimization (receipt thumbnails)
- [ ] Font loading optimization (font-display: swap)
- [ ] CSS optimization (remove unused CSS)
- [ ] JavaScript optimization (minify, tree-shake)
- [ ] Gzip/Brotli compression
- [ ] CDN for static assets
- [ ] Browser caching headers
- [ ] Preload critical resources
- [ ] Debounce search/filter inputs
- [ ] Virtualize long transaction lists
- [ ] Skeleton loading screens
- [ ] Progressive chart rendering

### 7.2 Backend Performance
- [ ] Database query optimization
- [ ] Database connection pooling
- [ ] Database index analysis (especially on transaction queries)
- [ ] API response time monitoring (target < 200ms p95)
- [ ] API pagination for list endpoints
- [ ] API response compression
- [ ] Redis caching for exchange rates, prices
- [ ] Background task processing for reports, OCR
- [ ] Rate limiting per endpoint
- [ ] Database query timeout limits
- [ ] Slow query logging
- [ ] Batch operations for bulk imports

### 7.3 Financial Data Performance
- [ ] Transaction query optimization for large datasets (100K+ rows)
- [ ] Report generation caching
- [ ] Incremental report updates (not full recalculation)
- [ ] Date-range indexed queries
- [ ] Aggregate queries with materialized views
- [ ] Time-series data optimization for charts

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
- [ ] ARIA live regions for dynamic content (balance updates, transaction notifications)
- [ ] ARIA expanded/collapsed states
- [ ] Color contrast ratio >= 4.5:1 for text
- [ ] Color contrast ratio >= 3:1 for UI components
- [ ] Information not conveyed by color alone (green=income, red=expense must also have icons/text)
- [ ] Form inputs have associated labels
- [ ] Form error messages linked to inputs
- [ ] Required fields indicated
- [ ] Error states announced to screen readers
- [ ] Currency values read correctly by screen readers ($1,234.56 as "one thousand two hundred thirty four dollars and fifty six cents")
- [ ] Chart data available as accessible table alternative

### 8.2 Screen Reader Testing
- [ ] Test with NVDA on Windows
- [ ] Test with VoiceOver on macOS
- [ ] Test with JAWS on Windows
- [ ] Test with TalkBack on Android
- [ ] Test with VoiceOver on iOS/iPadOS
- [ ] Verify financial data tables read correctly
- [ ] Verify transaction amounts announced with currency
- [ ] Verify positive/negative amounts distinguished

### 8.3 Motion & Visual Preferences
- [ ] Respect `prefers-reduced-motion`
- [ ] Respect `prefers-contrast`
- [ ] Respect `prefers-color-scheme`
- [ ] No auto-playing animations

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
- [ ] Charts: responsive sizing, touch-optimized tooltips
- [ ] Transaction list: card layout on mobile
- [ ] Budget bars: full-width on mobile

### 9.3 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] Swipe to delete transactions
- [ ] Swipe to categorize transactions
- [ ] Pull to refresh
- [ ] Long press for context menu
- [ ] Pinch to zoom on charts
- [ ] Touch-friendly date picker
- [ ] Touch-friendly number input (calculator-style)

### 9.4 Mobile-Specific Features
- [ ] PWA installable (Add to Home Screen)
- [ ] Offline indicator banner
- [ ] Camera access for receipt scanning
- [ ] Quick-add transaction floating action button
- [ ] Mobile-optimized navigation (bottom tabs)
- [ ] Biometric auth for secret reveals (FaceID/TouchID)
- [ ] Viewport height handling (100dvh)
- [ ] Safe area insets
- [ ] Input zoom prevention on iOS

---

## 10. Internationalization (i18n)

### 10.1 Infrastructure
- [ ] i18n library selection
- [ ] Translation file structure
- [ ] Default language: English (en)
- [ ] Language detection from browser/user preference
- [ ] Language switcher UI
- [ ] Language persistence

### 10.2 String Extraction
- [ ] Extract all UI strings from index.html
- [ ] Extract button labels
- [ ] Extract navigation labels
- [ ] Extract form labels and placeholders
- [ ] Extract error messages
- [ ] Extract success messages
- [ ] Extract empty state messages
- [ ] Extract financial terms
- [ ] Extract category names (default categories)

### 10.3 Locale Support
- [ ] English (en) — complete
- [ ] Spanish (es) — translation
- [ ] French (fr) — translation
- [ ] German (de) — translation
- [ ] Japanese (ja) — translation
- [ ] Chinese Simplified (zh-CN) — translation
- [ ] Arabic (ar) — RTL support
- [ ] Hindi (hi) — translation
- [ ] Portuguese (pt-BR) — translation

### 10.4 Financial Formatting
- [ ] Currency formatting per locale (Intl.NumberFormat)
- [ ] Date formatting per locale
- [ ] Number formatting per locale (decimal separators)
- [ ] Percentage formatting
- [ ] Currency symbol placement (before/after amount)
- [ ] Negative number display (parentheses vs minus sign)
- [ ] Thousand separator per locale

### 10.5 RTL Support
- [ ] CSS logical properties
- [ ] RTL layout testing
- [ ] Bidirectional text handling
- [ ] Number direction in RTL (always LTR for amounts)
- [ ] Chart axis direction

---

## 11. Security

### 11.1 Encryption Security
- [x] Fernet encryption for secrets (AES-128-CBC + HMAC)
- [x] MASTER_ENCRYPTION_KEY environment variable
- [ ] **ISSUE:** Fernet key fallback to auto-generated key if env not set — MUST REQUIRE env key in production
- [ ] Key rotation mechanism (re-encrypt all secrets with new key)
- [ ] Key management: use AWS KMS / HashiCorp Vault for master key
- [ ] Encryption at rest for database (PostgreSQL TDE)
- [ ] Encryption key backup procedure
- [ ] Encryption algorithm upgrade path (AES-256)

### 11.2 Authentication Security
- [x] Org-scoped data isolation
- [x] Gate auth module
- [ ] Token storage: HttpOnly cookie preferred over localStorage
- [ ] CSRF protection
- [ ] Session timeout (shorter for financial data)
- [ ] Re-authentication for sensitive operations (reveal secret, large transfers)
- [ ] Two-factor authentication enforcement
- [ ] Concurrent session detection
- [ ] Brute force protection

### 11.3 Financial Data Security
- [ ] All financial data over HTTPS only
- [ ] Strict CSP headers (no inline scripts in production)
- [ ] No financial data in URL query parameters
- [ ] No financial data in browser history
- [ ] Auto-clear clipboard after copying secrets
- [ ] Screen lock detection (blur sensitive data)
- [ ] No financial data in localStorage (use sessionStorage or memory only)
- [ ] PII masking in logs (account numbers, balances)
- [ ] Financial data retention policy
- [ ] Right to deletion (GDPR) implementation
- [ ] Data export for user portability

### 11.4 Input Security
- [ ] Input sanitization (XSS prevention)
- [ ] Output encoding
- [ ] SQL injection prevention (parameterized queries)
- [ ] Amount validation (prevent negative where inappropriate)
- [ ] Currency code validation (ISO 4217)
- [ ] Date validation
- [ ] File upload validation (receipt images)
- [ ] Content-Type validation
- [ ] Request body size limits

### 11.5 Network Security
- [ ] HTTPS enforcement
- [ ] HSTS headers
- [ ] Content Security Policy headers
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Referrer-Policy: no-referrer (for financial app)
- [ ] CORS configuration (strict origins)
- [ ] Certificate pinning (mobile)

### 11.6 Compliance
- [ ] PCI DSS compliance review (if handling card data)
- [ ] GDPR compliance (data export, deletion)
- [ ] SOC 2 compliance controls
- [ ] Financial data encryption standards
- [ ] Audit trail completeness
- [ ] Access control documentation
- [ ] Incident response plan for data breach
- [ ] Privacy policy documentation
- [ ] Terms of service documentation

### 11.7 Dependency Security
- [ ] Python dependency vulnerability scanning (pip-audit)
- [ ] JavaScript dependency vulnerability scanning
- [ ] Automated dependency updates
- [ ] Lock file integrity verification
- [ ] cryptography library kept up to date

---

## 12. Testing

### 12.1 Backend Unit Tests
- [x] `tests/test_api.py` — API endpoint tests
- [ ] Test: Create secret — valid input
- [ ] Test: Create secret — empty name
- [ ] Test: Create secret — empty value
- [ ] Test: Create secret — very long value
- [ ] Test: List secrets — empty
- [ ] Test: List secrets — with data
- [ ] Test: List secrets — org isolation (cannot see other org secrets)
- [ ] Test: Reveal secret — valid
- [ ] Test: Reveal secret — wrong org
- [ ] Test: Reveal secret — non-existent ID
- [ ] Test: Delete secret — existing
- [ ] Test: Delete secret — non-existent
- [ ] Test: Delete secret — wrong org
- [ ] Test: Encryption — value is encrypted in DB
- [ ] Test: Encryption — revealed value matches original
- [ ] Test: Encryption — different master key cannot decrypt
- [ ] Test: Vault CRUD (when implemented)
- [ ] Test: SharedInfo CRUD (when implemented)
- [ ] Test: AuditLog creation on operations
- [ ] Test: Transaction CRUD (when implemented)
- [ ] Test: Account CRUD (when implemented)
- [ ] Test: Budget CRUD (when implemented)
- [ ] Test: Category CRUD (when implemented)
- [ ] Test: Bill CRUD (when implemented)
- [ ] Test: Goal CRUD (when implemented)
- [ ] Test: Report generation (when implemented)
- [ ] Test: Multi-currency calculations
- [ ] Test: Recurring transaction scheduling
- [ ] Test: Budget alert triggering
- [ ] Test: Export CSV format correctness
- [ ] Test: Export PDF generation
- [ ] Test: Health endpoint

### 12.2 Backend Integration Tests
- [ ] Test: Full secret lifecycle (create -> reveal -> rotate -> delete)
- [ ] Test: Vault with nested secrets
- [ ] Test: Transaction with category and account
- [ ] Test: Budget enforcement with transactions
- [ ] Test: Report generation with real data
- [ ] Test: Database migration up/down
- [ ] Test: API with real PostgreSQL

### 12.3 Frontend Unit Tests
- [ ] Test: Secret list rendering
- [ ] Test: Secret reveal toggle
- [ ] Test: Secret copy to clipboard
- [ ] Test: Transaction list rendering
- [ ] Test: Transaction form validation
- [ ] Test: Budget progress bar calculation
- [ ] Test: Currency formatting
- [ ] Test: Date formatting
- [ ] Test: Chart data preparation
- [ ] Test: Theme toggle
- [ ] Test: Navigation state
- [ ] Test: Empty state rendering
- [ ] Test: Error state rendering

### 12.4 End-to-End Tests
- [ ] E2E: Login flow
- [ ] E2E: Create and reveal secret
- [ ] E2E: Create transaction
- [ ] E2E: Categorize transaction
- [ ] E2E: Create budget
- [ ] E2E: View budget vs actual
- [ ] E2E: Add bill reminder
- [ ] E2E: Set financial goal
- [ ] E2E: Generate report
- [ ] E2E: Export data
- [ ] E2E: Toggle dark mode
- [ ] E2E: Responsive layout
- [ ] E2E: Keyboard navigation
- [ ] E2E test framework setup (Playwright)

### 12.5 Security Tests
- [ ] Security: Secret never appears in API response (except reveal endpoint)
- [ ] Security: Secret encrypted in database
- [ ] Security: Org isolation enforced
- [ ] Security: Rate limiting on reveal endpoint
- [ ] Security: CSRF protection
- [ ] Security: XSS prevention
- [ ] Security: SQL injection prevention
- [ ] Security: Sensitive data not in logs
- [ ] Penetration testing schedule

### 12.6 Performance Tests
- [ ] Load test: Concurrent API requests
- [ ] Load test: Large transaction list (100K+ rows)
- [ ] Load test: Report generation with large datasets
- [ ] Lighthouse CI for performance scoring
- [ ] Bundle size regression tests

### 12.7 Visual Regression Tests
- [ ] Visual test: Dashboard view
- [ ] Visual test: Secret list view
- [ ] Visual test: Transaction list view
- [ ] Visual test: Budget view
- [ ] Visual test: Report charts
- [ ] Visual test: Dark mode
- [ ] Visual test: Light mode
- [ ] Visual test: Mobile layout

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] Backend: docstrings on all route handlers
- [ ] Backend: docstrings on all model classes
- [ ] Backend: encryption documentation
- [ ] Backend: README.md with setup instructions
- [ ] Frontend: JSDoc comments on all functions
- [ ] Frontend: README.md with setup instructions
- [ ] Architecture decision records
- [ ] Data model diagram
- [ ] Security architecture document

### 13.2 API Documentation
- [ ] FastAPI auto-generated OpenAPI docs
- [ ] API authentication guide
- [ ] API encryption details
- [ ] API error codes reference
- [ ] Postman/Insomnia collection

### 13.3 User Documentation
- [ ] Getting started guide
- [ ] Secret management guide
- [ ] Transaction tracking guide
- [ ] Budget management guide
- [ ] Bill reminders guide
- [ ] Financial goals guide
- [ ] Reports guide
- [ ] Receipt scanning guide
- [ ] Multi-currency guide
- [ ] Export/import guide
- [ ] FAQ
- [ ] Security FAQ (how data is protected)

### 13.4 Operations Documentation
- [ ] Deployment guide
- [ ] Environment variables reference
- [ ] Encryption key management guide
- [ ] Database migration guide
- [ ] Backup and recovery guide
- [ ] Incident response for financial data

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [ ] GitHub Actions / GitLab CI workflow
- [ ] Lint Python code (ruff/flake8)
- [ ] Type check Python code (mypy)
- [ ] Run backend unit tests
- [ ] Run backend integration tests
- [ ] Run security tests
- [ ] Lint frontend code
- [ ] Run frontend tests
- [ ] Build frontend assets
- [ ] Docker image build
- [ ] Docker image push to registry
- [ ] Security scanning (Snyk/Trivy)
- [ ] License compliance check
- [ ] Secret scanning (prevent committed secrets)

### 14.2 CD Pipeline
- [ ] Staging environment auto-deploy
- [ ] Production deploy with manual approval
- [ ] Blue/green deployment
- [ ] Canary deployment
- [ ] Rollback automation
- [ ] Database migration as part of deploy
- [ ] Health check post-deploy
- [ ] Smoke test post-deploy
- [ ] Deployment notification

### 14.3 Environment Configuration
- [ ] Development environment setup
- [ ] Staging environment
- [ ] Production environment
- [ ] Environment variable validation on startup
- [ ] **CRITICAL:** MASTER_ENCRYPTION_KEY must be set in production
- [ ] Secret management (HashiCorp Vault / AWS Secrets Manager)
- [ ] Feature flags system

### 14.4 Monitoring & Observability
- [ ] Application performance monitoring
- [ ] Error tracking (Sentry)
- [ ] Structured logging
- [ ] Request tracing
- [ ] Metrics endpoint (Prometheus)
- [ ] Grafana dashboards
- [ ] Alerting rules
- [ ] Uptime monitoring
- [ ] Database monitoring
- [ ] Encryption health monitoring
- [ ] Financial data integrity checks (scheduled)

---

## 15. Backend

### 15.1 Database & Models
- [x] Vault model — secret vaults/groups
- [x] Secret model — encrypted secrets with metadata
- [x] AuditLog model — action audit trail
- [x] SharedInfo model — org-wide shared information
- [x] Alembic migrations for all models
- [x] PostgreSQL-specific JSONB columns
- [x] Database indexes for org_id, timestamps, composite queries
- [ ] Transaction model — financial transactions
- [ ] FinancialAccount model — bank/credit/crypto accounts
- [ ] Budget model — budget definitions
- [ ] Category model — spending categories
- [ ] Bill model — recurring bills
- [ ] Goal model — financial goals
- [ ] RecurringTransaction model — recurring transaction templates
- [ ] Receipt model — receipt images and OCR data
- [ ] ExchangeRate model — cached exchange rates
- [ ] Database seed script for development
- [ ] Soft delete support
- [ ] Database backup automation
- [ ] Read replica configuration

### 15.2 API Architecture
- [x] FastAPI router
- [x] Pydantic request/response models
- [x] SQLAlchemy ORM
- [x] Fernet encryption layer
- [ ] API versioning (v1, v2)
- [ ] API pagination (cursor-based)
- [ ] API sorting
- [ ] API filtering
- [ ] API rate limiting middleware
- [ ] Background task queue (report generation, OCR)
- [ ] Webhook delivery
- [ ] OpenAPI spec customization

### 15.3 Authentication & Authorization
- [x] Org-scoped data queries (X-Org-Id header)
- [x] Gate auth module (gate_auth.py)
- [ ] Role-based access control
- [ ] User-level secret ownership
- [ ] Team-level vault access
- [ ] Re-authentication for sensitive operations
- [ ] API key support for service-to-service calls
- [ ] Rate limiting per user

### 15.4 Encryption & Key Management
- [x] Fernet encryption (AES-128-CBC + HMAC)
- [x] MASTER_ENCRYPTION_KEY from environment
- [ ] Key rotation without downtime
- [ ] Multiple active keys (decrypt with any, encrypt with latest)
- [ ] Key version tracking per secret
- [ ] Hardware security module (HSM) integration path
- [ ] Encryption audit logging
- [ ] Key derivation function (per-secret salt)
- [ ] Envelope encryption (data key encrypted by master key)

### 15.5 Error Handling
- [ ] Global exception handler
- [ ] Structured error responses
- [ ] Error logging with context (no sensitive data)
- [ ] Error alerting for critical failures
- [ ] Graceful degradation
- [ ] Database connection error recovery
- [ ] Encryption error handling (corrupted data)

### 15.6 Logging & Monitoring
- [ ] Structured JSON logging
- [ ] Request/response logging (sanitized — NO secret values)
- [ ] Slow query logging
- [ ] Error rate monitoring
- [ ] Prometheus metrics endpoint
- [ ] Custom business metrics
- [ ] Correlation ID propagation
- [ ] Audit log integrity monitoring

### 15.7 Data Integrity
- [x] Pydantic validation on API inputs
- [x] Unique constraint on Vault per org
- [x] Foreign key constraints (Secret -> Vault)
- [ ] Financial calculation precision (Decimal, not Float)
- [ ] Currency amount validation (max decimal places per currency)
- [ ] Double-entry bookkeeping enforcement (if applicable)
- [ ] Balance reconciliation checks
- [ ] Data consistency scheduled jobs

### 15.8 Scalability
- [ ] Horizontal scaling (stateless backend)
- [ ] Database connection pool tuning
- [ ] Caching layer (Redis) for exchange rates, balances
- [ ] Background job processing for heavy operations
- [ ] Queue-based event processing
- [ ] Load balancer configuration
- [ ] Auto-scaling rules

---

## Appendix A: Wallet Views & Pages Inventory

1. Dashboard / Home
2. Secrets List
3. Secret Detail / Reveal
4. Secret Create Form
5. Vault List
6. Vault Detail (secrets within)
7. Vault Create/Edit Form
8. Shared Info List
9. Shared Info Detail
10. Shared Info Create Form
11. Audit Log List
12. Audit Log Detail
13. Transaction List
14. Transaction Create/Edit Form
15. Transaction Detail
16. Account List
17. Account Detail
18. Account Create/Edit Form
19. Budget Overview
20. Budget Create/Edit Form
21. Budget vs Actual View
22. Category List
23. Category Create/Edit Form
24. Income Overview
25. Bill Reminders List
26. Bill Create/Edit Form
27. Bill Calendar View
28. Financial Goals List
29. Goal Detail (progress)
30. Goal Create/Edit Form
31. Report: Spending by Category
32. Report: Income vs Expense
33. Report: Net Worth
34. Report: Cash Flow
35. Report: Monthly Summary
36. Receipt Gallery
37. Receipt Scan/Upload
38. Investment Portfolio
39. Investment Detail
40. Tax Overview
41. Export Dialog
42. Settings — Accounts
43. Settings — Categories
44. Settings — Notifications
45. Settings — Security
46. Settings — Currency
47. Settings — Import/Export
48. Search Results
49. Error Page (404)
50. Error Page (500)
51. Loading/Splash Screen
52. Empty States (per section)

---

## Appendix B: React Migration Component Inventory

### Layout Components
- [ ] `AppLayout` — main layout shell
- [ ] `TopBar` — top navigation
- [ ] `Sidebar` — left navigation
- [ ] `ContextPanel` — right panel
- [ ] `PageHeader` — page title + breadcrumbs
- [ ] `PageContent` — main content area

### Feature Components — Secrets
- [ ] `SecretList` — secret list with search/filter
- [ ] `SecretCard` — individual secret card
- [ ] `SecretRevealDialog` — reveal with confirmation
- [ ] `SecretCreateForm` — create new secret
- [ ] `VaultList` — vault list
- [ ] `VaultCard` — vault card
- [ ] `SharedInfoList` — shared info list
- [ ] `AuditLogTable` — audit log with filtering

### Feature Components — Finance
- [ ] `TransactionList` — transaction list with filtering
- [ ] `TransactionRow` — individual transaction row
- [ ] `TransactionForm` — create/edit transaction
- [ ] `AccountList` — financial account list
- [ ] `AccountCard` — account card with balance
- [ ] `AccountForm` — create/edit account
- [ ] `BudgetOverview` — budget dashboard
- [ ] `BudgetProgressBar` — budget vs actual bar
- [ ] `BudgetForm` — create/edit budget
- [ ] `CategoryPicker` — category selection
- [ ] `CategoryManager` — category CRUD
- [ ] `BillList` — bill reminders list
- [ ] `BillForm` — create/edit bill
- [ ] `BillCalendar` — calendar view of bills
- [ ] `GoalList` — goals list
- [ ] `GoalProgress` — goal progress visualization
- [ ] `GoalForm` — create/edit goal
- [ ] `ReceiptScanner` — camera/upload receipt
- [ ] `ReceiptGallery` — receipt image gallery

### Chart Components
- [ ] `SpendingPieChart` — spending by category
- [ ] `IncomeExpenseBarChart` — income vs expense
- [ ] `NetWorthLineChart` — net worth over time
- [ ] `CashFlowWaterfallChart` — cash flow waterfall
- [ ] `BudgetComparisonChart` — budget vs actual
- [ ] `BalanceHistoryChart` — account balance over time
- [ ] `InvestmentPerformanceChart` — portfolio performance

### Shared Components
- [ ] `CurrencyDisplay` — formatted currency amount
- [ ] `CurrencyInput` — currency amount input
- [ ] `DateRangePicker` — date range selection
- [ ] `DataTable` — reusable sortable/filterable table
- [ ] `StatusBadge` — status pill
- [ ] `EmptyState` — empty state
- [ ] `ErrorBoundary` — error boundary
- [ ] `LoadingSkeleton` — skeleton loader
- [ ] `ConfirmDialog` — confirmation modal
- [ ] `Pagination` — pagination controls
- [ ] `FilterBar` — search + filter controls

### Hook Library
- [ ] `useSecrets()` — secret CRUD
- [ ] `useVaults()` — vault CRUD
- [ ] `useTransactions()` — transaction CRUD
- [ ] `useAccounts()` — account CRUD
- [ ] `useBudgets()` — budget CRUD
- [ ] `useCategories()` — category CRUD
- [ ] `useBills()` — bill CRUD
- [ ] `useGoals()` — goal CRUD
- [ ] `useReports()` — report queries
- [ ] `useAuth()` — authentication state
- [ ] `useCurrency()` — currency formatting
- [ ] `useTheme()` — theme toggle
- [ ] `useClipboard()` — copy to clipboard with auto-clear
- [ ] `useDebounce()` — debounce utility
- [ ] `useMediaQuery()` — responsive breakpoint detection

---

## Appendix C: Detailed Test Scenarios

### C.1 Secret Management Test Scenarios
- [ ] Scenario: Create secret with valid name and value
- [ ] Scenario: Create secret with empty name (expect 422)
- [ ] Scenario: Create secret with empty value (expect 422)
- [ ] Scenario: Create secret with very long name (1000+ chars)
- [ ] Scenario: Create secret with very long value (100KB+)
- [ ] Scenario: Create secret with special characters in name
- [ ] Scenario: Create secret with special characters in value
- [ ] Scenario: Create secret with unicode in value
- [ ] Scenario: Create secret with binary-like value (base64)
- [ ] Scenario: Create secret and verify it is encrypted in DB (not plaintext)
- [ ] Scenario: Create secret and reveal — value matches original
- [ ] Scenario: Create secret in org A, try to reveal from org B (expect 404)
- [ ] Scenario: Create secret in org A, try to delete from org B (expect 404)
- [ ] Scenario: Delete secret and verify it is gone
- [ ] Scenario: Delete non-existent secret (expect 404)
- [ ] Scenario: List secrets returns only current org
- [ ] Scenario: List secrets from empty org (expect empty list)
- [ ] Scenario: Reveal secret with correct org returns decrypted value
- [ ] Scenario: Reveal non-existent secret (expect 404)
- [ ] Scenario: Concurrent create operations (thread safety)
- [ ] Scenario: Concurrent reveal operations (thread safety)
- [ ] Scenario: Large number of secrets (1000+) list performance
- [ ] Scenario: Secret with null description
- [ ] Scenario: Secret with empty string description

### C.2 Encryption Test Scenarios
- [ ] Scenario: Encrypted value differs from plaintext
- [ ] Scenario: Same plaintext produces different ciphertext (Fernet uses random IV)
- [ ] Scenario: Decryption with correct key succeeds
- [ ] Scenario: Decryption with wrong key fails
- [ ] Scenario: Corrupted ciphertext fails gracefully (not crash)
- [ ] Scenario: Empty master key environment variable
- [ ] Scenario: Invalid master key format
- [ ] Scenario: Key rotation — re-encrypt with new key
- [ ] Scenario: Key rotation — old key cannot decrypt new secrets
- [ ] Scenario: Key rotation — new key can decrypt old secrets (during migration)

### C.3 Vault Test Scenarios
- [ ] Scenario: Create vault with name and description
- [ ] Scenario: Create vault with empty name (expect 422)
- [ ] Scenario: Create vault with owner_team
- [ ] Scenario: List vaults by org
- [ ] Scenario: Add secret to vault
- [ ] Scenario: Remove secret from vault
- [ ] Scenario: Delete vault with secrets (expect cascade warning)
- [ ] Scenario: Delete empty vault
- [ ] Scenario: List secrets within vault
- [ ] Scenario: Vault org isolation

### C.4 Audit Log Test Scenarios
- [ ] Scenario: Audit event on secret create
- [ ] Scenario: Audit event on secret reveal
- [ ] Scenario: Audit event on secret delete
- [ ] Scenario: Audit event on secret update
- [ ] Scenario: Audit event contains correct user_id
- [ ] Scenario: Audit event contains correct org_id
- [ ] Scenario: Audit event contains correct action
- [ ] Scenario: Audit event contains correct resource_type
- [ ] Scenario: Audit event contains correct ip_address
- [ ] Scenario: Audit event metadata populated
- [ ] Scenario: List audit events by org
- [ ] Scenario: List audit events by user
- [ ] Scenario: List audit events by action
- [ ] Scenario: List audit events by date range
- [ ] Scenario: Audit events org isolation

### C.5 Transaction Test Scenarios (When Implemented)
- [ ] Scenario: Create income transaction
- [ ] Scenario: Create expense transaction
- [ ] Scenario: Create transfer transaction
- [ ] Scenario: Create transaction with all fields
- [ ] Scenario: Create transaction with minimum fields
- [ ] Scenario: Create transaction with negative amount (expense)
- [ ] Scenario: Create transaction with zero amount (expect 422)
- [ ] Scenario: Create transaction with future date
- [ ] Scenario: Create transaction with past date
- [ ] Scenario: Update transaction amount
- [ ] Scenario: Update transaction category
- [ ] Scenario: Delete transaction
- [ ] Scenario: List transactions with date range filter
- [ ] Scenario: List transactions with category filter
- [ ] Scenario: List transactions with account filter
- [ ] Scenario: List transactions with amount range filter
- [ ] Scenario: List transactions sorted by date ascending
- [ ] Scenario: List transactions sorted by amount descending
- [ ] Scenario: Transaction pagination (100 per page)
- [ ] Scenario: Transaction search by description
- [ ] Scenario: Transaction with multi-currency
- [ ] Scenario: Transaction with receipt attachment
- [ ] Scenario: Recurring transaction auto-creation
- [ ] Scenario: Transaction duplicate detection
- [ ] Scenario: Transaction bulk import from CSV
- [ ] Scenario: Transaction CSV import with invalid data (graceful error)

### C.6 Budget Test Scenarios (When Implemented)
- [ ] Scenario: Create monthly budget
- [ ] Scenario: Create weekly budget
- [ ] Scenario: Create budget with category filter
- [ ] Scenario: Update budget amount
- [ ] Scenario: Delete budget
- [ ] Scenario: Budget progress calculation (% spent)
- [ ] Scenario: Budget alert at 80% threshold
- [ ] Scenario: Budget alert at 90% threshold
- [ ] Scenario: Budget alert at 100% (over budget)
- [ ] Scenario: Budget rollover calculation
- [ ] Scenario: Multiple budgets for same period
- [ ] Scenario: Budget with zero amount (tracking only)
- [ ] Scenario: Budget spanning category hierarchy

### C.7 Account Management Test Scenarios (When Implemented)
- [ ] Scenario: Create bank checking account
- [ ] Scenario: Create bank savings account
- [ ] Scenario: Create credit card account
- [ ] Scenario: Create crypto wallet account
- [ ] Scenario: Create cash account
- [ ] Scenario: Update account balance
- [ ] Scenario: Delete account with transactions (expect warning)
- [ ] Scenario: Delete account without transactions
- [ ] Scenario: Account balance calculation from transactions
- [ ] Scenario: Net worth calculation across all accounts
- [ ] Scenario: Account with different currencies
- [ ] Scenario: Account reconciliation (manual vs calculated balance)

### C.8 Report Generation Test Scenarios (When Implemented)
- [ ] Scenario: Spending by category report (last 30 days)
- [ ] Scenario: Spending by category report (custom date range)
- [ ] Scenario: Income vs expense report (monthly)
- [ ] Scenario: Net worth report (over time)
- [ ] Scenario: Cash flow report (monthly)
- [ ] Scenario: Report with no data (empty state)
- [ ] Scenario: Report with large dataset (10K+ transactions)
- [ ] Scenario: Report export to CSV
- [ ] Scenario: Report export to PDF
- [ ] Scenario: Report comparison (month vs month)

### C.9 Authentication Test Scenarios
- [ ] Scenario: Valid org header returns data
- [ ] Scenario: Missing org header returns default org
- [ ] Scenario: Gate auth token validation
- [ ] Scenario: Invalid gate token returns 401
- [ ] Scenario: Expired gate token returns 401
- [ ] Scenario: Gate auth timeout handling
- [ ] Scenario: Session timeout for financial views

---

## Appendix D: Detailed Responsive Design Specifications

### D.1 Mobile Layout (0-639px)
- [ ] Header: Logo + hamburger menu + notification icon
- [ ] Navigation: Full-screen slide-out drawer from left
- [ ] Navigation: Close on outside tap
- [ ] Navigation: Close on route change
- [ ] Content: Single column, full width
- [ ] Stat cards: Single column stack
- [ ] Table: Horizontal scroll with shadow indicator
- [ ] Table: Alternative card view for transactions
- [ ] Toolbar: Stacked vertically (search full-width, filters below)
- [ ] Modals: Full screen (bottom sheet style)
- [ ] Context panel: Hidden by default
- [ ] Charts: Full width, touch-optimized
- [ ] Transaction list: Card layout with swipe actions
- [ ] Budget bars: Full width
- [ ] Currency amounts: Larger font for readability
- [ ] Quick-add: Floating action button (bottom right)
- [ ] Bottom navigation: Home, Transactions, Budget, Goals, More

### D.2 Tablet Layout (640-1023px)
- [ ] Header: Full width with search bar
- [ ] Navigation: Collapsible sidebar (icon-only mode)
- [ ] Content: Two columns (content + sidebar summary)
- [ ] Stat cards: Two-column grid
- [ ] Table: Full width with selected columns
- [ ] Charts: Side by side where possible
- [ ] Transaction list: Table view with key columns
- [ ] Budget overview: Two-column grid

### D.3 Desktop Layout (1024-1279px)
- [ ] Header: Full width with search bar and quick actions
- [ ] Navigation: Fixed sidebar (~220px)
- [ ] Content: Three columns (sidebar + content + context)
- [ ] Stat cards: Four-column grid
- [ ] Table: Full width with all columns
- [ ] Charts: Comfortable sizing with legends
- [ ] Transaction detail: Side panel on click

### D.4 Wide Layout (1280px+)
- [ ] Content: Max-width container centered
- [ ] Dashboard: Widget grid layout
- [ ] Charts: Larger with more detail
- [ ] Table: Extra columns (notes, tags, etc.)

---

## Appendix E: Financial Data Models Specification

### E.1 Transaction Model
- [ ] `id` — unique identifier (UUID)
- [ ] `org_id` — organization scope
- [ ] `user_id` — user who created
- [ ] `account_id` — linked financial account
- [ ] `category_id` — spending category
- [ ] `type` — enum: income, expense, transfer
- [ ] `status` — enum: cleared, pending, reconciled, void
- [ ] `amount` — Decimal (not Float, for precision)
- [ ] `currency` — ISO 4217 code
- [ ] `description` — transaction description
- [ ] `merchant` — merchant/payee name
- [ ] `date` — transaction date
- [ ] `notes` — user notes
- [ ] `tags` — JSONB array of tags
- [ ] `receipt_id` — linked receipt (nullable)
- [ ] `recurring_id` — linked recurring template (nullable)
- [ ] `is_split` — boolean, is this a split transaction
- [ ] `parent_transaction_id` — for splits, reference parent
- [ ] `location` — merchant location (nullable)
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### E.2 Financial Account Model
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — account owner
- [ ] `name` — display name
- [ ] `type` — enum: checking, savings, credit_card, crypto, cash, investment, loan
- [ ] `institution` — bank/institution name
- [ ] `last_four` — last 4 digits for identification
- [ ] `currency` — default currency
- [ ] `current_balance` — current balance (Decimal)
- [ ] `credit_limit` — for credit cards (nullable)
- [ ] `interest_rate` — for savings/loans (nullable)
- [ ] `color` — display color
- [ ] `icon` — display icon
- [ ] `is_archived` — soft archive
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### E.3 Budget Model
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — budget owner
- [ ] `name` — budget name
- [ ] `amount` — budget amount (Decimal)
- [ ] `currency` — budget currency
- [ ] `period` — enum: weekly, biweekly, monthly, quarterly, yearly
- [ ] `start_date` — budget period start
- [ ] `end_date` — budget period end (nullable for recurring)
- [ ] `categories` — JSONB array of category_ids
- [ ] `rollover` — boolean, carry unused to next period
- [ ] `is_active` — active/inactive
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

### E.4 Category Model
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `name` — category name
- [ ] `parent_id` — parent category (nullable, for hierarchy)
- [ ] `icon` — display icon
- [ ] `color` — display color
- [ ] `is_income` — boolean, income vs expense category
- [ ] `is_system` — boolean, system-default vs user-created
- [ ] `sort_order` — display order
- [ ] `created_at` — creation timestamp

### E.5 Bill Model
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — bill owner
- [ ] `name` — bill name
- [ ] `amount` — expected amount (Decimal)
- [ ] `currency` — bill currency
- [ ] `frequency` — enum: one_time, weekly, monthly, quarterly, annually
- [ ] `next_due_date` — next payment due
- [ ] `account_id` — linked account (nullable)
- [ ] `category_id` — linked category (nullable)
- [ ] `is_auto_pay` — boolean
- [ ] `reminder_days_before` — int array [1, 3, 7]
- [ ] `is_active` — active/inactive
- [ ] `created_at` — creation timestamp

### E.6 Goal Model
- [ ] `id` — unique identifier
- [ ] `org_id` — organization scope
- [ ] `user_id` — goal owner
- [ ] `name` — goal name
- [ ] `type` — enum: emergency_fund, vacation, down_payment, debt_payoff, retirement, custom
- [ ] `target_amount` — target amount (Decimal)
- [ ] `current_amount` — current progress (Decimal)
- [ ] `currency` — goal currency
- [ ] `deadline` — target date (nullable)
- [ ] `account_id` — linked savings account (nullable)
- [ ] `priority` — int, priority ranking
- [ ] `is_completed` — boolean
- [ ] `completed_at` — completion timestamp (nullable)
- [ ] `created_at` — creation timestamp
- [ ] `updated_at` — last update timestamp

---

## Appendix F: Error State Inventory

### F.1 Network Errors
- [ ] Error state: No internet connection
- [ ] Error state: API request timeout
- [ ] Error state: Server 500 error
- [ ] Error state: Server 502/503 (backend down)
- [ ] Retry mechanism: Auto retry with exponential backoff
- [ ] Retry mechanism: Manual retry button
- [ ] Offline banner with reconnection detection

### F.2 Validation Errors
- [ ] Error state: Required field empty
- [ ] Error state: Invalid amount format
- [ ] Error state: Negative amount where not allowed
- [ ] Error state: Invalid date format
- [ ] Error state: Future date where not allowed
- [ ] Error state: Invalid currency code
- [ ] Error state: Duplicate entry
- [ ] Inline error messages under fields
- [ ] Form-level error summary

### F.3 Authorization Errors
- [ ] Error state: Session expired (401) — redirect to login
- [ ] Error state: Forbidden (403) — permission denied
- [ ] Error state: Financial session timeout — re-auth required
- [ ] Error state: Secret reveal denied — re-auth required

### F.4 Financial Errors
- [ ] Error state: Insufficient funds (for transfers)
- [ ] Error state: Budget exceeded warning
- [ ] Error state: Invalid currency conversion
- [ ] Error state: Exchange rate unavailable
- [ ] Error state: Import file format error
- [ ] Error state: Receipt OCR failed
- [ ] Error state: Bank connection error

---

## Appendix G: Loading State Inventory

### G.1 Page-Level Loading
- [ ] Loading state: Initial app load (splash screen)
- [ ] Loading state: Page navigation (skeleton screen)
- [ ] Loading state: Data fetching (skeleton cards/rows)

### G.2 Component-Level Loading
- [ ] Loading state: Transaction list (skeleton rows)
- [ ] Loading state: Stat cards (skeleton cards)
- [ ] Loading state: Charts (skeleton charts)
- [ ] Loading state: Account balances (shimmer)
- [ ] Loading state: Budget progress bars (skeleton)
- [ ] Loading state: Goal progress (skeleton)
- [ ] Loading state: Secret list (skeleton rows)

### G.3 Action-Level Loading
- [ ] Loading state: Form submission (button spinner)
- [ ] Loading state: Secret reveal (decryption spinner)
- [ ] Loading state: Report generation (progress indicator)
- [ ] Loading state: CSV import (progress bar with row count)
- [ ] Loading state: Receipt OCR (processing animation)
- [ ] Loading state: Exchange rate fetch (inline spinner)
- [ ] Loading state: Export generation (progress indicator)
- [ ] Loading state: Bulk operation (progress bar)

---

---

## Appendix H: Keyboard Shortcut Specification

### H.1 Global Shortcuts
- [ ] `Cmd/Ctrl + K` — Open command palette / quick search
- [ ] `Cmd/Ctrl + /` — Toggle sidebar
- [ ] `Cmd/Ctrl + Shift + D` — Toggle dark mode
- [ ] `Cmd/Ctrl + ,` — Open settings
- [ ] `Escape` — Close current modal/panel/overlay
- [ ] `?` — Show keyboard shortcuts help

### H.2 Navigation Shortcuts
- [ ] `G then H` — Go to Dashboard
- [ ] `G then S` — Go to Secrets
- [ ] `G then V` — Go to Vaults
- [ ] `G then T` — Go to Transactions
- [ ] `G then A` — Go to Accounts
- [ ] `G then B` — Go to Budgets
- [ ] `G then R` — Go to Reports
- [ ] `G then I` — Go to Shared Info
- [ ] `G then U` — Go to Audit Log
- [ ] `G then P` — Go to Settings

### H.3 Action Shortcuts
- [ ] `N then S` — New Secret
- [ ] `N then V` — New Vault
- [ ] `N then T` — New Transaction
- [ ] `N then A` — New Account
- [ ] `N then B` — New Budget
- [ ] `Cmd/Ctrl + Enter` — Submit current form
- [ ] `Cmd/Ctrl + E` — Export current view

### H.4 Table Navigation
- [ ] `J` / `Down Arrow` — Move to next row
- [ ] `K` / `Up Arrow` — Move to previous row
- [ ] `Enter` — Open selected row detail
- [ ] `Space` — Toggle row selection
- [ ] `R` — Reveal secret (when secret row selected)
- [ ] `C` — Copy value (when revealed)
- [ ] `Delete` / `Backspace` — Delete selected

---

## Appendix I: Security Hardening Checklist

### I.1 Encryption Hardening
- [ ] Verify Fernet key is at least 32 bytes (URL-safe base64)
- [ ] Verify master key is NOT logged anywhere
- [ ] Verify master key is NOT in any config file
- [ ] Verify master key is NOT in any Docker image layer
- [ ] Verify encrypted values are NOT searchable (no deterministic encryption)
- [ ] Verify decrypted values are NOT cached
- [ ] Verify decrypted values are NOT logged
- [ ] Verify decrypted values are NOT stored in browser history
- [ ] Verify decrypted values are NOT in URL parameters
- [ ] Verify clipboard auto-clear after copying secrets (30 seconds)
- [ ] Verify reveal endpoints have rate limiting
- [ ] Verify reveal endpoints require re-authentication
- [ ] Verify reveal endpoints log to audit trail

### I.2 API Security Hardening
- [ ] All endpoints require authentication (except health)
- [ ] All endpoints validate org isolation
- [ ] All endpoints validate request body size
- [ ] All endpoints validate Content-Type header
- [ ] All list endpoints have pagination limits
- [ ] All search endpoints sanitize input
- [ ] Sensitive fields never in URL query params
- [ ] API responses do not leak internal error details
- [ ] Stack traces never returned to client
- [ ] Database connection strings never in responses
- [ ] CORS allows only trusted origins

### I.3 Frontend Security Hardening
- [ ] No sensitive data in localStorage (use sessionStorage or memory)
- [ ] JWT access token in memory only (not localStorage)
- [ ] Refresh token in HttpOnly cookie
- [ ] All forms have CSRF protection
- [ ] All user input is sanitized before display (XSS prevention)
- [ ] All external links have rel="noopener noreferrer"
- [ ] No eval() or innerHTML with user content
- [ ] Subresource Integrity (SRI) on CDN resources
- [ ] Content Security Policy prevents inline scripts in production

### I.4 Infrastructure Security
- [ ] HTTPS enforced everywhere
- [ ] TLS 1.2+ only (no TLS 1.0/1.1)
- [ ] HSTS with long max-age (31536000)
- [ ] Database connections encrypted (SSL)
- [ ] Database credentials rotated regularly
- [ ] Container runs as non-root user
- [ ] Container has read-only filesystem where possible
- [ ] Container has no unnecessary capabilities
- [ ] Network policies restrict inter-service traffic
- [ ] Secrets stored in external secret manager (not env files on disk)

---

## Appendix J: Monitoring & Alerting Specifications

### J.1 Application Metrics
- [ ] Metric: HTTP request count by endpoint and status
- [ ] Metric: HTTP request latency (p50, p95, p99)
- [ ] Metric: Error rate by endpoint
- [ ] Metric: Database query latency
- [ ] Metric: Database connection pool usage
- [ ] Metric: Cache hit/miss ratio
- [ ] Metric: Secret reveal count per user per hour
- [ ] Metric: Encryption/decryption operation time
- [ ] Metric: Active sessions count

### J.2 Business Metrics
- [ ] Metric: Secrets created per day
- [ ] Metric: Secrets revealed per day
- [ ] Metric: Secrets expired per day
- [ ] Metric: Vaults created per day
- [ ] Metric: Active vaults count
- [ ] Metric: Transactions created per day (when financial features built)
- [ ] Metric: Budget utilization percentage
- [ ] Metric: Active users per day

### J.3 Security Metrics
- [ ] Metric: Failed reveal attempts per user
- [ ] Metric: Unauthorized access attempts
- [ ] Metric: Secret access patterns (anomaly detection)
- [ ] Metric: Audit log volume
- [ ] Metric: Encryption operation errors

### J.4 Alert Rules
- [ ] Alert: Error rate > 5% for 5 minutes
- [ ] Alert: p95 latency > 2s for 5 minutes
- [ ] Alert: Encryption operation failure
- [ ] Alert: Unusual reveal volume (> 3x normal)
- [ ] Alert: Master key environment variable missing on startup
- [ ] Alert: Database connection pool > 80%
- [ ] Alert: Health check failure for 1 minute
- [ ] Alert: Audit log write failure
- [ ] Alert: Secret expiry batch (multiple secrets expiring)

---

## Appendix K: Data Import/Export Specifications

### K.1 CSV Import Format (Transactions)
- [ ] Column: date (YYYY-MM-DD or locale format)
- [ ] Column: description (text)
- [ ] Column: amount (number, negative for expenses)
- [ ] Column: currency (ISO 4217, optional, defaults to account currency)
- [ ] Column: category (text, auto-map to existing categories)
- [ ] Column: account (text, match to existing account name)
- [ ] Column: type (income/expense/transfer, optional)
- [ ] Column: notes (text, optional)
- [ ] Column: tags (comma-separated, optional)
- [ ] Import preview with first 10 rows
- [ ] Column mapping UI (match CSV columns to fields)
- [ ] Duplicate detection during import
- [ ] Error report for failed rows
- [ ] Batch size limit (10,000 rows per import)

### K.2 CSV Export Format
- [ ] All transaction fields included
- [ ] Date formatted per user locale
- [ ] Amount formatted with currency symbol
- [ ] Category name (not ID)
- [ ] Account name (not ID)
- [ ] UTF-8 encoding with BOM for Excel compatibility
- [ ] Filename format: wallet_transactions_YYYY-MM-DD.csv

### K.3 PDF Export Format
- [ ] Header: RM Wallet logo + org name
- [ ] Date range of report
- [ ] Summary section: total income, total expenses, net
- [ ] Transaction table with all columns
- [ ] Category breakdown chart (if report type)
- [ ] Footer: page numbers, generation date
- [ ] Professional formatting matching orbit design system

### K.4 Bank Format Import (OFX/QFX)
- [ ] Parse OFX 2.0 format
- [ ] Parse QFX (Quicken) format
- [ ] Extract: date, amount, description, type
- [ ] Map bank categories to Wallet categories
- [ ] Handle multi-currency transactions
- [ ] Duplicate detection (by date + amount + description)
- [ ] Import summary with counts

### K.5 Secret Export/Import
- [ ] Export: encrypted archive format (ZIP + Fernet)
- [ ] Export: include name, description, encrypted value, metadata
- [ ] Export: password-protect archive
- [ ] Import: decrypt and re-encrypt with current master key
- [ ] Import: duplicate name detection
- [ ] Import: vault assignment during import

---

*Generated: 2026-04-06 | Total checkboxes: ~1300+ | Target: 2000+ lines*
