# 05 — Calendar: Scheduling App

> **Stack:** React 18.3.1 · Vite 5.3.1 · Tailwind v3 · Axios
> **Routes:** 3 main views (calendar, tasks, team)
> **Status:** ~55% feature complete
> **Components:** CalendarView, CreateEventView, EventModal, TaskModal, AIAssistant, TasksView, ScheduleListView, TeamView
> **Types:** CalendarEvent, Task, TeamMember, Profile, NotificationItem, EcosystemStatus, EcosystemAppLink, ViewMode
> **Critical:** `App.tsx` is 19K+ lines — needs code splitting
> **Last updated:** 2026-04-06

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration](#2-design-system-integration)
3. [Dark Mode](#3-dark-mode)
4. [Core Features](#4-core-features)
5. [API Integration](#5-api-integration)
6. [State Management](#6-state-management)
7. [Performance](#7-performance)
8. [Accessibility](#8-accessibility)
9. [Mobile & Responsive](#9-mobile--responsive)
10. [Internationalization](#10-internationalization)
11. [Security](#11-security)
12. [Testing](#12-testing)
13. [Documentation](#13-documentation)
14. [Deployment & CI/CD](#14-deployment--cicd)
15. [Backend](#15-backend)

---

## 1. Project Setup & Configuration

### 1.1 Package & Tooling
- [x] React 18 installed and configured
- [x] Vite 5 configured as build tool
- [x] TypeScript configured
- [x] Tailwind v3 configured
- [x] Axios installed for HTTP requests
- [ ] ESLint configured with recommended rules
- [ ] ESLint plugin for React hooks
- [ ] ESLint plugin for accessibility (jsx-a11y)
- [ ] Prettier configured and integrated with ESLint
- [ ] Husky pre-commit hooks configured
- [ ] lint-staged configured for staged file linting
- [ ] commitlint configured for conventional commits
- [ ] `.editorconfig` present with consistent settings
- [ ] `.nvmrc` or `.node-version` file present

### 1.2 Path Aliases & Imports
- [ ] `@/` path alias configured in Vite
- [ ] `@/` alias configured in TypeScript
- [ ] Import order enforced
- [ ] Barrel exports from `@/components/index.ts`
- [ ] Barrel exports from `@/lib/index.ts`

### 1.3 Environment Configuration
- [ ] `VITE_API_URL` env var for backend API
- [ ] `VITE_GATE_URL` env var for Gate auth
- [ ] `.env.example` file with all required env vars documented
- [ ] `.env.development` with local defaults
- [ ] `.env.production` with production values
- [ ] `.env.test` with test environment values
- [ ] Environment variable validation at app start

### 1.4 Project Structure
- [x] `src/components/` — UI components
- [x] `src/lib/` — Utility library (auth.ts)
- [ ] `src/hooks/` — Custom React hooks directory
- [ ] `src/store/` — State management directory
- [ ] `src/services/` — API service layer directory
- [ ] `src/types/` — TypeScript types (extracted from App.tsx)
- [ ] `src/constants/` — App constants directory
- [ ] `src/api/` — API client layer directory
- [ ] `src/utils/` — Utility functions directory

### 1.5 Code Quality — Critical Refactoring
- [ ] **Split `App.tsx` (19K+ lines) into separate modules** (TOP PRIORITY)
- [ ] Extract `CalendarEvent` type to `src/types/event.ts`
- [ ] Extract `Task` type to `src/types/task.ts`
- [ ] Extract `TeamMember` type to `src/types/team.ts`
- [ ] Extract `Profile` type to `src/types/profile.ts`
- [ ] Extract `NotificationItem` type to `src/types/notification.ts`
- [ ] Extract `EcosystemStatus` type to `src/types/ecosystem.ts`
- [ ] Extract `EcosystemAppLink` type to `src/types/ecosystem.ts`
- [ ] Extract `ViewMode` type to `src/types/view.ts`
- [ ] Extract event CRUD logic to `src/hooks/useEvents.ts`
- [ ] Extract task CRUD logic to `src/hooks/useTasks.ts`
- [ ] Extract team logic to `src/hooks/useTeam.ts`
- [ ] Extract auth logic to `src/hooks/useAuth.ts`
- [ ] Extract notification logic to `src/hooks/useNotifications.ts`
- [ ] Extract API calls to `src/api/events.ts`
- [ ] Extract API calls to `src/api/tasks.ts`
- [ ] Extract API calls to `src/api/team.ts`
- [ ] Extract API calls to `src/api/notifications.ts`
- [ ] Extract date utility functions to `src/utils/date.ts`
- [ ] Extract color utility functions to `src/utils/color.ts`
- [ ] Extract calendar grid calculation to `src/utils/calendar.ts`
- [ ] Set up state management (Zustand or React Context)
- [ ] Ensure each component file < 500 lines
- [ ] Remove console.log statements from production code

### 1.6 Build Configuration
- [x] Vite dev server running
- [ ] Production build optimized (minification, tree-shaking)
- [ ] Source maps configured for production
- [ ] Bundle analyzer configured
- [ ] Build output chunking (vendor, app, views)
- [ ] Asset hashing for cache busting
- [ ] Compression plugin (gzip/brotli)

---

## 2. Design System Integration

### 2.1 Token & Theme Foundation
- [x] Anti-FOUC script present in `index.html`
- [x] `ThemeProvider` wraps root
- [x] Google Fonts removed from `index.html`
- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css"`
- [ ] `tailwind.config.js` uses orbit preset (verify)
- [ ] Replace all hardcoded hex colors with design token CSS variables
- [ ] Replace `bg-gray-*` with semantic tokens (`bg-surface-*`)
- [ ] Replace `text-gray-*` with semantic tokens (`text-content-*`)
- [ ] Replace `border-gray-*` with semantic tokens (`border-border-*`)
- [ ] Replace hardcoded calendar grid colors with semantic tokens
- [ ] Replace hardcoded time slot colors with orbit color scale
- [ ] Replace hardcoded event chip colors with token-based palette
- [ ] Replace hardcoded focus ring styles with `focus-ring` utility class
- [ ] Replace custom scrollbar CSS with `.scrollbar-thin` plugin class

### 2.2 Replace Custom Modal
- [ ] Import `Modal` from `@orbit-ui/react`
- [ ] Replace `EventModal.tsx` custom modal wrapper with `<Modal>`
- [ ] Replace `TaskModal.tsx` custom modal wrapper with `<Modal>`
- [ ] Replace event creation modal with `<Modal>`
- [ ] Replace event edit modal with `<Modal>`
- [ ] Replace delete confirmation modal with `<Modal>`
- [ ] Replace recurring event edit dialog ("This event / All events") with `<Modal>`
- [ ] Replace import/export dialog with `<Modal>`
- [ ] Replace sharing settings dialog with `<Modal>`
- [ ] Ensure modal focus trap works
- [ ] Ensure modal close on Escape
- [ ] Ensure modal backdrop click-to-close

### 2.3 Replace Custom Avatar
- [ ] Import `Avatar`, `AvatarGroup` from `@orbit-ui/react`
- [ ] Replace attendee avatars in `EventModal.tsx` with `<Avatar>`
- [ ] Replace attendee avatars in event chips with `<Avatar>` (xs size)
- [ ] Replace team member avatars in `TeamView.tsx` with `<Avatar>`
- [ ] Replace profile avatar in app header with `<Avatar>`
- [ ] Replace task assignee avatars in `TasksView.tsx` with `<Avatar>`
- [ ] Use `<AvatarGroup>` for multi-attendee display on event chips
- [ ] Use `<AvatarGroup>` for team member overlay in TeamView

### 2.4 Replace Custom Badge
- [ ] Import `Badge` from `@orbit-ui/react`
- [ ] Replace event type badge with `<Badge>`
- [ ] Replace event category badge with `<Badge>`
- [ ] Replace task priority badge (High/Medium/Low) with `<Badge>`
- [ ] Replace task status badge (To Do/In Progress/Review/Done) with `<Badge>`
- [ ] Replace notification count badge with `<Badge>`
- [ ] Replace "Today" indicator badge with `<Badge>`
- [ ] Replace event count badge on date cell with `<Badge>`
- [ ] Replace "All day" event badge with `<Badge>`
- [ ] Replace recurring event indicator with `<Badge>`

### 2.5 Replace/Adopt Button Component
- [ ] Import `Button`, `IconButton` from `@orbit-ui/react`
- [ ] Replace "Create Event" button with `<Button>`
- [ ] Replace "Create Task" button with `<Button>`
- [ ] Replace "Today" navigation button with `<Button>`
- [ ] Replace prev/next navigation buttons with `<IconButton>`
- [ ] Replace view mode buttons (Day/Week/Month) with `<Button>` group
- [ ] Replace event modal save/cancel buttons with `<Button>`
- [ ] Replace task modal save/cancel buttons with `<Button>`
- [ ] Replace delete button with `<Button variant="danger">`
- [ ] Replace "Add attendee" button with `<Button>`
- [ ] Replace "Send invite" button with `<Button>`
- [ ] Replace AI Assistant action buttons with `<Button>`
- [ ] Replace settings save button with `<Button>`
- [ ] Replace import/export buttons with `<Button>`
- [ ] Replace close buttons on modals/panels with `<IconButton>`

### 2.6 Replace Custom Input
- [ ] Import `Input` from `@orbit-ui/react`
- [ ] Replace event title input with `<Input>`
- [ ] Replace event location input with `<Input>`
- [ ] Replace event description textarea with orbit `<Textarea>`
- [ ] Replace task name input with `<Input>`
- [ ] Replace search input with `<Input>`
- [ ] Replace attendee email input with `<Input>`
- [ ] Replace AI assistant input with `<Input>`
- [ ] Replace date range inputs with orbit `<DatePicker>`
- [ ] Replace time inputs with orbit `<TimePicker>`

### 2.7 Adopt Tabs Component
- [ ] Import `Tabs` from `@orbit-ui/react`
- [ ] Replace Calendar/Tasks/Team view switcher with `<Tabs>`
- [ ] Replace event detail tabs (if any) with `<Tabs>`
- [ ] Replace settings section tabs with `<Tabs>`
- [ ] Replace AI assistant mode tabs with `<Tabs>`

### 2.8 Adopt Dropdown Component
- [ ] Import `Dropdown` suite from `@orbit-ui/react`
- [ ] Replace event context menu (edit/delete/copy/move) with `<Dropdown>`
- [ ] Replace calendar selector dropdown with `<Dropdown>`
- [ ] Replace view mode selector (if dropdown style) with `<Dropdown>`
- [ ] Replace attendee role selector with `<Dropdown>`
- [ ] Replace task priority selector with `<Dropdown>`
- [ ] Replace task status selector with `<Dropdown>`
- [ ] Replace color category selector with `<Dropdown>`
- [ ] Replace reminder time selector with `<Dropdown>`
- [ ] Replace recurrence pattern selector with `<Dropdown>`
- [ ] Replace timezone selector with `<Dropdown>`

### 2.9 Adopt Card Component
- [ ] Import `Card` from `@orbit-ui/react`
- [ ] Use `<Card>` for event detail popover
- [ ] Use `<Card>` for task detail view
- [ ] Use `<Card>` for AI assistant panel
- [ ] Use `<Card>` for mini calendar sidebar
- [ ] Use `<Card>` for schedule list items
- [ ] Use `<Card>` for team availability card
- [ ] Use `<Card>` for notification items

### 2.10 Adopt Skeleton Component
- [ ] Import `Skeleton`, `SkeletonText`, `SkeletonCard` from `@orbit-ui/react`
- [ ] Add `<Skeleton>` for loading calendar grid
- [ ] Add `<Skeleton>` for loading event list
- [ ] Add `<Skeleton>` for loading task list
- [ ] Add `<Skeleton>` for loading team view
- [ ] Add `<SkeletonCard>` for loading event cards
- [ ] Add `<SkeletonText>` for loading AI responses

### 2.11 Adopt Spinner Component
- [ ] Import `Spinner`, `PageLoader` from `@orbit-ui/react`
- [ ] Use `<PageLoader>` for initial app loading
- [ ] Use `<Spinner>` for event creation saving
- [ ] Use `<Spinner>` for task creation saving
- [ ] Use `<Spinner>` for AI assistant processing
- [ ] Use `<Spinner>` for calendar sync in progress
- [ ] Use `<Spinner>` for data fetch loading

### 2.12 Adopt EmptyState Component
- [ ] Import `EmptyState` from `@orbit-ui/react`
- [ ] Add `<EmptyState>` for no events in view
- [ ] Add `<EmptyState>` for no tasks
- [ ] Add `<EmptyState>` for no team members
- [ ] Add `<EmptyState>` for no search results
- [ ] Add `<EmptyState>` for no notifications
- [ ] Add `<EmptyState>` for no upcoming events in agenda view
- [ ] Add `<EmptyState>` for empty day view
- [ ] Add `<EmptyState>` for no AI suggestions

### 2.13 Adopt Alert Component
- [ ] Import `Alert` from `@orbit-ui/react`
- [ ] Use `<Alert>` for event conflict warning
- [ ] Use `<Alert>` for past event warning
- [ ] Use `<Alert>` for calendar sync error
- [ ] Use `<Alert>` for permission denied error
- [ ] Use `<Alert>` for AI assistant errors
- [ ] Use `<Alert>` for network offline warning
- [ ] Use `<Alert>` for overdue task warning

### 2.14 Adopt Tooltip Component
- [ ] Import `Tooltip` from `@orbit-ui/react`
- [ ] Add `<Tooltip>` on event chips (show full title + time)
- [ ] Add `<Tooltip>` on navigation buttons (prev/next/today)
- [ ] Add `<Tooltip>` on view mode buttons
- [ ] Add `<Tooltip>` on action buttons (create, edit, delete)
- [ ] Add `<Tooltip>` on attendee avatars (show name)
- [ ] Add `<Tooltip>` on task priority badges
- [ ] Add `<Tooltip>` on mini calendar dates
- [ ] Add `<Tooltip>` on team availability slots
- [ ] Add `<Tooltip>` on color category swatches
- [ ] Add `<Tooltip>` on recurring event indicator

### 2.15 Adopt DatePicker Component
- [ ] Import `DatePicker` from `@orbit-ui/react`
- [ ] Replace event date selection with `<DatePicker>`
- [ ] Replace event date range selection with `<DatePicker>` range mode
- [ ] Replace task due date selection with `<DatePicker>`
- [ ] Replace calendar navigation date picker with `<DatePicker>`
- [ ] Replace date filter inputs with `<DatePicker>`

### 2.16 Adopt TimePicker Component
- [ ] Import `TimePicker` from `@orbit-ui/react`
- [ ] Replace event start time selection with `<TimePicker>`
- [ ] Replace event end time selection with `<TimePicker>`
- [ ] Replace reminder time selection with `<TimePicker>`
- [ ] Replace working hours configuration with `<TimePicker>`

### 2.17 Adopt Checkbox/Switch Components
- [ ] Import `Checkbox`, `Switch` from `@orbit-ui/react`
- [ ] Replace task completion checkbox with `<Checkbox>`
- [ ] Replace "all-day event" toggle with `<Switch>`
- [ ] Replace "repeat event" toggle with `<Switch>`
- [ ] Replace "private event" toggle with `<Switch>`
- [ ] Replace calendar visibility toggles with `<Checkbox>`
- [ ] Replace notification toggles with `<Switch>`
- [ ] Replace reminder enabled toggle with `<Switch>`
- [ ] Replace AI auto-schedule toggle with `<Switch>`

### 2.18 Adopt Tag/Chip Component
- [ ] Import `Tag` from `@orbit-ui/react`
- [ ] Use `<Tag>` for event attendee chips (with remove)
- [ ] Use `<Tag>` for task tags
- [ ] Use `<Tag>` for calendar category labels
- [ ] Use `<Tag>` for event source tags (Google Calendar, iCal)
- [ ] Use `<Tag>` for task project labels

### 2.19 Adopt Sidebar Component
- [ ] Import `Sidebar` from `@orbit-ui/react`
- [ ] Use `<Sidebar>` for left panel (mini calendar + calendars list)
- [ ] Use `Sidebar.Section` for calendar groups
- [ ] Use `Sidebar.Item` for individual calendars
- [ ] Sidebar collapse/expand integration

### 2.20 Adopt Divider Component
- [ ] Import `Divider` from `@orbit-ui/react`
- [ ] Use `<Divider>` between calendar views and side panel
- [ ] Use `<Divider>` between event modal sections
- [ ] Use `<Divider>` between task list sections
- [ ] Use `<Divider>` between settings sections
- [ ] Use `<Divider>` between schedule list date groups

### 2.21 Adopt Toast/Notification
- [ ] Import `useToast` from `@orbit-ui/react`
- [ ] Show toast on event created successfully
- [ ] Show toast on event updated
- [ ] Show toast on event deleted
- [ ] Show toast on task created
- [ ] Show toast on task completed
- [ ] Show toast on calendar synced
- [ ] Show toast on invitation sent
- [ ] Show toast on error (save failed, sync failed)
- [ ] Show toast on AI suggestion applied

### 2.22 Adopt Popover Component
- [ ] Import `Popover` from `@orbit-ui/react`
- [ ] Use `<Popover>` for quick event creation (click on time slot)
- [ ] Use `<Popover>` for event preview on chip click
- [ ] Use `<Popover>` for color picker
- [ ] Use `<Popover>` for attendee autocomplete
- [ ] Use `<Popover>` for timezone selector

### 2.23 Adopt Breadcrumb Component
- [ ] Import `Breadcrumb` from `@orbit-ui/react`
- [ ] Use `<Breadcrumb>` for Calendar > Week > Mon Jan 15 navigation
- [ ] Use `<Breadcrumb>` for nested team views

### 2.24 Adopt Progress Component
- [ ] Import `Progress` from `@orbit-ui/react`
- [ ] Use `<Progress>` for task completion progress (per project)
- [ ] Use `<Progress>` for AI assistant processing
- [ ] Use `<Progress>` for calendar sync progress
- [ ] Use `<Progress>` for import progress

---

## 3. Dark Mode

### 3.1 Calendar Grid — Month View
- [ ] Month grid background dark mode
- [ ] Month grid cell borders dark mode
- [ ] Month grid cell hover state dark mode
- [ ] Month grid today cell highlight dark mode
- [ ] Month grid weekend cell shading dark mode
- [ ] Month grid past dates muted color dark mode
- [ ] Month grid date numbers dark mode
- [ ] Month grid day headers (Mon-Sun) dark mode
- [ ] Month grid "more events" link dark mode
- [ ] Month grid event chips dark mode (all color variants)

### 3.2 Calendar Grid — Week View
- [ ] Week view time column dark mode
- [ ] Week view time slot borders dark mode
- [ ] Week view time slot hover state dark mode
- [ ] Week view current time indicator line dark mode
- [ ] Week view today column highlight dark mode
- [ ] Week view all-day events row dark mode
- [ ] Week view event blocks dark mode (all color variants)
- [ ] Week view event block hover state dark mode
- [ ] Week view event block selected state dark mode
- [ ] Week view working hours vs non-working hours dark mode
- [ ] Week view weekend columns dark mode
- [ ] Week view drag-to-create selection dark mode
- [ ] Week view column headers dark mode

### 3.3 Calendar Grid — Day View
- [ ] Day view time column dark mode
- [ ] Day view time slot borders dark mode
- [ ] Day view time slot hover state dark mode
- [ ] Day view current time indicator dark mode
- [ ] Day view all-day events section dark mode
- [ ] Day view event blocks dark mode
- [ ] Day view working hours shading dark mode

### 3.4 Calendar Grid — Agenda/Schedule View
- [ ] Agenda view background dark mode
- [ ] Agenda view date group headers dark mode
- [ ] Agenda view event list items dark mode
- [ ] Agenda view event time display dark mode
- [ ] Agenda view event location display dark mode
- [ ] Agenda view event attendees display dark mode
- [ ] Agenda view "no events" empty state dark mode
- [ ] Schedule list date separators dark mode

### 3.5 Event Chips
- [ ] Event chip: blue color variant dark mode
- [ ] Event chip: green color variant dark mode
- [ ] Event chip: red color variant dark mode
- [ ] Event chip: yellow/amber color variant dark mode
- [ ] Event chip: purple color variant dark mode
- [ ] Event chip: orange color variant dark mode
- [ ] Event chip: pink color variant dark mode
- [ ] Event chip: teal color variant dark mode
- [ ] Event chip: custom color variant dark mode
- [ ] Event chip text contrast in dark mode (all variants)
- [ ] Event chip hover state in dark mode
- [ ] Event chip selected state in dark mode
- [ ] All-day event chip dark mode
- [ ] Multi-day spanning event chip dark mode

### 3.6 Event Modal (EventModal.tsx)
- [ ] Modal background/overlay dark mode
- [ ] Modal card background dark mode
- [ ] Modal card border dark mode
- [ ] Event title input dark mode
- [ ] Event date picker dark mode
- [ ] Event time picker dark mode
- [ ] Event location input dark mode
- [ ] Event description textarea dark mode
- [ ] Attendee list dark mode
- [ ] Attendee email input dark mode
- [ ] RSVP status badges dark mode
- [ ] Color category selector dark mode
- [ ] Reminder selector dark mode
- [ ] Recurrence selector dark mode
- [ ] All-day toggle dark mode
- [ ] Private event toggle dark mode
- [ ] Save/cancel buttons dark mode
- [ ] Delete button dark mode
- [ ] Event source tag dark mode
- [ ] Permission info section dark mode

### 3.7 Task Modal (TaskModal.tsx)
- [ ] Modal background/overlay dark mode
- [ ] Modal card background dark mode
- [ ] Task name input dark mode
- [ ] Task description textarea dark mode
- [ ] Due date picker dark mode
- [ ] Priority selector dark mode
- [ ] Status selector dark mode
- [ ] Assignee selector dark mode
- [ ] Tags input dark mode
- [ ] Project selector dark mode
- [ ] Linked event selector dark mode
- [ ] Save/cancel buttons dark mode

### 3.8 Tasks View (TasksView.tsx)
- [ ] Tasks view background dark mode
- [ ] Tasks view header dark mode
- [ ] Task list container dark mode
- [ ] Task list item rows dark mode
- [ ] Task list item hover state dark mode
- [ ] Task list item selected state dark mode
- [ ] Task completion checkbox dark mode
- [ ] Task name text dark mode
- [ ] Task due date display dark mode
- [ ] Task overdue indicator dark mode
- [ ] Task priority badge dark mode (High/Medium/Low)
- [ ] Task status badge dark mode (To Do/In Progress/Review/Done)
- [ ] Task assignee avatar dark mode
- [ ] Task tags dark mode
- [ ] Task project label dark mode
- [ ] Task filter bar dark mode
- [ ] Task sort controls dark mode
- [ ] Task search input dark mode
- [ ] Task empty state dark mode
- [ ] Task creation button dark mode

### 3.9 Team View (TeamView.tsx)
- [ ] Team view background dark mode
- [ ] Team view header dark mode
- [ ] Team member rows dark mode
- [ ] Team member avatar dark mode
- [ ] Team member name/role text dark mode
- [ ] Availability grid dark mode
- [ ] Availability: free slots dark mode
- [ ] Availability: busy slots dark mode
- [ ] Availability: tentative slots dark mode
- [ ] Availability time columns dark mode
- [ ] Availability date headers dark mode
- [ ] "Find a time" button dark mode
- [ ] Suggested time slots dark mode
- [ ] Overlay calendars control dark mode
- [ ] Team member filter/search dark mode

### 3.10 AI Assistant Panel (AIAssistant.tsx)
- [ ] AI panel background dark mode
- [ ] AI panel header dark mode
- [ ] AI panel input field dark mode
- [ ] AI panel response bubbles dark mode
- [ ] AI panel suggestion cards dark mode
- [ ] AI panel action buttons dark mode
- [ ] AI panel loading state dark mode
- [ ] AI panel error state dark mode
- [ ] AI panel history items dark mode

### 3.11 Mini Calendar Sidebar
- [ ] Mini calendar background dark mode
- [ ] Mini calendar month/year header dark mode
- [ ] Mini calendar day numbers dark mode
- [ ] Mini calendar today highlight dark mode
- [ ] Mini calendar selected date highlight dark mode
- [ ] Mini calendar weekend dates dark mode
- [ ] Mini calendar event indicator dots dark mode
- [ ] Mini calendar navigation arrows dark mode
- [ ] Mini calendar week numbers (if shown) dark mode

### 3.12 Calendar List Sidebar
- [ ] Calendar list section header dark mode
- [ ] Calendar checkbox items dark mode
- [ ] Calendar color swatches dark mode
- [ ] Calendar name text dark mode
- [ ] "Add calendar" button dark mode
- [ ] Calendar settings button dark mode
- [ ] Calendar group dividers dark mode

### 3.13 App Header/Navigation
- [ ] Header background dark mode
- [ ] Header border dark mode
- [ ] Navigation buttons dark mode
- [ ] Date range display dark mode
- [ ] View mode selector dark mode
- [ ] Create event button dark mode
- [ ] Search input dark mode
- [ ] User avatar/menu dark mode
- [ ] Notification bell dark mode
- [ ] ThemeToggle verified dark mode

### 3.14 Notifications Panel
- [ ] Notification panel background dark mode
- [ ] Notification item rows dark mode
- [ ] Notification unread indicator dark mode
- [ ] Notification timestamp dark mode
- [ ] Notification action buttons dark mode
- [ ] Notification empty state dark mode

### 3.15 Schedule List View (ScheduleListView.tsx)
- [ ] Schedule list background dark mode
- [ ] Schedule list date group headers dark mode
- [ ] Schedule list event items dark mode
- [ ] Schedule list time display dark mode
- [ ] Schedule list event details dark mode
- [ ] Schedule list empty state dark mode

### 3.16 Create Event View (CreateEventView.tsx)
- [ ] Create event form background dark mode
- [ ] Create event form fields dark mode
- [ ] Create event form labels dark mode
- [ ] Create event action buttons dark mode

### 3.17 Dark Mode Testing
- [ ] Full dark mode visual audit of all views
- [ ] Test dark mode toggle (no flash)
- [ ] Test dark mode persistence across refresh
- [ ] Test system preference detection
- [ ] Screenshot comparison: light vs dark all views
- [ ] Verify no hardcoded white/black colors remain
- [ ] Verify event chip colors readable in dark mode
- [ ] Verify calendar grid borders visible in dark mode
- [ ] Verify time indicator line visible in dark mode
- [ ] Verify all form inputs have proper dark background

---

## 4. Core Features

### 4.1 Calendar Views — Month View
- [x] Full month grid with event chips (CalendarView.tsx)
- [ ] Month view: 6-row grid (always show 6 weeks)
- [ ] Month view: day number in each cell
- [ ] Month view: event chips in cells (truncated to 2-3 per cell)
- [ ] Month view: "+N more" link when events overflow cell
- [ ] Month view: click "+N more" to show all events popover
- [ ] Month view: today cell highlighted
- [ ] Month view: weekend cells shaded
- [ ] Month view: past dates muted
- [ ] Month view: click on date navigates to day view
- [ ] Month view: click on event chip opens event detail
- [ ] Month view: drag event chip to different date (move event)
- [ ] Month view: multi-day events span across cells
- [ ] Month view: all-day events shown at top of cell
- [ ] Month view: week number display (optional)
- [ ] Month view: responsive — fewer chips on smaller screens

### 4.2 Calendar Views — Week View
- [x] 7-column time grid with events (CalendarView.tsx)
- [x] Time slots (using 80px per hour)
- [x] Column-based event positioning
- [x] Drag-to-create event (drag selection state)
- [x] Drag-to-move event (drag info state)
- [ ] Week view: 24-hour time column on left
- [ ] Week view: 15-minute slot height markers
- [ ] Week view: 30-minute slot borders (visible)
- [ ] Week view: 1-hour slot borders (stronger)
- [ ] Week view: current time indicator (red line across current time)
- [ ] Week view: current time indicator auto-scrolls to view
- [ ] Week view: today column highlighted
- [ ] Week view: all-day events row at top
- [ ] Week view: working hours shading (non-working hours greyed)
- [ ] Week view: configurable working hours (default 9am-5pm)
- [ ] Week view: event blocks with title, time, color
- [ ] Week view: overlapping events side-by-side (column splitting)
- [ ] Week view: click on event opens event detail
- [ ] Week view: click on empty slot opens quick-create
- [ ] Week view: drag to select time range creates event
- [ ] Week view: drag event to new time (reschedule)
- [ ] Week view: drag event bottom edge to resize (change duration)
- [ ] Week view: scroll to current time on load
- [ ] Week view: snap to 15-minute intervals when dragging
- [ ] Week view: keyboard navigation (arrow keys between slots)

### 4.3 Calendar Views — Day View
- [ ] Day view: single column time grid
- [ ] Day view: 24-hour time column on left
- [ ] Day view: 15-minute slot markers
- [ ] Day view: current time indicator
- [ ] Day view: all-day events section at top
- [ ] Day view: event blocks full width
- [ ] Day view: overlapping events side-by-side
- [ ] Day view: click on empty slot opens quick-create
- [ ] Day view: drag to select time range
- [ ] Day view: drag event to reschedule
- [ ] Day view: drag event edge to resize
- [ ] Day view: weather/temperature display (optional)
- [ ] Day view: mini calendar in sidebar

### 4.4 Calendar Views — Agenda/List View
- [ ] Agenda view: chronological list of upcoming events
- [ ] Agenda view: grouped by date (date header)
- [ ] Agenda view: event item: title, time, location, attendees
- [ ] Agenda view: event item: color category indicator
- [ ] Agenda view: event item: click to open detail
- [ ] Agenda view: infinite scroll (load more events)
- [ ] Agenda view: configurable date range (next 7/30/90 days)
- [ ] Agenda view: today indicator
- [ ] Agenda view: empty days hidden or shown (configurable)
- [ ] Agenda view: event search/filter

### 4.5 Calendar Navigation
- [x] Navigate forward/backward (week/month/day)
- [x] Current date display
- [ ] "Today" button jumps to current date
- [ ] View mode selector: Day / Week / Month / Agenda
- [ ] View mode keyboard shortcuts (D/W/M/A)
- [ ] Date picker for jump-to-date
- [ ] Swipe gesture for prev/next (mobile)
- [ ] Keyboard shortcut: Left/Right arrow for prev/next
- [ ] Mini calendar in sidebar for quick date navigation
- [ ] Mini calendar click navigates to selected date

### 4.6 Event CRUD — Creation
- [x] Event type defined (CalendarEvent interface)
- [x] Event has id, title, start, end, color, type, description, location, attendees, userId
- [ ] Quick event creation: click on time slot → popover with title + time
- [ ] Quick event creation: type title and press Enter
- [ ] Full event form: title (required)
- [ ] Full event form: date picker (start date)
- [ ] Full event form: time picker (start time)
- [ ] Full event form: date picker (end date)
- [ ] Full event form: time picker (end time)
- [ ] Full event form: duration auto-calculation
- [ ] Full event form: all-day event toggle
- [ ] Full event form: location input (text or map link)
- [ ] Full event form: description (rich text)
- [ ] Full event form: color/category selection
- [ ] Full event form: attendees (email autocomplete)
- [ ] Full event form: reminder selection (15m, 30m, 1h, 1d, custom)
- [ ] Full event form: multiple reminders
- [ ] Full event form: recurrence (daily, weekly, monthly, yearly, custom)
- [ ] Full event form: recurrence end (after N occurrences, on date, never)
- [ ] Full event form: private event toggle
- [ ] Full event form: video meeting link (auto-create Meet link)
- [ ] Full event form: attachments
- [ ] Full event form: notes
- [ ] Full event form: free/busy status
- [ ] Full event form: default calendar selection
- [ ] Full event form: timezone selection
- [ ] Event validation: title required
- [ ] Event validation: end time after start time
- [ ] Event validation: conflict detection (warn if overlapping)
- [ ] Event saved via API on submit
- [ ] Event appears on calendar immediately (optimistic update)

### 4.7 Event CRUD — Reading/Display
- [ ] Event detail popover on chip click
- [ ] Event detail: title, date/time, location
- [ ] Event detail: description (rendered markdown)
- [ ] Event detail: attendees with RSVP status
- [ ] Event detail: color category
- [ ] Event detail: recurrence pattern display
- [ ] Event detail: reminders display
- [ ] Event detail: organizer display
- [ ] Event detail: edit button
- [ ] Event detail: delete button
- [ ] Event detail: duplicate button
- [ ] Event detail: share button
- [ ] Event detail: add to other calendar (ICS download)

### 4.8 Event CRUD — Updating
- [ ] Edit event: open full form pre-filled
- [ ] Edit event: save changes via API
- [ ] Edit event: calendar updates immediately
- [ ] Edit recurring event: "This event only" option
- [ ] Edit recurring event: "This and following events" option
- [ ] Edit recurring event: "All events" option
- [ ] Edit event: drag-to-move (day/time change)
- [ ] Edit event: drag-to-resize (duration change)
- [ ] Edit event: conflict check on save
- [ ] Edit event: undo support (Ctrl+Z after move)

### 4.9 Event CRUD — Deletion
- [ ] Delete event: confirmation dialog
- [ ] Delete event: remove from API
- [ ] Delete event: remove from calendar immediately
- [ ] Delete recurring event: "This event only" option
- [ ] Delete recurring event: "This and following events" option
- [ ] Delete recurring event: "All events" option
- [ ] Delete event: undo option (toast with "Undo" button)

### 4.10 Recurring Events
- [ ] Daily recurrence
- [ ] Weekly recurrence (select weekdays)
- [ ] Bi-weekly recurrence
- [ ] Monthly recurrence (day of month or day of week)
- [ ] Yearly recurrence
- [ ] Custom recurrence (every N days/weeks/months)
- [ ] Recurrence end: after N occurrences
- [ ] Recurrence end: on specific date
- [ ] Recurrence end: never
- [ ] RRULE generation and parsing (RFC 5545)
- [ ] Recurring event indicator on chips
- [ ] Recurring event expansion in views
- [ ] Exception handling (deleted/modified instances)

### 4.11 Event Invitations & RSVPs
- [ ] Add attendees by email to event
- [ ] Attendee autocomplete from org directory
- [ ] Send invitation email on event creation
- [ ] RSVP: Accept invitation
- [ ] RSVP: Decline invitation
- [ ] RSVP: Tentative/Maybe
- [ ] RSVP: Propose new time
- [ ] RSVP status displayed on event (accepted/declined/tentative/pending)
- [ ] RSVP count summary (3 accepted, 1 declined)
- [ ] Notification on RSVP response
- [ ] Update attendees on event edit (notify of changes)
- [ ] Remove attendee from event
- [ ] Optional attendees (vs required)
- [ ] Attendee permission: can modify / can invite others

### 4.12 Tasks — CRUD
- [x] Task type defined (Task interface: id, name, project, dueDate, priority, status, etc.)
- [x] TasksView component
- [x] TaskModal component
- [ ] Create task: name (required)
- [ ] Create task: due date
- [ ] Create task: priority (High/Medium/Low)
- [ ] Create task: status (To Do/In Progress/Review/Done)
- [ ] Create task: description
- [ ] Create task: assignee(s)
- [ ] Create task: tags
- [ ] Create task: project association
- [ ] Create task: linked calendar event
- [ ] Edit task: update all fields
- [ ] Delete task: with confirmation
- [ ] Task completion: toggle checkbox
- [ ] Task completion: strikethrough text and muted style
- [ ] Task saved via API

### 4.13 Tasks — Views & Interaction
- [ ] Task list: filter by status
- [ ] Task list: filter by priority
- [ ] Task list: filter by assignee
- [ ] Task list: filter by project
- [ ] Task list: filter by date range
- [ ] Task list: search by name
- [ ] Task list: sort by due date
- [ ] Task list: sort by priority
- [ ] Task list: sort by status
- [ ] Task list: sort by name
- [ ] Task list: group by status
- [ ] Task list: group by priority
- [ ] Task list: group by project
- [ ] Task overdue highlighting (past due date, not done)
- [ ] Task drag to calendar (creates time block event)
- [ ] Task detail panel (click on task)
- [ ] Task bulk actions (select multiple → bulk status change / delete)

### 4.14 Team View — Availability
- [x] TeamView component
- [ ] Team member list display
- [ ] Team member avatar, name, role
- [ ] Team member availability grid (free/busy)
- [ ] Availability: free slots (green/open)
- [ ] Availability: busy slots (red/blocked)
- [ ] Availability: tentative slots (yellow/hatched)
- [ ] Availability: out of office (gray)
- [ ] Availability time range (configurable, e.g., 8am-6pm)
- [ ] Availability date range (today + next 5 days)
- [ ] Overlay team member calendars on main calendar
- [ ] Toggle individual team members on/off
- [ ] "Find a time" feature: suggest available slots when all selected members are free
- [ ] Scheduling link generation (share link for others to book)
- [ ] Working hours display per team member

### 4.15 AI Scheduling Assistant
- [x] AIAssistant component
- [ ] AI input: natural language event creation ("Meeting with Sasi tomorrow at 3pm")
- [ ] AI input: find available time ("When can I meet with Alice and Bob this week?")
- [ ] AI input: reschedule ("Move my 2pm to Thursday")
- [ ] AI input: summarize schedule ("What does my week look like?")
- [ ] AI response: suggested event details (title, time, attendees)
- [ ] AI response: available time slots
- [ ] AI response: schedule summary
- [ ] AI: one-click apply suggestion (create event from suggestion)
- [ ] AI: conflict detection ("You already have a meeting at that time")
- [ ] AI: priority-based scheduling (suggest optimal times based on focus blocks)
- [ ] AI: travel time estimation between in-person events
- [ ] AI: smart reminders ("You haven't prepared for tomorrow's presentation")
- [ ] AI: meeting preparation prompts
- [ ] AI: auto-decline conflicts (configurable)
- [ ] AI chat history (conversation log)
- [ ] AI assistant toggle (show/hide panel)
- [ ] AI keyboard shortcut (Ctrl+Shift+A)

### 4.16 Calendar Management
- [ ] Multiple calendars (Personal, Work, Holidays)
- [ ] Calendar color coding (each calendar has a color)
- [ ] Show/hide individual calendars (checkbox toggle)
- [ ] Create new calendar
- [ ] Edit calendar (name, color)
- [ ] Delete calendar (with confirmation)
- [ ] Calendar sharing (share with other users)
- [ ] Calendar permissions (view-only, edit)
- [ ] Default calendar setting
- [ ] Calendar groups (if many calendars)

### 4.17 Import & Export
- [ ] Export events as ICS file (single event)
- [ ] Export events as ICS file (date range / full calendar)
- [ ] Import ICS file (upload and parse)
- [ ] Subscribe to external ICS URL (read-only)
- [ ] Google Calendar sync (OAuth, bidirectional)
- [ ] Microsoft Outlook sync (OAuth, bidirectional)
- [ ] Apple Calendar sync (CalDAV)
- [ ] Import conflict handling (skip / replace / create duplicate)

### 4.18 Timezone Support
- [ ] User timezone setting
- [ ] Events displayed in user's local timezone
- [ ] Timezone selector on event creation
- [ ] Multiple timezone columns (side-by-side display)
- [ ] Timezone conversion tooltip (hover on time shows other timezones)
- [ ] "World clock" mini widget (show 2-3 timezones)
- [ ] Timezone auto-detect from browser
- [ ] Timezone in event invitations

### 4.19 Reminders
- [ ] Default reminder (15 minutes before)
- [ ] Custom reminder times (5m, 10m, 15m, 30m, 1h, 2h, 1d, 2d, 1w)
- [ ] Multiple reminders per event
- [ ] Reminder notification: in-app popup
- [ ] Reminder notification: browser push notification
- [ ] Reminder notification: email
- [ ] Reminder snooze (5m, 10m, 15m, 30m, 1h)
- [ ] Reminder dismiss
- [ ] Default reminder setting per calendar

### 4.20 Room Booking
- [ ] Room resource list (conference rooms)
- [ ] Room availability check during event creation
- [ ] Room selector in event form
- [ ] Room conflict detection
- [ ] Room capacity display
- [ ] Room amenities display (screen, whiteboard, video)
- [ ] Room booking confirmation
- [ ] Room release on event cancellation

### 4.21 Color Categories
- [ ] Default color palette (8-12 colors)
- [ ] Assign color to event
- [ ] Assign color to calendar
- [ ] Color legend display
- [ ] Filter by color/category
- [ ] Custom color creation
- [ ] Color accessible (patterns for color-blind users)

### 4.22 Mini Calendar
- [ ] Mini calendar in sidebar
- [ ] Mini calendar shows current month
- [ ] Mini calendar highlights today
- [ ] Mini calendar highlights selected date
- [ ] Mini calendar shows event indicator dots
- [ ] Mini calendar click navigates main view
- [ ] Mini calendar prev/next month navigation
- [ ] Mini calendar year navigation

### 4.23 Printing
- [ ] Print current view (Day/Week/Month)
- [ ] Print-optimized CSS
- [ ] Print: hide navigation, show only calendar
- [ ] Print: event details included
- [ ] Print: color-coded events
- [ ] Print: page breaks between weeks/months
- [ ] Export to PDF

### 4.24 Orbit Ecosystem Integrations
- [ ] Meet integration: auto-create Meet link for events
- [ ] Meet integration: "Join meeting" button on event
- [ ] Meet integration: meeting recap linked to event
- [ ] Atlas integration: task linked to calendar events
- [ ] Atlas integration: project deadlines on calendar
- [ ] Connect integration: event notifications in Connect
- [ ] Connect integration: share event in channel
- [ ] Mail integration: invitation emails sent via Mail
- [ ] EventBus: publish calendar events to ecosystem
- [ ] EventBus: receive updates from other apps

### 4.25 Keyboard Shortcuts
- [ ] `C` — create new event
- [ ] `T` — go to today
- [ ] `D` — switch to day view
- [ ] `W` — switch to week view
- [ ] `M` — switch to month view
- [ ] `A` — switch to agenda view
- [ ] `Left/Right arrow` — prev/next period
- [ ] `Escape` — close modal/popover
- [ ] `Delete/Backspace` — delete selected event
- [ ] `Enter` — open selected event detail
- [ ] `Ctrl+Z` — undo last action
- [ ] `Ctrl+Shift+A` — open AI assistant
- [ ] `?` — show keyboard shortcuts
- [ ] Keyboard shortcuts help dialog

### 4.26 Search
- [ ] Search events by title
- [ ] Search events by description
- [ ] Search events by location
- [ ] Search events by attendee name/email
- [ ] Search tasks by name
- [ ] Search results with date/time display
- [ ] Search result click navigates to event
- [ ] Search keyboard shortcut (`/` or `Ctrl+F`)
- [ ] Search debounce (300ms)
- [ ] Search filters (date range, calendar, type)

### 4.27 Sharing
- [ ] Share calendar with specific users
- [ ] Share calendar with org
- [ ] Share calendar publicly (view-only link)
- [ ] Share event link (individual event)
- [ ] Embed calendar (iframe for external sites)
- [ ] Scheduling page (Calendly-like booking page)
- [ ] Scheduling page: available times configuration
- [ ] Scheduling page: booking confirmation

---

## 5. API Integration

### 5.1 Event API
- [ ] `GET /api/events` — list events (date range, calendar filter)
- [ ] `POST /api/events` — create event
- [ ] `GET /api/events/:id` — get event detail
- [ ] `PUT /api/events/:id` — update event
- [ ] `DELETE /api/events/:id` — delete event
- [ ] `POST /api/events/:id/rsvp` — respond to invitation
- [ ] `GET /api/events/:id/attendees` — list attendees with RSVP status
- [ ] `POST /api/events/:id/invite` — invite additional attendees
- [ ] `POST /api/events/:id/duplicate` — duplicate event

### 5.2 Recurring Event API
- [ ] `POST /api/events` with RRULE — create recurring event
- [ ] `PUT /api/events/:id?scope=this` — edit single instance
- [ ] `PUT /api/events/:id?scope=following` — edit this and following
- [ ] `PUT /api/events/:id?scope=all` — edit all instances
- [ ] `DELETE /api/events/:id?scope=this` — delete single instance
- [ ] `DELETE /api/events/:id?scope=following` — delete this and following
- [ ] `DELETE /api/events/:id?scope=all` — delete all instances
- [ ] Server-side RRULE expansion (return individual instances)

### 5.3 Task API
- [ ] `GET /api/tasks` — list tasks (filters: status, priority, assignee)
- [ ] `POST /api/tasks` — create task
- [ ] `GET /api/tasks/:id` — get task detail
- [ ] `PUT /api/tasks/:id` — update task
- [ ] `DELETE /api/tasks/:id` — delete task
- [ ] `PUT /api/tasks/:id/complete` — mark task complete
- [ ] `PUT /api/tasks/:id/status` — change task status

### 5.4 Calendar Management API
- [ ] `GET /api/calendars` — list user's calendars
- [ ] `POST /api/calendars` — create calendar
- [ ] `PUT /api/calendars/:id` — update calendar settings
- [ ] `DELETE /api/calendars/:id` — delete calendar
- [ ] `POST /api/calendars/:id/share` — share calendar
- [ ] `GET /api/calendars/:id/subscribers` — list subscribers

### 5.5 Team & Availability API
- [ ] `GET /api/team/members` — list team members
- [ ] `GET /api/availability?users=&start=&end=` — get availability
- [ ] `GET /api/availability/suggest?users=&duration=` — suggest times
- [ ] `POST /api/scheduling-links` — create scheduling link
- [ ] `GET /api/scheduling-links/:slug` — get scheduling page

### 5.6 AI Assistant API
- [ ] `POST /api/ai/schedule` — AI scheduling request
- [ ] `POST /api/ai/suggest` — AI time suggestions
- [ ] `POST /api/ai/summarize` — AI schedule summary
- [ ] `POST /api/ai/parse` — parse natural language to event

### 5.7 Import/Export API
- [ ] `POST /api/import/ics` — import ICS file
- [ ] `GET /api/export/ics?calendar=&start=&end=` — export ICS
- [ ] `POST /api/sync/google` — initiate Google Calendar sync
- [ ] `POST /api/sync/outlook` — initiate Outlook sync
- [ ] `GET /api/sync/status` — check sync status

### 5.8 Notification API
- [ ] `GET /api/notifications` — list notifications
- [ ] `PUT /api/notifications/:id/read` — mark read
- [ ] `PUT /api/notifications/read-all` — mark all read
- [ ] `POST /api/reminders` — create reminder
- [ ] `PUT /api/reminders/:id/snooze` — snooze reminder

### 5.9 Authentication
- [x] Auth helper functions in `lib/auth.ts`
- [x] `getStoredToken()` — retrieve JWT from storage
- [x] `getAuthHeaders()` — build Authorization header
- [x] `persistSessionToken()` — save token
- [x] `clearStoredTokens()` — remove tokens on logout
- [ ] Token refresh interceptor
- [ ] 401 redirect to Gate login
- [ ] `X-Org-Id` header on all requests
- [ ] Axios instance with interceptors configured

### 5.10 Real-time Updates
- [ ] SSE/WebSocket for event changes
- [ ] Real-time event create/update/delete
- [ ] Real-time RSVP updates
- [ ] Real-time reminder triggers
- [ ] EventBus subscription for cross-app events

---

## 6. State Management

### 6.1 Current State (in App.tsx)
- [ ] Extract state from monolithic App.tsx to Zustand store
- [ ] Event state: events list, selected event, editing event
- [ ] Task state: tasks list, selected task, editing task
- [ ] Calendar state: calendars list, visible calendars, active filter
- [ ] Navigation state: current date, view mode (day/week/month)
- [ ] UI state: modals open/closed, panels open/closed
- [ ] User state: profile, preferences, timezone
- [ ] Team state: team members, availability
- [ ] Notification state: notifications list, unread count
- [ ] AI state: conversation history, suggestions

### 6.2 Derived Selectors
- [ ] `getEventsForDateRange(start, end)` — events in visible range
- [ ] `getEventsForDate(date)` — events on specific date
- [ ] `getFilteredTasks(filters)` — tasks matching criteria
- [ ] `getOverdueTasks()` — tasks past due date, not done
- [ ] `getUpcomingEvents(count)` — next N events
- [ ] `getAvailableSlots(users, date)` — free time slots
- [ ] `getCalendarById(id)` — calendar details
- [ ] `getUnreadNotificationCount()` — unread count

### 6.3 Optimistic Updates
- [ ] Event create: show on calendar before API confirms
- [ ] Event update: reflect changes before API confirms
- [ ] Event delete: remove from calendar before API confirms
- [ ] Event move (drag): update position before API confirms
- [ ] Task status change: reflect before API confirms
- [ ] Rollback on API error

---

## 7. Performance

### 7.1 Rendering
- [ ] Memoize calendar grid cells (`React.memo`)
- [ ] Memoize event chips
- [ ] Only re-render visible date range events
- [ ] Virtualize long event lists in agenda view
- [ ] Virtualize task list for 100+ tasks
- [ ] Stable keys for event list (`event.id`)
- [ ] Use `useMemo` for date calculations
- [ ] Use `useCallback` for event handlers
- [ ] Profiler: no component renders > 16ms

### 7.2 Loading & Code Splitting
- [ ] **Split App.tsx into separate components** (critical — 19K lines)
- [ ] Lazy load CalendarView
- [ ] Lazy load TasksView
- [ ] Lazy load TeamView
- [ ] Lazy load EventModal
- [ ] Lazy load TaskModal
- [ ] Lazy load AIAssistant
- [ ] Lazy load ScheduleListView
- [ ] Lazy load CreateEventView
- [ ] Suspense boundaries with fallbacks
- [ ] Preload views on tab hover

### 7.3 Data Loading
- [ ] Only fetch events for visible date range (paginate by month)
- [ ] Cache events for recently viewed months
- [ ] Debounce search input (300ms)
- [ ] Debounce AI assistant input (500ms)
- [ ] Stale-while-revalidate for team availability
- [ ] Background refresh of upcoming events

### 7.4 Drag & Drop
- [ ] Smooth drag performance (requestAnimationFrame)
- [ ] Minimal DOM updates during drag
- [ ] Snap-to-grid during drag (15-minute intervals)
- [ ] Visual feedback during drag (ghost element)
- [ ] Cancel drag on Escape

### 7.5 Bundle Size
- [ ] Bundle size audit (target < 200KB gzipped)
- [ ] Tree-shake unused Axios features
- [ ] Dynamic import for AI assistant
- [ ] Dynamic import for print functionality
- [ ] Dynamic import for ICS parsing library

### 7.6 Web Vitals
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1 (calendar grid must not shift on load)
- [ ] TTI < 3.5s
- [ ] Calendar grid renders within 500ms

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Navigation & Structure
- [ ] Skip-to-main-content link
- [ ] Main content landmark
- [ ] Navigation landmark for header
- [ ] Complementary landmark for sidebar
- [ ] Heading hierarchy (h1 for date range, h2 for sections)
- [ ] Page title updates on view change

### 8.2 Calendar Grid Accessibility
- [ ] Calendar grid uses `role="grid"`
- [ ] Calendar cells use `role="gridcell"`
- [ ] Column headers use `role="columnheader"` (day names)
- [ ] Row headers use `role="rowheader"` (time slots)
- [ ] Arrow key navigation between cells
- [ ] Enter key to create event in selected cell
- [ ] Tab key moves between events within a cell
- [ ] Focus visible indicator on grid cells
- [ ] Screen reader announces date on cell focus
- [ ] Screen reader announces event count in cell

### 8.3 Event Accessibility
- [ ] Event chips are keyboard focusable
- [ ] Event chips have `aria-label` (title + time + location)
- [ ] Enter key opens event detail
- [ ] Delete key deletes selected event (with confirmation)
- [ ] Escape key closes event detail popover
- [ ] Drag-and-drop has keyboard alternative (cut/paste or dialog)
- [ ] Event creation dialog fully keyboard navigable
- [ ] Event form fields have visible labels
- [ ] Required fields marked with `aria-required`
- [ ] Error messages linked with `aria-describedby`

### 8.4 Screen Reader Support
- [ ] ARIA live region for event creation confirmation
- [ ] ARIA live region for event deletion confirmation
- [ ] ARIA live region for view change notification
- [ ] ARIA live region for reminder notifications
- [ ] `role="status"` on notification count
- [ ] `role="dialog"` on all modals
- [ ] `role="alert"` on error messages
- [ ] Announce navigation (e.g., "Now showing January 2026, Week view")
- [ ] Announce event drag result ("Event moved to Tuesday 3pm")

### 8.5 Color & Contrast
- [ ] All text meets 4.5:1 contrast ratio
- [ ] Interactive elements meet 3:1 contrast
- [ ] Event colors supplemented with patterns/icons for color-blind users
- [ ] Today highlight distinguishable without color alone
- [ ] Priority levels have text labels, not just colors
- [ ] Status indicators have text labels

### 8.6 Time & Date
- [ ] All dates displayed in accessible format (not abbreviations only)
- [ ] Time format configurable (12h/24h)
- [ ] Date format configurable (locale-based)
- [ ] Screen reader reads full date/time (not "1/15" but "January 15, 2026")

### 8.7 Testing
- [ ] Tested with NVDA on Windows
- [ ] Tested with VoiceOver on macOS
- [ ] Tested with TalkBack on Android
- [ ] Automated axe-core audit (0 violations)
- [ ] Lighthouse accessibility score > 90
- [ ] Calendar grid keyboard navigation tested end-to-end

---

## 9. Mobile & Responsive

### 9.1 Layout Breakpoints
- [ ] Mobile (< 640px): single-panel, agenda default
- [ ] Tablet (640px - 1024px): calendar with collapsible sidebar
- [ ] Desktop (> 1024px): full three-panel layout

### 9.2 Mobile Calendar View
- [ ] Mobile: agenda view as default (not month grid)
- [ ] Mobile: month view simplified (just date numbers + event dots)
- [ ] Mobile: week view horizontal scroll
- [ ] Mobile: day view full width
- [ ] Mobile: swipe left/right to change period
- [ ] Mobile: pull-down for today
- [ ] Mobile: mini calendar as top overlay
- [ ] Mobile: floating "+" button for create event

### 9.3 Mobile Event Management
- [ ] Mobile: event creation as bottom sheet
- [ ] Mobile: event detail as bottom sheet
- [ ] Mobile: event edit as full-screen modal
- [ ] Mobile: touch-and-hold to create event on time slot
- [ ] Mobile: swipe to delete event
- [ ] Mobile: date/time pickers native mobile pickers

### 9.4 Mobile Task Management
- [ ] Mobile: task list full width
- [ ] Mobile: task creation as bottom sheet
- [ ] Mobile: task detail as bottom sheet
- [ ] Mobile: swipe to complete task
- [ ] Mobile: swipe to delete task

### 9.5 Mobile AI Assistant
- [ ] Mobile: AI assistant as bottom sheet
- [ ] Mobile: AI voice input (speech-to-text)
- [ ] Mobile: AI suggestions as inline cards

### 9.6 Mobile Navigation
- [ ] Mobile: bottom tab bar (Calendar / Tasks / Team / AI)
- [ ] Mobile: header with date + view selector
- [ ] Mobile: sidebar hidden, accessible via hamburger
- [ ] Mobile: pull-to-refresh

### 9.7 Tablet Optimizations
- [ ] Tablet: sidebar collapsed by default
- [ ] Tablet: sidebar expands as overlay
- [ ] Tablet: week view 7 columns (may need horizontal scroll)
- [ ] Tablet: landscape mode uses full layout

### 9.8 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] Swipe gestures for navigation
- [ ] Long press for event context menu
- [ ] Pinch-to-zoom on month view (zoom to week/day)
- [ ] Touch drag to create events
- [ ] Touch drag to move events
- [ ] No hover-dependent interactions

---

## 10. Internationalization (i18n)

### 10.1 Setup
- [ ] i18n library installed (react-i18next)
- [ ] Translation files structure (`src/locales/`)
- [ ] Default locale: English
- [ ] Language detection from browser
- [ ] Language selector in settings

### 10.2 Text Extraction
- [ ] CalendarView text strings extracted
- [ ] EventModal text strings extracted
- [ ] TaskModal text strings extracted
- [ ] TasksView text strings extracted
- [ ] TeamView text strings extracted
- [ ] AIAssistant text strings extracted
- [ ] ScheduleListView text strings extracted
- [ ] CreateEventView text strings extracted
- [ ] Navigation text strings extracted
- [ ] Error messages extracted
- [ ] Empty state messages extracted
- [ ] Button labels extracted
- [ ] Placeholder text extracted
- [ ] Modal titles extracted
- [ ] Notification messages extracted
- [ ] Keyboard shortcut descriptions extracted

### 10.3 Date & Time Localization
- [ ] Month names localized
- [ ] Day names localized
- [ ] Date format follows locale (DD/MM/YYYY vs MM/DD/YYYY)
- [ ] Time format follows locale (12h vs 24h)
- [ ] Relative time ("2 hours ago") localized
- [ ] Duration format localized
- [ ] Week start day configurable (Monday vs Sunday)
- [ ] Calendar header date format localized
- [ ] Event time display localized

### 10.4 RTL Support
- [ ] RTL layout support (Arabic, Hebrew)
- [ ] Calendar grid mirrored for RTL
- [ ] Time column on correct side for RTL
- [ ] Navigation arrows mirrored for RTL
- [ ] Modal/dialog layout mirrored

### 10.5 Translation Files
- [ ] English (en) — complete
- [ ] Spanish (es)
- [ ] French (fr)
- [ ] German (de)
- [ ] Japanese (ja)
- [ ] Chinese Simplified (zh-CN)
- [ ] Arabic (ar) — RTL
- [ ] Portuguese (pt-BR)

---

## 11. Security

### 11.1 Authentication & Authorization
- [x] JWT token management via `lib/auth.ts`
- [x] Token storage and retrieval
- [x] Auth headers on API requests
- [x] Token clearing on logout
- [ ] Token refresh before expiry
- [ ] PKCE flow for OAuth2
- [ ] Session timeout handling
- [ ] Org-level authorization (multi-tenant isolation)
- [ ] Calendar-level permissions (owner/editor/viewer)
- [ ] Event-level permissions (organizer can edit, others view-only)

### 11.2 Input Sanitization
- [ ] Event title sanitized (no HTML injection)
- [ ] Event description sanitized (XSS prevention)
- [ ] Event location sanitized
- [ ] Task name sanitized
- [ ] AI assistant input sanitized
- [ ] Search input sanitized
- [ ] ICS import file validated
- [ ] Attachment upload validated

### 11.3 Data Protection
- [ ] No sensitive data in localStorage (only tokens)
- [ ] Console.log removed in production
- [ ] Error messages don't expose internals
- [ ] API keys not in client bundle
- [ ] Private events not visible to unauthorized users

### 11.4 Content Security
- [ ] CSP headers configured
- [ ] SRI for CDN resources
- [ ] HTTPS enforced
- [ ] CORS configured on backend
- [ ] XSS protection headers

### 11.5 Privacy
- [ ] Private event details hidden from non-attendees
- [ ] Availability shows only free/busy (not event titles) to non-members
- [ ] Team view respects privacy settings
- [ ] ICS export excludes private events (configurable)
- [ ] Scheduling page shows only availability, not event details

---

## 12. Testing

### 12.1 Unit Tests — Utilities
- [ ] Test date calculation utilities (getMonday, getWeekDates)
- [ ] Test event positioning (getColForDate, getTopForTime, getHeightForDuration)
- [ ] Test event overlap detection
- [ ] Test recurring event RRULE expansion
- [ ] Test ICS parsing
- [ ] Test ICS generation
- [ ] Test timezone conversion
- [ ] Test auth helpers (getStoredToken, getAuthHeaders, etc.)
- [ ] Test color utility functions
- [ ] Test search/filter logic

### 12.2 Unit Tests — Components
- [ ] Test `CalendarView` — renders correct month grid
- [ ] Test `CalendarView` — renders correct week grid
- [ ] Test `CalendarView` — renders correct day grid
- [ ] Test `CalendarView` — today highlight
- [ ] Test `CalendarView` — event chip rendering
- [ ] Test `CalendarView` — navigation (prev/next)
- [ ] Test `EventModal` — renders form fields
- [ ] Test `EventModal` — form validation
- [ ] Test `EventModal` — submit creates event
- [ ] Test `EventModal` — edit mode pre-fills data
- [ ] Test `TaskModal` — renders form fields
- [ ] Test `TaskModal` — form validation
- [ ] Test `TaskModal` — submit creates task
- [ ] Test `TasksView` — renders task list
- [ ] Test `TasksView` — filter by status
- [ ] Test `TasksView` — filter by priority
- [ ] Test `TasksView` — task completion toggle
- [ ] Test `TasksView` — sort by due date
- [ ] Test `TeamView` — renders team members
- [ ] Test `TeamView` — availability grid
- [ ] Test `AIAssistant` — renders input
- [ ] Test `AIAssistant` — sends query
- [ ] Test `AIAssistant` — displays response
- [ ] Test `ScheduleListView` — renders event groups
- [ ] Test `CreateEventView` — quick create form

### 12.3 Unit Tests — State/Hooks
- [ ] Test event CRUD actions
- [ ] Test task CRUD actions
- [ ] Test calendar filter state
- [ ] Test navigation state (view mode, current date)
- [ ] Test derived selectors (getEventsForDateRange, etc.)
- [ ] Test optimistic update and rollback

### 12.4 Integration Tests
- [ ] Create event → event appears on calendar
- [ ] Edit event → calendar updates
- [ ] Delete event → event removed from calendar
- [ ] Drag event to new time → event rescheduled
- [ ] Create task → task appears in list
- [ ] Complete task → task marked done
- [ ] Switch view (Month → Week → Day) → correct rendering
- [ ] Navigate (prev/next) → correct date range
- [ ] Search → results displayed
- [ ] AI assistant → suggestion → apply → event created
- [ ] RSVP → status updated on event
- [ ] Import ICS → events appear on calendar

### 12.5 End-to-End Tests (Playwright)
- [ ] E2E: Login → calendar loads with events
- [ ] E2E: Create event → fill form → save → event on calendar
- [ ] E2E: Click event → detail popover → edit → save
- [ ] E2E: Drag event to new time → verify new time
- [ ] E2E: Delete event → confirmation → event removed
- [ ] E2E: Switch views (Day/Week/Month/Agenda)
- [ ] E2E: Navigate forward/backward → correct dates
- [ ] E2E: Create task → mark complete
- [ ] E2E: Team view → check availability
- [ ] E2E: AI assistant → type query → receive suggestion
- [ ] E2E: Import ICS file → events imported
- [ ] E2E: Export ICS file → file downloads
- [ ] E2E: Dark mode toggle → all views render correctly
- [ ] E2E: Mobile viewport → agenda view default → create event
- [ ] E2E: Recurring event → create → edit single instance
- [ ] E2E: Keyboard navigation through calendar grid

### 12.6 Visual Regression Tests
- [ ] Snapshot: Month view (light mode)
- [ ] Snapshot: Month view (dark mode)
- [ ] Snapshot: Week view (light mode)
- [ ] Snapshot: Week view (dark mode)
- [ ] Snapshot: Day view (light mode)
- [ ] Snapshot: Day view (dark mode)
- [ ] Snapshot: Agenda view (light mode)
- [ ] Snapshot: Agenda view (dark mode)
- [ ] Snapshot: Event modal (light mode)
- [ ] Snapshot: Event modal (dark mode)
- [ ] Snapshot: Task modal (light mode)
- [ ] Snapshot: Task modal (dark mode)
- [ ] Snapshot: Tasks view (light mode)
- [ ] Snapshot: Tasks view (dark mode)
- [ ] Snapshot: Team view (light mode)
- [ ] Snapshot: Team view (dark mode)
- [ ] Snapshot: AI assistant (light mode)
- [ ] Snapshot: AI assistant (dark mode)
- [ ] Snapshot: Mobile layout (light + dark)
- [ ] Snapshot: Empty states (all variants)

### 12.7 Performance Tests
- [ ] Lighthouse performance score > 90
- [ ] Bundle size under budget
- [ ] Calendar grid render time < 500ms (100 events)
- [ ] View switch time < 200ms
- [ ] Event drag smoothness (60fps)
- [ ] Search response time < 300ms

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] All exported functions have JSDoc comments
- [ ] All exported types have JSDoc comments
- [ ] Calendar grid calculation documented
- [ ] Event positioning algorithm documented
- [ ] RRULE parsing/generation documented
- [ ] API integration patterns documented

### 13.2 Developer Documentation
- [ ] README.md with setup instructions
- [ ] Environment variables documentation
- [ ] Architecture overview (after App.tsx split)
- [ ] State management guide
- [ ] API endpoint reference
- [ ] Calendar math reference (date calculations)
- [ ] Drag-and-drop implementation guide
- [ ] Deployment guide

### 13.3 User Documentation
- [ ] Feature overview
- [ ] Calendar views guide
- [ ] Event creation guide
- [ ] Recurring events guide
- [ ] Task management guide
- [ ] Team scheduling guide
- [ ] AI assistant guide
- [ ] Keyboard shortcuts reference
- [ ] Import/export guide
- [ ] Troubleshooting FAQ

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [ ] GitHub Actions workflow configured
- [ ] Lint check on PR
- [ ] TypeScript type check on PR
- [ ] Unit tests on PR
- [ ] Integration tests on PR
- [ ] E2E tests on PR
- [ ] Build check on PR
- [ ] Bundle size check
- [ ] Accessibility audit on PR
- [ ] Visual regression on PR
- [ ] Code coverage threshold (> 80%)

### 14.2 CD Pipeline
- [ ] Auto-deploy to staging on develop merge
- [ ] Auto-deploy to production on main merge
- [ ] Docker image build
- [ ] Health check after deployment
- [ ] Rollback mechanism
- [ ] Deployment notifications

### 14.3 Infrastructure
- [ ] Static asset CDN
- [ ] Gzip/Brotli compression
- [ ] Cache headers for hashed assets
- [ ] Custom domain + SSL
- [ ] Error monitoring (Sentry)
- [ ] Performance monitoring (RUM)
- [ ] PWA manifest (add to home screen)
- [ ] Service worker (offline calendar view)

---

## 15. Backend

### 15.1 Calendar API Service
- [ ] Express/Fastify server configured
- [ ] JWT middleware for auth
- [ ] Org isolation middleware (multi-tenant)
- [ ] Request validation (Zod)
- [ ] Error response format
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Request logging

### 15.2 Database
- [ ] Schema: events table
- [ ] Schema: event_attendees table
- [ ] Schema: event_reminders table
- [ ] Schema: event_recurrences table
- [ ] Schema: calendars table
- [ ] Schema: calendar_shares table
- [ ] Schema: tasks table
- [ ] Schema: task_tags table
- [ ] Schema: rooms table (for room booking)
- [ ] Schema: scheduling_links table
- [ ] Schema: notifications table
- [ ] Indexes: events by date range, user_id, calendar_id
- [ ] Full-text search index on event title/description
- [ ] Database migrations setup
- [ ] Database seeding for development

### 15.3 RRULE Processing
- [ ] RRULE parsing (RFC 5545)
- [ ] RRULE expansion (generate instances for date range)
- [ ] RRULE exception handling (EXDATE)
- [ ] RRULE modified instances (RECURRENCE-ID)
- [ ] RRULE serialization for storage
- [ ] Efficient expansion (cache expanded instances)

### 15.4 ICS Processing
- [ ] ICS file parsing (VCALENDAR, VEVENT)
- [ ] ICS file generation
- [ ] ICS import: handle RRULE, VTIMEZONE, VALARM
- [ ] ICS export: include all event properties
- [ ] ICS subscription: periodic fetch from external URL
- [ ] CalDAV server (optional, for Apple Calendar sync)

### 15.5 External Calendar Sync
- [ ] Google Calendar OAuth2 setup
- [ ] Google Calendar API: list events
- [ ] Google Calendar API: create/update/delete events
- [ ] Google Calendar bidirectional sync (webhook or polling)
- [ ] Microsoft Graph API: calendar events
- [ ] Microsoft Graph bidirectional sync
- [ ] Sync conflict resolution (last-write-wins or merge)
- [ ] Sync scheduling (every 5 minutes)

### 15.6 AI Service
- [ ] NLP endpoint for natural language event parsing
- [ ] Availability calculation endpoint
- [ ] Schedule optimization endpoint
- [ ] Summary generation endpoint
- [ ] AI model integration (Anthropic/OpenAI)
- [ ] AI response caching
- [ ] AI rate limiting (per user)

### 15.7 Notification Service
- [ ] Email reminders (via Mail app or SMTP)
- [ ] Push notifications (web push API)
- [ ] In-app notification delivery
- [ ] Reminder scheduling (cron job or delayed queue)
- [ ] Reminder deduplication
- [ ] Timezone-aware scheduling

### 15.8 Monitoring & Ops
- [ ] Health check endpoint
- [ ] Metrics endpoint (Prometheus)
- [ ] Calendar metrics: events created, sync status
- [ ] AI metrics: query count, latency, quality
- [ ] Alert rules for sync failures
- [ ] Alert rules for API errors
- [ ] Log aggregation
- [ ] Database backup strategy
- [ ] Data retention policy

---

## Appendix A: Component-Level Audit

### A.1 App.tsx — Root Component (19K+ lines — MUST SPLIT)
- [x] ThemeToggle from `@orbit-ui/react`
- [x] Auth helpers imported from `lib/auth.ts`
- [x] CalendarEvent type defined inline
- [x] Task type defined inline
- [x] TeamMember type defined inline
- [x] Profile type defined inline
- [x] NotificationItem type defined inline
- [x] EcosystemStatus type defined inline
- [x] EcosystemAppLink type defined inline
- [x] ViewMode type defined ('calendar' | 'tasks' | 'team')
- [ ] Extract CalendarEvent to `src/types/event.ts`
- [ ] Extract Task to `src/types/task.ts`
- [ ] Extract TeamMember to `src/types/team.ts`
- [ ] Extract Profile to `src/types/profile.ts`
- [ ] Extract NotificationItem to `src/types/notification.ts`
- [ ] Extract EcosystemStatus to `src/types/ecosystem.ts`
- [ ] Extract EcosystemAppLink to `src/types/ecosystem.ts`
- [ ] Extract ViewMode to `src/types/view.ts`
- [ ] Extract event state and handlers to `src/hooks/useEvents.ts`
- [ ] Extract task state and handlers to `src/hooks/useTasks.ts`
- [ ] Extract team state and handlers to `src/hooks/useTeam.ts`
- [ ] Extract profile/auth state to `src/hooks/useProfile.ts`
- [ ] Extract notification state to `src/hooks/useNotifications.ts`
- [ ] Extract ecosystem state to `src/hooks/useEcosystem.ts`
- [ ] Extract calendar navigation state to `src/hooks/useCalendarNav.ts`
- [ ] Extract API calls to `src/api/events.ts`
- [ ] Extract API calls to `src/api/tasks.ts`
- [ ] Extract API calls to `src/api/team.ts`
- [ ] Extract API calls to `src/api/profile.ts`
- [ ] Extract API calls to `src/api/notifications.ts`
- [ ] Extract date utilities to `src/utils/date.ts`
- [ ] Extract color utilities to `src/utils/color.ts`
- [ ] Extract calendar grid calculation to `src/utils/calendar.ts`
- [ ] Extract auth flow to separate component/hook
- [ ] Extract header/navigation to `src/components/Header.tsx`
- [ ] Extract sidebar to `src/components/Sidebar.tsx`
- [ ] Extract mini calendar to `src/components/MiniCalendar.tsx`
- [ ] Extract calendar list to `src/components/CalendarList.tsx`
- [ ] Extract notification panel to `src/components/NotificationPanel.tsx`
- [ ] Add error boundary around main content
- [ ] Add error boundary around each view
- [ ] Add loading state for initial data fetch
- [ ] Verify no memory leaks from useEffect cleanup

### A.2 CalendarView.tsx — Calendar Grid
- [x] Week view with 7-column grid
- [x] Hour rows (24 hours, 80px per hour)
- [x] Event positioning by column and time
- [x] Drag-to-create event (drag selection)
- [x] Drag-to-move event (drag info)
- [x] `getMonday()` — calculate week start
- [x] `getColForDate()` — event to column mapping
- [x] `getTopForTime()` — time to Y position mapping
- [x] `getHeightForDuration()` — duration to height (min 42px)
- [x] Scroll container for time grid
- [ ] Month view rendering
- [ ] Day view rendering
- [ ] Agenda view rendering
- [ ] Today highlight in grid
- [ ] Current time indicator (red line)
- [ ] Auto-scroll to current time on load
- [ ] Overlapping event layout (side-by-side)
- [ ] All-day events row
- [ ] Multi-day event spanning
- [ ] Working hours shading
- [ ] Weekend column shading
- [ ] Event click handler (open detail)
- [ ] Empty slot click handler (create event)
- [ ] Drag snap to 15-minute intervals
- [ ] Resize event by dragging bottom edge
- [ ] Calendar grid keyboard navigation
- [ ] CalendarView a11y: grid role
- [ ] CalendarView a11y: cell roles
- [ ] CalendarView a11y: time row headers
- [ ] CalendarView a11y: day column headers

### A.3 EventModal.tsx — Event Detail/Edit Modal
- [ ] Event title display/edit
- [ ] Event date/time display/edit
- [ ] Event location display/edit
- [ ] Event description display/edit
- [ ] Event color/category display/edit
- [ ] Event attendees list
- [ ] Attendee RSVP status display
- [ ] Add attendee input (email autocomplete)
- [ ] Remove attendee button
- [ ] Reminder selector
- [ ] Recurrence selector
- [ ] All-day toggle
- [ ] Private event toggle
- [ ] Video meeting link
- [ ] Save button
- [ ] Cancel button
- [ ] Delete button
- [ ] Duplicate button
- [ ] Form validation (title required, end after start)
- [ ] Modal a11y: focus trap
- [ ] Modal a11y: role="dialog"
- [ ] Modal a11y: form labels

### A.4 TaskModal.tsx — Task Detail/Edit Modal
- [ ] Task name input
- [ ] Task description textarea
- [ ] Due date picker
- [ ] Priority selector (High/Medium/Low)
- [ ] Status selector (To Do/In Progress/Review/Done)
- [ ] Assignee selector
- [ ] Project selector
- [ ] Tags input
- [ ] Linked event selector
- [ ] Save button
- [ ] Cancel button
- [ ] Delete button
- [ ] Form validation (name required)
- [ ] Modal a11y: focus trap
- [ ] Modal a11y: form labels

### A.5 TasksView.tsx — Task List View
- [ ] Task list rendering
- [ ] Task completion checkbox
- [ ] Task name display
- [ ] Task due date display
- [ ] Task priority badge
- [ ] Task status badge
- [ ] Task assignee avatar
- [ ] Task tags display
- [ ] Task overdue highlighting
- [ ] Task click → open TaskModal
- [ ] Filter: by status
- [ ] Filter: by priority
- [ ] Filter: by assignee
- [ ] Filter: by project
- [ ] Sort: by due date
- [ ] Sort: by priority
- [ ] Sort: by name
- [ ] Search: by task name
- [ ] Create task button
- [ ] Bulk select mode
- [ ] Bulk actions (status change, delete)
- [ ] Empty state (no tasks)
- [ ] TasksView a11y: list role
- [ ] TasksView a11y: task items accessible

### A.6 TeamView.tsx — Team Availability View
- [ ] Team member list
- [ ] Team member avatar, name, role
- [ ] Availability grid (time × team members)
- [ ] Free slot display (green/open)
- [ ] Busy slot display (red/blocked)
- [ ] Tentative slot display (yellow)
- [ ] Out of office display (gray)
- [ ] Time range selector
- [ ] Date range selector
- [ ] "Find a time" button
- [ ] Suggested meeting slots
- [ ] Calendar overlay toggle per member
- [ ] TeamView a11y: grid structure
- [ ] TeamView a11y: slot descriptions

### A.7 AIAssistant.tsx — AI Scheduling Panel
- [ ] AI input field
- [ ] Send query button
- [ ] AI response display
- [ ] Suggestion cards (apply/dismiss)
- [ ] Loading state (AI processing)
- [ ] Error state (AI failed)
- [ ] Conversation history
- [ ] Clear history button
- [ ] AI panel toggle (show/hide)
- [ ] AI keyboard shortcut
- [ ] AI voice input (mobile)
- [ ] AI a11y: input labeled
- [ ] AI a11y: responses announced

### A.8 ScheduleListView.tsx — Schedule/Agenda View
- [x] ScheduleGroup type exported
- [ ] Date group headers
- [ ] Event list items within groups
- [ ] Event: time, title, location
- [ ] Event: color indicator
- [ ] Event: attendee avatars
- [ ] Click event → open EventModal
- [ ] Infinite scroll for more dates
- [ ] Empty state (no upcoming events)
- [ ] Today indicator
- [ ] ScheduleListView a11y: list structure

### A.9 CreateEventView.tsx — Quick Event Creation
- [ ] Quick form: title input
- [ ] Quick form: date/time (pre-filled from clicked slot)
- [ ] Quick form: save button
- [ ] Quick form: cancel button
- [ ] Quick form: expand to full form button
- [ ] Popover positioning (near clicked slot)
- [ ] CreateEventView a11y: form labels

---

## Appendix B: Auth Library Audit (lib/auth.ts)

### B.1 Token Management
- [x] `getStoredToken()` — retrieve JWT from storage
- [x] `persistSessionToken()` — save token to storage
- [x] `clearStoredTokens()` — remove all auth tokens
- [x] `getAuthHeaders()` — build headers with Authorization + X-Org-Id
- [x] `safeParseJson()` — safe JSON parse utility
- [ ] Token expiry checking
- [ ] Token refresh mechanism
- [ ] Automatic token refresh before API calls
- [ ] Multi-storage support (localStorage + sessionStorage)
- [ ] Token encoding/decoding utility
- [ ] Auth event broadcasting (login/logout across tabs)

### B.2 OAuth Flow
- [ ] PKCE challenge generation
- [ ] Authorization URL construction
- [ ] Callback code extraction
- [ ] Token exchange (code → access_token)
- [ ] User info fetch from Gate
- [ ] State parameter validation
- [ ] Error handling for failed OAuth

---

## Appendix C: Data Model Audit

### C.1 CalendarEvent Interface
- [x] `id: string`
- [x] `title: string`
- [x] `start: string` (ISO datetime)
- [x] `end: string` (ISO datetime)
- [x] `color: string`
- [x] `type: 'individual' | 'team'`
- [x] `description?: string`
- [x] `location?: string`
- [x] `attendees?: string[]`
- [x] `userId: string`
- [x] `category?: string`
- [x] `source?: string`
- [x] `permissions?: { canEdit: boolean; canDelete: boolean }`
- [ ] `allDay?: boolean` — all-day event flag
- [ ] `recurrence?: string` — RRULE string
- [ ] `recurrenceId?: string` — parent recurring event ID
- [ ] `reminders?: Reminder[]` — reminder configuration
- [ ] `calendarId?: string` — which calendar this belongs to
- [ ] `timezone?: string` — event timezone
- [ ] `videoLink?: string` — Meet/Zoom link
- [ ] `attachments?: Attachment[]` — file attachments
- [ ] `notes?: string` — organizer notes
- [ ] `status?: 'confirmed' | 'tentative' | 'cancelled'`
- [ ] `visibility?: 'public' | 'private'`
- [ ] `freebusy?: 'free' | 'busy' | 'tentative'`
- [ ] `createdAt?: string` — creation timestamp
- [ ] `updatedAt?: string` — last update timestamp

### C.2 Task Interface
- [x] `id: string`
- [x] `name: string`
- [x] `project: string`
- [x] `linkedEvent?: string`
- [x] `dueDate: string`
- [x] `priority: 'High' | 'Medium' | 'Low'`
- [x] `status: 'To Do' | 'In Progress' | 'Review' | 'Done'`
- [x] `description?: string`
- [x] `assignedTo?: string[]`
- [x] `tags?: string[]`
- [x] `mentions?: string[]`
- [x] `startedAt?: string | null`
- [x] `createdAt?: string`
- [x] `updatedAt?: string`
- [ ] `completedAt?: string` — completion timestamp
- [ ] `estimatedHours?: number` — time estimate
- [ ] `actualHours?: number` — time tracked
- [ ] `subtasks?: SubTask[]` — nested subtasks
- [ ] `attachments?: Attachment[]`
- [ ] `comments?: Comment[]`
- [ ] `calendarBlockId?: string` — linked time block event

### C.3 TeamMember Interface
- [x] `id: string`
- [x] `name: string`
- [x] `email?: string`
- [x] `avatar?: string`
- [x] `initials?: string`
- [x] `color?: string`
- [x] `role?: string`
- [ ] `timezone?: string`
- [ ] `workingHours?: { start: string; end: string }`
- [ ] `status?: 'online' | 'offline' | 'away' | 'busy'`
- [ ] `department?: string`

### C.4 Profile Interface
- [x] `id: string`
- [x] `name: string`
- [x] `email: string`
- [x] `initials?: string`
- [x] `avatar?: string`
- [x] `color?: string`
- [x] `role?: string`
- [x] `orgId?: string`
- [x] `tenantId?: string`
- [x] `workspaceId?: string`
- [ ] `timezone?: string`
- [ ] `locale?: string`
- [ ] `preferences?: CalendarPreferences`

### C.5 NotificationItem Interface
- [x] `id: string`
- [x] `title: string`
- [x] `message: string`
- [x] `type: string`
- [x] `read: boolean`
- [x] `createdAt: string`
- [x] `link?: string | null`
- [x] `metadata?: Record<string, unknown>`
- [ ] `eventId?: string` — linked event
- [ ] `taskId?: string` — linked task
- [ ] `actionType?: 'reminder' | 'invitation' | 'update' | 'cancellation'`
- [ ] `expiresAt?: string` — notification expiry

---

## Appendix D: Calendar Math & Utilities

### D.1 Date Calculations
- [x] `getMonday(date)` — get Monday of the week containing date
- [ ] `getWeekDates(date)` — array of 7 dates for the week
- [ ] `getMonthGrid(year, month)` — 6x7 grid of dates
- [ ] `getDaysInMonth(year, month)` — day count
- [ ] `isToday(date)` — check if date is today
- [ ] `isSameDay(date1, date2)` — check if same calendar day
- [ ] `isSameMonth(date1, date2)` — check if same month
- [ ] `isWeekend(date)` — check if Saturday or Sunday
- [ ] `isWorkingHours(date, start, end)` — check if within working hours
- [ ] `addDays(date, n)` — add N days
- [ ] `addWeeks(date, n)` — add N weeks
- [ ] `addMonths(date, n)` — add N months
- [ ] `startOfDay(date)` — midnight of date
- [ ] `endOfDay(date)` — 23:59:59 of date
- [ ] `startOfWeek(date)` — start of week
- [ ] `endOfWeek(date)` — end of week
- [ ] `startOfMonth(date)` — first day of month
- [ ] `endOfMonth(date)` — last day of month

### D.2 Event Positioning
- [x] `getColForDate(dateStr)` — map date to column index
- [x] `getTopForTime(dateStr)` — map time to Y position (80px/hr)
- [x] `getHeightForDuration(start, end)` — duration to height (min 42px)
- [ ] `getOverlappingEvents(events, event)` — find overlapping events
- [ ] `calculateEventColumns(events)` — assign columns for overlapping
- [ ] `calculateEventWidth(event, totalColumns)` — width based on overlap count
- [ ] `calculateEventLeft(event, columnIndex, totalColumns)` — left offset

### D.3 Timezone Utilities
- [ ] `getUserTimezone()` — get user's IANA timezone
- [ ] `convertTimezone(date, fromTz, toTz)` — convert between timezones
- [ ] `formatInTimezone(date, tz, format)` — display time in specific timezone
- [ ] `getTimezoneOffset(tz)` — UTC offset for timezone
- [ ] `getTimezoneAbbreviation(tz)` — e.g., "EST", "PST"

### D.4 RRULE Utilities
- [ ] `parseRRule(rruleString)` — parse RRULE to object
- [ ] `generateRRule(options)` — create RRULE string from options
- [ ] `expandRRule(rrule, start, end)` — generate instances in range
- [ ] `isRecurring(event)` — check if event has recurrence
- [ ] `getNextOccurrence(rrule, after)` — next instance after date
- [ ] `addException(rrule, date)` — add EXDATE
- [ ] `modifyInstance(rrule, date, changes)` — modify single instance

### D.5 ICS Utilities
- [ ] `parseICS(icsString)` — parse ICS text to events
- [ ] `generateICS(events)` — create ICS text from events
- [ ] `generateSingleEventICS(event)` — ICS for single event
- [ ] `parseVTimezone(vtimezone)` — parse timezone definition
- [ ] `parseVAlarm(valarm)` — parse reminder definition

---

*End of 05-CALENDAR.md — Calendar Scheduling App Checklist*
