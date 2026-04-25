# Mail -- Enterprise Email Client — Comprehensive Checklist
> Last updated: 2026-04-06
> Legend: [x] = done · [ ] = todo · [~] = in progress

> Mail is RM Orbit's Enterprise Email client (comparable to Gmail/Outlook/ProtonMail).
> Stack: React 18.3.1 · Vite 5.4.8 · React Router v6 · Tailwind v3 · Axios · React Quill · Framer Motion
> Routes: 7 (inbox, sent, drafts, trash, search, settings, admin)
> Backend: Python FastAPI · PostgreSQL · Rspamd · Postfix/Dovecot
> Status: ~65% feature complete

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration](#2-design-system-integration)
3. [Dark Mode — Per-View Audit](#3-dark-mode--per-view-audit)
4. [Core Features — Inbox](#4-core-features--inbox)
5. [Core Features — Thread View](#5-core-features--thread-view)
6. [Core Features — Compose](#6-core-features--compose)
7. [Core Features — Floating Composer](#7-core-features--floating-composer)
8. [Core Features — Folders (Inbox/Sent/Drafts/Trash)](#8-core-features--folders)
9. [Core Features — Labels & Organization](#9-core-features--labels--organization)
10. [Core Features — Search](#10-core-features--search)
11. [Core Features — Settings](#11-core-features--settings)
12. [Core Features — Admin](#12-core-features--admin)
13. [Core Features — Keyboard Shortcuts](#13-core-features--keyboard-shortcuts)
14. [Core Features — Attachments](#14-core-features--attachments)
15. [Core Features — Email Signatures](#15-core-features--email-signatures)
16. [Core Features — Filters & Rules](#16-core-features--filters--rules)
17. [Core Features — Multi-Account](#17-core-features--multi-account)
18. [Core Features — Email Security](#18-core-features--email-security)
19. [Core Features — AI Features](#19-core-features--ai-features)
20. [Core Features — Integrations](#20-core-features--integrations)
21. [Core Features — Auth & PKCE](#21-core-features--auth--pkce)
22. [Core Features — Notifications](#22-core-features--notifications)
23. [Core Features — Offline Support](#23-core-features--offline-support)
24. [Layout & Navigation (AppLayout)](#24-layout--navigation-applayout)
25. [API Integration](#25-api-integration)
26. [State Management](#26-state-management)
27. [Performance](#27-performance)
28. [Accessibility](#28-accessibility)
29. [Mobile & Responsive](#29-mobile--responsive)
30. [Internationalization (i18n)](#30-internationalization-i18n)
31. [Security](#31-security)
32. [Testing](#32-testing)
33. [Documentation](#33-documentation)
34. [Deployment & CI/CD](#34-deployment--cicd)
35. [Backend — API Endpoints](#35-backend--api-endpoints)
36. [Backend — Database Schema](#36-backend--database-schema)
37. [Backend — Email Delivery](#37-backend--email-delivery)
38. [Backend — Email Reception](#38-backend--email-reception)
39. [Backend — Spam & Security](#39-backend--spam--security)
40. [Backend — Search Service](#40-backend--search-service)
41. [Backend — Admin Service](#41-backend--admin-service)
42. [Backend — SSO / Auth Service](#42-backend--sso--auth-service)
43. [Backend — EventBus Integration](#43-backend--eventbus-integration)
44. [Backend — Background Workers](#44-backend--background-workers)
45. [Backend — Infrastructure](#45-backend--infrastructure)

---

## 1. Project Setup & Configuration

### 1.1 Package & Dependencies
- [x] `package.json` with all required dependencies
- [x] React 18.3.1 installed
- [x] React Router v6 installed
- [x] Tailwind CSS v3 installed
- [x] Axios installed for API calls
- [x] React Quill installed for rich text compose
- [x] Framer Motion installed for animations
- [x] Lucide React installed for icons
- [ ] Dependency audit: remove unused packages
- [ ] Pin all dependency versions (no `^` ranges)
- [ ] Verify no duplicate dependencies in lock file
- [ ] Add missing TypeScript type packages (@types/*)

### 1.2 Vite Configuration
- [x] Vite 5.4.8 configured
- [x] React plugin configured
- [x] Dev server running on port 45004
- [ ] Production build optimized (minify, tree-shake)
- [ ] Source maps disabled in production
- [ ] `.env.development` with local API URLs
- [ ] `.env.production` with production API URLs
- [ ] `.env.example` committed with variable names
- [ ] Chunk splitting strategy (vendor, app, per-route)
- [ ] Asset fingerprinting for cache busting

### 1.3 TypeScript Configuration
- [x] TypeScript configured (TSX files used)
- [ ] Strict mode enabled in tsconfig.json
- [ ] Path aliases configured (`@/` prefix)
- [ ] No `any` types in codebase (audit and fix)
- [ ] Type declarations for all API responses
- [ ] Type declarations for all component props

### 1.4 Linting & Formatting
- [ ] ESLint configured with recommended rules
- [ ] React-specific ESLint rules (hooks, jsx-a11y)
- [ ] Prettier configured
- [ ] Format-on-save configured
- [ ] Pre-commit hook runs lint + format
- [ ] No lint errors in codebase

### 1.5 Docker Setup
- [ ] Dockerfile for Mail frontend
- [ ] Docker Compose service for frontend
- [ ] Multi-stage build (build + Nginx serve)
- [ ] Health check endpoint
- [ ] Environment variable injection at build time

### 1.6 Project Structure
- [x] `src/api/client.ts` — Axios instance with auth
- [x] `src/api/pkce.ts` — PKCE helper functions
- [x] `src/components/` — shared components
- [x] `src/context/ComposeContext.tsx` — compose state management
- [x] `src/layouts/AppLayout.tsx` — main app layout
- [x] `src/pages/LoginPage.tsx` — login page
- [x] `src/pages/PageFactory.tsx` — main page component (renders all views)
- [x] `src/styles.css` — global styles
- [x] `src/utils/` — utility functions
- [ ] Refactor PageFactory.tsx into separate page components (currently monolithic)
- [ ] Extract inline components from PageFactory into dedicated files
- [ ] Create proper page components: InboxPage, SentPage, DraftsPage, TrashPage, SearchPage, SettingsPage, AdminPage

---

## 2. Design System Integration

### 2.1 Token Integration
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [x] `styles.css` imports `orbit-tokens.css` (`@import "/orbit-ui/orbit-tokens.css"`)
- [ ] Anti-FOUC script (`orbit-theme-init.js`) in `index.html`
- [ ] Verify `orbit-bar.js` loaded in `index.html`
- [ ] Verify `orbit-ui.css` loaded in `index.html`

### 2.2 Semantic Token Migration
- [ ] Replace all hardcoded colors in AppLayout.tsx
  - [ ] `bg-slate-50` -> `bg-surface-base` (main background)
  - [ ] `text-slate-900` -> `text-content-primary` (main text)
  - [ ] `border-slate-200` -> `border-border-default` (borders)
  - [ ] `bg-blue-600` -> `bg-primary-600` (primary buttons)
  - [ ] `text-slate-400` -> `text-content-muted` (secondary text)
  - [ ] `bg-slate-100` -> `bg-surface-subtle` (hover states)
  - [ ] `text-slate-500` -> `text-content-secondary`
  - [ ] `text-slate-600` -> `text-content-secondary`
  - [ ] `bg-slate-200` -> `bg-surface-muted` (progress bar bg)
  - [ ] `bg-red-500` -> `bg-danger-500` (offline banner)
  - [ ] `bg-amber-500` -> `bg-warning-500` (storage warning)
  - [ ] `shadow-blue-500/20` -> `shadow-primary-500/20`
  - [ ] `shadow-blue-600/20` -> `shadow-primary-600/20`
  - [ ] `from-blue-600 to-indigo-700` -> brand gradient token
- [ ] Replace all hardcoded colors in PageFactory.tsx
  - [ ] Mail list item backgrounds
  - [ ] Mail list item hover states
  - [ ] Mail list item selected state
  - [ ] Thread view backgrounds
  - [ ] Compose panel colors
  - [ ] Date/timestamp colors
  - [ ] Sender name colors
  - [ ] Subject line colors
  - [ ] Preview text colors
  - [ ] Unread indicator colors
  - [ ] Star/flag colors
  - [ ] Attachment indicator colors
  - [ ] Action button colors
  - [ ] Loading spinner colors
  - [ ] Empty state colors
  - [ ] Error state colors
- [ ] Replace all hardcoded colors in LoginPage.tsx
  - [ ] `bg-slate-50` -> `bg-surface-base`
  - [ ] `border-blue-600` -> `border-primary-600`
  - [ ] `text-blue-600` -> `text-primary-600`
  - [ ] `border-slate-200` -> `border-border-default`
  - [ ] `bg-blue-600` -> `bg-primary-600`
  - [ ] Spinner blue colors
- [ ] Replace all hardcoded colors in FloatingComposer.tsx
  - [ ] Composer background
  - [ ] Toolbar colors
  - [ ] Input field colors
  - [ ] Button colors
  - [ ] Border colors
- [ ] Replace all hardcoded colors in AppLauncher.tsx
  - [ ] Panel background
  - [ ] App icon colors
  - [ ] Hover states
- [ ] Verify no remaining `slate-`, `gray-`, `blue-` hardcoded classes

### 2.3 Component Replacement -- @orbit-ui/react
- [ ] Replace custom `Spinner` (inline div + animate-spin) with `<Spinner>`
  - [ ] AppLayout loading state spinner
  - [ ] LoginPage loading state spinner
  - [ ] PageFactory folder loading spinner
  - [ ] Mail thread loading spinner
  - [ ] Search loading spinner
  - [ ] Compose send loading spinner
  - [ ] OAuth callback loading spinner
- [ ] Replace custom toast notifications with `useToast`
  - [ ] Add `<ToastProvider>` to app root
  - [ ] Replace all success notifications (send, save, delete)
  - [ ] Replace all error notifications (API failures)
  - [ ] Replace all info notifications
- [ ] Replace custom `Avatar` for sender avatars with `<Avatar>`
  - [ ] Mail list sender avatar
  - [ ] Thread view message author avatar
  - [ ] Compose recipient chips avatar
  - [ ] Sidebar user avatar
- [ ] Adopt `<Badge>` for indicators
  - [ ] Unread count badge in sidebar
  - [ ] Attachment indicator badge
  - [ ] Label color badges
  - [ ] Spam/phishing warning badge
  - [ ] Priority badge (high importance)
  - [ ] Folder count badges
- [ ] Adopt `<EmptyState>` for empty views
  - [ ] Empty inbox ("No new emails")
  - [ ] Empty sent folder
  - [ ] Empty drafts folder
  - [ ] Empty trash folder
  - [ ] Empty search results ("No emails match your search")
  - [ ] Empty label/folder view
- [ ] Adopt `<Skeleton>` for loading states
  - [ ] Mail list loading skeleton (rows of email previews)
  - [ ] Thread view loading skeleton
  - [ ] Sidebar loading skeleton
  - [ ] Settings page loading skeleton
  - [ ] Admin page loading skeleton
- [ ] Replace hardcoded button classes with `<Button>`
  - [ ] Compose button (primary, prominent)
  - [ ] Reply button
  - [ ] Reply All button
  - [ ] Forward button
  - [ ] Send button
  - [ ] Save Draft button
  - [ ] Discard button
  - [ ] Delete button
  - [ ] Archive button
  - [ ] Mark read/unread button
  - [ ] Star/flag button
  - [ ] Search submit button
  - [ ] Settings save button
  - [ ] Admin action buttons
  - [ ] SSO login button
  - [ ] Bulk action buttons (select all, delete selected, etc.)
  - [ ] Mobile sidebar toggle button
  - [ ] Mobile search button
  - [ ] Notification bell button
- [ ] Replace custom focus styles with `focus-ring` utility
- [ ] Adopt `<Dropdown>` for email action menus
  - [ ] Reply/Reply All/Forward dropdown
  - [ ] More actions dropdown (move to, label, report spam)
  - [ ] Sort by dropdown
  - [ ] Filter by dropdown
- [ ] Adopt `<Modal>` for dialogs
  - [ ] Delete confirmation modal
  - [ ] Discard draft confirmation modal
  - [ ] Block sender confirmation modal
  - [ ] Create filter modal
  - [ ] Create label/folder modal
  - [ ] Account settings modal
- [ ] Adopt `<Tooltip>` for icon button labels
  - [ ] Reply tooltip
  - [ ] Forward tooltip
  - [ ] Delete tooltip
  - [ ] Archive tooltip
  - [ ] Star tooltip
  - [ ] More actions tooltip
  - [ ] Compose tooltip
- [ ] Adopt `<Tabs>` for tabbed sections
  - [ ] Settings tabs (General, Signatures, Filters, Labels, Shortcuts)
  - [ ] Admin tabs (Users, Domains, Routing, Quotas, Audit Log)
- [ ] Adopt `<Input>` for form fields
  - [ ] Search input
  - [ ] Settings form inputs
  - [ ] Admin form inputs
  - [ ] Filter rule inputs
- [ ] Adopt `<Select>` for dropdowns
  - [ ] Folder selector (move to folder)
  - [ ] Label selector
  - [ ] Settings dropdowns
  - [ ] Admin dropdowns
- [ ] Adopt `<Switch>` for toggles
  - [ ] Settings toggles (notifications, read receipts, etc.)
  - [ ] Admin feature toggles
- [ ] Adopt `<Alert>` for inline messages
  - [ ] Offline warning banner
  - [ ] Storage quota warning
  - [ ] Spam warning on suspicious emails
  - [ ] Phishing detection alert
  - [ ] External image blocked notice
- [ ] Adopt `<Progress>` for progress indicators
  - [ ] Storage usage progress bar
  - [ ] Attachment upload progress
  - [ ] Import progress
- [ ] Adopt `<Table>` for data tables
  - [ ] Admin user list table
  - [ ] Admin audit log table
  - [ ] Filter rules list table
  - [ ] Keyboard shortcuts reference table
- [ ] Adopt `<Sidebar>` component
  - [ ] Replace custom sidebar in AppLayout.tsx
  - [ ] Sidebar with folder navigation
  - [ ] Sidebar collapse on mobile
  - [ ] Sidebar badge counts per folder
- [ ] Adopt `<Card>` for content sections
  - [ ] Settings section cards
  - [ ] Admin dashboard cards
  - [ ] Storage info card
- [ ] Adopt `<Divider>` for section separators
  - [ ] Sidebar section dividers
  - [ ] Settings section dividers
  - [ ] Thread message separators
- [ ] Adopt `<Tag>` / `<TagInput>` for labels
  - [ ] Email label tags
  - [ ] Recipient chip tags (To, CC, BCC)
  - [ ] Filter condition tags
- [ ] Adopt `<Checkbox>` for selection
  - [ ] Bulk email selection checkboxes
  - [ ] Select all checkbox
  - [ ] Settings checkbox options
- [ ] Adopt `<Accordion>` for collapsible sections
  - [ ] Thread message collapse/expand
  - [ ] Settings expandable sections
  - [ ] Advanced search filters accordion
- [ ] Adopt `<Pagination>` for email lists
  - [ ] Inbox pagination (or infinite scroll)
  - [ ] Search results pagination
  - [ ] Admin list pagination
- [ ] Adopt `<Breadcrumb>` for navigation context
  - [ ] Folder > Thread navigation
  - [ ] Settings > Section navigation
  - [ ] Admin > Section navigation
- [ ] Adopt `<FileUpload>` for attachments
  - [ ] Compose: attachment upload zone
  - [ ] Settings: signature image upload
  - [ ] Admin: import/export

---

## 3. Dark Mode -- Per-View Audit

### 3.1 AppLayout
- [ ] Sidebar background (`bg-surface-base` in dark)
- [ ] Sidebar border (`border-border-default` in dark)
- [ ] Sidebar nav item default state
- [ ] Sidebar nav item hover state
- [ ] Sidebar nav item active state (currently `bg-blue-600`)
- [ ] Sidebar keyboard shortcut badges
- [ ] Sidebar storage utilization section
- [ ] Sidebar storage progress bar
- [ ] Header background
- [ ] Header border
- [ ] Header title text
- [ ] Header search input
- [ ] Header search input focus state
- [ ] Header buttons (AppLauncher, Notification, Compose)
- [ ] Compose button gradient
- [ ] Mobile sidebar backdrop overlay
- [ ] Mobile sidebar close button
- [ ] Offline banner

### 3.2 Inbox / Mail List
- [ ] Mail list container background
- [ ] Mail list item default state
- [ ] Mail list item hover state
- [ ] Mail list item selected/active state
- [ ] Mail list item unread state (bolder text)
- [ ] Mail list item read state
- [ ] Sender name text color
- [ ] Subject text color
- [ ] Preview text color
- [ ] Date/time text color
- [ ] Star/flag icon color (starred vs unstarred)
- [ ] Attachment indicator icon
- [ ] Unread dot indicator
- [ ] Bulk select checkbox
- [ ] "Select all" bar
- [ ] Empty inbox state
- [ ] Loading skeleton state
- [ ] Error state
- [ ] Thread count badge
- [ ] Label color badges on list items
- [ ] Divider between mail items

### 3.3 Thread View (Email Content)
- [ ] Thread container background
- [ ] Message header (from, to, date)
- [ ] Message sender name text
- [ ] Message sender email text
- [ ] Message timestamp text
- [ ] Message action buttons (reply, forward, more)
- [ ] Message body container
- [ ] Message body text
- [ ] Quoted/forwarded text styling
- [ ] Thread separator between messages
- [ ] Expand/collapse thread toggle
- [ ] Collapsed message preview
- [ ] Attachment list section
- [ ] Attachment card (icon, name, size, download)
- [ ] Reply input area at bottom
- [ ] "Email content" iframe/container
  - [ ] Inject `color-scheme: dark` for HTML emails in dark mode
  - [ ] Handle emails with hardcoded light backgrounds
  - [ ] Option to "View original" (bypass dark injection)
- [ ] External images blocked notice
- [ ] "Load images" button
- [ ] Phishing/spam warning banner
- [ ] AI summary section
- [ ] "Create task in Atlas" button
- [ ] "Create ticket in TurboTick" button
- [ ] Mobile thread bottom sheet

### 3.4 Compose Panel
- [ ] Compose container background
- [ ] Compose header (minimize, maximize, close buttons)
- [ ] To/CC/BCC recipient input fields
- [ ] Recipient chip styling
- [ ] Recipient chip remove button
- [ ] Recipient autocomplete dropdown
- [ ] Subject input field
- [ ] Subject input placeholder
- [ ] Rich text editor (React Quill) container
- [ ] React Quill toolbar background
- [ ] React Quill toolbar button states
- [ ] React Quill editor body background
- [ ] React Quill editor text color
- [ ] React Quill link color
- [ ] Attachment preview area
- [ ] Attachment chip styling
- [ ] Send button
- [ ] Save Draft button
- [ ] Discard button
- [ ] Format options (bold, italic, link, etc.)
- [ ] Emoji picker
- [ ] Signature block styling

### 3.5 Search Page
- [ ] Search input field
- [ ] Search filters (from, to, date, has attachment)
- [ ] Search results list (same as mail list)
- [ ] Search result highlighting (matched text)
- [ ] "No results" empty state
- [ ] Recent searches list
- [ ] Search suggestions dropdown
- [ ] Advanced search panel
- [ ] Clear search button

### 3.6 Settings Page
- [ ] Settings container background
- [ ] Settings section cards
- [ ] Settings section headers
- [ ] Form labels
- [ ] Form inputs (text, select, textarea)
- [ ] Toggle switches
- [ ] Radio buttons
- [ ] Save/cancel buttons
- [ ] Signature editor
- [ ] Vacation responder form
- [ ] Notification preferences section
- [ ] Keyboard shortcuts table

### 3.7 Admin Page
- [ ] Admin container background
- [ ] Admin navigation tabs
- [ ] User management table
  - [ ] Table header
  - [ ] Table rows
  - [ ] Action buttons per row
  - [ ] User status badges
- [ ] Domain management section
- [ ] Email routing rules section
- [ ] Quota management section
- [ ] Audit log table
  - [ ] Log entry rows
  - [ ] Timestamp column
  - [ ] Action column
  - [ ] User column

### 3.8 Login Page
- [ ] Login container background
- [ ] Logo/brand area
- [ ] SSO button
- [ ] Loading state
- [ ] Error message
- [ ] OAuth callback loading state

### 3.9 Cross-Cutting Dark Mode
- [ ] React Quill custom dark theme CSS
  - [ ] `.ql-toolbar` background and borders
  - [ ] `.ql-toolbar .ql-stroke` icon colors
  - [ ] `.ql-toolbar .ql-fill` icon colors
  - [ ] `.ql-toolbar .ql-picker` text color
  - [ ] `.ql-toolbar .ql-picker-options` dropdown bg
  - [ ] `.ql-editor` background and text
  - [ ] `.ql-editor.ql-blank::before` placeholder color
- [ ] Scrollbar styling in dark mode (all scrollable areas)
- [ ] Selection highlight color (::selection) in dark mode
- [ ] Link colors in email content dark mode
- [ ] Framer Motion animation colors in dark mode
- [ ] Context menu/dropdown background in dark mode
- [ ] Tooltip background in dark mode
- [ ] Toast notification colors in dark mode
- [ ] Verify color contrast ratios (WCAG AA 4.5:1) in dark mode
- [ ] Test theme toggle transition (no flash)
- [ ] Test glassmorphism effects in dark mode

---

## 4. Core Features -- Inbox

### 4.1 Thread List
- [x] Fetch email list from API (`/mail/inbox`)
- [x] Display list of email threads
- [x] Thread item: sender name
- [x] Thread item: subject line
- [x] Thread item: preview text
- [x] Thread item: date/time
- [ ] Thread item: sender avatar
- [ ] Thread item: unread indicator (bold text + dot)
- [ ] Thread item: read state (lighter text)
- [ ] Thread item: star/flag toggle
- [ ] Thread item: attachment indicator (paperclip icon)
- [ ] Thread item: label/tag badges
- [ ] Thread item: thread count (number of messages in thread)
- [ ] Thread item: importance/priority indicator
- [ ] Thread item: checkbox for bulk selection

### 4.2 Thread List Interaction
- [x] Click thread -> show thread detail in right panel
- [x] Active thread highlighted in list
- [ ] Mark as read on click/open (API call)
- [ ] Mark as unread (right-click or action button)
- [ ] Star/flag email (toggle)
- [ ] Unstar/unflag email
- [ ] Archive email (move to archive)
- [ ] Delete email (move to trash)
- [ ] Move to folder (dropdown)
- [ ] Apply label (dropdown)
- [ ] Report as spam
- [ ] Block sender
- [ ] Snooze (reappear at specified time)
- [ ] Right-click context menu with all actions

### 4.3 Bulk Actions
- [ ] Checkbox on each thread item
- [ ] "Select all" checkbox in header
- [ ] "Select all conversations in [folder]" link
- [ ] Bulk action bar appears when items selected:
  - [ ] Mark as read
  - [ ] Mark as unread
  - [ ] Star
  - [ ] Unstar
  - [ ] Archive
  - [ ] Delete (move to trash)
  - [ ] Move to folder
  - [ ] Apply label
  - [ ] Mark as spam
- [ ] Deselect all button
- [ ] Selected count display ("3 selected")

### 4.4 Pagination / Virtual Scroll
- [ ] Paginated thread list (load 20-50 at a time)
- [ ] "Load more" button or infinite scroll
- [ ] Virtual scroll for performance (handle 10,000+ threads)
- [ ] Page number indicator ("1-50 of 1,234")
- [ ] Previous/next page buttons
- [ ] Jump to page

### 4.5 Unread Count
- [ ] Unread count badge on Inbox in sidebar
- [ ] Unread count in browser tab title ("(5) RM Mail")
- [ ] Unread count updates in real-time (SSE/WebSocket)
- [ ] Unread count on other folders (Drafts count, Trash count)

### 4.6 Sorting
- [ ] Sort by date (newest first — default)
- [ ] Sort by date (oldest first)
- [ ] Sort by sender name
- [ ] Sort by subject
- [ ] Sort by unread first
- [ ] Sort by starred first
- [ ] Sort preference persisted

### 4.7 Filtering
- [ ] Filter by unread only
- [ ] Filter by starred only
- [ ] Filter by has attachment
- [ ] Filter by label
- [ ] Filter by sender
- [ ] Filter by date range
- [ ] Clear all filters
- [ ] Active filter indicator

---

## 5. Core Features -- Thread View

### 5.1 Thread Display
- [ ] Full conversation threading (email chain)
- [ ] Messages displayed chronologically (oldest first)
- [ ] Each message shows:
  - [ ] Sender name and email
  - [ ] Sender avatar
  - [ ] Date/time (absolute + relative)
  - [ ] To/CC recipients (collapsible if many)
  - [ ] Message body (HTML rendered safely)
  - [ ] Attachments list
- [ ] Thread subject as header
- [ ] Thread label badges
- [ ] Thread action buttons (reply, reply all, forward, delete, more)

### 5.2 Thread Navigation
- [ ] Expand/collapse individual messages in thread
- [ ] Collapsed message shows: sender, date, preview (first line)
- [ ] "Expand all" / "Collapse all" toggle
- [ ] Scroll to latest message on open
- [ ] Scroll to first unread message in thread

### 5.3 Email Content Rendering
- [ ] HTML email rendered safely (sanitized)
- [ ] Plain text email rendered with line breaks preserved
- [ ] External images blocked by default
  - [ ] "Images hidden" banner with "Show images" button
  - [ ] "Always show images from this sender" option
- [ ] External links: warning before navigating ("You are leaving RM Mail")
- [ ] Quoted text collapsed ("Show quoted text" toggle)
- [ ] Forwarded content styled differently
- [ ] Inline images displayed
- [ ] Embedded images (CID references) resolved and displayed
- [ ] Email signature detection (collapse signatures)
- [ ] Code blocks rendered with monospace font
- [ ] Table rendering (responsive, scrollable if wide)

### 5.4 Thread Actions
- [ ] Reply (opens compose with To: sender)
- [ ] Reply All (opens compose with To: sender, CC: all recipients)
- [ ] Forward (opens compose with body quoted, To: empty)
- [ ] Delete thread (move all messages to trash)
- [ ] Archive thread
- [ ] Mark thread as unread
- [ ] Star/flag thread
- [ ] Move to folder
- [ ] Apply label
- [ ] Print email
- [ ] Download email as .eml
- [ ] Report as spam
- [ ] Block sender
- [ ] Mute thread (no more notifications)
- [ ] Snooze thread

### 5.5 AI Features in Thread
- [x] AI summarize thread (calls API for summary)
- [x] Summary display area
- [x] Summarizing loading state
- [ ] AI-suggested reply drafts
- [ ] AI action item extraction ("You need to respond by Friday")
- [ ] AI sender sentiment analysis
- [ ] AI thread priority suggestion
- [ ] Create Atlas task from thread (cross-app link)
- [ ] Create TurboTick ticket from thread (cross-app link)

### 5.6 Mobile Thread View
- [x] Touch handlers for thread interaction (handleThreadTouchStart/Move/End)
- [x] Long-press to open thread action sheet on mobile
- [x] Mobile thread bottom sheet component
- [ ] Swipe right to archive
- [ ] Swipe left to delete
- [ ] Pull-to-refresh
- [ ] Bottom sheet for thread actions (reply, forward, etc.)

---

## 6. Core Features -- Compose

### 6.1 Compose Form
- [ ] To field (email recipient input)
  - [ ] Autocomplete from contacts/address book
  - [ ] Multiple recipients (chips/tags)
  - [ ] Validate email format
  - [ ] Remove recipient (X button on chip)
  - [ ] Paste multiple emails (comma-separated)
- [ ] CC field
  - [ ] Hidden by default, "CC" button shows it
  - [ ] Same features as To field
- [ ] BCC field
  - [ ] Hidden by default, "BCC" button shows it
  - [ ] Same features as To field
- [ ] Subject line input
  - [ ] Auto-prepend "Re:" for replies
  - [ ] Auto-prepend "Fwd:" for forwards
  - [ ] Empty subject warning on send
- [ ] Body (Rich Text Editor — React Quill)
  - [ ] Bold
  - [ ] Italic
  - [ ] Underline
  - [ ] Strikethrough
  - [ ] Font size selector
  - [ ] Font color selector
  - [ ] Background/highlight color
  - [ ] Bullet list
  - [ ] Numbered list
  - [ ] Indent / Outdent
  - [ ] Blockquote
  - [ ] Horizontal rule
  - [ ] Link insertion (URL + display text)
  - [ ] Image insertion (upload or URL)
  - [ ] Code block
  - [ ] Clean formatting (remove all)
  - [ ] Paste from Word/Google Docs (preserve formatting)
  - [ ] Paste plain text option
  - [ ] Emoji picker
  - [ ] Right-to-left text support
- [ ] Signature insertion
  - [ ] Auto-insert default signature
  - [ ] Signature selector (if multiple)
  - [ ] Signature separator line
- [ ] Quoted text (for replies/forwards)
  - [ ] Original message quoted below compose area
  - [ ] "On [date], [sender] wrote:" attribution line
  - [ ] Quoted text indented or styled

### 6.2 Compose Actions
- [ ] Send email (with loading state)
- [ ] Send with keyboard shortcut (Cmd+Enter / Ctrl+Enter)
- [ ] Undo send (configurable delay: 5s, 10s, 30s)
  - [ ] Toast with "Undo" button after send
  - [ ] Cancel send during delay window
- [ ] Schedule send (send later)
  - [ ] Date/time picker for scheduled send
  - [ ] "Send at [time]" button
  - [ ] View/edit/cancel scheduled sends
- [ ] Save as draft
  - [ ] Manual save button
  - [ ] Auto-save every 30 seconds
  - [ ] Auto-save on window blur/close
  - [ ] Draft indicator ("Saved at [time]")
- [ ] Discard draft
  - [ ] Confirmation dialog ("Discard this draft?")
  - [ ] Delete draft from server
- [ ] Attach files
  - [ ] Browse button
  - [ ] Drag-and-drop onto compose area
  - [ ] Multiple file attachment
  - [ ] Upload progress per file
  - [ ] Remove attachment before send
  - [ ] File size limit enforcement
  - [ ] Total attachment size limit
  - [ ] File type icons
  - [ ] Inline image toggle (attach vs inline)

### 6.3 Compose Modes
- [ ] New email (blank)
- [ ] Reply (pre-fill To, quote original)
- [ ] Reply All (pre-fill To + CC, quote original)
- [ ] Forward (quote original, empty To)
- [ ] Edit draft (load draft content)
- [ ] Compose from template
- [ ] Compose with prefilled data (from URL params or cross-app link)

---

## 7. Core Features -- Floating Composer

### 7.1 FloatingComposer.tsx
- [x] Floating composer component exists
- [ ] Floating composer UI (like Gmail — bottom-right panel)
- [ ] Minimize composer (collapse to title bar)
- [ ] Maximize composer (expand to full screen)
- [ ] Close composer (with draft save prompt if content exists)
- [ ] Multiple composers open simultaneously (stacked/tiled)
- [ ] Drag to reposition floating composer
- [ ] Resize floating composer
- [ ] Compose state managed via ComposeContext
- [ ] Open compose from:
  - [ ] Compose button in header/sidebar
  - [ ] Reply/Reply All/Forward buttons
  - [ ] Keyboard shortcut (C)
  - [ ] URL (mailto: links)
  - [ ] Cross-app integration (Atlas, TurboTick)
- [ ] Transition animations (slide up, slide down)
- [ ] Focus management (focus compose on open, return focus on close)

---

## 8. Core Features -- Folders

### 8.1 Inbox
- [x] Inbox route (`/inbox`)
- [x] Fetch inbox threads from API
- [ ] Inbox: unread count in sidebar badge
- [ ] Inbox: mark all as read
- [ ] Inbox: refresh button
- [ ] Primary/Social/Promotions/Updates tabs (category inbox)

### 8.2 Sent
- [x] Sent route (`/sent`)
- [ ] Sent: display all sent emails
- [ ] Sent: thread grouping (sent replies shown in thread context)
- [ ] Sent: delivery status indicator (sent, delivered, read)
- [ ] Sent: click to view sent email detail

### 8.3 Drafts
- [x] Drafts route (`/drafts`)
- [ ] Drafts: list all saved drafts
- [ ] Drafts: click to open in compose (edit draft)
- [ ] Drafts: delete draft
- [ ] Drafts: draft age display
- [ ] Drafts: auto-saved indicator

### 8.4 Trash
- [x] Trash route (`/trash`)
- [ ] Trash: list deleted emails
- [ ] Trash: restore email (move back to inbox/folder)
- [ ] Trash: permanent delete
- [ ] Trash: empty trash ("Delete all permanently")
- [ ] Trash: auto-purge after 30 days
- [ ] Trash: "Messages in Trash will be automatically deleted after 30 days" notice

### 8.5 Spam
- [ ] Spam route (`/spam`)
- [ ] Spam: list spam-flagged emails
- [ ] Spam: "Not spam" action (move to inbox)
- [ ] Spam: permanent delete
- [ ] Spam: empty spam folder
- [ ] Spam: auto-purge after 30 days
- [ ] Spam: spam count in sidebar

### 8.6 Archive
- [ ] Archive route (`/archive`)
- [ ] Archive: all archived emails
- [ ] Archive: move back to inbox
- [ ] Archive: search within archive

### 8.7 Custom Folders
- [ ] Create custom folder
  - [ ] Folder name input
  - [ ] Folder color selector
  - [ ] Parent folder selector (nested folders)
- [ ] Rename custom folder
- [ ] Delete custom folder (with "move emails to..." option)
- [ ] Drag email into custom folder (from list)
- [ ] Folder in sidebar navigation
- [ ] Folder email count badge

---

## 9. Core Features -- Labels & Organization

### 9.1 Labels
- [ ] Create label
  - [ ] Label name
  - [ ] Label color (predefined palette)
- [ ] Edit label (rename, change color)
- [ ] Delete label
- [ ] Apply label to email/thread
  - [ ] From thread action menu
  - [ ] From right-click context menu
  - [ ] From bulk action bar
  - [ ] Drag-and-drop to label in sidebar
- [ ] Remove label from email/thread
- [ ] Multiple labels per email
- [ ] Label filter view (click label in sidebar -> show labeled emails)
- [ ] Label badges on thread list items
- [ ] Nested labels (parent/child hierarchy)

### 9.2 Smart Labels
- [ ] Auto-categorize: Newsletters
- [ ] Auto-categorize: Receipts
- [ ] Auto-categorize: Social media notifications
- [ ] Auto-categorize: Promotions
- [ ] Auto-categorize: Updates/transactional
- [ ] Machine learning classification (over time)

---

## 10. Core Features -- Search

### 10.1 Search Page (route: `/search`)
- [x] Search route exists
- [x] Search input in header
- [x] Navigate to `/search?q=` on submit
- [ ] Full-text search across all emails (subject, body, sender, recipient)
- [ ] Search result list (same format as mail list)
- [ ] Search result highlighting (matched text in bold)
- [ ] Search result snippet (context around match)
- [ ] Search result count

### 10.2 Search Filters
- [ ] Filter: from (sender email/name)
- [ ] Filter: to (recipient)
- [ ] Filter: subject (keywords in subject)
- [ ] Filter: date range (after, before, between)
- [ ] Filter: has attachment
- [ ] Filter: has label
- [ ] Filter: in folder
- [ ] Filter: is unread
- [ ] Filter: is starred
- [ ] Filter: size (larger than, smaller than)
- [ ] Advanced search syntax: `from:user@example.com subject:invoice after:2026-01-01`
- [ ] Search suggestion chips (quick filters)

### 10.3 Search UX
- [ ] Recent searches history (last 10)
- [ ] Clear search history
- [ ] Search suggestions as you type
- [ ] "No results" empty state with suggestions
- [ ] Search loading state
- [ ] Search result pagination
- [ ] Save search as smart label/filter

---

## 11. Core Features -- Settings

### 11.1 Settings Page (route: `/settings`)
- [x] Settings route exists
- [ ] General settings
  - [ ] Display name
  - [ ] Default reply behavior (reply vs reply all)
  - [ ] Conversation view toggle (thread vs individual)
  - [ ] Messages per page (25, 50, 100)
  - [ ] Language/locale selector
  - [ ] Date format preference
  - [ ] Time format preference (12h/24h)

### 11.2 Email Signature
- [ ] Signature editor (rich text)
- [ ] Create multiple signatures
- [ ] Default signature per account
- [ ] Signature for new emails vs replies
- [ ] Preview signature
- [ ] Image insertion in signature (upload or URL)
- [ ] Delete signature

### 11.3 Vacation/Autoresponder
- [ ] Enable/disable vacation responder
- [ ] Start date / end date
- [ ] Subject line
- [ ] Message body (rich text)
- [ ] Only send to contacts / send to everyone
- [ ] Only send once per sender (configurable period)

### 11.4 Notification Preferences
- [ ] Desktop notification toggle
- [ ] Desktop notification permission request
- [ ] Sound notification toggle
- [ ] Email notification summary (daily digest)
- [ ] Notify for: all emails, important only, none

### 11.5 Keyboard Shortcuts
- [ ] Enable/disable keyboard shortcuts
- [ ] Keyboard shortcut reference table
- [ ] Custom shortcut mapping (stretch)

### 11.6 External Services
- [ ] Connected accounts display
- [ ] POP3/IMAP settings (for external access)
- [ ] Forwarding address configuration
- [ ] Import from other email providers

### 11.7 Privacy & Security Settings
- [ ] Read receipt toggle
- [ ] External image loading preference (always load, ask, never)
- [ ] Link tracking protection toggle
- [ ] Encryption preferences

---

## 12. Core Features -- Admin

### 12.1 Admin Page (route: `/admin`)
- [x] Admin route exists
- [ ] Admin access control (only org admins see this route)

### 12.2 User Management
- [ ] User list table
  - [ ] Username, email, role, status, storage used
  - [ ] Search users
  - [ ] Sort by columns
  - [ ] Pagination
- [ ] Create user account
  - [ ] Username, email, password, role
  - [ ] Storage quota assignment
  - [ ] Welcome email option
- [ ] Edit user
  - [ ] Change role
  - [ ] Reset password
  - [ ] Change storage quota
- [ ] Disable/enable user account
- [ ] Delete user account (with data handling options)
- [ ] Bulk user import (CSV)

### 12.3 Domain Management
- [ ] Domain list (managed domains)
- [ ] Add domain
  - [ ] Domain name input
  - [ ] DNS verification instructions (MX, SPF, DKIM, DMARC)
  - [ ] DNS verification status check
- [ ] Remove domain
- [ ] Domain aliases
- [ ] Default domain configuration

### 12.4 Email Routing Rules
- [ ] Inbound routing rules (where to deliver)
- [ ] Outbound routing rules (relay configuration)
- [ ] Catchall address configuration
- [ ] Distribution lists / group aliases
- [ ] Auto-forwarding rules

### 12.5 Quota Management
- [ ] Default storage quota per user
- [ ] Per-user quota override
- [ ] Attachment size limit
- [ ] Message size limit
- [ ] Sending rate limits (messages per hour)
- [ ] Storage usage dashboard (total, per-user breakdown)

### 12.6 Audit Log
- [ ] Admin action log (who did what, when)
- [ ] Login/logout events
- [ ] Setting changes
- [ ] User management events
- [ ] Domain changes
- [ ] Search/filter audit log
- [ ] Export audit log (CSV)
- [ ] Audit log retention period

### 12.7 Compliance
- [ ] Message retention policies (per org, per folder)
- [ ] Legal hold (prevent deletion of specific accounts/threads)
- [ ] Email export for eDiscovery
- [ ] Data loss prevention (DLP) rules
  - [ ] Detect sensitive content (SSN, credit card, etc.)
  - [ ] Block or warn on send
  - [ ] Quarantine flagged messages
- [ ] GDPR data export (user's full email archive)
- [ ] GDPR data deletion (right to erasure)

---

## 13. Core Features -- Keyboard Shortcuts

### 13.1 Existing Shortcuts
- [x] `I` — navigate to Inbox
- [x] `S` — navigate to Sent
- [x] `D` — navigate to Drafts
- [x] `T` — navigate to Trash
- [x] `/` — navigate to Search
- [x] `C` — open Compose

### 13.2 Missing Shortcuts
- [ ] `J` — next email in list
- [ ] `K` — previous email in list
- [ ] `Enter` or `O` — open selected email
- [ ] `Escape` — go back (close thread, close compose)
- [ ] `R` — reply (in thread view)
- [ ] `A` — reply all (in thread view)
- [ ] `F` — forward (in thread view)
- [ ] `E` — archive
- [ ] `#` or `Delete` — move to trash
- [ ] `!` — report as spam
- [ ] `.` — star/unstar
- [ ] `Shift+I` — mark as read
- [ ] `Shift+U` — mark as unread
- [ ] `X` — select/deselect email
- [ ] `Cmd+Enter` / `Ctrl+Enter` — send email (in compose)
- [ ] `Cmd+Shift+D` — discard draft (in compose)
- [ ] `?` — show keyboard shortcut help overlay

### 13.3 Shortcut System
- [ ] Shortcuts only active when not in text input
- [ ] Shortcut help overlay (modal or drawer)
- [ ] Shortcuts configurable in settings
- [ ] Shortcuts respect disabled state (in settings)

---

## 14. Core Features -- Attachments

### 14.1 Sending Attachments
- [ ] Attach file via browse button
- [ ] Attach file via drag-and-drop into compose
- [ ] Attach multiple files
- [ ] Per-file upload progress bar
- [ ] Remove attachment before send (X button)
- [ ] File type icon per attachment
- [ ] File size display
- [ ] Total attachment size display
- [ ] Size limit enforcement (client-side + server-side)
- [ ] Supported formats: all (with warnings for large/unusual)
- [ ] Inline image attachment (displayed in body)
- [ ] Attach from Orbit Files (cloud storage picker)

### 14.2 Receiving Attachments
- [ ] Attachment list in thread view
- [ ] Attachment card: icon, filename, size
- [ ] Image attachment: inline preview in email body
- [ ] Image attachment: click to view full size (lightbox)
- [ ] PDF attachment: preview in browser
- [ ] Office document preview (docx, xlsx, pptx) — link to Writer
- [ ] Audio/video attachment: play inline
- [ ] Download single attachment
- [ ] Download all attachments (zip)
- [ ] Save attachment to Orbit Files
- [ ] Virus scan status indicator (clean / suspicious / scanning)
- [ ] Attachment search (find emails with specific attachment name)

---

## 15. Core Features -- Email Signatures

- [ ] Signature editor (rich text: bold, italic, link, image)
- [ ] Create multiple signatures
- [ ] Set default signature for new emails
- [ ] Set default signature for replies/forwards
- [ ] Per-account signature (if multi-account)
- [ ] Preview signature
- [ ] Insert company logo in signature
- [ ] Insert social media links in signature
- [ ] Signature separator (`--` line above signature)
- [ ] Signature template gallery (pre-built designs)

---

## 16. Core Features -- Filters & Rules

### 16.1 Filter Rules
- [ ] Create filter rule
  - [ ] Conditions:
    - [ ] From (contains, equals)
    - [ ] To (contains, equals)
    - [ ] Subject (contains, equals)
    - [ ] Body (contains)
    - [ ] Has attachment
    - [ ] Size (greater than, less than)
    - [ ] Date (before, after)
  - [ ] Multiple conditions (AND / OR logic)
  - [ ] Actions:
    - [ ] Apply label
    - [ ] Move to folder
    - [ ] Star
    - [ ] Mark as read
    - [ ] Delete (move to trash)
    - [ ] Forward to address
    - [ ] Never send to spam
    - [ ] Mark as important
  - [ ] Multiple actions per filter
- [ ] Edit filter rule
- [ ] Delete filter rule
- [ ] Reorder filters (priority order)
- [ ] Enable/disable individual filters
- [ ] Apply existing filters to current inbox (retroactive)
- [ ] Import/export filter rules (JSON)
- [ ] Filter match test ("Show me emails that match this filter")

---

## 17. Core Features -- Multi-Account

- [ ] Add additional email accounts
  - [ ] Add account via IMAP/POP3 settings
  - [ ] Add account via OAuth (Gmail, Outlook)
  - [ ] Account name / display name
- [ ] Unified inbox (all accounts in one view)
- [ ] Per-account inbox view
- [ ] Send-as (choose sending address)
  - [ ] Default sending address
  - [ ] Per-compose sending address selector
  - [ ] Verified sending addresses only
- [ ] Account-specific signatures
- [ ] Account-specific settings
- [ ] Account color coding (visual indicator in thread list)
- [ ] Remove account

---

## 18. Core Features -- Email Security

### 18.1 Email Authentication
- [ ] DKIM signing for outgoing emails
- [ ] SPF validation on incoming emails
- [ ] DMARC enforcement
- [ ] Authentication result display in email header ("Passed SPF, DKIM, DMARC")
- [ ] Warning badge if authentication fails

### 18.2 Spam Protection
- [ ] Rspamd integration for spam scoring
- [ ] Spam folder for flagged emails
- [ ] "Not spam" action (train classifier)
- [ ] "Report as spam" action (train classifier)
- [ ] Spam threshold configuration (admin)
- [ ] Blocklist management (blocked senders)
- [ ] Allowlist management (trusted senders)
- [ ] Auto-move spam to spam folder
- [ ] Spam notification suppression

### 18.3 Phishing Protection
- [ ] Phishing detection on incoming emails
- [ ] Phishing warning banner on suspected emails
- [ ] Suspicious link detection (mismatched display/actual URL)
- [ ] Suspicious sender detection (display name spoofing)
- [ ] "This email looks suspicious" warning with details
- [ ] Report phishing button
- [ ] Phishing education tips

### 18.4 Content Security
- [ ] External image blocking by default
  - [ ] "Show images" button per email
  - [ ] "Always show images from [sender]" option
  - [ ] Admin setting: always block / always show / ask
- [ ] External link warning before navigating
- [ ] HTML content sanitization (no scripts, no iframes)
- [ ] Link safety checking (known malicious URL database)
- [ ] Tracking pixel detection and blocking

### 18.5 Encryption
- [ ] S/MIME support (send/receive encrypted emails)
- [ ] PGP support (send/receive encrypted emails)
- [ ] Key management (upload/generate keys)
- [ ] Encrypted email indicator (lock icon)
- [ ] Auto-encrypt when recipient has public key

---

## 19. Core Features -- AI Features

### 19.1 AI Compose Assistance
- [ ] Smart compose (auto-complete suggestions as you type)
- [ ] AI draft generation ("Write a reply declining the meeting")
- [ ] Tone adjustment (make more formal, more casual, shorter)
- [ ] Grammar and spelling check
- [ ] Translation (compose in another language)
- [ ] Subject line suggestions

### 19.2 AI Inbox Management
- [ ] Priority inbox (AI-ranked by importance)
- [ ] Email categorization (auto-label)
- [ ] Smart notifications (only notify for important emails)
- [ ] Unsubscribe suggestions (detect newsletter, offer unsubscribe)
- [ ] Duplicate/similar email detection

### 19.3 AI Thread Analysis
- [x] Thread summarization (condense long threads)
- [ ] Action item extraction ("You need to respond by Friday")
- [ ] Key decision extraction ("We agreed to go with Option B")
- [ ] Sender sentiment analysis
- [ ] Meeting detection (extract date/time, offer calendar event)
- [ ] Contact extraction (detect new contacts in emails)

---

## 20. Core Features -- Integrations

### 20.1 Orbit Ecosystem Integrations
- [x] Cross-app links (open Atlas, TurboTick from Mail)
- [x] `openOrbitApp()` utility for cross-app navigation
- [x] Port mapping for local development
- [x] Subdomain mapping for production
- [ ] Mail -> Atlas: convert email to task (one-click)
  - [ ] Prefill task title from subject
  - [ ] Prefill task description from email body
  - [ ] Link task to email thread
- [ ] Mail -> TurboTick: convert email to support ticket
  - [ ] Prefill ticket from email
  - [ ] Link ticket to email thread
- [ ] Mail -> Planet: associate email with CRM contact/deal
  - [ ] Auto-detect contact by sender email
  - [ ] Show CRM context in thread view
- [ ] Mail -> Calendar: detect meeting invites
  - [ ] Parse ICS attachments
  - [ ] Accept/decline/tentative buttons
  - [ ] Add to Orbit Calendar
- [ ] Mail -> Connect: share email to channel
  - [ ] Share as link
  - [ ] Share with preview
- [ ] Mail -> Writer: save email content as document

### 20.2 External Integrations
- [ ] Mailto: link handler (set RM Mail as default email client)
- [ ] Browser extension for Gmail import
- [ ] CalDAV integration (calendar invites)
- [ ] CardDAV integration (contacts)

---

## 21. Core Features -- Auth & PKCE

### 21.1 PKCE OAuth Flow
- [x] PKCE helper functions (generateRandomString, sha256, base64UrlEncode, generatePKCE)
- [x] SSO config fetch from `/auth/sso/config`
- [x] Authorization URL construction with PKCE challenge
- [x] Code exchange via `/auth/sso/exchange`
- [x] PKCE verifier stored in sessionStorage
- [x] Cleanup verifier after exchange
- [ ] PKCE tests (unit tests for helper functions)
- [ ] Error handling: SSO config fetch failure
- [ ] Error handling: code exchange failure
- [ ] Error handling: expired/invalid code

### 21.2 Protected Routes
- [x] ProtectedRoute component wraps authenticated pages
- [x] Auth check via `/auth/me` endpoint
- [x] Redirect to `/login` if not authenticated
- [x] Loading state during auth check
- [ ] Auth check uses cookies (not localStorage tokens)
- [ ] Token refresh on 401 (interceptor)
- [ ] Session timeout handling (redirect after inactivity)
- [ ] Cross-tab auth sync (logout in one tab -> all tabs)

### 21.3 Logout
- [x] Logout clears localStorage tokens
- [x] Logout calls `/auth/logout` endpoint
- [x] Unauthorized event handler registered
- [ ] Logout clears all session state
- [ ] Logout redirects to Gate login page
- [ ] Logout invalidates server session (not just cookies)

---

## 22. Core Features -- Notifications

- [ ] Desktop push notifications for new email
- [ ] Browser notification permission request
- [ ] Notification click: open email in RM Mail
- [ ] In-app notification indicator (bell icon badge)
- [ ] Notification sound (configurable)
- [ ] Notification preferences per folder
- [ ] Do Not Disturb mode (suppress all notifications)
- [ ] Notification for specific senders only
- [ ] Real-time notification via SSE/WebSocket
- [ ] Notification badge in browser tab title

---

## 23. Core Features -- Offline Support

- [x] Offline detection (`navigator.onLine`)
- [x] Offline banner display in AppLayout
- [ ] Cache inbox emails in IndexedDB/localStorage
- [ ] Read cached emails while offline
- [ ] Queue compose/send for when back online
- [ ] Queue actions (star, delete, move) for when back online
- [ ] Sync queue replay on reconnect
- [ ] "Pending changes" indicator
- [ ] Service worker for offline page shell
- [ ] Background sync API for queued actions

---

## 24. Layout & Navigation (AppLayout)

### 24.1 Sidebar
- [x] Sidebar with navigation items (Inbox, Sent, Drafts, Trash, Compose, Search, Settings, Admin)
- [x] Active item highlighting
- [x] Keyboard shortcut hints per nav item
- [x] Logo and branding area
- [x] Storage utilization display
- [x] Storage progress bar
- [ ] Unread count badges per folder
- [ ] Custom folder section
- [ ] Label section (below folders)
- [ ] Collapse/expand sidebar
- [ ] Sidebar footer: user info
- [ ] Sidebar footer: sign out link
- [ ] Resize sidebar width (drag handle)

### 24.2 Header
- [x] Page title display
- [x] Search input (desktop)
- [x] Mobile search button
- [x] AppLauncher button
- [x] Notification bell button
- [x] Compose button (primary)
- [x] Mobile hamburger menu button
- [ ] User avatar in header
- [ ] Breadcrumb navigation
- [ ] Refresh/sync button

### 24.3 Mobile Layout
- [x] Sidebar hidden on mobile by default
- [x] Hamburger button opens sidebar overlay
- [x] Backdrop overlay behind mobile sidebar
- [x] Close button on mobile sidebar
- [ ] Bottom navigation bar on mobile (Inbox, Search, Compose)
- [ ] Swipe gesture to open sidebar
- [ ] Full-screen compose on mobile
- [ ] Back button on thread view (return to list)

### 24.4 App Launcher
- [x] AppLauncher component exists
- [ ] Opens panel with all Orbit apps
- [ ] Grid layout with app icons
- [ ] Click to navigate to app
- [ ] Keyboard navigation
- [ ] Close on outside click

---

## 25. API Integration

### 25.1 HTTP Client (client.ts)
- [x] Axios instance configured
- [x] Base URL configuration
- [ ] Auth token in request headers (cookies preferred over localStorage)
- [ ] `X-Org-Id` header on all requests
- [ ] Request timeout configuration (30s default)
- [ ] Request logging (development only)

### 25.2 Auth Interceptors
- [ ] 401 response interceptor -> trigger token refresh
- [ ] Refresh token: call Gate refresh endpoint
- [ ] Retry original request after refresh
- [ ] If refresh fails -> redirect to login
- [ ] Queue concurrent requests during refresh

### 25.3 Error Handling
- [ ] Show user-facing toast on API failure
- [ ] Network error detection (offline)
- [ ] Timeout error handling
- [ ] 403 Forbidden handling
- [ ] 404 Not Found handling
- [ ] 422 Validation error handling
- [ ] 500 Server error handling (retry)
- [ ] Rate limit (429) handling

### 25.4 API Endpoints Used
- [x] `GET /auth/sso/config` — fetch SSO configuration
- [x] `POST /auth/sso/exchange` — exchange code for tokens
- [x] `GET /auth/me` — check authentication status
- [x] `POST /auth/logout` — logout
- [x] `GET /mail/context` — fetch storage/context info
- [x] `GET /mail/{folder}` — fetch emails in folder (inbox, sent, drafts, trash)
- [ ] `GET /mail/thread/{thread_id}` — fetch full thread
- [ ] `POST /mail/send` — send email
- [ ] `POST /mail/draft` — save draft
- [ ] `PUT /mail/draft/{id}` — update draft
- [ ] `DELETE /mail/draft/{id}` — delete draft
- [ ] `POST /mail/thread/{id}/star` — star thread
- [ ] `DELETE /mail/thread/{id}/star` — unstar thread
- [ ] `POST /mail/thread/{id}/read` — mark as read
- [ ] `POST /mail/thread/{id}/unread` — mark as unread
- [ ] `POST /mail/thread/{id}/archive` — archive thread
- [ ] `POST /mail/thread/{id}/trash` — move to trash
- [ ] `POST /mail/thread/{id}/move` — move to folder
- [ ] `POST /mail/thread/{id}/label` — apply label
- [ ] `DELETE /mail/thread/{id}/label/{label_id}` — remove label
- [ ] `GET /mail/search?q=` — search emails
- [ ] `POST /mail/attachment` — upload attachment
- [ ] `GET /mail/attachment/{id}` — download attachment
- [ ] `GET /mail/labels` — list labels
- [ ] `POST /mail/labels` — create label
- [ ] `PUT /mail/labels/{id}` — update label
- [ ] `DELETE /mail/labels/{id}` — delete label
- [ ] `GET /mail/filters` — list filter rules
- [ ] `POST /mail/filters` — create filter rule
- [ ] `GET /mail/settings` — get user mail settings
- [ ] `PUT /mail/settings` — update user mail settings
- [ ] `GET /mail/signatures` — list signatures
- [ ] `POST /mail/signatures` — create signature
- [ ] `PUT /mail/signatures/{id}` — update signature
- [ ] `POST /mail/ai/summarize` — AI summarize thread
- [ ] `POST /mail/ai/compose` — AI compose assistant
- [ ] `GET /admin/users` — list users (admin)
- [ ] `POST /admin/users` — create user (admin)
- [ ] `GET /admin/domains` — list domains (admin)
- [ ] `GET /admin/audit-log` — audit log (admin)

### 25.5 Real-Time
- [ ] SSE or WebSocket for new email notifications
- [ ] New email -> update unread count
- [ ] New email -> show desktop notification
- [ ] New email -> add to top of inbox list
- [ ] EventBus integration for cross-app events

---

## 26. State Management

### 26.1 Context
- [x] ComposeContext (`context/ComposeContext.tsx`)
  - [x] `openCompose()` function
  - [ ] `closeCompose()` function
  - [ ] Compose state: recipients, subject, body, attachments
  - [ ] Compose mode: new, reply, replyAll, forward, editDraft
  - [ ] Multiple compose instances
  - [ ] Draft auto-save state

### 26.2 Local State (per-component)
- [x] Mail list state (mails, loading, activeMail)
- [x] Active mail detail state
- [x] AI summary state
- [x] Mobile thread sheet state
- [ ] Consider migrating to Zustand for complex state
  - [ ] Mail store: inbox, sent, drafts, trash lists
  - [ ] Thread store: current thread, messages
  - [ ] UI store: sidebar, compose, search
  - [ ] Settings store: user preferences

### 26.3 Persistence
- [ ] Theme preference persisted to localStorage
- [ ] Sidebar collapsed state persisted
- [ ] Sort/filter preferences persisted per folder
- [ ] Recent searches persisted
- [ ] Draft auto-saves persisted
- [ ] Compose window state persisted (survive page reload)

### 26.4 Cross-Tab Sync
- [ ] Theme changes sync across tabs
- [ ] Auth state sync (logout in one tab -> all tabs)
- [ ] Unread count sync across tabs
- [ ] New email notification across tabs (one tab shows notification, others don't)

---

## 27. Performance

### 27.1 Code Splitting
- [ ] Route-level code splitting for all 7+ routes
  - [ ] LoginPage lazy loaded
  - [ ] Inbox lazy loaded
  - [ ] Sent lazy loaded
  - [ ] Drafts lazy loaded
  - [ ] Trash lazy loaded
  - [ ] Search lazy loaded
  - [ ] Settings lazy loaded
  - [ ] Admin lazy loaded
- [ ] Suspense fallback for each route (loading skeleton)
- [ ] React Quill lazy loaded (only when compose opens)
- [ ] Framer Motion lazy loaded

### 27.2 Virtual Scrolling
- [ ] Thread list: virtual scroll for 10,000+ emails
  - [ ] react-window or @tanstack/react-virtual
  - [ ] Variable height rows (for different preview lengths)
  - [ ] Smooth scrolling
  - [ ] Scroll position restoration on back navigation
- [ ] Thread messages: virtual scroll for long threads (50+ messages)
- [ ] Search results: virtual scroll
- [ ] Admin user list: virtual scroll

### 27.3 Email Content
- [ ] Email content rendered in iframe sandbox
  - [ ] Prevent runaway scripts
  - [ ] Prevent style leakage
  - [ ] Prevent navigation hijacking
  - [ ] Lazy load iframe when scrolled into view
- [ ] Email HTML sanitization (server-side + client-side)
- [ ] Large email truncation ("Click to view entire message")
- [ ] Image proxying (load external images through proxy)

### 27.4 API Optimization
- [ ] Progressive loading: load first 20 threads, lazy load more
- [ ] Debounce search input (400ms)
- [ ] API response caching (SWR or React Query)
- [ ] Prefetch next page on scroll near bottom
- [ ] Attachment thumbnail generation (server-side)
- [ ] Email body lazy loading (load on thread open, not list fetch)

### 27.5 Bundle Optimization
- [ ] Tree-shake React Quill (only needed modules)
- [ ] Tree-shake Framer Motion (only needed animations)
- [ ] Tree-shake Lucide icons (only imported icons)
- [ ] Analyze bundle size (vite-bundle-visualizer)
- [ ] Bundle size budget (< 400KB initial JS)
- [ ] Critical CSS inlined
- [ ] First meaningful paint < 2s on fast 3G

### 27.6 Caching
- [ ] Service worker for static assets
- [ ] Email list cached for instant back navigation
- [ ] Thread content cached (don't re-fetch on back)
- [ ] Attachment thumbnail cached
- [ ] Search results cached for repeated queries

---

## 28. Accessibility

### 28.1 Navigation
- [ ] Skip-to-main-content link at top of page
- [x] Skip link exists (`.mail-skip-link` in App.tsx)
- [ ] Skip link visible on focus
- [ ] Sidebar navigation: arrow key navigation
- [ ] Sidebar navigation: Enter to activate
- [ ] Page title updates on route change

### 28.2 Email List
- [ ] Thread list: arrow key navigation (J/K or up/down)
- [ ] Thread list: Enter to open thread
- [ ] Thread list: Space to select/deselect
- [ ] Thread list: ARIA live region for "X new emails"
- [ ] Thread list: item has role="option" or role="row"
- [ ] Thread list container: role="list" or role="grid"
- [ ] Selected item: aria-selected="true"
- [ ] Unread indicator: accessible (not just visual bold)
- [ ] Star button: aria-pressed state

### 28.3 Compose
- [ ] Tab order: To -> CC -> BCC -> Subject -> Body -> Attach -> Send
- [ ] Recipient chips: keyboard removable (Backspace on focused chip)
- [ ] Recipient autocomplete: keyboard navigable
- [ ] Rich text editor: toolbar keyboard accessible
- [ ] Rich text editor: format shortcuts (Cmd+B, Cmd+I)
- [ ] Send button: aria-label includes "Send email"
- [ ] Attachment upload: accessible drag-and-drop alternative
- [ ] Close compose: Escape key or close button

### 28.4 Thread View
- [ ] Thread messages: navigable with heading structure
- [ ] Expand/collapse: keyboard accessible (Enter/Space)
- [ ] Attachment download: keyboard accessible
- [ ] Action buttons: keyboard accessible with aria-labels
- [ ] "Load images" button: focus management

### 28.5 Keyboard Shortcut Overlay
- [ ] Press `?` to show all keyboard shortcuts
- [ ] Overlay: keyboard dismissible (Escape)
- [ ] Overlay: focus trapped
- [ ] Shortcuts listed with descriptions

### 28.6 Screen Reader
- [ ] New email announcement: aria-live region
- [ ] Send confirmation: announced to screen reader
- [ ] Error messages: announced to screen reader
- [ ] Loading states: aria-busy="true"
- [ ] All icons: aria-label or aria-hidden
- [ ] Email content: accessible tables, images with alt text

### 28.7 Color & Visual
- [ ] Color contrast WCAG AA (4.5:1) in light mode
- [ ] Color contrast WCAG AA (4.5:1) in dark mode
- [ ] Focus-visible ring on all interactive elements
- [ ] Unread status not dependent on color alone (also bold text)
- [ ] Star status not dependent on color alone (also aria state)
- [ ] `prefers-reduced-motion` respected (no compose animations)

---

## 29. Mobile & Responsive

### 29.1 Layout Adaptation
- [x] Mobile sidebar hidden by default
- [x] Hamburger menu opens sidebar overlay
- [x] Backdrop overlay on mobile sidebar
- [ ] Two-panel layout (list + thread) collapses to single panel on mobile
  - [ ] Mobile: full-width email list
  - [ ] Mobile: tap email -> full-width thread view
  - [ ] Mobile: back button returns to list
- [ ] Tablet: side-by-side panels (narrow list + wide thread)
- [ ] Desktop: full side-by-side with sidebar

### 29.2 Mobile-Specific UI
- [ ] Bottom sheet for compose (instead of floating panel)
- [ ] Swipe right on thread to archive
- [ ] Swipe left on thread to delete
- [ ] Pull-to-refresh on email list
- [ ] Touch-friendly attachment upload (camera, gallery, files)
- [ ] Pinch-to-zoom on email content
- [ ] Mobile-optimized compose (full screen)
- [ ] Bottom action bar for thread (reply, forward, delete)
- [x] Long-press for context actions on threads

### 29.3 Responsive Testing
- [ ] Test at 320px (small phone)
- [ ] Test at 375px (iPhone SE)
- [ ] Test at 414px (iPhone Pro Max)
- [ ] Test at 768px (iPad portrait)
- [ ] Test at 1024px (iPad landscape)
- [ ] Test at 1280px (laptop)
- [ ] Test at 1440px (desktop)
- [ ] Test at 1920px (large desktop)
- [ ] No horizontal scroll on any viewport
- [ ] Touch targets minimum 44x44px on mobile

---

## 30. Internationalization (i18n)

- [ ] i18n library chosen and configured
- [ ] All user-facing strings externalized to locale files
- [ ] English locale file complete
- [ ] Date formatting uses locale (Intl.DateTimeFormat)
- [ ] Time formatting uses locale (12h/24h based on locale)
- [ ] Number formatting uses locale (file sizes, counts)
- [ ] RTL layout support (Arabic, Hebrew)
- [ ] Locale switching UI in settings
- [ ] Email date display respects user timezone
- [ ] Relative date display ("2 hours ago") uses locale

---

## 31. Security

### 31.1 Frontend Security
- [ ] XSS prevention: all user input sanitized
- [ ] Email content sanitization (no script execution)
- [ ] CSP headers: no inline scripts
- [ ] No `dangerouslySetInnerHTML` without sanitizer
- [ ] React Quill output sanitized before send
- [ ] External link warnings
- [ ] No sensitive data in localStorage (use httpOnly cookies)
- [ ] Environment variables: no secrets in frontend code
- [ ] CORS: only allow Orbit domains
- [ ] iframe sandbox for email content

### 31.2 Auth Security
- [x] PKCE OAuth flow (no client secret in frontend)
- [ ] Token refresh via httpOnly cookies
- [ ] Session timeout after inactivity
- [ ] CSRF protection
- [ ] Logout clears all auth state

### 31.3 Input Validation
- [ ] Email address format validation
- [ ] Subject line length validation
- [ ] Attachment file type validation
- [ ] Attachment file size validation
- [ ] Search query sanitization
- [ ] Admin form input validation

---

## 32. Testing

### 32.1 Unit Tests
- [x] PKCE helper tests exist (`pkce.test.ts`)
- [x] API client tests exist (`client.test.ts`)
- [ ] Compose form validation tests
- [ ] Thread grouping logic tests
- [ ] Email address parser tests
- [ ] Date formatting utility tests
- [ ] Keyboard shortcut handler tests
- [ ] Search query parser tests
- [ ] Offline detection tests
- [ ] Storage calculation tests

### 32.2 Component Tests
- [ ] LoginPage renders correctly
- [ ] AppLayout renders sidebar and header
- [ ] FloatingComposer opens/closes
- [ ] AppLauncher opens/closes
- [ ] Mail list renders threads
- [ ] Thread view renders messages
- [ ] Compose form accepts input
- [ ] Recipient chips add/remove correctly
- [ ] Rich text editor renders toolbar
- [ ] Empty state renders correctly
- [ ] Loading skeleton renders correctly
- [ ] Error state renders correctly

### 32.3 Integration Tests
- [ ] Login -> navigate to inbox -> see emails
- [ ] Open thread -> read email -> reply
- [ ] Compose -> add recipients -> send
- [ ] Search -> enter query -> view results
- [ ] Star email -> verify starred state
- [ ] Delete email -> verify in trash
- [ ] Create draft -> verify in drafts -> edit -> send
- [ ] Upload attachment -> verify in compose -> send

### 32.4 E2E Tests (Playwright)
- [ ] Full login flow (SSO with Gate)
- [ ] Open inbox -> open thread -> reply
- [ ] Compose new email with attachment -> send
- [ ] Search for email -> find result -> open
- [ ] Keyboard navigation: navigate inbox with J/K
- [ ] Mobile: hamburger menu navigation
- [ ] Mobile: swipe gestures
- [ ] Dark mode: toggle and verify visual

### 32.5 Visual Regression Tests
- [ ] Inbox screenshot comparison
- [ ] Thread view screenshot comparison
- [ ] Compose panel screenshot comparison
- [ ] Settings page screenshot comparison
- [ ] Admin page screenshot comparison
- [ ] All pages in dark mode
- [ ] Mobile viewport screenshots

### 32.6 Performance Tests
- [ ] Inbox with 10,000 threads: renders in < 3s
- [ ] Thread with 50 messages: renders in < 2s
- [ ] Search with 1000 results: renders in < 2s
- [ ] Compose with 10 attachments: no jank
- [ ] Lighthouse score > 85 (Performance)
- [ ] First meaningful paint < 2s on 4G

---

## 33. Documentation

### 33.1 Component Documentation
- [ ] README for each component
- [ ] Props documentation
- [ ] Usage examples

### 33.2 API Documentation
- [ ] All API endpoints documented (request/response)
- [ ] Authentication flow documented
- [ ] Error codes documented
- [ ] Rate limits documented
- [ ] WebSocket/SSE protocol documented

### 33.3 User Guide
- [ ] Getting started guide (first login, compose email)
- [ ] Keyboard shortcuts reference
- [ ] Search syntax guide
- [ ] Settings walkthrough
- [ ] Admin guide (user management, domain setup)

### 33.4 Developer Guide
- [ ] Local development setup
- [ ] Architecture overview
- [ ] Email delivery pipeline documentation
- [ ] Database schema documentation
- [ ] Deployment guide

---

## 34. Deployment & CI/CD

### 34.1 Build Pipeline
- [ ] Vite production build configured
- [ ] Build runs on every PR
- [ ] TypeScript check in CI
- [ ] Lint check in CI
- [ ] Test run in CI

### 34.2 Docker
- [x] Docker Compose files exist (multiple variants)
- [ ] Frontend Dockerfile
- [ ] Backend Dockerfile
- [ ] Nginx config for SPA serving
- [ ] Health check endpoints
- [ ] Docker Compose for local development
- [ ] Docker Compose for production

### 34.3 Environment Configs
- [ ] Development environment
- [ ] Staging environment
- [ ] Production environment
- [ ] Environment variable documentation

### 34.4 Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring
- [ ] Email delivery monitoring (bounce rates, delivery success)
- [ ] Uptime monitoring
- [ ] Queue depth monitoring

---

## 35. Backend -- API Endpoints

### 35.1 Auth Endpoints
- [x] `GET /auth/sso/config` — SSO configuration
- [x] `POST /auth/sso/exchange` — code exchange
- [x] `GET /auth/me` — current user
- [x] `POST /auth/logout` — logout

### 35.2 Mail Endpoints
- [x] `GET /mail/{folder}` — list emails in folder
- [x] `GET /mail/context` — storage/context info
- [ ] `GET /mail/thread/{id}` — full thread
- [ ] `POST /mail/send` — send email
- [ ] `POST /mail/draft` — create draft
- [ ] `PUT /mail/draft/{id}` — update draft
- [ ] `DELETE /mail/draft/{id}` — delete draft
- [ ] `PATCH /mail/thread/{id}` — update thread (star, read, labels)
- [ ] `POST /mail/thread/{id}/move` — move thread
- [ ] `POST /mail/thread/{id}/archive` — archive
- [ ] `DELETE /mail/thread/{id}` — delete permanently

### 35.3 Attachment Endpoints
- [ ] `POST /mail/attachment` — upload attachment
- [ ] `GET /mail/attachment/{id}` — download (signed URL)
- [ ] `DELETE /mail/attachment/{id}` — delete

### 35.4 Search Endpoints
- [ ] `GET /mail/search?q=&from=&to=&after=&before=&has_attachment=` — search
- [ ] Full-text search indexing
- [ ] Search result pagination
- [ ] Search highlight snippets

### 35.5 Settings Endpoints
- [ ] `GET /mail/settings` — user settings
- [ ] `PUT /mail/settings` — update settings
- [ ] `GET /mail/signatures` — list signatures
- [ ] `POST /mail/signatures` — create
- [ ] `PUT /mail/signatures/{id}` — update
- [ ] `DELETE /mail/signatures/{id}` — delete
- [ ] `GET /mail/filters` — list rules
- [ ] `POST /mail/filters` — create rule
- [ ] `PUT /mail/filters/{id}` — update rule
- [ ] `DELETE /mail/filters/{id}` — delete rule
- [ ] `GET /mail/labels` — list labels
- [ ] `POST /mail/labels` — create
- [ ] `PUT /mail/labels/{id}` — update
- [ ] `DELETE /mail/labels/{id}` — delete

### 35.6 Admin Endpoints
- [ ] `GET /admin/users` — list users
- [ ] `POST /admin/users` — create user
- [ ] `PUT /admin/users/{id}` — update user
- [ ] `DELETE /admin/users/{id}` — disable user
- [ ] `GET /admin/domains` — list domains
- [ ] `POST /admin/domains` — add domain
- [ ] `DELETE /admin/domains/{id}` — remove domain
- [ ] `GET /admin/domains/{id}/verify` — check DNS
- [ ] `GET /admin/audit-log` — audit log
- [ ] `GET /admin/quotas` — quota overview
- [ ] `PUT /admin/quotas/{user_id}` — set user quota
- [ ] `GET /admin/routing-rules` — list rules
- [ ] `POST /admin/routing-rules` — create rule

### 35.7 AI Endpoints
- [ ] `POST /mail/ai/summarize` — summarize thread
- [ ] `POST /mail/ai/compose` — generate draft
- [ ] `POST /mail/ai/extract-actions` — extract action items
- [ ] `POST /mail/ai/classify` — classify/categorize email

---

## 36. Backend -- Database Schema

- [ ] `users` table (id, org_id, email, name, role, storage_quota, status)
- [ ] `mailboxes` table (id, user_id, name, type, unread_count)
- [ ] `emails` table (id, mailbox_id, thread_id, message_id, subject, from_addr, to_addrs, cc_addrs, bcc_addrs, body_text, body_html, date, size, is_read, is_starred, is_draft, headers_json)
- [ ] `threads` table (id, mailbox_id, subject, snippet, last_date, message_count, is_read, is_starred)
- [ ] `attachments` table (id, email_id, filename, content_type, size, storage_path, checksum)
- [ ] `labels` table (id, user_id, name, color, type)
- [ ] `email_labels` join table (email_id, label_id)
- [ ] `thread_labels` join table (thread_id, label_id)
- [ ] `folders` table (id, user_id, name, parent_id, position)
- [ ] `signatures` table (id, user_id, name, content_html, is_default)
- [ ] `filter_rules` table (id, user_id, conditions_json, actions_json, priority, is_enabled)
- [ ] `contacts` table (id, user_id, email, name, avatar_url, frequency)
- [ ] `drafts` table (id, user_id, to_addrs, cc_addrs, bcc_addrs, subject, body_html, attachments_json, updated_at)
- [ ] `scheduled_sends` table (id, draft_id, scheduled_time, status)
- [ ] `admin_audit_log` table (id, admin_user_id, action, target_type, target_id, details_json, timestamp)
- [ ] `domains` table (id, org_id, domain_name, verified, dkim_key, spf_record, dmarc_record)
- [ ] `routing_rules` table (id, org_id, pattern, action, destination)
- [ ] `blocklist` table (id, user_id, email_or_domain)
- [ ] `allowlist` table (id, user_id, email_or_domain)

### Database Indexes
- [ ] Index on `emails.thread_id`
- [ ] Index on `emails.mailbox_id, date`
- [ ] Index on `threads.mailbox_id, last_date`
- [ ] Full-text index on `emails.subject, body_text`
- [ ] Index on `emails.from_addr`
- [ ] Index on `email_labels.label_id`

### Migrations
- [ ] Alembic configured
- [ ] Initial migration (create all tables)
- [ ] Migration for each schema change
- [ ] Rollback migrations tested
- [ ] Seed data script (demo accounts, sample emails)

---

## 37. Backend -- Email Delivery

- [ ] Outbound SMTP sending (Postfix or direct)
- [ ] DKIM signing on outbound emails
- [ ] SPF record configuration
- [ ] DMARC record configuration
- [ ] Return-Path header configuration
- [ ] Message-ID generation
- [ ] MIME encoding (multipart/mixed for attachments)
- [ ] HTML + plain text multipart (multipart/alternative)
- [ ] Inline image handling (Content-ID references)
- [ ] Attachment encoding (base64)
- [ ] Email queue (async sending)
- [ ] Delivery retry on temporary failure (4xx SMTP responses)
- [ ] Bounce handling (process NDR emails)
- [ ] Delivery status tracking (sent, delivered, bounced, failed)
- [ ] Unsubscribe header (List-Unsubscribe)
- [ ] Feedback loop processing (FBL from ISPs)
- [ ] IP reputation monitoring
- [ ] Warm-up schedule for new IPs
- [ ] Rate limiting outbound sending (per domain)

---

## 38. Backend -- Email Reception

- [ ] Inbound SMTP server (Postfix or Haraka)
- [ ] MX record configuration
- [ ] TLS encryption (STARTTLS)
- [ ] Email parsing (MIME decoding)
- [ ] Threading (In-Reply-To / References headers)
- [ ] Thread-ID assignment
- [ ] Attachment extraction and storage
- [ ] HTML sanitization on inbound
- [ ] Envelope recipient routing (virtual users)
- [ ] Catchall handling
- [ ] Auto-reply detection (avoid reply loops)
- [ ] Forwarding rule execution
- [ ] Filter rule execution on inbound
- [ ] Label auto-assignment on inbound
- [ ] Unread count update
- [ ] New email notification trigger (EventBus)
- [ ] Size limit enforcement (reject oversized emails)
- [ ] Rate limiting inbound (per sender)

---

## 39. Backend -- Spam & Security

- [ ] Rspamd integration
- [ ] Spam score threshold (configurable)
- [ ] Spam folder routing (score > threshold)
- [ ] Reject emails with very high spam score
- [ ] SPF checking on inbound
- [ ] DKIM verification on inbound
- [ ] DMARC checking on inbound
- [ ] Virus scanning (ClamAV integration)
- [ ] Phishing URL detection
- [ ] Sender reputation checking
- [ ] Blocklist checking (RBL/DNSBL)
- [ ] Content filtering rules
- [ ] Attachment type blocking (configurable)
- [ ] Bayesian learning from user actions (spam/not spam)
- [ ] Quarantine for suspicious emails
- [ ] Admin quarantine review

---

## 40. Backend -- Search Service

- [ ] Full-text search engine (PostgreSQL FTS or Elasticsearch)
- [ ] Index: subject, body_text, from_addr, to_addrs
- [ ] Search query parsing (from:, to:, subject:, has:attachment)
- [ ] Search result ranking (relevance)
- [ ] Search result snippets (context around match)
- [ ] Search result highlighting
- [ ] Search autocomplete suggestions
- [ ] Index updates on new email (real-time or near-real-time)
- [ ] Index updates on email delete/move
- [ ] Search performance: < 200ms for common queries
- [ ] Search pagination

---

## 41. Backend -- Admin Service

- [ ] User CRUD operations
- [ ] Domain management
- [ ] DNS verification (check MX, SPF, DKIM, DMARC records)
- [ ] Quota management
- [ ] Routing rule management
- [ ] Audit logging
- [ ] Admin permission enforcement
- [ ] Bulk user import
- [ ] Storage usage reporting
- [ ] Email delivery statistics

---

## 42. Backend -- SSO / Auth Service

- [x] SSO configuration endpoint
- [x] Code exchange endpoint
- [x] Session management
- [x] Logout endpoint
- [ ] Token refresh endpoint
- [ ] Gate JWT validation middleware
- [ ] Permission checking middleware
- [ ] Admin role enforcement
- [ ] Cross-origin session handling

---

## 43. Backend -- EventBus Integration

- [ ] Publish "new email received" event
- [ ] Publish "email sent" event
- [ ] Publish "email deleted" event
- [ ] Subscribe to org change events
- [ ] Subscribe to user deactivation events
- [ ] Event schema definition
- [ ] Event publishing retry on failure

---

## 44. Backend -- Background Workers

- [ ] Email queue worker (process outbound queue)
- [ ] Inbound processing worker (parse, filter, store)
- [ ] Attachment processing worker (virus scan, thumbnail)
- [ ] Search indexing worker
- [ ] Scheduled send worker (check and send at scheduled time)
- [ ] Trash auto-purge worker (delete emails > 30 days old)
- [ ] Spam auto-purge worker (delete spam > 30 days old)
- [ ] Bounce processing worker
- [ ] AI processing worker (summarize, classify)
- [ ] Notification worker (push, email digest)
- [ ] Vacation responder worker
- [ ] Filter rule execution worker

---

## 45. Backend -- Infrastructure

### 45.1 Docker
- [x] Docker Compose files (demo, standalone, onprem, prod)
- [ ] PostgreSQL container
- [ ] Redis container (caching, queue)
- [ ] Postfix container (SMTP)
- [ ] Rspamd container (spam filtering)
- [ ] ClamAV container (virus scanning)
- [ ] Mail frontend container (Nginx + SPA)
- [ ] Mail backend container (FastAPI)
- [ ] Worker container(s)
- [ ] Health checks on all containers
- [ ] Volume mounts for persistent data

### 45.2 SSL/TLS
- [ ] Let's Encrypt certificate automation
- [ ] TLS on SMTP (STARTTLS)
- [ ] TLS on IMAP (if exposed)
- [ ] TLS on web frontend
- [ ] Certificate renewal automation

### 45.3 Monitoring
- [ ] Email delivery success rate dashboard
- [ ] Email queue depth monitoring
- [ ] Spam detection rate
- [ ] Storage usage per user
- [ ] API response time monitoring
- [ ] Error rate monitoring
- [ ] Uptime monitoring

### 45.4 Backup
- [ ] Database backup schedule (daily)
- [ ] Email storage backup
- [ ] Attachment storage backup
- [ ] Backup verification (restore test)
- [ ] Backup retention policy (30 days)

---

## Summary

| Section | Done | Todo | Total |
|---------|------|------|-------|
| Project Setup | ~12 | ~30 | ~42 |
| Design System | ~3 | ~200 | ~203 |
| Dark Mode | 0 | ~95 | ~95 |
| Inbox | ~5 | ~55 | ~60 |
| Thread View | ~6 | ~55 | ~61 |
| Compose | 0 | ~75 | ~75 |
| Floating Composer | ~1 | ~15 | ~16 |
| Folders | ~5 | ~40 | ~45 |
| Labels | 0 | ~20 | ~20 |
| Search | ~3 | ~25 | ~28 |
| Settings | ~1 | ~30 | ~31 |
| Admin | ~1 | ~40 | ~41 |
| Keyboard Shortcuts | ~6 | ~20 | ~26 |
| Attachments | 0 | ~25 | ~25 |
| Signatures | 0 | ~10 | ~10 |
| Filters | 0 | ~20 | ~20 |
| Multi-Account | 0 | ~10 | ~10 |
| Email Security | 0 | ~30 | ~30 |
| AI Features | ~3 | ~15 | ~18 |
| Integrations | ~4 | ~15 | ~19 |
| Auth & PKCE | ~10 | ~10 | ~20 |
| Notifications | 0 | ~10 | ~10 |
| Offline Support | ~2 | ~10 | ~12 |
| Layout | ~12 | ~15 | ~27 |
| API Integration | ~6 | ~60 | ~66 |
| State Management | ~5 | ~20 | ~25 |
| Performance | 0 | ~35 | ~35 |
| Accessibility | ~1 | ~35 | ~36 |
| Mobile | ~4 | ~20 | ~24 |
| i18n | 0 | ~10 | ~10 |
| Security | ~1 | ~20 | ~21 |
| Testing | ~2 | ~40 | ~42 |
| Documentation | 0 | ~15 | ~15 |
| Deployment | ~1 | ~15 | ~16 |
| Backend API | ~6 | ~60 | ~66 |
| Backend DB | 0 | ~25 | ~25 |
| Backend Delivery | 0 | ~20 | ~20 |
| Backend Reception | 0 | ~18 | ~18 |
| Backend Spam | 0 | ~16 | ~16 |
| Backend Search | 0 | ~11 | ~11 |
| Backend Admin | 0 | ~10 | ~10 |
| Backend Auth | ~4 | ~5 | ~9 |
| Backend EventBus | 0 | ~7 | ~7 |
| Backend Workers | 0 | ~12 | ~12 |
| Backend Infra | ~1 | ~20 | ~21 |
| **TOTAL** | **~105** | **~1429** | **~1534** |
