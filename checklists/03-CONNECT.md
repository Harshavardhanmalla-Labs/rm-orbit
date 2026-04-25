# 03 — Connect: Team Communication App

> **Stack:** React 19.2.3 · Vite 7.2.4 · SPA (no router) · Tailwind v4 · Zustand · Socket.io · WebRTC
> **Routes:** N/A (SPA — view state managed by Zustand store)
> **Status:** ~75% feature complete
> **Components:** App, TopNav, StreamList, ChatArea, RightPanel, MessageItem, MessageComposer, Avatar, BrandMark, AppLauncher, AuthLayout, CommandPalette, ThemeToggle, KeyboardShortcuts, CreateChannelModal, UserSettingsModal, CallOverlay
> **Store:** useStore (Zustand with persist middleware)
> **Services:** webrtc.ts (Socket.io + RTCPeerConnection)
> **Types:** User, Channel, Message, Notification, Attachment, Reaction, Thread, SidebarView, SearchResult, WritingSuggestion
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
- [x] React 19 installed and configured
- [x] Vite 7 configured as build tool
- [x] TypeScript configured (`tsconfig.json`)
- [x] Tailwind v4 configured (`index.css` with `@import "tailwindcss"`)
- [x] Zustand installed for state management
- [x] Socket.io-client installed for real-time messaging
- [x] uuid installed for ID generation
- [x] Lucide React installed for icons
- [x] date-fns installed for date formatting
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
- [x] `@/` path alias configured in Vite (`vite.config.ts`)
- [x] `@/` alias configured in TypeScript (`tsconfig.json`)
- [ ] Import order enforced (external → internal → relative → styles)
- [ ] Barrel exports from `@/components/index.ts`
- [ ] Barrel exports from `@/utils/index.ts`
- [ ] Barrel exports from `@/services/index.ts`

### 1.3 Environment Configuration
- [x] `VITE_SIGNALING_SERVER` env var for backend URL
- [x] `VITE_GATE_URL` env var for Gate auth server
- [ ] `.env.example` file with all required env vars documented
- [ ] `.env.development` with local defaults
- [ ] `.env.production` with production values (placeholder)
- [ ] `.env.test` with test environment values
- [ ] Environment variable validation at app start (fail fast if missing)

### 1.4 Project Structure
- [x] `src/components/` — UI components
- [x] `src/pages/` — Login, Signup pages
- [x] `src/store/` — Zustand store
- [x] `src/services/` — WebRTC service
- [x] `src/types/` — TypeScript type definitions
- [x] `src/utils/` — Utility functions (cn, authContext, writingAssistant, orbitIntegrations)
- [x] `src/data/` — Mock data
- [ ] `src/hooks/` — Custom React hooks directory
- [ ] `src/constants/` — App constants directory
- [ ] `src/api/` — API client layer directory

### 1.5 Build Configuration
- [x] Vite dev server running on configured port
- [ ] Production build optimized (minification, tree-shaking)
- [ ] Source maps configured for production (hidden or external)
- [ ] Bundle analyzer configured (rollup-plugin-visualizer)
- [ ] Build output split into vendor and app chunks
- [ ] Asset hashing for cache busting
- [ ] Compression plugin (gzip/brotli) for production builds

---

## 2. Design System Integration

### 2.1 Token & Theme Foundation
- [x] `ThemeProvider` wraps root in `main.tsx`
- [x] Anti-FOUC script present in `index.html`
- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css"` before `@import "tailwindcss"`
- [x] `index.css` imports `@import "/orbit-ui/orbit-tailwind-v4.css"` after tailwindcss
- [ ] Remove Google Fonts DM Sans reference (verify no CSS `@import` or `font-face` remains)
- [ ] Replace all `font-['DM_Sans']` occurrences with `font-sans`
- [ ] Configure `JetBrains Mono` for code blocks via orbit-tailwind-v4 theme
- [ ] Replace all hardcoded hex colors with design token CSS variables
- [ ] Replace `bg-gray-*` with semantic tokens (`bg-surface-*`)
- [ ] Replace `text-gray-*` with semantic tokens (`text-content-*`)
- [ ] Replace `border-gray-*` with semantic tokens (`border-border-*`)
- [ ] Replace hardcoded sidebar background colors with `bg-surface-subtle`
- [ ] Replace hardcoded message bubble colors with semantic tokens
- [ ] Replace hardcoded focus ring styles with `focus-ring` utility class
- [ ] Replace custom scrollbar CSS with `.scrollbar-thin` plugin class
- [ ] Verify all color contrast ratios meet WCAG AA (4.5:1 normal text, 3:1 large text)

### 2.2 Replace Custom Avatar Component
- [ ] Remove `src/components/Avatar.tsx` custom implementation
- [ ] Import `Avatar` from `@orbit-ui/react` in `ChatArea.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `StreamList.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `RightPanel.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `MessageItem.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `TopNav.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `UserSettingsModal.tsx`
- [ ] Import `Avatar` from `@orbit-ui/react` in `CommandPalette.tsx`
- [ ] Use `AvatarGroup` for group DM participant display
- [ ] Use `Avatar` status prop for online/away/busy/offline indicator
- [ ] Ensure Avatar fallback initials match existing behavior

### 2.3 Replace Custom Badge
- [ ] Import `Badge` from `@orbit-ui/react`
- [ ] Replace unread count badge in `StreamList.tsx` with `<Badge>`
- [ ] Replace mention count badge in `TopNav.tsx` with `<Badge>`
- [ ] Replace online status indicator dot with `<Badge>` dot variant
- [ ] Replace notification count badge with `<Badge>`
- [ ] Replace channel type indicator with `<Badge>`
- [ ] Replace user role badge in profile panel with `<Badge>`

### 2.4 Replace Custom Button
- [ ] Import `Button` from `@orbit-ui/react`
- [ ] Replace send message button in `MessageComposer.tsx` with `<Button>`
- [ ] Replace call buttons (voice/video) in `ChatArea.tsx` with `<Button>`
- [ ] Replace panel toggle buttons in `ChatArea.tsx` with `<Button>`
- [ ] Replace create channel button in `StreamList.tsx` with `<Button>`
- [ ] Replace login button in `Login.tsx` with `<Button>`
- [ ] Replace signup button in `Signup.tsx` with `<Button>`
- [ ] Replace sidebar view toggle buttons with `<Button>` group
- [ ] Replace "Mark all read" button with `<Button>`
- [ ] Replace settings save button with `<Button>`
- [ ] Replace modal action buttons (create, cancel, confirm) with `<Button>`
- [ ] Replace file upload trigger button with `<Button>`
- [ ] Import `IconButton` from `@orbit-ui/react`
- [ ] Replace icon-only action buttons (pin, bookmark, edit, delete) with `<IconButton>`
- [ ] Replace close buttons (panels, modals) with `<IconButton>`
- [ ] Replace reaction trigger button with `<IconButton>`

### 2.5 Replace Custom Input
- [ ] Import `Input` from `@orbit-ui/react`
- [ ] Replace search input in `StreamList.tsx` with `<Input>`
- [ ] Replace search input in `CommandPalette.tsx` with `<Input>`
- [ ] Replace search input in `RightPanel.tsx` with `<Input>`
- [ ] Replace channel name input in `CreateChannelModal.tsx` with `<Input>`
- [ ] Replace login email input with `<Input>`
- [ ] Replace login password input with `<Input>`
- [ ] Replace signup name/email/password inputs with `<Input>`
- [ ] Replace user settings inputs with `<Input>`

### 2.6 Replace Custom Modal
- [ ] Import `Modal` from `@orbit-ui/react`
- [ ] Replace `CreateChannelModal.tsx` custom modal wrapper with `<Modal>`
- [ ] Replace `UserSettingsModal.tsx` custom modal wrapper with `<Modal>`
- [ ] Replace `KeyboardShortcuts.tsx` modal wrapper with `<Modal>`
- [ ] Ensure modal focus trap works with `<Modal>` component
- [ ] Ensure modal close on Escape works with `<Modal>`
- [ ] Ensure modal backdrop click-to-close works

### 2.7 Replace Custom Tooltip
- [ ] Import `Tooltip` from `@orbit-ui/react`
- [ ] Add `<Tooltip>` on all icon-only buttons in `ChatArea.tsx`
- [ ] Add `<Tooltip>` on call control buttons in `CallOverlay.tsx`
- [ ] Add `<Tooltip>` on message action buttons in `MessageItem.tsx`
- [ ] Add `<Tooltip>` on sidebar view tabs in `StreamList.tsx`
- [ ] Add `<Tooltip>` on reaction emoji hover (show who reacted)
- [ ] Add `<Tooltip>` on user status indicator in `Avatar`
- [ ] Add `<Tooltip>` on notification bell in `TopNav.tsx`
- [ ] Add `<Tooltip>` on theme toggle button

### 2.8 Replace Custom Dropdown
- [ ] Import `Dropdown`, `DropdownTrigger`, `DropdownContent`, `DropdownItem`, `DropdownSeparator` from `@orbit-ui/react`
- [ ] Replace message action menu (edit/delete/pin/bookmark/reply) in `MessageItem.tsx` with `<Dropdown>`
- [ ] Replace channel action menu (archive/leave/settings) with `<Dropdown>`
- [ ] Replace user status selector in `TopNav.tsx` with `<Dropdown>`
- [ ] Replace notification actions menu with `<Dropdown>`
- [ ] Replace message composer formatting menu with `<Dropdown>`
- [ ] Replace emoji picker trigger with `<Dropdown>` or `<Popover>`

### 2.9 Replace Custom Switch
- [ ] Import `Switch` from `@orbit-ui/react`
- [ ] Replace notification toggle in `UserSettingsModal.tsx` with `<Switch>`
- [ ] Replace sound toggle in settings with `<Switch>`
- [ ] Replace "Private channel" toggle in `CreateChannelModal.tsx` with `<Switch>`
- [ ] Replace do-not-disturb toggle with `<Switch>`
- [ ] Replace desktop notification toggle with `<Switch>`

### 2.10 Adopt Tabs Component
- [ ] Import `Tabs` from `@orbit-ui/react`
- [ ] Replace sidebar view switcher (Channels/DMs/Threads/Search/Mentions/Bookmarks) with `<Tabs>`
- [ ] Replace right panel content tabs (Thread/Profile/Members/Search/Pinned) with `<Tabs>`
- [ ] Replace user settings section tabs with `<Tabs>`

### 2.11 Adopt Card Component
- [ ] Import `Card` from `@orbit-ui/react`
- [ ] Use `<Card>` for channel info card in right panel
- [ ] Use `<Card>` for user profile card in right panel
- [ ] Use `<Card>` for file preview cards in chat
- [ ] Use `<Card>` for link unfurling cards
- [ ] Use `<Card>` for search result items

### 2.12 Adopt Skeleton Component
- [ ] Import `Skeleton`, `SkeletonText`, `SkeletonCard` from `@orbit-ui/react`
- [ ] Add `<Skeleton>` for loading message list
- [ ] Add `<Skeleton>` for loading channel list in sidebar
- [ ] Add `<Skeleton>` for loading user list in members panel
- [ ] Add `<Skeleton>` for loading thread replies
- [ ] Add `<Skeleton>` for loading search results
- [ ] Add `<SkeletonCard>` for loading file preview cards

### 2.13 Adopt Spinner Component
- [ ] Import `Spinner` from `@orbit-ui/react`
- [ ] Replace custom loading indicator in `App.tsx` Suspense fallback with `<Spinner>`
- [ ] Use `<Spinner>` for WebRTC connection loading state
- [ ] Use `<Spinner>` for file upload in-progress state
- [ ] Use `<Spinner>` for initial data fetch loading
- [ ] Use `<Spinner>` for message sending pending state

### 2.14 Adopt EmptyState Component
- [ ] Import `EmptyState` from `@orbit-ui/react`
- [ ] Add `<EmptyState>` for empty channel (no messages yet)
- [ ] Add `<EmptyState>` for no search results
- [ ] Add `<EmptyState>` for empty DM list
- [ ] Add `<EmptyState>` for empty thread list
- [ ] Add `<EmptyState>` for empty pinned messages
- [ ] Add `<EmptyState>` for empty bookmarks
- [ ] Add `<EmptyState>` for empty mentions
- [ ] Add `<EmptyState>` for empty notification list
- [ ] Add `<EmptyState>` for no channels joined

### 2.15 Adopt Alert Component
- [ ] Import `Alert` from `@orbit-ui/react`
- [ ] Replace offline banner (`bg-red-500` div in `App.tsx`) with `<Alert variant="danger">`
- [ ] Use `<Alert>` for connection lost warning
- [ ] Use `<Alert>` for auth error messages
- [ ] Use `<Alert>` for permission denied messages
- [ ] Use `<Alert>` for file upload error messages

### 2.16 Adopt Sidebar Component
- [ ] Import `Sidebar`, `useSidebar` from `@orbit-ui/react`
- [ ] Evaluate replacing custom `StreamList.tsx` sidebar wrapper with `<Sidebar>`
- [ ] Use `Sidebar.Section` for channel groups (Pinned, Channels, DMs)
- [ ] Use `Sidebar.Item` for individual channel items
- [ ] Integrate sidebar collapse/expand with `useSidebar` hook

### 2.17 Adopt CommandPalette Component
- [ ] Import `CommandPalette` from `@orbit-ui/react`
- [ ] Replace custom `CommandPalette.tsx` with shared `<CommandPalette>`
- [ ] Ensure `Cmd+K` / `Ctrl+K` keyboard shortcut works
- [ ] Ensure `/` shortcut still triggers command palette
- [ ] Preserve search categories (channels, users, messages, actions)

### 2.18 Adopt Toast/Notification
- [ ] Import `useToast` from `@orbit-ui/react`
- [ ] Replace custom notification display with `useToast`
- [ ] Show toast on message send failure
- [ ] Show toast on file upload success/failure
- [ ] Show toast on channel creation success
- [ ] Show toast on settings saved
- [ ] Show toast on call connection failure

### 2.19 Adopt Tag/Chip Component
- [ ] Import `Tag` from `@orbit-ui/react`
- [ ] Use `<Tag>` for user mention chips in message composer
- [ ] Use `<Tag>` for channel link chips
- [ ] Use `<Tag>` for file type indicator chips
- [ ] Use `<Tag>` for user role display

### 2.20 Adopt Divider Component
- [ ] Import `Divider` from `@orbit-ui/react`
- [ ] Replace custom date divider in `ChatArea.tsx` with `<Divider>`
- [ ] Use `<Divider>` between sidebar sections
- [ ] Use `<Divider>` in settings modal between sections
- [ ] Use `<Divider>` in right panel between profile sections

### 2.21 Adopt Popover Component
- [ ] Import `Popover` from `@orbit-ui/react`
- [ ] Use `<Popover>` for emoji picker
- [ ] Use `<Popover>` for user status selector
- [ ] Use `<Popover>` for reaction picker on messages
- [ ] Use `<Popover>` for mention autocomplete dropdown

### 2.22 Adopt ContextMenu Component
- [ ] Import `ContextMenu` from `@orbit-ui/react`
- [ ] Add right-click context menu on messages (reply, edit, pin, bookmark, copy, delete)
- [ ] Add right-click context menu on channels (mark read, pin, mute, leave)
- [ ] Add right-click context menu on users (DM, profile, call)

---

## 3. Dark Mode

### 3.1 Layout Shell
- [ ] App root container (`bg-surface`) verified in dark mode
- [ ] Offline banner dark mode contrast verified
- [ ] Skip-to-content link visible in dark mode

### 3.2 Top Navigation (TopNav.tsx)
- [ ] TopNav background in dark mode
- [ ] TopNav border/separator in dark mode
- [ ] Search input in TopNav dark mode styling
- [ ] Notification bell icon color in dark mode
- [ ] User avatar ring/border in dark mode
- [ ] App launcher button in dark mode
- [ ] Unread count badge contrast in dark mode
- [ ] Theme toggle button visibility in dark mode
- [ ] TopNav dropdown menus dark mode

### 3.3 Stream List / Sidebar (StreamList.tsx)
- [ ] Sidebar background color in dark mode
- [ ] Sidebar header section dark mode
- [ ] Channel list item default state dark mode
- [ ] Channel list item hover state dark mode
- [ ] Channel list item active/selected state dark mode
- [ ] Channel icon (hash/lock) colors in dark mode
- [ ] Channel unread count badge contrast dark mode
- [ ] Pinned channel section header dark mode
- [ ] DM list user status indicator dark mode
- [ ] DM list last message preview text dark mode
- [ ] Sidebar view tabs (Channels/DMs/Threads) dark mode
- [ ] Search input in sidebar dark mode
- [ ] Create channel button dark mode
- [ ] Sidebar collapse button dark mode
- [ ] Sidebar scrollbar in dark mode
- [ ] Sidebar section dividers dark mode

### 3.4 Chat Area (ChatArea.tsx)
- [ ] Chat area background in dark mode
- [ ] Channel header (name, description) dark mode
- [ ] Channel header action buttons (search, pin, members, panel) dark mode
- [ ] Call buttons (voice/video) dark mode
- [ ] Date divider line and label dark mode
- [ ] Empty channel state illustration dark mode
- [ ] Connection status indicator dark mode

### 3.5 Message Items (MessageItem.tsx)
- [ ] Message bubble (own messages) dark mode
- [ ] Message bubble (other users' messages) dark mode
- [ ] System messages dark mode
- [ ] Message sender name color dark mode
- [ ] Message timestamp color dark mode
- [ ] Message content text color dark mode
- [ ] Message edited indicator dark mode
- [ ] Reaction badges dark mode
- [ ] Reaction badges hover state dark mode
- [ ] Message hover action bar dark mode
- [ ] Thread reply count link dark mode
- [ ] File attachment card dark mode
- [ ] Image attachment preview dark mode
- [ ] Code block background in dark mode
- [ ] Inline code background in dark mode
- [ ] Blockquote border and background dark mode
- [ ] Link color in messages dark mode
- [ ] @mention highlight color dark mode
- [ ] Pinned message indicator dark mode
- [ ] Bookmarked message indicator dark mode
- [ ] Message selection highlight dark mode

### 3.6 Message Composer (MessageComposer.tsx)
- [ ] Composer container border dark mode
- [ ] Composer textarea background dark mode
- [ ] Composer textarea placeholder text dark mode
- [ ] Composer formatting toolbar dark mode
- [ ] Send button dark mode
- [ ] Attachment button dark mode
- [ ] Emoji button dark mode
- [ ] Mention button dark mode
- [ ] File attachment preview cards dark mode
- [ ] Writing assistant suggestions panel dark mode
- [ ] Smart follow-up suggestions dark mode
- [ ] Emoji picker overlay background dark mode
- [ ] Emoji picker category tabs dark mode
- [ ] Mention autocomplete dropdown dark mode
- [ ] Orbit integrations panel (TurboTick, Atlas) dark mode

### 3.7 Right Panel (RightPanel.tsx)
- [ ] Right panel background dark mode
- [ ] Right panel header dark mode
- [ ] Right panel close button dark mode
- [ ] Thread view: parent message dark mode
- [ ] Thread view: reply messages dark mode
- [ ] Thread view: reply composer dark mode
- [ ] Thread view: thread timeline entries dark mode
- [ ] Profile view: user avatar section dark mode
- [ ] Profile view: user info fields dark mode
- [ ] Profile view: action buttons (DM, call) dark mode
- [ ] Members view: member list rows dark mode
- [ ] Members view: role badges dark mode
- [ ] Members view: status indicators dark mode
- [ ] Search view: search input dark mode
- [ ] Search view: search results dark mode
- [ ] Search view: result highlights dark mode
- [ ] Pinned messages view: pinned message list dark mode
- [ ] Panel tab switcher dark mode

### 3.8 Call Overlay (CallOverlay.tsx)
- [ ] Call overlay backdrop dark mode
- [ ] Video grid background dark mode
- [ ] Participant name labels dark mode
- [ ] Mute/camera indicator badges dark mode
- [ ] Active speaker highlight border dark mode
- [ ] Call controls bar background dark mode
- [ ] Mute button active/inactive dark mode
- [ ] Camera button active/inactive dark mode
- [ ] Screen share button dark mode
- [ ] End call button dark mode
- [ ] Call timer display dark mode
- [ ] Call status text (connecting, ringing) dark mode
- [ ] Incoming call prompt dark mode
- [ ] Connection quality indicator dark mode

### 3.9 Modals
- [ ] Create Channel Modal: background dark mode
- [ ] Create Channel Modal: form inputs dark mode
- [ ] Create Channel Modal: private toggle dark mode
- [ ] Create Channel Modal: action buttons dark mode
- [ ] User Settings Modal: background dark mode
- [ ] User Settings Modal: section headers dark mode
- [ ] User Settings Modal: form inputs dark mode
- [ ] User Settings Modal: toggle switches dark mode
- [ ] User Settings Modal: avatar editor section dark mode
- [ ] Keyboard Shortcuts Modal: background dark mode
- [ ] Keyboard Shortcuts Modal: shortcut key badges dark mode
- [ ] Keyboard Shortcuts Modal: section dividers dark mode

### 3.10 Command Palette
- [ ] Command palette overlay background dark mode
- [ ] Command palette search input dark mode
- [ ] Command palette result items dark mode
- [ ] Command palette result item hover state dark mode
- [ ] Command palette category headers dark mode
- [ ] Command palette keyboard hint badges dark mode
- [ ] Command palette empty results dark mode

### 3.11 Auth Pages
- [ ] Login page background dark mode
- [ ] Login form card dark mode
- [ ] Login form inputs dark mode
- [ ] Login button dark mode
- [ ] Login error message dark mode
- [ ] Signup page background dark mode
- [ ] Signup form card dark mode
- [ ] Signup form inputs dark mode
- [ ] Signup button dark mode
- [ ] Signup error message dark mode
- [ ] Auth switch link ("Already have account?") dark mode

### 3.12 Dark Mode Testing
- [ ] Full dark mode visual audit of all views
- [ ] Test dark mode toggle transition (no flash)
- [ ] Test dark mode persistence across page refresh
- [ ] Test system preference detection (`prefers-color-scheme: dark`)
- [ ] Screenshot comparison: light vs dark for all major views
- [ ] Verify no hardcoded white/black colors remain
- [ ] Verify all shadows appropriate for dark mode
- [ ] Verify all borders visible in dark mode

---

## 4. Core Features

### 4.1 Authentication
- [x] Login page with email/password
- [x] Signup page with name/email/password
- [x] Gate SSO OAuth2 token exchange
- [x] Gate JWT token stored in localStorage
- [x] Auto-detect existing Gate token on load
- [x] Logout clears tokens from localStorage
- [x] Auth state managed in Zustand store
- [ ] Login form validation (email format, password required)
- [ ] Signup form validation (name required, email format, password strength)
- [ ] Password strength indicator on signup
- [ ] "Forgot password" link to Gate reset flow
- [ ] Remember me checkbox
- [ ] OAuth callback handling (redirect from Gate)
- [ ] Token refresh on 401 response
- [ ] Session expiry warning (5 min before expiry)
- [ ] Multi-tab session sync
- [ ] Graceful redirect to login on token expiry

### 4.2 Channels — Public
- [x] List public channels in sidebar
- [x] Create public channel (name, description)
- [x] Set active channel on click
- [x] Channel name displayed in chat header
- [ ] Channel description displayed in chat header
- [ ] Channel topic editing (inline in header)
- [ ] Channel search/filter in sidebar
- [ ] Channel sort (alphabetical, recent activity, unread first)
- [ ] Channel browse/discover (see all public channels)
- [ ] Join public channel
- [ ] Leave channel
- [ ] Archive channel (admin only)
- [ ] Delete channel (admin only, with confirmation)
- [ ] Channel settings page (name, description, topic, permissions)
- [ ] Channel member count displayed
- [ ] Channel creation date displayed
- [ ] Channel creator displayed
- [ ] Default channels for new users (e.g., #general, #random)

### 4.3 Channels — Private
- [x] Create private channel (private toggle in create modal)
- [ ] Private channel lock icon in sidebar
- [ ] Invite-only access for private channels
- [ ] Channel invite: add members by name search
- [ ] Channel invite: add members by email
- [ ] Remove member from private channel (admin)
- [ ] Private channel permissions (who can post, who can invite)
- [ ] Private channel visibility (hidden from non-members)

### 4.4 Direct Messages (DMs)
- [x] 1-on-1 DM creation via `navigateToDM`
- [x] DM list in sidebar (DMs view)
- [x] DM user avatar with status indicator
- [ ] DM search (find user to start conversation)
- [ ] DM online/offline status display
- [ ] DM "last seen" timestamp for offline users
- [ ] DM typing indicator
- [ ] DM read receipts (sent/delivered/read)
- [ ] DM notification badge (unread count)
- [ ] Close/hide DM conversation
- [ ] Block user from DM

### 4.5 Group Direct Messages
- [ ] Create group DM (select multiple users)
- [ ] Group DM name (auto-generated from participants or custom)
- [ ] Group DM avatar (composite of participant avatars)
- [ ] Add participant to existing group DM
- [ ] Remove participant from group DM
- [ ] Leave group DM
- [ ] Group DM member list view
- [ ] Group DM limit (max 8 participants)
- [ ] Convert group DM to private channel

### 4.6 Messaging — Sending
- [x] Send text message to active channel
- [x] Message stored in Zustand with UUID
- [x] Message emitted via Socket.io (`webrtcService.sendMessage`)
- [x] Thread replies (send message with `threadId`)
- [x] Attachments support in message send
- [ ] Multi-line message support (Shift+Enter for newline)
- [ ] Message draft auto-save per channel
- [ ] Message send with Enter key
- [ ] Message send button click
- [ ] Paste image from clipboard (auto-attach)
- [ ] Drag-and-drop file into composer (auto-attach)
- [ ] Schedule message for later sending
- [ ] Message character limit (4000 chars) with counter
- [ ] Prevent sending empty messages
- [ ] Prevent double-send (debounce/disable button)

### 4.7 Messaging — Formatting
- [ ] **Bold** text rendering (`**text**`)
- [ ] _Italic_ text rendering (`_text_`)
- [ ] ~~Strikethrough~~ text rendering (`~~text~~`)
- [ ] `Inline code` rendering (`` `code` ``)
- [ ] Code block rendering (``` multi-line ```)
- [ ] Code block syntax highlighting (language detection)
- [ ] Code block copy-to-clipboard button
- [ ] Blockquote rendering (`> quoted text`)
- [ ] Bulleted list rendering (`- item`)
- [ ] Numbered list rendering (`1. item`)
- [ ] Link auto-detection and clickable rendering
- [ ] Markdown formatting toolbar in composer (bold, italic, code, list buttons)
- [ ] Keyboard shortcuts for formatting (Ctrl+B, Ctrl+I, Ctrl+Shift+C)
- [ ] Message preview before sending (toggle)

### 4.8 Messaging — Reactions
- [x] Add reaction to message (emoji picker)
- [x] Remove own reaction from message
- [x] Reaction count displayed on message
- [x] Reaction users tracked per emoji
- [ ] Quick reaction bar (frequently used emojis)
- [ ] Emoji picker with search
- [ ] Emoji picker with categories
- [ ] Emoji picker with skin tone selection
- [ ] Custom emoji support (org-level)
- [ ] Reaction tooltip showing who reacted
- [ ] Animated emoji for certain reactions
- [ ] `:shortcode:` autocomplete in composer

### 4.9 Messaging — Editing & Deletion
- [x] Edit own message (content update, `edited` flag set)
- [x] Delete own message
- [ ] Edit message via keyboard shortcut (Up arrow on last message)
- [ ] Edit history visible (click "edited" to see changes)
- [ ] Admin can delete any message
- [ ] Delete message with confirmation dialog
- [ ] Deleted message placeholder ("This message was deleted")
- [ ] Bulk message deletion (admin, for moderation)

### 4.10 Messaging — Pinning & Bookmarks
- [x] Pin message toggle
- [x] Bookmark message toggle
- [x] Get pinned messages per channel
- [ ] Pinned messages panel in right panel
- [ ] Pinned message badge/indicator on message
- [ ] Bookmarked messages panel (global, across all channels)
- [ ] Pin/unpin notification to channel
- [ ] Pin limit per channel (with warning)
- [ ] Bookmark categories/tags

### 4.11 Messaging — Threads
- [x] Reply in thread (send message with `threadId`)
- [x] Thread reply count on parent message
- [x] Thread panel in right panel
- [x] `getThreadReplies` helper in store
- [ ] Thread notification badge on parent message
- [ ] "Follow thread" toggle (get notified of new replies)
- [ ] Thread participants list
- [ ] Thread timestamp for last reply
- [ ] Mark thread as resolved
- [ ] Thread keyboard shortcut (T to open thread)
- [ ] Thread auto-scroll to latest reply
- [ ] Thread composer with full formatting support

### 4.12 Messaging — Mentions
- [x] `mentions` field on Message type
- [ ] @mention autocomplete in composer (type `@` to see user list)
- [ ] @mention highlight rendering in messages
- [ ] @channel mention (notify all channel members)
- [ ] @here mention (notify online channel members)
- [ ] Unread mention badge per channel
- [ ] Mentions panel in sidebar (all messages mentioning current user)
- [ ] Click mention to open user profile
- [ ] Mention notification (push + in-app)

### 4.13 Messaging — File Sharing
- [x] Attachment type definition (id, name, type, url, size, mimeType)
- [ ] File upload via button click
- [ ] File upload via drag-and-drop into chat area
- [ ] File upload via paste from clipboard
- [ ] File upload progress indicator
- [ ] File size limit enforcement (client-side, e.g., 50MB)
- [ ] File type restrictions (configurable whitelist)
- [ ] Image inline preview in message
- [ ] Image lightbox (click to enlarge)
- [ ] Image gallery (multiple images in one message)
- [ ] Video inline preview/player
- [ ] Audio inline player
- [ ] PDF preview (thumbnail + download link)
- [ ] Document file download link
- [ ] File name and size display
- [ ] File type icon based on MIME type
- [ ] File delete (by uploader)
- [ ] Files panel (all files shared in channel)
- [ ] File search across channels

### 4.14 Messaging — Search
- [x] Search query state in store
- [ ] Full-text message search across all channels
- [ ] Search results with highlighted match text
- [ ] Search results grouped by channel
- [ ] Search filters: channel, user, date range, has attachment
- [ ] Search result click navigates to message in channel
- [ ] Recent searches history
- [ ] Search keyboard shortcut (Ctrl+F or /)
- [ ] Search debounce (300ms)
- [ ] Search pagination (load more results)
- [ ] Empty search state with suggestions

### 4.15 Messaging — URL Unfurling
- [ ] URL detection in messages
- [ ] Link preview card (title, description, image, favicon)
- [ ] YouTube video embed preview
- [ ] Twitter/X tweet embed preview
- [ ] GitHub issue/PR preview
- [ ] Image URL auto-expand to inline preview
- [ ] Unfurl toggle (collapse/expand preview)
- [ ] Unfurl disabled for private/internal URLs

### 4.16 Messaging — Notifications
- [x] In-app notification system (Notification type defined)
- [x] Add system notification to store
- [x] Mark notification read
- [x] Mark all notifications read
- [x] Notification limit (200 max)
- [ ] Desktop push notification (Notification API permission)
- [ ] Desktop notification for new DM
- [ ] Desktop notification for @mention
- [ ] Desktop notification for thread reply
- [ ] Sound notification on new message
- [ ] Notification preferences: per channel (all/mentions/none)
- [ ] Notification preferences: DMs (on/off)
- [ ] Notification preferences: sounds (on/off)
- [ ] Notification bell in TopNav with unread count
- [ ] Notification dropdown panel
- [ ] Notification click navigates to relevant message
- [ ] Do Not Disturb mode
- [ ] Do Not Disturb schedule (automatic)
- [ ] Mute channel (no notifications)
- [ ] Snooze notifications (for N minutes)

### 4.17 User Presence & Status
- [x] User status types: online, away, busy, offline
- [x] Set user status in store
- [x] Set users online/offline (bulk)
- [x] Set individual user online status
- [ ] Custom status: emoji + text + expiry time
- [ ] Auto-set away after N minutes of inactivity
- [ ] Status displayed on user avatar (green/yellow/red/gray dot)
- [ ] Status displayed in user profile panel
- [ ] Status displayed in DM list
- [ ] Status change propagated via Socket.io
- [ ] "Set yourself as away" manual toggle
- [ ] Custom status presets (In a meeting, Commuting, Vacationing)
- [ ] Clear status button
- [ ] Status expiry (auto-clear after set time)

### 4.18 User Profile
- [x] User type with id, name, email, avatar, status, role, title, department
- [ ] User profile panel in right panel
- [ ] Profile: display name editing
- [ ] Profile: avatar upload/change
- [ ] Profile: title/role display
- [ ] Profile: department display
- [ ] Profile: timezone display
- [ ] Profile: contact info (email, phone)
- [ ] Profile: "Message" button (open DM)
- [ ] Profile: "Call" button (start voice/video call)
- [ ] Profile: "View files shared" link
- [ ] User preferences: notification settings
- [ ] User preferences: theme selection
- [ ] User preferences: language selection
- [ ] User preferences: keyboard shortcut customization

### 4.19 Voice & Video Calls (WebRTC)
- [x] WebRTC service initialized on mount
- [x] Socket.io signaling server connection
- [x] ICE server configuration (STUN servers)
- [x] Call state management (status, direction, type, streams)
- [x] Start call by user ID
- [x] Call overlay component (lazy loaded)
- [ ] 1-on-1 voice call from DM
- [ ] 1-on-1 video call from DM
- [ ] Group voice call (channel huddle)
- [ ] Group video call (channel)
- [ ] Incoming call notification with accept/decline
- [ ] Call ringing sound
- [ ] Call connected sound
- [ ] Call ended sound
- [ ] Mute/unmute audio toggle
- [ ] Camera on/off toggle
- [ ] Speaker selection (output device)
- [ ] Microphone selection (input device)
- [ ] Camera selection (video device)
- [ ] Audio level indicator (voice activity)
- [ ] Active speaker detection and highlight
- [ ] Participant grid layout (2-8 participants)
- [ ] Spotlight/speaker view toggle
- [ ] Gallery view toggle
- [ ] Mini call window (picture-in-picture)
- [ ] Call duration timer
- [ ] Call quality indicator (signal strength)
- [ ] End call for self
- [ ] End call for everyone (host)
- [ ] Call reconnection on network drop
- [ ] Call participant join/leave notification

### 4.20 Screen Sharing
- [ ] Start screen sharing (full screen or window)
- [ ] Stop screen sharing
- [ ] Screen share viewer layout (screen large, participants small)
- [ ] Screen share with audio (system audio)
- [ ] Screen share annotation tools
- [ ] Screen share remote control request
- [ ] Multiple screen shares (if supported)

### 4.21 Background Effects
- [ ] Background blur toggle during call
- [ ] Virtual background selection (preset images)
- [ ] Custom virtual background upload
- [ ] Background effect processing (TensorFlow.js or similar)
- [ ] Background effect performance optimization

### 4.22 Call Recording
- [ ] Start recording (host only)
- [ ] Stop recording
- [ ] Recording indicator visible to all participants
- [ ] Recording consent notification
- [ ] Recording saved to file storage
- [ ] Recording download link
- [ ] Recording playback

### 4.23 Noise Cancellation
- [ ] Enable/disable noise cancellation toggle
- [ ] AI-based noise cancellation (Web Audio API or library)
- [ ] Noise cancellation quality settings (low/medium/high)

### 4.24 Command Palette
- [x] Command palette open/close toggle
- [x] Keyboard shortcut `/` to open (when not in input)
- [x] Lazy loaded component
- [ ] Search channels by name
- [ ] Search users by name
- [ ] Search messages by content
- [ ] Quick actions: create channel, start DM, change status
- [ ] Quick actions: toggle theme, open settings
- [ ] Quick actions: switch to channel by name
- [ ] Keyboard navigation (arrow keys + Enter)
- [ ] Recently used commands section
- [ ] Category headers (Channels, People, Actions)
- [ ] Command palette result highlighting

### 4.25 Keyboard Shortcuts
- [x] Keyboard shortcuts modal component
- [x] Toggle keyboard shortcuts modal
- [ ] `Ctrl+K` / `Cmd+K` — open command palette
- [ ] `/` — open command palette (from non-input context)
- [ ] `Escape` — close modals/panels
- [ ] `Ctrl+Shift+M` — toggle mute (in call)
- [ ] `Ctrl+Shift+V` — toggle camera (in call)
- [ ] `Up arrow` — edit last message
- [ ] `Ctrl+/` — show keyboard shortcuts
- [ ] `Ctrl+N` — new DM
- [ ] `Ctrl+Shift+N` — new channel
- [ ] `Alt+Up/Down` — navigate channels
- [ ] `Ctrl+F` — search messages

### 4.26 Channel Pinning
- [x] Pin/unpin channel toggle in store
- [ ] Pinned channels section at top of sidebar
- [ ] Pinned channel star icon indicator
- [ ] Pin channel from context menu
- [ ] Unpin channel from context menu
- [ ] Pinned channels persisted per user

### 4.27 Unread Tracking
- [x] Unread count per channel in store
- [x] Mark channel read when channel is activated
- [x] Increment unread on received message (if not active channel)
- [ ] Unread count badge in sidebar
- [ ] Bold channel name for unread channels
- [ ] Scroll to first unread message on channel open
- [ ] "New messages" divider in message list
- [ ] "Mark as unread" on any message
- [ ] Total unread count in app title/favicon
- [ ] Unread mentions count separate from total unread

### 4.28 Typing Indicators
- [x] Typing users tracked per channel in store
- [x] Add/remove typing user actions
- [x] Typing indicator component in ChatArea
- [ ] Emit typing event via Socket.io when user is typing
- [ ] Debounce typing events (stop after 3s of no typing)
- [ ] Show "User is typing..." with animated dots
- [ ] Show multiple users typing ("Alice and Bob are typing")
- [ ] Typing indicator in DM conversations
- [ ] Typing indicator in threads

### 4.29 Orbit Ecosystem Integrations
- [x] `orbitIntegrations.ts` utility for cross-app linking
- [x] Atlas task reference detection in messages
- [x] TurboTick ticket detection in messages
- [x] Open Orbit app navigation utility
- [ ] Create Atlas task from message
- [ ] Create TurboTick ticket from message
- [ ] Link shared Calendar events in messages
- [ ] Link shared Meet meeting in messages
- [ ] EventBus integration for cross-app notifications
- [ ] Deep link to specific Atlas project/task
- [ ] Deep link to specific Calendar event
- [ ] Deep link to specific Mail thread

### 4.30 Writing Assistant
- [x] `writingAssistant.ts` with text analysis
- [x] Spelling/grammar/style suggestion types
- [x] Sentence completion suggestions
- [x] Smart follow-up suggestions
- [ ] Writing assistant toggle in composer settings
- [ ] Inline spelling corrections (red underline)
- [ ] Inline grammar suggestions (blue underline)
- [ ] Style improvement suggestions
- [ ] Accept/reject suggestion UI
- [ ] Accept all suggestions action
- [ ] AI tone adjustment (formal, casual, concise)
- [ ] AI message rewrite suggestion
- [ ] AI thread summary generation

### 4.31 Bots & Integrations
- [ ] Bot user type (distinguished from human users)
- [ ] Bot message rendering (with bot badge)
- [ ] Slash commands (`/remind`, `/poll`, `/giphy`)
- [ ] `/remind` — set a reminder
- [ ] `/poll` — create a simple poll in channel
- [ ] `/giphy` — search and post GIF
- [ ] `/shrug` — append shrug emoji
- [ ] Incoming webhook support (post messages from external services)
- [ ] Outgoing webhook support (trigger on message patterns)
- [ ] GitHub integration bot (PR/issue notifications)
- [ ] CI/CD integration bot (build status notifications)
- [ ] Custom bot creation interface

---

## 5. API Integration

### 5.1 Socket.io Connection
- [x] Socket.io client connection to signaling server
- [x] Socket connection URL from `VITE_SIGNALING_SERVER` env
- [ ] Auto-reconnect with exponential backoff
- [ ] Max reconnection attempts (10) with final error state
- [ ] Connection status indicator (connected/reconnecting/disconnected)
- [ ] Socket authentication (send JWT on connect)
- [ ] Socket room management (join/leave channel rooms)
- [ ] Socket event: `message:new` — receive new message
- [ ] Socket event: `message:edit` — receive edited message
- [ ] Socket event: `message:delete` — receive deleted message
- [ ] Socket event: `reaction:add` — receive new reaction
- [ ] Socket event: `reaction:remove` — receive removed reaction
- [ ] Socket event: `typing:start` — user started typing
- [ ] Socket event: `typing:stop` — user stopped typing
- [ ] Socket event: `presence:update` — user status change
- [ ] Socket event: `channel:created` — new channel created
- [ ] Socket event: `channel:updated` — channel settings changed
- [ ] Socket event: `channel:deleted` — channel removed
- [ ] Socket event: `user:joined` — user joined channel
- [ ] Socket event: `user:left` — user left channel

### 5.2 REST API Endpoints
- [x] `GET /api/initial-data` — fetch channels, users, messages on login
- [ ] `POST /api/channels` — create channel
- [ ] `PUT /api/channels/:id` — update channel settings
- [ ] `DELETE /api/channels/:id` — delete channel
- [ ] `POST /api/channels/:id/join` — join channel
- [ ] `POST /api/channels/:id/leave` — leave channel
- [ ] `GET /api/channels/:id/members` — list channel members
- [ ] `POST /api/channels/:id/invite` — invite user to channel
- [ ] `GET /api/channels/:id/messages` — paginated message history
- [ ] `POST /api/messages` — send message (REST fallback if Socket fails)
- [ ] `PUT /api/messages/:id` — edit message
- [ ] `DELETE /api/messages/:id` — delete message
- [ ] `POST /api/messages/:id/reactions` — add reaction
- [ ] `DELETE /api/messages/:id/reactions/:emoji` — remove reaction
- [ ] `POST /api/messages/:id/pin` — pin message
- [ ] `DELETE /api/messages/:id/pin` — unpin message
- [ ] `GET /api/search?q=` — search messages
- [ ] `POST /api/files/upload` — upload file
- [ ] `GET /api/files/:id` — download file (signed URL)
- [ ] `GET /api/users/me` — current user profile
- [ ] `PUT /api/users/me` — update profile
- [ ] `PUT /api/users/me/status` — update status
- [ ] `GET /api/users` — list org users
- [ ] `GET /api/notifications` — list notifications
- [ ] `PUT /api/notifications/:id/read` — mark notification read

### 5.3 Authentication Headers
- [x] Auth token from localStorage
- [x] Auth headers helper function (`getAuthHeaders`)
- [x] 401 response handling (logout + redirect)
- [ ] `X-Org-Id` header on all API requests
- [ ] Token refresh interceptor (auto-refresh before expiry)
- [ ] Request retry on 401 after token refresh
- [ ] CSRF token handling (if applicable)

### 5.4 Presence Heartbeat
- [ ] Ping server every 30s with online status
- [ ] Server timeout: mark user offline after 60s of no ping
- [ ] Resume online status after network reconnect
- [ ] Presence sync on tab focus/blur

### 5.5 WebRTC Signaling
- [x] Socket.io used for WebRTC signaling
- [x] ICE candidate exchange via Socket
- [x] SDP offer/answer exchange via Socket
- [ ] TURN server configuration for NAT traversal
- [ ] Signaling reconnection on Socket disconnect
- [ ] Graceful call teardown on signaling loss
- [ ] Multi-party call signaling (mesh or SFU)

### 5.6 Message Delivery
- [ ] Delivery receipts: sent (message reached server)
- [ ] Delivery receipts: delivered (message reached recipient client)
- [ ] Delivery receipts: read (recipient opened channel)
- [ ] Read receipt UI (checkmarks: single = sent, double = delivered, blue = read)
- [ ] Message queue for offline sending
- [ ] Offline queue replay on reconnect

---

## 6. State Management

### 6.1 Zustand Store Structure
- [x] `useStore` created with Zustand `create`
- [x] `persist` middleware for localStorage persistence
- [x] Partial persistence (messages, channels, currentUser, notifications)
- [ ] Separate slices for messages, channels, users, UI state
- [ ] Immer middleware for immutable state updates
- [ ] DevTools middleware for debugging
- [ ] Store reset on logout (clear all state)
- [ ] Store hydration indicator (loading state while rehydrating from localStorage)
- [ ] Store migration strategy (handle schema changes between versions)

### 6.2 Derived State / Selectors
- [x] `getChannelMessages(channelId)` selector
- [x] `getUserById(userId)` selector
- [x] `getUnreadCount()` selector
- [x] `getPinnedMessages(channelId)` selector
- [x] `getThreadReplies(threadId)` selector
- [ ] `getOnlineUsers()` selector
- [ ] `getChannelsByType(type)` selector
- [ ] `getUnreadMentionsCount()` selector
- [ ] `getBookmarkedMessages()` selector
- [ ] `getSearchResults(query)` selector
- [ ] Memoized selectors to prevent unnecessary re-renders

### 6.3 Optimistic Updates
- [ ] Optimistic message send (show in UI before server confirms)
- [ ] Optimistic reaction add/remove
- [ ] Optimistic pin/unpin
- [ ] Optimistic channel read marking
- [ ] Rollback on server error (revert optimistic update)
- [ ] Conflict resolution for concurrent edits

---

## 7. Performance

### 7.1 Rendering
- [ ] Virtual scroll for message list (only render visible messages)
- [ ] Virtualize channel list in sidebar (for 100+ channels)
- [ ] Memoize message items (`React.memo` with custom comparator)
- [ ] Memoize channel list items
- [ ] Avoid full message list re-render on new message (append only)
- [ ] Stable keys for message list (`message.id`)
- [ ] Use `useMemo` for filtered/sorted message computations
- [ ] Use `useCallback` for event handlers passed to child components
- [ ] Profiler: no component renders > 16ms

### 7.2 Loading & Code Splitting
- [x] Lazy load `CommandPalette` component
- [x] Lazy load `CreateChannelModal` component
- [x] Lazy load `UserSettingsModal` component
- [x] Lazy load `CallOverlay` component
- [x] Lazy load `KeyboardShortcuts` component
- [ ] Lazy load emoji picker
- [ ] Lazy load file upload/preview components
- [ ] Lazy load writing assistant
- [ ] Suspense boundaries with proper fallback UI
- [ ] Preload critical components on hover intent

### 7.3 Media & Assets
- [ ] Lazy load images (placeholder until in viewport)
- [ ] Progressive image loading (blur-up technique)
- [ ] Image compression before upload (client-side)
- [ ] Thumbnail generation for large images
- [ ] Avatar image caching (service worker or memory cache)
- [ ] Emoji sprite sheet (not individual SVGs)

### 7.4 Network
- [ ] Message pagination (load 50 at a time, infinite scroll upward)
- [ ] Channel message cache (last 50 messages per channel in memory)
- [ ] Debounce search input (300ms)
- [ ] Debounce typing indicator emission (1s)
- [ ] Request deduplication (prevent duplicate fetches)
- [ ] Stale-while-revalidate pattern for user list

### 7.5 Memory
- [ ] Clean up WebRTC peer connections on unmount
- [ ] Release MediaStreams when call ends
- [ ] Limit notification storage (200 cap — already implemented)
- [ ] Prune old messages from store (keep last 1000 per channel)
- [ ] Garbage collect detached DOM nodes (check with DevTools)

### 7.6 Bundle Size
- [ ] Bundle size audit (target < 200KB gzipped initial)
- [ ] Tree-shake unused Lucide icons
- [ ] Tree-shake unused date-fns functions
- [ ] Analyze Zustand persist middleware size
- [ ] Consider dynamic import for Socket.io (not needed until auth)
- [ ] Consider dynamic import for WebRTC service

### 7.7 Web Vitals
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] First Input Delay (FID) < 100ms
- [ ] Cumulative Layout Shift (CLS) < 0.1
- [ ] Time to Interactive (TTI) < 3.5s
- [ ] First meaningful paint < 1.5s on fast 3G

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Navigation & Structure
- [x] Skip-to-main-content link present (`App.tsx`)
- [x] Main content landmark with `id="connect-main-content"`
- [ ] Navigation landmark for sidebar (`<nav>` element)
- [ ] Complementary landmark for right panel (`<aside>`)
- [ ] Heading hierarchy: h1 for app name, h2 for sections, h3 for sub-sections
- [ ] Page title updates on view change
- [ ] Breadcrumb navigation for nested views

### 8.2 Keyboard Navigation
- [ ] Tab order follows visual layout (left → center → right)
- [ ] Focus visible indicator on all interactive elements
- [ ] Arrow key navigation through channel list
- [ ] Arrow key navigation through message list
- [ ] Arrow key navigation through member list
- [ ] Enter key activates buttons and links
- [ ] Escape key closes modals and panels
- [ ] Focus trapped within modals when open
- [ ] Focus returned to trigger when modal closes
- [ ] Focus management on channel switch
- [ ] Focus management after sending message (return to composer)
- [ ] Roving tabindex for toolbar buttons

### 8.3 Screen Reader Support
- [ ] ARIA live region for new messages (`aria-live="polite"`)
- [ ] ARIA live region for typing indicator
- [ ] ARIA live region for notification count changes
- [ ] ARIA live region for call status changes
- [ ] `aria-label` on all icon-only buttons
- [ ] `aria-label` on channel type icons (public/private/DM)
- [ ] `aria-expanded` on collapsible sidebar sections
- [ ] `aria-selected` on active channel
- [ ] `aria-current` on active sidebar view
- [ ] `role="listbox"` on channel list
- [ ] `role="option"` on channel items
- [ ] `role="log"` on message list
- [ ] `role="article"` on individual messages
- [ ] `role="status"` on typing indicator
- [ ] `role="alert"` on error messages
- [ ] `role="dialog"` on modals
- [ ] Screen reader announcement for new messages
- [ ] Screen reader announcement for reactions added
- [ ] Screen reader announcement for user join/leave

### 8.4 Forms & Inputs
- [ ] All form inputs have visible labels
- [ ] All form inputs have accessible names (label or aria-label)
- [ ] Error messages linked to inputs with `aria-describedby`
- [ ] Required fields marked with `aria-required`
- [ ] Form validation errors announced to screen readers
- [ ] Autocomplete attributes on login/signup forms

### 8.5 Color & Contrast
- [ ] All text meets 4.5:1 contrast ratio (normal text)
- [ ] All text meets 3:1 contrast ratio (large text)
- [ ] Interactive element boundaries meet 3:1 contrast
- [ ] Focus indicators meet 3:1 contrast against background
- [ ] Color is not the only indicator of status (icons/text accompany colors)
- [ ] Online status has text label in addition to colored dot
- [ ] Message priority has text label in addition to color
- [ ] Tested with color blindness simulators (protanopia, deuteranopia, tritanopia)

### 8.6 Media & Motion
- [ ] Respect `prefers-reduced-motion` for animations
- [ ] Disable auto-playing animations when reduced motion preferred
- [ ] Video calls have captions option
- [ ] Audio content has transcript option
- [ ] Images have alt text
- [ ] Decorative images have `aria-hidden="true"` and empty alt

### 8.7 Screen Reader Testing
- [ ] Tested with NVDA on Windows
- [ ] Tested with VoiceOver on macOS
- [ ] Tested with TalkBack on Android
- [ ] Tested with VoiceOver on iOS
- [ ] Automated accessibility audit with axe-core (0 violations)
- [ ] Automated accessibility audit with Lighthouse (score > 90)

---

## 9. Mobile & Responsive

### 9.1 Layout Breakpoints
- [ ] Mobile (< 640px): single-panel layout
- [ ] Tablet (640px - 1024px): two-panel layout
- [ ] Desktop (> 1024px): three-panel layout
- [ ] Sidebar hidden by default on mobile
- [ ] Right panel hidden by default on mobile/tablet

### 9.2 Mobile Navigation
- [x] Mobile menu toggle (`isMobileMenuOpen` in store)
- [x] Hamburger button to open sidebar on mobile
- [x] Close mobile menu action
- [ ] Mobile: hamburger icon in TopNav
- [ ] Mobile: sidebar slides in as overlay
- [ ] Mobile: backdrop behind sidebar overlay
- [ ] Mobile: swipe right to open sidebar
- [ ] Mobile: swipe left to close sidebar
- [ ] Mobile: bottom navigation bar
- [ ] Mobile: full-screen channel view (no sidebar)
- [ ] Mobile: back button to return to channel list

### 9.3 Mobile Chat
- [ ] Mobile: message bubbles full-width
- [ ] Mobile: message actions on long-press
- [ ] Mobile: swipe left on message for quick actions
- [ ] Mobile: composer sticks to bottom with virtual keyboard
- [ ] Mobile: composer shrinks when keyboard opens
- [ ] Mobile: emoji picker bottom sheet
- [ ] Mobile: file attachment bottom sheet
- [ ] Mobile: mention autocomplete full-width

### 9.4 Mobile Call UI
- [ ] Mobile: call UI optimized for portrait
- [ ] Mobile: call controls at bottom
- [ ] Mobile: speaker view default (not grid)
- [ ] Mobile: swipe to switch between video feeds
- [ ] Mobile: proximity sensor to turn off screen during audio call
- [ ] Mobile: call continues in background (PiP)

### 9.5 Mobile Right Panel
- [ ] Mobile: right panel opens as full-screen overlay
- [ ] Mobile: swipe down to close panel
- [ ] Mobile: thread view full-screen
- [ ] Mobile: profile view full-screen
- [ ] Mobile: members view full-screen

### 9.6 Tablet Optimizations
- [ ] Tablet: sidebar collapsed to icons by default
- [ ] Tablet: sidebar expands on hover
- [ ] Tablet: right panel as slide-over
- [ ] Tablet: landscape mode uses full three-panel layout

### 9.7 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] No hover-dependent features (have touch alternatives)
- [ ] Pull-to-refresh for message list
- [ ] Pinch-to-zoom on images
- [ ] Long press for context menus

---

## 10. Internationalization (i18n)

### 10.1 Setup
- [ ] i18n library installed (react-i18next or similar)
- [ ] Translation files structure created (`src/locales/`)
- [ ] Default locale set to English (en)
- [ ] Language detection from browser settings
- [ ] Language selection in user settings
- [ ] Language persisted in user preferences

### 10.2 Text Extraction
- [ ] All static UI text extracted to translation keys
- [ ] TopNav text strings extracted
- [ ] StreamList text strings extracted
- [ ] ChatArea text strings extracted
- [ ] MessageComposer text strings extracted
- [ ] RightPanel text strings extracted
- [ ] CallOverlay text strings extracted
- [ ] CreateChannelModal text strings extracted
- [ ] UserSettingsModal text strings extracted
- [ ] CommandPalette text strings extracted
- [ ] KeyboardShortcuts text strings extracted
- [ ] Login page text strings extracted
- [ ] Signup page text strings extracted
- [ ] Error messages extracted
- [ ] Notification messages extracted
- [ ] Empty state messages extracted
- [ ] Placeholder text extracted

### 10.3 Locale Support
- [ ] Date formatting uses locale-aware formatter
- [ ] Time formatting (12h vs 24h based on locale)
- [ ] Number formatting (decimal separator, thousands separator)
- [ ] Relative time display ("5 minutes ago" in locale)
- [ ] Pluralization rules per locale
- [ ] RTL layout support (Arabic, Hebrew)
- [ ] RTL: message bubbles mirrored
- [ ] RTL: sidebar on right side
- [ ] RTL: text direction correct

### 10.4 Translation Files
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
- [x] JWT token stored in localStorage
- [x] Token sent in Authorization header
- [x] Logout clears all stored tokens
- [ ] Token stored in httpOnly cookie (more secure than localStorage)
- [ ] PKCE flow for OAuth2 (prevent code interception)
- [ ] Token refresh before expiry
- [ ] Session timeout after inactivity
- [ ] Rate limiting on login attempts (client-side + server-side)
- [ ] CSRF protection (token or SameSite cookie)
- [ ] Org-level authorization checks on all API calls

### 11.2 Input Sanitization
- [ ] HTML sanitization on message rendering (prevent XSS)
- [ ] Markdown rendering sanitized (no raw HTML injection)
- [ ] File upload validation (MIME type + file extension)
- [ ] File name sanitization (no path traversal)
- [ ] URL validation before unfurling
- [ ] Image URL validation (prevent SSRF)
- [ ] Message content length limits
- [ ] Channel name/description sanitization

### 11.3 Data Protection
- [ ] No sensitive data in Zustand persist (no passwords, no full tokens)
- [ ] Console.log statements removed in production
- [ ] Error messages don't expose internal details
- [ ] API keys not exposed in client bundle
- [ ] Environment variables validated (no secrets in VITE_ vars)

### 11.4 Content Security
- [ ] Content Security Policy (CSP) headers configured
- [ ] Subresource Integrity (SRI) for CDN resources
- [ ] X-Frame-Options to prevent clickjacking
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured
- [ ] HTTPS enforced in production

### 11.5 WebRTC Security
- [ ] SRTP encryption for media streams (WebRTC default)
- [ ] DTLS handshake for key exchange
- [ ] TURN server with authentication
- [ ] Peer identity verification
- [ ] Call metadata not stored in browser history

### 11.6 File Security
- [ ] Virus scan on uploaded files (server-side)
- [ ] File type whitelist enforcement
- [ ] File size limits enforced (server-side)
- [ ] Signed URLs for file download (time-limited)
- [ ] File access control (only channel members can download)

---

## 12. Testing

### 12.1 Unit Tests — Utilities
- [ ] Test `cn()` utility (class merging)
- [ ] Test `getAuthContext()` — returns token and org ID
- [ ] Test `getAuthHeaders()` — returns correct headers
- [ ] Test `analyzeText()` — returns spelling/grammar suggestions
- [ ] Test `getSentenceCompletions()` — returns completions
- [ ] Test `applyAllSuggestions()` — applies corrections
- [ ] Test `applySingleSuggestion()` — applies single correction
- [ ] Test `buildSmartFollowUps()` — returns follow-up suggestions
- [ ] Test `findAtlasReferences()` — detects Atlas task mentions
- [ ] Test `findTurboTickTickets()` — detects ticket mentions
- [ ] Test `resolveCurrentUser()` — parses auth_user from localStorage
- [ ] Test `hasGateToken()` — detects stored tokens

### 12.2 Unit Tests — Store Actions
- [ ] Test `sendMessage` — adds message to store
- [ ] Test `receiveMessage` — adds message, increments unread
- [ ] Test `receiveMessage` — prevents duplicate messages
- [ ] Test `addReaction` — adds reaction to message
- [ ] Test `removeReaction` — removes reaction from message
- [ ] Test `editMessage` — updates content, sets edited flag
- [ ] Test `deleteMessage` — removes message from store
- [ ] Test `togglePinMessage` — toggles pin state
- [ ] Test `toggleBookmarkMessage` — toggles bookmark state
- [ ] Test `createChannel` — adds channel, sets as active
- [ ] Test `setActiveChannel` — updates active channel, marks read
- [ ] Test `navigateToDM` — finds existing or creates new DM
- [ ] Test `markChannelRead` — resets unread count to 0
- [ ] Test `addTypingUser` — adds user to typing list
- [ ] Test `removeTypingUser` — removes user from typing list
- [ ] Test `login` — authenticates via Gate, sets user
- [ ] Test `signup` — creates user, sets authenticated
- [ ] Test `logout` — clears tokens, sets unauthenticated
- [ ] Test `setUserStatus` — updates current user status
- [ ] Test `togglePinChannel` — toggles channel pin state

### 12.3 Unit Tests — Store Selectors
- [ ] Test `getChannelMessages` — returns filtered, sorted messages
- [ ] Test `getUserById` — returns correct user
- [ ] Test `getUnreadCount` — sums all channel unread counts
- [ ] Test `getPinnedMessages` — returns pinned messages for channel
- [ ] Test `getThreadReplies` — returns replies for thread

### 12.4 Unit Tests — Components
- [ ] Test `Avatar` — renders initials fallback
- [ ] Test `Avatar` — renders image when provided
- [ ] Test `Avatar` — shows status indicator
- [ ] Test `DateDivider` — shows "Today" for today's date
- [ ] Test `DateDivider` — shows "Yesterday" for yesterday
- [ ] Test `DateDivider` — shows formatted date for older dates
- [ ] Test `TypingIndicator` — shows single user typing
- [ ] Test `TypingIndicator` — shows multiple users typing
- [ ] Test `TypingIndicator` — hidden when no one typing
- [ ] Test `StreamItem` — renders channel icon and name
- [ ] Test `StreamItem` — shows active state when selected
- [ ] Test `StreamItem` — shows unread badge
- [ ] Test `MessageItem` — renders message content
- [ ] Test `MessageItem` — renders reactions
- [ ] Test `MessageItem` — renders attachments
- [ ] Test `MessageItem` — shows edited indicator
- [ ] Test `MessageComposer` — sends message on Enter
- [ ] Test `MessageComposer` — shows emoji picker on click
- [ ] Test `MessageComposer` — handles file attachment

### 12.5 Integration Tests
- [ ] Login flow: enter credentials → redirect to chat
- [ ] Create channel → channel appears in sidebar → send message
- [ ] Send message → message appears in chat → reaction
- [ ] Open thread → send reply → reply count increments
- [ ] Pin message → pinned messages panel shows it
- [ ] Search for message → results displayed → click to navigate
- [ ] Start DM → conversation created → send message
- [ ] Create channel modal → fill form → channel created
- [ ] User settings → change status → status updated in sidebar
- [ ] Command palette → search channel → navigate to channel

### 12.6 End-to-End Tests (Playwright)
- [ ] E2E: Login with email/password → land on chat
- [ ] E2E: Login → create channel → send message → verify in message list
- [ ] E2E: Two browsers → same channel → send message → both see it
- [ ] E2E: DM → send message → other user sees notification
- [ ] E2E: Open thread → reply → parent shows reply count
- [ ] E2E: Add reaction → verify reaction badge appears
- [ ] E2E: Pin message → open pinned panel → message visible
- [ ] E2E: Search message → results appear → click navigates
- [ ] E2E: Voice call → accept → audio connected → end call
- [ ] E2E: Video call → accept → video visible → end call
- [ ] E2E: Screen share → start → viewer sees shared screen → stop
- [ ] E2E: Command palette → search → navigate
- [ ] E2E: Keyboard shortcuts → test all documented shortcuts
- [ ] E2E: Dark mode toggle → verify all views render correctly
- [ ] E2E: Mobile viewport → sidebar toggle → chat visible

### 12.7 Visual Regression Tests
- [ ] Snapshot: Login page (light mode)
- [ ] Snapshot: Login page (dark mode)
- [ ] Snapshot: Chat area with messages (light mode)
- [ ] Snapshot: Chat area with messages (dark mode)
- [ ] Snapshot: Sidebar with channels (light mode)
- [ ] Snapshot: Sidebar with channels (dark mode)
- [ ] Snapshot: Thread panel (light mode)
- [ ] Snapshot: Thread panel (dark mode)
- [ ] Snapshot: Call overlay (light mode)
- [ ] Snapshot: Call overlay (dark mode)
- [ ] Snapshot: Command palette (light mode)
- [ ] Snapshot: Command palette (dark mode)
- [ ] Snapshot: Mobile layout (light mode)
- [ ] Snapshot: Mobile layout (dark mode)
- [ ] Snapshot: Empty states (all variants)

### 12.8 Performance Tests
- [ ] Lighthouse performance score > 90
- [ ] Bundle size under budget (< 200KB gzipped)
- [ ] Message list scroll performance (60fps with 1000 messages)
- [ ] Channel switch latency < 100ms
- [ ] Message send latency < 50ms (local)

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] All exported functions have JSDoc comments
- [ ] All exported types/interfaces have JSDoc comments
- [ ] Complex algorithms documented with inline comments
- [ ] Store actions documented with parameter descriptions
- [ ] WebRTC service methods documented
- [ ] Auth flow documented with sequence diagram

### 13.2 Developer Documentation
- [ ] README.md with project overview and getting started
- [ ] Environment variables documentation
- [ ] Development setup guide (install, run, test)
- [ ] Architecture overview (component tree, data flow)
- [ ] State management patterns used
- [ ] WebRTC integration guide
- [ ] Socket.io event documentation
- [ ] API endpoint reference
- [ ] Deployment guide

### 13.3 User Documentation
- [ ] Feature overview for end users
- [ ] Keyboard shortcuts reference
- [ ] Messaging formatting guide (markdown)
- [ ] Channel management guide
- [ ] Call and video conferencing guide
- [ ] Troubleshooting FAQ

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [ ] GitHub Actions workflow configured
- [ ] Lint check on PR
- [ ] TypeScript type check on PR
- [ ] Unit tests run on PR
- [ ] Integration tests run on PR
- [ ] E2E tests run on PR (headless browser)
- [ ] Build check on PR (verify production build succeeds)
- [ ] Bundle size check (fail if over budget)
- [ ] Accessibility audit on PR (axe-core)
- [ ] Visual regression tests on PR
- [ ] Code coverage report generated
- [ ] Code coverage threshold enforced (> 80%)

### 14.2 CD Pipeline
- [ ] Automated deployment to staging on merge to `develop`
- [ ] Automated deployment to production on merge to `main`
- [ ] Environment-specific builds (staging vs production)
- [ ] Docker image build
- [ ] Docker image pushed to registry
- [ ] Health check after deployment
- [ ] Rollback mechanism (one-click revert)
- [ ] Deployment notifications (Slack/Connect)

### 14.3 Infrastructure
- [ ] Static asset CDN configured
- [ ] Gzip/Brotli compression on serving
- [ ] Cache headers configured (immutable for hashed assets)
- [ ] Service worker for offline support
- [ ] PWA manifest configured
- [ ] Custom domain configured
- [ ] SSL/TLS certificate configured
- [ ] Error monitoring (Sentry or similar)
- [ ] Performance monitoring (real user metrics)
- [ ] Log aggregation configured

---

## 15. Backend

### 15.1 Signaling Server (Socket.io)
- [ ] Socket.io server running on configured port
- [ ] JWT authentication on socket handshake
- [ ] Room management (channel rooms)
- [ ] Message broadcast to channel room
- [ ] Typing indicator relay
- [ ] Presence tracking (heartbeat + timeout)
- [ ] Rate limiting per socket connection
- [ ] Connection logging
- [ ] Error handling and disconnect cleanup

### 15.2 REST API Server
- [ ] Express/Fastify server configured
- [ ] CORS configured for Connect frontend origin
- [ ] JWT middleware for route protection
- [ ] Org isolation middleware (X-Org-Id header)
- [ ] Request validation (Zod or Joi schemas)
- [ ] Error response format standardized
- [ ] Request logging middleware
- [ ] Rate limiting middleware

### 15.3 Database
- [ ] Database chosen (PostgreSQL recommended)
- [ ] Schema: users table
- [ ] Schema: channels table
- [ ] Schema: channel_members table
- [ ] Schema: messages table (with thread support)
- [ ] Schema: reactions table
- [ ] Schema: attachments table
- [ ] Schema: notifications table
- [ ] Schema: user_preferences table
- [ ] Indexes on frequently queried columns
- [ ] Full-text search index on messages.content
- [ ] Database migrations setup (Prisma or Knex)
- [ ] Database seeding script for development

### 15.4 File Storage
- [ ] Object storage configured (S3/MinIO/GCS)
- [ ] File upload endpoint with multipart handling
- [ ] File size limit enforcement (server-side)
- [ ] File type validation (server-side)
- [ ] Signed URL generation for downloads
- [ ] Thumbnail generation for images
- [ ] File cleanup job (delete orphaned files)

### 15.5 WebRTC Infrastructure
- [ ] STUN server accessible
- [ ] TURN server configured and running
- [ ] TURN server authentication (time-limited credentials)
- [ ] SFU (Selective Forwarding Unit) for group calls (optional)
- [ ] Recording service (server-side media capture)
- [ ] Bandwidth estimation and adaptation

### 15.6 Monitoring & Ops
- [ ] Health check endpoint (`/health`)
- [ ] Metrics endpoint (`/metrics`)
- [ ] Prometheus metrics for request latency, error rate
- [ ] Socket.io metrics (active connections, rooms, messages/sec)
- [ ] WebRTC metrics (call duration, quality scores)
- [ ] Alert rules for error rate spikes
- [ ] Alert rules for connection drops
- [ ] Log retention policy
- [ ] Backup strategy for database

---

## Appendix A: Component-Level Audit

### A.1 App.tsx — Root Component
- [x] Lazy loading for CommandPalette
- [x] Lazy loading for CreateChannelModal
- [x] Lazy loading for UserSettingsModal
- [x] Lazy loading for CallOverlay
- [x] Lazy loading for KeyboardShortcuts
- [x] Keyboard shortcut handler for `/` key
- [x] Theme toggle on mount (dark class on html)
- [x] Offline detection (navigator.onLine + events)
- [x] Unauthorized event listener
- [x] WebRTC initialization on auth
- [x] Initial data fetch on auth
- [x] Auth view toggle (login/signup)
- [x] Skip-to-main-content link
- [ ] Suspense fallback with proper loading UI (currently `null`)
- [ ] Error boundary wrapping main content
- [ ] Error boundary wrapping Suspense overlays
- [ ] Performance: profile App re-renders on state change

### A.2 TopNav.tsx — Top Navigation
- [ ] App logo/branding displayed
- [ ] Current channel name displayed
- [ ] Search button with keyboard shortcut hint
- [ ] Notification bell with unread count
- [ ] User avatar with status
- [ ] User menu dropdown (profile, settings, logout)
- [ ] Theme toggle button
- [ ] App launcher button
- [ ] Connection status indicator (Socket.io)
- [ ] Mobile hamburger menu button (< 768px)
- [ ] TopNav responsive layout (collapse items on smaller screens)
- [ ] TopNav a11y: all buttons have aria-labels
- [ ] TopNav a11y: landmark role="banner"

### A.3 StreamList.tsx — Channel Sidebar
- [ ] Sidebar sections: Pinned Channels, Channels, Direct Messages
- [ ] Sidebar view switcher: Channels, DMs, Threads, Mentions, Bookmarks, Search
- [ ] Channel search/filter input
- [ ] Create channel button
- [ ] Channel list items with icons
- [ ] DM list items with avatars
- [ ] Unread badge on channels
- [ ] Active channel highlight
- [ ] Last message preview text
- [ ] Pinned channel star indicator
- [ ] Collapse/expand sidebar
- [ ] Sidebar scroll behavior (scrollbar-thin)
- [ ] Sidebar keyboard navigation (arrow keys)
- [ ] Sidebar a11y: role="navigation"
- [ ] Sidebar a11y: aria-label="Channel list"
- [ ] Sidebar a11y: channel list role="listbox"

### A.4 ChatArea.tsx — Main Chat
- [x] Channel header with name and description
- [x] Call buttons (voice, video)
- [x] Panel toggle buttons (search, pin, members, right panel)
- [x] Message list with date dividers
- [x] Typing indicator
- [x] Message composer
- [x] Empty channel state
- [ ] Channel header: topic editing inline
- [ ] Channel header: member count display
- [ ] Message list: virtual scroll for large histories
- [ ] Message list: infinite scroll upward (load older)
- [ ] Message list: "scroll to bottom" floating button
- [ ] Message list: "New messages" banner when scrolled up
- [ ] Message list: unread divider line
- [ ] Connection indicator: show reconnecting state
- [ ] ChatArea a11y: role="log" on message list
- [ ] ChatArea a11y: aria-live on new message region

### A.5 MessageItem.tsx — Individual Message
- [ ] Message: sender avatar
- [ ] Message: sender name (clickable for profile)
- [ ] Message: timestamp
- [ ] Message: content (with markdown rendering)
- [ ] Message: reactions row
- [ ] Message: thread reply count link
- [ ] Message: attachment previews
- [ ] Message: edited indicator ("edited")
- [ ] Message: pinned indicator
- [ ] Message: bookmarked indicator
- [ ] Message hover: action bar (reply, react, pin, bookmark, more)
- [ ] Message hover: edit button (own messages)
- [ ] Message hover: delete button (own messages)
- [ ] Message: inline edit mode (textarea replaces content)
- [ ] Message: @mention highlighting
- [ ] Message: #channel link detection
- [ ] Message: URL link rendering
- [ ] Message: code block rendering with copy button
- [ ] Message: blockquote rendering
- [ ] Message: image attachment inline preview
- [ ] Message: file attachment card
- [ ] Message a11y: role="article"
- [ ] Message a11y: aria-label with sender name and timestamp

### A.6 MessageComposer.tsx — Input Area
- [x] Text input (contentEditable or textarea)
- [x] Send button
- [x] Attachment button
- [x] Emoji picker button
- [x] Mention button (@)
- [x] Formatting toolbar (bold, italic, code, list)
- [x] Writing assistant integration
- [x] Smart follow-up suggestions
- [x] Orbit integrations (Atlas, TurboTick)
- [ ] Composer: multi-line support (Shift+Enter)
- [ ] Composer: paste image from clipboard
- [ ] Composer: drag-drop file zone
- [ ] Composer: file preview before send
- [ ] Composer: mention autocomplete dropdown
- [ ] Composer: emoji autocomplete (`:smile:`)
- [ ] Composer: channel link autocomplete (`#channel`)
- [ ] Composer: slash commands (`/remind`, `/poll`)
- [ ] Composer: character count (near limit)
- [ ] Composer: draft persistence per channel
- [ ] Composer: reply indicator (when replying in thread)
- [ ] Composer a11y: aria-label="Message input"
- [ ] Composer a11y: role="textbox"

### A.7 RightPanel.tsx — Side Panel
- [ ] Panel: close button
- [ ] Panel: thread view (parent + replies + composer)
- [ ] Panel: user profile view (avatar, name, title, department, status)
- [ ] Panel: channel members list view
- [ ] Panel: search results view
- [ ] Panel: pinned messages view
- [ ] Panel: thread timeline (blocker/status/reference detection)
- [ ] Panel: profile action buttons (DM, voice call, video call)
- [ ] Panel: Orbit app links from profile (Atlas, Mail)
- [ ] Panel: resize handle (drag to resize width)
- [ ] Panel a11y: role="complementary"
- [ ] Panel a11y: aria-label based on content type

### A.8 CallOverlay.tsx — Voice/Video Call
- [ ] Incoming call: caller name + avatar
- [ ] Incoming call: accept/decline buttons
- [ ] Incoming call: ringtone audio
- [ ] Active call: local video preview
- [ ] Active call: remote video/audio stream
- [ ] Active call: participant name labels
- [ ] Active call: mute button
- [ ] Active call: camera button
- [ ] Active call: screen share button
- [ ] Active call: end call button
- [ ] Active call: call timer
- [ ] Active call: connection quality indicator
- [ ] Active call: minimizable overlay
- [ ] Active call: PiP mode
- [ ] Call status display: dialing, ringing, connecting, connected, reconnecting
- [ ] Call error handling: permission denied, connection failed
- [ ] Call cleanup on component unmount
- [ ] Call a11y: all buttons labeled
- [ ] Call a11y: status announced to screen reader

### A.9 CreateChannelModal.tsx
- [ ] Channel name input
- [ ] Channel description input
- [ ] Channel type: public/private toggle
- [ ] Create button
- [ ] Cancel button
- [ ] Form validation: name required, no special chars
- [ ] Channel name auto-format (lowercase, hyphens)
- [ ] Success: channel created, modal closes, navigates to new channel
- [ ] Modal a11y: focus trapped
- [ ] Modal a11y: role="dialog"

### A.10 UserSettingsModal.tsx
- [ ] Profile section: name, email, title, department
- [ ] Avatar section: current avatar, upload new
- [ ] Status section: status selector, custom status
- [ ] Notifications section: toggles for different notification types
- [ ] Theme section: light/dark/system selector
- [ ] Sound section: toggle notification sounds
- [ ] Language section: language selector
- [ ] Keyboard shortcuts section: view/customize shortcuts
- [ ] Save button
- [ ] Cancel button
- [ ] Settings persisted to API
- [ ] Modal a11y: focus trapped, role="dialog"

### A.11 CommandPalette.tsx
- [ ] Search input with autofocus
- [ ] Results: channels (icon + name)
- [ ] Results: users (avatar + name)
- [ ] Results: messages (content snippet + channel)
- [ ] Results: actions (icon + label)
- [ ] Category headers
- [ ] Keyboard navigation (arrow up/down)
- [ ] Enter to select result
- [ ] Escape to close
- [ ] Empty state: "No results"
- [ ] Recent items section
- [ ] Loading state while searching
- [ ] Palette a11y: role="dialog" or role="combobox"
- [ ] Palette a11y: aria-activedescendant for keyboard focus

### A.12 Login.tsx — Login Page
- [ ] Email input field
- [ ] Password input field
- [ ] Login button
- [ ] Error message display
- [ ] "Sign up" link to toggle to signup
- [ ] "Forgot password" link
- [ ] Loading state on submit
- [ ] Form validation (email format, password not empty)
- [ ] Login a11y: form labels, error linking

### A.13 Signup.tsx — Signup Page
- [ ] Name input field
- [ ] Email input field
- [ ] Password input field
- [ ] Confirm password field
- [ ] Signup button
- [ ] Error message display
- [ ] "Log in" link to toggle to login
- [ ] Password strength indicator
- [ ] Loading state on submit
- [ ] Form validation (all fields required, password match)
- [ ] Signup a11y: form labels, error linking

---

## Appendix B: WebRTC Service Audit (webrtc.ts)

### B.1 Service Initialization
- [x] Socket.io connection to signaling server
- [x] ICE server configuration (5 STUN servers)
- [x] User ID and socket ID tracking
- [x] Call state management with listeners
- [ ] TURN server integration
- [ ] Multiple ICE server fallback
- [ ] Connection timeout handling
- [ ] Socket reconnection strategy
- [ ] Service singleton pattern verified

### B.2 Call Lifecycle
- [ ] Initialize → socket connected → ready for calls
- [ ] Start call → send offer → wait for answer → connected
- [ ] Receive call → show incoming → accept → send answer → connected
- [ ] End call → teardown peer connection → cleanup streams
- [ ] Reject call → send rejection → cleanup
- [ ] Call timeout → auto-reject after 30s

### B.3 Media Management
- [ ] Get user media (audio + video)
- [ ] Handle permission denied gracefully
- [ ] Handle no camera/mic available
- [ ] Add local tracks to peer connection
- [ ] Remove tracks when muting
- [ ] Replace track when switching device
- [ ] Release all tracks on call end
- [ ] Screen capture via getDisplayMedia
- [ ] Screen capture audio support

### B.4 Peer Connection
- [ ] Create RTCPeerConnection with ICE config
- [ ] Handle ICE candidate events
- [ ] Handle ICE connection state changes
- [ ] Handle signaling state changes
- [ ] Handle track events (remote stream)
- [ ] ICE restart on connection failure
- [ ] Peer connection close and cleanup
- [ ] Multiple peer connections (for group calls)

### B.5 Signaling Events
- [ ] Socket emit: `call:initiate`
- [ ] Socket emit: `call:accept`
- [ ] Socket emit: `call:reject`
- [ ] Socket emit: `call:end`
- [ ] Socket emit: `call:ice-candidate`
- [ ] Socket emit: `call:offer`
- [ ] Socket emit: `call:answer`
- [ ] Socket on: `call:incoming`
- [ ] Socket on: `call:accepted`
- [ ] Socket on: `call:rejected`
- [ ] Socket on: `call:ended`
- [ ] Socket on: `call:ice-candidate`
- [ ] Socket on: `call:offer`
- [ ] Socket on: `call:answer`

### B.6 Channel/Room Management
- [x] Join channel room (socket emit)
- [x] Leave channel room (socket emit)
- [x] Send message via socket
- [ ] Receive message via socket
- [ ] Message acknowledgment
- [ ] Presence heartbeat via socket
- [ ] Typing indicator via socket

---

## Appendix C: Zustand Store Audit (useStore.ts)

### C.1 State Fields
- [x] `currentUser` — resolved from Gate auth
- [x] `users` — array of org users
- [x] `channels` — array of channels
- [x] `messages` — array of all messages
- [x] `activeChannelId` — currently selected channel
- [x] `sidebarView` — channels/dms/threads/search/mentions/bookmarks
- [x] `isSidebarCollapsed` — sidebar collapse state
- [x] `isMobileMenuOpen` — mobile menu state
- [x] `isRightPanelOpen` — right panel visibility
- [x] `rightPanelContent` — thread/profile/members/search/pinned
- [x] `activeThreadMessageId` — open thread
- [x] `selectedUserId` — selected user profile
- [x] `notifications` — notification array
- [x] `searchQuery` — current search
- [x] `isCommandPaletteOpen` — command palette state
- [x] `isCreateChannelOpen` — create channel modal state
- [x] `isUserSettingsOpen` — settings modal state
- [x] `isKeyboardShortcutsOpen` — shortcuts modal state
- [x] `typingUsers` — per-channel typing users map
- [x] `theme` — light/dark
- [x] `activeCall` — current call state
- [x] `incomingCall` — incoming call state
- [x] `callStatus` — call lifecycle status
- [x] `socketConnected` — socket connection state
- [x] `isAuthenticated` — auth state

### C.2 Actions Audit
- [x] `setActiveChannel` — switch channel, leave old room, join new
- [x] `setSidebarView` — change sidebar tab
- [x] `toggleSidebar` — collapse/expand
- [x] `toggleMobileMenu` — mobile menu toggle
- [x] `closeMobileMenu` — close mobile menu
- [x] `setTheme` / `toggleTheme` — theme management
- [x] `toggleKeyboardShortcuts` — shortcuts modal
- [x] `toggleRightPanel` — open/close right panel with content type
- [x] `setActiveThread` — open thread in right panel
- [x] `setSelectedUser` — open profile in right panel
- [x] `sendMessage` — create message, emit via socket
- [x] `receiveMessage` — add message, increment unread, deduplicate
- [x] `addReaction` / `removeReaction` — emoji reactions
- [x] `togglePinMessage` — pin/unpin
- [x] `toggleBookmarkMessage` — bookmark toggle
- [x] `editMessage` — update content, set edited flag
- [x] `deleteMessage` — remove from store
- [x] `setSearchQuery` — update search
- [x] `toggleCommandPalette` — command palette toggle
- [x] `setIsCreateChannelOpen` / `setIsUserSettingsOpen` — modal toggles
- [x] `createChannel` — create and switch to new channel
- [x] `markChannelRead` — reset unread count
- [x] `addSystemNotification` — add notification (max 200)
- [x] `markNotificationRead` / `markAllNotificationsRead`
- [x] `setUserStatus` — change user status
- [x] `togglePinChannel` — pin/unpin channel
- [x] `navigateToDM` — find or create DM
- [x] `addTypingUser` / `removeTypingUser` — typing state
- [x] `initializeWebRTC` — init WebRTC service
- [x] `fetchInitialData` — load data from backend
- [x] `startCall` — initiate WebRTC call
- [x] `login` / `signup` / `logout` — auth actions

---

## Appendix D: Error Handling Matrix

### D.1 Network Errors
- [ ] Socket.io disconnect → show "Reconnecting..." banner
- [ ] Socket.io reconnect → hide banner, resume operations
- [ ] Socket.io reconnect failed (max retries) → show "Connection lost" with retry button
- [ ] API fetch failed (network) → show error toast
- [ ] API fetch timeout → show timeout error toast
- [ ] API 401 Unauthorized → redirect to login
- [ ] API 403 Forbidden → show permission denied message
- [ ] API 404 Not Found → show resource not found
- [ ] API 429 Rate Limited → show "Too many requests" message
- [ ] API 500 Server Error → show "Something went wrong" with retry

### D.2 Auth Errors
- [ ] Login failed: invalid credentials → show error on login form
- [ ] Login failed: account locked → show lockout message
- [ ] Login failed: network error → show network error message
- [ ] Signup failed: email already exists → show error
- [ ] Signup failed: password too weak → show requirements
- [ ] Token expired → attempt refresh, redirect if fails
- [ ] Token corrupted → clear storage, redirect to login

### D.3 WebRTC Errors
- [ ] Camera permission denied → show instructions with settings link
- [ ] Microphone permission denied → show instructions
- [ ] No media devices → show "No camera/microphone found"
- [ ] Peer connection failed → attempt ICE restart
- [ ] ICE restart failed → end call with error message
- [ ] Socket disconnected during call → attempt reconnect
- [ ] Media stream ended unexpectedly → notify user
- [ ] Screen share cancelled by user → graceful handling (no error)
- [ ] Screen share permission denied → show message
- [ ] TURN server unreachable → warn about connection quality

### D.4 File Upload Errors
- [ ] File too large → show size limit message
- [ ] File type not allowed → show allowed types
- [ ] Upload failed (network) → show retry option
- [ ] Upload failed (server) → show error toast
- [ ] Upload cancelled by user → cleanup partial upload

### D.5 UI Errors
- [ ] Error boundary: component crash → show fallback UI
- [ ] Error boundary: log error to monitoring service
- [ ] Error boundary: "Reload" button in fallback
- [ ] Empty state: handle null/undefined data gracefully
- [ ] Loading state: show skeleton/spinner for all async operations
- [ ] Timeout: show timeout message for long operations (>10s)

---

## Appendix E: Data Flow Diagrams

### E.1 Message Send Flow
- [ ] User types in MessageComposer
- [ ] User presses Enter or clicks Send
- [ ] `sendMessage` action called in Zustand store
- [ ] Message object created with UUID
- [ ] Message added to local `messages` array (optimistic)
- [ ] Channel `lastMessage` updated
- [ ] `webrtcService.sendMessage()` emits via Socket.io
- [ ] Server receives and broadcasts to channel room
- [ ] Other clients receive via `receiveMessage`
- [ ] Server persists message to database
- [ ] If send fails: rollback local message, show error toast

### E.2 Channel Switch Flow
- [ ] User clicks channel in StreamList
- [ ] `setActiveChannel(channelId)` called
- [ ] If previous channel exists: `webrtcService.leaveChannel(oldId)`
- [ ] `webrtcService.joinChannel(newId)` — join Socket room
- [ ] `activeChannelId` updated in store
- [ ] `activeThreadMessageId` cleared
- [ ] `isMobileMenuOpen` set to false
- [ ] `markChannelRead(channelId)` called — unread count reset
- [ ] ChatArea re-renders with new channel's messages
- [ ] Scroll position reset (or restored from cache)

### E.3 Auth Flow
- [ ] User visits Connect
- [ ] `hasGateToken()` checks localStorage for existing token
- [ ] If token exists: `isAuthenticated = true`, `resolveCurrentUser()` from storage
- [ ] If no token: show Login page
- [ ] User enters credentials, clicks Login
- [ ] `login(email, password)` called
- [ ] Attempt Gate SSO token exchange (`/oauth/token`)
- [ ] If successful: store token, fetch user info, set authenticated
- [ ] If Gate unavailable: fall back to localStorage check
- [ ] On auth: `fetchInitialData()` loads channels/users/messages
- [ ] On auth: `initializeWebRTC()` connects Socket.io

---

*End of 03-CONNECT.md — Connect Team Communication App Checklist*
