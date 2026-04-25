# RM Orbit — World-Class Workspace Ecosystem Master Checklist

> **Total Checkpoints: ~1,800+**
> Track progress by checking boxes `[x]` as each item is completed.
> Last updated: 2026-04-06

---

## Table of Contents

1. [Phase 0: Unified Design System & UI Consistency](#phase-0-unified-design-system--ui-consistency)
2. [Phase 1: Core Eight — Polish to World Class](#phase-1-core-eight--polish-to-world-class)
3. [Phase 2: Orbit AI — The Intelligence Layer](#phase-2-orbit-ai--the-intelligence-layer)
4. [Phase 3: Experience Layer — One Product Feel](#phase-3-experience-layer--one-product-feel)
5. [Phase 4: Platform & Extensibility](#phase-4-platform--extensibility)
6. [Phase 5: Infrastructure & DevOps](#phase-5-infrastructure--devops)
7. [Phase 6: Security, Compliance & Enterprise Readiness](#phase-6-security-compliance--enterprise-readiness)
8. [Phase 7: Go-To-Market & Growth](#phase-7-go-to-market--growth)

---

## Phase 0: Unified Design System & UI Consistency

### 0.1 Design Tokens — Single Source of Truth

- [x] Create `/orbit-ui/tokens/` directory structure
- [x] Define master color palette JSON (`colors.json`)
  - [x] Pick single primary blue (standardized: `#2b7cee`)
  - [x] Define primary scale: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
  - [x] Define neutral/gray scale (slate-based)
  - [x] Define success color scale (green)
  - [x] Define warning color scale (amber)
  - [x] Define danger/error color scale (red)
  - [x] Define info color scale (cyan/sky)
  - [x] Define surface colors (light mode): background, card, elevated, overlay
  - [x] Define surface colors (dark mode): background, card, elevated, overlay
  - [x] Define text colors: primary, secondary, muted, disabled, inverse
  - [x] Define border colors: default, subtle, strong, focus
  - [x] Define glass colors: bg, border (light + dark)
- [x] Define master typography tokens (`typography.json`)
  - [x] Font families: display (RM Samplet), sans (RM Forma), mono (JetBrains Mono)
  - [x] Font sizes: 2xs–6xl with line heights
  - [x] Font weights: light–extrabold
  - [x] Line heights: none, tight, snug, normal, relaxed, loose
  - [x] Letter spacing: tighter–widest
- [x] Define border radius tokens (`radius.json`)
  - [x] none, xs, sm, md, lg, xl, 2xl, 3xl, full
  - [x] Component-specific: button, input, card, modal, badge, panel, chip
- [x] Define shadow tokens (`shadows.json`)
  - [x] sm, md, lg, xl, 2xl, inner, none
  - [x] glass, glass-sm (glassmorphism shadows)
  - [x] focus, focus-danger, focus-success (ring shadows)
  - [x] card, card-hover, modal, dropdown, tooltip
  - [x] glow, glow-lg, glow-pulse
- [x] Define z-index tokens (`z-index.json`)
  - [x] base → max, all overlay layers named
- [x] Define animation/motion tokens (`motion.json`)
  - [x] Durations: instant (0ms), fast (100ms), normal (200ms), slow (300ms), slower (500ms), slowest (700ms)
  - [x] Easings: ease-in, ease-out, ease-in-out, spring, spring-soft, overshoot
  - [x] Keyframes: fade-in/out, slide-up/down/left/right, scale-in/out, shimmer, pulse-ring, float, spin, bounce-soft
- [x] Build CSS custom properties file (`orbit-tokens.css`)
  - [x] All static palette tokens
  - [x] Light mode semantic tokens (`:root`)
  - [x] Dark mode semantic tokens (`.dark`)
  - [x] Font face declarations
  - [x] Base reset & defaults
  - [x] Theme transition (smooth dark/light switch)
  - [x] Global focus-visible style
  - [x] Skip link component
  - [x] Global thin scrollbar style
- [x] Build shared Tailwind preset (`tailwind-preset.js`)
  - [x] All tokens wired into Tailwind theme
  - [x] Glass utility plugin (`.glass`, `.glass-sm`, `.glass-subtle`)
  - [x] Focus ring plugin (`.focus-ring`, `.focus-ring-inset`)
  - [x] Scrollbar plugin (`.scrollbar-thin`, `.scrollbar-none`)
  - [x] Skeleton/shimmer plugin (`.skeleton`)
- [x] Build token sync script (`scripts/sync-tokens.sh`)
  - [x] Syncs `orbit-tokens.css` + `orbit-bar.js` to all 16 app public dirs
- [x] Integrate tokens into Atlas (reference implementation)
  - [x] Atlas `index.css` imports `orbit-tokens.css`
  - [x] Atlas `tailwind.config.js` uses shared preset
  - [x] Atlas builds successfully ✓
- [ ] Integrate token build into CI pipeline
- [ ] Document token usage guidelines
- [ ] Migrate remaining 15 apps to use shared preset (in progress)

### 0.2 Shared Tailwind Preset

- [x] Create `/orbit-ui/tailwind-preset.js`
- [x] Define shared color palette in preset (from tokens)
- [x] Define shared font families in preset
- [x] Define shared font sizes in preset
- [x] Define shared spacing scale in preset
- [x] Define shared border radius in preset
- [x] Define shared shadows in preset
- [x] Define shared z-index scale in preset
- [x] Define shared animations in preset
- [x] Define shared breakpoints in preset
- [x] Configure darkMode: "class" in preset
- [x] Add shared plugins (glass, focus-ring, scrollbar, skeleton)
- [x] Migrate Atlas `tailwind.config.js` to use preset
- [x] Migrate Mail `tailwind.config.js` to use preset
- [x] Migrate Connect `tailwind.config.js` to use preset
- [x] Migrate Meet `tailwind.config.js` to use preset
- [x] Migrate Calendar `tailwind.config.js` to use preset
- [x] Migrate Writer `tailwind.config.js` to use preset
- [x] Migrate Planet `tailwind.config.js` to use preset
- [x] Migrate Secure `tailwind.config.js` to use preset
- [ ] Migrate Control Center `tailwind.config.js` to use preset
- [x] Migrate Capital Hub `tailwind.config.js` to use preset
- [ ] Migrate TurboTick `tailwind.config.js` to use preset
- [ ] Migrate Dock `tailwind.config.js` to use preset
- [ ] Migrate Wallet `tailwind.config.js` to use preset
- [ ] Migrate FitterMe `tailwind.config.js` to use preset
- [ ] Migrate Learn `tailwind.config.js` to use preset
- [x] Remove all app-specific color overrides that conflict with shared palette
- [ ] Verify visual consistency after migration (each app)

### 0.3 Shared React Component Library — `@orbit-ui/react`

#### 0.3.1 Project Setup
- [x] Create `/orbit-ui/react/` package directory
- [x] Initialize `package.json` with `@orbit-ui/react` name
- [x] Configure TypeScript (`tsconfig.json`)
- [x] Configure Vite for library build mode
- [x] Set up exports map (tree-shakeable ESM)
- [x] Add `cn()` utility (clsx + tailwind-merge)
- [ ] Create component template/generator script
- [ ] Configure Storybook 8 for component development
- [ ] Set up Vitest for component testing
- [x] Add `@orbit-ui/react` as file: dependency in all 9 primary apps

#### 0.3.2 Primitive Components
- [x] **Button**
  - [x] Variants: primary, secondary, outline, ghost, danger, success, warning
  - [x] Sizes: xs, sm, md, lg, xl
  - [x] States: default, hover, active, focus, disabled, loading
  - [x] Icon support (left icon, right icon, icon-only)
  - [x] Loading spinner integration
  - [x] Polymorphic `as` prop (button, a, Link)
  - [x] Full keyboard accessibility
  - [ ] Write Storybook stories
  - [ ] Write unit tests
- [x] **IconButton**
  - [x] Square variant with all sizes
  - [x] Loading spinner support
  - [x] Accessibility: aria-label required
  - [ ] Tooltip on hover
  - [ ] Write Storybook stories
- [x] **ButtonGroup**
  - [x] Horizontal grouping with connected borders
  - [x] Vertical grouping option
  - [x] Active state management
- [x] **Input**
  - [x] Sizes: sm, md, lg
  - [x] States: default, focus, error, disabled
  - [x] Prefix/suffix elements (icons, text)
  - [x] Error message display
  - [x] Helper text
  - [x] Auto-generated accessible id + aria-describedby
  - [ ] Clear button option
  - [ ] Character count display
  - [ ] Write Storybook stories
  - [ ] Write unit tests
- [ ] **Textarea**
  - [ ] Auto-resize option
  - [ ] Character count
  - [ ] Min/max rows
  - [ ] Error/helper text
- [ ] **Select**
  - [ ] Native select wrapper
  - [ ] Custom dropdown select (searchable)
  - [ ] Multi-select variant
  - [ ] Option groups
  - [ ] Clear button
  - [ ] Loading state
- [x] **Checkbox**
  - [x] Checked, unchecked, indeterminate states
  - [x] Label + description support
  - [x] Disabled state
  - [ ] Checkbox group component
- [x] **Radio**
  - [x] Radio button component
  - [x] Radio group with vertical/horizontal layouts
  - [ ] Card-style radio (selectable cards)
- [x] **Switch/Toggle**
  - [x] Sizes: sm, md
  - [x] Label + description support
  - [x] Disabled state
  - [x] Color variants
- [x] **Slider**
  - [x] Single value
  - [x] Range (two thumbs)
  - [ ] Step markers
  - [x] Value tooltip
- [x] **DatePicker**
  - [x] Single date selection
  - [x] Date range selection
  - [x] Month/year navigation
  - [x] Min/max date constraints
  - [ ] Keyboard navigation
  - [x] Locale support
- [x] **TimePicker**
  - [x] 12h/24h format
  - [x] Minute intervals (5, 10, 15, 30)
  - [ ] Keyboard input support
- [ ] **ColorPicker**
  - [ ] Preset palette
  - [ ] Custom color input (hex, rgb)
  - [ ] Opacity slider

#### 0.3.3 Layout Components
- [ ] **Box**
  - [ ] Polymorphic base layout component
  - [ ] Padding, margin, border-radius props from tokens
- [ ] **Flex**
  - [ ] Direction, align, justify, wrap, gap props
  - [ ] Responsive variants
- [ ] **Grid**
  - [ ] Columns, rows, gap props
  - [ ] Responsive column count
  - [ ] Auto-fit/auto-fill modes
- [ ] **Stack**
  - [ ] VStack (vertical)
  - [ ] HStack (horizontal)
  - [ ] Spacing from tokens
  - [ ] Divider option between items
- [ ] **Container**
  - [ ] Max-width variants (sm, md, lg, xl, full)
  - [ ] Centered by default
  - [ ] Responsive padding
- [x] **Divider**
  - [x] Horizontal/vertical
  - [x] With label/text
  - [x] Color variants (default, strong, subtle)
- [ ] **Spacer**
  - [ ] Flexible space filler
  - [ ] Fixed size option
- [ ] **AspectRatio**
  - [ ] Common ratios: 1:1, 4:3, 16:9, 21:9
  - [ ] Custom ratio support
- [ ] **ScrollArea**
  - [ ] Custom styled scrollbar
  - [ ] Auto-hide option
  - [ ] Horizontal scroll support
  - [ ] Scroll-to-top button

#### 0.3.4 Data Display Components
- [x] **Avatar**
  - [x] Image avatar with error fallback
  - [x] Initials fallback (deterministic color from name)
  - [x] Sizes: xs, sm, md, lg, xl
  - [x] Status indicator: online, offline, busy, away
  - [x] AvatarGroup with overlap and +N counter
- [x] **Badge**
  - [x] Variants: solid, subtle, outline
  - [x] Colors: primary, success, warning, danger, info, neutral
  - [x] Sizes: sm, md, lg
  - [x] Dot indicator (no text)
  - [x] Removable (with X button)
- [x] **Card**
  - [x] Default card (border + shadow)
  - [x] Elevated card (larger shadow)
  - [x] Glass card (glassmorphism)
  - [x] Flat card
  - [x] Interactive card (hover/click states)
  - [x] Card.Header, Card.Title, Card.Description, Card.Body, Card.Footer, Card.Divider
  - [ ] With image/media slot
- [x] **Tag**
  - [x] Color variants
  - [x] Removable
  - [x] With icon
  - [x] Tag input component
- [x] **Table**
  - [x] Sortable headers
  - [ ] Row selection (single, multi)
  - [x] Sticky header option
  - [ ] Sticky first column option
  - [x] Striped rows option
  - [x] Hover highlight
  - [x] Empty state
  - [ ] Loading skeleton
  - [ ] Pagination integration
  - [ ] Resizable columns
  - [ ] Column visibility toggle
- [ ] **DataGrid** (advanced table)
  - [ ] Virtual scrolling for large datasets
  - [ ] Inline editing
  - [ ] Column filtering
  - [ ] Column grouping
  - [ ] Row expansion
  - [ ] Export (CSV, JSON)
- [ ] **List**
  - [ ] Simple list
  - [ ] List with icons
  - [ ] List with avatars
  - [ ] Interactive list items
  - [ ] Drag-and-drop reordering
- [ ] **Timeline**
  - [ ] Vertical timeline
  - [ ] Horizontal timeline
  - [ ] With icons
  - [ ] With status colors
- [ ] **Stat/KPI**
  - [ ] Value with label
  - [ ] Trend indicator (up/down/neutral)
  - [ ] Comparison text
  - [ ] Spark line option
- [ ] **EmptyState**
  - [ ] Illustration slot
  - [ ] Title + description
  - [ ] Action button
  - [ ] Different sizes
- [ ] **Code**
  - [ ] Inline code
  - [ ] Code block with syntax highlighting
  - [ ] Copy button
  - [ ] Line numbers
  - [ ] Language label

#### 0.3.5 Feedback Components
- [ ] **Toast/Notification**
  - [ ] Variants: info, success, warning, error
  - [ ] Positions: top-right, top-center, top-left, bottom-right, bottom-center, bottom-left
  - [ ] Auto-dismiss with configurable duration
  - [ ] Action button support
  - [ ] Stackable with limit
  - [ ] Progress bar option
  - [ ] Toast provider context
- [ ] **Alert**
  - [ ] Variants: info, success, warning, error
  - [ ] Dismissible option
  - [x] With icon
  - [ ] With title + description
  - [ ] With action buttons
- [ ] **Banner**
  - [ ] Full-width sticky banner
  - [ ] Variants: info, warning, error, promo
  - [ ] Dismissible
  - [ ] With CTA button
- [x] **Progress**
  - [x] Linear progress bar (sizes: xs, sm, md, lg)
  - [ ] Circular/ring progress
  - [ ] Indeterminate/animated state
  - [x] With label/percentage display
  - [x] Color variants: default, success, warning, danger
  - [x] Stacked/segmented progress bar
- [ ] **Spinner/Loader**
  - [ ] Sizes: sm, md, lg
  - [x] Color variants
  - [ ] Full-page overlay loader
  - [ ] Inline loader
  - [ ] Skeleton loader component
- [ ] **Skeleton**
  - [ ] Text skeleton (single line, multi-line)
  - [ ] Circle skeleton (avatar)
  - [ ] Rectangle skeleton (card, image)
  - [ ] Table row skeleton
  - [ ] Pulse animation
  - [ ] Wave animation option

#### 0.3.6 Overlay Components
- [ ] **Modal/Dialog**
  - [ ] Sizes: sm, md, lg, xl, full
  - [ ] Centered and slide-in variants
  - [ ] Header, body, footer sections
  - [ ] Close on backdrop click (configurable)
  - [ ] Close on Escape
  - [ ] Focus trap
  - [ ] Scroll locking
  - [ ] Nested modal support
  - [ ] Transition animations
  - [ ] AlertDialog variant (confirm/cancel)
- [x] **Drawer/Sheet**
  - [x] Positions: left, right, top, bottom
  - [x] Sizes: sm, md, lg, xl, full
  - [x] Overlay backdrop
  - [ ] Swipe-to-close on mobile
- [x] **Popover**
  - [x] Trigger element
  - [x] Placement (top, bottom, left, right)
  - [ ] Arrow option
  - [x] Click trigger
  - [ ] Focus management
- [ ] **Tooltip**
  - [ ] Placement (top, bottom, left, right)
  - [ ] Delay (show/hide)
  - [ ] Arrow option
  - [ ] Rich content (not just text)
  - [ ] Touch device support
- [x] **Dropdown Menu**
  - [x] Menu items with icons (left + right)
  - [x] Sub-trigger (ChevronRight indicator)
  - [x] Dividers and labels/groups
  - [x] Keyboard: Escape to close, outside-click to close
  - [x] Disabled items
  - [x] Checked menu items
  - [x] Destructive item style
- [x] **Context Menu**
  - [x] Right-click trigger
  - [x] Same API as Dropdown Menu
  - [x] Nested submenus
- [x] **Command Palette**
  - [x] Search input with instant filtering
  - [x] Categorized results
  - [x] Keyboard navigation
  - [ ] Recent items
  - [x] Shortcut display
  - [x] Action execution
  - [ ] Extensible command registry

#### 0.3.7 Navigation Components
- [ ] **Tabs**
  - [ ] Horizontal tabs
  - [ ] Vertical tabs
  - [ ] Underline style
  - [ ] Pill/segment style
  - [ ] With icons
  - [ ] With badge counts
  - [ ] Overflow scrolling for many tabs
  - [ ] Lazy rendering of tab content
- [ ] **Sidebar**
  - [ ] Collapsible (icon-only mode)
  - [ ] Expandable on hover
  - [ ] Sections with headers
  - [ ] Navigation items with icons
  - [ ] Active state indicator
  - [ ] Badge/count indicators
  - [ ] Footer section (settings, profile)
  - [ ] Mobile: drawer overlay
  - [ ] Keyboard shortcut to toggle
- [x] **Breadcrumb**
  - [x] Auto-truncation with ellipsis
  - [x] Custom separator
  - [ ] With dropdown for long paths
- [x] **Pagination**
  - [x] Page numbers
  - [x] Previous/next
  - [x] First/last
  - [ ] Items per page selector
  - [ ] Total count display
  - [ ] Compact mode for mobile
- [x] **Stepper**
  - [x] Horizontal steps
  - [x] Vertical steps
  - [x] Completed/active/upcoming/error states
  - [x] With descriptions
  - [ ] Clickable navigation
- [ ] **NavigationMenu**
  - [ ] Horizontal nav with dropdowns
  - [ ] Mega menu support
  - [ ] Mobile hamburger collapse

#### 0.3.8 Utility Components
- [ ] **Portal**
  - [ ] Render children in document.body
  - [ ] Custom container target
- [ ] **VisuallyHidden**
  - [ ] Screen reader only content
- [ ] **FocusTrap**
  - [ ] Trap focus within a container
  - [ ] Return focus on unmount
- [ ] **ClickOutside**
  - [ ] Detect clicks outside a container
- [ ] **ResizeObserver**
  - [ ] Hook for element resize detection
- [ ] **IntersectionObserver**
  - [ ] Hook for visibility detection
  - [ ] Lazy loading trigger
- [ ] **Transition/AnimatePresence**
  - [ ] Enter/exit animations
  - [ ] Shared layout animations
  - [ ] Stagger children

#### 0.3.9 Shared Hooks Library
- [ ] `useTheme()` — access and toggle dark/light mode
- [ ] `useMediaQuery(query)` — responsive breakpoint detection
- [ ] `useClickOutside(ref, handler)` — click outside detection
- [ ] `useDebounce(value, delay)` — debounced value
- [ ] `useThrottle(callback, delay)` — throttled callback
- [ ] `useLocalStorage(key, initial)` — persistent local state
- [ ] `useSessionStorage(key, initial)` — session-scoped state
- [ ] `useCopyToClipboard()` — copy text with success feedback
- [ ] `useKeyboardShortcut(keys, handler)` — keyboard shortcut registration
- [ ] `useOnline()` — network status detection
- [ ] `useWindowSize()` — window dimensions
- [ ] `useScrollPosition()` — scroll position tracking
- [ ] `useIntersection(ref)` — intersection observer hook
- [ ] `usePrevious(value)` — previous value reference
- [ ] `useToggle(initial)` — boolean toggle
- [ ] `useDisclosure()` — open/close state management
- [ ] `useOrbitAuth()` — Gate authentication context
- [ ] `useOrbitOrg()` — current organization context
- [ ] `useOrbitUser()` — current user context
- [ ] `useOrbitEventBus(channel, handler)` — subscribe to event bus
- [ ] `useOrbitApi(endpoint)` — authenticated API calls with SWR/React Query

### 0.4 Dark Mode — Ecosystem-Wide

- [x] Define dark mode color palette in design tokens
- [x] Implement theme provider context (`ThemeProvider` in `@orbit-ui/react`)
- [ ] Store theme preference in Gate user settings (server-synced)
- [x] Fallback to `localStorage` for unauthenticated pages
- [x] Respect OS `prefers-color-scheme` as default
- [x] Anti-FOUC script in all 16 app index.html files
- [x] `ThemeProvider` wired into all React app entry points (main.tsx/jsx)
- [x] Add dark mode to Atlas
  - [x] Audit all hardcoded colors in Atlas CSS
  - [x] Replace with Tailwind dark: variants (semantic token migration)
  - [ ] Test all views in dark mode
- [x] Add dark mode to Mail
  - [x] Audit all hardcoded colors in Mail CSS
  - [x] Replace with semantic orbit tokens
  - [ ] Handle email content iframe (keep original email colors)
  - [ ] Test all views in dark mode
- [x] Add dark mode to Connect
  - [x] Audit all hardcoded colors
  - [x] Replace with dark: variants
  - [ ] Test all views
- [x] Add dark mode to Calendar
  - [x] Audit all hardcoded colors
  - [x] Replace with dark: variants
  - [ ] Test all views
- [x] Add dark mode to Planet
  - [x] Audit all hardcoded colors
  - [x] Replace with dark: variants
  - [ ] Test all views (especially charts)
- [x] Verify dark mode in Meet
- [x] Verify dark mode in Writer
- [x] Verify dark mode in Secure
- [x] Add dark mode to Control Center
- [x] Add dark mode to TurboTick (orbit-tokens.css + anti-FOUC)
- [x] Add dark mode to Capital Hub (ThemeProvider + semantic tokens)
- [x] Add dark mode to Dock (orbit-tokens.css + anti-FOUC)
- [x] Add dark mode to Wallet (orbit-tokens.css + anti-FOUC)
- [x] Add dark mode to Learn (ThemeProvider + semantic tokens)
- [x] Add dark mode to FitterMe (orbit-tokens.css + anti-FOUC)
- [x] Update Orbit Bar to respect theme toggle (applies/removes `.dark` on `<html>`)
- [x] Add theme toggle to Orbit Bar UI (sun/moon SVG button cycles light→dark→system)
- [ ] Animate theme transitions (no flash on switch)
- [ ] Test all glassmorphism effects in both modes
- [ ] Test all charts/graphs in dark mode

### 0.5 Typography Consistency

- [ ] Audit all apps for font-family declarations — remove any non-standard fonts
- [ ] Ensure RM Forma is used for all body text in all apps
- [ ] Ensure RM Samplet is used for all display/hero text
- [ ] Ensure JetBrains Mono is used for all code/monospace
- [ ] Standardize heading sizes (h1-h6) across all apps
- [ ] Standardize body text size (16px base) across all apps
- [ ] Standardize line-height across all apps
- [ ] Remove all inline font-size overrides that break the scale
- [ ] Ensure font files are loaded consistently (woff2 preferred)
- [ ] Add font-display: swap for performance
- [ ] Test font rendering on Windows, macOS, Linux
- [ ] Test font rendering in Chrome, Firefox, Safari, Edge

### 0.6 Icon System Consistency

- [ ] Pin `lucide-react` version across all apps (latest stable)
- [ ] Create icon usage guide (which icons for which actions)
- [ ] Standardize icon sizes: sm (16px), md (20px), lg (24px), xl (32px)
- [ ] Remove Material Symbols dependency (replace with Lucide equivalents)
- [ ] Audit all apps for inconsistent icon usage
- [ ] Create app-specific icon sets if needed (via Lucide tree-shaking)
- [ ] Ensure all interactive icons have aria-labels

### 0.7 Animation & Motion Language

- [ ] Standardize on `motion` (Framer Motion successor) as the animation library
- [ ] Remove `framer-motion` dependency (upgrade to `motion`)
- [ ] Define shared animation presets in `@orbit-ui/react`
  - [ ] `fadeIn` / `fadeOut`
  - [ ] `slideUp` / `slideDown` / `slideLeft` / `slideRight`
  - [ ] `scaleIn` / `scaleOut`
  - [ ] `stagger` (children animation)
  - [ ] `skeleton` (shimmer/pulse)
  - [ ] `spring` (interactive feedback)
- [ ] Implement `prefers-reduced-motion` respect across all animations
- [ ] Document motion principles (when to animate, duration guidelines)

### 0.8 Glassmorphism Design Language

- [ ] Define glassmorphism token set
  - [ ] `glass-bg`: `rgba(255, 255, 255, 0.08)` (dark), `rgba(255, 255, 255, 0.7)` (light)
  - [ ] `glass-blur`: `blur(12px)`
  - [ ] `glass-border`: `1px solid rgba(255, 255, 255, 0.12)`
  - [ ] `glass-shadow`: defined in shadow tokens
- [ ] Create `.glass` Tailwind utility class via plugin
- [ ] Apply glassmorphism consistently to: modals, sidebars, floating panels, dropdowns
- [ ] Ensure glassmorphism degrades gracefully on non-supporting browsers
- [ ] Test glassmorphism on low-performance devices

### 0.9 Responsive Design Standards

- [ ] Define responsive breakpoint strategy using shared tokens
- [ ] Define mobile-first design patterns for each component
- [ ] Audit Atlas for responsive issues
- [ ] Audit Mail for responsive issues
- [ ] Audit Connect for responsive issues
- [ ] Audit Meet for responsive issues
- [ ] Audit Calendar for responsive issues
- [ ] Audit Writer for responsive issues
- [ ] Audit Planet for responsive issues
- [ ] Audit Control Center for responsive issues
- [ ] Define sidebar collapse behavior at tablet breakpoint (all apps)
- [ ] Define navigation switch to hamburger at mobile breakpoint
- [ ] Test all apps at 320px, 375px, 768px, 1024px, 1440px, 1920px
- [ ] Test with touch interactions on mobile viewport

### 0.10 Accessibility (a11y)

- [ ] Add skip links to all apps (standardized from shared component)
- [ ] Ensure all interactive elements are keyboard accessible
- [ ] Add ARIA labels to all icon buttons across all apps
- [ ] Ensure color contrast meets WCAG 2.1 AA in light mode
- [ ] Ensure color contrast meets WCAG 2.1 AA in dark mode
- [ ] Add focus-visible ring to all interactive elements (standardized)
- [ ] Implement roving tabindex in all list/grid components
- [ ] Ensure all modals trap focus
- [ ] Ensure all modals return focus on close
- [ ] Add screen reader announcements for toasts/notifications
- [ ] Add `role` attributes to all landmark regions
- [ ] Test with VoiceOver (macOS)
- [ ] Test with NVDA (Windows)
- [ ] Test with keyboard-only navigation (all apps)
- [ ] Add `prefers-reduced-motion` support
- [ ] Add `prefers-contrast` support (high contrast mode)

### 0.11 Storybook & Documentation

- [ ] Set up Storybook 8 with Vite builder
- [ ] Configure Storybook with Orbit design tokens
- [ ] Configure Storybook dark mode toggle
- [ ] Write stories for every component (all states/variants)
- [ ] Add interaction tests in Storybook
- [ ] Add accessibility audits in Storybook (a11y addon)
- [ ] Deploy Storybook to a URL for team access
- [ ] Write component usage guidelines
- [ ] Write "do's and don'ts" for each component
- [ ] Create page-level composition examples (login, dashboard, settings, list, detail)

### 0.12 App-by-App UI Migration

- [ ] **Atlas** — Replace custom CSS utilities with `@orbit-ui/react` components
  - [ ] Replace `.btn-primary`, `.btn-secondary` with `<Button>`
  - [ ] Replace `.card`, `.card-hover` with `<Card>`
  - [ ] Replace `.input`, `.textarea`, `.select` with shared form components
  - [ ] Replace `.badge` with `<Badge>`
  - [ ] Replace `.nav-item` with `<Sidebar>` navigation
  - [ ] Replace custom modal with `<Modal>`
  - [ ] Replace custom toast with `<Toast>`
  - [ ] Replace custom empty states with `<EmptyState>`
  - [ ] Verify all views after migration
- [ ] **Mail** — Migrate to shared components
  - [ ] Replace custom buttons
  - [ ] Replace custom inputs/forms
  - [ ] Replace custom modals
  - [ ] Replace custom sidebar
  - [ ] Verify all views after migration
- [ ] **Connect** — Migrate to shared components
  - [ ] Replace custom buttons
  - [ ] Replace custom inputs/forms
  - [ ] Replace channel list with `<Sidebar>`
  - [ ] Replace message components with shared patterns
  - [ ] Verify all views after migration
- [ ] **Meet** — Migrate to shared components
  - [ ] Replace MeetNavigation with shared `<Sidebar>`
  - [ ] Replace custom buttons
  - [ ] Replace custom modals
  - [ ] Verify all views after migration
- [ ] **Calendar** — Migrate to shared components
  - [ ] Replace event modals
  - [ ] Replace form inputs
  - [ ] Replace buttons
  - [ ] Verify all views after migration
- [ ] **Writer** — Migrate to shared components
  - [ ] Replace toolbar buttons
  - [ ] Replace modals/dialogs
  - [ ] Replace form elements
  - [ ] Verify all views after migration
- [ ] **Planet** — Migrate to shared components
  - [ ] Replace CRM pipeline cards
  - [ ] Replace form elements
  - [ ] Replace data tables
  - [ ] Replace modals
  - [ ] Verify all views after migration
- [ ] **Control Center** — Migrate to shared components
  - [ ] Replace Button.tsx with shared `<Button>`
  - [ ] Replace other custom components
  - [ ] Verify all views after migration

---

## Phase 1: Core Eight — Polish to World Class

### 1.1 Gate (AuthX) — Identity Core

#### Authentication & SSO
- [ ] OIDC discovery endpoint (`/.well-known/openid-configuration`)
- [ ] Support PKCE flow for all web apps
- [ ] Support authorization code flow for server-side apps
- [ ] Support client credentials flow for service-to-service
- [ ] Refresh token rotation with reuse detection
- [ ] Token revocation endpoint
- [ ] Session listing and remote session kill
- [ ] Concurrent session limits (configurable per org)
- [ ] Step-up authentication for sensitive operations
- [ ] Remember device / trusted device management

#### Multi-Factor Authentication
- [ ] TOTP (Google Authenticator, Authy)
- [ ] WebAuthn / FIDO2 (hardware keys, biometric)
- [ ] SMS OTP (Twilio integration)
- [ ] Email OTP
- [ ] Recovery codes generation and management
- [ ] Enforce MFA per organization policy
- [ ] Enforce MFA per role
- [ ] MFA challenge on new device/location
- [ ] Backup MFA method requirement

#### Directory & User Management
- [ ] SCIM 2.0 provisioning endpoint
  - [ ] User create/update/delete/disable
  - [ ] Group create/update/delete
  - [ ] Bulk operations
  - [ ] Filtering and pagination
- [ ] Azure AD connector
- [ ] Okta connector
- [ ] Google Workspace connector
- [ ] LDAP/Active Directory connector
- [ ] Just-in-time (JIT) provisioning from SAML
- [ ] User profile fields (name, avatar, bio, timezone, locale)
- [ ] User status (active, suspended, invited, deactivated)
- [ ] User search and filtering
- [ ] Bulk user import (CSV)
- [ ] Bulk user export

#### Organization & Tenant Management
- [ ] Organization create/update/delete
- [ ] Organization settings (name, logo, domain, billing plan)
- [ ] Custom branding per org (logo, colors, favicon, login background)
- [ ] Custom domain per org (CNAME mapping)
- [ ] Organization member management (invite, remove, role change)
- [ ] Organization-level feature flags
- [ ] Organization data export (GDPR)
- [ ] Organization data deletion (GDPR right to erasure)
- [ ] Organization transfer (change owner)
- [ ] Multi-org membership for users

#### Roles & Permissions
- [ ] Role-based access control (RBAC)
  - [ ] Built-in roles: Owner, Admin, Member, Guest, Billing
  - [ ] Custom roles with granular permissions
  - [ ] Permission inheritance (org → project → resource)
- [ ] Attribute-based access control (ABAC) for advanced policies
- [ ] Permission check API for all apps
- [ ] Role assignment UI
- [ ] Permission audit view (who has access to what)

#### API Keys & Service Accounts
- [ ] Personal API key generation
- [ ] Org-level API key management
- [ ] API key scoping (per-app, per-permission)
- [ ] API key expiration
- [ ] API key usage tracking
- [ ] Service account creation (non-human identity)
- [ ] Service account key rotation

#### Audit & Compliance
- [ ] Authentication event logging (login, logout, MFA, failed attempts)
- [ ] Admin action logging
- [ ] Permission change logging
- [ ] Audit log search and filtering
- [ ] Audit log export (CSV, JSON)
- [ ] Audit log retention policies
- [ ] Real-time audit stream to external SIEM

#### Gate UI
- [x] Login page with org branding
- [x] Registration page
- [x] Forgot password flow
- [x] Reset password flow
- [x] MFA enrollment flow
- [x] MFA challenge flow
- [x] Profile settings page
- [x] Security settings page (sessions, MFA, API keys)
- [x] Organization settings page (admin)
- [x] User management page (admin)
- [ ] Role management page (admin)
- [x] Audit log viewer (admin)
- [ ] Branding customization page (admin)

### 1.2 Atlas — Project Management

#### Project Management Core
- [ ] Project CRUD with templates
- [ ] Project archiving and restoration
- [ ] Project cloning/duplication
- [ ] Project favorites and pinning
- [ ] Project categories/folders
- [ ] Project-level settings (visibility, default view, custom fields)
- [ ] Project readme/wiki page
- [ ] Project activity feed

#### Task Management
- [ ] Task CRUD with rich description (Tiptap)
- [ ] Task types: Task, Bug, Story, Epic, Sub-task
- [ ] Task status workflow (customizable per project)
- [ ] Task priority: Critical, High, Medium, Low, None
- [ ] Task assignee (single and multiple)
- [ ] Task labels/tags
- [ ] Task due dates and date ranges
- [ ] Task time estimates and tracking
- [ ] Task dependencies (blocks, blocked-by, related-to)
- [ ] Task parent/child hierarchy (sub-tasks)
- [ ] Task recurring (daily, weekly, monthly, custom)
- [ ] Task templates
- [ ] Task duplication
- [ ] Task move between projects
- [ ] Task bulk actions (assign, label, status, priority, delete)
- [ ] Task history/activity log
- [ ] Task watchers/subscribers
- [ ] Task mentions (@user, #task)

#### Views
- [ ] Board view (Kanban)
  - [ ] Drag-and-drop between columns
  - [ ] Column customization (add, remove, rename, reorder)
  - [ ] WIP limits per column
  - [ ] Swimlanes (group by assignee, priority, label)
  - [ ] Card preview customization (which fields to show)
- [ ] List view
  - [ ] Sortable columns
  - [ ] Grouping (by status, priority, assignee, label, sprint)
  - [ ] Inline editing
  - [ ] Expandable rows
- [ ] Calendar view
  - [ ] Tasks on due dates
  - [ ] Drag to reschedule
  - [ ] Integration with Orbit Calendar
- [ ] Gantt chart view
  - [ ] Task bars with dependencies
  - [ ] Critical path highlighting
  - [ ] Drag to resize/move
  - [ ] Zoom levels (day, week, month, quarter)
  - [ ] Baseline comparison
- [ ] Timeline view
  - [ ] Chronological activity view
  - [ ] Milestone markers
- [ ] Table view
  - [ ] Spreadsheet-like editing
  - [ ] Custom columns
  - [ ] Formulas (basic)
  - [ ] Freeze columns
- [ ] Dashboard view
  - [ ] Project health KPIs
  - [ ] Burndown/burnup charts
  - [ ] Velocity chart
  - [ ] Task distribution charts
  - [ ] Overdue tasks widget
  - [ ] Team workload widget

#### Sprints & Agile
- [ ] Sprint creation (start date, end date, goal)
- [ ] Sprint backlog management
- [ ] Sprint board
- [ ] Sprint burndown chart
- [ ] Sprint velocity tracking
- [ ] Sprint retrospective notes
- [ ] Sprint completion and carryover
- [ ] Backlog grooming view
- [ ] Story points estimation

#### Resource Management
- [ ] Team workload view (who is overloaded/underloaded)
- [ ] Capacity planning (hours per person per week)
- [ ] Resource allocation across projects
- [ ] Availability calendar (vacations, leaves)
- [ ] Utilization reports

#### Automations
- [ ] Rule-based automations
  - [ ] When status changes → assign to, notify, update field
  - [ ] When priority is critical → notify channel, escalate
  - [ ] When due date is approaching → remind assignee
  - [ ] When task created → auto-assign, set defaults
  - [ ] When label added → move to column
- [ ] Custom automation builder (trigger → condition → action)
- [ ] Scheduled automations (daily/weekly cleanup, reports)
- [ ] Automation execution log

#### Integrations
- [ ] Atlas ↔ Calendar: push task deadlines as events
- [ ] Atlas ↔ Mail: convert email to task
- [ ] Atlas ↔ Connect: task notifications in channels
- [ ] Atlas ↔ Meet: link meetings to projects/tasks
- [ ] Atlas ↔ Writer: link documents to tasks
- [ ] Atlas ↔ Planet: client portal, link deals to projects
- [ ] Atlas ↔ TurboTick: bidirectional ticket↔task linking
- [ ] Atlas ↔ Git: branch/PR/commit linking (GitHub, GitLab)
- [ ] Atlas → Webhooks: send task events to external systems

#### Client Portal
- [ ] Shared project view for external clients
- [ ] Client can view task status
- [ ] Client can comment on tasks
- [ ] Client can upload files
- [ ] Client access is scoped (no internal tasks visible)
- [ ] Client branding options
- [ ] Client invitation flow (via Planet CRM contact)

### 1.3 Connect — Enterprise Messaging

#### Core Messaging
- [ ] Real-time message delivery via WebSocket
- [ ] Message types: text, file, image, video, audio, code block, link preview
- [ ] Rich text formatting (bold, italic, strikethrough, lists, code, quotes)
- [ ] Markdown support
- [ ] Emoji picker with custom emoji support
- [ ] Emoji reactions on messages
- [ ] Message threading (replies)
- [ ] Message editing (with edit history)
- [ ] Message deletion (soft delete with "message deleted" placeholder)
- [ ] Message pinning
- [ ] Message bookmarking/saving
- [ ] Message forwarding to another channel/DM
- [ ] Message search (full-text, filters by sender, date, channel)
- [ ] Message link previews (unfurling)
- [ ] @mention users (with notification)
- [ ] @channel / @here mentions
- [ ] Message read receipts
- [ ] Typing indicators

#### Channels
- [ ] Public channels (visible to all org members)
- [ ] Private channels (invite-only)
- [ ] Channel creation with name, description, purpose
- [ ] Channel topics
- [ ] Channel archiving
- [ ] Channel member management (add, remove, role)
- [ ] Channel notification preferences (all, mentions, none)
- [ ] Channel sections/categories (sidebar organization)
- [ ] Channel favorites/starring
- [ ] Channel search
- [ ] Default channels for new members

#### Direct Messages
- [ ] 1:1 direct messages
- [ ] Group DMs (up to 8 people)
- [ ] DM search

#### File Sharing
- [ ] Drag-and-drop file upload
- [ ] File preview in-chat (images, PDFs, videos)
- [ ] File gallery per channel
- [ ] File size limits (configurable per org)
- [ ] File type restrictions (configurable)
- [ ] Integration with Orbit Files (MinIO)

#### Voice & Video (in-chat)
- [ ] Start voice call from DM
- [ ] Start video call from DM (launches Meet)
- [ ] Huddle (persistent voice channel)
- [ ] Screen sharing in huddle

#### Bots & Integrations
- [ ] Bot framework (register bots, handle commands)
- [ ] Slash commands (`/atlas create task`, `/meet start`, etc.)
- [ ] Incoming webhooks (post from external services)
- [ ] Outgoing webhooks (send events to external services)
- [ ] Atlas bot (task updates in channels)
- [ ] Calendar bot (meeting reminders)
- [ ] Mail bot (email notifications)
- [ ] Meet bot (meeting links)
- [ ] TurboTick bot (ticket updates)
- [ ] AI bot (Orbit AI assistant in chat)

#### Admin & Compliance
- [ ] Message retention policies (per org, per channel)
- [ ] Message export for compliance
- [ ] Data loss prevention (DLP) rules
- [ ] Admin message deletion
- [ ] Channel creation permissions
- [ ] Guest access with limited channels
- [ ] User presence (online, away, busy, offline)
- [ ] Custom status with emoji
- [ ] Do not disturb schedule

### 1.4 Mail — Email Client

#### Core Email
- [x] Inbox with conversation threading
- [x] Compose email (rich text editor — ReactQuill, full-page + FloatingComposer)
- [x] Reply, Reply All, Forward
- [x] CC, BCC
- [x] Drafts auto-save (30s interval + manual save)
- [x] Sent mail folder
- [x] Trash folder with auto-purge
- [x] Archive functionality
- [x] Star/flag emails (toggle in list + reading pane, Starred folder)
- [x] Mark read/unread
- [ ] Snooze (reappear at specified time)
- [ ] Schedule send (send later)
- [ ] Undo send (configurable delay: 5s, 10s, 30s)
- [x] Email signatures (per-user, in Settings → Signature tab)
- [ ] Email templates
- [ ] Bulk actions (archive, delete, mark read, move)
- [x] Email search (cross-app unified search via /integrations/unified-search)

#### Organization & Labels
- [ ] Label/folder creation and management
- [ ] Color-coded labels
- [ ] Nested labels/folders
- [ ] Smart/filter labels (auto-categorize)
- [ ] Drag-and-drop to label
- [ ] Multiple labels per email

#### Filters & Rules
- [ ] Auto-filter rules (from, to, subject, contains)
- [ ] Actions: label, archive, delete, forward, star, mark read
- [ ] Apply existing rules to current inbox
- [ ] Import/export filter rules

#### Attachments
- [ ] File attachments (drag-and-drop, file picker)
- [ ] Inline images
- [ ] Attachment preview (images, PDFs, office docs)
- [ ] Save attachment to Orbit Files
- [ ] Attachment size limits
- [ ] Virus scanning on attachments

#### Multi-Account
- [ ] Multiple email accounts per user
- [ ] Unified inbox across accounts
- [ ] Send-as (choose sending address)
- [ ] Account-specific signatures

#### Security
- [ ] DKIM signing
- [ ] SPF validation
- [ ] DMARC enforcement
- [ ] Spam filtering (Rspamd integration)
- [ ] Phishing detection and warnings
- [ ] Encrypted email support (S/MIME or PGP)
- [ ] External image blocking with click-to-load
- [ ] Link safety checking

#### Integrations
- [x] Mail ↔ Atlas: convert email to task (one-click, ✨ Task button)
- [ ] Mail ↔ Planet: auto-associate emails with CRM contacts/deals
- [x] Mail ↔ TurboTick: convert email to support ticket (mobile long-press sheet)
- [ ] Mail ↔ Calendar: detect meeting invites, show accept/decline
- [ ] Mail ↔ Connect: share email to channel
- [ ] Mail ↔ Writer: save email content as document

### 1.5 Meet — Video Conferencing

#### Core Video
- [ ] HD video calls (720p, 1080p)
- [ ] Audio calls
- [ ] Pre-join device check (camera, mic, speaker selection)
- [ ] In-call camera toggle
- [ ] In-call microphone toggle
- [ ] Speaker view (active speaker highlight)
- [ ] Gallery view (grid of participants)
- [ ] Participant sidebar with list
- [ ] Hand raising
- [ ] In-call reactions (thumbs up, clap, etc.)
- [ ] Virtual backgrounds (blur, images, custom upload)
- [ ] Noise suppression
- [ ] Echo cancellation
- [ ] Low-bandwidth mode
- [ ] Network quality indicator

#### Screen Sharing
- [ ] Share entire screen
- [ ] Share application window
- [ ] Share browser tab (with audio)
- [ ] Annotation tools on shared screen
- [ ] Remote control (with permission)

#### Chat & Communication
- [ ] In-meeting chat
- [ ] Chat persists after meeting ends
- [ ] File sharing in meeting chat
- [ ] Private messages to individuals
- [ ] Polls/voting

#### Recording & Transcription
- [ ] Cloud recording
- [ ] Local recording
- [ ] Recording consent notification
- [ ] Recording access management
- [ ] Automatic transcription (AI)
- [ ] Speaker-attributed transcription
- [ ] Transcript search
- [ ] Transcript export (TXT, SRT, VTT)
- [ ] AI meeting summary generation
- [ ] AI action items extraction → Atlas tasks

#### Meeting Management
- [ ] Instant meeting (generate link)
- [ ] Scheduled meeting (via Calendar integration)
- [ ] Recurring meetings
- [ ] Meeting lobby/waiting room
- [ ] Host controls (mute all, remove participant, lock meeting)
- [ ] Co-host assignment
- [ ] Meeting password protection
- [ ] Meeting capacity limits
- [ ] Meeting timer/duration display

#### Breakout Rooms
- [ ] Create breakout rooms
- [ ] Auto-assign participants
- [ ] Manual assign participants
- [ ] Host can broadcast message to all rooms
- [ ] Timer for breakout sessions
- [ ] Return all to main room

#### Integrations
- [ ] Meet ↔ Calendar: auto-create Meet links for calendar events
- [ ] Meet ↔ Control Center: link meetings to agendas and notes
- [ ] Meet ↔ Atlas: create tasks from meeting action items
- [ ] Meet ↔ Connect: post meeting link in channel
- [ ] Meet ↔ Writer: save meeting notes as document
- [ ] Meet → External: dial-in phone number (SIP/PSTN gateway)

### 1.6 Writer — Collaborative Documents

#### Editor Core
- [x] Block-based editor (contenteditable with toolbar)
- [x] Paragraph, headings (H1-H3)
- [x] Bold, italic, underline, strikethrough
- [x] Bullet list, numbered list
- [x] Blockquote
- [ ] Code block with syntax highlighting
- [x] Horizontal rule (divider block)
- [ ] Tables (with merge, resize, color)
- [ ] Images (upload, URL, resize, caption)
- [ ] Videos (embed YouTube, Vimeo, upload)
- [ ] File attachments
- [ ] Embeds (links with preview cards)
- [ ] Math equations (LaTeX)
- [ ] Callout/admonition blocks (info, warning, tip, danger)
- [ ] Toggle/accordion blocks
- [ ] Columns layout (2, 3 column)
- [ ] Divider block
- [ ] Table of contents (auto-generated)
- [ ] Slash command menu (/ to insert any block type)
- [ ] Drag-and-drop block reordering
- [ ] Block-level comments

#### Collaboration
- [ ] Real-time co-editing (Yjs CRDT)
- [ ] Cursor presence (see others' cursors with names/colors)
- [ ] Selection presence (see others' selections)
- [ ] Commenting system
  - [ ] Inline comments on text selections
  - [ ] Comment threads (replies)
  - [ ] Resolve/unresolve comments
  - [ ] @mention in comments
  - [ ] Comment notifications
- [ ] Suggesting mode (track changes)
  - [ ] Accept/reject suggestions
  - [ ] Suggestion diff view
- [ ] Version history
  - [ ] Auto-save versions
  - [ ] Named versions (manual save points)
  - [ ] Version comparison (diff view)
  - [ ] Restore previous version
  - [ ] Version author tracking

#### Document Management
- [ ] Folder/workspace organization
- [ ] Document favorites/starring
- [ ] Document search (full-text)
- [ ] Recent documents
- [ ] Document templates
  - [ ] Meeting notes template
  - [ ] Project brief template
  - [ ] RFC/proposal template
  - [ ] Weekly update template
  - [ ] Custom templates
- [ ] Document duplication
- [ ] Document archiving
- [ ] Document trash and recovery
- [ ] Document cover image
- [ ] Document icon/emoji

#### Sharing & Permissions
- [ ] Share with org members (view, comment, edit)
- [ ] Share via link (public, anyone with link, org-only)
- [ ] Password-protected links
- [ ] Expiring links
- [ ] Guest access (external collaborators)
- [ ] Document-level permissions override
- [ ] Folder-level inherited permissions

#### Export & Import
- [ ] Export to PDF
- [ ] Export to DOCX
- [ ] Export to Markdown
- [ ] Export to HTML
- [ ] Import from DOCX
- [ ] Import from Markdown
- [ ] Import from Google Docs
- [ ] Import from Notion
- [ ] Copy-paste from web (clean HTML parsing)

#### Integrations
- [ ] Writer ↔ Atlas: embed task lists from Atlas
- [ ] Writer ↔ Meet: auto-create meeting notes doc
- [ ] Writer ↔ Mail: share doc via email
- [ ] Writer ↔ Connect: share doc in channel
- [ ] Embed Writer docs in other apps

### 1.7 Calendar — Enterprise Scheduling

#### Calendar Core
- [ ] Day view
- [ ] Week view
- [ ] Month view
- [ ] Year view (overview)
- [ ] Agenda/list view
- [ ] Event creation (title, time, location, description, color)
- [ ] All-day events
- [ ] Multi-day events
- [ ] Recurring events (daily, weekly, monthly, yearly, custom)
- [ ] Event editing (single, this and following, all occurrences)
- [ ] Event deletion
- [ ] Event duplication
- [ ] Drag-and-drop event rescheduling
- [ ] Drag to resize event duration
- [ ] Event reminders (notification, email) at configurable times
- [ ] Multiple calendars (personal, team, project)
- [ ] Calendar color coding
- [ ] Calendar overlay (view multiple calendars)
- [ ] Calendar sharing (view, edit)
- [ ] Calendar subscribe (read-only external)

#### Scheduling
- [ ] Availability engine
  - [ ] Working hours configuration per user
  - [ ] Time-off/vacation blocking
  - [ ] Automatic free/busy detection
  - [ ] Find available time slots for group meetings
- [ ] Scheduling links (like Calendly)
  - [ ] Personal scheduling page
  - [ ] Custom availability per link
  - [ ] Buffer time between meetings
  - [ ] Maximum meetings per day
  - [ ] Minimum notice period
  - [ ] Custom questions for invitees
  - [ ] Confirmation and reminder emails
- [ ] Room/resource booking
  - [ ] Meeting room calendar
  - [ ] Equipment booking
  - [ ] Room amenities and capacity filtering
  - [ ] Conflict prevention
  - [ ] Auto-release on no-show

#### Integrations
- [ ] Calendar ↔ Meet: auto-generate Meet link for virtual events
- [ ] Calendar ↔ Atlas: show task deadlines on calendar
- [ ] Calendar ↔ Control Center: link calendar events to meeting agendas
- [ ] Calendar ↔ Planet: sales follow-up scheduling
- [ ] Calendar ↔ Connect: meeting reminders in channels
- [ ] Calendar ↔ Mail: email invitations (accept/decline/tentative)
- [ ] iCal feed export/import
- [ ] Google Calendar sync
- [ ] Outlook Calendar sync
- [ ] CalDAV protocol support

#### Time & Timezone
- [ ] Timezone detection (auto)
- [ ] Timezone display toggle (show in multiple TZs)
- [ ] World clock widget
- [ ] Working hours across timezones for team scheduling

### 1.8 Planet — Advanced CRM

#### Contact Management
- [ ] Contact CRUD (name, email, phone, company, title, social links)
- [ ] Contact import (CSV, vCard)
- [ ] Contact export
- [ ] Contact merge/dedup
- [ ] Contact tags/segments
- [ ] Contact activity timeline (all interactions across Orbit)
- [ ] Contact enrichment (auto-fill from public data)
- [ ] Contact notes
- [ ] Contact task assignments
- [ ] Contact company/organization association
- [ ] Company CRUD (name, domain, industry, size, revenue)
- [ ] Company hierarchy (parent/subsidiary)
- [ ] Company contacts list

#### Sales Pipeline
- [ ] Pipeline CRUD (stages, probabilities, colors)
- [ ] Multiple pipelines per org
- [ ] Deal CRUD (title, value, probability, close date, stage)
- [ ] Deal drag-and-drop between stages
- [ ] Deal history/activity log
- [ ] Deal notes
- [ ] Deal tasks
- [ ] Deal attachments
- [ ] Deal contacts/company association
- [ ] Deal products/line items
- [ ] Deal win/loss reasons
- [ ] Weighted pipeline value
- [ ] Pipeline health metrics

#### Lead Management
- [ ] Lead capture forms (embeddable)
- [ ] Lead scoring (manual rules + AI)
- [ ] Lead sources tracking
- [ ] Lead assignment (round-robin, rules-based)
- [ ] Lead qualification stages
- [ ] Lead conversion to deal
- [ ] Lead nurturing workflows

#### Email Sequences
- [ ] Multi-step email sequences
- [ ] Personalization variables
- [ ] Send schedule (delays between steps)
- [ ] A/B testing subject lines
- [ ] Open/click tracking
- [ ] Auto-stop on reply
- [ ] Sequence templates
- [ ] Sequence analytics (open rate, reply rate, bounce rate)

#### Reporting & Analytics
- [ ] Revenue forecast (by stage, by rep, by period)
- [ ] Pipeline conversion rates
- [ ] Sales velocity metrics
- [ ] Win/loss analysis
- [ ] Rep performance dashboard
- [ ] Activity metrics (calls, emails, meetings per rep)
- [ ] Custom reports builder
- [ ] Report scheduling (email weekly/monthly)
- [ ] Dashboard widgets (drag-and-drop)

#### Integrations
- [ ] Planet ↔ Mail: auto-associate emails with contacts/deals
- [ ] Planet ↔ Calendar: schedule follow-ups from CRM
- [ ] Planet ↔ Connect: deal channel auto-creation
- [ ] Planet ↔ Atlas: link deals to delivery projects
- [ ] Planet ↔ Meet: log meeting outcomes on deals
- [ ] Planet ↔ Writer: proposals and contracts linked to deals
- [ ] Planet ↔ TurboTick: customer support ticket visibility on contact

---

## Phase 2: Orbit AI — The Intelligence Layer

### 2.1 AI Service Architecture

- [ ] Create `/OrbitAI/` service directory
- [ ] Set up FastAPI backend with async endpoints
- [ ] Configure Claude API integration (primary LLM)
- [ ] Configure OpenAI API integration (fallback)
- [ ] Implement LLM gateway (route to providers, handle fallback)
- [ ] Implement token usage tracking per org
- [ ] Implement rate limiting per org/user
- [ ] Implement prompt template registry
- [ ] Implement streaming responses (SSE)
- [ ] Set up vector database (pgvector or Qdrant)
- [ ] Implement embedding pipeline (text → vectors)
- [ ] Implement RAG (Retrieval-Augmented Generation) pipeline
- [ ] Build context assembly engine (gather cross-app data for prompts)
- [ ] Implement conversation memory (chat history per user)
- [ ] Implement tool/function calling framework
- [ ] Set up AI action executor (take actions across apps)
- [ ] Build permission-aware AI (respect user's access per app)
- [ ] Implement AI audit logging (every AI action logged)
- [ ] Set up AI cost dashboard (usage per org, per feature)
- [ ] Add AI kill switch per org (admin can disable)

### 2.2 Knowledge Graph

- [ ] Design unified entity schema (contacts, tasks, docs, emails, meetings, deals)
- [ ] Build entity extraction pipeline from each app
- [ ] Build relationship mapping (who works with whom, what's related to what)
- [ ] Implement entity resolution (same person across apps)
- [ ] Build incremental indexing (real-time updates via EventBus)
- [ ] Build full reindex capability
- [ ] Add semantic search across all entities
- [ ] Build "entity page" API (everything about a person/project/company)

### 2.3 AI Features — Per App

#### Writer AI
- [ ] AI writing assistant (continue writing, expand, shorten)
- [ ] AI tone adjustment (formal, casual, technical)
- [ ] AI translation (multi-language)
- [ ] AI grammar and spelling check
- [ ] AI summarize document
- [ ] AI generate document from prompt
- [ ] AI extract action items from document
- [ ] AI generate table of contents
- [ ] AI content suggestions based on context

#### Mail AI
- [ ] AI email compose (describe intent → draft email)
- [ ] AI email reply suggestions (one-click reply options)
- [ ] AI email summarize (long email → bullet points)
- [ ] AI email categorization (auto-label)
- [ ] AI email priority detection
- [ ] AI email sentiment analysis
- [ ] AI smart unsubscribe suggestions
- [ ] AI email thread summary

#### Atlas AI
- [ ] AI task description generation from title
- [ ] AI task breakdown (epic → stories → tasks)
- [ ] AI sprint planning suggestions
- [ ] AI effort estimation
- [ ] AI task duplicate detection
- [ ] AI project risk analysis
- [ ] AI status update generation (weekly summary)
- [ ] AI task assignment suggestions (based on workload/expertise)

#### Connect AI
- [ ] AI message summarize (catch up on channel)
- [ ] AI thread summary
- [ ] AI response suggestions
- [ ] AI channel digest (daily/weekly)
- [ ] AI language translation in-chat
- [ ] AI-powered search (natural language)

#### Meet AI
- [ ] Real-time transcription
- [ ] Speaker attribution in transcription
- [ ] AI meeting summary (generated after meeting ends)
- [ ] AI action items extraction
- [ ] AI key decisions extraction
- [ ] AI meeting highlights (important moments)
- [ ] AI follow-up email draft
- [ ] Live captions

#### Calendar AI
- [ ] AI scheduling assistant ("find a time for me and John next week")
- [ ] AI meeting agenda suggestions
- [ ] AI time blocking recommendations
- [ ] AI reschedule suggestions (conflict resolution)

#### Planet AI
- [ ] AI lead scoring
- [ ] AI deal win probability
- [ ] AI next-best-action recommendations
- [ ] AI email sequence content generation
- [ ] AI sales call prep (summarize contact history)
- [ ] AI pipeline forecast
- [ ] AI churn risk detection

#### Search AI
- [ ] Natural language search ("emails from John about the contract last month")
- [ ] AI search result ranking
- [ ] AI answer generation (not just links, synthesized answers)
- [ ] AI follow-up question suggestions
- [ ] Cross-app search with context

### 2.4 Orbit Assistant (Chat Agent)

- [ ] Persistent chat panel accessible from any app (slide-in drawer)
- [ ] Invoke via keyboard shortcut (Cmd+J or similar)
- [ ] Conversational interface with streaming responses
- [ ] Context-aware (knows which app/page you're on)
- [ ] Can read data from all apps (with user permissions)
- [ ] Can take actions across apps:
  - [ ] "Create a task in Atlas called..."
  - [ ] "Send an email to..."
  - [ ] "Schedule a meeting with..."
  - [ ] "Find the document about..."
  - [ ] "What's the status of the Q3 deal?"
  - [ ] "Summarize yesterday's messages in #engineering"
- [ ] Action confirmation before executing (user must approve)
- [ ] Conversation history persistence
- [ ] Suggested prompts based on context
- [ ] Multi-turn conversations with memory
- [ ] Handoff to human (escalate to Connect channel)

### 2.5 Workflow Automation (AI-Powered)

- [ ] Natural language workflow definition
  - [ ] "When a deal closes, create a project, schedule a kickoff, notify the team"
  - [ ] "Every Monday morning, send me a summary of overdue tasks"
  - [ ] "When a support ticket is critical, page the on-call in Connect"
- [ ] Visual workflow builder (node-based, drag-and-drop)
- [ ] Trigger types: event, schedule, webhook, manual
- [ ] Condition nodes (if/else, filters)
- [ ] Action nodes (one per app)
- [ ] Delay/wait nodes
- [ ] Loop nodes
- [ ] Error handling (retry, fallback, notify)
- [ ] Workflow execution log
- [ ] Workflow versioning
- [ ] Workflow templates library
- [ ] Workflow testing/dry-run mode

---

## Phase 3: Experience Layer — One Product Feel

### 3.1 Orbit Shell (Unified App Shell)

- [ ] Upgrade Orbit Bar from web component to React component
- [ ] Global app switcher with icons, search, and recent apps
- [ ] Unified notification center
  - [ ] Aggregate notifications from all apps
  - [ ] Notification categories (tasks, messages, emails, meetings, mentions)
  - [ ] Mark as read (individual, all)
  - [ ] Notification preferences per app per channel (push, email, in-app)
  - [ ] Do not disturb mode
  - [ ] Snooze notifications
  - [ ] Notification actions (reply, complete task, accept meeting)
- [ ] Global search (Cmd+K)
  - [ ] Search across all apps simultaneously
  - [ ] Result categories (tasks, messages, emails, docs, contacts, meetings)
  - [ ] Recent searches
  - [ ] Search filters
  - [ ] Preview panel
  - [ ] Keyboard navigation
  - [ ] Quick actions from search results
- [ ] Command palette
  - [ ] All app actions accessible via keyboard
  - [ ] Recently used commands
  - [ ] Contextual commands (based on current app/page)
  - [ ] Custom keyboard shortcuts
- [ ] Quick create menu
  - [ ] Create task (any project)
  - [ ] Create event
  - [ ] Create document
  - [ ] Compose email
  - [ ] Start meeting
  - [ ] Create contact
  - [ ] Create deal
- [ ] User presence across shell (who's online)
- [ ] Org switcher in shell
- [ ] Theme toggle in shell
- [ ] Settings link in shell
- [ ] Help/feedback link in shell

### 3.2 Unified Contact Graph

- [ ] Single contact record shared across Planet, Mail, Connect, Calendar, Meet
- [ ] Contact profile page showing:
  - [ ] All emails exchanged
  - [ ] All tasks involving this person
  - [ ] All meetings attended together
  - [ ] All chat messages
  - [ ] All documents shared
  - [ ] All deals in CRM
  - [ ] All support tickets
  - [ ] Activity timeline
- [ ] Click any person's name in any app → contact profile
- [ ] Smart contact suggestions (auto-complete from unified directory)
- [ ] Contact sync with external address books

### 3.3 Activity Feed

- [ ] Global activity feed ("what happened while I was away")
- [ ] Personalized (based on your projects, channels, contacts)
- [ ] Filterable by app, time range, person
- [ ] Group related activities (3 comments on one task → single entry)
- [ ] Quick actions from feed (reply, complete, view)
- [ ] Mark as read
- [ ] Feed widget embeddable in dashboards

### 3.4 Unified Settings

- [ ] Central settings page for all apps
- [ ] Profile settings (name, avatar, bio, timezone)
- [ ] Notification settings (per app, per event type)
- [ ] Appearance settings (theme, density, language)
- [ ] Keyboard shortcuts customization
- [ ] Connected accounts (email, calendar, integrations)
- [ ] Security settings (password, MFA, sessions, API keys)
- [ ] Data export settings (GDPR)

### 3.5 Onboarding Experience

- [ ] Welcome wizard for new users
  - [ ] Profile setup
  - [ ] Team/org selection
  - [ ] App tour (interactive)
  - [ ] Import data wizard
  - [ ] Invite team members
- [ ] Per-app onboarding tips
- [ ] Feature discovery tooltips
- [ ] Checklist-style onboarding (complete 5 tasks to get started)
- [ ] Admin onboarding (org setup, branding, integrations)

### 3.6 Orbit Mobile App

#### Setup
- [ ] Initialize React Native project
- [ ] Configure navigation (React Navigation)
- [ ] Configure state management (Zustand)
- [ ] Configure API client (authenticated via Gate)
- [ ] Configure push notifications (Firebase)
- [ ] Configure deep linking
- [ ] Configure biometric authentication
- [ ] Set up CI/CD for iOS and Android builds

#### Mobile — Connect
- [ ] Channel list
- [ ] Message list with real-time updates
- [ ] Message compose with attachments
- [ ] Push notifications for messages/mentions
- [ ] Message reactions
- [ ] Thread view
- [ ] DM view
- [ ] Presence indicators
- [ ] Voice message recording

#### Mobile — Mail
- [ ] Inbox list
- [ ] Email thread view
- [ ] Compose email
- [ ] Reply/forward
- [ ] Push notifications for new emails
- [ ] Swipe actions (archive, delete, snooze)
- [ ] Search
- [ ] Attachment handling

#### Mobile — Calendar
- [ ] Day/week/month views
- [ ] Event creation
- [ ] Event editing
- [ ] Push notifications for reminders
- [ ] Quick RSVP from notification
- [ ] Join meeting link

#### Mobile — Meet
- [ ] Join meeting (video/audio)
- [ ] Camera/mic controls
- [ ] Speaker/gallery view
- [ ] Screen sharing (share mobile screen)
- [ ] Chat in meeting
- [ ] Meeting creation

#### Mobile — Atlas
- [ ] Task list view
- [ ] Task detail view
- [ ] Update task status
- [ ] Comment on tasks
- [ ] Push notifications for assignments/mentions
- [ ] Quick create task

#### Mobile — General
- [ ] Global search
- [ ] Notification center
- [ ] Profile/settings
- [ ] Offline mode (queue actions, sync when online)
- [ ] Widget support (iOS/Android)
  - [ ] Calendar widget
  - [ ] Tasks widget
  - [ ] Unread messages widget
- [ ] Share extension (share from other apps into Orbit)
- [ ] App Store submission (iOS)
- [ ] Play Store submission (Android)

### 3.7 Orbit Desktop App

- [ ] Choose framework: Tauri (lightweight) or Electron
- [ ] Window management (multiple windows for different apps)
- [ ] System tray icon with notification badge
- [ ] Native notifications
- [ ] Deep linking (orbit://app/resource)
- [ ] Auto-update mechanism
- [ ] Offline mode
- [ ] Keyboard shortcuts (OS-level)
- [ ] Menu bar integration
- [ ] Build for macOS (.dmg)
- [ ] Build for Windows (.exe/.msi)
- [ ] Build for Linux (.AppImage/.deb)

---

## Phase 4: Platform & Extensibility

### 4.1 Public API

- [ ] Design RESTful API for all core apps
- [ ] API versioning strategy (v1, v2)
- [ ] OpenAPI 3.1 spec for all endpoints
- [ ] API authentication via Gate API keys
- [ ] API rate limiting (per key, per endpoint)
- [ ] API usage analytics
- [ ] API documentation portal (interactive, like Stripe docs)
- [ ] API SDKs
  - [ ] JavaScript/TypeScript SDK
  - [ ] Python SDK
  - [ ] Go SDK
  - [ ] CLI tool
- [ ] GraphQL API (optional, for complex queries)
- [ ] Webhook delivery system
  - [ ] Event subscription management
  - [ ] Webhook signing (HMAC)
  - [ ] Retry with exponential backoff
  - [ ] Webhook logs and debugging
  - [ ] Webhook testing tool

### 4.2 Plugin/Extension SDK

- [ ] Define plugin manifest format (JSON)
- [ ] Plugin types: sidebar panel, command, widget, bot, theme
- [ ] Plugin sandboxing (iframe for UI, API-only for backend)
- [ ] Plugin permissions model
- [ ] Plugin lifecycle hooks (install, activate, deactivate, uninstall)
- [ ] Plugin storage API (key-value per plugin per org)
- [ ] Plugin UI components (inherit Orbit design system)
- [ ] Plugin CLI for development
- [ ] Plugin documentation and tutorials
- [ ] Plugin testing framework

### 4.3 Marketplace

- [ ] Marketplace web UI
- [ ] Plugin listing (categories, search, featured)
- [ ] Plugin detail page (description, screenshots, reviews, installs)
- [ ] One-click install/uninstall
- [ ] Plugin ratings and reviews
- [ ] Plugin developer portal
- [ ] Plugin submission and review process
- [ ] Plugin analytics (installs, active users, errors)
- [ ] First-party plugins (built by Orbit team)
  - [ ] Jira import/sync plugin
  - [ ] Slack import plugin
  - [ ] Google Workspace connector
  - [ ] Microsoft 365 connector
  - [ ] GitHub/GitLab integration
  - [ ] Figma integration
  - [ ] Zapier/Make connector
  - [ ] Salesforce connector
  - [ ] HubSpot connector

### 4.4 Admin Console

- [ ] Organization overview dashboard
- [ ] User management (list, invite, suspend, delete, role change)
- [ ] Group management (create, add/remove members)
- [ ] App management (enable/disable apps per org)
- [ ] Feature flags per org
- [ ] Usage analytics (DAU, MAU, storage, API calls per app)
- [ ] Billing management
  - [ ] Plan selection (Free, Pro, Enterprise)
  - [ ] Seat management
  - [ ] Storage usage and limits
  - [ ] AI usage and limits
  - [ ] Invoice history
  - [ ] Payment method management
  - [ ] Upgrade/downgrade flow
- [ ] Branding settings (logo, colors, domain)
- [ ] Security policies
  - [ ] Password policy (length, complexity, expiration)
  - [ ] MFA enforcement
  - [ ] Session duration
  - [ ] IP allowlist
  - [ ] Device management
- [ ] Data governance
  - [ ] Data retention policies
  - [ ] Data export (full org)
  - [ ] Data deletion request
  - [ ] DLP rules
- [ ] Audit log viewer
- [ ] Integration management (connected apps, API keys, webhooks)
- [ ] Plugin management (installed plugins, permissions)

### 4.5 White-Label & Self-Hosted

- [ ] Complete white-label capability (no Orbit branding)
- [ ] Custom domain mapping
- [ ] Custom email domain
- [ ] Docker Compose for self-hosted deployment
- [ ] Kubernetes Helm chart
- [ ] Installation wizard for self-hosted
- [ ] Backup and restore tooling
- [ ] Upgrade/migration tooling
- [ ] Health check endpoints
- [ ] License key management (for enterprise self-hosted)

---

## Phase 5: Infrastructure & DevOps

### 5.1 Monorepo Conversion

- [ ] Evaluate monorepo tools (npm workspaces, Turborepo, Nx)
- [ ] Create root `package.json` with workspaces
- [ ] Move shared dependencies to root
- [ ] Create shared packages:
  - [ ] `@orbit/ui` (React components)
  - [ ] `@orbit/tokens` (design tokens)
  - [ ] `@orbit/tailwind-preset`
  - [ ] `@orbit/hooks` (shared React hooks)
  - [ ] `@orbit/auth` (Gate client SDK)
  - [ ] `@orbit/api-client` (authenticated API helpers)
  - [ ] `@orbit/event-bus-client` (EventBus subscription helpers)
  - [ ] `@orbit/types` (shared TypeScript types)
  - [ ] `@orbit/utils` (shared utilities)
- [ ] Configure Turborepo/Nx for build orchestration
- [ ] Set up dependency graph (build order)
- [ ] Configure caching for builds
- [ ] Migrate all app `package.json` files
- [ ] Verify all apps build and run after migration
- [ ] Update Docker builds for monorepo structure

### 5.2 CI/CD Pipeline

- [ ] Choose CI platform (GitHub Actions, GitLab CI)
- [ ] Lint pipeline (ESLint + Prettier for all apps)
- [ ] Type check pipeline (TypeScript strict mode)
- [ ] Unit test pipeline (Vitest)
- [ ] Integration test pipeline
- [ ] E2E test pipeline (Playwright)
- [ ] Build pipeline (all apps)
- [ ] Docker image build pipeline
- [ ] Security scanning (Snyk, Trivy)
- [ ] Dependency audit (npm audit)
- [ ] Preview deployments (per PR)
- [ ] Staging deployment (on merge to develop)
- [ ] Production deployment (on merge to main)
- [ ] Rollback automation
- [ ] Release notes generation (from commits/PRs)
- [ ] Version bumping (semantic versioning)

### 5.3 Testing Strategy

- [ ] Unit test coverage target: 80% for all backend services
- [ ] Unit test coverage target: 70% for all frontend apps
- [ ] Integration tests for all API endpoints
- [ ] Integration tests for all cross-app connectors
- [ ] E2E tests for critical user flows:
  - [ ] Sign up → create org → invite member
  - [ ] Create project → add tasks → move through workflow
  - [ ] Send email → convert to task
  - [ ] Schedule meeting → join → get summary
  - [ ] Create deal → manage pipeline → close
  - [ ] Create document → share → collaborate
  - [ ] Send message → thread → react
- [ ] Performance/load tests for all APIs
- [ ] Visual regression tests (Chromatic or Percy)
- [ ] Accessibility tests (axe-core in CI)
- [ ] API contract tests (between services)
- [ ] Chaos testing for event bus failures

### 5.4 Observability

- [ ] Structured logging (JSON) across all services
- [ ] Log aggregation (ELK stack or Loki)
- [ ] Request tracing (OpenTelemetry distributed traces)
- [ ] Correlation IDs across all services
- [ ] Metrics collection (Prometheus)
- [ ] Metrics dashboards (Grafana)
  - [ ] API latency (p50, p95, p99 per endpoint)
  - [ ] Error rates per service
  - [ ] Request throughput
  - [ ] Database query performance
  - [ ] WebSocket connection counts
  - [ ] Event bus throughput and lag
  - [ ] AI token usage
  - [ ] Storage usage
- [ ] Alerting rules
  - [ ] Error rate spike
  - [ ] Latency degradation
  - [ ] Service down
  - [ ] Disk/memory/CPU thresholds
  - [ ] Event bus lag
  - [ ] Certificate expiration
- [ ] Error tracking (Sentry) for all services
- [ ] Uptime monitoring (health check endpoints)
- [ ] Status page (public)

### 5.5 Database & Storage

- [ ] PostgreSQL connection pooling (PgBouncer)
- [ ] Read replicas for heavy-read services
- [ ] Database backup strategy (automated daily)
- [ ] Point-in-time recovery
- [ ] Database migration CI check (all Alembic migrations)
- [ ] Tenant data partitioning (for scale)
- [ ] Database performance monitoring (pg_stat_statements)
- [ ] Slow query detection and alerting
- [ ] MinIO/S3 lifecycle policies (archive old files)
- [ ] CDN for static assets and file downloads
- [ ] Redis cluster for high availability
- [ ] Redis Sentinel for failover

### 5.6 Performance

- [ ] Frontend performance budget (< 3s initial load per app)
- [ ] Code splitting and lazy loading (all apps)
- [ ] Tree shaking for shared component library
- [ ] Image optimization pipeline (WebP, AVIF)
- [ ] Font subsetting (only used glyphs)
- [ ] Service worker for offline caching
- [ ] API response caching (Redis)
- [ ] Database query optimization (N+1 detection)
- [ ] Connection pooling for all backends
- [ ] Gzip/Brotli compression
- [ ] HTTP/2 or HTTP/3 support
- [ ] Lighthouse CI (automated performance audits)
- [ ] Bundle size monitoring per app

---

## Phase 6: Security, Compliance & Enterprise Readiness

### 6.1 Security Hardening

- [ ] Security audit of all API endpoints
- [ ] Input validation on all endpoints (Pydantic strict mode)
- [ ] Output encoding/sanitization (XSS prevention)
- [ ] SQL injection prevention audit (parameterized queries)
- [ ] CSRF protection on all state-changing endpoints
- [ ] Content Security Policy headers
- [ ] HSTS headers
- [ ] X-Frame-Options headers
- [ ] Rate limiting on all public endpoints
- [ ] Brute-force protection on login
- [ ] Account lockout after failed attempts
- [ ] Secure session management (httpOnly, secure, sameSite cookies)
- [ ] Secret rotation procedures
- [ ] Dependency vulnerability scanning (automated)
- [ ] SAST (Static Application Security Testing) in CI
- [ ] DAST (Dynamic Application Security Testing) periodic
- [ ] Penetration testing (annual, external)
- [ ] Bug bounty program
- [ ] Security incident response plan
- [ ] Data encryption at rest (AES-256)
- [ ] Data encryption in transit (TLS 1.3)
- [ ] Key management (KMS)

### 6.2 Compliance

- [ ] GDPR compliance
  - [ ] Data processing agreements
  - [ ] Right to access (data export)
  - [ ] Right to erasure (data deletion)
  - [ ] Data portability
  - [ ] Consent management
  - [ ] Privacy policy
  - [ ] Cookie consent
  - [ ] Data retention policies
  - [ ] DPA (Data Processing Agreement) template
- [ ] SOC 2 Type II preparation
  - [ ] Access control documentation
  - [ ] Change management documentation
  - [ ] Incident response documentation
  - [ ] Risk assessment
  - [ ] Vendor management
  - [ ] Employee security training
  - [ ] Background checks
- [ ] HIPAA readiness (for healthcare customers)
  - [ ] BAA (Business Associate Agreement) template
  - [ ] PHI handling procedures
  - [ ] Audit controls
  - [ ] Access controls
  - [ ] Transmission security
- [ ] ISO 27001 readiness
- [ ] CCPA compliance (California)
- [ ] Accessibility compliance (WCAG 2.1 AA)
  - [ ] Accessibility statement
  - [ ] VPAT (Voluntary Product Accessibility Template)

### 6.3 Enterprise Features

- [ ] SSO enforcement (require SSO for org)
- [ ] IP allowlist (restrict access by IP)
- [ ] Device management (trusted devices only)
- [ ] Conditional access policies (location, device, risk)
- [ ] Data loss prevention (DLP) policies
  - [ ] Block sharing outside org
  - [ ] Block file downloads on unmanaged devices
  - [ ] Sensitive data detection (credit cards, SSN)
- [ ] eDiscovery (legal hold, search, export)
- [ ] Information barriers (Chinese walls between teams)
- [ ] Customer-managed encryption keys (CMEK)
- [ ] Single-tenant deployment option
- [ ] SLA guarantees (99.9%, 99.99%)
- [ ] Priority support channel
- [ ] Dedicated account manager
- [ ] Custom contract terms

---

## Phase 7: Go-To-Market & Growth

### 7.1 Marketing Website

- [ ] Landing page (hero, features, pricing, testimonials)
- [ ] Product pages (one per core app)
- [ ] Pricing page (Free, Pro, Enterprise tiers)
- [ ] Comparison pages (vs Google Workspace, vs Microsoft 365, vs Notion)
- [ ] Blog/content hub
- [ ] Changelog/release notes page
- [ ] Security page (certifications, practices)
- [ ] About/team page
- [ ] Contact/demo request page
- [ ] SEO optimization
- [ ] Analytics (Plausible/PostHog)

### 7.2 Pricing & Billing

- [ ] Free tier (core apps, limited storage, limited AI)
- [ ] Pro tier (all apps, more storage, more AI, priority support)
- [ ] Enterprise tier (SSO, SCIM, compliance, custom)
- [ ] Stripe integration for billing
- [ ] Subscription management (upgrade, downgrade, cancel)
- [ ] Usage-based billing for storage and AI
- [ ] Seat-based billing
- [ ] Annual vs monthly pricing
- [ ] Invoice generation
- [ ] Tax handling (Stripe Tax)
- [ ] Promo codes/discounts

### 7.3 Developer Experience

- [ ] API documentation site (interactive, code samples)
- [ ] Developer blog
- [ ] SDK quickstart guides
- [ ] Plugin development tutorials
- [ ] Sample apps/templates
- [ ] Developer forum/community
- [ ] API changelog
- [ ] Postman/Insomnia collections
- [ ] OpenAPI spec download

### 7.4 Support

- [ ] Help center/knowledge base (self-serve)
- [ ] In-app help widget
- [ ] Email support
- [ ] Chat support (via Connect/TurboTick)
- [ ] Community forum
- [ ] Video tutorials/academy
- [ ] Status page (uptime, incidents)
- [ ] Feedback collection (in-app)
- [ ] Bug reporting workflow
- [ ] Feature request voting

### 7.5 Migration & Onboarding Tools

- [ ] Google Workspace importer
  - [ ] Gmail → Orbit Mail
  - [ ] Google Drive → Orbit Writer + Files
  - [ ] Google Calendar → Orbit Calendar
  - [ ] Google Meet → Orbit Meet (settings)
  - [ ] Google Chat → Orbit Connect
  - [ ] Google Contacts → Orbit Contacts
- [ ] Microsoft 365 importer
  - [ ] Outlook → Orbit Mail
  - [ ] OneDrive/SharePoint → Orbit Writer + Files
  - [ ] Outlook Calendar → Orbit Calendar
  - [ ] Teams → Orbit Connect + Meet
- [ ] Slack importer
  - [ ] Channels → Orbit Connect channels
  - [ ] Messages → Orbit Connect messages
  - [ ] Files → Orbit Files
  - [ ] Users → Gate users
- [ ] Jira importer
  - [ ] Projects → Atlas projects
  - [ ] Issues → Atlas tasks
  - [ ] Workflows → Atlas statuses
  - [ ] Sprints → Atlas sprints
  - [ ] Attachments → Atlas attachments
- [ ] Salesforce importer
  - [ ] Contacts → Planet contacts
  - [ ] Leads → Planet leads
  - [ ] Opportunities → Planet deals
  - [ ] Accounts → Planet companies
- [ ] HubSpot importer
  - [ ] Contacts → Planet contacts
  - [ ] Deals → Planet deals
  - [ ] Companies → Planet companies
- [ ] Notion importer
  - [ ] Pages → Writer documents
  - [ ] Databases → Atlas/Writer
- [ ] CSV/JSON generic importer for each app
- [ ] Dual-sync mode (run both old and new during transition)
- [ ] Migration validation reports

---

## Orbit Labs — Graduated App Checklists

> These apps graduate from Labs to Core one at a time, after the Core Eight are polished.

### Labs: TurboTick — Support & Ticketing

- [ ] Ticket CRUD (title, description, priority, status, assignee)
- [ ] Ticket types (bug, feature request, question, incident)
- [ ] Ticket SLA management (response time, resolution time)
- [ ] Ticket priority queues
- [ ] Ticket escalation rules
- [ ] Multi-channel intake (email, chat, API, web form)
- [ ] Customer portal (self-serve ticket view)
- [ ] Ticket macros/canned responses
- [ ] Ticket merge/split
- [ ] Ticket tags
- [ ] Ticket custom fields
- [ ] Knowledge base integration (suggest articles before ticket creation)
- [ ] CSAT surveys (after resolution)
- [ ] SLA breach notifications
- [ ] Ticket analytics dashboard
- [ ] Agent workload distribution
- [ ] TurboTick ↔ Atlas integration
- [ ] TurboTick ↔ Mail integration
- [ ] TurboTick ↔ Connect integration
- [ ] TurboTick ↔ Secure integration

### Labs: Secure — Endpoint & Vulnerability Management

- [ ] Device inventory (enrolled endpoints)
- [ ] Device compliance status
- [ ] Vulnerability scanning (CVE database)
- [ ] Vulnerability prioritization (CVSS scoring)
- [ ] Patch management tracking
- [ ] Zero-trust policy engine
- [ ] Device health attestation before Gate login
- [ ] Security dashboard (risk score, open vulns, compliance %)
- [ ] Incident response workflows
- [ ] Threat intelligence feeds
- [ ] Secure ↔ Gate integration (block non-compliant devices)
- [ ] Secure ↔ Capital Hub integration (asset risk sync)
- [ ] Secure ↔ TurboTick integration (incident tickets)

### Labs: Capital Hub — Asset & Finance

- [ ] Asset CRUD (hardware, software, subscriptions)
- [ ] Asset lifecycle tracking (procure → deploy → retire)
- [ ] Asset assignment to users
- [ ] Asset depreciation calculation
- [ ] SaaS license management
- [ ] License usage tracking (unused seats)
- [ ] Renewal alerts
- [ ] Cost allocation to projects/departments
- [ ] Budget tracking
- [ ] Vendor management
- [ ] Purchase order workflows
- [ ] Barcode/QR code asset tagging
- [ ] Capital Hub ↔ Atlas integration (project costs)
- [ ] Capital Hub ↔ Secure integration (asset risk)
- [ ] Capital Hub ↔ Dock integration (license sync)

### Labs: Control Center — Meeting Lifecycle

- [ ] Pre-meeting agenda builder
- [ ] Meeting notes (collaborative, real-time)
- [ ] Action items tracking
- [ ] Meeting templates
- [ ] One-click export action items → Atlas tasks
- [ ] Meeting recap distribution (email, Connect)
- [ ] Meeting search (across all meeting notes)
- [ ] Control Center ↔ Meet integration
- [ ] Control Center ↔ Calendar integration
- [ ] Control Center ↔ Atlas integration

### Labs: Wallet — Secrets Vault

- [ ] Secret CRUD (API keys, passwords, certificates, tokens)
- [ ] Secret versioning
- [ ] Secret sharing (user, group, project scope)
- [ ] Secret expiration and rotation reminders
- [ ] Envelope encryption (AES-256 + KMS)
- [ ] Break-glass access procedure
- [ ] Secret access audit log
- [ ] Service account secret leasing
- [ ] Wallet ↔ Atlas integration (project-scoped secrets)
- [ ] Wallet ↔ Connect integration (insert vault reference)
- [ ] Wallet ↔ Mail integration (secure credential sharing)

### Labs: Dock — Software Portal

- [ ] Software catalog (approved apps)
- [ ] Software request workflow (CARF)
- [ ] Approval chains
- [ ] License assignment tracking
- [ ] Unused license reclamation
- [ ] Software compliance reporting
- [ ] Self-serve app installation
- [ ] Dock ↔ Capital Hub integration (license costs)
- [ ] Dock ↔ TurboTick integration (request tickets)
- [ ] Dock ↔ Atlas integration (rollout tasks)

### Labs: FitterMe — Ecosystem Health

- [ ] Service health dashboard (all Orbit apps)
- [ ] Uptime tracking per service
- [ ] Response time monitoring
- [ ] Error rate monitoring
- [ ] Dependency mapping (which service depends on which)
- [ ] Alerting (PagerDuty, Connect, email)
- [ ] Incident timeline
- [ ] Post-mortem templates
- [ ] SLA tracking and reporting

### Labs: Learn — Documentation Portal

- [ ] Auto-generated API docs from OpenAPI specs
- [ ] Product knowledge base articles
- [ ] Article search (full-text)
- [ ] Article categories and tags
- [ ] Article versioning
- [ ] Feedback on articles (helpful/not helpful)
- [ ] Admin article editor (WYSIWYG)
- [ ] Public knowledge base for customers
- [ ] Internal knowledge base for team
- [ ] Learn ↔ TurboTick integration (suggest articles)
- [ ] Learn ↔ Search integration (include in global search)

### Labs: Search — Global Search Aggregator

- [ ] Federated search across all apps
- [ ] Result ranking algorithm
- [ ] Search filters (app, date, author, type)
- [ ] Search suggestions (autocomplete)
- [ ] Search analytics (popular queries, zero-result queries)
- [ ] Full-text indexing for all apps
- [ ] Near-real-time index updates via EventBus
- [ ] Search API for other apps to use
- [ ] Elasticsearch/Meilisearch backend
- [ ] Tenant-isolated search indexes

### Labs: EventBus — Event Streaming

- [ ] Upgrade from Redis pub/sub to Redis Streams (for persistence)
- [ ] Event schema registry (versioned schemas)
- [ ] Dead letter queue for failed consumers
- [ ] Event replay capability
- [ ] Consumer group management
- [ ] Event monitoring dashboard
- [ ] Event flow visualization
- [ ] Backpressure handling
- [ ] At-least-once delivery guarantees
- [ ] Event filtering for consumers
- [ ] Multi-tenant event isolation

---

## Cross-Cutting Concerns (Applicable to All Phases)

### Internationalization (i18n)

- [ ] Set up i18n framework (react-intl or i18next)
- [ ] Extract all user-facing strings to translation files
- [ ] English (en) — complete baseline
- [ ] Spanish (es)
- [ ] French (fr)
- [ ] German (de)
- [ ] Portuguese (pt)
- [ ] Japanese (ja)
- [ ] Chinese Simplified (zh-CN)
- [ ] Arabic (ar) — RTL support
- [ ] Hindi (hi)
- [ ] Date/time/number formatting per locale
- [ ] RTL layout support
- [ ] Translation management workflow
- [ ] AI-assisted translation for documentation

### Documentation

- [ ] Architecture decision records (ADRs) for major decisions
- [ ] API documentation (OpenAPI for all endpoints)
- [ ] Developer setup guide (updated, tested)
- [ ] Deployment guide (cloud, self-hosted)
- [ ] Troubleshooting guide
- [ ] Runbook for operations
- [ ] Data model documentation
- [ ] Integration patterns documentation
- [ ] Security documentation
- [ ] Compliance documentation

### Legal

- [ ] Terms of Service
- [ ] Privacy Policy
- [ ] Cookie Policy
- [ ] Data Processing Agreement (DPA)
- [ ] Acceptable Use Policy
- [ ] SLA document
- [ ] Open source license compliance
- [ ] Third-party license audit
- [ ] Trademark registration (RM Orbit)
- [ ] DMCA/takedown procedures

---

> **How to use this checklist:**
> 1. Work top-down: Phase 0 (Design System) → Phase 1 (Core Eight) → Phase 2 (AI) → etc.
> 2. Within each phase, prioritize by user impact and dependency order.
> 3. Check items `[x]` as completed.
> 4. Review weekly to adjust priorities.
>
> **Estimated scope:** This checklist represents a full product lifecycle from current state to enterprise-grade SaaS platform.
