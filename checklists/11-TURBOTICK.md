# 11 -- TurboTick (Issue Tracker) -- Comprehensive Checklist

> **App:** TurboTick -- Issue Tracker / Service Desk (Tickets, Incidents, Requests, Knowledge Base)
> **Stack:** Vanilla HTML/JS Frontend | Python FastAPI Backend | SQLAlchemy + PostgreSQL
> **Architecture:** Vanilla SPA (index.html + inline JS) with orbit-bar.js shell, backend on FastAPI
> **Ports:** Frontend served statically | Backend localhost:45011
> **Models:** Ticket, Incident, Request, Queue, KnowledgeArticle, SlaPolicy, Workflow
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

### 1.1 Frontend Architecture Decision
- [ ] Decision: keep vanilla HTML/JS OR migrate to React
- [ ] If staying vanilla: document architecture and conventions
- [ ] If migrating to React: create Vite + React 19 + TypeScript project
- [ ] Document chosen approach in ADR (Architecture Decision Record)

### 1.2 Current Vanilla Frontend Setup
- [x] `frontend/index.html` exists as main entry
- [x] `frontend/public/orbit-ui/orbit-tokens.css` synced
- [x] `frontend/public/orbit-ui/orbit-theme-init.js` synced
- [x] `frontend/public/orbit-ui/orbit-ui.css` synced
- [x] `frontend/public/orbit-ui/orbit-bar.js` synced
- [x] `frontend/public/orbit-ui/orbit-tailwind-v4.css` synced
- [x] Anti-FOUC script in `index.html` (inline localStorage check)
- [x] `orbit-tokens.css` linked via `<link>` tag
- [x] `orbit-bar.js` loaded with defer
- [x] `orbit-ui.css` loaded
- [x] Custom fonts loaded (RMForma-Regular, RMForma-SemiBold, RMForma-Bold, RM-Samplet-Regular)
- [ ] Remove inline `<style>` block (580+ lines) from index.html
- [ ] Extract CSS to external stylesheet (`styles.css`)
- [ ] Extract JS to external script (`app.js`)
- [ ] Create module system for JS (ES modules or bundled)
- [ ] Add `<meta name="description">` for TurboTick
- [ ] Add `<meta name="theme-color">`
- [ ] Add favicon
- [ ] Add Apple touch icon
- [ ] Add `<noscript>` fallback message

### 1.3 React Migration Setup (If Chosen)
- [ ] Create `TurboTick/frontend/` Vite + React 19 + TypeScript project
- [ ] `package.json`: add `@orbit-ui/react`
- [ ] `package.json`: add Tailwind v3
- [ ] `package.json`: add React Router v7
- [ ] `package.json`: add Zustand
- [ ] `package.json`: add Axios
- [ ] `package.json`: add Lucide React
- [ ] `package.json`: add date-fns
- [ ] `tailwind.config.js`: use orbit preset
- [ ] `index.html`: anti-FOUC script + orbit-ui asset links
- [ ] `main.tsx`: `ThemeProvider` wraps root
- [ ] `index.css`: `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Vite proxy: `/api` -> `http://localhost:45011`
- [ ] Auth: Gate OAuth PKCE flow (reuse pattern from Atlas)
- [ ] Add to sync script `FRONTENDS` array
- [ ] TypeScript strict mode enabled
- [ ] ESLint configured
- [ ] Prettier configured
- [ ] Husky pre-commit hook

### 1.4 Backend Setup
- [x] Python FastAPI backend initialized (`backend/app/main.py`)
- [x] SQLAlchemy models defined (`backend/app/models.py`)
- [x] Database module (`backend/app/database.py`)
- [x] Alembic migrations configured
- [x] Initial migration: tickets, incidents, requests, queues, knowledge_base tables
- [x] Second migration: SLA policies and workflow models
- [x] Requirements.txt exists
- [x] `.env.example` exists
- [x] Start script (`start-backend.sh`)
- [ ] Backend running on port 45011
- [ ] CORS configured for frontend origin
- [ ] Request logging middleware
- [ ] Error handling middleware
- [ ] Health check endpoint (`GET /health`)
- [ ] API versioning

### 1.5 Stitch Designs (Reference)
- [x] `stitch 4/ticket_list_light_theme/` -- ticket list design
- [x] `stitch 4/ticket_detail_light_theme/` -- ticket detail design
- [x] `stitch 4/incident_war_room_light/` -- incident war room design
- [x] `stitch 4/dashboard_light_theme/` -- dashboard design
- [x] `stitch 4/automation_builder_light_theme/` -- automation builder design
- [ ] Implement ticket list matching stitch design
- [ ] Implement ticket detail matching stitch design
- [ ] Implement incident war room matching stitch design
- [ ] Implement dashboard matching stitch design
- [ ] Implement automation builder matching stitch design

### 1.6 Existing Custom CSS Variables
- [x] `--bg`, `--bg-soft`, `--bg-card`, `--bg-card-alt` defined
- [x] `--text`, `--muted`, `--border` defined
- [x] `--accent`, `--accent-2` defined
- [x] `--p1` (critical), `--p2` (high), `--p3` (medium), `--p4` (low) defined
- [ ] Replace all custom CSS variables with orbit token variables
- [ ] Replace `--bg` (#070b14) with `var(--orbit-surface-base)`
- [ ] Replace `--bg-soft` (#0e1320) with `var(--orbit-surface-muted)`
- [ ] Replace `--bg-card` (#121a2b) with `var(--orbit-surface-raised)`
- [ ] Replace `--bg-card-alt` (#171f33) with `var(--orbit-surface-overlay)`
- [ ] Replace `--text` (#e6ecff) with `var(--orbit-content-primary)`
- [ ] Replace `--muted` (#8fa1c9) with `var(--orbit-content-muted)`
- [ ] Replace `--border` (#273351) with `var(--orbit-border-default)`
- [ ] Replace `--accent` (#3b82f6) with `var(--orbit-primary-500)`
- [ ] Replace `--accent-2` (#06b6d4) with `var(--orbit-info-500)`
- [ ] Replace `--p1` (#ef4444) with `var(--orbit-danger-500)`
- [ ] Replace `--p2` (#f97316) with `var(--orbit-warning-600)`
- [ ] Replace `--p3` (#f59e0b) with `var(--orbit-warning-500)`
- [ ] Replace `--p4` (#22c55e) with `var(--orbit-success-500)`
- [ ] Remove custom CSS variable declarations after migration

---

## 2. Design System Integration

### 2.1 Token Integration (Vanilla)
- [x] `orbit-tokens.css` loaded in `<head>`
- [x] `orbit-ui.css` loaded
- [x] `orbit-bar.js` loaded for shell
- [ ] Replace all hardcoded colors in inline `<style>` with orbit tokens
- [ ] Replace all `#070b14` references with `var(--orbit-surface-base)`
- [ ] Replace all `#0e1320` references with `var(--orbit-surface-muted)`
- [ ] Replace all `#121a2b` references with `var(--orbit-surface-raised)`
- [ ] Replace all `#171f33` references with `var(--orbit-surface-overlay)`
- [ ] Replace all `#e6ecff` references with `var(--orbit-content-primary)`
- [ ] Replace all `#8fa1c9` references with `var(--orbit-content-muted)`
- [ ] Replace all `#273351` references with `var(--orbit-border-default)`
- [ ] Replace all `#3b82f6` (accent blue) with `var(--orbit-primary-500)`
- [ ] Replace all `#06b6d4` (cyan) with `var(--orbit-info-500)`
- [ ] Replace all `#ef4444` (red/P1) with `var(--orbit-danger-500)`
- [ ] Replace all `#f97316` (orange/P2) with `var(--orbit-warning-600)`
- [ ] Replace all `#f59e0b` (amber/P3) with `var(--orbit-warning-500)`
- [ ] Replace all `#22c55e` (green/P4) with `var(--orbit-success-500)`
- [ ] Replace body background gradient with orbit token-based gradient
- [ ] Replace `.top-nav` background with orbit surface token
- [ ] Replace `.top-nav` border with orbit border token
- [ ] Replace `.input`, `.select`, `.button`, `.textarea` backgrounds with orbit tokens
- [ ] Replace `.input`, `.select` border with orbit border token
- [ ] Font family uses orbit font family or RM Forma via token

### 2.2 Token Integration (React -- if migrated)
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `index.css` imports `orbit-tokens.css`
- [ ] `ThemeProvider` wraps root
- [ ] All components use orbit semantic classes
- [ ] No hardcoded hex colors anywhere

### 2.3 Replace Custom Components with @orbit-ui/react (If React Migration)

#### Button Replacement
- [ ] Replace all `.button` class elements with `<Button>` from `@orbit-ui/react`
- [ ] "New Ticket" button uses `<Button variant="primary">`
- [ ] "New Incident" button uses `<Button variant="danger">`
- [ ] "New Request" button uses `<Button variant="outline">`
- [ ] Filter/sort toggle buttons use `<Button variant="ghost">`
- [ ] Ticket detail "Edit" uses `<Button variant="outline">`
- [ ] Ticket detail "Close" uses `<Button variant="danger">`
- [ ] Ticket detail "Assign" uses `<Button variant="outline">`
- [ ] Ticket detail "Escalate" uses `<Button variant="warning">`
- [ ] Comment "Submit" uses `<Button variant="primary" size="sm">`
- [ ] Bulk action buttons use `<Button variant="outline">`
- [ ] Knowledge base "New Article" uses `<Button variant="primary">`
- [ ] SLA "Create Policy" uses `<Button variant="primary">`
- [ ] Workflow "Create" uses `<Button variant="primary">`
- [ ] All action buttons in tables use `<IconButton>`

#### Badge Replacement
- [ ] Replace priority badges with `<Badge>` from `@orbit-ui/react`
- [ ] Priority: P1 Critical uses `<Badge variant="danger">`
- [ ] Priority: P2 High uses `<Badge variant="warning">`
- [ ] Priority: P3 Medium uses `<Badge variant="default">`
- [ ] Priority: P4 Low uses `<Badge variant="success">`
- [ ] Replace status badges with `<Badge>`
- [ ] Status: Open uses `<Badge variant="info">`
- [ ] Status: Acknowledged uses `<Badge variant="purple">`
- [ ] Status: In Progress uses `<Badge variant="warning">`
- [ ] Status: Waiting uses `<Badge variant="default">`
- [ ] Status: Escalated uses `<Badge variant="danger">`
- [ ] Status: Resolved uses `<Badge variant="success">`
- [ ] Status: Closed uses `<Badge variant="default">`
- [ ] Replace incident severity badges
- [ ] Severity: SEV1 uses `<Badge variant="danger">`
- [ ] Severity: SEV2 uses `<Badge variant="warning">`
- [ ] Severity: SEV3 uses `<Badge variant="default">`
- [ ] Severity: SEV4 uses `<Badge variant="info">`
- [ ] Replace incident status badges
- [ ] Incident: Detected uses `<Badge variant="danger">`
- [ ] Incident: Acknowledged uses `<Badge variant="warning">`
- [ ] Incident: Investigating uses `<Badge variant="info">`
- [ ] Incident: Mitigating uses `<Badge variant="purple">`
- [ ] Incident: Resolved uses `<Badge variant="success">`
- [ ] Incident: Postmortem uses `<Badge variant="default">`
- [ ] Replace request status badges
- [ ] Request: Submitted uses `<Badge variant="info">`
- [ ] Request: Approved uses `<Badge variant="success">`
- [ ] Request: Rejected uses `<Badge variant="danger">`
- [ ] Request: In Progress uses `<Badge variant="warning">`
- [ ] Request: Fulfilled uses `<Badge variant="success">`
- [ ] Request: Closed uses `<Badge variant="default">`
- [ ] Replace ticket source badges
- [ ] Source: Web Portal uses `<Badge variant="info">`
- [ ] Source: Email Ingestion uses `<Badge variant="default">`
- [ ] Source: API Integration uses `<Badge variant="purple">`
- [ ] Source: Monitoring Alerts uses `<Badge variant="warning">`
- [ ] Source: Security Alerts uses `<Badge variant="danger">`
- [ ] Source: Automation Workflows uses `<Badge variant="default">`
- [ ] Source: External Systems uses `<Badge variant="info">`
- [ ] Replace SLA deadline badges (within SLA / breaching / breached)
- [ ] Replace ticket category badges

#### Card Replacement
- [ ] Replace custom card divs with `<Card>` from `@orbit-ui/react`
- [ ] Dashboard: KPI metric cards
- [ ] Dashboard: ticket queue cards
- [ ] Dashboard: recent activity cards
- [ ] Dashboard: SLA status cards
- [ ] Dashboard: incident summary cards
- [ ] Ticket list: individual ticket cards (if card view)
- [ ] Ticket detail: info card
- [ ] Ticket detail: comments section card
- [ ] Ticket detail: timeline card
- [ ] Ticket detail: linked items card
- [ ] Ticket detail: SLA info card
- [ ] Incident war room: incident info card
- [ ] Incident war room: timeline card
- [ ] Incident war room: affected services card
- [ ] Incident war room: linked ticket card
- [ ] Request detail: request info card
- [ ] Request detail: form data card
- [ ] Knowledge base: article cards
- [ ] SLA: policy cards
- [ ] Workflow: workflow cards
- [ ] Automation builder: step cards

#### Table Replacement
- [ ] Replace custom table styles with `<Table>` from `@orbit-ui/react`
- [ ] Ticket list table (sortable columns)
- [ ] Ticket list table: checkbox column for bulk select
- [ ] Ticket list table: ID column
- [ ] Ticket list table: title column
- [ ] Ticket list table: status column (badge)
- [ ] Ticket list table: priority column (badge)
- [ ] Ticket list table: category column
- [ ] Ticket list table: assignee column
- [ ] Ticket list table: queue column
- [ ] Ticket list table: source column
- [ ] Ticket list table: SLA deadline column
- [ ] Ticket list table: created date column
- [ ] Ticket list table: updated date column
- [ ] Ticket list table: actions column
- [ ] Ticket list table: pagination
- [ ] Incident list table
- [ ] Request list table
- [ ] Knowledge base article list table
- [ ] SLA policy list table
- [ ] Workflow list table
- [ ] Queue management table

#### Input Replacement
- [ ] Replace `.input` class elements with `<Input>` from `@orbit-ui/react`
- [ ] Ticket search input
- [ ] Ticket title input (create/edit)
- [ ] Ticket description textarea
- [ ] Comment textarea
- [ ] Knowledge article title input
- [ ] Knowledge article content textarea
- [ ] SLA policy name input
- [ ] SLA response time input
- [ ] SLA resolution time input
- [ ] Workflow name input
- [ ] Workflow description input
- [ ] Filter inputs (various)

#### Select Replacement
- [ ] Replace `.select` class elements with `<Select>` from `@orbit-ui/react`
- [ ] Ticket priority select (P1-P4)
- [ ] Ticket status select
- [ ] Ticket category select
- [ ] Ticket queue select
- [ ] Ticket source select
- [ ] Ticket assignee select
- [ ] Incident severity select
- [ ] Incident status select
- [ ] Request type select
- [ ] Request status select
- [ ] Filter selects (priority, status, category, queue, assignee)
- [ ] Workflow trigger event select
- [ ] Workflow action type select

#### Additional Component Adoptions
- [ ] Adopt `<Sidebar>` for navigation
- [ ] Adopt `<Modal>` for create/edit dialogs
- [ ] Adopt `<Tabs>` for ticket detail sections
- [ ] Adopt `<EmptyState>` for empty lists
- [ ] Adopt `<Skeleton>` for loading states
- [ ] Adopt `<Tooltip>` for icon explanations
- [ ] Adopt `<Spinner>` for loading indicators
- [ ] Adopt `<Avatar>` for assignee/requester avatars
- [ ] Adopt `<Tag>` for ticket tags
- [ ] Adopt `<Alert>` for SLA breach alerts
- [ ] Adopt `<Dropdown>` for action menus
- [ ] Adopt `<Pagination>` for lists
- [ ] Adopt `<Breadcrumb>` for navigation
- [ ] Adopt `<Drawer>` for detail panels
- [ ] Adopt `<Progress>` for SLA countdown bars
- [ ] Adopt `<Steps>` for workflow visualization
- [ ] Adopt `<Accordion>` for collapsible sections
- [ ] Adopt `<Switch>` for workflow enable/disable
- [ ] Adopt `<Checkbox>` for bulk selection
- [ ] Adopt `<DatePicker>` for SLA deadlines
- [ ] Adopt `<CommandPalette>` for global search (Cmd+K)
- [ ] Adopt `<Divider>` for section separation
- [ ] Adopt `<Toast>` / `useToast` for notifications
- [ ] Adopt `<Popover>` for quick info panels
- [ ] Adopt `<ContextMenu>` for right-click ticket actions

### 2.4 Vanilla JS Component Equivalents (If Staying Vanilla)
- [ ] Create reusable button component function
- [ ] Create reusable badge component function
- [ ] Create reusable card component function
- [ ] Create reusable table component function
- [ ] Create reusable input component function
- [ ] Create reusable select component function
- [ ] Create reusable modal component function
- [ ] Create reusable toast notification function
- [ ] Create reusable tooltip function
- [ ] Create reusable dropdown menu function
- [ ] Create reusable pagination function
- [ ] Create reusable tabs component function
- [ ] Create reusable empty state function
- [ ] Create reusable loading skeleton function
- [ ] Create reusable avatar component function
- [ ] Create reusable tag/chip component function
- [ ] Create reusable progress bar function
- [ ] All components use orbit token CSS variables
- [ ] All components support light and dark themes

---

## 3. Dark Mode

### 3.1 Global Dark Mode Setup
- [x] Anti-FOUC script checks `orbit-theme` in localStorage
- [x] Anti-FOUC script checks `prefers-color-scheme: dark`
- [x] Anti-FOUC script applies `.dark` class to `<html>`
- [ ] Current CSS only supports dark theme (hardcoded dark colors)
- [ ] Add light theme CSS variables / token mapping
- [ ] Theme toggle button in UI (or rely on orbit-bar theme toggle)
- [ ] Theme persists across page reloads (orbit-theme-init handles this)
- [ ] No FOUC on theme switch

### 3.2 Light Theme Implementation (Currently Missing)
- [ ] Body background: light gradient / white
- [ ] Top nav: light background, dark text
- [ ] Top nav: light border bottom
- [ ] Card backgrounds: white / light gray
- [ ] Card borders: light gray
- [ ] Text colors: dark text on light background
- [ ] Muted text: medium gray on light background
- [ ] Input backgrounds: white
- [ ] Input borders: light gray
- [ ] Button backgrounds: light variants
- [ ] Badge backgrounds: light variants
- [ ] Table backgrounds: white with subtle striping
- [ ] Scrollbar: light track and medium thumb
- [ ] Code/pre blocks: light background
- [ ] Link colors: visible on light background
- [ ] Focus rings: visible on light background
- [ ] Shadows: subtle light shadows

### 3.3 Dashboard -- Dark Mode
- [ ] Page background
- [ ] KPI cards: background, border, text
- [ ] KPI card: ticket count number
- [ ] KPI card: open tickets count
- [ ] KPI card: average resolution time
- [ ] KPI card: SLA compliance rate
- [ ] KPI card: unassigned tickets
- [ ] KPI card: trend indicators
- [ ] Ticket queue breakdown chart
- [ ] Priority distribution chart
- [ ] Recent activity feed
- [ ] Activity feed item backgrounds
- [ ] Activity feed timestamps
- [ ] SLA status indicators
- [ ] Quick action buttons

### 3.4 Ticket List -- Dark Mode
- [ ] Page header
- [ ] Search input
- [ ] Filter bar background
- [ ] Filter select dropdowns
- [ ] Active filter badges
- [ ] Table header background
- [ ] Table header text
- [ ] Table row backgrounds
- [ ] Table row hover state
- [ ] Table cell text colors
- [ ] Table borders
- [ ] Priority badges (P1 red, P2 orange, P3 amber, P4 green)
- [ ] Status badges (open, acknowledged, in_progress, waiting, escalated, resolved, closed)
- [ ] Source badges
- [ ] Category text
- [ ] Assignee text
- [ ] Queue text
- [ ] SLA deadline (normal, warning, breached)
- [ ] Date columns
- [ ] Action buttons
- [ ] Bulk selection checkboxes
- [ ] Pagination controls
- [ ] Empty state

### 3.5 Ticket Detail -- Dark Mode
- [ ] Page header / breadcrumb
- [ ] Ticket title
- [ ] Ticket description content
- [ ] Ticket metadata section
- [ ] Priority badge
- [ ] Status badge
- [ ] Category display
- [ ] Queue display
- [ ] Source display
- [ ] Assignee display with avatar
- [ ] Requester display with avatar
- [ ] Tags display
- [ ] SLA deadline display and countdown
- [ ] Created/updated timestamps
- [ ] Attachment list
- [ ] Attachment thumbnails
- [ ] Comments section header
- [ ] Comment cards
- [ ] Comment author and timestamp
- [ ] Comment content
- [ ] Comment input textarea
- [ ] Comment submit button
- [ ] Timeline / activity log
- [ ] Timeline event items
- [ ] Timeline event icons
- [ ] Timeline event timestamps
- [ ] Timeline event descriptions
- [ ] Linked items section
- [ ] Linked ticket/incident references
- [ ] Action buttons (Edit, Assign, Escalate, Resolve, Close)
- [ ] Status transition buttons

### 3.6 Incident War Room -- Dark Mode
- [ ] Page header
- [ ] Incident severity badge
- [ ] Incident status badge
- [ ] Incident title
- [ ] Affected services list
- [ ] Affected service status indicators
- [ ] Incident start time
- [ ] Incident resolution time
- [ ] Root cause display
- [ ] Timeline section
- [ ] Timeline entries
- [ ] Timeline entry timestamps
- [ ] Timeline entry descriptions
- [ ] Timeline entry severity indicators
- [ ] Linked ticket reference
- [ ] Action buttons
- [ ] Communication panel
- [ ] War room participants list
- [ ] Status update form
- [ ] Severity change controls

### 3.7 Request -- Dark Mode
- [ ] Request list page background
- [ ] Request list table
- [ ] Request type badges
- [ ] Request status badges
- [ ] Request detail page
- [ ] Request form data display
- [ ] Business justification text
- [ ] Approval/rejection buttons
- [ ] Timeline entries
- [ ] Request creation form

### 3.8 Knowledge Base -- Dark Mode
- [ ] Article list page background
- [ ] Article cards
- [ ] Article title text
- [ ] Article category badge
- [ ] Article tags
- [ ] Article content area
- [ ] Article content: headings
- [ ] Article content: paragraphs
- [ ] Article content: code blocks
- [ ] Article content: lists
- [ ] Article content: links
- [ ] Article editor
- [ ] Article search input
- [ ] Category filter

### 3.9 SLA & Workflows -- Dark Mode
- [ ] SLA policy list
- [ ] SLA policy cards
- [ ] SLA countdown timers
- [ ] SLA breach indicators (red)
- [ ] SLA warning indicators (amber)
- [ ] SLA on-track indicators (green)
- [ ] Workflow list
- [ ] Workflow cards
- [ ] Workflow status (active/inactive)
- [ ] Workflow trigger badges
- [ ] Workflow action badges
- [ ] Automation builder canvas
- [ ] Automation builder node cards
- [ ] Automation builder connection lines
- [ ] Automation builder property panels

### 3.10 Layout Components -- Dark Mode
- [ ] Top nav bar: background
- [ ] Top nav bar: border
- [ ] Top nav bar: brand text
- [ ] Top nav bar: action buttons
- [ ] Top nav bar: search input
- [ ] Sidebar (if added): background
- [ ] Sidebar: border
- [ ] Sidebar: nav item text
- [ ] Sidebar: nav item active state
- [ ] Sidebar: nav item hover state
- [ ] Sidebar: section headers
- [ ] Footer (if applicable)
- [ ] Offline banner

### 3.11 Scrollbar -- Dark Mode
- [ ] Scrollbar track color
- [ ] Scrollbar thumb color
- [ ] Scrollbar thumb hover color
- [ ] All scrollable containers

---

## 4. Core Features

### 4.1 Dashboard
- [ ] Dashboard page/view implemented
- [ ] Total tickets KPI card
- [ ] Open tickets KPI card
- [ ] Unassigned tickets KPI card
- [ ] Average resolution time KPI card
- [ ] SLA compliance rate KPI card
- [ ] First response time KPI card
- [ ] Tickets created today count
- [ ] Tickets resolved today count
- [ ] Tickets by priority chart (pie/donut)
- [ ] Tickets by status chart (bar)
- [ ] Tickets by category chart
- [ ] Tickets by queue chart
- [ ] Tickets by source chart
- [ ] Tickets trend chart (daily/weekly)
- [ ] SLA compliance trend chart
- [ ] Resolution time trend chart
- [ ] Recent activity feed (last 20 events)
- [ ] Activity feed: ticket created events
- [ ] Activity feed: ticket updated events
- [ ] Activity feed: ticket resolved events
- [ ] Activity feed: incident created events
- [ ] Activity feed: comment added events
- [ ] Activity feed: assignment changed events
- [ ] Top assignees by ticket count
- [ ] Queue depth by queue
- [ ] Overdue tickets list (SLA breached)
- [ ] Quick actions: create ticket
- [ ] Quick actions: create incident
- [ ] Quick actions: view queue
- [ ] Dashboard auto-refresh interval
- [ ] Dashboard loading state
- [ ] Dashboard error state
- [ ] Dashboard empty state

### 4.2 Ticket Management -- List View
- [ ] Ticket list page implemented
- [ ] Display all tickets in table format
- [ ] Table columns: ID, Title, Status, Priority, Category, Assignee, Queue, Source, SLA, Created, Updated
- [ ] Filter by status (open, acknowledged, in_progress, waiting, escalated, resolved, closed)
- [ ] Filter by priority (P1 critical, P2 high, P3 medium, P4 low)
- [ ] Filter by priority level (P1, P2, P3, P4)
- [ ] Filter by category
- [ ] Filter by queue
- [ ] Filter by source (web_portal, email_ingestion, api_integrations, monitoring_alerts, security_alerts, automation_workflows, external_systems)
- [ ] Filter by assignee
- [ ] Filter by requester
- [ ] Filter by date range (created)
- [ ] Filter by date range (updated)
- [ ] Filter by SLA status (within SLA, at risk, breached)
- [ ] Filter by tags
- [ ] Search by title (full-text)
- [ ] Search by description (full-text)
- [ ] Search by ticket ID
- [ ] Sort by created date (newest/oldest)
- [ ] Sort by updated date
- [ ] Sort by priority (highest/lowest)
- [ ] Sort by status
- [ ] Sort by SLA deadline
- [ ] Sort by title (alphabetical)
- [ ] Pagination (configurable items per page)
- [ ] Items per page selector (10, 25, 50, 100)
- [ ] Total ticket count display
- [ ] Active filters display (removable chips)
- [ ] Clear all filters button
- [ ] Save filter presets
- [ ] Quick filter: "My Tickets" (assigned to current user)
- [ ] Quick filter: "Unassigned" (no assignee)
- [ ] Quick filter: "Overdue" (SLA breached)
- [ ] Quick filter: "High Priority" (P1 + P2)
- [ ] Bulk selection (checkbox per row)
- [ ] Bulk action: assign to user
- [ ] Bulk action: change status
- [ ] Bulk action: change priority
- [ ] Bulk action: change queue
- [ ] Bulk action: add tags
- [ ] Bulk action: close tickets
- [ ] Bulk action: delete tickets
- [ ] Row click navigates to ticket detail
- [ ] Row action menu (edit, assign, close, delete)
- [ ] Ticket list loading state
- [ ] Ticket list error state
- [ ] Ticket list empty state

### 4.3 Ticket Management -- Creation
- [ ] Create ticket form/modal
- [ ] Title input (required, min 5 chars)
- [ ] Description textarea (required, supports markdown)
- [ ] Category select
- [ ] Queue select
- [ ] Source select (defaults to web_portal)
- [ ] Priority select (P1-P4, default P3)
- [ ] Priority level select (P1-P4)
- [ ] Assignee select (search from org users)
- [ ] Requester select (defaults to current user)
- [ ] Tags input (multi-tag, autocomplete from existing tags)
- [ ] Attachments upload (drag-and-drop)
- [ ] Attachments: file type validation
- [ ] Attachments: file size limit
- [ ] Attachments: preview before submit
- [ ] SLA deadline auto-set based on priority + SLA policy
- [ ] Linked items: link to existing ticket/incident
- [ ] Form validation messages
- [ ] Submit button creates ticket
- [ ] Cancel button discards form
- [ ] Success notification on creation
- [ ] Error handling on creation failure
- [ ] Redirect to ticket detail after creation

### 4.4 Ticket Management -- Detail View
- [ ] Ticket detail page implemented
- [ ] Ticket ID display
- [ ] Ticket title (editable inline)
- [ ] Ticket description (editable, markdown rendering)
- [ ] Ticket status badge with transition dropdown
- [ ] Status workflow: open -> acknowledged -> in_progress -> waiting -> escalated -> resolved -> closed
- [ ] Status transition validation (not all transitions allowed)
- [ ] Status transition: record in timeline
- [ ] Priority badge (editable)
- [ ] Priority change: record in timeline
- [ ] Category display (editable)
- [ ] Queue display (editable)
- [ ] Source display (read-only)
- [ ] Assignee display with avatar (editable)
- [ ] Assignment change: record in timeline
- [ ] Requester display with avatar
- [ ] Tags display (editable, add/remove)
- [ ] SLA deadline display
- [ ] SLA countdown timer (live)
- [ ] SLA status indicator (on track / at risk / breached)
- [ ] Created at timestamp
- [ ] Updated at timestamp
- [ ] Attachments list
- [ ] Attachment: download button
- [ ] Attachment: preview (images)
- [ ] Attachment: upload new attachment
- [ ] Linked items section
- [ ] Link: add link to another ticket
- [ ] Link: add link to incident
- [ ] Link: relationship type (blocks, blocked_by, duplicate, related)
- [ ] Link: remove link
- [ ] Link: navigate to linked item

### 4.5 Ticket Management -- Comments
- [ ] Comments section in ticket detail
- [ ] Comment list (chronological)
- [ ] Comment: author name and avatar
- [ ] Comment: timestamp
- [ ] Comment: content (markdown rendered)
- [ ] Comment: edit own comment
- [ ] Comment: delete own comment (with confirmation)
- [ ] Comment: admin can delete any comment
- [ ] Add comment: textarea with markdown support
- [ ] Add comment: @mention users
- [ ] Add comment: emoji reactions
- [ ] Add comment: attachment upload
- [ ] Add comment: preview before posting
- [ ] Add comment: submit button
- [ ] Internal comment (visible to team only, not requester)
- [ ] Comment count display
- [ ] Comment notification to mentioned users

### 4.6 Ticket Management -- Timeline / Activity Log
- [ ] Timeline section in ticket detail
- [ ] Timeline: ticket created event
- [ ] Timeline: status changed event (old -> new)
- [ ] Timeline: priority changed event
- [ ] Timeline: assignee changed event
- [ ] Timeline: category changed event
- [ ] Timeline: queue changed event
- [ ] Timeline: tag added/removed event
- [ ] Timeline: comment added event
- [ ] Timeline: attachment added event
- [ ] Timeline: link added/removed event
- [ ] Timeline: SLA started event
- [ ] Timeline: SLA breached event
- [ ] Timeline: escalation event
- [ ] Timeline: workflow triggered event
- [ ] Timeline event: timestamp
- [ ] Timeline event: actor (who made the change)
- [ ] Timeline event: icon per event type
- [ ] Timeline event: description
- [ ] Timeline: filter by event type
- [ ] Timeline: chronological order (newest first or oldest first toggle)

### 4.7 Incident Management
- [ ] Incident list view
- [ ] Incident list: columns (ID, Title, Severity, Status, Affected Services, Start Time, Resolution Time)
- [ ] Incident list: filter by severity (sev1, sev2, sev3, sev4)
- [ ] Incident list: filter by status (detected, acknowledged, investigating, mitigating, resolved, postmortem)
- [ ] Incident list: search by title
- [ ] Incident list: sort by start time
- [ ] Incident list: sort by severity
- [ ] Incident list: pagination
- [ ] Incident creation form
- [ ] Incident creation: title (required)
- [ ] Incident creation: severity select (sev1-sev4)
- [ ] Incident creation: affected services (multi-select)
- [ ] Incident creation: start time
- [ ] Incident creation: initial status
- [ ] Incident creation: linked ticket
- [ ] Incident detail / war room view
- [ ] War room: incident info header
- [ ] War room: severity badge
- [ ] War room: status badge with transition
- [ ] War room: affected services list with status
- [ ] War room: start time and duration counter
- [ ] War room: resolution time (when resolved)
- [ ] War room: root cause entry (when resolved)
- [ ] War room: timeline / updates log
- [ ] War room: add update entry
- [ ] War room: linked ticket reference
- [ ] War room: severity escalation/de-escalation
- [ ] War room: real-time updates (SSE/WebSocket)
- [ ] War room: Meet integration (start war room meeting)
- [ ] Postmortem template and editor
- [ ] Postmortem: incident summary
- [ ] Postmortem: impact assessment
- [ ] Postmortem: root cause analysis
- [ ] Postmortem: corrective actions
- [ ] Postmortem: lessons learned
- [ ] Incident loading state
- [ ] Incident error state
- [ ] Incident empty state

### 4.8 Request Management
- [ ] Request list view
- [ ] Request list: columns (ID, Type, Title, Status, Created, Updated)
- [ ] Request list: filter by type
- [ ] Request list: filter by status (submitted, approved, rejected, in_progress, fulfilled, closed)
- [ ] Request list: search by title
- [ ] Request list: sort by date
- [ ] Request list: pagination
- [ ] Request creation form
- [ ] Request creation: request type select
- [ ] Request creation: title (required)
- [ ] Request creation: business justification (required)
- [ ] Request creation: dynamic form fields based on type
- [ ] Request creation: form data (JSON)
- [ ] Request detail view
- [ ] Request detail: type and title
- [ ] Request detail: status badge with transition
- [ ] Request detail: business justification
- [ ] Request detail: form data display
- [ ] Request detail: timeline
- [ ] Request detail: approve button (for approvers)
- [ ] Request detail: reject button with reason
- [ ] Request detail: fulfill button
- [ ] Request detail: close button
- [ ] Request loading state
- [ ] Request error state
- [ ] Request empty state

### 4.9 Queue Management
- [ ] Queue list view
- [ ] Queue creation: name, description
- [ ] Queue editing
- [ ] Queue deletion (with reassignment of tickets)
- [ ] Queue depth display (ticket count per queue)
- [ ] Assign ticket to queue
- [ ] Queue-based ticket views
- [ ] Queue-based notifications
- [ ] Default queue configuration

### 4.10 Knowledge Base
- [ ] Knowledge base article list
- [ ] Article list: search by title/content
- [ ] Article list: filter by category
- [ ] Article list: filter by tags
- [ ] Article list: sort by date, title
- [ ] Article creation form
- [ ] Article creation: title (required)
- [ ] Article creation: category select
- [ ] Article creation: content (markdown editor)
- [ ] Article creation: tags (multi-tag)
- [ ] Article detail view
- [ ] Article detail: rendered markdown content
- [ ] Article detail: category badge
- [ ] Article detail: tags display
- [ ] Article detail: created/updated timestamps
- [ ] Article editing
- [ ] Article deletion (with confirmation)
- [ ] Article search (full-text)
- [ ] Link knowledge article to ticket
- [ ] Article suggestion when creating ticket (based on title/description)
- [ ] Article loading state
- [ ] Article error state
- [ ] Article empty state

### 4.11 SLA Management
- [ ] SLA policy list
- [ ] SLA policy creation: name, priority, response time, resolution time
- [ ] SLA policy editing
- [ ] SLA policy deletion
- [ ] SLA policy: response time in minutes
- [ ] SLA policy: resolution time in minutes
- [ ] SLA auto-applied to tickets based on priority
- [ ] SLA countdown display on ticket
- [ ] SLA breach alert (ticket breaches SLA)
- [ ] SLA approaching alert (80% of SLA time elapsed)
- [ ] SLA metrics: compliance rate per queue
- [ ] SLA metrics: compliance rate per priority
- [ ] SLA metrics: average response time
- [ ] SLA metrics: average resolution time
- [ ] SLA report generation

### 4.12 Workflow / Automation
- [ ] Workflow list view
- [ ] Workflow creation: name, description, trigger, conditions, actions
- [ ] Workflow editing
- [ ] Workflow deletion
- [ ] Workflow enable/disable toggle
- [ ] Workflow triggers: ticket_created
- [ ] Workflow triggers: ticket_updated
- [ ] Workflow triggers: incident_created
- [ ] Workflow triggers: request_created
- [ ] Workflow conditions: priority matches
- [ ] Workflow conditions: category matches
- [ ] Workflow conditions: source matches
- [ ] Workflow conditions: custom field matches
- [ ] Workflow actions: assign_team
- [ ] Workflow actions: assign_queue
- [ ] Workflow actions: notify (email, in-app)
- [ ] Workflow actions: start_sla
- [ ] Workflow actions: set_priority
- [ ] Workflow actions: set_assignee
- [ ] Workflow actions: add_tag
- [ ] Automation builder visual editor (if applicable)
- [ ] Automation builder: drag-and-drop nodes
- [ ] Automation builder: connect nodes
- [ ] Automation builder: configure node properties
- [ ] Automation builder: test workflow
- [ ] Workflow execution log
- [ ] Workflow error handling

### 4.13 Search & Filter
- [ ] Global search bar
- [ ] Global search: search across tickets, incidents, requests, articles
- [ ] Global search: results grouped by type
- [ ] Global search: keyboard shortcut (Cmd+K or /)
- [ ] Advanced search: field-specific queries
- [ ] Advanced search: boolean operators (AND, OR, NOT)
- [ ] Advanced search: date range queries
- [ ] Search results: highlighted matches
- [ ] Search results: result count
- [ ] Search results: click to navigate
- [ ] Saved searches
- [ ] Recent searches

### 4.14 Keyboard Shortcuts
- [ ] `n` -- new ticket
- [ ] `i` -- new incident
- [ ] `/` or `Cmd+K` -- focus search
- [ ] `j` / `k` -- navigate ticket list up/down
- [ ] `Enter` -- open selected ticket
- [ ] `Escape` -- close modal/panel
- [ ] `a` -- assign ticket (when viewing detail)
- [ ] `s` -- change status (when viewing detail)
- [ ] `p` -- change priority (when viewing detail)
- [ ] `c` -- add comment (when viewing detail)
- [ ] `Cmd+Enter` -- submit form
- [ ] `?` -- show keyboard shortcut help
- [ ] Keyboard shortcut help modal/panel

### 4.15 Markdown Support
- [ ] Markdown rendering in ticket descriptions
- [ ] Markdown rendering in comments
- [ ] Markdown rendering in knowledge base articles
- [ ] Markdown preview toggle in editors
- [ ] Markdown toolbar (bold, italic, code, link, list, heading)
- [ ] Markdown: code blocks with syntax highlighting
- [ ] Markdown: images (inline from attachments)
- [ ] Markdown: tables
- [ ] Markdown: task lists (checkboxes)
- [ ] Markdown: @mentions
- [ ] Markdown: emojis

### 4.16 Notifications & Alerts
- [ ] In-app notification panel/page
- [ ] Notification bell icon with unread count
- [ ] Notification: ticket assigned to you
- [ ] Notification: ticket you watch was updated
- [ ] Notification: new comment on your ticket
- [ ] Notification: @mention in comment
- [ ] Notification: SLA approaching (80% elapsed)
- [ ] Notification: SLA breached
- [ ] Notification: ticket escalated
- [ ] Notification: incident created (on-call team)
- [ ] Notification: request needs your approval
- [ ] Notification: request approved/rejected
- [ ] Notification: workflow triggered
- [ ] Notification: mark as read
- [ ] Notification: mark all as read
- [ ] Notification: dismiss notification
- [ ] Notification: click to navigate to source
- [ ] Notification preferences per type
- [ ] Notification sound option
- [ ] Desktop/browser notification permission
- [ ] Desktop notification for high priority events
- [ ] Email notification delivery
- [ ] Email digest (daily summary)
- [ ] Notification loading state
- [ ] Notification empty state

### 4.17 Reporting & Analytics
- [ ] Analytics dashboard/page
- [ ] Ticket volume over time chart (daily/weekly/monthly)
- [ ] Ticket volume by category chart
- [ ] Ticket volume by source chart
- [ ] Ticket volume by queue chart
- [ ] Resolution time distribution chart
- [ ] First response time distribution chart
- [ ] SLA compliance rate over time chart
- [ ] SLA compliance by priority chart
- [ ] SLA compliance by queue chart
- [ ] Agent performance: tickets resolved per agent
- [ ] Agent performance: average resolution time per agent
- [ ] Agent performance: SLA compliance per agent
- [ ] Agent performance: customer satisfaction per agent
- [ ] Backlog trend chart (open tickets over time)
- [ ] Priority distribution chart (pie/donut)
- [ ] Status distribution chart
- [ ] Top 10 ticket categories
- [ ] Top 10 ticket requesters
- [ ] Incident count and severity over time
- [ ] Mean time to resolve (MTTR) by severity
- [ ] Mean time to detect (MTTD)
- [ ] Export analytics as CSV
- [ ] Export analytics as PDF
- [ ] Date range selector for all analytics
- [ ] Analytics loading state
- [ ] Analytics empty state (no data)

### 4.18 Settings Page
- [ ] Settings page/view
- [ ] Organization settings: org name, timezone
- [ ] Ticket settings: default priority
- [ ] Ticket settings: default queue
- [ ] Ticket settings: auto-assignment rules
- [ ] Ticket settings: required fields configuration
- [ ] SLA settings: manage SLA policies
- [ ] Queue settings: manage queues
- [ ] Workflow settings: manage workflows
- [ ] Notification settings: per-type toggles
- [ ] Notification settings: email delivery toggle
- [ ] Notification settings: sound toggle
- [ ] Display settings: default ticket list view (table/cards)
- [ ] Display settings: default items per page
- [ ] Display settings: compact/comfortable density
- [ ] Display settings: theme (light/dark/system)
- [ ] Integration settings: EventBus configuration
- [ ] Integration settings: Meet bridge configuration
- [ ] Integration settings: email ingestion configuration
- [ ] Save settings confirmation
- [ ] Reset to defaults

### 4.19 Bulk Operations
- [ ] Select all tickets on current page
- [ ] Select all tickets matching current filter
- [ ] Deselect all
- [ ] Bulk assign to user
- [ ] Bulk change status
- [ ] Bulk change priority
- [ ] Bulk change queue
- [ ] Bulk add tags
- [ ] Bulk remove tags
- [ ] Bulk close tickets
- [ ] Bulk delete tickets (with confirmation)
- [ ] Bulk action confirmation dialog (shows count)
- [ ] Bulk action progress indicator
- [ ] Bulk action success/error summary
- [ ] Undo bulk action (within 30 seconds)

---

## 5. API Integration

### 5.1 API Client Setup
- [ ] API client module created
- [ ] Base URL from environment variable
- [ ] Authorization header from Gate token
- [ ] X-Org-Id header from localStorage
- [ ] X-Workspace-Id header from localStorage
- [ ] X-User-Id header (or from token)
- [ ] X-User-Role header (or from token)
- [ ] 401 handler: redirect to login
- [ ] 403 handler: show forbidden message
- [ ] Error handling: network errors
- [ ] Error handling: timeout
- [ ] Request/response logging (dev only)

### 5.2 Auth Integration
- [x] Gate auth mode configurable (headers, gate, hybrid)
- [x] Gate userinfo endpoint configured
- [x] Actor resolution from Gate token
- [x] Actor resolution from headers (dev mode)
- [ ] Frontend: Gate OAuth PKCE flow
- [ ] Frontend: token storage
- [ ] Frontend: token refresh
- [ ] Frontend: auto-logout on expiry

### 5.3 Ticket API Endpoints
- [ ] GET `/api/tickets` -- list tickets (with filters, pagination, sort)
- [ ] POST `/api/tickets` -- create ticket
- [ ] GET `/api/tickets/:id` -- get ticket detail
- [ ] PUT `/api/tickets/:id` -- update ticket
- [ ] DELETE `/api/tickets/:id` -- delete ticket
- [ ] PATCH `/api/tickets/:id/status` -- change status
- [ ] PATCH `/api/tickets/:id/priority` -- change priority
- [ ] PATCH `/api/tickets/:id/assign` -- assign ticket
- [ ] POST `/api/tickets/:id/comments` -- add comment
- [ ] GET `/api/tickets/:id/comments` -- list comments
- [ ] PUT `/api/tickets/:id/comments/:commentId` -- edit comment
- [ ] DELETE `/api/tickets/:id/comments/:commentId` -- delete comment
- [ ] POST `/api/tickets/:id/attachments` -- upload attachment
- [ ] DELETE `/api/tickets/:id/attachments/:attachmentId` -- delete attachment
- [ ] POST `/api/tickets/:id/links` -- add link
- [ ] DELETE `/api/tickets/:id/links/:linkId` -- remove link
- [ ] GET `/api/tickets/:id/timeline` -- get activity timeline
- [ ] POST `/api/tickets/bulk` -- bulk actions
- [ ] GET `/api/tickets/search` -- full-text search
- [ ] GET `/api/tickets/export` -- export as CSV

### 5.4 Incident API Endpoints
- [ ] GET `/api/incidents` -- list incidents
- [ ] POST `/api/incidents` -- create incident
- [ ] GET `/api/incidents/:id` -- get incident detail
- [ ] PUT `/api/incidents/:id` -- update incident
- [ ] PATCH `/api/incidents/:id/severity` -- change severity
- [ ] PATCH `/api/incidents/:id/status` -- change status
- [ ] POST `/api/incidents/:id/timeline` -- add timeline entry
- [ ] GET `/api/incidents/:id/timeline` -- get timeline

### 5.5 Request API Endpoints
- [ ] GET `/api/requests` -- list requests
- [ ] POST `/api/requests` -- create request
- [ ] GET `/api/requests/:id` -- get request detail
- [ ] PUT `/api/requests/:id` -- update request
- [ ] PATCH `/api/requests/:id/approve` -- approve request
- [ ] PATCH `/api/requests/:id/reject` -- reject request
- [ ] PATCH `/api/requests/:id/fulfill` -- fulfill request

### 5.6 Queue API Endpoints
- [ ] GET `/api/queues` -- list queues
- [ ] POST `/api/queues` -- create queue
- [ ] PUT `/api/queues/:id` -- update queue
- [ ] DELETE `/api/queues/:id` -- delete queue

### 5.7 Knowledge Base API Endpoints
- [ ] GET `/api/knowledge` -- list articles
- [ ] POST `/api/knowledge` -- create article
- [ ] GET `/api/knowledge/:id` -- get article
- [ ] PUT `/api/knowledge/:id` -- update article
- [ ] DELETE `/api/knowledge/:id` -- delete article
- [ ] GET `/api/knowledge/search` -- search articles

### 5.8 SLA API Endpoints
- [ ] GET `/api/sla-policies` -- list SLA policies
- [ ] POST `/api/sla-policies` -- create SLA policy
- [ ] PUT `/api/sla-policies/:id` -- update SLA policy
- [ ] DELETE `/api/sla-policies/:id` -- delete SLA policy

### 5.9 Workflow API Endpoints
- [ ] GET `/api/workflows` -- list workflows
- [ ] POST `/api/workflows` -- create workflow
- [ ] PUT `/api/workflows/:id` -- update workflow
- [ ] DELETE `/api/workflows/:id` -- delete workflow
- [ ] PATCH `/api/workflows/:id/toggle` -- enable/disable workflow
- [ ] POST `/api/workflows/:id/test` -- test workflow

### 5.10 Dashboard / Analytics API
- [ ] GET `/api/dashboard/summary` -- dashboard KPIs
- [ ] GET `/api/dashboard/charts` -- chart data
- [ ] GET `/api/analytics/tickets` -- ticket analytics
- [ ] GET `/api/analytics/sla` -- SLA analytics
- [ ] GET `/api/analytics/agents` -- agent performance

### 5.11 EventBus Integration
- [x] Event publish enabled (configurable)
- [x] Event sink URL configurable
- [x] Event consumer enabled (configurable)
- [x] Redis stream backend for events
- [x] Consumer event types defined (mail.ticket.intake, connect.ticket.intake, etc.)
- [x] Dead letter queue prefix configured
- [x] Consumer worker configurable
- [ ] Publish: ticket.created event
- [ ] Publish: ticket.updated event
- [ ] Publish: ticket.resolved event
- [ ] Publish: ticket.escalated event
- [ ] Publish: incident.created event
- [ ] Publish: incident.resolved event
- [ ] Consume: mail.ticket.intake (auto-create ticket from email)
- [ ] Consume: connect.ticket.intake (auto-create from chat)
- [ ] Consume: ticket.create.external (cross-app ticket creation)
- [ ] Consume: ticket.status.sync (status sync from external)
- [ ] SSE/WebSocket for real-time frontend updates
- [ ] Real-time ticket list updates
- [ ] Real-time incident war room updates
- [ ] Real-time comment notifications

### 5.12 Meet Bridge Integration
- [x] Meet bridge enabled (configurable)
- [x] Meet web URL configured
- [ ] Start Meet room from incident war room
- [ ] Link Meet session to incident
- [ ] Meet recording linked to incident postmortem

---

## 6. State Management

### 6.1 Vanilla JS State (Current)
- [ ] Define state management approach for vanilla JS
- [ ] Global state object for app state
- [ ] State: current view (dashboard, tickets, incidents, requests, etc.)
- [ ] State: current user (from auth)
- [ ] State: ticket list (array)
- [ ] State: filters (priority, status, category, queue, etc.)
- [ ] State: sort settings (field, direction)
- [ ] State: pagination (page, limit, total)
- [ ] State: selected ticket (for detail view)
- [ ] State: incidents list
- [ ] State: requests list
- [ ] State: knowledge articles list
- [ ] State: SLA policies list
- [ ] State: workflows list
- [ ] State: queues list
- [ ] State: loading states per section
- [ ] State: error states per section
- [ ] State: theme (light/dark)
- [ ] State change triggers DOM re-render
- [ ] Event-based state updates (custom events)

### 6.2 Zustand Store (If React Migration)
- [ ] Create `src/store/useTicketStore.ts`
- [ ] Store: tickets list
- [ ] Store: selected ticket
- [ ] Store: filters
- [ ] Store: sort settings
- [ ] Store: pagination
- [ ] Store: loading states
- [ ] Store: error states
- [ ] Create `src/store/useIncidentStore.ts`
- [ ] Create `src/store/useRequestStore.ts`
- [ ] Create `src/store/useKnowledgeStore.ts`
- [ ] Create `src/store/useUIStore.ts`
- [ ] Store persistence for preferences
- [ ] Derived selectors: filtered tickets
- [ ] Derived selectors: ticket counts by status
- [ ] Derived selectors: ticket counts by priority
- [ ] Derived selectors: overdue tickets

---

## 7. Performance

### 7.1 Frontend Performance (Vanilla)
- [ ] Minimize DOM manipulation (batch updates)
- [ ] Use DocumentFragment for list rendering
- [ ] Event delegation for table rows
- [ ] Debounced search input (300ms)
- [ ] Lazy render long ticket lists (virtual scrolling)
- [ ] Cache API responses in memory
- [ ] Avoid layout thrashing (read/write separation)
- [ ] Minimize CSS recalculations
- [ ] Use requestAnimationFrame for animations
- [ ] Compress images/attachments

### 7.2 Frontend Performance (React -- if migrated)
- [ ] All views lazy-loaded with React.lazy()
- [ ] Suspense boundaries with Skeleton fallbacks
- [ ] Vendor chunk splitting (react, react-dom, @orbit-ui/react)
- [ ] Bundle size < 500KB gzipped
- [ ] Virtual scrolling for ticket lists (>100 items)
- [ ] React.memo on pure components
- [ ] useMemo for filtered/sorted lists
- [ ] useCallback for event handlers
- [ ] Debounced search input
- [ ] Memoized badge/status lookups

### 7.3 Network Performance
- [ ] API response caching
- [ ] Pagination instead of loading all tickets
- [ ] Conditional requests (ETag/If-None-Match)
- [ ] Prefetch ticket detail on hover
- [ ] Compress API responses (gzip/brotli)
- [ ] Service worker for static asset caching
- [ ] Offline support: cache last-fetched ticket list

### 7.4 Rendering Performance
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
- [ ] Focus visible indicator on all elements
- [ ] Skip to main content link
- [ ] Escape closes modals/dropdowns/panels
- [ ] Enter/Space activates buttons and links
- [ ] Arrow keys in menus, lists, tables
- [ ] Table row keyboard navigation
- [ ] Table column sort via keyboard
- [ ] Modal trap focus
- [ ] Dropdown menu keyboard navigation
- [ ] Custom keyboard shortcuts (documented above)
- [ ] Keyboard shortcut help (? key)
- [ ] Ticket list: j/k navigation
- [ ] Search: / to focus

### 8.2 Screen Reader Support
- [ ] All images have alt text
- [ ] All icons have aria-labels or aria-hidden
- [ ] All form inputs have labels
- [ ] All form inputs have aria-describedby for errors
- [ ] Navigation uses `<nav>` with aria-label
- [ ] Main content uses `<main>` landmark
- [ ] Tables have `<caption>` or aria-label
- [ ] Table headers use `<th>` with scope
- [ ] Sort direction via aria-sort
- [ ] Loading states announced (aria-live)
- [ ] Ticket status changes announced
- [ ] SLA breach alerts announced
- [ ] Comment additions announced
- [ ] Page title updates on view change
- [ ] Priority badges have text labels (not just color)
- [ ] Status badges have text labels
- [ ] Timeline events announced
- [ ] Markdown content semantic HTML

### 8.3 Color & Contrast
- [ ] All text meets 4.5:1 contrast ratio
- [ ] Large text meets 3:1 contrast ratio
- [ ] Interactive elements meet 3:1 contrast
- [ ] Priority not solely indicated by color (P1/P2/P3/P4 text labels)
- [ ] Status not solely indicated by color (text labels)
- [ ] Severity not solely indicated by color (text + icon)
- [ ] SLA status not solely indicated by color (icon + text)
- [ ] Charts accessible without color (patterns/labels)
- [ ] Focus ring visible on all backgrounds
- [ ] Error messages not just red
- [ ] Success messages not just green

### 8.4 Forms & Inputs
- [ ] All fields have visible labels
- [ ] Required fields indicated
- [ ] Error messages adjacent to field
- [ ] Error messages descriptive
- [ ] Autocomplete attributes
- [ ] Correct input types
- [ ] Placeholder not sole label

### 8.5 Motion & Animation
- [ ] `prefers-reduced-motion` respected
- [ ] SLA countdown timer respects motion preference
- [ ] Real-time feed updates smooth (not jarring)
- [ ] No flashing content

### 8.6 Responsive Accessibility
- [ ] Content readable at 200% zoom
- [ ] Content readable at 400% zoom
- [ ] No horizontal scroll at 320px
- [ ] Touch targets min 44x44px
- [ ] Tap target spacing min 8px

### 8.7 Data Table Accessibility
- [ ] Ticket table: column headers announced
- [ ] Ticket table: sort state announced (aria-sort)
- [ ] Ticket table: row selection announced
- [ ] Ticket table: pagination controls have aria-labels
- [ ] Incident table: all headers and cells associated
- [ ] Request table: all headers and cells associated
- [ ] Knowledge base table: all headers and cells associated
- [ ] Empty table: "No data" announced
- [ ] Table loading: "Loading" announced (aria-busy)
- [ ] Bulk selection: count announced to screen reader

### 8.8 Status & Priority Accessibility
- [ ] All priority levels have text labels (not just color/icon)
- [ ] P1 Critical: text + icon + color
- [ ] P2 High: text + icon + color
- [ ] P3 Medium: text + icon + color
- [ ] P4 Low: text + icon + color
- [ ] All statuses have text labels
- [ ] Status transitions: new status announced
- [ ] SLA status: time remaining announced
- [ ] SLA breach: alert announced immediately
- [ ] Incident severity: text + icon + color
- [ ] Timeline events: each event announced with context

### 8.9 Rich Content Accessibility
- [ ] Markdown rendered content uses semantic HTML (h1-h6, ul, ol, code, etc.)
- [ ] Code blocks have language announced
- [ ] Links in rendered content have descriptive text
- [ ] Images in content have alt text
- [ ] Task lists have proper checkbox semantics
- [ ] @mentions link to user profiles

---

## 9. Mobile & Responsive

### 9.1 Breakpoint Strategy
- [ ] Mobile: 0-639px
- [ ] Tablet: 640-1023px
- [ ] Desktop: 1024px+
- [ ] All breakpoints tested

### 9.2 Layout Responsive Behavior
- [ ] Navigation: hamburger menu on mobile
- [ ] Navigation: sidebar slide-in on mobile
- [ ] Navigation: persistent sidebar on desktop
- [ ] Ticket list: card view on mobile (instead of table)
- [ ] Ticket list: simplified columns on tablet
- [ ] Ticket list: full table on desktop
- [ ] Ticket detail: single column on mobile
- [ ] Ticket detail: two-column on desktop (info + timeline)
- [ ] Dashboard: KPI cards stack on mobile
- [ ] Dashboard: charts full width on mobile
- [ ] Incident war room: stack sections vertically on mobile
- [ ] Knowledge base: card layout adjusts
- [ ] All modals: full-screen on mobile
- [ ] Filter panel: collapsible on mobile
- [ ] Search: full-width on mobile

### 9.3 Touch Interactions
- [ ] Touch-friendly button sizes (min 44px)
- [ ] Swipe actions on ticket rows (mobile)
- [ ] Pull to refresh
- [ ] Touch-friendly dropdowns
- [ ] Touch-friendly tag input
- [ ] No hover-only interactions

### 9.4 Mobile Features
- [ ] Mobile: floating action button (create ticket)
- [ ] Mobile: bottom tab navigation
- [ ] Mobile: compact ticket cards
- [ ] Mobile: gesture navigation

---

## 10. Internationalization

### 10.1 i18n Framework
- [ ] i18n approach chosen (vanilla: simple key-value, React: react-i18next)
- [ ] Default language: English
- [ ] Language detection from browser
- [ ] Language persistence
- [ ] Language selector

### 10.2 String Extraction
- [ ] All user-facing strings extracted
- [ ] Dashboard strings
- [ ] Ticket list strings
- [ ] Ticket detail strings
- [ ] Ticket creation strings
- [ ] Incident strings
- [ ] Request strings
- [ ] Knowledge base strings
- [ ] SLA strings
- [ ] Workflow strings
- [ ] Error messages
- [ ] Empty states
- [ ] Validation messages
- [ ] Priority labels (Critical, High, Medium, Low)
- [ ] Status labels (all statuses across all entity types)
- [ ] Source labels
- [ ] Category labels

### 10.3 Date & Number Formatting
- [ ] Dates locale-aware
- [ ] Times locale-aware
- [ ] Relative times ("2 hours ago") locale-aware
- [ ] Duration formatting
- [ ] Numbers formatted with grouping

### 10.4 RTL Support
- [ ] Layout supports RTL
- [ ] Tables adjust for RTL
- [ ] Timeline adjusts for RTL
- [ ] Text alignment adjusts

---

## 11. Security

### 11.1 Authentication
- [x] Backend: Gate auth mode configurable (headers/gate/hybrid)
- [x] Backend: bearer token validation via Gate userinfo
- [x] Backend: header-based auth for development
- [ ] Frontend: Gate OAuth PKCE flow
- [ ] Frontend: token storage
- [ ] Frontend: token refresh
- [ ] Frontend: auto-logout on expiry
- [ ] Frontend: redirect to login when unauthenticated

### 11.2 Authorization
- [x] Backend: Actor model with org_id, workspace_id, user_id, role
- [x] Backend: role validation (admin, manager, member)
- [x] Backend: org isolation via X-Org-Id
- [x] Backend: workspace isolation via X-Workspace-Id
- [ ] Role-based UI (admin sees all, member sees own tickets)
- [ ] Admin: manage queues, SLA policies, workflows
- [ ] Manager: assign tickets, approve requests
- [ ] Member: create tickets, comment, update own tickets

### 11.3 Data Protection
- [ ] No sensitive data in URLs
- [ ] No sensitive data in console logs
- [ ] Org isolation on all queries (backend)
- [ ] Workspace isolation on applicable queries
- [ ] No cross-tenant data leakage
- [ ] Attachment access controlled by org/workspace
- [ ] Audit trail for ticket operations

### 11.4 Input Validation
- [ ] All form inputs validated client-side
- [ ] All inputs validated server-side
- [ ] XSS prevention: sanitize markdown before rendering
- [ ] XSS prevention: sanitize comment content
- [ ] SQL injection prevention (SQLAlchemy parameterized)
- [ ] File upload: type validation
- [ ] File upload: size limits
- [ ] File upload: malware scanning (future)

### 11.5 Network Security
- [ ] HTTPS enforced
- [ ] Content-Security-Policy header
- [ ] CORS restricted to specific origins
- [ ] Rate limiting on API endpoints
- [ ] Request size limits

### 11.6 Dependency Security
- [ ] `pip audit` clean (backend)
- [ ] `npm audit` clean (if Node frontend)
- [ ] No known vulnerabilities
- [ ] Lock files committed
- [ ] Dependabot configured

---

## 12. Testing

### 12.1 Backend Unit Tests
- [x] Test file exists (`backend/tests/test_api.py`)
- [ ] Test: create ticket
- [ ] Test: list tickets with filters
- [ ] Test: get ticket by ID
- [ ] Test: update ticket
- [ ] Test: delete ticket
- [ ] Test: change ticket status
- [ ] Test: change ticket priority
- [ ] Test: assign ticket
- [ ] Test: add comment to ticket
- [ ] Test: list ticket comments
- [ ] Test: edit comment
- [ ] Test: delete comment
- [ ] Test: ticket timeline events
- [ ] Test: bulk ticket actions
- [ ] Test: ticket search
- [ ] Test: create incident
- [ ] Test: list incidents
- [ ] Test: update incident
- [ ] Test: incident status transitions
- [ ] Test: incident timeline
- [ ] Test: create request
- [ ] Test: list requests
- [ ] Test: approve/reject request
- [ ] Test: create queue
- [ ] Test: list queues
- [ ] Test: create knowledge article
- [ ] Test: list knowledge articles
- [ ] Test: search knowledge articles
- [ ] Test: create SLA policy
- [ ] Test: SLA auto-assignment
- [ ] Test: SLA breach detection
- [ ] Test: create workflow
- [ ] Test: workflow trigger execution
- [ ] Test: workflow condition evaluation
- [ ] Test: workflow action execution
- [ ] Test: org isolation (tickets from different orgs)
- [ ] Test: workspace isolation
- [ ] Test: auth middleware (gate mode)
- [ ] Test: auth middleware (headers mode)
- [ ] Test: unauthorized access
- [ ] Test: invalid token

### 12.2 Frontend Unit Tests (Vanilla JS)
- [ ] Test: state management functions
- [ ] Test: API client functions
- [ ] Test: date formatting helpers
- [ ] Test: markdown rendering
- [ ] Test: search/filter logic
- [ ] Test: status transition validation
- [ ] Test: SLA countdown calculation
- [ ] Test: keyboard shortcut handlers

### 12.3 Frontend Component Tests (If React)
- [ ] Test: Dashboard renders KPIs
- [ ] Test: Ticket list renders
- [ ] Test: Ticket list filter functionality
- [ ] Test: Ticket list search functionality
- [ ] Test: Ticket list sort functionality
- [ ] Test: Ticket list pagination
- [ ] Test: Ticket detail renders
- [ ] Test: Ticket creation form validation
- [ ] Test: Ticket status transition
- [ ] Test: Comment CRUD
- [ ] Test: Timeline rendering
- [ ] Test: Incident list renders
- [ ] Test: Incident war room renders
- [ ] Test: Request list renders
- [ ] Test: Knowledge base renders
- [ ] Test: SLA policy management
- [ ] Test: Workflow management
- [ ] Test: Empty states
- [ ] Test: Loading states
- [ ] Test: Error states

### 12.4 Integration Tests
- [ ] Ticket CRUD flow: create -> update -> resolve -> close
- [ ] Ticket with comments: create ticket -> add comment -> edit -> delete
- [ ] Incident flow: create -> investigate -> mitigate -> resolve -> postmortem
- [ ] Request flow: create -> approve -> fulfill -> close
- [ ] SLA flow: create policy -> create ticket -> verify SLA applied
- [ ] Workflow flow: create workflow -> create ticket -> verify workflow executed
- [ ] Search: create tickets -> search -> verify results
- [ ] Bulk actions: select multiple -> apply action -> verify
- [ ] Auth: login -> perform actions -> logout

### 12.5 End-to-End Tests
- [ ] E2E framework configured
- [ ] E2E: login and view dashboard
- [ ] E2E: create ticket
- [ ] E2E: search and filter tickets
- [ ] E2E: update ticket status through workflow
- [ ] E2E: add comments to ticket
- [ ] E2E: create and manage incident
- [ ] E2E: knowledge base CRUD
- [ ] E2E: dark mode toggle
- [ ] E2E: mobile responsive layout
- [ ] E2E: keyboard navigation

### 12.6 Visual Regression Tests
- [ ] Dashboard: light mode
- [ ] Dashboard: dark mode
- [ ] Ticket list: light mode
- [ ] Ticket list: dark mode
- [ ] Ticket detail: light mode
- [ ] Ticket detail: dark mode
- [ ] Incident war room: light mode
- [ ] Incident war room: dark mode
- [ ] All pages at mobile, tablet, desktop breakpoints

### 12.7 Test Coverage
- [ ] Backend test coverage > 80%
- [ ] Frontend test coverage > 70%
- [ ] CI runs all tests on PR
- [ ] Test results in PR comments

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] Backend: all API routes documented with docstrings
- [ ] Backend: model fields documented
- [ ] Backend: Pydantic schemas documented
- [ ] Backend: workflow engine documented
- [ ] Frontend: component functions documented
- [ ] Frontend: state management documented
- [ ] Frontend: API client documented
- [ ] Complex business logic commented

### 13.2 Developer Documentation
- [x] README.md exists
- [ ] README: project overview
- [ ] README: tech stack
- [ ] README: setup instructions (frontend + backend)
- [ ] README: environment variables
- [ ] README: folder structure
- [ ] README: available scripts
- [ ] README: API documentation link
- [ ] CONTRIBUTING.md: coding standards
- [ ] CONTRIBUTING.md: PR process
- [ ] CHANGELOG.md: version history
- [ ] Architecture Decision Records (ADRs)
- [ ] ADR: vanilla JS vs React decision
- [ ] ADR: state management approach
- [ ] ADR: ticket workflow engine design

### 13.3 API Documentation
- [ ] OpenAPI/Swagger spec (FastAPI auto-generates)
- [ ] All endpoints documented with examples
- [ ] Error codes documented
- [ ] Authentication documented
- [ ] Rate limits documented
- [ ] Webhook payloads documented
- [ ] EventBus event schemas documented
- [ ] Postman/Insomnia collection

### 13.4 User Documentation
- [ ] Feature guide: ticket management
- [ ] Feature guide: incident management
- [ ] Feature guide: request management
- [ ] Feature guide: knowledge base
- [ ] Feature guide: SLA management
- [ ] Feature guide: workflow automation
- [ ] Keyboard shortcuts reference
- [ ] FAQ document

---

## 14. Deployment & CI/CD

### 14.1 Frontend Build
- [ ] Static assets optimized (minified CSS/JS)
- [ ] Images optimized
- [ ] Cache busting via file hashing (if bundled)
- [ ] Gzip/brotli compression configured on server
- [ ] If React migration: Vite production build succeeds

### 14.2 Docker
- [x] Dockerfile exists
- [ ] Dockerfile: multi-stage build
- [ ] Dockerfile: Python backend stage
- [ ] Dockerfile: static frontend serving (Nginx)
- [ ] Dockerfile: health check
- [ ] Docker compose entry
- [ ] Docker compose: port mapping (backend 45011, frontend static)
- [ ] Docker compose: volume mounts
- [ ] Docker compose: environment variables
- [ ] Docker compose: database dependency
- [ ] `.dockerignore` configured

### 14.3 CI Pipeline
- [ ] GitHub Actions workflow configured
- [ ] CI: install backend dependencies
- [ ] CI: backend lint (ruff/flake8)
- [ ] CI: backend type check (mypy)
- [ ] CI: backend tests (pytest)
- [ ] CI: frontend lint (if applicable)
- [ ] CI: frontend tests (if applicable)
- [ ] CI: frontend build (if applicable)
- [ ] CI: security audit
- [ ] CI: deploy preview on PR

### 14.4 Deployment
- [ ] Staging environment
- [ ] Production environment
- [ ] Database migration on deploy (Alembic)
- [ ] Rollback procedure
- [ ] Zero-downtime deployment
- [ ] Health check endpoint
- [ ] Error monitoring (Sentry)
- [ ] Performance monitoring
- [ ] Log aggregation

### 14.5 Environment Management
- [x] `.env.example` exists (backend)
- [ ] All environment variables documented
- [ ] `TURBOTICK_AUTH_MODE` documented (headers/gate/hybrid)
- [ ] `TURBOTICK_GATE_USERINFO_URL` documented
- [ ] `TURBOTICK_EVENT_PUBLISH_ENABLED` documented
- [ ] `TURBOTICK_EVENT_SINK_URL` documented
- [ ] `TURBOTICK_EVENT_BUS_BACKEND` documented (none/redis)
- [ ] `TURBOTICK_EVENT_STREAM_REDIS_URL` documented
- [ ] `TURBOTICK_EVENT_CONSUMER_ENABLED` documented
- [ ] `TURBOTICK_MEET_BRIDGE_ENABLED` documented
- [ ] `TURBOTICK_MEET_WEB_URL` documented
- [ ] Secrets not in git
- [ ] `.gitignore` includes env files

---

## 15. Backend

### 15.1 API Server (FastAPI)
- [x] FastAPI application initialized
- [x] Lifespan handler for startup/shutdown
- [x] Auth middleware (Gate / headers / hybrid)
- [x] Actor context variable
- [x] Request ID context variable
- [x] Unauthenticated paths defined (/health, /docs, etc.)
- [ ] Request logging middleware
- [ ] Error handling middleware (structured errors)
- [ ] Health check endpoint
- [ ] Metrics endpoint
- [ ] API versioning
- [ ] Rate limiting
- [ ] CORS configuration (production origins)
- [ ] Request size limits
- [ ] Compression middleware (gzip)

### 15.2 Database Models
- [x] Ticket model: id, org_id, workspace_id, title, description, category, queue, source, priority, priority_level, status, requester_id, assignee_id, tags, attachments, comments, links, timeline, sla_deadline, timestamps
- [x] Incident model: id, org_id, workspace_id, title, severity, status, affected_services, start_time, resolution_time, root_cause, timeline, linked_ticket_id, timestamps
- [x] Request model: id, org_id, workspace_id, request_type, title, business_justification, status, form_data, timeline, timestamps
- [x] Queue model: id, org_id, name, description, created_at
- [x] KnowledgeArticle model: id, org_id, workspace_id, title, category, content, tags, timestamps
- [x] SlaPolicy model: id, org_id, name, priority, response_time_mins, resolution_time_mins, created_at
- [x] Workflow model: id, org_id, name, description, trigger_event, conditions, actions, is_active, created_at
- [x] Indexes: org_id + workspace_id composite indexes on main tables
- [x] Indexes: org_id on SLA policies and workflows
- [ ] Migration: add user model or reference Gate users
- [ ] Migration: add attachment storage model
- [ ] Migration: add audit log table
- [ ] Migration: add search index (full-text)
- [ ] Database connection pooling
- [ ] Database backup strategy

### 15.3 API Routes Implementation
- [ ] Ticket CRUD routes
- [ ] Ticket search route (full-text)
- [ ] Ticket bulk operations route
- [ ] Ticket comment CRUD routes
- [ ] Ticket attachment routes
- [ ] Ticket link routes
- [ ] Ticket timeline route
- [ ] Ticket status transition route (with validation)
- [ ] Incident CRUD routes
- [ ] Incident timeline routes
- [ ] Request CRUD routes
- [ ] Request approval routes
- [ ] Queue CRUD routes
- [ ] Knowledge article CRUD routes
- [ ] Knowledge article search route
- [ ] SLA policy CRUD routes
- [ ] SLA enforcement logic (auto-set deadline on ticket creation)
- [ ] SLA breach detection (background task)
- [ ] Workflow CRUD routes
- [ ] Workflow execution engine
- [ ] Workflow condition evaluator
- [ ] Workflow action executor
- [ ] Dashboard aggregation routes
- [ ] Analytics routes
- [ ] Export routes (CSV)

### 15.4 Business Logic
- [ ] Ticket status workflow validation
- [ ] Ticket auto-assignment based on queue/workflow
- [ ] SLA deadline calculation from policy + priority
- [ ] SLA breach detection (periodic check)
- [ ] SLA approaching notification (80% threshold)
- [ ] Workflow trigger evaluation on ticket/incident/request events
- [ ] Workflow condition matching
- [ ] Workflow action execution
- [ ] Notification generation on ticket events
- [ ] Email notification sending
- [ ] Ticket escalation logic
- [ ] Incident severity auto-escalation
- [ ] Request approval chain logic
- [ ] Full-text search implementation (PostgreSQL tsvector or ElasticSearch)

### 15.5 EventBus Integration
- [x] Event publish configuration
- [x] Event consumer configuration
- [x] Redis stream support
- [x] Dead letter queue support
- [x] Consumer event types defined
- [x] Consumer worker configuration
- [ ] Publish: ticket CRUD events
- [ ] Publish: incident CRUD events
- [ ] Publish: request CRUD events
- [ ] Publish: SLA breach events
- [ ] Consume: create tickets from email (mail.ticket.intake)
- [ ] Consume: create tickets from chat (connect.ticket.intake)
- [ ] Consume: external ticket creation (ticket.create.external)
- [ ] Consume: status sync (ticket.status.sync)
- [ ] Event schema validation (Pydantic)
- [ ] Event replay capability
- [ ] Event consumer health monitoring

### 15.6 Meet Bridge
- [x] Meet bridge enabled flag
- [x] Meet web URL configured
- [ ] API endpoint: start Meet room for incident
- [ ] API endpoint: get Meet room status
- [ ] Link Meet room URL to incident
- [ ] Automatic Meet room creation on SEV1/SEV2 incidents

### 15.7 Backend Testing
- [x] Test file exists
- [x] Test infrastructure (pytest)
- [ ] Test database configuration (SQLite in-memory)
- [ ] Test fixtures: sample tickets
- [ ] Test fixtures: sample incidents
- [ ] Test fixtures: sample requests
- [ ] Test fixtures: sample queues
- [ ] Test fixtures: sample SLA policies
- [ ] Test fixtures: sample workflows
- [ ] Unit tests: ticket operations (30+ test cases)
- [ ] Unit tests: incident operations (15+ test cases)
- [ ] Unit tests: request operations (10+ test cases)
- [ ] Unit tests: queue operations (5+ test cases)
- [ ] Unit tests: knowledge article operations (10+ test cases)
- [ ] Unit tests: SLA logic (10+ test cases)
- [ ] Unit tests: workflow engine (20+ test cases)
- [ ] Unit tests: auth middleware (10+ test cases)
- [ ] Unit tests: org isolation (5+ test cases)
- [ ] Integration tests: full ticket lifecycle
- [ ] Integration tests: incident lifecycle
- [ ] Integration tests: request approval flow
- [ ] Integration tests: SLA enforcement
- [ ] Integration tests: workflow execution
- [ ] Integration tests: EventBus publish/consume
- [ ] Test coverage > 80%
- [ ] CI runs all tests

### 15.8 Backend Data Integrity
- [ ] Ticket ID generation: unique per org (prefixed, e.g., TT-001)
- [ ] Incident ID generation: unique per org (prefixed, e.g., INC-001)
- [ ] Request ID generation: unique per org (prefixed, e.g., REQ-001)
- [ ] Org_id never null on any record
- [ ] Workspace_id never null on tickets/incidents/requests
- [ ] Status transitions validated (not all transitions allowed)
- [ ] Priority values constrained to valid enum
- [ ] Severity values constrained to valid enum
- [ ] Tags stored as JSONB array (validated)
- [ ] Attachments stored as JSONB array (validated)
- [ ] Comments stored as JSONB array (validated structure)
- [ ] Timeline entries stored as JSONB array (append-only)
- [ ] Links stored as JSONB array (validated references)
- [ ] Cascade rules: queue deletion reassigns tickets
- [ ] Cascade rules: user deletion reassigns tickets
- [ ] Soft delete for tickets (status=closed, not hard delete)
- [ ] Audit trail: timeline records all changes
- [ ] Concurrent update handling (optimistic locking or row-level)
- [ ] Data export for compliance/audit

### 15.9 Backend API Error Handling
- [ ] Consistent error response format: `{ "detail": "...", "code": "..." }`
- [ ] 400 Bad Request: invalid input
- [ ] 401 Unauthorized: missing/invalid token
- [ ] 403 Forbidden: insufficient permissions or org mismatch
- [ ] 404 Not Found: ticket/incident/request not found
- [ ] 409 Conflict: duplicate ticket creation
- [ ] 422 Unprocessable Entity: validation errors
- [ ] 429 Too Many Requests: rate limited
- [ ] 500 Internal Server Error: unexpected failures
- [ ] Error logging with request_id and org_id
- [ ] Error monitoring (Sentry integration)
- [ ] Database errors mapped to HTTP codes
- [ ] External service errors handled gracefully
- [ ] Validation errors return field-level details

### 15.10 Backend Caching
- [ ] Cache: ticket list queries (invalidate on CRUD)
- [ ] Cache: dashboard KPIs (TTL 30s)
- [ ] Cache: SLA policies per org (invalidate on change)
- [ ] Cache: queue list per org (invalidate on change)
- [ ] Cache: knowledge article search results (TTL 60s)
- [ ] Cache strategy: Redis or in-memory
- [ ] Cache key includes org_id + workspace_id
- [ ] Cache invalidation on write operations
- [ ] Cache headers on responses

### 15.11 Backend Background Tasks
- [ ] SLA breach detection (periodic check every 60s)
- [ ] SLA approaching notification (80% threshold)
- [ ] Workflow trigger evaluation (on ticket events)
- [ ] EventBus consumer worker (continuous)
- [ ] Stale ticket alerts (unactioned for >24h)
- [ ] Auto-close resolved tickets after N days
- [ ] Cleanup: expired search cache
- [ ] Cleanup: orphaned attachments
- [ ] Report generation (async)
- [ ] Email notification sending (async queue)
- [ ] Health check: database connectivity
- [ ] Health check: Redis connectivity
- [ ] Health check: Gate service reachability
- [ ] Health check: EventBus connectivity

### 15.12 Backend Search Implementation
- [ ] Full-text search on ticket title + description
- [ ] Full-text search on knowledge article title + content
- [ ] Full-text search on incident title + root_cause
- [ ] PostgreSQL tsvector/tsquery implementation
- [ ] Search ranking (relevance scoring)
- [ ] Search highlighting (match snippets)
- [ ] Search suggestions (autocomplete)
- [ ] Search filters combinable with text search
- [ ] Search pagination
- [ ] Search indexing on insert/update (trigger or application-level)
- [ ] Optional: ElasticSearch integration for advanced search
- [ ] Search performance: query time < 200ms

### 15.13 Backend Metrics & Observability
- [ ] Request count by endpoint (Prometheus counter)
- [ ] Request latency by endpoint (Prometheus histogram)
- [ ] Error rate by endpoint
- [ ] Active ticket count gauge per org
- [ ] SLA breach count gauge per org
- [ ] EventBus event publish count
- [ ] EventBus event consume count
- [ ] Database query latency

### 15.14 Backend Notification System
- [ ] In-app notification generation on ticket events
- [ ] Notification: ticket assigned to you
- [ ] Notification: ticket you watch was updated
- [ ] Notification: comment on your ticket
- [ ] Notification: @mention in comment
- [ ] Notification: SLA approaching for your ticket
- [ ] Notification: SLA breached for your ticket
- [ ] Notification: ticket escalated
- [ ] Notification: incident created (to on-call team)
- [ ] Notification: request needs approval (to approvers)
- [ ] Email notification delivery
- [ ] Notification preferences per user
- [ ] Notification batching (digest mode)
- [ ] Notification read/unread tracking
- [ ] Notification API endpoints (list, mark read, dismiss)

---

## Summary

| Section | Total Items | Done | Remaining |
|---------|------------|------|-----------|
| 1. Project Setup | 63 | 25 | 38 |
| 2. Design System | 172 | 3 | 169 |
| 3. Dark Mode | 121 | 3 | 118 |
| 4. Core Features | 315 | 0 | 315 |
| 5. API Integration | 77 | 10 | 67 |
| 6. State Management | 34 | 0 | 34 |
| 7. Performance | 30 | 0 | 30 |
| 8. Accessibility | 50 | 0 | 50 |
| 9. Mobile & Responsive | 26 | 0 | 26 |
| 10. Internationalization | 22 | 0 | 22 |
| 11. Security | 29 | 5 | 24 |
| 12. Testing | 75 | 2 | 73 |
| 13. Documentation | 26 | 1 | 25 |
| 14. Deployment & CI/CD | 29 | 3 | 26 |
| 15. Backend | 69 | 17 | 52 |
| **TOTAL** | **1138** | **69** | **1069** |
