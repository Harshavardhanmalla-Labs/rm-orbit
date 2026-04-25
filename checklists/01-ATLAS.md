# Atlas -- Project Management — Comprehensive Checklist
> Last updated: 2026-04-06
> Legend: [x] = done · [ ] = todo · [~] = in progress

> Atlas is RM Orbit's Project Management app (comparable to Jira/Asana/Linear).
> Stack: React 18.3.1 · Vite 5.4.2 · React Router v6 · Tailwind v3 · Axios · @dnd-kit · Tiptap · Chart.js · Yjs
> Routes: 22 pages · Status: ~70% feature complete

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration](#2-design-system-integration)
3. [Dark Mode — Per-View Audit](#3-dark-mode--per-view-audit)
4. [Core Features — Dashboard](#4-core-features--dashboard)
5. [Core Features — Projects CRUD](#5-core-features--projects-crud)
6. [Core Features — Kanban Board](#6-core-features--kanban-board)
7. [Core Features — Task Management](#7-core-features--task-management)
8. [Core Features — Task Detail View](#8-core-features--task-detail-view)
9. [Core Features — Timeline / Gantt](#9-core-features--timeline--gantt)
10. [Core Features — Sprint Management](#10-core-features--sprint-management)
11. [Core Features — Portfolio View](#11-core-features--portfolio-view)
12. [Core Features — Team Management](#12-core-features--team-management)
13. [Core Features — Project Files](#13-core-features--project-files)
14. [Core Features — AI Inbox / Copilot](#14-core-features--ai-inbox--copilot)
15. [Core Features — Analytics](#15-core-features--analytics)
16. [Core Features — Timesheet / Time Tracking](#16-core-features--timesheet--time-tracking)
17. [Core Features — Import / Export](#17-core-features--import--export)
18. [Core Features — Project Settings](#18-core-features--project-settings)
19. [Core Features — Billing](#19-core-features--billing)
20. [Core Features — Settings (App-Level)](#20-core-features--settings-app-level)
21. [Core Features — Auth Pages](#21-core-features--auth-pages)
22. [Core Features — Command Palette](#22-core-features--command-palette)
23. [Core Features — Collaborative Editing](#23-core-features--collaborative-editing)
24. [Core Features — Views System](#24-core-features--views-system)
25. [Core Features — Automations](#25-core-features--automations)
26. [Core Features — Integrations](#26-core-features--integrations)
27. [Core Features — Client Portal](#27-core-features--client-portal)
28. [API Integration](#28-api-integration)
29. [State Management](#29-state-management)
30. [Performance](#30-performance)
31. [Accessibility](#31-accessibility)
32. [Mobile & Responsive](#32-mobile--responsive)
33. [Internationalization (i18n)](#33-internationalization-i18n)
34. [Security](#34-security)
35. [Testing](#35-testing)
36. [Documentation](#36-documentation)
37. [Deployment & CI/CD](#37-deployment--cicd)
38. [Backend API](#38-backend-api)

---

## 1. Project Setup & Configuration

### 1.1 Package & Dependencies
- [x] `package.json` with all required dependencies
- [x] React 18.3.1 installed
- [x] React Router v6 installed
- [x] Tailwind CSS v3 installed
- [x] Axios installed for API calls
- [x] @dnd-kit installed for drag-and-drop
- [x] Tiptap installed for rich text editing
- [x] Chart.js installed for data visualization
- [x] Yjs installed for collaborative editing
- [ ] Dependency audit: remove unused packages
- [ ] Pin all dependency versions (no `^` ranges)
- [ ] Verify no duplicate dependencies in lock file

### 1.2 Vite Configuration
- [x] Vite 5.4.2 configured
- [x] React plugin configured
- [x] Dev server running on configured port
- [ ] Production build optimized (minify, tree-shake)
- [ ] Source maps disabled in production
- [ ] Environment variables configured via `.env` files
- [ ] `.env.development` with local API URLs
- [ ] `.env.production` with production API URLs
- [ ] `.env.example` committed with variable names (no secrets)
- [ ] Build output directory configured
- [ ] Chunk splitting strategy (vendor, app, per-route)
- [ ] Asset fingerprinting for cache busting

### 1.3 TypeScript Configuration
- [ ] `tsconfig.json` configured with strict mode
- [ ] Path aliases configured (`@/` or `~/` prefix)
- [ ] No `any` types in codebase (or tracked exceptions)
- [ ] Type declarations for all API responses
- [ ] Type declarations for all component props
- [ ] Note: Atlas currently uses JSX (not TSX) — migration planned

### 1.4 Linting & Formatting
- [ ] ESLint configured with recommended rules
- [ ] React-specific ESLint rules (hooks, jsx-a11y)
- [ ] Prettier configured for consistent formatting
- [ ] Format-on-save configured in editor settings
- [ ] Pre-commit hook runs lint + format
- [ ] No lint errors in codebase

### 1.5 Docker Setup
- [ ] Dockerfile for Atlas frontend
- [ ] Docker Compose service definition
- [ ] Multi-stage build (build stage + serve stage)
- [ ] Nginx or static server for production serving
- [ ] Health check in Docker configuration
- [ ] Environment variable injection at build time

---

## 2. Design System Integration

### 2.1 Token Integration
- [x] `index.css` imports `orbit-tokens.css`
- [x] `tailwind.config.js` uses orbit preset (`tailwind-preset.js`)
- [x] `ThemeProvider` wraps root in `main.jsx`
- [x] Anti-FOUC script in `index.html`

### 2.2 Semantic Token Migration
- [x] Replace `bg-gray-*` with `bg-surface-*` tokens (bulk migration done)
- [x] Replace `text-gray-*` with `text-content-*` tokens (bulk migration done)
- [x] Replace `border-gray-*` with `border-border-*` tokens (bulk migration done)
- [x] Remove all remaining hardcoded hex colors from component files
- [ ] Remove `bg-gray-50 text-gray-900` from `<body>` in `index.html`
- [ ] Replace custom focus styles with `focus-ring` utility class
- [ ] Replace custom scrollbar CSS with `.scrollbar-thin` plugin
- [ ] Verify all hardcoded blue-500/600/700 replaced with `primary-*` tokens
- [ ] Verify all success/warning/danger colors use semantic tokens
- [ ] Audit `styles/` directory for any remaining hardcoded colors
- [ ] Audit `animations.css` for hardcoded color values

### 2.3 Component Replacement — @orbit-ui/react
- [ ] Replace custom `Spinner` with shared `<Spinner>` component
  - [ ] `DashboardPage.jsx` spinner
  - [ ] `BoardPage.jsx` spinner
  - [ ] `ProjectsPage.jsx` spinner
  - [ ] `TaskDetailPage.jsx` spinner
  - [ ] `TimelinePage.jsx` spinner
  - [ ] `SprintsPage.jsx` spinner
  - [ ] `PortfolioPage.jsx` spinner
  - [ ] `TeamPage.jsx` spinner
  - [ ] `AnalyticsPage.jsx` spinner
  - [ ] `ProjectFilesPage.jsx` spinner
  - [ ] `TimesheetPage.jsx` spinner
  - [ ] `ImportPage.jsx` spinner
- [ ] Replace custom toast with shared `useToast` from `@orbit-ui/react`
  - [ ] Remove any custom toast implementation
  - [ ] Add `<ToastProvider>` to app root
  - [ ] Replace all toast calls with `useToast()` hook
- [ ] Replace skeleton loading with `<Skeleton>` / `<SkeletonCard>` components
  - [ ] Dashboard loading skeleton
  - [ ] Projects list loading skeleton
  - [ ] Board loading skeleton
  - [ ] Task detail loading skeleton
- [ ] Replace hardcoded button classes with `<Button>` from `@orbit-ui/react`
  - [ ] `Layout.jsx` buttons (sidebar nav, actions)
  - [ ] `DashboardPage.jsx` buttons
  - [ ] `ProjectsPage.jsx` buttons (create project, filters)
  - [ ] `BoardPage.jsx` buttons (add column, add task)
  - [ ] `TaskDetailPage.jsx` buttons (save, delete, actions)
  - [ ] `SprintsPage.jsx` buttons
  - [ ] `TimelinePage.jsx` buttons
  - [ ] `SettingsPage.jsx` buttons
  - [ ] `ProjectSettingsPage.jsx` buttons
  - [ ] `TeamPage.jsx` buttons (invite, remove)
  - [ ] `ImportPage.jsx` buttons (upload, import)
  - [ ] `CreateTaskModal.jsx` buttons
  - [ ] `AITaskReviewModal.jsx` buttons
  - [ ] `AIQualityAnalysisModal.jsx` buttons
  - [ ] `AICapacityPlanner.jsx` buttons
  - [ ] `TemplatePicker.jsx` buttons
  - [ ] `QuickActionsPanel.jsx` buttons
  - [ ] `OnboardingTour.jsx` buttons
- [ ] Replace custom `Badge` variants with shared `<Badge>`
  - [ ] Task priority badges
  - [ ] Task status badges
  - [ ] Task type badges (bug, story, epic)
  - [ ] Sprint badges
  - [ ] Team member role badges
  - [ ] Notification count badges
- [ ] Replace custom `Card` layouts with `<Card>` component
  - [ ] Dashboard widget cards
  - [ ] Project cards in projects list
  - [ ] Portfolio project cards
  - [ ] Analytics metric cards
  - [ ] Team member cards
- [ ] Replace custom `Modal` with shared `<Modal>`
  - [ ] `CreateTaskModal.jsx` -> `<Modal>`
  - [ ] `AITaskReviewModal.jsx` -> `<Modal>`
  - [ ] `AIQualityAnalysisModal.jsx` -> `<Modal>`
  - [ ] Confirmation dialogs -> `<Modal>` AlertDialog variant
  - [ ] Delete confirmation dialogs
  - [ ] Archive confirmation dialogs
- [ ] Replace custom `Tooltip` with shared `<Tooltip>`
  - [ ] `Tooltip.jsx` in components -> remove, use shared
  - [ ] All icon button tooltips
  - [ ] Avatar tooltips (show user name)
  - [ ] Status indicator tooltips
  - [ ] Chart data point tooltips
- [ ] Replace custom `Avatar` with shared `<Avatar>` / `<AvatarGroup>`
  - [ ] Task assignee avatars
  - [ ] Team member avatars
  - [ ] Comment author avatars
  - [ ] Project member avatars
  - [ ] Activity feed user avatars
- [ ] Adopt `<Tabs>` component in project detail
  - [ ] Board/Timeline/Sprints/Files tab navigation
  - [ ] Task detail tabs (details, comments, history, attachments)
  - [ ] Settings page tabs
- [ ] Adopt `<Sidebar>` component
  - [ ] Replace custom `Layout.jsx` sidebar implementation
  - [ ] Sidebar collapse/expand
  - [ ] Sidebar sections (projects, favorites, recent)
  - [ ] Sidebar items with icons and counts
- [ ] Adopt `<Dropdown>` for context menus
  - [ ] Project card context menu (edit, archive, delete)
  - [ ] Task card context menu (edit, move, delete, assign)
  - [ ] Column header context menu (rename, delete, set WIP limit)
  - [ ] File context menu (download, rename, delete)
  - [ ] Team member context menu (change role, remove)
- [ ] Adopt `<EmptyState>` for empty views
  - [ ] No projects yet (projects page)
  - [ ] No tasks in column (board view)
  - [ ] No tasks matching filter (filtered views)
  - [ ] No sprints created (sprints page)
  - [ ] No files uploaded (files page)
  - [ ] No team members (team page)
  - [ ] No search results
  - [ ] No activity (activity feed)
- [ ] Adopt `<Alert>` for inline messages
  - [ ] Project at-risk warnings
  - [ ] Sprint overdue alerts
  - [ ] Permission denied messages
  - [ ] API error messages
- [ ] Adopt `<Progress>` for progress indicators
  - [ ] Sprint progress bar
  - [ ] Project completion percentage
  - [ ] File upload progress
  - [ ] Portfolio project progress bars
- [ ] Adopt `<Table>` for list views
  - [ ] Task list view (alternative to board)
  - [ ] Team member list
  - [ ] Timesheet entries table
  - [ ] Import preview table
- [ ] Adopt `<Breadcrumb>` for page navigation
  - [ ] Project > Board
  - [ ] Project > Timeline
  - [ ] Project > Settings
  - [ ] Project > Task Detail
- [ ] Adopt `<Pagination>` where needed
  - [ ] Project list pagination
  - [ ] Task list pagination
  - [ ] Activity feed pagination
  - [ ] Timesheet entries pagination
- [ ] Adopt `<DatePicker>` for date fields
  - [ ] Task due date
  - [ ] Sprint start/end dates
  - [ ] Timesheet date picker
  - [ ] Timeline date range selector
- [ ] Adopt `<FileUpload>` for file areas
  - [ ] Project files upload
  - [ ] Task attachment upload
  - [ ] Import CSV upload
- [ ] Adopt `<Accordion>` for collapsible sections
  - [ ] Settings page sections
  - [ ] Task detail expandable sections
  - [ ] Filter panel sections
- [ ] Adopt `<Tag>` / `<TagInput>` for labels
  - [ ] Task labels
  - [ ] Project tags
  - [ ] Filter by tags
- [ ] Adopt `<Switch>` for toggles
  - [ ] Settings toggles
  - [ ] Notification preference toggles
  - [ ] Feature flag toggles
- [ ] Adopt `<Checkbox>` for selection
  - [ ] Bulk task selection
  - [ ] Subtask completion checkboxes
  - [ ] Filter checkboxes
- [ ] Adopt `<Radio>` / `<RadioGroup>` for single-select
  - [ ] View type selection
  - [ ] Priority selection
  - [ ] Task type selection
- [ ] Adopt `<Input>` for form fields
  - [ ] Search inputs
  - [ ] Project name input
  - [ ] Task title input
  - [ ] Settings form inputs
- [ ] Adopt `<Select>` for dropdowns
  - [ ] Assignee selector
  - [ ] Status selector
  - [ ] Priority selector
  - [ ] Project selector
- [ ] Adopt `<Textarea>` for multi-line text
  - [ ] Project description
  - [ ] Sprint goal
  - [ ] Comment input (when not using rich text)

---

## 3. Dark Mode -- Per-View Audit

### 3.1 Completed Pages
- [x] Dashboard page — hardcoded light colors replaced with dark: variants
- [x] Kanban Board — semantic token migration applied
- [x] Task Detail modal — border-gray-50 fixed, semantic tokens applied
- [x] Settings page — form inputs, section dividers
- [x] Login/Auth pages — form fields, error states

### 3.2 Pages Needing Audit
- [ ] Timeline view
  - [ ] Grid lines in dark mode
  - [ ] Event bars colors in dark mode
  - [ ] Date headers in dark mode
  - [ ] Today marker line in dark mode
  - [ ] Dependency arrows in dark mode
  - [ ] Milestone markers in dark mode
- [ ] Sprint view
  - [ ] Sprint cards background
  - [ ] Burndown chart in dark mode
  - [ ] Story point badges in dark mode
  - [ ] Sprint status indicators
  - [ ] Backlog section background
  - [ ] Sprint goal text
- [ ] Portfolio page
  - [ ] Project cards in dark mode
  - [ ] Progress bars in dark mode
  - [ ] Status indicators in dark mode
  - [ ] Health score badges
  - [ ] Resource allocation heatmap
- [ ] Projects list page
  - [ ] Project cards hover state
  - [ ] Grid/list toggle buttons
  - [ ] Filter dropdowns
  - [ ] Empty state
- [ ] Team page
  - [ ] Team member cards
  - [ ] Role badges
  - [ ] Invite form
  - [ ] Member details panel
- [ ] Project Files page
  - [ ] File cards/list items
  - [ ] Upload zone
  - [ ] File preview overlay
  - [ ] Folder tree
- [ ] AI Inbox page
  - [ ] AI suggestion cards
  - [ ] Priority indicators
  - [ ] Action buttons
- [ ] Analytics page
  - [ ] All Chart.js charts
  - [ ] Metric cards
  - [ ] Date range selector
  - [ ] Filter dropdowns
- [ ] Timesheet page
  - [ ] Time entries table
  - [ ] Timer widget
  - [ ] Date navigation
  - [ ] Summary cards
- [ ] Import page
  - [ ] Upload zone
  - [ ] Preview table
  - [ ] Mapping configuration
  - [ ] Progress indicator
- [ ] Billing page
  - [ ] Plan cards
  - [ ] Usage meters
  - [ ] Invoice table
- [ ] Project Settings page
  - [ ] Form fields
  - [ ] Color picker
  - [ ] Icon selector
  - [ ] Danger zone (delete/archive)
- [ ] Register page
  - [ ] Form fields
  - [ ] Links
  - [ ] Error states
- [ ] Forgot Password page
  - [ ] Form fields
  - [ ] Success/error states
- [ ] Reset Password page
  - [ ] Form fields
  - [ ] Validation messages
- [ ] Callback page (OAuth)
  - [ ] Loading state
  - [ ] Error state

### 3.3 Components Needing Audit
- [ ] `Layout.jsx` sidebar in dark mode
  - [ ] Sidebar background
  - [ ] Active item highlight
  - [ ] Hover state
  - [ ] Section headers
  - [ ] Collapse/expand button
- [ ] `OrbitBar.jsx` in dark mode
- [ ] `AppLauncher.jsx` in dark mode
- [ ] `CreateTaskModal.jsx` in dark mode
- [ ] `CommandPalette.jsx` in dark mode
- [ ] `CommandPaletteEnhanced.jsx` in dark mode
- [ ] `CollaborativeEditor.jsx` in dark mode
- [ ] `MarkdownEditor.jsx` in dark mode
- [ ] `SprintBurndownChart.jsx` in dark mode
- [ ] `TimeTrackerWidget.jsx` in dark mode
- [ ] `QuickActionsPanel.jsx` in dark mode
- [ ] `OnboardingTour.jsx` in dark mode
- [ ] `TemplatePicker.jsx` in dark mode
- [ ] `AICapacityPlanner.jsx` in dark mode
- [ ] `AIQualityAnalysisModal.jsx` in dark mode
- [ ] `AITaskReviewModal.jsx` in dark mode
- [ ] `AtlasCopilot.jsx` in dark mode
- [ ] `StartMeetingButton.jsx` in dark mode
- [ ] `ProtectedButton.jsx` in dark mode
- [ ] All `ui/` components in dark mode
  - [ ] `Avatar.jsx`
  - [ ] `Badge.jsx`
  - [ ] `button.tsx`
  - [ ] `EmptyState.jsx`
  - [ ] `Skeleton.jsx`
  - [ ] `tooltip.tsx`
  - [ ] `animated-tooltip.tsx`
  - [ ] `shadcn-avatar.tsx`

### 3.4 Charts & Graphs Dark Mode
- [ ] Chart.js global defaults use CSS variable colors
- [ ] Burndown chart: axis labels, gridlines, data points in dark mode
- [ ] Velocity chart: bars, labels in dark mode
- [ ] Task distribution pie chart: labels, legend in dark mode
- [ ] Analytics line charts: all elements in dark mode
- [ ] Chart tooltip backgrounds in dark mode
- [ ] Chart legend text in dark mode

### 3.5 Third-Party Components Dark Mode
- [ ] Tiptap editor: toolbar, content area, bubble menu in dark mode
- [ ] @dnd-kit: drag overlay, drop indicators in dark mode
- [ ] Scrollbar styling in dark mode
- [ ] Date picker (if custom) in dark mode

### 3.6 Cross-Cutting Dark Mode
- [ ] Verify color contrast ratios in dark mode (WCAG AA: 4.5:1)
- [ ] Test dark mode on all 22 routes
- [ ] Test theme toggle transitions (no flash, smooth switch)
- [ ] Verify glassmorphism effects in dark mode
- [ ] Verify shadows in dark mode (subtler)

---

## 4. Core Features -- Dashboard

### 4.1 Dashboard Page (DashboardPage.jsx)
- [ ] Activity feed widget
  - [ ] Real-time updates (WebSocket or polling)
  - [ ] Activity items: task created, status changed, commented, assigned
  - [ ] Activity item user avatar
  - [ ] Activity item timestamp (relative: "2m ago")
  - [ ] Activity item click -> navigate to source
  - [ ] Activity feed pagination/infinite scroll
  - [ ] Activity feed empty state
- [ ] My Tasks widget
  - [ ] Filtered to current user's assigned tasks
  - [ ] Grouped by status (To Do, In Progress, Done)
  - [ ] Task priority indicator
  - [ ] Task due date with overdue highlighting
  - [ ] Click task -> navigate to task detail
  - [ ] Quick status change (dropdown on each task)
  - [ ] "View all" link to filtered task list
- [ ] Project Health Overview widget
  - [ ] Cards showing: On Track / At Risk / Overdue / Completed
  - [ ] Click card -> filtered projects list
  - [ ] Health indicator color coding
  - [ ] Project count per health status
- [ ] Recent Projects widget
  - [ ] Last 5 accessed projects
  - [ ] Project name, icon, last activity
  - [ ] Click -> navigate to project
- [ ] Upcoming Deadlines widget
  - [ ] Tasks due in next 7 days
  - [ ] Sorted by due date
  - [ ] Overdue items highlighted red
- [ ] Team Workload widget
  - [ ] Bar chart: tasks per team member
  - [ ] Overloaded members highlighted
  - [ ] Click member -> filtered task view
- [ ] Sprint Progress widget
  - [ ] Active sprint progress bar
  - [ ] Days remaining
  - [ ] Burndown sparkline
  - [ ] Click -> sprint detail
- [ ] Quick Actions
  - [ ] Create new project button
  - [ ] Create new task button
  - [ ] Start timer button
  - [ ] Open command palette
- [ ] Dashboard layout customization
  - [ ] Drag-to-reorder widgets
  - [ ] Show/hide widgets
  - [ ] Widget size options (full width, half width)
  - [ ] Persist layout to user preferences

---

## 5. Core Features -- Projects CRUD

### 5.1 Projects List (ProjectsPage.jsx)
- [ ] List all projects for current org
- [ ] Grid view layout (project cards)
- [ ] List view layout (table rows)
- [ ] Grid vs. list view toggle (persisted preference)
- [ ] Sort by: name, created date, last updated, due date, status
- [ ] Sort direction toggle (asc/desc)
- [ ] Filter by status: active, archived, completed, all
- [ ] Filter by team member (assigned to)
- [ ] Filter by label/tag
- [ ] Search by project name (debounced, 300ms)
- [ ] Clear all filters button
- [ ] Active filter indicator count
- [ ] Empty state: no projects (with "Create your first project" CTA)
- [ ] Empty state: no projects matching filter
- [ ] Loading state (skeleton cards)
- [ ] Error state (API failure with retry button)
- [ ] Pagination (or infinite scroll for many projects)
- [ ] Project card: name, icon, description preview
- [ ] Project card: status badge
- [ ] Project card: progress bar
- [ ] Project card: member avatars
- [ ] Project card: last updated timestamp
- [ ] Project card: hover state
- [ ] Project card: context menu (edit, archive, delete, duplicate)
- [ ] Project card: click -> navigate to project detail
- [ ] Favorites/starred projects section at top
- [ ] Star/unstar project toggle

### 5.2 Project Creation
- [ ] "Create Project" button prominently placed
- [ ] Create project modal/dialog
  - [ ] Project name (required, validated)
  - [ ] Project description (optional, rich text or plain)
  - [ ] Project icon/emoji selector
  - [ ] Project color selector
  - [ ] Start date picker
  - [ ] End date picker
  - [ ] Initial team members (multi-select)
  - [ ] Project template selector (blank, kanban, scrum, waterfall)
  - [ ] Visibility: public (org-wide) or private (invited only)
  - [ ] Create button (with loading state)
  - [ ] Cancel button
  - [ ] Validation errors inline
  - [ ] After create -> navigate to new project board

### 5.3 Project Editing
- [ ] Edit project name (inline or modal)
- [ ] Edit project description
- [ ] Change project icon/emoji
- [ ] Change project color
- [ ] Update start/end dates
- [ ] Change project visibility

### 5.4 Project Operations
- [ ] Archive project (soft delete, can restore)
- [ ] Restore archived project
- [ ] Delete project permanently (with confirmation dialog)
- [ ] Duplicate/clone project (name, settings, optionally tasks)
- [ ] Favorite/star project
- [ ] Pin project to sidebar

---

## 6. Core Features -- Kanban Board

### 6.1 Board Page (BoardPage.jsx)
- [ ] Load board with columns and tasks from API
- [ ] Loading state (skeleton board)
- [ ] Error state (with retry)
- [ ] Empty board state (no columns, prompt to add)

### 6.2 Columns
- [ ] Display columns in horizontal scroll layout
- [ ] Column header: name, task count, WIP indicator
- [ ] Column creation: "Add Column" button at end
  - [ ] Column name input
  - [ ] Column color selector (optional)
  - [ ] Save/cancel
- [ ] Column renaming (double-click header or edit button)
- [ ] Column deletion (with confirmation, move tasks to other column)
- [ ] Column reordering (drag column headers)
- [ ] Column WIP limit setting
  - [ ] Set max tasks per column
  - [ ] Visual warning when at limit (yellow)
  - [ ] Visual error when over limit (red)
- [ ] Column collapse/expand
- [ ] Column menu (rename, set WIP limit, hide, delete)

### 6.3 Cards (Tasks on Board)
- [ ] Task card: title (truncated if long)
- [ ] Task card: assignee avatar
- [ ] Task card: priority indicator (color/icon)
- [ ] Task card: due date (with overdue highlight)
- [ ] Task card: label/tag chips
- [ ] Task card: subtask count (e.g., "3/5")
- [ ] Task card: attachment indicator
- [ ] Task card: comment count
- [ ] Task card: story points badge
- [ ] Task card: task type icon (task, bug, story, epic)
- [ ] Task card: hover state (shadow/elevation)
- [ ] Task card: click -> open task detail (modal or page)
- [ ] Task card: context menu (right-click or ... button)
  - [ ] Edit task
  - [ ] Assign to...
  - [ ] Change priority
  - [ ] Change status
  - [ ] Add label
  - [ ] Move to column...
  - [ ] Duplicate task
  - [ ] Delete task
- [ ] Quick-add task in column
  - [ ] Click "+" in column header or footer
  - [ ] Inline text input for task title
  - [ ] Enter to create, Escape to cancel
  - [ ] Created task appears at top/bottom of column

### 6.4 Drag-and-Drop (@dnd-kit)
- [ ] Drag task card between columns
  - [ ] Grab handle or entire card draggable
  - [ ] Drag overlay (card preview follows cursor)
  - [ ] Drop indicator (highlight target position)
  - [ ] Smooth animation on drop
  - [ ] Optimistic update (card moves immediately)
  - [ ] API call to update task status
  - [ ] Rollback on API failure
- [ ] Drag task within column (reorder)
  - [ ] Reorder tasks within same column
  - [ ] Position persisted to API
- [ ] Drag column to reorder
- [ ] Touch-friendly drag-and-drop (mobile drag handle)
- [ ] Keyboard alternative for drag-and-drop
  - [ ] Select task with Enter
  - [ ] Arrow keys to choose target column/position
  - [ ] Enter to confirm move
  - [ ] Escape to cancel
- [ ] Multi-select and drag (bulk move)
- [ ] Cross-board drag (move task to different project)

### 6.5 Board Filters & Grouping
- [ ] Filter by assignee
- [ ] Filter by priority
- [ ] Filter by label/tag
- [ ] Filter by due date (overdue, due this week, no due date)
- [ ] Filter by task type (task, bug, story, epic)
- [ ] Search tasks on board (highlight matching cards)
- [ ] Clear all filters
- [ ] Swimlane grouping: by assignee
- [ ] Swimlane grouping: by priority
- [ ] Swimlane grouping: by epic
- [ ] Swimlane grouping: by label
- [ ] Swimlane toggle on/off

### 6.6 Board Real-Time
- [ ] Real-time board updates via WebSocket/SSE
  - [ ] New task appears on board
  - [ ] Task moved by another user
  - [ ] Task updated (title, assignee, etc.)
  - [ ] Task deleted
  - [ ] Column added/removed
- [ ] Conflict resolution (task moved by two users simultaneously)
- [ ] "Someone else is editing" indicator

---

## 7. Core Features -- Task Management

### 7.1 Task CRUD
- [ ] Create task (modal: `CreateTaskModal.jsx`)
  - [ ] Task title (required)
  - [ ] Task description (rich text, Tiptap)
  - [ ] Task type selector (Task, Bug, Story, Epic, Sub-task)
  - [ ] Status selector (maps to board column)
  - [ ] Priority selector (Critical, High, Medium, Low, None)
  - [ ] Assignee selector (single user)
  - [ ] Multiple assignees support
  - [ ] Due date picker
  - [ ] Start date picker
  - [ ] Labels/tags (multi-select, create new)
  - [ ] Story points / estimate
  - [ ] Sprint assignment
  - [ ] Parent task (for sub-tasks)
  - [ ] Custom fields
  - [ ] Create button with loading state
  - [ ] Keyboard shortcut: Cmd+Enter to create
- [ ] Edit task (inline or in detail view)
- [ ] Delete task (with confirmation)
- [ ] Duplicate task
- [ ] Move task between projects
- [ ] Convert task type (e.g., Task -> Bug)

### 7.2 Task Properties
- [ ] Task title editing (inline, click to edit)
- [ ] Task description (rich text editor)
- [ ] Task status (dropdown, triggers column move on board)
- [ ] Task priority (dropdown or radio)
- [ ] Task type (icon + label)
- [ ] Task assignee(s) (avatar dropdown)
- [ ] Task labels/tags (tag input, color coded)
- [ ] Task due date (date picker)
- [ ] Task start date (date picker)
- [ ] Task story points (number input)
- [ ] Task sprint (dropdown)
- [ ] Task parent (breadcrumb to parent)
- [ ] Custom fields per project:
  - [ ] Dropdown custom field
  - [ ] Text custom field
  - [ ] Number custom field
  - [ ] Date custom field
  - [ ] Checkbox custom field
  - [ ] URL custom field

### 7.3 Task Relationships
- [ ] Link related tasks
  - [ ] "Blocks" relationship
  - [ ] "Blocked by" relationship
  - [ ] "Related to" relationship
  - [ ] "Duplicates" relationship
- [ ] Dependency visualization (arrows on timeline/board)
- [ ] Circular dependency detection/prevention

### 7.4 Task Bulk Actions
- [ ] Select multiple tasks (checkboxes)
- [ ] Bulk assign to user
- [ ] Bulk change status
- [ ] Bulk change priority
- [ ] Bulk add label
- [ ] Bulk move to sprint
- [ ] Bulk delete (with confirmation)
- [ ] Bulk archive

### 7.5 Task Templates
- [ ] Save task as template
- [ ] Create task from template
- [ ] Template library (project-level and org-level)
- [ ] Template variables (auto-fill dates, assignees)

### 7.6 Recurring Tasks
- [ ] Create recurring task (daily, weekly, monthly, custom)
- [ ] Recurrence pattern configuration
- [ ] Auto-create next occurrence on completion
- [ ] Skip occurrence option
- [ ] End recurrence date

---

## 8. Core Features -- Task Detail View

### 8.1 Task Detail Page (TaskDetailPage.jsx)
- [ ] Full-page view for task details
- [ ] Back button to return to board/list
- [ ] Task type icon and ID
- [ ] Task title (editable inline)
- [ ] Status badge (click to change)
- [ ] Priority badge (click to change)

### 8.2 Description
- [ ] Rich text editor (Tiptap)
  - [ ] Bold, italic, underline, strikethrough
  - [ ] Headings (H1-H3)
  - [ ] Bullet list, numbered list, checklist
  - [ ] Code block with syntax highlighting
  - [ ] Blockquote
  - [ ] Horizontal rule
  - [ ] Links (inline)
  - [ ] Images (upload or paste)
  - [ ] Tables
  - [ ] @mention users in description
  - [ ] #reference other tasks
  - [ ] Slash commands (/, /heading, /list, /code, etc.)
- [ ] Description auto-save (debounced)
- [ ] Description edit/view toggle
- [ ] Description collaborative editing (Yjs)

### 8.3 Subtasks
- [ ] Subtask list with completion checkboxes
- [ ] Add subtask (inline input)
- [ ] Subtask completion progress (e.g., "3/5 complete")
- [ ] Subtask assignee (avatar)
- [ ] Subtask due date
- [ ] Subtask priority
- [ ] Reorder subtasks (drag-and-drop)
- [ ] Delete subtask
- [ ] Convert subtask to full task
- [ ] Indent/outdent subtask (hierarchy)

### 8.4 Comments / Activity Thread
- [ ] Comment input (rich text editor)
- [ ] Post comment button
- [ ] Comment list (newest first or oldest first toggle)
- [ ] Comment author avatar + name + timestamp
- [ ] Edit own comment
- [ ] Delete own comment (admin can delete any)
- [ ] @mention in comments (triggers notification)
- [ ] Emoji reactions on comments
- [ ] Comment with attachments (drag-drop file into comment)
- [ ] Activity log interleaved with comments:
  - [ ] Status changes
  - [ ] Assignee changes
  - [ ] Priority changes
  - [ ] Label changes
  - [ ] Due date changes
  - [ ] Description edits
  - [ ] File uploads
  - [ ] Sprint changes

### 8.5 File Attachments
- [ ] Upload files (drag-and-drop or browse)
- [ ] File list with name, size, upload date, uploader
- [ ] Image preview (thumbnail)
- [ ] PDF preview (embedded viewer)
- [ ] Download file
- [ ] Delete file (with confirmation)
- [ ] File upload progress bar

### 8.6 Time Tracking
- [ ] Time estimate field (hours/minutes)
- [ ] Time logged display
- [ ] Start/stop timer button
- [ ] Manual time entry (date, duration, description)
- [ ] Time log list (who, when, duration, description)
- [ ] Delete time entry
- [ ] Edit time entry
- [ ] Estimate vs actual comparison
- [ ] Overtime warning (logged > estimated)

### 8.7 Task History / Audit Trail
- [ ] Complete history of all changes
- [ ] Change: field name, old value, new value
- [ ] Change: user who made the change
- [ ] Change: timestamp
- [ ] Filterable by field type
- [ ] Expandable/collapsible

### 8.8 Task Sidebar (right panel)
- [ ] Properties panel (status, priority, assignee, dates, labels, sprint)
- [ ] Relationships panel (blocks, blocked by, related)
- [ ] Watchers/subscribers list
- [ ] Add/remove watcher
- [ ] Link to external resources (URLs)
- [ ] Copy task URL to clipboard

---

## 9. Core Features -- Timeline / Gantt

### 9.1 Timeline Page (TimelinePage.jsx)
- [ ] Gantt chart rendering
- [ ] Task bars with start/end dates
- [ ] Bar color indicates task priority or status
- [ ] Bar text shows task title
- [ ] Bar hover shows tooltip with details
- [ ] Click bar -> open task detail
- [ ] Dependency arrows between tasks
  - [ ] "Blocks" shown as arrow from blocker to blocked
  - [ ] Arrow style (curved, straight)
  - [ ] Arrow color for critical path
- [ ] Drag-resize bars to change dates
  - [ ] Drag left edge: change start date
  - [ ] Drag right edge: change end date
  - [ ] Drag middle: move entire date range
  - [ ] Optimistic update + API call
- [ ] Milestone markers (diamond shapes)
- [ ] Today line (vertical red/blue line)
- [ ] Critical path highlighting (longest dependency chain)
- [ ] Zoom levels:
  - [ ] Day view
  - [ ] Week view
  - [ ] Month view
  - [ ] Quarter view
- [ ] Scroll navigation (horizontal for time, vertical for tasks)
- [ ] Group tasks by:
  - [ ] Status
  - [ ] Assignee
  - [ ] Label
  - [ ] Sprint
  - [ ] Epic
- [ ] Filter tasks (same filters as board)
- [ ] Baseline comparison (planned vs actual dates)
- [ ] Progress indicator on bars (% complete shading)
- [ ] Resource row (assignee capacity per day/week)
- [ ] Export to image/PDF

---

## 10. Core Features -- Sprint Management

### 10.1 Sprints Page (SprintsPage.jsx)
- [ ] Sprint list (all sprints for project)
- [ ] Active sprint highlighted
- [ ] Sprint states: Planning, Active, Completed
- [ ] Create new sprint
  - [ ] Sprint name (auto: "Sprint 1", "Sprint 2", etc.)
  - [ ] Sprint goal (text)
  - [ ] Start date
  - [ ] End date (typically 2 weeks)
  - [ ] Story point capacity
- [ ] Start sprint (moves from Planning to Active)
- [ ] Complete sprint
  - [ ] Summary of completed vs incomplete tasks
  - [ ] Move incomplete tasks to: next sprint / backlog
  - [ ] Sprint review notes
  - [ ] Sprint retrospective notes

### 10.2 Sprint Board
- [ ] Sprint-scoped board view (only tasks in this sprint)
- [ ] Sprint progress bar (story points: done / total)
- [ ] Days remaining indicator
- [ ] Sprint goal display

### 10.3 Backlog
- [ ] Backlog view: all unassigned tasks (not in any sprint)
- [ ] Drag tasks from backlog to sprint
- [ ] Drag tasks from sprint to backlog
- [ ] Backlog priority ordering (drag to reorder)
- [ ] Backlog grooming: estimate story points inline
- [ ] Backlog refinement: break down stories into sub-tasks

### 10.4 Sprint Charts (SprintBurndownChart.jsx)
- [ ] Burndown chart per sprint
  - [ ] Ideal burndown line
  - [ ] Actual burndown line
  - [ ] Story points remaining per day
  - [ ] Chart updates daily
  - [ ] Dark mode chart colors
- [ ] Burnup chart
  - [ ] Scope line (total story points)
  - [ ] Work completed line
  - [ ] Scope creep visualization
- [ ] Velocity chart
  - [ ] Story points completed per sprint (bar chart)
  - [ ] Average velocity line
  - [ ] Rolling average (last 3-5 sprints)
- [ ] Sprint comparison table
  - [ ] Sprint name, goal, planned points, completed points, velocity

### 10.5 Sprint Retrospective
- [ ] What went well (text area)
- [ ] What didn't go well (text area)
- [ ] Action items (checklist)
- [ ] Action items assigned to team members
- [ ] Retrospective linked to sprint

---

## 11. Core Features -- Portfolio View

### 11.1 Portfolio Page (PortfolioPage.jsx)
- [ ] Cross-project overview (all projects in org)
- [ ] Project cards with:
  - [ ] Project name and icon
  - [ ] Health status: On Track / At Risk / Off Track
  - [ ] Completion percentage with progress bar
  - [ ] Active sprint info
  - [ ] Team member count
  - [ ] Open issues count
  - [ ] Overdue tasks count
- [ ] Sort projects by: health, completion, name, activity
- [ ] Filter projects by: health status, team member, tag
- [ ] Resource allocation heatmap
  - [ ] Team members as rows
  - [ ] Weeks as columns
  - [ ] Color intensity = hours allocated
  - [ ] Over-allocation warning (red)
- [ ] Project timeline (multi-project Gantt)
  - [ ] Each project as a bar with start/end dates
  - [ ] Milestone markers
- [ ] Aggregated metrics:
  - [ ] Total tasks across all projects
  - [ ] Total completed this week
  - [ ] Average project health
  - [ ] Team utilization percentage

---

## 12. Core Features -- Team Management

### 12.1 Team Page (TeamPage.jsx)
- [ ] Team member list
  - [ ] Avatar, name, email, role
  - [ ] Role badge (Owner, Admin, Member, Viewer)
  - [ ] Active status (online/offline)
  - [ ] Task count assigned
- [ ] Invite team member
  - [ ] Email input
  - [ ] Role selector
  - [ ] Send invitation button
  - [ ] Invitation confirmation
- [ ] Change member role
- [ ] Remove member (with confirmation)
- [ ] Member detail panel
  - [ ] Assigned tasks list
  - [ ] Workload (hours this week)
  - [ ] Recent activity
- [ ] Team member search
- [ ] Bulk invite (comma-separated emails)

---

## 13. Core Features -- Project Files

### 13.1 Project Files Page (ProjectFilesPage.jsx)
- [ ] File browser view (grid of file cards)
- [ ] File list view (table with columns: name, size, uploaded by, date)
- [ ] Grid/list toggle
- [ ] Folder creation
  - [ ] Create new folder
  - [ ] Rename folder
  - [ ] Delete folder (with contents warning)
  - [ ] Nested folders
- [ ] File upload
  - [ ] Drag-and-drop zone
  - [ ] Browse button
  - [ ] Multiple file upload
  - [ ] Upload progress indicator
  - [ ] File type icons
- [ ] File preview
  - [ ] Image preview (lightbox)
  - [ ] PDF preview (embedded viewer)
  - [ ] Document preview (office files)
  - [ ] Code file preview (syntax highlighted)
  - [ ] Audio/video preview (player)
- [ ] File operations
  - [ ] Download file
  - [ ] Rename file
  - [ ] Move to folder
  - [ ] Delete file (with confirmation)
  - [ ] Copy shareable link
- [ ] File search (by name)
- [ ] Sort files (by name, size, date, type)
- [ ] File version history (if multiple uploads of same name)
- [ ] Storage usage display (quota used / total)
- [ ] Breadcrumb navigation for folders

---

## 14. Core Features -- AI Inbox / Copilot

### 14.1 AI Inbox Page (AIInboxPage.jsx)
- [ ] AI-suggested task priorities
  - [ ] Re-prioritization recommendations based on deadlines, dependencies
  - [ ] Accept/reject suggestion buttons
  - [ ] Explanation of why AI suggests the change
- [ ] Automated status update summaries
  - [ ] Daily project status summary (AI-generated)
  - [ ] Weekly progress report
  - [ ] Blockers identification
- [ ] Smart task suggestions
  - [ ] Break down large tasks into subtasks (AI)
  - [ ] Suggest assignees based on workload and skills
  - [ ] Suggest due dates based on velocity
- [ ] Risk detection
  - [ ] Overdue task alerts
  - [ ] Scope creep warnings
  - [ ] Resource over-allocation warnings

### 14.2 Atlas Copilot (AtlasCopilot.jsx)
- [ ] Chat interface for AI assistant
- [ ] Natural language task creation ("Create a task for...")
- [ ] Natural language queries ("What tasks are overdue?")
- [ ] Context-aware suggestions (knows current project, sprint, user)
- [ ] Copilot panel toggle (slide-in from right)
- [ ] Conversation history
- [ ] Code/markdown output formatting

### 14.3 AI Modals
- [ ] `AITaskReviewModal.jsx` — AI reviews task quality
  - [ ] Description clarity score
  - [ ] Acceptance criteria suggestions
  - [ ] Missing fields warnings
- [ ] `AIQualityAnalysisModal.jsx` — project quality analysis
  - [ ] Code coverage recommendations
  - [ ] Sprint health analysis
  - [ ] Technical debt indicators
- [ ] `AICapacityPlanner.jsx` — AI capacity planning
  - [ ] Team capacity visualization
  - [ ] Sprint planning suggestions
  - [ ] Resource allocation recommendations

---

## 15. Core Features -- Analytics

### 15.1 Analytics Page (AnalyticsPage.jsx)
- [ ] Task completion trends
  - [ ] Line chart: tasks completed per day/week/month
  - [ ] Date range selector
  - [ ] Compare periods
- [ ] Team velocity
  - [ ] Bar chart: story points per sprint
  - [ ] Average velocity line
  - [ ] Projected completion date based on velocity
- [ ] Task distribution
  - [ ] Pie chart: tasks by status
  - [ ] Pie chart: tasks by priority
  - [ ] Pie chart: tasks by type
  - [ ] Pie chart: tasks by assignee
- [ ] Cycle time metrics
  - [ ] Average time from created to done
  - [ ] Cycle time trend over time
  - [ ] Cycle time by task type
- [ ] Lead time metrics
  - [ ] Time from request to delivery
  - [ ] Lead time distribution histogram
- [ ] Cumulative flow diagram
  - [ ] Stacked area chart: task count per status over time
  - [ ] Bottleneck identification
- [ ] Overdue tasks report
  - [ ] List of all overdue tasks
  - [ ] Days overdue count
  - [ ] Assignee accountability
- [ ] Team workload chart
  - [ ] Horizontal bar: tasks per member
  - [ ] Capacity vs assigned
- [ ] Custom report builder (stretch)
  - [ ] Choose metrics
  - [ ] Choose grouping
  - [ ] Choose date range
  - [ ] Save report
  - [ ] Export report (PDF, CSV)

---

## 16. Core Features -- Timesheet / Time Tracking

### 16.1 Timesheet Page (TimesheetPage.jsx)
- [ ] Weekly timesheet view
  - [ ] Rows: tasks
  - [ ] Columns: days of the week
  - [ ] Cells: hours logged
  - [ ] Row totals
  - [ ] Column totals
  - [ ] Grand total
- [ ] Daily timesheet view
  - [ ] List of time entries for the day
  - [ ] Add entry: task, duration, description
- [ ] Start/stop timer (TimeTrackerWidget.jsx)
  - [ ] Timer display (HH:MM:SS)
  - [ ] Associated task selector
  - [ ] Start button
  - [ ] Pause button
  - [ ] Stop button (logs entry)
  - [ ] Timer persists across page navigation
  - [ ] Timer state saved to localStorage
- [ ] Manual time entry
  - [ ] Task selector
  - [ ] Date picker
  - [ ] Duration input (hours:minutes)
  - [ ] Description text
  - [ ] Save entry
- [ ] Edit time entry
- [ ] Delete time entry
- [ ] Time reports
  - [ ] Hours per project (pie chart)
  - [ ] Hours per task (bar chart)
  - [ ] Hours per day (line chart)
  - [ ] Billable vs non-billable hours
  - [ ] Export report (CSV)
- [ ] Date navigation (prev/next week, date picker)

---

## 17. Core Features -- Import / Export

### 17.1 Import Page (ImportPage.jsx)
- [ ] CSV import for tasks
  - [ ] File upload zone
  - [ ] Column mapping UI (CSV column -> Atlas field)
  - [ ] Preview table (first 10 rows)
  - [ ] Validation warnings (missing required fields)
  - [ ] Import button with progress
  - [ ] Import success summary (X tasks created)
  - [ ] Import error report (which rows failed, why)
- [ ] Jira import
  - [ ] Jira JSON export file upload
  - [ ] Project mapping
  - [ ] Status mapping
  - [ ] User mapping
  - [ ] Import progress
- [ ] Trello import
  - [ ] Trello JSON export file upload
  - [ ] Board -> project mapping
  - [ ] List -> column mapping
  - [ ] Card -> task mapping
- [ ] Export
  - [ ] Export tasks to CSV
  - [ ] Export project to JSON
  - [ ] Export report to PDF

---

## 18. Core Features -- Project Settings

### 18.1 Project Settings Page (ProjectSettingsPage.jsx)
- [ ] General settings
  - [ ] Project name (editable)
  - [ ] Project description (editable)
  - [ ] Project icon/emoji selector
  - [ ] Project color selector
  - [ ] Project visibility (public/private)
- [ ] Workflow settings
  - [ ] Custom status workflow (add/remove/rename statuses)
  - [ ] Default status for new tasks
  - [ ] Status transitions (optional: allowed moves)
- [ ] Custom fields
  - [ ] Add custom field (name, type, options)
  - [ ] Edit custom field
  - [ ] Delete custom field
  - [ ] Reorder custom fields
- [ ] Labels management
  - [ ] Create label (name, color)
  - [ ] Edit label
  - [ ] Delete label
  - [ ] Default labels
- [ ] Notifications settings
  - [ ] Email notifications toggle per event type
  - [ ] In-app notifications toggle per event type
- [ ] Integrations settings
  - [ ] GitHub/GitLab repository link
  - [ ] Webhook URL configuration
  - [ ] Slack/Connect channel link
- [ ] Danger zone
  - [ ] Archive project (reversible)
  - [ ] Delete project (irreversible, confirmation required)
  - [ ] Transfer project ownership

---

## 19. Core Features -- Billing

### 19.1 Billing Page (BillingPage.jsx)
- [ ] Current plan display
- [ ] Plan comparison (Free, Pro, Enterprise)
- [ ] Upgrade/downgrade buttons
- [ ] Usage metrics
  - [ ] Projects used / limit
  - [ ] Storage used / limit
  - [ ] Team members / limit
  - [ ] AI credits used / limit
- [ ] Invoice history table
  - [ ] Date, amount, status, download link
- [ ] Payment method management
  - [ ] Add credit card
  - [ ] Change payment method
  - [ ] Remove payment method
- [ ] Billing address

---

## 20. Core Features -- Settings (App-Level)

### 20.1 Settings Page (SettingsPage.jsx)
- [ ] Profile settings
  - [ ] Avatar upload
  - [ ] Display name
  - [ ] Email (read-only, linked to Gate)
  - [ ] Timezone selector
  - [ ] Language/locale selector
- [ ] Notification preferences
  - [ ] Email notification toggles
  - [ ] Desktop push notification toggles
  - [ ] In-app notification toggles
- [ ] Appearance
  - [ ] Theme: light / dark / system (via ThemeProvider)
  - [ ] Sidebar collapsed by default toggle
  - [ ] Dense mode toggle (compact UI)
- [ ] Keyboard shortcuts
  - [ ] Display all shortcuts
  - [ ] Enable/disable shortcuts
  - [ ] Custom shortcut mapping (stretch)
- [ ] Connected apps
  - [ ] GitHub / GitLab integration
  - [ ] Slack / Connect integration
  - [ ] Calendar integration
  - [ ] Mail integration

---

## 21. Core Features -- Auth Pages

### 21.1 Login Page (LoginPage.jsx)
- [ ] Email input field
- [ ] Password input field
- [ ] Sign in button (with loading state)
- [ ] "Sign in with RM Gate" SSO button
- [ ] "Forgot password?" link
- [ ] "Don't have an account? Register" link
- [ ] Error message display (invalid credentials)
- [ ] Remember me checkbox
- [ ] Redirect to originally requested page after login

### 21.2 Register Page (RegisterPage.jsx)
- [ ] Full name input
- [ ] Email input
- [ ] Password input (with strength indicator)
- [ ] Confirm password input
- [ ] Terms of service checkbox
- [ ] Register button (with loading state)
- [ ] "Already have an account? Sign in" link
- [ ] Email verification sent confirmation

### 21.3 Forgot Password Page (ForgotPasswordPage.jsx)
- [ ] Email input
- [ ] Send reset link button
- [ ] Success message ("Check your email")
- [ ] "Back to login" link

### 21.4 Reset Password Page (ResetPasswordPage.jsx)
- [ ] New password input
- [ ] Confirm new password input
- [ ] Reset button
- [ ] Token validation (expired/invalid token handling)
- [ ] Success message with redirect to login

### 21.5 Callback Page (CallbackPage.jsx)
- [ ] OAuth callback handler
- [ ] Loading state while exchanging code for token
- [ ] Error state display
- [ ] Redirect to dashboard on success

---

## 22. Core Features -- Command Palette

### 22.1 CommandPalette (CommandPalette.jsx / CommandPaletteEnhanced.jsx)
- [ ] Open with Cmd+K (or Ctrl+K)
- [ ] Search input with instant filtering
- [ ] Categories:
  - [ ] Navigation (go to page)
  - [ ] Actions (create task, create project)
  - [ ] Recent items
  - [ ] Tasks (search tasks)
  - [ ] Projects (search projects)
  - [ ] Team members
- [ ] Keyboard navigation (arrow keys, Enter to select, Escape to close)
- [ ] Shortcut display for each action
- [ ] Fuzzy search matching
- [ ] Result icons/avatars
- [ ] Recent searches history
- [ ] Loading state for async results

---

## 23. Core Features -- Collaborative Editing

### 23.1 Collaborative Editor (CollaborativeEditor.jsx)
- [ ] Yjs integration for real-time collaboration
- [ ] Multiple cursors (see other users' cursor positions)
- [ ] Cursor labels (show user name)
- [ ] Cursor colors (distinct per user)
- [ ] Real-time character-by-character sync
- [ ] Conflict-free resolution (CRDT)
- [ ] Presence awareness (who is viewing/editing)
- [ ] Connection status indicator (connected, syncing, offline)
- [ ] Offline editing with sync on reconnect
- [ ] Version history (point-in-time snapshots)
- [ ] Undo/redo per user (not shared undo stack)

---

## 24. Core Features -- Views System

### 24.1 Board View (Kanban)
- [ ] (Covered in Section 6)

### 24.2 List View
- [ ] Sortable columns (title, status, priority, assignee, due date, created)
- [ ] Grouping by status / priority / assignee / label / sprint
- [ ] Inline editing (click cell to edit)
- [ ] Expandable rows (show description/subtasks)
- [ ] Column visibility toggle
- [ ] Column resize
- [ ] Freeze first column (task title)
- [ ] Bulk selection with checkboxes
- [ ] Row hover actions (quick-edit, delete)

### 24.3 Calendar View
- [ ] Month view with tasks on due dates
- [ ] Week view with tasks on due dates
- [ ] Day view with tasks on due dates
- [ ] Drag task to different date (reschedule)
- [ ] Click date to create task
- [ ] Color coding by status/priority
- [ ] Overdue task indicators
- [ ] Integration with Orbit Calendar

### 24.4 Table View (Spreadsheet)
- [ ] Spreadsheet-like editing
- [ ] Custom columns per view
- [ ] Basic formulas (SUM, COUNT, AVG)
- [ ] Freeze columns
- [ ] Row numbers
- [ ] Cell-level formatting

### 24.5 View Management
- [ ] Save custom views (filters + sort + grouping + columns)
- [ ] Name views
- [ ] Share views with team
- [ ] Default view per project
- [ ] Quick-switch between saved views

---

## 25. Core Features -- Automations

- [ ] Rule-based automations
  - [ ] When status changes -> assign to, notify, update field
  - [ ] When priority is critical -> notify channel, escalate
  - [ ] When due date approaching -> remind assignee
  - [ ] When task created -> auto-assign, set defaults
  - [ ] When label added -> move to column
- [ ] Custom automation builder UI
  - [ ] Trigger selector (event type)
  - [ ] Condition builder (field comparisons)
  - [ ] Action selector (what to do)
  - [ ] Test automation
- [ ] Scheduled automations (daily/weekly cleanup, reports)
- [ ] Automation execution log
  - [ ] Timestamp, trigger, actions taken
  - [ ] Success/failure status
  - [ ] Re-run button

---

## 26. Core Features -- Integrations

### 26.1 Orbit Ecosystem
- [ ] Atlas <-> Calendar: push task deadlines as calendar events
- [ ] Atlas <-> Mail: convert email to task (from Mail context menu)
- [ ] Atlas <-> Connect: task notifications in Connect channels
  - [ ] Channel selection per project
  - [ ] Events to post: task created, completed, overdue
- [ ] Atlas <-> Meet: link meetings to projects/tasks (StartMeetingButton.jsx)
  - [ ] Start meeting from task detail
  - [ ] Meeting notes linked to task
  - [ ] Action items from meeting -> tasks
- [ ] Atlas <-> Writer: link documents to tasks
- [ ] Atlas <-> Planet: client portal, link deals to projects
- [ ] Atlas <-> TurboTick: bidirectional ticket<->task linking

### 26.2 External Integrations
- [ ] GitHub integration
  - [ ] Link repository to project
  - [ ] Branch/PR/commit references on tasks
  - [ ] Auto-update task status on PR merge
  - [ ] GitHub webhook handler
- [ ] GitLab integration
  - [ ] Same features as GitHub
- [ ] Webhooks
  - [ ] Outgoing webhooks (send task events to external URL)
  - [ ] Incoming webhooks (receive events to create/update tasks)
  - [ ] Webhook secret verification
  - [ ] Webhook retry on failure
- [ ] Slack integration
  - [ ] Post task updates to Slack channel
  - [ ] Create task from Slack message
  - [ ] Slash commands in Slack

---

## 27. Core Features -- Client Portal

- [ ] Shared project view for external clients
- [ ] Client can view task status (read-only)
- [ ] Client can comment on tasks
- [ ] Client can upload files
- [ ] Client access scoped (no internal tasks visible)
- [ ] Client branding options (logo, colors)
- [ ] Client invitation flow (via email)
- [ ] Client permission management
- [ ] Client view: hide internal fields (story points, sprint, etc.)
- [ ] Client approval workflow (approve/reject deliverables)

---

## 28. API Integration

### 28.1 HTTP Client Setup
- [ ] Centralized Axios instance with base URL configuration
- [ ] Auth token in request headers (from cookie or interceptor)
- [ ] `X-Org-Id` header on all requests for tenant isolation
- [ ] Request timeout configuration
- [ ] Request/response logging (development only)

### 28.2 Auth Interceptors
- [ ] 401 response interceptor -> trigger token refresh
- [ ] Token refresh: call Gate refresh endpoint
- [ ] Retry original request after refresh
- [ ] If refresh fails -> redirect to login
- [ ] Queue concurrent requests during refresh (don't trigger multiple refreshes)

### 28.3 Error Handling
- [ ] Show user-facing error messages on API failures
- [ ] Network error detection (offline)
- [ ] Timeout error handling
- [ ] 403 Forbidden handling (permission denied message)
- [ ] 404 Not Found handling (resource not found)
- [ ] 422 Validation error handling (show field-level errors)
- [ ] 500 Server error handling (generic error with retry)
- [ ] Rate limit (429) handling with retry-after

### 28.4 Optimistic Updates
- [ ] Task status change: update UI immediately, rollback on error
- [ ] Task move (drag-and-drop): update board immediately
- [ ] Task priority change: update immediately
- [ ] Comment creation: show immediately, confirm on response
- [ ] Subtask toggle: check/uncheck immediately

### 28.5 Real-Time Updates
- [ ] WebSocket or SSE subscription for project/board changes
  - [ ] New task notification
  - [ ] Task updated notification
  - [ ] Task moved notification
  - [ ] Task deleted notification
  - [ ] Comment added notification
  - [ ] Sprint updated notification
- [ ] EventBus integration (subscribe to atlas events)
- [ ] Conflict detection (another user edited same task)
- [ ] Auto-reconnect on connection loss

### 28.6 Offline Support
- [ ] Detect offline status (useOnline hook)
- [ ] Queue actions taken offline
- [ ] Replay queue on reconnect
- [ ] Show offline indicator in UI
- [ ] Cache critical data in localStorage/IndexedDB

### 28.7 API Endpoints Needed
- [ ] `GET /projects` — list projects
- [ ] `POST /projects` — create project
- [ ] `GET /projects/:id` — get project detail
- [ ] `PUT /projects/:id` — update project
- [ ] `DELETE /projects/:id` — delete project
- [ ] `GET /projects/:id/tasks` — list tasks
- [ ] `POST /projects/:id/tasks` — create task
- [ ] `GET /tasks/:id` — get task detail
- [ ] `PUT /tasks/:id` — update task
- [ ] `DELETE /tasks/:id` — delete task
- [ ] `POST /tasks/:id/comments` — add comment
- [ ] `GET /tasks/:id/comments` — list comments
- [ ] `POST /tasks/:id/attachments` — upload file
- [ ] `GET /tasks/:id/attachments` — list files
- [ ] `POST /tasks/:id/time-entries` — log time
- [ ] `GET /tasks/:id/time-entries` — list time entries
- [ ] `GET /projects/:id/board` — get board (columns + tasks)
- [ ] `PUT /tasks/:id/move` — move task (status change)
- [ ] `GET /projects/:id/sprints` — list sprints
- [ ] `POST /projects/:id/sprints` — create sprint
- [ ] `PUT /sprints/:id` — update sprint
- [ ] `GET /projects/:id/timeline` — get timeline data
- [ ] `GET /projects/:id/analytics` — get analytics data
- [ ] `GET /projects/:id/members` — list team members
- [ ] `POST /projects/:id/members` — invite member
- [ ] `GET /search?q=` — search tasks/projects
- [ ] `GET /dashboard` — dashboard data (aggregated)
- [ ] `GET /portfolio` — portfolio data (all projects summary)

---

## 29. State Management

### 29.1 Context / Store Architecture
- [ ] AuthContext (`context/AuthContext.jsx`) — user, token, login/logout
- [ ] Project context or store — current project, project list
- [ ] Board store — columns, tasks, drag state
- [ ] Task detail store — current task, comments, attachments
- [ ] Sprint store — sprints, active sprint, backlog
- [ ] UI store — sidebar state, modals, toasts

### 29.2 Custom Hooks
- [ ] `useBoardSync.js` — real-time board synchronization
- [ ] `useOptimisticUpdate.js` — optimistic update pattern
- [ ] `useProjectWebSocket.js` — WebSocket connection for project
- [ ] `useDebounce` — debounced values
- [ ] `useKeyboardShortcuts` — keyboard shortcut registration

### 29.3 Persistence
- [ ] Sidebar collapsed state persisted to localStorage
- [ ] View preferences persisted (grid vs list, sort order)
- [ ] Filter state persisted per project
- [ ] Theme preference persisted
- [ ] Timer state persisted (active timer survives page refresh)

### 29.4 Cross-Tab Sync
- [ ] Theme changes sync across tabs
- [ ] Org changes sync across tabs
- [ ] Auth state changes sync across tabs (logout in one tab -> logout all)

---

## 30. Performance

### 30.1 Code Splitting
- [ ] Route-level code splitting for all 22 pages
  - [ ] `DashboardPage.jsx` lazy loaded
  - [ ] `ProjectsPage.jsx` lazy loaded
  - [ ] `BoardPage.jsx` lazy loaded
  - [ ] `TaskDetailPage.jsx` lazy loaded
  - [ ] `TimelinePage.jsx` lazy loaded
  - [ ] `SprintsPage.jsx` lazy loaded
  - [ ] `PortfolioPage.jsx` lazy loaded
  - [ ] `TeamPage.jsx` lazy loaded
  - [ ] `ProjectFilesPage.jsx` lazy loaded
  - [ ] `AIInboxPage.jsx` lazy loaded
  - [ ] `AnalyticsPage.jsx` lazy loaded
  - [ ] `TimesheetPage.jsx` lazy loaded
  - [ ] `ImportPage.jsx` lazy loaded
  - [ ] `SettingsPage.jsx` lazy loaded
  - [ ] `ProjectSettingsPage.jsx` lazy loaded
  - [ ] `BillingPage.jsx` lazy loaded
  - [ ] `LoginPage.jsx` lazy loaded
  - [ ] `RegisterPage.jsx` lazy loaded
  - [ ] `ForgotPasswordPage.jsx` lazy loaded
  - [ ] `ResetPasswordPage.jsx` lazy loaded
  - [ ] `CallbackPage.jsx` lazy loaded
  - [ ] `ProjectDetailPage.jsx` lazy loaded
- [ ] Suspense fallback for each lazy route (loading spinner/skeleton)

### 30.2 Virtual Scrolling
- [ ] Task list: virtual scroll for >100 items
- [ ] Kanban board: virtual columns for >8 columns
- [ ] Timeline view: virtual rows for many tasks
- [ ] Activity feed: virtual scroll for long history
- [ ] Comments list: virtual scroll for many comments
- [ ] File list: virtual scroll for many files

### 30.3 Memoization
- [ ] Task filter computation memoized (useMemo)
- [ ] Gantt chart calculations memoized
- [ ] Board column computation memoized
- [ ] Analytics chart data memoized
- [ ] Component-level React.memo for expensive components
  - [ ] TaskCard
  - [ ] BoardColumn
  - [ ] TimelineBar
  - [ ] ChartWidget

### 30.4 Image & Asset Optimization
- [ ] Image thumbnails: lazy loaded with `loading="lazy"`
- [ ] Avatar images: lazy loaded
- [ ] File previews: thumbnail instead of full image
- [ ] SVG icons: inline (no network requests)

### 30.5 API Optimization
- [ ] Debounce search input (300ms)
- [ ] Debounce filter changes (200ms)
- [ ] Pagination instead of loading all data
- [ ] Cursor-based pagination for infinite scroll
- [ ] API response caching (SWR/React Query stale-while-revalidate)
- [ ] Prefetch next page data on hover

### 30.6 Bundle Optimization
- [ ] Tree-shake unused Chart.js modules (only import needed chart types)
- [ ] Tree-shake unused Tiptap extensions
- [ ] Tree-shake unused @dnd-kit modules
- [ ] Analyze bundle size (vite-bundle-visualizer)
- [ ] Set bundle size budget (< 500KB initial JS)
- [ ] First meaningful paint < 1.5s on fast 3G

---

## 31. Accessibility

### 31.1 Global
- [ ] Skip-to-main-content link at top of page
- [ ] All landmark regions have `role` attributes
- [ ] Page title updates on navigation
- [ ] Focus management on route change

### 31.2 Kanban Board
- [ ] Keyboard navigation between columns (arrow keys)
- [ ] Keyboard navigation between tasks within column
- [ ] Keyboard drag-and-drop alternative (cut/paste tasks)
- [ ] ARIA live region for board updates ("Task moved to Done")
- [ ] Column headers as headings (h2/h3)
- [ ] Task count announced per column

### 31.3 Modals & Overlays
- [ ] All modals trap focus
- [ ] All modals return focus on close
- [ ] All modals close on Escape
- [ ] All modals have aria-label or aria-labelledby
- [ ] Dialog role on all modal containers

### 31.4 Forms
- [ ] All form fields have visible labels
- [ ] All form fields have associated labels (htmlFor or aria-labelledby)
- [ ] Error messages linked via aria-describedby
- [ ] Required fields marked with aria-required
- [ ] Form submission accessible via keyboard (Enter)

### 31.5 Color & Visual
- [ ] Color is not the only indicator of task status/priority
  - [ ] Status has icon + text + color
  - [ ] Priority has icon + text + color
- [ ] Focus-visible ring on all interactive elements
- [ ] Sufficient color contrast (WCAG AA 4.5:1)

### 31.6 Screen Reader
- [ ] Tested with VoiceOver (macOS)
- [ ] Tested with NVDA (Windows)
- [ ] All interactive icons have aria-label or aria-hidden
- [ ] Dynamic content updates announced (toast, status change, new task)
- [ ] Table data accessible (proper th/td, scope, caption)

### 31.7 Motion
- [ ] `prefers-reduced-motion` disables animations
- [ ] Drag-and-drop animations respect reduced motion
- [ ] Chart animations respect reduced motion

---

## 32. Mobile & Responsive

### 32.1 Mobile Layout
- [ ] Sidebar hidden by default on mobile
- [ ] Hamburger menu opens sidebar as overlay
- [ ] Bottom tab navigation on mobile (Dashboard, Board, Tasks, More)
- [ ] All modals full-screen on mobile
- [ ] Touch-friendly tap targets (min 44x44px)

### 32.2 Board on Mobile
- [ ] Board collapses to single-column list view
- [ ] Horizontal swipe between columns
- [ ] Touch-friendly drag-and-drop (visible drag handle)
- [ ] Swipe left on task card for quick actions (complete, delete)

### 32.3 Tablet Layout
- [ ] Sidebar collapses to icon-only
- [ ] Board shows 2-3 columns visible
- [ ] Split-view for task list + task detail

### 32.4 Responsive Testing
- [ ] Test at 320px (small phone)
- [ ] Test at 375px (iPhone SE)
- [ ] Test at 414px (iPhone 14 Pro Max)
- [ ] Test at 768px (iPad portrait)
- [ ] Test at 1024px (iPad landscape)
- [ ] Test at 1280px (laptop)
- [ ] Test at 1440px (desktop)
- [ ] Test at 1920px (large desktop)
- [ ] No horizontal scroll on any viewport

---

## 33. Internationalization (i18n)

- [ ] i18n library chosen and configured (react-i18next or similar)
- [ ] All user-facing strings externalized to locale files
- [ ] English locale file complete
- [ ] Date formatting uses locale (date-fns or Intl)
- [ ] Number formatting uses locale
- [ ] RTL layout support
- [ ] Locale switching UI in settings
- [ ] Pluralization rules
- [ ] Dynamic string interpolation

---

## 34. Security

### 34.1 Frontend Security
- [ ] XSS prevention: all user input sanitized before rendering
- [ ] CSP headers configured (no inline scripts)
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] Tiptap content sanitized (no script tags in rich text)
- [ ] File upload: validate file type on client side
- [ ] File upload: validate file size on client side
- [ ] External link warning before navigating
- [ ] No sensitive data in localStorage (tokens in httpOnly cookies)
- [ ] Environment variables: no secrets in frontend .env
- [ ] CORS: only allow Orbit domains

### 34.2 Auth Security
- [ ] PKCE OAuth flow (no client secret in frontend)
- [ ] Token refresh handled via httpOnly cookies
- [ ] Session timeout (redirect to login after inactivity)
- [ ] CSRF protection (token in headers)
- [ ] Logout clears all auth state

### 34.3 Input Validation
- [ ] All form inputs validated (client-side + server-side)
- [ ] Email format validation
- [ ] URL format validation
- [ ] File type validation
- [ ] SQL injection prevention (parameterized queries on backend)

---

## 35. Testing

### 35.1 Unit Tests
- [ ] Task filtering logic
- [ ] Date calculation utilities
- [ ] Permission checking logic
- [ ] Story point calculation
- [ ] Sprint velocity calculation
- [ ] Cycle time calculation
- [ ] Board column sorting
- [ ] Search query parsing
- [ ] URL routing logic
- [ ] Form validation functions
- [ ] API response transformations
- [ ] Custom hook: useBoardSync
- [ ] Custom hook: useOptimisticUpdate
- [ ] Custom hook: useProjectWebSocket

### 35.2 Component Tests
- [ ] TaskCard renders correctly
- [ ] BoardColumn renders tasks
- [ ] ProjectCard renders project info
- [ ] CreateTaskModal form validation
- [ ] Timeline bar positioning
- [ ] Sprint burndown chart data
- [ ] Analytics chart rendering
- [ ] Sidebar navigation active state
- [ ] Search input debounce
- [ ] File upload drag-and-drop

### 35.3 Integration Tests
- [ ] Create project -> add task -> move to Done
- [ ] Create sprint -> assign tasks -> complete sprint
- [ ] Upload file -> view in files page -> download
- [ ] Search task -> open result -> verify content
- [ ] Edit task description -> save -> verify persistence
- [ ] Add comment -> verify in activity feed
- [ ] Timer start -> stop -> verify time entry

### 35.4 E2E Tests (Playwright)
- [ ] Full board interaction flow
  - [ ] Navigate to board
  - [ ] Create task
  - [ ] Drag to different column
  - [ ] Open task detail
  - [ ] Edit description
  - [ ] Add comment
  - [ ] Close detail
- [ ] OAuth login flow
  - [ ] Navigate to app
  - [ ] Redirect to Gate login
  - [ ] Enter credentials
  - [ ] Redirect back with token
  - [ ] Verify authenticated state
- [ ] Sprint workflow
  - [ ] Create sprint
  - [ ] Assign tasks
  - [ ] Start sprint
  - [ ] Complete tasks
  - [ ] Complete sprint
  - [ ] View burndown chart
- [ ] Project lifecycle
  - [ ] Create project
  - [ ] Add team members
  - [ ] Create tasks
  - [ ] Track progress
  - [ ] Archive project
- [ ] Mobile viewport tests
  - [ ] Navigation works on mobile
  - [ ] Board usable on mobile
  - [ ] Task detail readable on mobile

### 35.5 Visual Regression Tests
- [ ] Dashboard screenshot comparison
- [ ] Board page screenshot comparison
- [ ] Task detail screenshot comparison
- [ ] Timeline screenshot comparison
- [ ] Dark mode screenshots for all pages

### 35.6 Performance Tests
- [ ] Board with 500 tasks: renders in < 2s
- [ ] Task list with 1000 items: smooth scroll
- [ ] Timeline with 200 tasks: no jank
- [ ] Initial page load < 3s on 4G
- [ ] Lighthouse score > 90 (Performance)

---

## 36. Documentation

### 36.1 Component Documentation
- [ ] README for each custom component
- [ ] Props documentation for each component
- [ ] Usage examples for each component

### 36.2 API Documentation
- [ ] All API endpoints documented (request/response format)
- [ ] Authentication flow documented
- [ ] Error codes documented
- [ ] Rate limits documented

### 36.3 User Guide
- [ ] Getting started guide
- [ ] Board usage guide
- [ ] Sprint management guide
- [ ] Time tracking guide
- [ ] Keyboard shortcuts reference

### 36.4 Developer Guide
- [ ] Local development setup instructions
- [ ] Architecture overview (component tree, data flow)
- [ ] Code style guide
- [ ] Contributing guide
- [ ] Deployment guide

---

## 37. Deployment & CI/CD

### 37.1 Build Pipeline
- [ ] Vite production build configured
- [ ] Build runs on every PR
- [ ] Build artifacts stored (for deployment)
- [ ] TypeScript / lint checks in CI

### 37.2 Environment Configs
- [ ] Development environment config
- [ ] Staging environment config
- [ ] Production environment config
- [ ] Environment variable documentation

### 37.3 Docker
- [ ] Dockerfile for Atlas frontend
- [ ] Docker Compose service
- [ ] Nginx config for SPA serving
- [ ] Health check endpoint

### 37.4 Monitoring
- [ ] Error tracking (Sentry or similar)
- [ ] Performance monitoring (Core Web Vitals)
- [ ] User analytics (page views, feature usage)
- [ ] Uptime monitoring

### 37.5 Logging
- [ ] Structured error logging
- [ ] User action logging (for debugging)
- [ ] API call logging (dev only)

---

## 38. Backend API

### 38.1 Atlas Backend Service
- [ ] Framework chosen (FastAPI / Express / etc.)
- [ ] Database: PostgreSQL with project/task schema
- [ ] Migrations: Alembic or similar
- [ ] Authentication: Gate JWT validation middleware
- [ ] Org isolation: all queries filtered by org_id
- [ ] API versioning (v1 prefix)

### 38.2 Database Schema
- [ ] `projects` table (id, org_id, name, description, status, icon, color, dates, settings)
- [ ] `tasks` table (id, project_id, title, description, status, priority, type, assignee, dates, estimate, parent_id)
- [ ] `columns` table (id, project_id, name, position, wip_limit, color)
- [ ] `sprints` table (id, project_id, name, goal, start_date, end_date, status)
- [ ] `comments` table (id, task_id, user_id, content, created_at)
- [ ] `attachments` table (id, task_id, filename, url, size, uploaded_by)
- [ ] `time_entries` table (id, task_id, user_id, date, duration, description)
- [ ] `labels` table (id, project_id, name, color)
- [ ] `task_labels` join table
- [ ] `task_dependencies` table (blocker_id, blocked_id, type)
- [ ] `project_members` table (project_id, user_id, role)
- [ ] `custom_fields` table (id, project_id, name, type, options)
- [ ] `task_custom_values` table (task_id, field_id, value)
- [ ] `automation_rules` table (id, project_id, trigger, conditions, actions)
- [ ] `activity_log` table (id, entity_type, entity_id, action, user_id, changes, timestamp)

### 38.3 Background Jobs
- [ ] Sprint auto-start (when start date reached)
- [ ] Overdue task notifications
- [ ] Recurring task creation
- [ ] Automation rule execution
- [ ] Analytics pre-computation
- [ ] Attachment cleanup (orphaned files)

### 38.4 Caching
- [ ] Redis for session cache
- [ ] Redis for board state cache
- [ ] Cache invalidation on write
- [ ] Cache TTL configuration

### 38.5 Rate Limiting
- [ ] Per-user rate limits on API
- [ ] Per-org rate limits on API
- [ ] Rate limit headers in responses

---

## Summary

| Section | Done | Todo | Total |
|---------|------|------|-------|
| Project Setup | ~8 | ~25 | ~33 |
| Design System | ~10 | ~150 | ~160 |
| Dark Mode | ~5 | ~75 | ~80 |
| Dashboard | 0 | ~35 | ~35 |
| Projects CRUD | 0 | ~40 | ~40 |
| Kanban Board | 0 | ~65 | ~65 |
| Task Management | 0 | ~70 | ~70 |
| Task Detail | 0 | ~60 | ~60 |
| Timeline/Gantt | 0 | ~30 | ~30 |
| Sprint Mgmt | 0 | ~40 | ~40 |
| Portfolio | 0 | ~20 | ~20 |
| Team Mgmt | 0 | ~15 | ~15 |
| Files | 0 | ~25 | ~25 |
| AI Features | 0 | ~30 | ~30 |
| Analytics | 0 | ~25 | ~25 |
| Timesheet | 0 | ~25 | ~25 |
| Import/Export | 0 | ~20 | ~20 |
| Settings | 0 | ~30 | ~30 |
| Auth Pages | 0 | ~20 | ~20 |
| Command Palette | 0 | ~15 | ~15 |
| Collaborative | 0 | ~12 | ~12 |
| Views System | 0 | ~25 | ~25 |
| Automations | 0 | ~15 | ~15 |
| Integrations | 0 | ~25 | ~25 |
| Client Portal | 0 | ~10 | ~10 |
| API Integration | 0 | ~60 | ~60 |
| State Mgmt | 0 | ~15 | ~15 |
| Performance | 0 | ~45 | ~45 |
| Accessibility | 0 | ~30 | ~30 |
| Mobile | 0 | ~20 | ~20 |
| i18n | 0 | ~10 | ~10 |
| Security | 0 | ~20 | ~20 |
| Testing | 0 | ~50 | ~50 |
| Documentation | 0 | ~15 | ~15 |
| Deployment | 0 | ~15 | ~15 |
| Backend | 0 | ~35 | ~35 |
| **TOTAL** | **~23** | **~1282** | **~1305** |
