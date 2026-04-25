# 04 — Meet: Video Conferencing App

> **Stack:** React 19.2.0 · Vite 7.3.1 · React Router v7 · Tailwind (orbit preset) · Socket.io · WebRTC · Framer Motion
> **Routes:** /lobby, /meeting/:meetingId, /chat/:meetingId, /participants/:meetingId, /screen-share, /recap, /mobile-active, /mobile-grid
> **Status:** ~60% feature complete
> **Views:** PreJoinLobby, ActiveMeeting, ChatPanel, ParticipantsView, ScreenShareMode, PostMeetingRecap, MobileActiveSpeaker, MobileGrid
> **Components:** MeetNavigation, MeetingNotesDrawer, NetworkQualityIndicator
> **Contexts:** AuthContext
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
- [x] React Router v7 installed for client-side routing
- [x] Socket.io-client installed for real-time signaling
- [x] Framer Motion installed for animations
- [ ] TypeScript migration (currently JSX — convert to TSX)
- [ ] ESLint configured with recommended rules
- [ ] ESLint plugin for React hooks
- [ ] ESLint plugin for accessibility (jsx-a11y)
- [ ] Prettier configured and integrated with ESLint
- [ ] Husky pre-commit hooks configured
- [ ] lint-staged configured for staged file linting
- [ ] commitlint configured for conventional commits
- [ ] `.editorconfig` present with consistent settings
- [ ] `.nvmrc` or `.node-version` file present

### 1.2 Tailwind Configuration
- [ ] `tailwind.config.js` created with orbit preset
- [ ] Orbit preset imported and applied
- [ ] `darkMode: "class"` configured
- [ ] Custom Meet-specific utilities (if any) defined
- [ ] Tailwind v3 to v4 migration evaluated
- [ ] PostCSS configuration verified

### 1.3 Path Aliases & Imports
- [ ] `@/` path alias configured in Vite
- [ ] `@/` alias configured in tsconfig/jsconfig
- [ ] Import order enforced
- [ ] Barrel exports from `@/views/index.ts`
- [ ] Barrel exports from `@/components/index.ts`

### 1.4 Environment Configuration
- [x] `VITE_MEET_BACKEND_URL` env var for backend URL
- [ ] `VITE_GATE_URL` env var for Gate auth server
- [ ] `VITE_ICE_SERVERS` env var for custom ICE server config
- [ ] `VITE_SFU_URL` env var for SFU server
- [ ] `.env.example` file with all required env vars documented
- [ ] `.env.development` with local defaults
- [ ] `.env.production` with production values
- [ ] `.env.test` with test environment values
- [ ] Environment variable validation at app start

### 1.5 Project Structure
- [x] `src/views/` — View components (PreJoinLobby, ActiveMeeting, etc.)
- [x] `src/components/` — Shared components (MeetNavigation, etc.)
- [x] `src/contexts/` — React context providers (AuthContext)
- [x] `src/utils/` — Utility functions (connectionRecovery)
- [ ] `src/hooks/` — Custom React hooks directory
- [ ] `src/services/` — API/WebRTC service layer
- [ ] `src/types/` — TypeScript type definitions
- [ ] `src/constants/` — App constants directory
- [ ] `src/api/` — API client layer directory
- [ ] `src/store/` — State management (Zustand or Context)

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
- [x] `ThemeProvider` wraps root in `App.jsx`
- [x] Google Fonts Inter removed from `index.html`
- [ ] `index.css` imports `@import "/orbit-ui/orbit-tokens.css"`
- [ ] `index.css` imports `@import "/orbit-ui/orbit-tailwind-v4.css"` (if migrating to v4)
- [ ] Configure Tailwind with orbit preset (no `tailwind.config.js` found)
- [ ] Replace all hardcoded hex colors with design token CSS variables
- [ ] Replace `bg-gray-*` with semantic tokens (`bg-surface-*`)
- [ ] Replace `text-gray-*` with semantic tokens (`text-content-*`)
- [ ] Replace `border-gray-*` with semantic tokens (`border-border-*`)
- [ ] Replace `bg-blue-600` on auth buttons with `bg-primary-600`
- [ ] Replace `hover:bg-blue-700` with `hover:bg-primary-700`
- [ ] Replace `text-red-600` error text with `text-danger-600`
- [ ] Replace hardcoded lobby form colors with semantic tokens
- [ ] Replace hardcoded meeting controls colors with semantic tokens
- [ ] Replace hardcoded focus ring styles with `focus-ring` utility class
- [ ] Migrate Material Symbols icons to Lucide React for consistency

### 2.2 Replace/Adopt Button Component
- [ ] Import `Button` from `@orbit-ui/react`
- [ ] Replace "Sign in with RM Gate" button in `AuthScreen` with `<Button>`
- [ ] Replace "Continue Local Demo" button in `AuthScreen` with `<Button>`
- [ ] Replace "New Meeting" button in `PreJoinLobby` with `<Button>`
- [ ] Replace "Join Meeting" button in `PreJoinLobby` with `<Button>`
- [ ] Replace mute/unmute toggle in `ActiveMeeting` with `<Button>`
- [ ] Replace camera on/off toggle in `ActiveMeeting` with `<Button>`
- [ ] Replace screen share button in `ActiveMeeting` with `<Button>`
- [ ] Replace hand raise button in `ActiveMeeting` with `<Button>`
- [ ] Replace end call button in `ActiveMeeting` with `<Button variant="danger">`
- [ ] Replace chat panel toggle button with `<Button>`
- [ ] Replace participants panel toggle button with `<Button>`
- [ ] Replace recording button with `<Button>`
- [ ] Replace meeting notes button with `<Button>`
- [ ] Replace "Leave meeting" button in controls with `<Button>`
- [ ] Replace "End for all" button with `<Button variant="danger">`
- [ ] Replace "Back to lobby" button in `PostMeetingRecap` with `<Button>`
- [ ] Replace "Copy recap" button with `<Button>`
- [ ] Replace "Share via Mail" button with `<Button>`
- [ ] Replace "Sync to TurboTick" button with `<Button>`
- [ ] Import `IconButton` from `@orbit-ui/react`
- [ ] Replace icon-only control buttons with `<IconButton>`
- [ ] Replace close buttons on panels with `<IconButton>`

### 2.3 Adopt Avatar Component
- [ ] Import `Avatar` from `@orbit-ui/react`
- [ ] Replace participant avatars in video grid with `<Avatar>`
- [ ] Replace participant avatars in `ParticipantsView` with `<Avatar>`
- [ ] Replace participant avatars in `ChatPanel` with `<Avatar>`
- [ ] Replace user avatar in `MeetNavigation` with `<Avatar>`
- [ ] Replace user avatar in `AuthScreen` with `<Avatar>`
- [ ] Replace participant avatars in `PostMeetingRecap` with `<Avatar>`
- [ ] Use `AvatarGroup` for meeting participant summary
- [ ] Avatar used when video is off (show initials/image)

### 2.4 Adopt Badge Component
- [ ] Import `Badge` from `@orbit-ui/react`
- [ ] Use `<Badge>` for hand-raise indicator on participant tile
- [ ] Use `<Badge>` for recording indicator (red dot + "REC")
- [ ] Use `<Badge>` for unread chat message count
- [ ] Use `<Badge>` for participant count
- [ ] Use `<Badge>` for network quality indicator
- [ ] Use `<Badge>` for mute status indicator on participant tile
- [ ] Use `<Badge>` for host indicator
- [ ] Use `<Badge>` for meeting duration

### 2.5 Adopt Tooltip Component
- [ ] Import `Tooltip` from `@orbit-ui/react`
- [ ] Add `<Tooltip>` on mute/unmute button ("Mute microphone" / "Unmute microphone")
- [ ] Add `<Tooltip>` on camera button ("Turn off camera" / "Turn on camera")
- [ ] Add `<Tooltip>` on screen share button ("Share screen" / "Stop sharing")
- [ ] Add `<Tooltip>` on hand raise button ("Raise hand" / "Lower hand")
- [ ] Add `<Tooltip>` on recording button ("Start recording" / "Stop recording")
- [ ] Add `<Tooltip>` on chat button ("Open chat")
- [ ] Add `<Tooltip>` on participants button ("View participants")
- [ ] Add `<Tooltip>` on end call button ("Leave meeting")
- [ ] Add `<Tooltip>` on meeting notes button ("Meeting notes")
- [ ] Add `<Tooltip>` on settings button ("Settings")
- [ ] Add `<Tooltip>` on device selection buttons
- [ ] Add `<Tooltip>` on network quality indicator

### 2.6 Adopt Modal Component
- [ ] Import `Modal` from `@orbit-ui/react`
- [ ] Use `<Modal>` for meeting settings dialog
- [ ] Use `<Modal>` for invite participants dialog
- [ ] Use `<Modal>` for end meeting confirmation dialog
- [ ] Use `<Modal>` for recording consent notification
- [ ] Use `<Modal>` for device permission denied dialog
- [ ] Use `<Modal>` for meeting password entry
- [ ] Use `<Modal>` for breakout room creation
- [ ] Use `<Modal>` for meeting info/share link
- [ ] Use `<Modal>` for virtual background selection
- [ ] Use `<Modal>` for feedback dialog (post-meeting)

### 2.7 Adopt Spinner Component
- [ ] Import `Spinner`, `PageLoader` from `@orbit-ui/react`
- [ ] Replace "Loading Meet..." text with `<PageLoader>`
- [ ] Use `<Spinner>` for joining meeting state
- [ ] Use `<Spinner>` for connecting to room state
- [ ] Use `<Spinner>` for recording start pending state
- [ ] Use `<Spinner>` for recap loading state
- [ ] Use `<Spinner>` for device enumeration loading

### 2.8 Adopt EmptyState Component
- [ ] Import `EmptyState` from `@orbit-ui/react`
- [ ] Use `<EmptyState>` for empty participants panel
- [ ] Use `<EmptyState>` for empty chat panel
- [ ] Use `<EmptyState>` for no recordings available
- [ ] Use `<EmptyState>` for no meeting notes
- [ ] Use `<EmptyState>` for no action items in recap
- [ ] Use `<EmptyState>` for meeting not found

### 2.9 Adopt Alert Component
- [ ] Import `Alert` from `@orbit-ui/react`
- [ ] Replace offline banner (`bg-red-500` div) with `<Alert variant="danger">`
- [ ] Use `<Alert>` for device permission error
- [ ] Use `<Alert>` for connection error
- [ ] Use `<Alert>` for browser compatibility warning
- [ ] Use `<Alert>` for meeting ended notification
- [ ] Use `<Alert>` for recording failed notification
- [ ] Use `<Alert>` for low bandwidth warning

### 2.10 Adopt Card Component
- [ ] Import `Card` from `@orbit-ui/react`
- [ ] Use `<Card>` for lobby device preview section
- [ ] Use `<Card>` for meeting info card
- [ ] Use `<Card>` for recap summary card
- [ ] Use `<Card>` for action items card in recap
- [ ] Use `<Card>` for recording card in recap
- [ ] Use `<Card>` for participant info card

### 2.11 Adopt Tabs Component
- [ ] Import `Tabs` from `@orbit-ui/react`
- [ ] Use `<Tabs>` for lobby view tabs (if applicable)
- [ ] Use `<Tabs>` for recap sections (Summary/Action Items/Recordings)
- [ ] Use `<Tabs>` for meeting notes sections

### 2.12 Adopt Skeleton Component
- [ ] Import `Skeleton`, `SkeletonText` from `@orbit-ui/react`
- [ ] Use `<Skeleton>` for loading participant tiles
- [ ] Use `<Skeleton>` for loading chat messages
- [ ] Use `<Skeleton>` for loading recap content
- [ ] Use `<SkeletonText>` for loading meeting summary text

### 2.13 Adopt Dropdown Component
- [ ] Import `Dropdown` suite from `@orbit-ui/react`
- [ ] Use `<Dropdown>` for audio device selection in lobby
- [ ] Use `<Dropdown>` for video device selection in lobby
- [ ] Use `<Dropdown>` for speaker device selection
- [ ] Use `<Dropdown>` for meeting more actions menu
- [ ] Use `<Dropdown>` for participant actions (mute, remove, spotlight)
- [ ] Use `<Dropdown>` for layout selection (grid/speaker/sidebar)
- [ ] Use `<Dropdown>` for virtual background options

### 2.14 Adopt Sidebar/Drawer Component
- [ ] Import `Drawer` from `@orbit-ui/react`
- [ ] Use `<Drawer>` for meeting notes drawer (replace `MeetingNotesDrawer.jsx`)
- [ ] Use `<Drawer>` for chat panel side drawer
- [ ] Use `<Drawer>` for participants panel side drawer
- [ ] Use `<Drawer>` for settings panel

### 2.15 Adopt Toast/Notification
- [ ] Import `useToast` from `@orbit-ui/react`
- [ ] Show toast when participant joins
- [ ] Show toast when participant leaves
- [ ] Show toast when recording starts/stops
- [ ] Show toast when hand is raised
- [ ] Show toast on connection recovery
- [ ] Show toast on meeting link copied
- [ ] Show toast on recap shared

### 2.16 Adopt Divider Component
- [ ] Import `Divider` from `@orbit-ui/react`
- [ ] Use `<Divider>` between recap sections
- [ ] Use `<Divider>` between participant groups
- [ ] Use `<Divider>` in meeting notes sections
- [ ] Use `<Divider>` in settings panel sections

### 2.17 Adopt Progress Component
- [ ] Import `Progress` from `@orbit-ui/react`
- [ ] Use `<Progress>` for recording time progress
- [ ] Use `<Progress>` for upload progress (when sharing files in chat)
- [ ] Use `<Progress>` for meeting recap generation progress

---

## 3. Dark Mode

### 3.1 Auth Screen
- [ ] Auth screen background (`bg-surface-muted`) verified dark mode
- [ ] Auth card (`bg-surface-base`) verified dark mode
- [ ] Auth card border dark mode
- [ ] Auth screen heading text dark mode
- [ ] Auth screen description text dark mode
- [ ] Sign in button dark mode
- [ ] Local demo button dark mode
- [ ] Error message text dark mode

### 3.2 Loading State
- [ ] Loading screen background dark mode
- [ ] Loading text color dark mode
- [ ] Loading spinner dark mode

### 3.3 Navigation (MeetNavigation.jsx)
- [ ] Navigation bar background dark mode
- [ ] Navigation links color dark mode
- [ ] Navigation active link indicator dark mode
- [ ] Navigation user avatar section dark mode
- [ ] Navigation meeting info section dark mode

### 3.4 Pre-Join Lobby (PreJoinLobby.jsx)
- [ ] Lobby page background dark mode
- [ ] Video preview container border dark mode
- [ ] Video preview placeholder (camera off) dark mode
- [ ] Device selector dropdowns dark mode
- [ ] Audio toggle button dark mode (active/inactive states)
- [ ] Video toggle button dark mode (active/inactive states)
- [ ] Meeting code input dark mode
- [ ] Join button dark mode
- [ ] New meeting button dark mode
- [ ] Time/date display dark mode
- [ ] Error messages dark mode
- [ ] Device error banner dark mode
- [ ] Audio level indicator dark mode
- [ ] Network quality indicator dark mode
- [ ] Lobby form labels dark mode
- [ ] Lobby tooltips dark mode

### 3.5 Active Meeting (ActiveMeeting.jsx)
- [ ] Meeting background (full page) dark mode (default dark recommended)
- [ ] Video grid container background dark mode
- [ ] Video tile border/frame dark mode
- [ ] Video tile participant name label dark mode
- [ ] Video tile mute indicator dark mode
- [ ] Video tile camera-off placeholder dark mode
- [ ] Active speaker highlight border dark mode
- [ ] Controls bar background dark mode
- [ ] Mute button active state dark mode
- [ ] Mute button inactive state dark mode
- [ ] Camera button active state dark mode
- [ ] Camera button inactive state dark mode
- [ ] Screen share button dark mode
- [ ] Hand raise button dark mode (raised state highlight)
- [ ] Recording button dark mode (recording state red indicator)
- [ ] End call button dark mode
- [ ] More options button dark mode
- [ ] Meeting timer dark mode
- [ ] Connection status meter dark mode
- [ ] Connection status labels dark mode
- [ ] "Reconnecting..." overlay dark mode
- [ ] Meeting info bar (top) dark mode

### 3.6 Chat Panel (ChatPanel.jsx)
- [ ] Chat panel background dark mode
- [ ] Chat panel header dark mode
- [ ] Chat messages list background dark mode
- [ ] Chat message bubbles (own) dark mode
- [ ] Chat message bubbles (others) dark mode
- [ ] Chat message sender name dark mode
- [ ] Chat message timestamp dark mode
- [ ] Chat input field dark mode
- [ ] Chat input placeholder dark mode
- [ ] Chat send button dark mode
- [ ] Chat empty state dark mode
- [ ] Chat system messages dark mode

### 3.7 Participants View (ParticipantsView.jsx)
- [ ] Participants panel background dark mode
- [ ] Participants panel header dark mode
- [ ] Participant row background dark mode
- [ ] Participant row hover state dark mode
- [ ] Participant name text dark mode
- [ ] Participant role badge dark mode
- [ ] Participant mute indicator dark mode
- [ ] Participant camera indicator dark mode
- [ ] Participant hand raised indicator dark mode
- [ ] "Mute All" button dark mode
- [ ] Search participants input dark mode
- [ ] Waiting room section header dark mode
- [ ] Admit/deny buttons dark mode
- [ ] Participant count badge dark mode

### 3.8 Screen Share Mode (ScreenShareMode.jsx)
- [ ] Screen share viewer background dark mode
- [ ] Screen share border/frame dark mode
- [ ] Screen share controls overlay dark mode
- [ ] Screen share participant strip (bottom) dark mode
- [ ] Screen share "You are sharing" banner dark mode
- [ ] Screen share stop button dark mode
- [ ] Screen share annotation tools dark mode

### 3.9 Post-Meeting Recap (PostMeetingRecap.jsx)
- [ ] Recap page background dark mode
- [ ] Recap header section dark mode
- [ ] Meeting title text dark mode
- [ ] Meeting metadata (date, duration, host) dark mode
- [ ] Summary section card dark mode
- [ ] Summary text content dark mode
- [ ] Action items section card dark mode
- [ ] Action item rows dark mode
- [ ] Action item checkbox dark mode
- [ ] Action item assignee badge dark mode
- [ ] Action item priority badge dark mode
- [ ] "Sync to TurboTick" button dark mode
- [ ] Recordings section card dark mode
- [ ] Recording list items dark mode
- [ ] Recording download button dark mode
- [ ] Recording playback controls dark mode
- [ ] Participants section dark mode
- [ ] Copy/share buttons dark mode
- [ ] Recap loading skeleton dark mode
- [ ] Recap error state dark mode
- [ ] "Refreshing summary" spinner dark mode

### 3.10 Meeting Notes Drawer (MeetingNotesDrawer.jsx)
- [ ] Drawer overlay background dark mode
- [ ] Drawer panel background dark mode
- [ ] Drawer header dark mode
- [ ] Notes textarea dark mode
- [ ] Notes sections (if tabbed) dark mode
- [ ] Save button dark mode
- [ ] Close button dark mode
- [ ] Include chat toggle dark mode
- [ ] Auto-sync toggle dark mode

### 3.11 Network Quality Indicator (NetworkQualityIndicator.jsx)
- [ ] Signal bars color in dark mode (green/yellow/red)
- [ ] Signal label text dark mode
- [ ] Tooltip background dark mode

### 3.12 Mobile Views
- [ ] MobileActiveSpeaker background dark mode
- [ ] MobileActiveSpeaker controls dark mode
- [ ] MobileGrid background dark mode
- [ ] MobileGrid tile borders dark mode
- [ ] MobileGrid participant labels dark mode

### 3.13 Offline Banner
- [ ] Offline banner background dark mode
- [ ] Offline banner text contrast dark mode
- [ ] Offline icon color dark mode

### 3.14 Dark Mode Testing
- [ ] Default to dark mode (meetings are typically in dark environments)
- [ ] Test dark mode toggle transition (no flash)
- [ ] Test dark mode persistence across page refresh
- [ ] Test system preference detection
- [ ] Screenshot comparison: light vs dark for all views
- [ ] Verify no hardcoded white/black colors remain
- [ ] Verify all shadows appropriate for dark mode
- [ ] Verify all borders visible in dark mode
- [ ] Verify video tiles look good on dark background
- [ ] Verify control buttons have sufficient contrast in dark mode

---

## 4. Core Features

### 4.1 Authentication
- [x] AuthContext with login, logout, isAuthenticated
- [x] Gate SSO login flow (redirect to Gate)
- [x] Local demo login fallback
- [x] OAuth callback handling
- [x] Token stored and used for API calls
- [ ] Token refresh before expiry
- [ ] Session timeout handling
- [ ] Multi-tab session sync
- [ ] Guest access (join without account, with display name)
- [ ] Meeting-specific auth (meeting password)

### 4.2 Pre-Join Lobby — Device Management
- [x] Camera preview before joining (video element)
- [x] Microphone toggle (audio enabled/disabled)
- [x] Video toggle (video enabled/disabled)
- [x] Device enumeration (audio inputs, video inputs)
- [x] Device selection persisted to sessionStorage
- [x] Preview stream management (start/stop)
- [x] Device list refresh
- [ ] Audio output (speaker) device selection
- [ ] Audio level indicator (microphone input visualizer)
- [ ] Device test: play test sound through selected speaker
- [ ] Camera resolution selection
- [ ] Microphone gain/volume adjustment
- [ ] Echo cancellation toggle
- [ ] Noise suppression toggle in lobby
- [ ] Device permissions error handling (clear instructions)
- [ ] Browser compatibility check (show warning if unsupported)
- [ ] Fallback UI when no camera/mic available

### 4.3 Pre-Join Lobby — Meeting Entry
- [x] Meeting code input field
- [x] Meeting code auto-generation
- [x] Navigate to meeting on join
- [x] Time/date display in lobby
- [x] Online/offline detection
- [ ] Join with audio muted toggle
- [ ] Join with video off toggle
- [ ] Display name editing (pre-filled from auth, editable)
- [ ] Background blur toggle in lobby
- [ ] Virtual background selection in lobby
- [ ] Meeting info display (title, host, scheduled time)
- [ ] Meeting password entry (for protected meetings)
- [ ] Waiting room notice ("Host will let you in shortly")
- [ ] Bandwidth/connection quality test before joining
- [ ] Recent meetings list (quick rejoin)
- [ ] Schedule new meeting button
- [ ] Copy meeting link button
- [ ] Share meeting link via email

### 4.4 Active Meeting — Video Grid
- [ ] Grid layout: 1 participant (full screen)
- [ ] Grid layout: 2 participants (side by side)
- [ ] Grid layout: 3-4 participants (2x2 grid)
- [ ] Grid layout: 5-6 participants (2x3 grid)
- [ ] Grid layout: 7-9 participants (3x3 grid)
- [ ] Grid layout: 10-16 participants (4x4 grid)
- [ ] Grid layout: 17-25 participants (5x5 grid with pagination)
- [ ] Participant tile: video stream rendering
- [ ] Participant tile: name label overlay (bottom)
- [ ] Participant tile: mute indicator icon
- [ ] Participant tile: camera-off avatar/initials display
- [ ] Participant tile: hand raised indicator
- [ ] Participant tile: active speaker border highlight
- [ ] Participant tile: connection quality indicator
- [ ] Participant tile: pin button (always show this participant)
- [ ] Participant tile: spotlight button (enlarge this participant)
- [ ] Self-view: local video preview (mirrored)
- [ ] Self-view: repositionable (drag to corner)
- [ ] Self-view: hide self-view option
- [ ] Grid responsive: tiles resize based on container
- [ ] Grid animation: smooth tile rearrangement on join/leave
- [ ] Video aspect ratio: 16:9 with letterboxing
- [ ] Video quality: auto-adjust based on bandwidth

### 4.5 Active Meeting — Layout Modes
- [ ] Gallery view: equal-sized tiles (default)
- [ ] Speaker view: active speaker large, others in strip
- [ ] Sidebar view: speaker large, strip on right
- [ ] Presentation view: screen share large, others small
- [ ] Focus view: single participant maximized
- [ ] Layout selector dropdown in controls
- [ ] Layout keyboard shortcut (L to cycle layouts)
- [ ] Layout persistence (remember preference)

### 4.6 Active Meeting — Audio Controls
- [x] Mute/unmute toggle (in ActiveMeeting)
- [ ] Mute keyboard shortcut: `M` key
- [ ] Push-to-talk: hold Space to unmute temporarily
- [ ] Mute indicator on own tile
- [ ] "You are muted" notification when speaking while muted
- [ ] Audio device switch during call (dropdown arrow next to mute button)
- [ ] Audio level meter (input volume visualization)
- [ ] Echo detection warning
- [ ] Audio output test (play chime through selected speaker)
- [ ] Mute all participants (host only)
- [ ] Request to unmute (host sends request to muted participant)
- [ ] Disable participant audio (host removes audio capability)

### 4.7 Active Meeting — Video Controls
- [x] Camera on/off toggle (in ActiveMeeting)
- [ ] Camera keyboard shortcut: `V` key
- [ ] Camera device switch during call
- [ ] Camera preview in settings during call
- [ ] Video quality selector (low/medium/high/auto)
- [ ] Turn off incoming video (bandwidth saving)
- [ ] Camera-off placeholder (avatar or initials)
- [ ] Camera flip (front/back on mobile)
- [ ] Disable participant video (host removes video capability)

### 4.8 Active Meeting — Screen Sharing
- [ ] Start screen sharing button
- [ ] Screen share keyboard shortcut: `Shift+S`
- [ ] Choose: entire screen, application window, browser tab
- [ ] Screen share with system audio
- [ ] Screen share layout switch (presentation mode)
- [ ] Screen share stop button (floating)
- [ ] "You are sharing your screen" banner
- [ ] Screen share viewer: full resolution, scrollable
- [ ] Screen share annotation tools overlay
- [ ] Screen share remote control (request/grant)
- [ ] Multiple simultaneous screen shares (toggle between)
- [ ] Screen share recording (included in recording)

### 4.9 Active Meeting — Hand Raising
- [ ] Raise hand button in controls
- [ ] Hand raise visual indicator on participant tile
- [ ] Hand raise animation
- [ ] Raise hand queue (host sees order)
- [ ] Lower hand button (own hand)
- [ ] Lower all hands (host only)
- [ ] Hand raise notification sound
- [ ] Hand raise ARIA announcement

### 4.10 Active Meeting — In-Meeting Chat
- [x] Chat panel view (ChatPanel.jsx)
- [ ] Open/close chat panel toggle
- [ ] Chat panel keyboard shortcut: `C` key
- [ ] Send text message in meeting chat
- [ ] Chat message: sender name, timestamp
- [ ] Chat message: emoji support
- [ ] Chat message: link detection
- [ ] Chat message: file sharing
- [ ] Chat unread badge on chat button
- [ ] Chat notification sound for new messages
- [ ] Chat history preserved during meeting
- [ ] Chat history included in meeting recap
- [ ] Chat to everyone vs private message to specific participant
- [ ] Chat reactions (react to messages)
- [ ] Chat: disable chat option (host)
- [ ] Chat: clear chat (host)

### 4.11 Active Meeting — Participants Panel
- [x] Participants list view (ParticipantsView.jsx)
- [ ] Open/close participants panel toggle
- [ ] Participants panel keyboard shortcut: `P` key
- [ ] Participant list: name, avatar, role (host/co-host/participant)
- [ ] Participant list: audio status (muted/unmuted)
- [ ] Participant list: video status (on/off)
- [ ] Participant list: hand raised indicator
- [ ] Participant list: network quality indicator
- [ ] Participant list: search/filter participants
- [ ] Participant actions (host): mute
- [ ] Participant actions (host): stop video
- [ ] Participant actions (host): make co-host
- [ ] Participant actions (host): remove from meeting
- [ ] Participant actions (host): move to waiting room
- [ ] Participant actions (host): spotlight
- [ ] Participant actions (host): pin
- [ ] "Mute all" button (host)
- [ ] "Unmute all" button (host — sends request)
- [ ] Participant count display
- [ ] Invite more participants button
- [ ] Copy invite link from participants panel

### 4.12 Active Meeting — Waiting Room
- [ ] Waiting room enabled/disabled toggle (host, before or during meeting)
- [ ] Waiting room: show pending participants to host
- [ ] Waiting room: admit individual participant
- [ ] Waiting room: admit all participants
- [ ] Waiting room: deny/reject participant
- [ ] Waiting room: customizable message for waiting participants
- [ ] Waiting room: participant sees "Waiting for host to let you in"
- [ ] Waiting room: notification sound when someone is waiting

### 4.13 Active Meeting — Recording
- [ ] Start recording button (host/co-host only)
- [ ] Stop recording button
- [ ] Recording indicator visible to all participants (red dot + "Recording")
- [ ] Recording consent notification (all participants notified)
- [ ] Recording consent dialog (participant can leave if objects)
- [ ] Recording timer display
- [ ] Pause/resume recording
- [ ] Recording includes: all video streams
- [ ] Recording includes: all audio streams
- [ ] Recording includes: screen share content
- [ ] Recording includes: chat messages (optional)
- [ ] Recording saved server-side
- [ ] Recording available in PostMeetingRecap
- [ ] Recording download link generation
- [ ] Recording playback in-app
- [ ] Recording storage management (quota)
- [ ] Recording auto-start option (meeting setting)

### 4.14 Active Meeting — Reactions
- [ ] Reaction bar (thumbs up, clap, heart, laugh, surprised, celebrate)
- [ ] Reaction animation on video tile
- [ ] Reaction floating animation over grid
- [ ] Reaction sound effect (optional)
- [ ] Reaction cooldown (prevent spam)
- [ ] Reaction visible to all participants

### 4.15 Active Meeting — Captions & Transcription
- [ ] Live captions toggle
- [ ] Captions display at bottom of meeting view
- [ ] Captions speaker identification
- [ ] Captions language selection
- [ ] Captions font size adjustment
- [ ] Full meeting transcription (AI-generated)
- [ ] Transcription saved to meeting record
- [ ] Transcription available in PostMeetingRecap
- [ ] Transcription search within meeting

### 4.16 Active Meeting — Breakout Rooms
- [ ] Create breakout rooms (host)
- [ ] Assign participants to rooms manually
- [ ] Auto-assign participants to rooms (random)
- [ ] Set breakout room duration (auto-close timer)
- [ ] Open all breakout rooms
- [ ] Close all breakout rooms (bring everyone back)
- [ ] Broadcast message to all breakout rooms
- [ ] Join any breakout room (host can hop between)
- [ ] Breakout room participant list
- [ ] Breakout room chat (separate from main)
- [ ] Ask for help button (participant signals host)

### 4.17 Active Meeting — Virtual Backgrounds
- [ ] Background blur (Gaussian blur on background)
- [ ] Preset virtual backgrounds (5-10 images)
- [ ] Custom background upload
- [ ] No background (original video)
- [ ] Background selection during meeting (settings)
- [ ] Background preview before applying
- [ ] Background processing optimization (WebGL or WASM)
- [ ] Background applied via TensorFlow.js body segmentation

### 4.18 Active Meeting — Noise Cancellation
- [ ] AI noise cancellation toggle
- [ ] Noise cancellation levels (auto/low/high)
- [ ] Noise cancellation using Web Audio API
- [ ] Noise cancellation works on incoming audio (optional)
- [ ] Noise cancellation processing indicator

### 4.19 Active Meeting — Network & Quality
- [x] Connection quality indicator (ConnectionMeter component)
- [x] Connection state resolution (SFU, socket, peer states)
- [x] Network states: green (stable), yellow (connecting), red (failed)
- [ ] Per-participant network quality indicator
- [ ] Adaptive bitrate: reduce video quality on poor connection
- [ ] Adaptive bitrate: switch to audio-only on very poor connection
- [ ] Reconnection on network drop (auto-rejoin)
- [ ] "Reconnecting..." overlay during recovery
- [ ] Connection recovery utility (`connectionRecovery.js`)
- [ ] Bandwidth usage display
- [ ] Packet loss percentage display
- [ ] Jitter display
- [ ] Latency display

### 4.20 Active Meeting — Meeting Controls
- [ ] Meeting timer display (duration since start)
- [ ] Meeting lock: prevent new participants from joining
- [ ] Meeting unlock
- [ ] Meeting password change during meeting
- [ ] End meeting: leave for self
- [ ] End meeting: end for all (host only)
- [ ] End meeting confirmation dialog
- [ ] Meeting info display (title, meeting ID, host)
- [ ] Meeting link copy button
- [ ] Meeting settings during call (open settings modal)
- [ ] Full-screen toggle
- [ ] PiP (Picture-in-Picture) mode

### 4.21 Active Meeting — Polls & Q&A
- [ ] Create poll (host): question + options
- [ ] Launch poll to all participants
- [ ] Vote on poll (participant)
- [ ] Poll results display (live, after voting)
- [ ] Close poll
- [ ] Share poll results
- [ ] Q&A panel: submit question
- [ ] Q&A panel: upvote questions
- [ ] Q&A panel: answer question (host)
- [ ] Q&A panel: dismiss question (host)
- [ ] Q&A included in meeting recap

### 4.22 Active Meeting — Whiteboard
- [ ] Open whiteboard during meeting
- [ ] Drawing tools: pen, highlighter, eraser, shapes, text
- [ ] Color and size selection
- [ ] Collaborative whiteboard (all participants draw)
- [ ] Whiteboard zoom/pan
- [ ] Whiteboard pages (multiple canvases)
- [ ] Save whiteboard as image
- [ ] Whiteboard included in meeting recap

### 4.23 Active Meeting — RTMP Streaming
- [ ] Start RTMP stream (host)
- [ ] RTMP URL + stream key input
- [ ] Stream to YouTube Live
- [ ] Stream to Twitch
- [ ] Stream to custom RTMP endpoint
- [ ] Streaming indicator visible to all
- [ ] Stop stream
- [ ] Stream quality selection

### 4.24 Post-Meeting Recap (PostMeetingRecap.jsx)
- [x] Recap page with meeting snapshot loading
- [x] Meeting ID from URL params or sessionStorage
- [x] Backend URL from environment variable
- [x] Recordings list loading
- [x] "Refresh summary" action
- [x] "Refresh action items" action
- [x] "Sync to TurboTick" per action item
- [x] "Sync all action items" action
- [x] Copy recap to clipboard
- [ ] Auto-generated meeting summary (AI)
- [ ] Action items extracted from transcript (AI)
- [ ] Meeting duration display
- [ ] Participant list display
- [ ] Meeting start/end time display
- [ ] Meeting recording playback
- [ ] Meeting recording download
- [ ] Meeting transcript view
- [ ] Share recap via Connect message
- [ ] Share recap via Mail email
- [ ] Share recap to Calendar event
- [ ] Export recap as PDF
- [ ] Recap feedback (thumbs up/down on AI summary)
- [ ] Edit action items (correct AI extraction)
- [ ] Create follow-up meeting from recap
- [ ] Recap accessible from meeting history

### 4.25 Meeting History & Dashboard
- [ ] Meeting history list (past meetings)
- [ ] Meeting history: title, date, duration, participants
- [ ] Meeting history: search by title/participant
- [ ] Meeting history: filter by date range
- [ ] Meeting history: link to recap for each meeting
- [ ] Upcoming meetings list (from Calendar integration)
- [ ] Quick start: new instant meeting
- [ ] Quick start: schedule meeting
- [ ] Meeting templates (recurring meeting settings)

### 4.26 Calendar Integration
- [ ] Fetch upcoming meetings from Calendar app
- [ ] Display upcoming meetings in lobby/dashboard
- [ ] Auto-create Calendar event when scheduling meeting
- [ ] Calendar event includes Meet link
- [ ] Join meeting from Calendar event
- [ ] Sync meeting recap to Calendar event
- [ ] Calendar reminder triggers Meet pre-join

### 4.27 Meeting Notes Drawer
- [x] MeetingNotesDrawer component
- [ ] Open/close notes drawer during meeting
- [ ] Manual note taking (rich text)
- [ ] Auto-generated notes from transcript
- [ ] Include chat messages toggle
- [ ] Auto-sync to TurboTick toggle
- [ ] Save notes to meeting record
- [ ] Notes available in post-meeting recap
- [ ] Notes collaboration (multiple note-takers)

### 4.28 Keyboard Shortcuts
- [ ] `M` — toggle mute
- [ ] `V` — toggle camera
- [ ] `Shift+S` — toggle screen share
- [ ] `C` — toggle chat panel
- [ ] `P` — toggle participants panel
- [ ] `H` — toggle hand raise
- [ ] `R` — toggle recording (host)
- [ ] `L` — cycle layout modes
- [ ] `F` — toggle fullscreen
- [ ] `Escape` — close panels/modals
- [ ] `Space` — push-to-talk (hold)
- [ ] `Ctrl+D` — leave meeting
- [ ] `?` — show keyboard shortcuts help
- [ ] Keyboard shortcuts help dialog
- [ ] Keyboard shortcuts configurable in settings

---

## 5. API Integration

### 5.1 Meeting API
- [ ] `POST /api/meetings` — create new meeting
- [ ] `GET /api/meetings/:id` — get meeting details
- [ ] `PUT /api/meetings/:id` — update meeting settings
- [ ] `DELETE /api/meetings/:id` — cancel/delete meeting
- [ ] `GET /api/meetings` — list user's meetings (upcoming + past)
- [ ] `POST /api/meetings/:id/join` — join meeting (get room token)
- [ ] `POST /api/meetings/:id/leave` — leave meeting
- [ ] `POST /api/meetings/:id/end` — end meeting for all
- [ ] `GET /api/meetings/:id/token` — get WebRTC/SFU room token
- [ ] `POST /api/meetings/:id/invite` — send meeting invite

### 5.2 Participant API
- [ ] `GET /api/meetings/:id/participants` — list participants
- [ ] `PUT /api/meetings/:id/participants/:userId` — update participant role
- [ ] `DELETE /api/meetings/:id/participants/:userId` — remove participant
- [ ] `POST /api/meetings/:id/participants/:userId/mute` — force mute
- [ ] `POST /api/meetings/:id/waiting-room/admit` — admit from waiting room
- [ ] `POST /api/meetings/:id/waiting-room/deny` — deny from waiting room

### 5.3 Recording API
- [x] Recordings fetched in PostMeetingRecap
- [ ] `POST /api/meetings/:id/recording/start` — start recording
- [ ] `POST /api/meetings/:id/recording/stop` — stop recording
- [ ] `GET /api/meetings/:id/recordings` — list recordings
- [ ] `GET /api/recordings/:id/download` — download recording (signed URL)
- [ ] `DELETE /api/recordings/:id` — delete recording

### 5.4 Recap API
- [x] Recap snapshot fetched from backend
- [x] Summary refresh endpoint
- [x] Action items refresh endpoint
- [x] Sync action items to TurboTick
- [ ] `GET /api/meetings/:id/recap` — get meeting recap
- [ ] `POST /api/meetings/:id/recap/regenerate` — regenerate AI summary
- [ ] `GET /api/meetings/:id/transcript` — get full transcript
- [ ] `PUT /api/meetings/:id/recap/actions/:actionId` — edit action item
- [ ] `POST /api/meetings/:id/recap/share` — share recap via email/Connect

### 5.5 WebRTC Signaling
- [x] Socket.io used for peer signaling
- [x] ICE servers configured (STUN: stun.l.google.com)
- [x] SDP offer/answer exchange
- [x] ICE candidate exchange
- [x] Peer connection state tracking
- [ ] TURN server configuration for NAT traversal
- [ ] SFU server connection (for large meetings)
- [ ] Signaling reconnection on disconnect
- [ ] Graceful call teardown on signaling loss
- [ ] SFU token authentication
- [ ] Simulcast support (multiple quality layers)

### 5.6 Authentication Headers
- [x] Bearer token in Authorization header
- [x] X-Org-Id header from user context
- [ ] Token refresh interceptor
- [ ] 401 redirect to login
- [ ] Request retry on token refresh

### 5.7 Real-time Events
- [ ] Socket event: `participant:joined` — new participant
- [ ] Socket event: `participant:left` — participant left
- [ ] Socket event: `participant:muted` — participant muted
- [ ] Socket event: `participant:unmuted` — participant unmuted
- [ ] Socket event: `participant:video-on` — camera turned on
- [ ] Socket event: `participant:video-off` — camera turned off
- [ ] Socket event: `participant:hand-raised` — hand raised
- [ ] Socket event: `participant:hand-lowered` — hand lowered
- [ ] Socket event: `meeting:recording-started` — recording began
- [ ] Socket event: `meeting:recording-stopped` — recording ended
- [ ] Socket event: `meeting:ended` — meeting ended by host
- [ ] Socket event: `chat:message` — new chat message
- [ ] Socket event: `reaction` — participant reaction

---

## 6. State Management

### 6.1 Current State
- [x] AuthContext for authentication state
- [x] Local component state in each view
- [x] sessionStorage for device preferences
- [ ] Centralized state management (Zustand recommended)
- [ ] Global meeting state store
- [ ] Participant state store
- [ ] Device state store
- [ ] Chat state store
- [ ] UI state store (panels, modals)

### 6.2 Meeting State
- [ ] Meeting ID
- [ ] Meeting title
- [ ] Meeting status (lobby/active/ended)
- [ ] Meeting host info
- [ ] Meeting settings (waiting room, recording, lock)
- [ ] Meeting start time
- [ ] Meeting duration (calculated)

### 6.3 Participant State
- [ ] Local participant (self) info
- [ ] Remote participants list
- [ ] Per-participant: audio muted state
- [ ] Per-participant: video on/off state
- [ ] Per-participant: screen sharing state
- [ ] Per-participant: hand raised state
- [ ] Per-participant: speaking state (active speaker)
- [ ] Per-participant: network quality
- [ ] Per-participant: role (host/co-host/participant)

### 6.4 Media State
- [ ] Local audio stream
- [ ] Local video stream
- [ ] Local screen share stream
- [ ] Remote streams map (peerId → stream)
- [ ] Selected audio input device
- [ ] Selected video input device
- [ ] Selected audio output device
- [ ] Available devices list

### 6.5 UI State
- [ ] Active layout mode
- [ ] Chat panel open/closed
- [ ] Participants panel open/closed
- [ ] Notes drawer open/closed
- [ ] Settings modal open/closed
- [ ] Fullscreen mode
- [ ] PiP mode
- [ ] Active panel (which side panel is open)

---

## 7. Performance

### 7.1 Rendering
- [ ] Memoize participant tiles (`React.memo`)
- [ ] Avoid re-rendering all tiles when one participant changes
- [ ] Stable keys for participant list
- [ ] Virtualize participant list for large meetings (50+)
- [ ] Throttle video grid layout recalculations
- [ ] Use `requestAnimationFrame` for smooth animations

### 7.2 Loading & Code Splitting
- [ ] Lazy load ActiveMeeting view (only when navigating to meeting)
- [ ] Lazy load ChatPanel view
- [ ] Lazy load ParticipantsView
- [ ] Lazy load ScreenShareMode
- [ ] Lazy load PostMeetingRecap
- [ ] Lazy load MobileActiveSpeaker
- [ ] Lazy load MobileGrid
- [ ] Lazy load virtual background processing library
- [ ] Lazy load noise cancellation library
- [ ] Lazy load whiteboard component
- [ ] Suspense boundaries with loading fallbacks
- [ ] Preload meeting view on lobby "Join" hover

### 7.3 Media Performance
- [ ] Video resolution adapts to tile size (small tile = low res)
- [ ] Simulcast: send multiple quality layers
- [ ] Selective subscription: only receive video of visible tiles
- [ ] Audio: disable processing on muted streams
- [ ] Canvas-based virtual background (GPU accelerated)
- [ ] WebGL background processing (avoid CPU bottleneck)
- [ ] MediaStream track cleanup on unmount
- [ ] Peer connection cleanup on participant leave

### 7.4 Network
- [ ] Bandwidth estimation and adaptive quality
- [ ] Reconnection with exponential backoff
- [ ] Connection timeout (fail fast after 15s)
- [ ] Stale connection detection (ICE restart)
- [ ] Reduce polling frequency when tab is in background
- [ ] Efficient signaling (batch messages when possible)

### 7.5 Memory
- [ ] Release MediaStreams when leaving meeting
- [ ] Release peer connections on unmount
- [ ] Clear chat history on meeting end (if not needed)
- [ ] Limit recording buffer size
- [ ] Monitor memory usage during long meetings

### 7.6 Bundle Size
- [ ] Bundle size audit (target < 150KB gzipped initial)
- [ ] Tree-shake unused Socket.io features
- [ ] Tree-shake unused Framer Motion features
- [ ] Analyze WebRTC adapter polyfill size
- [ ] Dynamic import for heavy libraries (TensorFlow.js, etc.)

### 7.7 Web Vitals
- [ ] LCP < 2.5s (lobby load)
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] TTI < 3.5s
- [ ] Time to first video frame < 3s after joining

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Navigation & Structure
- [x] Skip-to-main-content link present (`App.jsx`)
- [x] Main content landmark with `id="meet-main-content"`
- [ ] Navigation landmark for MeetNavigation
- [ ] Heading hierarchy: h1 for page title, h2 for sections
- [ ] Page title updates on route change (implemented in `MeetRoutesContent`)
- [ ] Breadcrumb for meeting > chat > participants navigation

### 8.2 Keyboard Navigation
- [ ] Tab order follows visual layout
- [ ] Focus visible indicator on all interactive elements
- [ ] Arrow key navigation through control bar
- [ ] Arrow key navigation through participant tiles
- [ ] Enter key activates buttons
- [ ] Escape key closes panels/modals
- [ ] Focus trapped within modals
- [ ] Focus returned to trigger on modal/panel close
- [ ] Keyboard shortcuts for all major actions
- [ ] Roving tabindex for control bar buttons

### 8.3 Screen Reader Support
- [ ] All control buttons have `aria-label` (not just icons)
- [ ] `aria-label` on mute: "Mute microphone" / "Unmute microphone"
- [ ] `aria-label` on camera: "Turn off camera" / "Turn on camera"
- [ ] `aria-label` on screen share: "Share screen" / "Stop sharing"
- [ ] `aria-pressed` on toggle buttons (mute, camera, hand raise)
- [ ] ARIA live region for participant join/leave
- [ ] ARIA live region for chat messages
- [ ] ARIA live region for hand raise notifications
- [ ] ARIA live region for recording status changes
- [ ] `role="status"` on connection quality indicator
- [ ] `role="log"` on chat message list
- [ ] `role="dialog"` on modals
- [ ] `role="grid"` on video grid
- [ ] Participant name read by screen reader on focus

### 8.4 Forms & Inputs
- [ ] Lobby: meeting code input has visible label
- [ ] Lobby: device selectors have visible labels
- [ ] Chat: message input has accessible name
- [ ] All form validation errors announced
- [ ] Required fields marked

### 8.5 Color & Contrast
- [ ] Control buttons meet 3:1 contrast
- [ ] Text labels meet 4.5:1 contrast
- [ ] Mute indicator not color-only (icon changes shape)
- [ ] Network quality not color-only (label text + bars)
- [ ] Recording indicator not color-only (text "REC" + icon)
- [ ] Hand raise not color-only (icon visible)

### 8.6 Captions & Alternatives
- [ ] Live captions for deaf/HoH participants
- [ ] Captions positioned to avoid overlapping controls
- [ ] Captions font size adjustable
- [ ] Audio descriptions for visual content
- [ ] Screen share has verbal description by presenter

### 8.7 Testing
- [ ] Tested with NVDA on Windows
- [ ] Tested with VoiceOver on macOS
- [ ] Tested with TalkBack on Android
- [ ] Automated axe-core audit (0 violations)
- [ ] Lighthouse accessibility score > 90

---

## 9. Mobile & Responsive

### 9.1 Layout Breakpoints
- [ ] Mobile (< 640px): optimized single-panel layout
- [ ] Tablet (640px - 1024px): adjusted grid layout
- [ ] Desktop (> 1024px): full multi-panel layout

### 9.2 Mobile Pre-Join Lobby
- [ ] Mobile: video preview fills width
- [ ] Mobile: controls below video preview
- [ ] Mobile: device selectors as bottom sheet
- [ ] Mobile: meeting code input full width
- [ ] Mobile: join button full width
- [ ] Mobile: virtual keyboard doesn't overlap form

### 9.3 Mobile Active Meeting
- [x] MobileActiveSpeaker view (speaker + small self view)
- [x] MobileGrid view (2x2 or 3x3 grid)
- [ ] Mobile: speaker view as default layout
- [ ] Mobile: swipe to switch between speaker view and grid
- [ ] Mobile: controls at bottom of screen
- [ ] Mobile: simplified controls (mute, camera, end as primary)
- [ ] Mobile: more actions in overflow menu
- [ ] Mobile: tap to show/hide controls
- [ ] Mobile: portrait mode layout
- [ ] Mobile: landscape mode layout
- [ ] Mobile: PiP when leaving app
- [ ] Mobile: proximity sensor dims screen during audio call
- [ ] Mobile: double-tap to zoom on participant
- [ ] Mobile: swipe up for participants panel
- [ ] Mobile: swipe left for chat panel

### 9.4 Mobile Chat Panel
- [ ] Mobile: chat opens as full-screen overlay
- [ ] Mobile: chat input sticks above keyboard
- [ ] Mobile: swipe down to close chat
- [ ] Mobile: chat notification badge visible

### 9.5 Mobile Participants Panel
- [ ] Mobile: participants opens as full-screen overlay
- [ ] Mobile: swipe down to close
- [ ] Mobile: participant actions via long press

### 9.6 Mobile Post-Meeting Recap
- [ ] Mobile: recap sections stacked vertically
- [ ] Mobile: action items full width
- [ ] Mobile: recording playback full width
- [ ] Mobile: share/copy buttons full width

### 9.7 Tablet Optimizations
- [ ] Tablet: side-by-side chat + video
- [ ] Tablet: floating participant panel
- [ ] Tablet: landscape grid optimized for 10+ participants

### 9.8 Touch Interactions
- [ ] Touch targets minimum 44x44px
- [ ] Swipe gestures for navigation
- [ ] Long press for context menus
- [ ] Pinch-to-zoom on screen share content
- [ ] No hover-dependent features

---

## 10. Internationalization (i18n)

### 10.1 Setup
- [ ] i18n library installed (react-i18next)
- [ ] Translation files structure (`src/locales/`)
- [ ] Default locale: English
- [ ] Language detection from browser
- [ ] Language selector in settings

### 10.2 Text Extraction
- [ ] AuthScreen text strings extracted
- [ ] PreJoinLobby text strings extracted
- [ ] ActiveMeeting text strings extracted
- [ ] ChatPanel text strings extracted
- [ ] ParticipantsView text strings extracted
- [ ] ScreenShareMode text strings extracted
- [ ] PostMeetingRecap text strings extracted
- [ ] MeetNavigation text strings extracted
- [ ] MeetingNotesDrawer text strings extracted
- [ ] Control button labels extracted
- [ ] Error messages extracted
- [ ] Notification messages extracted
- [ ] Placeholder text extracted
- [ ] Dialog/modal text extracted

### 10.3 Locale Support
- [ ] Date/time formatting locale-aware
- [ ] Duration formatting locale-aware
- [ ] Number formatting locale-aware
- [ ] RTL layout support
- [ ] Meeting recap in selected language (AI-generated)

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
- [x] JWT token used for API calls
- [x] Token stored and retrieved from AuthContext
- [ ] Token refresh before expiry
- [ ] Meeting-level authorization (host vs participant permissions)
- [ ] Guest access with limited permissions
- [ ] Meeting password protection
- [ ] Rate limiting on meeting creation
- [ ] Rate limiting on join attempts

### 11.2 WebRTC Security
- [ ] SRTP encryption for all media streams (WebRTC default)
- [ ] DTLS key exchange
- [ ] TURN server with time-limited credentials
- [ ] Peer identity verification via signaling server
- [ ] No direct IP exposure (TURN relay mode option)
- [ ] WebRTC security headers

### 11.3 Meeting Security
- [ ] Meeting lock (prevent new joins)
- [ ] Waiting room (approve before joining)
- [ ] Meeting password
- [ ] Unique meeting IDs (not guessable)
- [ ] Meeting expiry (links expire after meeting ends)
- [ ] Host-only controls enforced server-side
- [ ] Remove participant enforced server-side
- [ ] Recording requires host permission

### 11.4 Content Security
- [ ] Chat messages sanitized (no XSS)
- [ ] File uploads validated (type, size)
- [ ] Screen share permission verified
- [ ] CSP headers configured
- [ ] No sensitive data in URL params
- [ ] Meeting recordings encrypted at rest

### 11.5 Privacy
- [ ] Recording consent notification mandatory
- [ ] Camera/mic permission request with clear explanation
- [ ] No recording without participant awareness
- [ ] Meeting data retention policy
- [ ] Participant data not exposed to other participants unnecessarily
- [ ] IP addresses not logged unnecessarily

---

## 12. Testing

### 12.1 Unit Tests — Utilities
- [ ] Test `generateMeetingCode()` — unique, correct format
- [ ] Test `readBoolPref()` — reads from sessionStorage correctly
- [ ] Test `formatDateTime()` — formats dates correctly
- [ ] Test `formatDuration()` — formats seconds to human-readable
- [ ] Test `resolveConnectionSignalState()` — returns correct level/label
- [ ] Test `shouldInitiateOffer()` — deterministic initiator selection
- [ ] Test `normalizeConnectionState()` — normalizes state strings
- [ ] Test connection recovery utility functions

### 12.2 Unit Tests — Components
- [ ] Test `ConnectionMeter` — renders correct bars for signal level
- [ ] Test `StreamVideo` — renders video element with stream
- [ ] Test `NetworkQualityIndicator` — shows correct quality state
- [ ] Test `MeetNavigation` — renders links, highlights active route
- [ ] Test `MeetingNotesDrawer` — opens/closes, saves notes
- [ ] Test `AuthScreen` — renders login buttons, handles click

### 12.3 Unit Tests — Views
- [ ] Test `PreJoinLobby` — renders device preview, selectors
- [ ] Test `PreJoinLobby` — generates meeting code
- [ ] Test `PreJoinLobby` — navigates to meeting on join
- [ ] Test `ActiveMeeting` — renders video grid
- [ ] Test `ActiveMeeting` — mute/unmute toggle
- [ ] Test `ActiveMeeting` — camera toggle
- [ ] Test `ChatPanel` — renders messages
- [ ] Test `ChatPanel` — sends message
- [ ] Test `ParticipantsView` — renders participant list
- [ ] Test `ScreenShareMode` — renders screen share view
- [ ] Test `PostMeetingRecap` — loads and displays recap
- [ ] Test `PostMeetingRecap` — handles loading/error states
- [ ] Test `MobileActiveSpeaker` — renders speaker view
- [ ] Test `MobileGrid` — renders grid view

### 12.4 Unit Tests — Auth Context
- [ ] Test `AuthProvider` — provides auth state
- [ ] Test `login()` — initiates OAuth flow
- [ ] Test `loginLocalDemo()` — sets demo user
- [ ] Test `handleCallback()` — processes OAuth callback
- [ ] Test `logout()` — clears auth state
- [ ] Test `isAuthenticated` — reflects token presence

### 12.5 Integration Tests
- [ ] Auth flow: login → redirect → lobby
- [ ] Lobby → join → navigate to active meeting
- [ ] Active meeting: mute → unmute → verify audio state
- [ ] Active meeting: camera toggle → verify video state
- [ ] Active meeting: open chat → send message → message appears
- [ ] Active meeting: open participants → verify list
- [ ] Active meeting: end meeting → redirect to recap
- [ ] Recap: load data → display summary and action items
- [ ] Recap: sync action item to TurboTick
- [ ] Recap: copy recap to clipboard
- [ ] Device selection: change device → preview updates

### 12.6 End-to-End Tests (Playwright)
- [ ] E2E: Login → land on lobby
- [ ] E2E: Create meeting → join → land on active meeting
- [ ] E2E: Two browsers → same meeting → see each other's video
- [ ] E2E: Two browsers → one mutes → other sees mute indicator
- [ ] E2E: Two browsers → send chat message → both see it
- [ ] E2E: Screen share → viewer sees shared screen
- [ ] E2E: Hand raise → host sees raised hand
- [ ] E2E: End meeting → both redirected to recap
- [ ] E2E: Recording → start → indicator shown → stop → recording available
- [ ] E2E: Waiting room → guest waits → host admits → guest joins
- [ ] E2E: Mobile viewport → verify mobile layout renders
- [ ] E2E: Dark mode toggle → verify all views
- [ ] E2E: Device selection → verify preview updates
- [ ] E2E: Network disconnect → reconnection → meeting continues

### 12.7 Visual Regression Tests
- [ ] Snapshot: Auth screen (light mode)
- [ ] Snapshot: Auth screen (dark mode)
- [ ] Snapshot: Pre-join lobby (light mode)
- [ ] Snapshot: Pre-join lobby (dark mode)
- [ ] Snapshot: Active meeting — 1 participant
- [ ] Snapshot: Active meeting — 4 participants grid
- [ ] Snapshot: Active meeting — 9 participants grid
- [ ] Snapshot: Active meeting — speaker view
- [ ] Snapshot: Screen share mode
- [ ] Snapshot: Chat panel
- [ ] Snapshot: Participants panel
- [ ] Snapshot: Post-meeting recap
- [ ] Snapshot: Mobile speaker view
- [ ] Snapshot: Mobile grid view
- [ ] Snapshot: Meeting controls bar
- [ ] Snapshot: All views in dark mode

### 12.8 Performance Tests
- [ ] Lighthouse performance score > 85
- [ ] Bundle size under budget
- [ ] Lobby load time < 2s
- [ ] Time to first video frame < 3s
- [ ] Video grid 60fps with 9 participants
- [ ] Memory usage stable during 1-hour meeting
- [ ] CPU usage < 30% during audio-only call

### 12.9 WebRTC Tests
- [ ] Peer connection establishment (two peers)
- [ ] ICE candidate gathering
- [ ] SDP offer/answer exchange
- [ ] Audio stream flow verification
- [ ] Video stream flow verification
- [ ] Screen share stream flow
- [ ] Reconnection after ICE restart
- [ ] TURN relay fallback test
- [ ] Simulcast quality layers test

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] All components have JSDoc/prop documentation
- [ ] Complex WebRTC logic documented with comments
- [ ] Socket.io event handlers documented
- [ ] Connection state machine documented
- [ ] Device management flow documented

### 13.2 Developer Documentation
- [ ] README.md with setup instructions
- [ ] Environment variables documentation
- [ ] Architecture overview (component tree, data flow)
- [ ] WebRTC integration guide
- [ ] Socket.io signaling protocol documentation
- [ ] Meeting lifecycle documentation
- [ ] Device management guide
- [ ] Deployment guide

### 13.3 User Documentation
- [ ] Meeting creation guide
- [ ] Joining a meeting guide
- [ ] In-meeting controls reference
- [ ] Keyboard shortcuts reference
- [ ] Troubleshooting (camera/mic issues)
- [ ] Browser compatibility matrix

---

## 14. Deployment & CI/CD

### 14.1 CI Pipeline
- [ ] GitHub Actions workflow configured
- [ ] Lint check on PR
- [ ] TypeScript type check on PR (after migration)
- [ ] Unit tests on PR
- [ ] Integration tests on PR
- [ ] E2E tests on PR (headless browser with mock WebRTC)
- [ ] Build check on PR
- [ ] Bundle size check
- [ ] Accessibility audit on PR
- [ ] Visual regression on PR

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
- [ ] TURN server infrastructure
- [ ] SFU server infrastructure (for large meetings)

---

## 15. Backend

### 15.1 Meeting Service
- [ ] Meeting CRUD API (Express/Fastify)
- [ ] Meeting ID generation (unique, URL-safe)
- [ ] Meeting settings storage (waiting room, recording, lock)
- [ ] Meeting scheduling (date/time, recurring)
- [ ] Meeting participant tracking
- [ ] Meeting state management (scheduled → active → ended)
- [ ] Meeting expiry and cleanup

### 15.2 Signaling Server
- [ ] Socket.io server for WebRTC signaling
- [ ] JWT authentication on connection
- [ ] Room management (meeting rooms)
- [ ] SDP relay (offer/answer forwarding)
- [ ] ICE candidate relay
- [ ] Participant join/leave events
- [ ] Mute/camera state relay
- [ ] Hand raise relay
- [ ] Chat message relay
- [ ] Reaction relay
- [ ] Rate limiting per connection
- [ ] Connection logging

### 15.3 SFU (Selective Forwarding Unit)
- [ ] SFU server running (LiveKit, Janus, or Mediasoup)
- [ ] Room creation/destruction
- [ ] Track publishing (audio, video, screen share)
- [ ] Track subscription management
- [ ] Simulcast support
- [ ] Adaptive bitrate forwarding
- [ ] Recording integration (server-side)
- [ ] SFU health monitoring
- [ ] SFU horizontal scaling

### 15.4 Recording Service
- [ ] Server-side recording pipeline
- [ ] Composite recording (all participants in one video)
- [ ] Individual track recording (separate per participant)
- [ ] Recording storage (S3/GCS)
- [ ] Recording transcoding (to standard format)
- [ ] Recording metadata storage
- [ ] Recording access control
- [ ] Recording retention policy

### 15.5 AI Services
- [ ] Meeting transcription (speech-to-text)
- [ ] Meeting summary generation (LLM)
- [ ] Action item extraction (LLM)
- [ ] Meeting recap template generation
- [ ] Noise cancellation model serving
- [ ] Background segmentation model serving

### 15.6 TURN Server
- [ ] TURN server running (coturn or cloud service)
- [ ] Time-limited TURN credentials generation
- [ ] TURN relay for NAT traversal
- [ ] TURN TLS (port 443) for restrictive networks
- [ ] TURN monitoring and logging
- [ ] TURN geographic distribution

### 15.7 Database
- [ ] Schema: meetings table
- [ ] Schema: meeting_participants table
- [ ] Schema: meeting_recordings table
- [ ] Schema: meeting_chat_messages table
- [ ] Schema: meeting_notes table
- [ ] Schema: meeting_recaps table (AI-generated)
- [ ] Schema: meeting_action_items table
- [ ] Indexes on meeting_id, user_id, created_at
- [ ] Database migrations setup

### 15.8 Monitoring & Ops
- [ ] Health check endpoint
- [ ] Metrics endpoint (Prometheus)
- [ ] Meeting metrics: concurrent meetings, participants
- [ ] WebRTC metrics: connection success rate, quality scores
- [ ] Recording metrics: storage usage, transcoding queue
- [ ] Alert rules for SFU overload
- [ ] Alert rules for signaling server errors
- [ ] Log aggregation
- [ ] Backup strategy

---

## Appendix A: View-Level Audit

### A.1 PreJoinLobby.jsx — Pre-Join View
- [x] Meeting code input field
- [x] Meeting code auto-generation (`generateMeetingCode()`)
- [x] Camera preview via `<video>` element
- [x] Audio toggle with sessionStorage persistence
- [x] Video toggle with sessionStorage persistence
- [x] Audio device selection from enumerated devices
- [x] Video device selection from enumerated devices
- [x] Device preferences persistence to sessionStorage
- [x] Device list refresh on mount
- [x] Preview stream start/stop lifecycle
- [x] Preview stream cleanup on unmount
- [x] Online/offline detection
- [x] Time/date display with interval update
- [x] Navigate to `/meeting/:meetingId` on join
- [x] Auth user info from context
- [ ] Audio level visualizer (input level meter)
- [ ] Speaker device selection (output)
- [ ] Device test button (play sound)
- [ ] Camera resolution info display
- [ ] Permission denied error state with instructions
- [ ] No camera/mic available fallback UI
- [ ] Bandwidth/connection quality pre-test
- [ ] Display name input (editable)
- [ ] Background blur preview toggle
- [ ] Virtual background selection
- [ ] Meeting info card (host, title, scheduled time)
- [ ] Meeting password field (if required)
- [ ] Waiting room indicator
- [ ] Recent meetings quick-join list
- [ ] Copy meeting link button
- [ ] Share meeting link button
- [ ] PreJoinLobby a11y: all form elements labeled
- [ ] PreJoinLobby a11y: device selector accessible
- [ ] PreJoinLobby a11y: keyboard navigable

### A.2 ActiveMeeting.jsx — Live Meeting View
- [x] Socket.io connection to signaling server
- [x] ICE server configuration
- [x] Peer connection management
- [x] Local stream acquisition (audio + video)
- [x] Remote stream handling via `ontrack`
- [x] SDP offer/answer exchange
- [x] ICE candidate exchange
- [x] Connection state tracking (per peer)
- [x] ConnectionMeter component for signal quality
- [x] StreamVideo component for rendering streams
- [x] Deterministic offer initiator selection
- [x] Session preferences loaded from sessionStorage
- [x] Meeting notes drawer integration
- [ ] Video grid layout (responsive tile arrangement)
- [ ] Active speaker detection (audio level monitoring)
- [ ] Speaker highlight border on active speaker
- [ ] Layout mode: gallery, speaker, sidebar, focus
- [ ] Mute/unmute with keyboard shortcut
- [ ] Camera toggle with keyboard shortcut
- [ ] Screen share with getDisplayMedia
- [ ] Hand raise button and state
- [ ] Recording controls
- [ ] Chat panel toggle
- [ ] Participants panel toggle
- [ ] Meeting timer display
- [ ] Meeting lock/unlock
- [ ] End meeting for self
- [ ] End meeting for all
- [ ] PiP mode support
- [ ] Full-screen toggle
- [ ] Reconnection on ICE failure
- [ ] Participant join/leave notifications
- [ ] ActiveMeeting a11y: control buttons labeled
- [ ] ActiveMeeting a11y: participant names announced
- [ ] ActiveMeeting a11y: keyboard shortcuts

### A.3 ChatPanel.jsx — In-Meeting Chat
- [ ] Chat message list display
- [ ] Chat message: sender name + avatar
- [ ] Chat message: timestamp
- [ ] Chat message: text content
- [ ] Chat input field
- [ ] Send message button
- [ ] Send on Enter key
- [ ] Chat scroll to bottom on new message
- [ ] Chat empty state
- [ ] Chat notification badge (unread count)
- [ ] Chat message: emoji support
- [ ] Chat message: link detection
- [ ] Chat: to everyone vs private message
- [ ] Chat: file sharing
- [ ] Chat: reactions on messages
- [ ] Chat a11y: role="log" on message list
- [ ] Chat a11y: message input labeled

### A.4 ParticipantsView.jsx — Participants Panel
- [ ] Participant list with name, avatar, role
- [ ] Participant audio status icon (muted/unmuted)
- [ ] Participant video status icon (on/off)
- [ ] Participant hand raised icon
- [ ] Participant network quality indicator
- [ ] Participant count header
- [ ] Search/filter participants
- [ ] Host actions: mute participant
- [ ] Host actions: remove participant
- [ ] Host actions: make co-host
- [ ] Host actions: spotlight
- [ ] "Mute All" button (host)
- [ ] Waiting room section (if enabled)
- [ ] Admit/deny from waiting room
- [ ] Invite button (copy link or send invite)
- [ ] Participants a11y: list role
- [ ] Participants a11y: action buttons labeled

### A.5 ScreenShareMode.jsx — Screen Share View
- [ ] Large screen share content display
- [ ] Participant strip (small tiles) below/beside screen share
- [ ] Screen share border/frame
- [ ] "You are sharing" banner (if self sharing)
- [ ] Stop sharing button
- [ ] Annotation tools overlay
- [ ] Screen share controls
- [ ] Fit-to-window toggle
- [ ] Screen share a11y: announced to participants

### A.6 PostMeetingRecap.jsx — Recap View
- [x] Load recap from backend by meeting ID
- [x] Meeting ID from URL params or sessionStorage
- [x] Loading state handling
- [x] Error state handling
- [x] Recordings list fetch
- [x] Refresh summary action
- [x] Refresh action items action
- [x] Sync individual action item to TurboTick
- [x] Sync all action items batch
- [x] Retry deferred action items
- [x] Copy recap to clipboard
- [x] Copy status feedback
- [ ] Meeting title display
- [ ] Meeting date/time display
- [ ] Meeting duration display
- [ ] Participant list display
- [ ] AI-generated summary section
- [ ] Action items list with checkboxes
- [ ] Action item assignee display
- [ ] Action item priority badge
- [ ] Recording playback player
- [ ] Recording download button
- [ ] Transcript view (expandable)
- [ ] Share recap via email button
- [ ] Share recap via Connect button
- [ ] Export recap as PDF
- [ ] Create follow-up meeting button
- [ ] Recap feedback (thumbs up/down)
- [ ] Navigate back to lobby button
- [ ] Recap a11y: heading structure
- [ ] Recap a11y: action item list accessible

### A.7 MobileActiveSpeaker.jsx — Mobile Speaker View
- [ ] Large active speaker video
- [ ] Small self-view overlay (bottom corner)
- [ ] Simplified control bar (mute, camera, end)
- [ ] Swipe to toggle to grid view
- [ ] Tap to show/hide controls
- [ ] Portrait and landscape support
- [ ] Participant name label on speaker
- [ ] Active speaker auto-switches

### A.8 MobileGrid.jsx — Mobile Grid View
- [ ] 2x2 grid layout (4 participants)
- [ ] Each tile: video or avatar
- [ ] Each tile: name label
- [ ] Each tile: mute indicator
- [ ] Simplified control bar
- [ ] Swipe to toggle to speaker view
- [ ] Tap to show/hide controls
- [ ] Portrait and landscape support

### A.9 MeetNavigation.jsx — Navigation Component
- [ ] App logo/branding
- [ ] Navigation links (Lobby, Chat, Participants, Recap)
- [ ] Active route highlighting
- [ ] User avatar display
- [ ] Theme toggle (if present)
- [ ] Navigation hidden during active meeting
- [ ] Responsive navigation (mobile)
- [ ] Navigation a11y: role="navigation"

### A.10 MeetingNotesDrawer.jsx — Notes Drawer
- [x] Notes drawer component
- [ ] Open/close toggle
- [ ] Notes textarea (rich text or plain text)
- [ ] Auto-save notes
- [ ] Include chat messages toggle
- [ ] Auto-sync to TurboTick toggle
- [ ] Notes saved to meeting record
- [ ] Notes available in recap
- [ ] Drawer a11y: focus management

### A.11 NetworkQualityIndicator.jsx — Quality Display
- [ ] Signal bars visualization (1-5 bars)
- [ ] Color coding: green (good), yellow (fair), red (poor)
- [ ] Quality label text
- [ ] Tooltip with detailed metrics
- [ ] Updates in real-time
- [ ] a11y: role="status", aria-label with quality level

---

## Appendix B: Authentication Context Audit (AuthContext.jsx)

### B.1 Auth State
- [x] `isAuthenticated` — boolean
- [x] `isLoading` — loading state
- [x] `user` — user profile object
- [x] `token` — JWT access token
- [ ] `refreshToken` — refresh token
- [ ] `tokenExpiry` — token expiration time
- [ ] `permissions` — user permissions
- [ ] `orgId` — organization ID

### B.2 Auth Actions
- [x] `login()` — redirect to Gate OAuth
- [x] `loginLocalDemo()` — local demo authentication
- [x] `handleCallback()` — process OAuth callback
- [x] `logout()` — clear tokens, reset state
- [ ] `refreshAccessToken()` — refresh expired token
- [ ] `updateProfile()` — update user info
- [ ] `checkSession()` — verify token still valid

### B.3 Auth Flow
- [x] OAuth redirect to Gate
- [x] OAuth callback handling (code exchange)
- [x] Token storage in localStorage
- [x] User info extraction from token/API
- [ ] PKCE challenge generation
- [ ] PKCE verifier storage during redirect
- [ ] State parameter for CSRF protection
- [ ] Nonce for token validation
- [ ] Multi-tab session coordination

---

## Appendix C: Connection Recovery Audit (connectionRecovery.js)

### C.1 Recovery Mechanisms
- [ ] Detect ICE connection failure
- [ ] ICE restart attempt
- [ ] Full peer reconnection attempt
- [ ] Socket reconnection handling
- [ ] Exponential backoff for retries
- [ ] Max retry limit
- [ ] Recovery status notification to user
- [ ] Fallback to audio-only on poor connection
- [ ] Recovery metrics collection

### C.2 Recovery States
- [ ] `stable` — normal operation
- [ ] `detecting` — monitoring for issues
- [ ] `recovering` — actively attempting recovery
- [ ] `recovered` — successfully recovered
- [ ] `failed` — all recovery attempts exhausted
- [ ] State transitions logged for debugging
- [ ] UI reflects current recovery state

---

## Appendix D: WebRTC & Media Audit

### D.1 Peer Connection Configuration
- [x] RTCPeerConnection created with ICE servers
- [x] STUN servers: stun.l.google.com:19302 (ports 1-4)
- [ ] TURN server: UDP relay
- [ ] TURN server: TCP relay
- [ ] TURN server: TLS relay (port 443)
- [ ] ICE candidate trickling (send candidates as discovered)
- [ ] ICE candidate pooling
- [ ] ICE transport policy: `all` or `relay` (configurable)
- [ ] Bundle policy: `max-bundle`
- [ ] RTC codec preferences (VP8/VP9/H.264, Opus)
- [ ] Simulcast encoding layers (low/medium/high)

### D.2 Media Track Management
- [ ] Audio track: acquire from selected microphone
- [ ] Audio track: apply constraints (echoCancellation, noiseSuppression, autoGainControl)
- [ ] Audio track: mute/unmute (track.enabled toggle)
- [ ] Audio track: replace track (device switch without renegotiation)
- [ ] Audio track: detect audio level (AudioContext analyser)
- [ ] Video track: acquire from selected camera
- [ ] Video track: apply constraints (width, height, frameRate)
- [ ] Video track: enable/disable (track.enabled toggle)
- [ ] Video track: replace track (device switch)
- [ ] Video track: apply transform (virtual background via TransformStream)
- [ ] Screen capture track: acquire via getDisplayMedia
- [ ] Screen capture track: with audio option
- [ ] Screen capture track: surface switching (tab → window → screen)
- [ ] Track cleanup: stop all tracks on call end
- [ ] Track cleanup: stop preview tracks on lobby leave

### D.3 SDP Management
- [x] Create offer (initiator)
- [x] Set local description (offer)
- [x] Send offer via signaling
- [x] Receive answer via signaling
- [x] Set remote description (answer)
- [x] Create answer (responder)
- [ ] SDP munging for codec preferences
- [ ] SDP munging for bandwidth limits
- [ ] SDP rollback on renegotiation failure
- [ ] Renegotiation on track add/remove

### D.4 Data Channel
- [ ] Data channel for in-meeting chat (peer-to-peer fallback)
- [ ] Data channel for participant status updates
- [ ] Data channel for reactions
- [ ] Data channel for hand raise signals
- [ ] Data channel ordered delivery
- [ ] Data channel reliability settings

### D.5 Quality Monitoring
- [ ] `getStats()` polling (every 2 seconds)
- [ ] Parse inbound-rtp stats (packets received, bytes, jitter)
- [ ] Parse outbound-rtp stats (packets sent, bytes, bitrate)
- [ ] Parse candidate-pair stats (round-trip-time, available bandwidth)
- [ ] Audio quality score calculation
- [ ] Video quality score calculation
- [ ] Frame drop rate monitoring
- [ ] Resolution adaptation tracking
- [ ] Bandwidth estimation display
- [ ] Quality alerts (warn when quality drops below threshold)

### D.6 Adaptive Bitrate
- [ ] Detect bandwidth constraints from stats
- [ ] Lower video resolution on bandwidth drop
- [ ] Lower video framerate on bandwidth drop
- [ ] Switch to audio-only on severe bandwidth constraints
- [ ] Restore quality when bandwidth improves
- [ ] Per-track bitrate allocation (prioritize screen share over camera)

---

## Appendix E: Meeting Lifecycle

### E.1 Meeting States
- [ ] `scheduled` — meeting created, not yet started
- [ ] `waiting` — host has not yet joined
- [ ] `active` — meeting in progress
- [ ] `paused` — all participants muted/on hold (breakout rooms)
- [ ] `ending` — meeting end triggered, cleanup in progress
- [ ] `ended` — meeting finalized, recap available
- [ ] `cancelled` — meeting was cancelled before starting

### E.2 Meeting Creation Flow
- [ ] User clicks "New Meeting" in lobby
- [ ] Meeting code generated (3-segment alphanumeric)
- [ ] Meeting record created via API
- [ ] Meeting link generated (base URL + code)
- [ ] Meeting link copyable
- [ ] Meeting link shareable (email, Connect)
- [ ] Meeting settings: enable/disable waiting room
- [ ] Meeting settings: enable/disable recording
- [ ] Meeting settings: set meeting password
- [ ] Meeting settings: allow/disallow screen sharing for participants
- [ ] Meeting settings: mute participants on join
- [ ] Meeting settings: video off on join

### E.3 Meeting Join Flow
- [ ] User enters meeting code or clicks link
- [ ] Lobby loads with device preview
- [ ] User configures audio/video preferences
- [ ] User clicks "Join"
- [ ] Client requests room token from API
- [ ] Client connects to signaling server
- [ ] If waiting room: client waits for host admission
- [ ] If no waiting room: client joins room immediately
- [ ] Peer connections established with existing participants
- [ ] Media streams exchanged
- [ ] Participant grid renders
- [ ] "Joined meeting" notification sent to others

### E.4 Meeting Leave Flow
- [ ] User clicks "Leave"
- [ ] Peer connections closed
- [ ] Media tracks stopped
- [ ] Socket room left
- [ ] Leave event sent to signaling server
- [ ] Other participants notified
- [ ] User redirected to recap or lobby
- [ ] If host leaves: co-host becomes host (or meeting ends)

### E.5 Meeting End Flow (Host)
- [ ] Host clicks "End meeting for all"
- [ ] Confirmation dialog shown
- [ ] End event sent to all participants
- [ ] All participants disconnected
- [ ] Recording stopped (if active)
- [ ] Meeting state set to `ended`
- [ ] Recap generation triggered
- [ ] All participants redirected to recap page

---

## Appendix F: Detailed Feature Matrix

### F.1 Features by Participant Role

| Feature | Host | Co-Host | Participant | Guest |
|---------|------|---------|-------------|-------|
| Mute/unmute self | - [ ] | - [ ] | - [ ] | - [ ] |
| Camera on/off | - [ ] | - [ ] | - [ ] | - [ ] |
| Screen share | - [ ] | - [ ] | - [ ] | - [ ] |
| Raise hand | - [ ] | - [ ] | - [ ] | - [ ] |
| In-meeting chat | - [ ] | - [ ] | - [ ] | - [ ] |
| Start recording | - [ ] | - [ ] | N/A | N/A |
| Stop recording | - [ ] | - [ ] | N/A | N/A |
| Mute others | - [ ] | - [ ] | N/A | N/A |
| Remove participant | - [ ] | - [ ] | N/A | N/A |
| Lock meeting | - [ ] | N/A | N/A | N/A |
| End for all | - [ ] | N/A | N/A | N/A |
| Create breakout rooms | - [ ] | N/A | N/A | N/A |
| Manage waiting room | - [ ] | - [ ] | N/A | N/A |
| Start poll | - [ ] | - [ ] | N/A | N/A |
| Start Q&A | - [ ] | - [ ] | N/A | N/A |
| RTMP streaming | - [ ] | N/A | N/A | N/A |

### F.2 Device Compatibility Matrix

| Feature | Chrome | Firefox | Safari | Edge | Mobile Chrome | Mobile Safari |
|---------|--------|---------|--------|------|---------------|---------------|
| Audio call | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] |
| Video call | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] |
| Screen share | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | N/A |
| Screen share audio | - [ ] | - [ ] | N/A | - [ ] | N/A | N/A |
| Virtual background | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] |
| Recording | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] |
| PiP mode | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] | - [ ] |

---

## Appendix G: Error Handling Matrix

### G.1 Error Scenarios
- [ ] Camera permission denied → show instructions to enable
- [ ] Microphone permission denied → show instructions to enable
- [ ] No camera found → show "camera not available" with audio-only option
- [ ] No microphone found → show "microphone not available" warning
- [ ] Meeting not found → show "meeting does not exist" with back to lobby
- [ ] Meeting ended → show "this meeting has ended" with recap link
- [ ] Meeting full → show "meeting is at capacity"
- [ ] Meeting locked → show "meeting is locked by host"
- [ ] Wrong password → show "incorrect meeting password"
- [ ] Network disconnected → show "reconnecting..." with recovery
- [ ] Network timeout → show "unable to connect" with retry
- [ ] Signaling server down → show "service unavailable" with retry
- [ ] TURN server unreachable → show "connection issues" fallback
- [ ] Peer connection failed → attempt ICE restart, then show error
- [ ] Recording failed → show "recording could not be saved"
- [ ] Screen share cancelled → gracefully handle, no error shown
- [ ] Browser not supported → show "please use Chrome/Firefox/Edge"
- [ ] WebRTC not supported → show "your browser does not support video calls"
- [ ] Insufficient bandwidth → show "poor connection" with quality options
- [ ] Token expired during meeting → attempt refresh, show error if fails
- [ ] API error (500) → show generic "something went wrong" with retry

---

*End of 04-MEET.md — Meet Video Conferencing App Checklist*
