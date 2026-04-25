# 09 -- Control Center (Operations Hub) -- Comprehensive Checklist

> **App:** Control Center -- Operations Hub (Meeting Management + Org Runtime Status)
> **Stack:** React 19.2.0 | Vite 7 (TW v4) | Tailwind v3 | Zustand | Axios | EventSource SSE
> **Architecture:** SPA with Zustand-managed views (17 views, no React Router)
> **Port:** localhost:45009
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

### 1.1 Toolchain
- [x] Vite 7 initialized with React 19 template
- [x] TypeScript configured (`tsconfig.json`)
- [ ] TypeScript strict mode enabled (`"strict": true`)
- [ ] TypeScript `noUncheckedIndexedAccess` enabled
- [ ] TypeScript `exactOptionalPropertyTypes` enabled
- [x] Tailwind CSS v3 installed and configured
- [ ] Tailwind CSS purge paths verified for production builds
- [ ] PostCSS config validated
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

### 1.2 Dependencies
- [x] `react` 19.2.0 installed
- [x] `react-dom` 19.2.0 installed
- [x] `zustand` installed
- [x] `axios` installed
- [x] `date-fns` installed
- [x] `lucide-react` installed
- [x] `react-hot-toast` installed
- [x] `uuid` installed
- [x] `@orbit-ui/react` installed
- [ ] `clsx` installed (used by cn utility)
- [ ] `tailwind-merge` installed (used by cn utility)
- [ ] All dependencies pinned to exact versions in package.json
- [ ] `package-lock.json` committed and up to date
- [ ] No unused dependencies (run `depcheck`)
- [ ] No known vulnerabilities (`npm audit`)

### 1.3 Project Structure
- [x] `src/App.tsx` -- root component with view router
- [x] `src/main.tsx` -- entry point
- [x] `src/index.css` -- global styles
- [x] `src/store/useAppStore.ts` -- Zustand store
- [x] `src/types/index.ts` -- TypeScript type definitions
- [x] `src/utils/api.ts` -- Axios instance
- [x] `src/utils/cn.ts` -- className utility
- [x] `src/contexts/AuthContext.tsx` -- Gate auth context
- [x] `src/data/seed.ts` -- seed/sample data
- [x] `src/components/layout/Header.tsx` -- top header bar
- [x] `src/components/layout/Sidebar.tsx` -- navigation sidebar
- [x] `src/components/ui/Button.tsx` -- custom button (to be replaced)
- [x] `src/components/ui/Avatar.tsx` -- custom avatar (to be replaced)
- [x] `src/components/ui/Badge.tsx` -- custom badge (to be replaced)
- [x] `src/components/AppLauncher.tsx` -- orbit app launcher
- [ ] `src/hooks/` directory created for custom hooks
- [ ] `src/hooks/useEventBus.ts` -- extracted SSE logic
- [ ] `src/hooks/useMeetings.ts` -- meeting-specific selectors
- [ ] `src/hooks/useNotifications.ts` -- notification-specific selectors
- [ ] `src/hooks/useKeyboardShortcuts.ts` -- global hotkeys
- [ ] `src/hooks/useMediaQuery.ts` -- responsive breakpoint hook
- [ ] `src/hooks/useDebounce.ts` -- debounce utility hook
- [ ] `src/hooks/useLocalStorage.ts` -- typed localStorage hook
- [ ] `src/constants/` directory created
- [ ] `src/constants/routes.ts` -- view name constants
- [ ] `src/constants/config.ts` -- API URLs, feature flags

### 1.4 Index HTML & Shell
- [x] Anti-FOUC script in `index.html` (reads orbit-theme, applies .dark)
- [x] `orbit-tokens.css` linked in `index.html`
- [x] `orbit-bar.js` loaded (deferred)
- [x] `orbit-ui.css` linked
- [x] `orbit-theme-init.js` loaded
- [ ] `<meta name="description">` set for Control Center
- [ ] `<meta name="theme-color">` set (light + dark)
- [ ] Favicon set to Control Center icon
- [ ] Apple touch icon configured
- [ ] Open Graph meta tags for link previews
- [ ] CSP meta tag (Content-Security-Policy)
- [ ] `<noscript>` fallback message

---

## 2. Design System Integration

### 2.1 Token Integration
- [x] `index.css` imports `orbit-tokens.css`
- [x] `index.css` imports `orbit-tailwind-v4.css`
- [x] `ThemeProvider` from `@orbit-ui/react` wraps root
- [ ] `tailwind.config.js` uses orbit tailwind preset
- [ ] All `#6366f1` (indigo) hardcoded hex replaced with `primary-500`
- [ ] All `#4f46e5` hardcoded hex replaced with `primary-600`
- [ ] All `#818cf8` hardcoded hex replaced with `primary-400`
- [ ] All `#e0e7ff` hardcoded hex replaced with `primary-100`
- [ ] All `#eef2ff` hardcoded hex replaced with `primary-50`
- [ ] All `#3730a3` hardcoded hex replaced with `primary-800`
- [ ] All `#1e293b` hardcoded hex replaced with `content-primary` or `neutral-800`
- [ ] All `#475569` hardcoded hex replaced with `content-secondary` or `neutral-600`
- [ ] All `#64748b` hardcoded hex replaced with `content-muted` or `neutral-500`
- [ ] All `#94a3b8` hardcoded hex replaced with `neutral-400`
- [ ] All `#cbd5e1` hardcoded hex replaced with `border-default` or `neutral-300`
- [ ] All `#e2e8f0` hardcoded hex replaced with `border-subtle` or `neutral-200`
- [ ] All `#f1f5f9` hardcoded hex replaced with `surface-muted` or `neutral-100`
- [ ] All `#f8fafc` hardcoded hex replaced with `surface-base` or `neutral-50`
- [ ] All `#ffffff` / `#fff` backgrounds replaced with `surface-base`
- [ ] All `#10b981` (emerald/green) replaced with `success-500`
- [ ] All `#ef4444` (red) replaced with `danger-500`
- [ ] All `#f59e0b` (amber) replaced with `warning-500`
- [ ] All `#3b82f6` (blue) replaced with `info-500`
- [ ] All `outline: 2px solid #6366f1` replaced with `focus-ring` utility
- [ ] All `::selection` hardcoded colors replaced with orbit primary
- [ ] All scrollbar CSS replaced with `.scrollbar-thin` plugin class
- [ ] Remove Google Fonts CDN link (already done per checklist, verify no remnants)
- [ ] Font family uses `var(--orbit-font-family)` or orbit preset

### 2.2 Replace Custom Button Component
- [ ] Replace `src/components/ui/Button.tsx` with `<Button>` from `@orbit-ui/react`
- [ ] Dashboard: "Create Meeting" button uses `<Button variant="primary" size="md">`
- [ ] Dashboard: "View All" links use `<Button variant="ghost" size="sm">`
- [ ] Dashboard: "Load Sample Data" button uses `<Button variant="outline">`
- [ ] Meetings page: "New Meeting" button uses `<Button variant="primary">`
- [ ] Meetings page: filter/sort toggle buttons use `<Button variant="ghost">`
- [ ] MeetingDetail: "Edit" button uses `<Button variant="outline">`
- [ ] MeetingDetail: "Cancel Meeting" button uses `<Button variant="danger">`
- [ ] MeetingDetail: "Accept Invite" button uses `<Button variant="success">`
- [ ] MeetingDetail: "Decline Invite" button uses `<Button variant="danger" variant="outline">`
- [ ] CreateMeeting: "Submit" button uses `<Button variant="primary">`
- [ ] CreateMeeting: "Cancel" button uses `<Button variant="ghost">`
- [ ] ActionItems: "Add Action Item" button uses `<Button variant="primary" size="sm">`
- [ ] ActionItems: complete/delete buttons use `<IconButton>`
- [ ] Notes: "Add Note" button uses `<Button variant="primary">`
- [ ] Notes: pin/delete buttons use `<IconButton>`
- [ ] Settings: "Save" button uses `<Button variant="primary">`
- [ ] Settings: "Cancel" button uses `<Button variant="ghost">`
- [ ] Settings: "Clear Data" button uses `<Button variant="danger">`
- [ ] Analytics: "Export" button uses `<Button variant="outline">`
- [ ] Operations: "Refresh" button uses `<Button variant="ghost">`
- [ ] Notifications: "Mark All Read" button uses `<Button variant="ghost" size="sm">`
- [ ] Notifications: individual "Dismiss" buttons use `<IconButton>`
- [ ] Header: mobile menu toggle uses `<IconButton>`
- [ ] Sidebar: collapse toggle uses `<IconButton>`
- [ ] All button `loading` states use `<Button loading>` prop
- [ ] All button `disabled` states use `<Button disabled>` prop
- [ ] Remove `src/components/ui/Button.tsx` after all replacements

### 2.3 Replace Custom Badge Component
- [ ] Replace `src/components/ui/Badge.tsx` with `<Badge>` from `@orbit-ui/react`
- [ ] Dashboard: meeting type badges (standup, planning, review, retro, 1:1, all-hands, client, other)
- [ ] Dashboard: meeting status badges (scheduled, in-progress, completed, cancelled)
- [ ] Dashboard: notification count badge
- [ ] Meetings: meeting type badges in list
- [ ] Meetings: RSVP status badges (pending, accepted, declined, tentative)
- [ ] MeetingDetail: meeting type badge
- [ ] MeetingDetail: participant RSVP badges
- [ ] MeetingDetail: agenda item status badges
- [ ] MeetingDetail: action item priority badges
- [ ] Analytics: metric change badges (up/down percentages)
- [ ] Operations: service health status badges (up/down)
- [ ] Operations: incident severity badges
- [ ] Pulse: event type badges (project, deal, calendar, mail, planet, connect)
- [ ] Notifications: notification type badges
- [ ] People: role badges (admin, organizer, member)
- [ ] People: online/offline status badges
- [ ] TimeCards: time card status badges (draft, submitted, approved, rejected)
- [ ] Sidebar: unread notification count badge
- [ ] Remove `src/components/ui/Badge.tsx` after all replacements

### 2.4 Replace Custom Avatar Component
- [ ] Replace `src/components/ui/Avatar.tsx` with `<Avatar>` from `@orbit-ui/react`
- [ ] Replace all `<AvatarGroup>` usages with `@orbit-ui/react` `<AvatarGroup>`
- [ ] Dashboard: upcoming meeting participant avatars
- [ ] Dashboard: current user avatar
- [ ] Meetings: meeting card participant avatars
- [ ] MeetingDetail: participant list avatars
- [ ] MeetingDetail: note author avatars
- [ ] MeetingDetail: action item assignee avatars
- [ ] People: team member list avatars
- [ ] Header: current user avatar
- [ ] Sidebar: current user avatar (bottom section)
- [ ] Notifications: notification source avatars
- [ ] Settings: profile avatar with upload
- [ ] Remove `src/components/ui/Avatar.tsx` after all replacements

### 2.5 Adopt Card Component
- [ ] Adopt `<Card>` from `@orbit-ui/react` for all card layouts
- [ ] Dashboard: stats cards (Today's Meetings, In Progress, Completed, Hours)
- [ ] Dashboard: upcoming meetings list card
- [ ] Dashboard: in-progress meetings card
- [ ] Dashboard: pending invites card
- [ ] Dashboard: recent notifications card
- [ ] Dashboard: quick actions card
- [ ] Meetings: individual meeting cards in list
- [ ] MeetingDetail: meeting info card
- [ ] MeetingDetail: agenda card
- [ ] MeetingDetail: notes card
- [ ] MeetingDetail: action items card
- [ ] MeetingDetail: participants card
- [ ] Analytics: metric cards (meeting hours, productivity, etc.)
- [ ] Analytics: chart container cards
- [ ] Operations: service health cards
- [ ] Operations: event flow card
- [ ] Operations: org runtime card
- [ ] Operations: KPI metric cards
- [ ] Pulse: KPI cards
- [ ] Pulse: event feed item cards
- [ ] Pulse: risk cards
- [ ] People: team member cards
- [ ] TimeCards: time card entries
- [ ] TimeCards: summary card
- [ ] Posture: location cards
- [ ] Notifications: notification item cards
- [ ] Settings: settings section cards

### 2.6 Adopt Sidebar Component
- [ ] Replace custom `src/components/layout/Sidebar.tsx` with `<Sidebar>` + `useSidebar` from `@orbit-ui/react`
- [ ] Sidebar: collapsible toggle (expanded/collapsed)
- [ ] Sidebar: section grouping (Main, Tools, System)
- [ ] Sidebar: active item highlight via `activeView` state
- [ ] Sidebar: navigation items with icons (all 12 nav items)
- [ ] Sidebar: unread notification badge on Notifications item
- [ ] Sidebar: user profile section at bottom
- [ ] Sidebar: sign-out button
- [ ] Sidebar: responsive behavior (mobile slide-in, desktop persistent)
- [ ] Sidebar: backdrop overlay on mobile when open
- [ ] Remove custom sidebar CSS and inline styles

### 2.7 Adopt Modal Component
- [ ] Adopt `<Modal>` from `@orbit-ui/react` for all dialogs
- [ ] CreateMeeting: meeting creation modal/page
- [ ] MeetingDetail: edit meeting modal
- [ ] MeetingDetail: cancel meeting confirmation modal
- [ ] MeetingDetail: delete meeting confirmation modal
- [ ] ActionItems: add action item modal
- [ ] ActionItems: edit action item modal
- [ ] ActionItems: delete confirmation modal
- [ ] Notes: add note modal
- [ ] Notes: edit note modal
- [ ] Notes: delete confirmation modal
- [ ] People: add participant modal
- [ ] People: edit participant role modal
- [ ] Settings: clear data confirmation modal
- [ ] Settings: profile edit modal
- [ ] Notifications: notification detail modal
- [ ] TimeCards: create time card modal
- [ ] TimeCards: edit time card modal
- [ ] TimeCards: approval/rejection modal

### 2.8 Adopt Tabs Component
- [ ] Adopt `<Tabs>` from `@orbit-ui/react`
- [ ] Analytics: tab switching between meeting analytics / team activity / cross-app reports
- [ ] Settings: tab switching between Profile / Notifications / Appearance / Data
- [ ] MeetingDetail: tab switching between Agenda / Notes / Action Items / Participants
- [ ] Operations: tab switching between Services / Events / Runtime / Risks
- [ ] People: tab switching between Team / Departments / Roles
- [ ] Pulse: tab switching between KPIs / Trends / Risks / Services
- [ ] TimeCards: tab switching between My Cards / Team Cards / Summary

### 2.9 Adopt EmptyState Component
- [ ] Adopt `<EmptyState>` from `@orbit-ui/react`
- [ ] Dashboard: no meetings scheduled empty state
- [ ] Dashboard: no notifications empty state
- [ ] Dashboard: no action items empty state
- [ ] Meetings: no meetings found empty state
- [ ] Meetings: no search results empty state
- [ ] MeetingDetail: no agenda items empty state
- [ ] MeetingDetail: no notes empty state
- [ ] MeetingDetail: no action items empty state
- [ ] MeetingDetail: no participants empty state
- [ ] CalendarView: no events for selected date empty state
- [ ] Analytics: no data available empty state
- [ ] Operations: no services configured empty state
- [ ] Operations: no incidents empty state
- [ ] Pulse: no events in feed empty state
- [ ] Notifications: no notifications empty state
- [ ] ActionItems: no action items empty state
- [ ] Notes: no notes empty state
- [ ] People: no team members empty state
- [ ] TimeCards: no time cards empty state
- [ ] Posture: no posture data empty state
- [ ] Settings: empty sections placeholder

### 2.10 Adopt Skeleton Component
- [ ] Adopt `<Skeleton>` / `<SkeletonCard>` / `<SkeletonText>` from `@orbit-ui/react`
- [ ] Dashboard: stats cards skeleton
- [ ] Dashboard: upcoming meetings list skeleton
- [ ] Dashboard: in-progress meetings skeleton
- [ ] Dashboard: notifications skeleton
- [ ] Meetings: meeting list skeleton
- [ ] MeetingDetail: meeting info skeleton
- [ ] MeetingDetail: agenda skeleton
- [ ] MeetingDetail: notes skeleton
- [ ] MeetingDetail: action items skeleton
- [ ] CalendarView: calendar grid skeleton
- [ ] Analytics: chart skeletons
- [ ] Analytics: metric cards skeleton
- [ ] Operations: service health skeleton
- [ ] Operations: metric cards skeleton
- [ ] Pulse: KPI skeleton
- [ ] Pulse: feed skeleton
- [ ] Notifications: notification list skeleton
- [ ] People: team member list skeleton
- [ ] TimeCards: time card list skeleton
- [ ] Settings: settings form skeleton

### 2.11 Adopt Toast (Replace react-hot-toast)
- [ ] Replace `react-hot-toast` with `useToast` from `@orbit-ui/react`
- [ ] Remove `<Toaster>` from App.tsx (both auth and main layout)
- [ ] Remove `react-hot-toast` from package.json
- [ ] App.tsx: replace EventBus toast calls with useToast
- [ ] App.tsx: replace session expiry toast with useToast
- [ ] Meeting creation success toast
- [ ] Meeting update success toast
- [ ] Meeting cancellation toast
- [ ] Meeting deletion toast
- [ ] RSVP update toast
- [ ] Note creation toast
- [ ] Note update toast
- [ ] Note deletion toast
- [ ] Agenda item creation toast
- [ ] Agenda item update toast
- [ ] Agenda item deletion toast
- [ ] Action item creation toast
- [ ] Action item completion toast
- [ ] Action item deletion toast
- [ ] Notification dismissed toast
- [ ] Settings saved toast
- [ ] Data cleared toast
- [ ] Profile updated toast
- [ ] Login success toast
- [ ] Login failure toast
- [ ] Registration success toast
- [ ] Registration failure toast
- [ ] Network error toast
- [ ] Offline mode toast
- [ ] Back online toast

### 2.12 Adopt Table Component
- [ ] Adopt `<Table>` from `@orbit-ui/react`
- [ ] People: team members table (sortable by name, role, department)
- [ ] TimeCards: time cards table (sortable by employee, week, hours, status)
- [ ] ActionItems: action items table (sortable by title, assignee, due date, status)
- [ ] Analytics: meeting data table
- [ ] Operations: service health table
- [ ] Notifications: notification log table (admin view)

### 2.13 Adopt Tooltip Component
- [ ] Adopt `<Tooltip>` from `@orbit-ui/react`
- [ ] Sidebar: nav item tooltips when collapsed
- [ ] Dashboard: stat card info tooltips
- [ ] Dashboard: avatar group overflow tooltip ("+3 more")
- [ ] Header: icon button tooltips (notifications, settings, profile)
- [ ] MeetingDetail: participant RSVP status tooltip
- [ ] MeetingDetail: agenda item duration tooltip
- [ ] Analytics: chart data point tooltips
- [ ] Operations: service latency tooltip
- [ ] TimeCards: hours breakdown tooltip

### 2.14 Adopt Spinner / PageLoader Component
- [ ] Replace custom loading spinners with `<Spinner>` from `@orbit-ui/react`
- [ ] App.tsx: auth loading spinner
- [ ] Dashboard: data loading spinner
- [ ] Meetings: list loading spinner
- [ ] MeetingDetail: detail loading spinner
- [ ] Analytics: charts loading spinner
- [ ] Operations: data loading spinner
- [ ] Replace full-page loading with `<PageLoader>` from `@orbit-ui/react`

### 2.15 Adopt Input Component
- [ ] Adopt `<Input>` from `@orbit-ui/react`
- [ ] Header: search input field
- [ ] CreateMeeting: title input
- [ ] CreateMeeting: location input
- [ ] CreateMeeting: meeting link input
- [ ] Settings: profile name input
- [ ] Settings: profile email input
- [ ] Settings: timezone input
- [ ] People: search/filter input
- [ ] ActionItems: action item title input
- [ ] Notes: search notes input

### 2.16 Adopt Select Component
- [ ] Adopt `<Select>` from `@orbit-ui/react`
- [ ] CreateMeeting: meeting type select
- [ ] CreateMeeting: recurrence select
- [ ] CreateMeeting: timezone select
- [ ] CreateMeeting: duration select
- [ ] Meetings: filter by type select
- [ ] Meetings: filter by status select
- [ ] Settings: theme select
- [ ] Settings: timezone select
- [ ] Settings: language select
- [ ] TimeCards: filter by status select
- [ ] People: filter by role select
- [ ] People: filter by department select

### 2.17 Adopt Dropdown Component
- [ ] Adopt `<Dropdown>` from `@orbit-ui/react`
- [ ] Header: user profile dropdown menu
- [ ] Header: notifications dropdown
- [ ] Meetings: meeting card action dropdown (edit, cancel, delete)
- [ ] MeetingDetail: more actions dropdown
- [ ] People: member action dropdown
- [ ] TimeCards: time card action dropdown
- [ ] Analytics: export format dropdown

### 2.18 Adopt DatePicker / TimePicker Component
- [ ] Adopt `<DatePicker>` from `@orbit-ui/react`
- [ ] CreateMeeting: meeting date picker
- [ ] ActionItems: due date picker
- [ ] TimeCards: week start date picker
- [ ] Analytics: date range picker
- [ ] Adopt `<TimePicker>` from `@orbit-ui/react`
- [ ] CreateMeeting: meeting start time picker
- [ ] CreateMeeting: meeting end time picker

### 2.19 Adopt Progress Component
- [ ] Adopt `<Progress>` from `@orbit-ui/react`
- [ ] Dashboard: meeting completion progress
- [ ] Analytics: productivity progress bars
- [ ] Operations: service health score progress
- [ ] Pulse: engagement rate progress
- [ ] TimeCards: hours logged vs. target progress

### 2.20 Adopt Divider Component
- [ ] Adopt `<Divider>` from `@orbit-ui/react`
- [ ] Sidebar: section dividers
- [ ] MeetingDetail: section dividers (agenda/notes/actions)
- [ ] Settings: section dividers
- [ ] People: section dividers

### 2.21 Adopt Accordion Component
- [ ] Adopt `<Accordion>` from `@orbit-ui/react`
- [ ] Settings: collapsible settings sections
- [ ] MeetingDetail: collapsible agenda items with details
- [ ] Operations: collapsible service detail panels

### 2.22 Adopt Pagination Component
- [ ] Adopt `<Pagination>` from `@orbit-ui/react`
- [ ] Meetings: paginated meeting list
- [ ] Notifications: paginated notification list
- [ ] People: paginated team list
- [ ] TimeCards: paginated time card list
- [ ] ActionItems: paginated action items

### 2.23 Adopt Breadcrumb Component
- [ ] Adopt `<Breadcrumb>` from `@orbit-ui/react`
- [ ] MeetingDetail: Dashboard > Meetings > Meeting Title
- [ ] CreateMeeting: Dashboard > Meetings > Create Meeting
- [ ] Settings: Dashboard > Settings > [Section]

### 2.24 Adopt Switch Component
- [ ] Adopt `<Switch>` from `@orbit-ui/react`
- [ ] Settings: notification toggles (email, push, sound)
- [ ] Settings: feature toggles
- [ ] CreateMeeting: "Virtual Meeting" toggle
- [ ] CreateMeeting: "Recurring" toggle

### 2.25 Adopt Checkbox Component
- [ ] Adopt `<Checkbox>` from `@orbit-ui/react`
- [ ] CreateMeeting: attendee selection checkboxes
- [ ] MeetingDetail: agenda item completion checkboxes
- [ ] ActionItems: action item completion checkboxes
- [ ] Settings: preference checkboxes
- [ ] People: bulk selection checkboxes

### 2.26 Adopt Tag / Chip Component
- [ ] Adopt `<Tag>` from `@orbit-ui/react`
- [ ] Meetings: meeting tags display
- [ ] CreateMeeting: tag input/selection
- [ ] MeetingDetail: meeting tags
- [ ] People: skill/role tags

### 2.27 Adopt Alert Component
- [ ] Adopt `<Alert>` from `@orbit-ui/react`
- [ ] Dashboard: upcoming meeting alert
- [ ] Operations: service down alert
- [ ] Pulse: risk alert
- [ ] Settings: unsaved changes alert
- [ ] App: offline mode alert (replace custom banner)

### 2.28 Adopt Drawer / Sheet Component
- [ ] Adopt `<Drawer>` from `@orbit-ui/react`
- [ ] Notifications: notification detail drawer
- [ ] People: member detail drawer
- [ ] MeetingDetail: participant detail drawer

### 2.29 Adopt CommandPalette Component
- [ ] Adopt `<CommandPalette>` from `@orbit-ui/react`
- [ ] Global: Cmd+K / Ctrl+K opens command palette
- [ ] Command: navigate to any view
- [ ] Command: create new meeting
- [ ] Command: search meetings
- [ ] Command: search people
- [ ] Command: search notes
- [ ] Command: toggle theme

---

## 3. Dark Mode

### 3.1 Global Dark Mode
- [ ] `<html>` element gets `.dark` class correctly via orbit-theme-init
- [ ] `ThemeProvider` initializes dark mode from localStorage
- [ ] Theme toggle in header/sidebar works correctly
- [ ] Theme persists across page reloads
- [ ] System preference detection (`prefers-color-scheme: dark`)
- [ ] No FOUC (flash of unstyled content) on page load
- [ ] CSS custom properties switch correctly in dark mode
- [ ] `bg-linear-to-br from-slate-50 via-white to-slate-50` in App.tsx replaced with semantic dark-aware classes

### 3.2 Dashboard Page -- Dark Mode
- [ ] Page background color
- [ ] Stats cards background and border
- [ ] Stats card icon backgrounds
- [ ] Stats card text colors (primary, secondary, muted)
- [ ] Stats card sub-text colors
- [ ] Upcoming meetings list background
- [ ] Meeting card backgrounds
- [ ] Meeting card hover states
- [ ] Meeting card borders
- [ ] Meeting type badge colors in dark mode
- [ ] Meeting status badge colors in dark mode
- [ ] Meeting time text colors
- [ ] Meeting duration text colors
- [ ] In-progress meeting card highlight
- [ ] Pending invites section background
- [ ] Quick actions card background
- [ ] Recent notifications card background
- [ ] Empty state illustrations and text
- [ ] Avatar fallback background colors
- [ ] "View All" link colors

### 3.3 Meetings Page -- Dark Mode
- [ ] Page header background
- [ ] Meeting list container background
- [ ] Individual meeting card backgrounds
- [ ] Meeting card hover effects
- [ ] Meeting card borders
- [ ] Filter bar background
- [ ] Filter button active/inactive states
- [ ] Sort dropdown background
- [ ] Search input background and border
- [ ] Search input placeholder color
- [ ] Meeting type badges
- [ ] Meeting status badges
- [ ] RSVP status indicators
- [ ] Participant avatar borders
- [ ] "No meetings" empty state
- [ ] Pagination controls

### 3.4 MeetingDetail Page -- Dark Mode
- [ ] Page header with meeting title
- [ ] Meeting info card background
- [ ] Meeting type badge
- [ ] Meeting status badge
- [ ] Date/time display
- [ ] Location/link display
- [ ] Participants section background
- [ ] Participant cards
- [ ] RSVP status colors
- [ ] Agenda section background
- [ ] Agenda item cards
- [ ] Agenda item completion checkbox
- [ ] Agenda item duration indicator
- [ ] Notes section background
- [ ] Note cards
- [ ] Note author and timestamp colors
- [ ] Pinned note highlight
- [ ] Note editor background
- [ ] Action items section background
- [ ] Action item cards
- [ ] Action item checkbox
- [ ] Action item due date colors (overdue = red)
- [ ] Action item assignee colors
- [ ] Edit/Cancel/Delete button colors
- [ ] Breadcrumb text colors

### 3.5 CreateMeeting Page -- Dark Mode
- [ ] Form container background
- [ ] Form field labels
- [ ] Input field backgrounds
- [ ] Input field borders
- [ ] Input field focus rings
- [ ] Input field placeholder colors
- [ ] Select dropdown backgrounds
- [ ] Select dropdown options
- [ ] Date picker calendar background
- [ ] Date picker selected date highlight
- [ ] Time picker background
- [ ] Attendee search input
- [ ] Attendee chip/tag colors
- [ ] Attendee list checkbox colors
- [ ] Form validation error colors
- [ ] Form validation error text
- [ ] Submit/Cancel button colors
- [ ] Virtual meeting toggle colors

### 3.6 CalendarView Page -- Dark Mode
- [ ] Calendar grid background
- [ ] Calendar header (month/year)
- [ ] Day cell backgrounds
- [ ] Day cell borders
- [ ] Today highlight
- [ ] Selected day highlight
- [ ] Event chips on calendar
- [ ] Event chip text colors
- [ ] Event chip category colors
- [ ] Month/Week/Day view toggle
- [ ] Navigation arrows
- [ ] Weekend day shading
- [ ] Past day dimming
- [ ] Calendar overlay/popover background
- [ ] Time grid lines (week/day view)
- [ ] Time labels

### 3.7 Analytics Page -- Dark Mode
- [ ] Page header
- [ ] Metric cards backgrounds
- [ ] Metric card numbers
- [ ] Metric card labels
- [ ] Metric change indicators (green up, red down)
- [ ] Chart container backgrounds
- [ ] Chart axis labels
- [ ] Chart grid lines
- [ ] Chart tooltip backgrounds
- [ ] Chart tooltip text
- [ ] Chart dataset colors (ensure contrast in dark mode)
- [ ] Line chart stroke colors
- [ ] Bar chart fill colors
- [ ] Pie/donut chart segment colors
- [ ] Legend text colors
- [ ] Date range selector
- [ ] Export button
- [ ] Tab navigation

### 3.8 Operations Page -- Dark Mode
- [ ] Page header
- [ ] Service health cards
- [ ] Service status indicators (up = green, down = red)
- [ ] Service latency numbers
- [ ] Service name labels
- [ ] Event flow section
- [ ] Event flow timeline
- [ ] Event type badges
- [ ] Org runtime section
- [ ] Runtime metric cards
- [ ] Incident list
- [ ] Incident severity colors
- [ ] Risk cards
- [ ] Risk severity indicators
- [ ] Refresh button

### 3.9 Pulse Page -- Dark Mode
- [ ] Page header
- [ ] KPI cards backgrounds
- [ ] KPI numbers
- [ ] KPI labels
- [ ] KPI trend indicators
- [ ] Service health score bar
- [ ] Trend charts backgrounds
- [ ] Trend chart lines
- [ ] Trend chart axes
- [ ] Risk cards backgrounds
- [ ] Risk severity badges
- [ ] Risk detail text
- [ ] Real-time feed container
- [ ] Feed item cards
- [ ] Feed item timestamps
- [ ] Feed event type badges

### 3.10 Notifications Page -- Dark Mode
- [ ] Page header
- [ ] Notification list container
- [ ] Individual notification cards
- [ ] Unread notification highlight
- [ ] Read notification dimming
- [ ] Notification type icons
- [ ] Notification timestamp colors
- [ ] Notification message text
- [ ] "Mark All Read" button
- [ ] Dismiss button
- [ ] Empty notifications state
- [ ] Notification detail panel

### 3.11 ActionItems Page -- Dark Mode
- [ ] Page header
- [ ] Action item list container
- [ ] Individual action item cards
- [ ] Completion checkbox
- [ ] Completed item strikethrough/dimming
- [ ] Due date colors (upcoming, overdue, no date)
- [ ] Assignee avatar and name
- [ ] Linked meeting reference
- [ ] Add action item button
- [ ] Filter controls
- [ ] Sort controls
- [ ] Empty state

### 3.12 Notes Page -- Dark Mode
- [ ] Page header
- [ ] Note list container
- [ ] Individual note cards
- [ ] Pinned note highlight
- [ ] Note content text
- [ ] Note author and timestamp
- [ ] Note linked meeting reference
- [ ] Add note button
- [ ] Search input
- [ ] Rich text editor (if applicable)
- [ ] Empty state

### 3.13 People Page -- Dark Mode
- [ ] Page header
- [ ] Team member list container
- [ ] Individual member cards
- [ ] Member avatar
- [ ] Member name and role
- [ ] Member department
- [ ] Online/offline status indicator
- [ ] Member email
- [ ] Action buttons (edit, remove)
- [ ] Search input
- [ ] Filter controls
- [ ] Empty state

### 3.14 TimeCards Page -- Dark Mode
- [ ] Page header
- [ ] Time card list container
- [ ] Individual time card cards
- [ ] Week date range display
- [ ] Hours logged display
- [ ] Status badges (draft, submitted, approved, rejected)
- [ ] Employee name and avatar
- [ ] Entries breakdown
- [ ] Submission/approval timestamps
- [ ] Action buttons
- [ ] Filter controls
- [ ] Summary section

### 3.15 Posture Page -- Dark Mode
- [ ] Page header
- [ ] Location status cards
- [ ] In-office/Remote/OOO indicators
- [ ] Team member location list
- [ ] Map/grid view (if applicable)
- [ ] Status toggle controls
- [ ] Summary metrics

### 3.16 Settings Page -- Dark Mode
- [ ] Page header
- [ ] Settings sections cards
- [ ] Form field labels
- [ ] Input backgrounds and borders
- [ ] Toggle/switch track colors
- [ ] Toggle/switch thumb colors
- [ ] Dropdown backgrounds
- [ ] Section dividers
- [ ] Save/Cancel buttons
- [ ] Danger zone section (clear data)
- [ ] Profile section
- [ ] Notification preferences section
- [ ] Appearance section (theme selector)

### 3.17 Auth Page -- Dark Mode
- [ ] Auth page background
- [ ] Login card background
- [ ] Login card border
- [ ] Form field backgrounds
- [ ] Form field borders
- [ ] Form field labels
- [ ] Logo/brand colors
- [ ] Submit button
- [ ] Link colors (register, forgot password)
- [ ] Error message colors
- [ ] Loading spinner

### 3.18 Layout Components -- Dark Mode
- [ ] Header background (`bg-surface-base`)
- [ ] Header border bottom
- [ ] Header text colors
- [ ] Header icon colors
- [ ] Header search input
- [ ] Sidebar background
- [ ] Sidebar border right
- [ ] Sidebar nav item text colors
- [ ] Sidebar nav item active state
- [ ] Sidebar nav item hover state
- [ ] Sidebar collapse toggle button
- [ ] Sidebar logo area
- [ ] Sidebar user profile section
- [ ] Sidebar sign-out button
- [ ] Mobile backdrop overlay color
- [ ] Offline banner (replace hardcoded `bg-red-500`)

### 3.19 Scrollbar Dark Mode
- [ ] Replace `#f1f5f9` scrollbar track with `var(--orbit-surface-muted)`
- [ ] Replace `#cbd5e1` scrollbar thumb with `var(--orbit-border-strong)`
- [ ] Scrollbar hover thumb color
- [ ] Scrollbar in all scrollable containers

### 3.20 Toaster Dark Mode
- [ ] Toast background color in dark mode
- [ ] Toast text color in dark mode
- [ ] Toast border color in dark mode
- [ ] Toast success icon color
- [ ] Toast error icon color
- [ ] Toast shadow in dark mode

---

## 4. Core Features

### 4.1 Dashboard
- [ ] Today's meeting count card
- [ ] Today's meetings count shows accurate number
- [ ] Next meeting countdown timer
- [ ] Next meeting shows correct meeting name and time
- [ ] In-progress meetings count card
- [ ] Completed meetings this week count
- [ ] Total meeting hours this week
- [ ] Acceptance rate metric card
- [ ] Team activity feed widget (cross-app events from EventBus)
- [ ] Action items due today widget
- [ ] Action items due today: shows count and list
- [ ] Action items due today: link to full action items view
- [ ] Quick meeting creation button
- [ ] Quick meeting creation: opens CreateMeeting view
- [ ] Upcoming meetings list (next 5)
- [ ] Upcoming meetings: shows title, time, participants
- [ ] Upcoming meetings: click navigates to MeetingDetail
- [ ] Upcoming meetings: RSVP status shown per meeting
- [ ] In-progress meetings section
- [ ] In-progress meetings: shows title, started time, participants
- [ ] In-progress meetings: "Join" button for virtual meetings
- [ ] Pending invites section
- [ ] Pending invites: list meetings awaiting RSVP
- [ ] Pending invites: accept/decline buttons inline
- [ ] Recent notifications widget (last 5)
- [ ] Recent notifications: click navigates to notification detail
- [ ] Key metrics from other Orbit apps: projects active (Atlas)
- [ ] Key metrics from other Orbit apps: unread emails (Mail)
- [ ] Key metrics from other Orbit apps: deals in pipeline (Planet)
- [ ] Quick actions: navigate to Create Meeting
- [ ] Quick actions: navigate to Meetings
- [ ] Quick actions: navigate to Calendar
- [ ] Quick actions: navigate to Analytics
- [ ] "Load Sample Data" button (development only)
- [ ] Auto-refresh dashboard data on view activation
- [ ] Dashboard data loading state (skeleton)
- [ ] Dashboard error state (API failure)
- [ ] Dashboard empty state (no meetings at all)

### 4.2 Meetings
- [ ] Meeting list view: all meetings
- [ ] Meeting list: filter by status (scheduled, in-progress, completed, cancelled)
- [ ] Meeting list: filter by type (standup, planning, review, retro, 1:1, all-hands, client, other)
- [ ] Meeting list: filter by date range
- [ ] Meeting list: filter by creator
- [ ] Meeting list: filter by attendee/participant
- [ ] Meeting list: search by title
- [ ] Meeting list: search by description
- [ ] Meeting list: sort by date (ascending/descending)
- [ ] Meeting list: sort by title (alphabetical)
- [ ] Meeting list: sort by status
- [ ] Meeting list: sort by type
- [ ] Meeting list: upcoming tab
- [ ] Meeting list: today tab
- [ ] Meeting list: past tab
- [ ] Meeting card: shows title
- [ ] Meeting card: shows meeting type badge
- [ ] Meeting card: shows status badge
- [ ] Meeting card: shows date and time
- [ ] Meeting card: shows duration
- [ ] Meeting card: shows participant avatars
- [ ] Meeting card: shows participant count
- [ ] Meeting card: shows location or meeting link
- [ ] Meeting card: shows virtual meeting indicator
- [ ] Meeting card: click navigates to MeetingDetail
- [ ] Meeting card: action menu (edit, cancel, delete)
- [ ] Meeting card: RSVP quick action (accept/decline)
- [ ] Meeting list: pagination (if >20 meetings)
- [ ] Meeting list: loading state
- [ ] Meeting list: error state
- [ ] Meeting list: empty state (no meetings)
- [ ] Meeting list: no results state (after filtering)

### 4.3 Meeting Detail
- [ ] Meeting title display
- [ ] Meeting description display
- [ ] Meeting type badge
- [ ] Meeting status badge
- [ ] Meeting date and time display
- [ ] Meeting duration display
- [ ] Meeting timezone display
- [ ] Meeting location display (physical)
- [ ] Meeting link display (virtual) with copy button
- [ ] Meeting organizer display
- [ ] Meeting recurrence display
- [ ] Meeting tags display
- [ ] Meeting created/updated timestamps
- [ ] Edit meeting button
- [ ] Cancel meeting button with confirmation
- [ ] Delete meeting button with confirmation
- [ ] RSVP section: accept button
- [ ] RSVP section: decline button
- [ ] RSVP section: tentative button
- [ ] RSVP section: current RSVP status shown
- [ ] Participants list: name, email, avatar
- [ ] Participants list: RSVP status per participant
- [ ] Participants list: organizer badge
- [ ] Participants list: joined-at time (if applicable)
- [ ] Participants: add participant
- [ ] Participants: remove participant
- [ ] Agenda section: list of agenda items
- [ ] Agenda: add new agenda item (title, description, duration, presenter)
- [ ] Agenda: edit agenda item
- [ ] Agenda: delete agenda item
- [ ] Agenda: reorder agenda items (drag-and-drop or up/down)
- [ ] Agenda: mark item complete/incomplete
- [ ] Agenda: total duration calculation
- [ ] Notes section: list of meeting notes
- [ ] Notes: add new note
- [ ] Notes: edit existing note
- [ ] Notes: delete note with confirmation
- [ ] Notes: pin/unpin note
- [ ] Notes: note author and timestamp
- [ ] Notes: rich text formatting (bold, italic, lists)
- [ ] Notes: auto-save while typing
- [ ] Action items section: list of action items
- [ ] Action items: add new action item (title, assignee, due date)
- [ ] Action items: mark complete/incomplete
- [ ] Action items: edit action item
- [ ] Action items: delete action item
- [ ] Action items: assignee avatar and name
- [ ] Action items: due date display (with overdue highlight)
- [ ] Action items: created-at timestamp
- [ ] Back navigation to meetings list
- [ ] Breadcrumb navigation
- [ ] Loading state
- [ ] Error state (meeting not found)

### 4.4 Create Meeting
- [ ] Title input (required, validation)
- [ ] Description textarea (optional)
- [ ] Meeting type selection (standup, planning, review, retro, 1:1, all-hands, client, other)
- [ ] Date selection (date picker)
- [ ] Start time selection (time picker)
- [ ] End time selection (time picker)
- [ ] Duration auto-calculation from start/end
- [ ] Timezone selection
- [ ] Location input (physical address)
- [ ] Virtual meeting toggle
- [ ] Meeting link input (when virtual)
- [ ] Auto-generate Meet room link
- [ ] Auto-create Calendar event
- [ ] Recurrence selection (none, daily, weekly, biweekly, monthly)
- [ ] Participant selection: search by name/email
- [ ] Participant selection: multi-select from org users
- [ ] Participant selection: show selected participants as chips
- [ ] Participant selection: remove selected participant
- [ ] Tags input: add tags
- [ ] Tags input: remove tags
- [ ] Tags input: autocomplete from existing tags
- [ ] Initial agenda items (optional, add during creation)
- [ ] Form validation: title required
- [ ] Form validation: date required
- [ ] Form validation: start time required
- [ ] Form validation: end time required
- [ ] Form validation: end time after start time
- [ ] Form validation: at least one participant (optional)
- [ ] Submit button: creates meeting and navigates to detail
- [ ] Cancel button: navigates back without creating
- [ ] Loading state during submission
- [ ] Error handling: API failure
- [ ] Success toast on creation

### 4.5 Calendar View
- [ ] Month view: full month calendar grid
- [ ] Month view: events displayed as colored chips
- [ ] Month view: click on day to see day's events
- [ ] Month view: click on event to navigate to detail
- [ ] Week view: 7-day grid with time slots
- [ ] Week view: events positioned by time
- [ ] Week view: event duration represented by height
- [ ] Day view: single day with time slots
- [ ] Day view: events positioned by time
- [ ] Day view: event detail on click
- [ ] View toggle: month / week / day
- [ ] Navigation: previous/next month/week/day
- [ ] Navigation: "Today" button
- [ ] Today indicator/highlight
- [ ] Cross-app events: Atlas project milestones
- [ ] Cross-app events: Calendar app events
- [ ] Cross-app events: Meet scheduled meetings
- [ ] Cross-app event aggregation via EventBus
- [ ] Create new meeting from calendar click (date pre-filled)
- [ ] Create new event from calendar click
- [ ] Event color coding by type
- [ ] Event color coding by source app
- [ ] Calendar loading state
- [ ] Calendar empty state (no events)
- [ ] Responsive calendar layout (mobile-friendly)

### 4.6 Analytics
- [ ] Meeting analytics: meetings per week chart
- [ ] Meeting analytics: average duration per meeting type
- [ ] Meeting analytics: no-show rate
- [ ] Meeting analytics: cancellation rate
- [ ] Meeting analytics: most active meeting organizers
- [ ] Meeting analytics: most attended meeting types
- [ ] Meeting analytics: meeting hours per user
- [ ] Meeting analytics: total meeting hours this month
- [ ] Meeting analytics: meetings by day of week
- [ ] Meeting analytics: meetings by time of day
- [ ] Team activity metrics: messages sent (Connect integration)
- [ ] Team activity metrics: tasks completed (Atlas integration)
- [ ] Team activity metrics: deals closed (Planet integration)
- [ ] Cross-app engagement report
- [ ] Time tracking summary (from Atlas timesheets)
- [ ] Productivity score calculation
- [ ] Date range selector (MTD, QTD, YTD, custom)
- [ ] Chart export as PNG
- [ ] Data export as CSV
- [ ] Analytics loading state
- [ ] Analytics empty state (no data)
- [ ] Chart tooltips with detailed data
- [ ] Chart legends
- [ ] Chart responsive sizing

### 4.7 Operations
- [ ] Operations status board: active incidents list
- [ ] Operations status board: blockers
- [ ] Operations status board: risks
- [ ] Service health overview: list all Orbit services
- [ ] Service health: status indicator (up/down)
- [ ] Service health: latency display
- [ ] Service health: last checked timestamp
- [ ] Service health: error message on failure
- [ ] Service health: auto-refresh on interval
- [ ] Department / team health overview
- [ ] Department health: headcount
- [ ] Department health: meeting load
- [ ] Department health: action item completion rate
- [ ] Resource allocation view
- [ ] Resource allocation: team members by department
- [ ] Resource allocation: hours allocated vs. capacity
- [ ] Budget utilization (Capital Hub integration)
- [ ] Budget utilization: department budgets
- [ ] Budget utilization: burn rate
- [ ] Event flow visualization
- [ ] Event flow: recent events from EventBus
- [ ] Event flow: event type distribution
- [ ] Org runtime summary
- [ ] Org runtime: active users
- [ ] Org runtime: storage usage
- [ ] Org runtime: API request count
- [ ] Operations metric cards
- [ ] Operations loading state
- [ ] Operations error state
- [ ] Operations refresh button

### 4.8 Pulse (Real-time Feed)
- [ ] Live event stream from EventBus (SSE)
- [ ] SSE connection established on page load
- [ ] Auto-reconnect EventSource with exponential backoff
- [ ] Reconnect: initial delay 1s
- [ ] Reconnect: max delay 30s
- [ ] Reconnect: backoff multiplier 2x
- [ ] Filter feed by event type: project events
- [ ] Filter feed by event type: deal events
- [ ] Filter feed by event type: calendar events
- [ ] Filter feed by event type: mail events
- [ ] Filter feed by event type: planet events
- [ ] Filter feed by event type: connect events
- [ ] Mark events as seen
- [ ] Mark events as dismissed
- [ ] KPI cards: meetings last 7 days
- [ ] KPI cards: meeting completion rate (30d)
- [ ] KPI cards: open action items
- [ ] KPI cards: overdue action items
- [ ] KPI cards: participant engagement rate
- [ ] KPI cards: flow executions (24h)
- [ ] KPI cards: flow success rate (7d)
- [ ] KPI cards: service health score
- [ ] Trends section: meeting trends chart
- [ ] Trends section: flow execution trends chart
- [ ] Risks section: risk items list
- [ ] Risk items: severity badge (low, medium, high)
- [ ] Risk items: title and detail
- [ ] Services section: service health list
- [ ] Pulse loading state
- [ ] Pulse empty state (no events)
- [ ] Pulse connection status indicator

### 4.9 Notifications
- [ ] Notification list: all notifications
- [ ] Notification list: filter unread only
- [ ] Notification list: filter by type (meeting_invite, meeting_reminder, meeting_cancelled, meeting_updated, rsvp_update, mention)
- [ ] Notification item: title
- [ ] Notification item: message
- [ ] Notification item: type icon
- [ ] Notification item: timestamp (relative: "2 minutes ago")
- [ ] Notification item: read/unread indicator
- [ ] Notification item: click to navigate (if actionUrl exists)
- [ ] Notification item: dismiss button
- [ ] Mark individual notification as read
- [ ] Mark all notifications as read
- [ ] Clear individual notification
- [ ] Notification bell icon in header with unread count
- [ ] Notification bell: click shows dropdown or navigates to page
- [ ] Real-time notification arrival (via EventBus)
- [ ] Desktop notification permission request
- [ ] Desktop notification display for important events
- [ ] Sound notification option
- [ ] Notification preferences in Settings
- [ ] Notification loading state
- [ ] Notification empty state

### 4.10 People & Team
- [ ] Team members list
- [ ] Team member: name
- [ ] Team member: email
- [ ] Team member: avatar
- [ ] Team member: role (admin, organizer, member)
- [ ] Team member: department
- [ ] Team member: timezone
- [ ] Team member: online/offline status
- [ ] Search team members by name
- [ ] Search team members by email
- [ ] Filter by role
- [ ] Filter by department
- [ ] Sort by name
- [ ] Sort by role
- [ ] Sort by department
- [ ] Add team member (invite)
- [ ] Edit team member role
- [ ] Remove team member
- [ ] Team member detail panel/drawer
- [ ] Loading state
- [ ] Empty state

### 4.11 Time Cards
- [ ] Time card list view
- [ ] Time card: week date range display
- [ ] Time card: employee name and avatar
- [ ] Time card: total hours
- [ ] Time card: status badge (draft, submitted, approved, rejected)
- [ ] Time card: entries breakdown (by day)
- [ ] Time card: project code per entry
- [ ] Time card: department per entry
- [ ] Time card: cost center per entry
- [ ] Time card: entry notes
- [ ] Create new time card
- [ ] Edit time card entries
- [ ] Submit time card
- [ ] Approve time card (manager)
- [ ] Reject time card with reason (manager)
- [ ] Time card summary: total hours by period
- [ ] Time card summary: by employee
- [ ] Time card summary: by department
- [ ] Time card summary: by cost center
- [ ] Overtime tracking
- [ ] Overtime alerts
- [ ] Filter by status
- [ ] Filter by employee
- [ ] Filter by week
- [ ] Sort by date
- [ ] Sort by employee
- [ ] Sort by hours
- [ ] Loading state
- [ ] Empty state

### 4.12 Posture
- [ ] Team working locations view
- [ ] Location types: in-office, remote, OOO
- [ ] Per-member location display
- [ ] Location summary counts
- [ ] Update own location status
- [ ] View team members by location
- [ ] Filter by location type
- [ ] Loading state
- [ ] Empty state

### 4.13 Action Items (Standalone View)
- [ ] All action items across all meetings
- [ ] Filter by status (complete/incomplete)
- [ ] Filter by assignee
- [ ] Filter by meeting
- [ ] Filter by due date (overdue, due today, due this week, no date)
- [ ] Sort by due date
- [ ] Sort by created date
- [ ] Sort by title
- [ ] Sort by meeting
- [ ] Mark complete/incomplete
- [ ] Edit action item
- [ ] Delete action item
- [ ] Linked meeting reference (click to navigate)
- [ ] Sync action items to Atlas tasks
- [ ] Bulk actions: mark multiple complete
- [ ] Bulk actions: delete multiple
- [ ] Loading state
- [ ] Empty state

### 4.14 Notes (Standalone View)
- [ ] All notes across all meetings
- [ ] Search notes by content
- [ ] Filter by meeting
- [ ] Filter by author
- [ ] Filter by pinned status
- [ ] Sort by date (newest/oldest)
- [ ] Sort by meeting
- [ ] Note detail view
- [ ] Pin/unpin note
- [ ] Edit note
- [ ] Delete note
- [ ] Export note as PDF
- [ ] Export note as Markdown
- [ ] Rich text rendering
- [ ] Loading state
- [ ] Empty state

### 4.15 Settings
- [ ] Profile section: name edit
- [ ] Profile section: email display
- [ ] Profile section: avatar upload/change
- [ ] Profile section: department edit
- [ ] Profile section: timezone select
- [ ] Notification preferences: email notifications toggle
- [ ] Notification preferences: push notifications toggle
- [ ] Notification preferences: sound toggle
- [ ] Notification preferences: meeting reminders (15min, 30min, 1hr before)
- [ ] Notification preferences: daily digest toggle
- [ ] Appearance: theme selector (light, dark, system)
- [ ] Appearance: sidebar default state (expanded/collapsed)
- [ ] Appearance: density (comfortable, compact)
- [ ] Data management: clear all data
- [ ] Data management: export all data
- [ ] Data management: load sample data (dev only)
- [ ] About section: app version
- [ ] About section: build number
- [ ] Keyboard shortcuts reference
- [ ] Save settings confirmation
- [ ] Unsaved changes warning
- [ ] Loading state
- [ ] Error handling

### 4.16 Auth
- [ ] Gate OAuth PKCE flow
- [ ] Login form: email field
- [ ] Login form: password field
- [ ] Login form: submit button
- [ ] Login form: validation
- [ ] Login form: error messages
- [ ] Login form: loading state
- [ ] Registration form: name field
- [ ] Registration form: email field
- [ ] Registration form: password field
- [ ] Registration form: submit button
- [ ] Registration form: validation
- [ ] OAuth callback handling
- [ ] Token storage in localStorage
- [ ] Token refresh
- [ ] Auto-logout on token expiry
- [ ] Session expiry listener
- [ ] Redirect to Gate login when unauthenticated
- [ ] "Sign out" action: clear tokens, redirect

---

## 5. API Integration

### 5.1 Axios Configuration
- [x] Base Axios instance created (`src/utils/api.ts`)
- [ ] Base URL configurable via environment variable
- [ ] Request interceptor: add Authorization header
- [ ] Request interceptor: add X-Org-Id header
- [ ] Request interceptor: add X-Request-Id header
- [ ] Response interceptor: handle 401 (token expired)
- [ ] Response interceptor: handle 403 (forbidden)
- [ ] Response interceptor: handle 404 (not found)
- [ ] Response interceptor: handle 429 (rate limited)
- [ ] Response interceptor: handle 500 (server error)
- [ ] Response interceptor: handle network errors
- [ ] Request timeout configuration (30s default)
- [ ] Retry logic for failed requests (exponential backoff)
- [ ] Request cancellation on component unmount

### 5.2 Auth API
- [x] POST `/auth/login` -- login
- [x] POST `/auth/register` -- register
- [ ] POST `/auth/refresh` -- token refresh
- [ ] POST `/auth/logout` -- server-side logout
- [ ] GET `/auth/me` -- current user info

### 5.3 Meetings API
- [x] GET `/meetings` -- list all meetings
- [x] POST `/meetings` -- create meeting
- [x] PATCH `/meetings/:id` -- update meeting
- [x] PATCH `/meetings/:id` (status=cancelled) -- cancel meeting
- [x] POST `/meetings/:id/rsvp` -- RSVP to meeting
- [ ] GET `/meetings/:id` -- get single meeting detail
- [ ] DELETE `/meetings/:id` -- hard delete meeting
- [ ] GET `/meetings?status=` -- filter by status
- [ ] GET `/meetings?type=` -- filter by type
- [ ] GET `/meetings?date_from=&date_to=` -- filter by date range
- [ ] GET `/meetings?search=` -- search by title/description
- [ ] GET `/meetings?sort=` -- sort results
- [ ] GET `/meetings?page=&limit=` -- pagination

### 5.4 Notes API
- [x] POST `/notes/:meetingId` -- add note
- [x] PATCH `/notes/:noteId` -- update note
- [x] DELETE `/notes/:noteId` -- delete note
- [x] POST `/notes/:noteId/pin` -- toggle pin

### 5.5 Agenda API
- [x] POST `/agenda/:meetingId` -- add agenda item
- [x] PATCH `/agenda/:itemId` -- update agenda item
- [x] DELETE `/agenda/:itemId` -- delete agenda item
- [x] POST `/agenda/:itemId/toggle` -- toggle completion

### 5.6 Action Items API
- [x] POST `/action-items/:meetingId` -- add action item
- [x] POST `/action-items/:itemId/toggle` -- toggle completion
- [x] DELETE `/action-items/:itemId` -- delete action item
- [ ] PATCH `/action-items/:itemId` -- update action item
- [ ] GET `/action-items` -- list all action items (cross-meeting)

### 5.7 Notifications API
- [x] GET `/notifications` -- list notifications
- [x] POST `/notifications/:id/read` -- mark read
- [x] POST `/notifications/read-all` -- mark all read
- [x] DELETE `/notifications/:id` -- clear notification

### 5.8 Users API
- [x] GET `/users` -- list users
- [x] PATCH `/users/profile` -- update profile
- [ ] GET `/users/:id` -- get single user
- [ ] POST `/users/invite` -- invite new user

### 5.9 Operations API
- [ ] GET `/ops/overview` -- operations overview
- [ ] GET `/ops/services/health` -- service health check
- [ ] GET `/ops/pulse` -- pulse overview

### 5.10 Time Cards API
- [ ] GET `/time-cards` -- list time cards
- [ ] POST `/time-cards` -- create time card
- [ ] PATCH `/time-cards/:id` -- update time card
- [ ] POST `/time-cards/:id/submit` -- submit time card
- [ ] POST `/time-cards/:id/approve` -- approve time card
- [ ] POST `/time-cards/:id/reject` -- reject time card
- [ ] GET `/time-cards/summary` -- time card summary

### 5.11 EventBus Integration
- [x] SSE connection on app load (token + org_id params)
- [ ] SSE connection: use environment variable for EventBus URL
- [ ] SSE reconnect logic: exponential backoff on error
- [ ] SSE reconnect: initial delay 1000ms
- [ ] SSE reconnect: max delay 30000ms
- [ ] SSE reconnect: backoff multiplier 2x
- [ ] SSE reconnect: max retry count (optional)
- [ ] SSE: parse event types correctly (project.updated, deal.created, etc.)
- [ ] SSE: handle all 6 event categories (project, deal, calendar, mail, planet, connect)
- [ ] SSE: show real-time toast for critical events
- [ ] SSE: update Zustand store with new events
- [ ] SSE: don't re-subscribe on view change
- [ ] SSE: clean up connection on logout
- [ ] SSE: handle connection timeout
- [ ] SSE: show connection status indicator

---

## 6. State Management

### 6.1 Zustand Store Structure
- [x] Auth state: currentUser, isAuthenticated, token
- [x] Meeting state: meetings array, meetingsLoaded flag
- [x] Notification state: notifications array
- [x] UI state: sidebarOpen, activeView, searchQuery, selectedMeetingId, loading
- [ ] Analytics state: cached analytics data
- [ ] Operations state: service health data, ops overview
- [ ] Pulse state: KPIs, trends, risks
- [ ] Time cards state: time cards array
- [ ] People state: team members (separate from users)
- [ ] Calendar state: selected date, view mode (month/week/day)

### 6.2 Store Actions
- [x] Auth: login, logout, register, updateProfile
- [x] Meetings: fetchMeetings, createMeeting, updateMeeting, deleteMeeting, cancelMeeting, getMeetingById, rsvpMeeting
- [x] Notes: addNote, updateNote, deleteNote, togglePinNote
- [x] Agenda: addAgendaItem, updateAgendaItem, deleteAgendaItem, toggleAgendaItem
- [x] Action Items: addActionItem, toggleActionItem, deleteActionItem
- [x] Notifications: fetchNotifications, markNotificationRead, markAllNotificationsRead, clearNotification, addNotification
- [x] Users: fetchUsers
- [x] UI: setSidebarOpen, setActiveView, setSearchQuery, setSelectedMeetingId
- [x] Data: clearAllData, loadSampleData
- [ ] Analytics: fetchAnalytics, setDateRange
- [ ] Operations: fetchOpsOverview, fetchServiceHealth
- [ ] Pulse: fetchPulseOverview
- [ ] Time Cards: fetchTimeCards, createTimeCard, updateTimeCard, submitTimeCard, approveTimeCard, rejectTimeCard

### 6.3 Store Persistence
- [x] Zustand persist middleware configured
- [x] Persists: currentUser, isAuthenticated, token
- [x] Rehydration: restores auth header from persisted token
- [x] Rehydration: fetches fresh data on rehydrate
- [ ] Persist: sidebarOpen preference
- [ ] Persist: activeView (restore last view on reload)
- [ ] Persist: theme preference (already handled by orbit-theme-init)
- [ ] Clear persisted data on logout

### 6.4 Store Selectors & Derived State
- [ ] Selector: upcoming meetings (sorted by startTime)
- [ ] Selector: today's meetings
- [ ] Selector: past meetings
- [ ] Selector: in-progress meetings
- [ ] Selector: meetings by type
- [ ] Selector: meetings by status
- [ ] Selector: my meetings (where user is organizer)
- [ ] Selector: pending invites (where user RSVP is pending)
- [ ] Selector: unread notification count
- [ ] Selector: overdue action items
- [ ] Selector: action items due today
- [ ] Selector: current meeting (by selectedMeetingId)
- [ ] Use `useShallow` or `useMemo` to prevent unnecessary re-renders

### 6.5 Optimistic Updates
- [x] Meeting update: optimistic UI
- [x] Meeting cancel: optimistic UI
- [x] Note update: optimistic UI
- [x] Agenda item toggle: optimistic UI
- [x] Action item toggle: optimistic UI
- [x] Notification mark-read: optimistic UI
- [ ] Rollback on API failure for all optimistic updates
- [ ] Show error toast on rollback

---

## 7. Performance

### 7.1 Code Splitting & Lazy Loading
- [ ] All 17 views lazy-loaded with `React.lazy()`
- [ ] Dashboard lazy-loaded
- [ ] Meetings lazy-loaded
- [ ] MeetingDetail lazy-loaded
- [ ] CreateMeeting lazy-loaded
- [ ] CalendarView lazy-loaded
- [ ] Analytics lazy-loaded
- [ ] Operations lazy-loaded
- [ ] Pulse lazy-loaded
- [ ] Notifications lazy-loaded
- [ ] Settings lazy-loaded
- [ ] ActionItems lazy-loaded
- [ ] Notes lazy-loaded
- [ ] People lazy-loaded
- [ ] TimeCards lazy-loaded
- [ ] Posture lazy-loaded
- [ ] Auth lazy-loaded
- [ ] OAuthCallback lazy-loaded
- [ ] `<Suspense>` boundaries around each lazy-loaded view
- [ ] Suspense fallback shows `<Skeleton>` or `<PageLoader>`

### 7.2 Bundle Optimization
- [ ] Vite code splitting configured
- [ ] Vendor chunk: react, react-dom
- [ ] Vendor chunk: date-fns
- [ ] Vendor chunk: lucide-react (tree-shaken)
- [ ] Vendor chunk: zustand
- [ ] Vendor chunk: @orbit-ui/react
- [ ] Bundle size analyzed with `vite-plugin-visualizer`
- [ ] Total bundle size < 500KB gzipped
- [ ] No duplicate dependencies
- [ ] Tree-shaking verified for all imports

### 7.3 Runtime Performance
- [ ] EventSource: don't re-subscribe on view change
- [ ] EventSource: single connection for entire app
- [ ] Dashboard widgets: stale-while-revalidate pattern
- [ ] Meeting list: virtual scrolling for >100 items
- [ ] Notification list: virtual scrolling for >100 items
- [ ] Search: debounced input (300ms)
- [ ] API calls: deduplicated concurrent requests
- [ ] Images/avatars: lazy loading
- [ ] Memoized expensive computations (meeting filters, sorts)
- [ ] React.memo on pure components
- [ ] useMemo for derived state
- [ ] useCallback for event handlers passed to children
- [ ] No unnecessary re-renders (verified with React DevTools Profiler)

### 7.4 Network Performance
- [ ] API response caching (SWR or React Query pattern)
- [ ] Conditional requests (If-None-Match / ETag)
- [ ] Request batching where applicable
- [ ] Prefetch data on hover (meetings detail)
- [ ] Offline support: cache last-fetched data
- [ ] Service worker for asset caching
- [ ] Compression: gzip/brotli on server responses

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
- [ ] Arrow keys navigate within menus, lists, tabs
- [ ] Sidebar navigation keyboard accessible
- [ ] View switching via keyboard
- [ ] Modal trap focus within modal
- [ ] Dropdown menu keyboard navigation
- [ ] Calendar keyboard navigation (arrow keys for days)
- [ ] Meeting card keyboard activation
- [ ] Notification dismiss via keyboard
- [ ] Action item toggle via keyboard
- [ ] Note pin/delete via keyboard
- [ ] Global keyboard shortcuts documented
- [ ] Keyboard shortcut: Cmd+K for command palette
- [ ] Keyboard shortcut: Escape to close panels

### 8.2 Screen Reader Support
- [ ] All images have alt text
- [ ] All icons have aria-labels or aria-hidden
- [ ] All form inputs have associated labels
- [ ] All form inputs have aria-describedby for error messages
- [ ] Sidebar navigation uses `<nav>` with aria-label
- [ ] Main content area uses `<main>` landmark
- [ ] Header uses `<header>` landmark
- [ ] Sidebar uses `<aside>` landmark
- [ ] Modals have aria-modal="true" and role="dialog"
- [ ] Modals have aria-labelledby pointing to title
- [ ] Alerts use role="alert" for live announcements
- [ ] Loading states announced with aria-live="polite"
- [ ] Dynamic content updates announced via aria-live regions
- [ ] Notification count announced to screen readers
- [ ] Meeting status changes announced
- [ ] Action item completion announced
- [ ] Page title updates on view change
- [ ] Breadcrumbs use `<nav>` with aria-label="Breadcrumb"

### 8.3 Color & Contrast
- [ ] All text meets 4.5:1 contrast ratio (normal text)
- [ ] All large text meets 3:1 contrast ratio
- [ ] All interactive elements meet 3:1 contrast against background
- [ ] Status colors not solely reliant on color (include icons/text)
- [ ] Meeting type badges readable in both themes
- [ ] Meeting status badges readable in both themes
- [ ] Chart data distinguishable without color (patterns/labels)
- [ ] Focus ring visible against all backgrounds
- [ ] Error messages not solely indicated by red color
- [ ] Success messages not solely indicated by green color
- [ ] Link text distinguishable from body text (not just by color)

### 8.4 Forms & Inputs
- [ ] All form fields have visible labels
- [ ] Required fields indicated (not just by color)
- [ ] Error messages displayed adjacent to invalid field
- [ ] Error messages descriptive (not just "invalid")
- [ ] Form submission errors summarized at form top
- [ ] Autocomplete attributes on appropriate inputs
- [ ] Input type attributes correct (email, tel, date, etc.)
- [ ] Placeholder text not used as sole label

### 8.5 Motion & Animation
- [ ] `prefers-reduced-motion` respected
- [ ] Animations can be disabled
- [ ] No auto-playing animations that last >5 seconds
- [ ] No flashing content (>3 flashes per second)
- [ ] Skeleton loading does not cause excessive motion

### 8.6 Responsive Accessibility
- [ ] Content readable at 200% zoom
- [ ] Content readable at 400% zoom
- [ ] No horizontal scroll at 320px viewport width
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Tap target spacing minimum 8px

---

## 9. Mobile & Responsive

### 9.1 Breakpoint Strategy
- [ ] Mobile: 0-639px (sm)
- [ ] Tablet: 640-1023px (md)
- [ ] Desktop: 1024-1279px (lg)
- [ ] Wide: 1280px+ (xl)
- [ ] All breakpoints tested

### 9.2 Layout Responsive Behavior
- [x] Sidebar: hidden on mobile, slide-in on toggle
- [x] Sidebar: fixed on desktop, collapsible
- [x] Mobile backdrop overlay when sidebar open
- [ ] Header: simplified on mobile (hamburger menu)
- [ ] Main content: full width on mobile
- [ ] Main content: padding adjusts per breakpoint
- [ ] Dashboard: cards stack vertically on mobile
- [ ] Dashboard: 2 columns on tablet, 4 on desktop
- [ ] Meetings: single column cards on mobile
- [ ] MeetingDetail: single column layout on mobile
- [ ] CalendarView: simplified month view on mobile
- [ ] CalendarView: swipe gesture for navigation (mobile)
- [ ] Analytics: charts stack vertically on mobile
- [ ] Analytics: charts resize responsively
- [ ] Operations: cards stack on mobile
- [ ] People: list view on mobile, grid on desktop
- [ ] TimeCards: simplified card view on mobile
- [ ] Settings: single column on mobile

### 9.3 Touch Interactions
- [ ] Touch-friendly button sizes (minimum 44px)
- [ ] Swipe to dismiss notifications (mobile)
- [ ] Pull to refresh (mobile)
- [ ] Touch-friendly dropdowns
- [ ] Touch-friendly date/time pickers
- [ ] No hover-only interactions (always touch alternative)

### 9.4 Mobile-Specific Features
- [ ] Mobile navigation: bottom tab bar (optional)
- [ ] Mobile: floating action button for create meeting
- [ ] Mobile: compact meeting cards
- [ ] Mobile: collapsible sections
- [ ] Mobile: gesture navigation between views

---

## 10. Internationalization

### 10.1 i18n Framework
- [ ] i18n library installed (react-i18next or similar)
- [ ] i18n provider wrapping app
- [ ] Default language: English (en)
- [ ] Language detection from browser
- [ ] Language persistence in localStorage
- [ ] Language selector in Settings

### 10.2 String Extraction
- [ ] All user-facing strings extracted to translation files
- [ ] Dashboard strings extracted
- [ ] Meetings strings extracted
- [ ] MeetingDetail strings extracted
- [ ] CreateMeeting strings extracted
- [ ] CalendarView strings extracted
- [ ] Analytics strings extracted
- [ ] Operations strings extracted
- [ ] Pulse strings extracted
- [ ] Notifications strings extracted
- [ ] Settings strings extracted
- [ ] ActionItems strings extracted
- [ ] Notes strings extracted
- [ ] People strings extracted
- [ ] TimeCards strings extracted
- [ ] Posture strings extracted
- [ ] Auth strings extracted
- [ ] Error messages extracted
- [ ] Toast messages extracted
- [ ] Empty state messages extracted
- [ ] Validation messages extracted

### 10.3 Date & Number Formatting
- [ ] Dates formatted with locale-aware formatter
- [ ] Times formatted with locale-aware formatter (12h/24h)
- [ ] Numbers formatted with locale-aware formatter
- [ ] Currency formatted with locale-aware formatter
- [ ] Relative time formatting ("2 hours ago")
- [ ] Calendar respects locale (first day of week)
- [ ] Duration formatting respects locale

### 10.4 RTL Support
- [ ] Layout supports RTL languages (dir="rtl")
- [ ] Sidebar position mirrors in RTL
- [ ] Icons that indicate direction mirror in RTL
- [ ] Text alignment adjusts for RTL
- [ ] Padding/margin adjusted for RTL (logical properties)

---

## 11. Security

### 11.1 Authentication
- [x] Gate OAuth PKCE flow implemented
- [x] Token stored in localStorage
- [ ] Token stored in httpOnly cookie (more secure alternative)
- [ ] Token refresh on near-expiry
- [ ] Auto-logout on token expiry
- [x] Session expiry listener
- [x] Redirect to login when unauthenticated
- [ ] CSRF protection
- [ ] Secure cookie flags (httpOnly, secure, sameSite)

### 11.2 Authorization
- [ ] Role-based access control (admin, organizer, member)
- [ ] Admin-only features gated
- [ ] Organizer-only meeting edit/delete gated
- [ ] Member permissions enforced on frontend
- [ ] Server-side authorization verified for all actions

### 11.3 Data Protection
- [ ] No sensitive data in URL parameters
- [ ] No sensitive data logged to console
- [ ] API responses filtered (no server internals exposed)
- [ ] Org isolation: X-Org-Id on all requests
- [ ] Workspace isolation: X-Workspace-Id on requests
- [ ] No cross-tenant data leakage

### 11.4 Input Validation
- [ ] All form inputs validated on client
- [ ] All form inputs validated on server
- [ ] XSS prevention: sanitize user input before rendering
- [ ] XSS prevention: rich text content sanitized (DOMPurify)
- [ ] SQL injection prevention (parameterized queries on backend)
- [ ] Meeting description: sanitized HTML rendering
- [ ] Note content: sanitized HTML rendering
- [ ] Comment content: sanitized HTML rendering

### 11.5 Network Security
- [ ] HTTPS enforced
- [ ] Content-Security-Policy header
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Strict-Transport-Security header
- [ ] Referrer-Policy header
- [ ] Permissions-Policy header

### 11.6 Dependency Security
- [ ] `npm audit` clean (no high/critical vulnerabilities)
- [ ] Dependabot or Renovate configured
- [ ] No known vulnerable dependencies
- [ ] Lock file committed
- [ ] Supply chain security: verified package integrity

---

## 12. Testing

### 12.1 Unit Tests
- [ ] Zustand store: auth actions
- [ ] Zustand store: meeting actions
- [ ] Zustand store: note actions
- [ ] Zustand store: agenda actions
- [ ] Zustand store: action item actions
- [ ] Zustand store: notification actions
- [ ] Zustand store: user actions
- [ ] Zustand store: UI actions
- [ ] Zustand store: persistence and rehydration
- [ ] Zustand store: derived state selectors
- [ ] Utils: cn() utility
- [ ] Utils: date formatting helpers
- [ ] Utils: meeting time label generation
- [ ] Utils: duration calculation
- [ ] Types: type validation tests

### 12.2 Component Tests
- [ ] Button component renders all variants
- [ ] Badge component renders all variants
- [ ] Avatar component renders with/without image
- [ ] AvatarGroup component renders overflow
- [ ] Sidebar component: expanded/collapsed states
- [ ] Sidebar component: navigation click
- [ ] Sidebar component: active item highlight
- [ ] Header component: renders user info
- [ ] Header component: search input
- [ ] Header component: notification badge
- [ ] Dashboard component: renders stats cards
- [ ] Dashboard component: renders upcoming meetings
- [ ] Dashboard component: empty state
- [ ] Meetings component: renders meeting list
- [ ] Meetings component: filter functionality
- [ ] Meetings component: sort functionality
- [ ] Meetings component: search functionality
- [ ] MeetingDetail component: renders meeting info
- [ ] MeetingDetail component: RSVP actions
- [ ] MeetingDetail component: agenda CRUD
- [ ] MeetingDetail component: notes CRUD
- [ ] MeetingDetail component: action items CRUD
- [ ] CreateMeeting component: form validation
- [ ] CreateMeeting component: form submission
- [ ] CalendarView component: renders calendar grid
- [ ] CalendarView component: view switching
- [ ] Analytics component: renders charts
- [ ] Operations component: renders service health
- [ ] Pulse component: renders KPIs
- [ ] Notifications component: renders list
- [ ] Notifications component: mark read
- [ ] Settings component: renders form
- [ ] Settings component: save settings
- [ ] ActionItems component: renders list
- [ ] ActionItems component: toggle completion
- [ ] Notes component: renders list
- [ ] Notes component: search
- [ ] People component: renders list
- [ ] TimeCards component: renders list
- [ ] Auth component: login form
- [ ] Auth component: register form

### 12.3 Integration Tests
- [ ] Login flow: email + password -> dashboard
- [ ] OAuth flow: redirect -> callback -> dashboard
- [ ] Meeting creation flow: form -> submit -> detail view
- [ ] Meeting RSVP flow: accept/decline -> update shown
- [ ] Agenda CRUD flow: add -> edit -> complete -> delete
- [ ] Notes CRUD flow: add -> edit -> pin -> delete
- [ ] Action items flow: add -> toggle -> delete
- [ ] Notification flow: receive -> read -> dismiss
- [ ] EventBus integration: receive SSE event -> toast shown
- [ ] Settings flow: update -> save -> persist on reload
- [ ] Time card flow: create -> submit -> approve
- [ ] Auth: token expiry -> redirect to login

### 12.4 End-to-End Tests
- [ ] E2E framework configured (Playwright or Cypress)
- [ ] E2E: complete login flow
- [ ] E2E: create meeting end-to-end
- [ ] E2E: navigate all 17 views
- [ ] E2E: dark mode toggle
- [ ] E2E: responsive layout at mobile breakpoint
- [ ] E2E: responsive layout at tablet breakpoint
- [ ] E2E: responsive layout at desktop breakpoint
- [ ] E2E: sidebar collapse/expand
- [ ] E2E: meeting detail CRUD operations
- [ ] E2E: notification interactions

### 12.5 Visual Regression Tests
- [ ] Visual regression tool configured (Chromatic, Percy, or Playwright screenshots)
- [ ] Dashboard: light mode screenshot
- [ ] Dashboard: dark mode screenshot
- [ ] Meetings: light mode screenshot
- [ ] Meetings: dark mode screenshot
- [ ] MeetingDetail: light mode screenshot
- [ ] MeetingDetail: dark mode screenshot
- [ ] Calendar: light mode screenshot
- [ ] Calendar: dark mode screenshot
- [ ] All views captured at mobile, tablet, desktop breakpoints

### 12.6 Test Coverage
- [ ] Unit test coverage > 80%
- [ ] Component test coverage > 70%
- [ ] Integration test coverage > 60%
- [ ] CI pipeline runs all tests on PR
- [ ] Test results reported in PR comments

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] All TypeScript interfaces documented with JSDoc
- [ ] All Zustand store actions documented with JSDoc
- [ ] All custom hooks documented with JSDoc
- [ ] All utility functions documented with JSDoc
- [ ] All components have prop documentation
- [ ] Complex business logic has inline comments
- [ ] API endpoints documented in comments

### 13.2 Developer Documentation
- [ ] README.md: project overview
- [ ] README.md: setup instructions
- [ ] README.md: development workflow
- [ ] README.md: environment variables
- [ ] README.md: folder structure
- [ ] README.md: available scripts
- [ ] CONTRIBUTING.md: coding standards
- [ ] CONTRIBUTING.md: PR process
- [ ] CHANGELOG.md: version history
- [ ] Architecture decision records (ADRs) for key decisions

### 13.3 API Documentation
- [ ] All API endpoints documented (method, URL, params, response)
- [ ] API error codes documented
- [ ] API authentication documented
- [ ] API rate limits documented
- [ ] Postman/Insomnia collection exported

### 13.4 User Documentation
- [ ] Feature guide: meetings management
- [ ] Feature guide: calendar usage
- [ ] Feature guide: analytics interpretation
- [ ] Feature guide: operations monitoring
- [ ] Feature guide: time cards
- [ ] Keyboard shortcuts reference
- [ ] FAQ document

---

## 14. Deployment & CI/CD

### 14.1 Build Configuration
- [ ] Production build succeeds (`vite build`)
- [ ] Build output optimized (minified, tree-shaken)
- [ ] Source maps generated (for error tracking)
- [ ] Environment variables validated at build time
- [ ] Build hash in filenames for cache busting
- [ ] Asset size limits configured (warn if bundle too large)

### 14.2 Docker
- [ ] Dockerfile created (multi-stage build)
- [ ] Dockerfile: Node build stage
- [ ] Dockerfile: Nginx serve stage
- [ ] Dockerfile: health check configured
- [ ] Docker compose entry for Control Center
- [ ] Docker compose: port mapping (45009)
- [ ] Docker compose: volume mounts for development
- [ ] Docker compose: environment variable passthrough
- [ ] `.dockerignore` configured

### 14.3 CI Pipeline
- [ ] GitHub Actions / CI workflow configured
- [ ] CI: install dependencies
- [ ] CI: lint check
- [ ] CI: type check (`tsc --noEmit`)
- [ ] CI: unit tests
- [ ] CI: build
- [ ] CI: E2E tests (optional, on main branch)
- [ ] CI: security audit
- [ ] CI: bundle size check
- [ ] CI: deploy preview on PR

### 14.4 Deployment
- [ ] Staging environment configured
- [ ] Production environment configured
- [ ] Deployment script / pipeline
- [ ] Rollback procedure documented
- [ ] Zero-downtime deployment
- [ ] Health check endpoint
- [ ] Error monitoring (Sentry or similar)
- [ ] Performance monitoring (Web Vitals)
- [ ] Log aggregation configured

### 14.5 Environment Management
- [ ] `.env.example` with all required variables
- [ ] `.env.development` for local development
- [ ] `.env.production` for production build
- [ ] Environment variables: `VITE_API_BASE`
- [ ] Environment variables: `VITE_EVENTBUS_URL`
- [ ] Environment variables: `VITE_GATE_URL`
- [ ] Environment variables: `VITE_GATE_CLIENT_ID`
- [ ] Secrets not committed to git
- [ ] `.gitignore` includes `.env*` (except `.env.example`)

---

## 15. Backend

### 15.1 Backend API Server
- [ ] Backend framework chosen (FastAPI / Express)
- [ ] Backend running on designated port
- [ ] CORS configured for frontend origin
- [ ] Request logging middleware
- [ ] Error handling middleware
- [ ] Health check endpoint (`GET /health`)
- [ ] API versioning (`/api/v1/`)

### 15.2 Database
- [ ] Database chosen (PostgreSQL recommended)
- [ ] ORM/query builder configured (Prisma / SQLAlchemy)
- [ ] Database migrations setup
- [ ] Initial migration: users table
- [ ] Initial migration: meetings table
- [ ] Initial migration: participants table
- [ ] Initial migration: agenda_items table
- [ ] Initial migration: notes table
- [ ] Initial migration: action_items table
- [ ] Initial migration: notifications table
- [ ] Initial migration: time_cards table
- [ ] Seed data script
- [ ] Database indexes on frequently queried columns
- [ ] Database connection pooling

### 15.3 Backend Auth
- [ ] Gate token validation middleware
- [ ] JWT verification
- [ ] Token introspection endpoint integration
- [ ] Org isolation middleware (X-Org-Id)
- [ ] Role-based authorization middleware
- [ ] Rate limiting middleware

### 15.4 Backend API Endpoints
- [ ] Meetings CRUD endpoints
- [ ] Participants CRUD endpoints
- [ ] Agenda items CRUD endpoints
- [ ] Notes CRUD endpoints
- [ ] Action items CRUD endpoints
- [ ] Notifications CRUD endpoints
- [ ] Users CRUD endpoints
- [ ] Time cards CRUD endpoints
- [ ] Operations/health endpoints
- [ ] Analytics aggregate endpoints
- [ ] Search endpoints (full-text)
- [ ] Export endpoints (CSV/PDF)

### 15.5 Backend EventBus Integration
- [ ] Publish events on meeting created/updated/cancelled
- [ ] Publish events on action item created/completed
- [ ] Consume events from other Orbit apps
- [ ] Event schema validation
- [ ] Dead letter queue for failed event processing
- [ ] Event replay capability

### 15.6 Backend Testing
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Database tests with test fixtures
- [ ] Test coverage > 80%
- [ ] CI runs backend tests

---

## Summary

| Section | Total Items | Done | Remaining |
|---------|------------|------|-----------|
| 1. Project Setup | 48 | 22 | 26 |
| 2. Design System | 198 | 6 | 192 |
| 3. Dark Mode | 166 | 0 | 166 |
| 4. Core Features | 288 | 0 | 288 |
| 5. API Integration | 68 | 23 | 45 |
| 6. State Management | 52 | 26 | 26 |
| 7. Performance | 39 | 0 | 39 |
| 8. Accessibility | 54 | 0 | 54 |
| 9. Mobile & Responsive | 32 | 3 | 29 |
| 10. Internationalization | 30 | 0 | 30 |
| 11. Security | 28 | 5 | 23 |
| 12. Testing | 76 | 0 | 76 |
| 13. Documentation | 22 | 0 | 22 |
| 14. Deployment & CI/CD | 33 | 0 | 33 |
| 15. Backend | 37 | 0 | 37 |
| **TOTAL** | **1171** | **85** | **1086** |
