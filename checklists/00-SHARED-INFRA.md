# Shared Infrastructure — Comprehensive Checklist
> Last updated: 2026-04-06
> Legend: [x] = done · [ ] = todo · [~] = in progress

> Covers: orbit-ui design tokens, orbit-bar web component, @orbit-ui/react component library,
> tailwind-preset, token sync, EventBus service, Gateway/proxy setup.

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design Tokens](#2-design-tokens)
3. [orbit-tokens.css (CSS Custom Properties)](#3-orbit-tokenscss-css-custom-properties)
4. [Tailwind Preset](#4-tailwind-preset)
5. [Tailwind v4 Integration](#5-tailwind-v4-integration)
6. [orbit-bar Shell Web Component](#6-orbit-bar-shell-web-component)
7. [orbit-theme-init.js (Anti-FOUC)](#7-orbit-theme-initjs-anti-fouc)
8. [@orbit-ui/react Component Library — Setup](#8-orbit-uireact-component-library--setup)
9. [@orbit-ui/react — Button](#9-orbit-uireact--button)
10. [@orbit-ui/react — IconButton](#10-orbit-uireact--iconbutton)
11. [@orbit-ui/react — ButtonGroup](#11-orbit-uireact--buttongroup)
12. [@orbit-ui/react — Input](#12-orbit-uireact--input)
13. [@orbit-ui/react — Textarea](#13-orbit-uireact--textarea)
14. [@orbit-ui/react — Select](#14-orbit-uireact--select)
15. [@orbit-ui/react — Checkbox](#15-orbit-uireact--checkbox)
16. [@orbit-ui/react — Radio & RadioGroup](#16-orbit-uireact--radio--radiogroup)
17. [@orbit-ui/react — Switch](#17-orbit-uireact--switch)
18. [@orbit-ui/react — Slider](#18-orbit-uireact--slider)
19. [@orbit-ui/react — NumberInput](#19-orbit-uireact--numberinput)
20. [@orbit-ui/react — DatePicker](#20-orbit-uireact--datepicker)
21. [@orbit-ui/react — TimePicker](#21-orbit-uireact--timepicker)
22. [@orbit-ui/react — Badge](#22-orbit-uireact--badge)
23. [@orbit-ui/react — Card](#23-orbit-uireact--card)
24. [@orbit-ui/react — Avatar & AvatarGroup](#24-orbit-uireact--avatar--avatargroup)
25. [@orbit-ui/react — Tag & TagInput](#25-orbit-uireact--tag--taginput)
26. [@orbit-ui/react — Table](#26-orbit-uireact--table)
27. [@orbit-ui/react — EmptyState](#27-orbit-uireact--emptystate)
28. [@orbit-ui/react — Skeleton](#28-orbit-uireact--skeleton)
29. [@orbit-ui/react — Spinner & PageLoader](#29-orbit-uireact--spinner--pageloader)
30. [@orbit-ui/react — Progress & ProgressStacked](#30-orbit-uireact--progress--progressstacked)
31. [@orbit-ui/react — Divider](#31-orbit-uireact--divider)
32. [@orbit-ui/react — Alert](#32-orbit-uireact--alert)
33. [@orbit-ui/react — Tooltip](#33-orbit-uireact--tooltip)
34. [@orbit-ui/react — Toast & ToastProvider](#34-orbit-uireact--toast--toastprovider)
35. [@orbit-ui/react — Modal](#35-orbit-uireact--modal)
36. [@orbit-ui/react — Drawer / Sheet](#36-orbit-uireact--drawer--sheet)
37. [@orbit-ui/react — Popover](#37-orbit-uireact--popover)
38. [@orbit-ui/react — Dropdown Menu](#38-orbit-uireact--dropdown-menu)
39. [@orbit-ui/react — ContextMenu](#39-orbit-uireact--contextmenu)
40. [@orbit-ui/react — CommandPalette](#40-orbit-uireact--commandpalette)
41. [@orbit-ui/react — Sidebar](#41-orbit-uireact--sidebar)
42. [@orbit-ui/react — Tabs](#42-orbit-uireact--tabs)
43. [@orbit-ui/react — Breadcrumb](#43-orbit-uireact--breadcrumb)
44. [@orbit-ui/react — Pagination](#44-orbit-uireact--pagination)
45. [@orbit-ui/react — Steps / Stepper](#45-orbit-uireact--steps--stepper)
46. [@orbit-ui/react — Accordion](#46-orbit-uireact--accordion)
47. [@orbit-ui/react — FileUpload](#47-orbit-uireact--fileupload)
48. [@orbit-ui/react — ThemeProvider & ThemeToggle](#48-orbit-uireact--themeprovider--themetoggle)
49. [@orbit-ui/react — Planned / Missing Components](#49-orbit-uireact--planned--missing-components)
50. [@orbit-ui/react — Shared Hooks Library](#50-orbit-uireact--shared-hooks-library)
51. [Token Sync Script](#51-token-sync-script)
52. [App-by-App Token Integration Status](#52-app-by-app-token-integration-status)
53. [EventBus Service](#53-eventbus-service)
54. [Gate Authentication (AuthX)](#54-gate-authentication-authx)
55. [Gateway / Reverse Proxy](#55-gateway--reverse-proxy)
56. [Storybook & Documentation](#56-storybook--documentation)
57. [CI/CD & Build Pipeline](#57-cicd--build-pipeline)
58. [Testing — Shared Infrastructure](#58-testing--shared-infrastructure)
59. [Security — Shared Infrastructure](#59-security--shared-infrastructure)
60. [Performance — Shared Infrastructure](#60-performance--shared-infrastructure)
61. [Accessibility — Cross-Cutting](#61-accessibility--cross-cutting)
62. [Typography Consistency](#62-typography-consistency)
63. [Icon System Consistency](#63-icon-system-consistency)
64. [Animation & Motion Language](#64-animation--motion-language)
65. [Glassmorphism Design Language](#65-glassmorphism-design-language)
66. [Responsive Design Standards](#66-responsive-design-standards)

---

## 1. Project Setup & Configuration

### 1.1 orbit-ui Package Root
- [x] `/orbit-ui/` directory created at repo root
- [x] `/orbit-ui/tokens/` directory for design token JSON files
- [x] `/orbit-ui/react/` directory for shared React component library
- [x] `/orbit-ui/scripts/` directory for token sync and build scripts
- [x] `/orbit-ui/README.md` documentation file exists
- [ ] `/orbit-ui/CHANGELOG.md` for tracking version changes
- [ ] `/orbit-ui/package.json` root workspace configuration
- [ ] Monorepo workspace linking (npm/pnpm/yarn workspaces)
- [ ] Husky pre-commit hook for linting orbit-ui changes
- [ ] Husky pre-push hook for running orbit-ui tests

### 1.2 orbit-ui/react Package Setup
- [x] `package.json` with `name: "@orbit-ui/react"`
- [x] TypeScript configuration (`tsconfig.json`)
- [x] Vite configured for library build mode (ESM output)
- [x] Exports map in package.json (tree-shakeable ESM)
- [x] `cn()` utility function (clsx + tailwind-merge)
- [x] `src/index.ts` barrel export for all components
- [ ] CJS fallback output for Node.js environments
- [ ] Source maps enabled in production build
- [ ] Type declarations emitted (`.d.ts` files)
- [ ] Package README with installation and usage instructions
- [ ] `peerDependencies` declared (react, react-dom, tailwindcss)
- [ ] `devDependencies` pinned for reproducible builds
- [ ] ESLint configuration (extends shared orbit config)
- [ ] Prettier configuration (extends shared orbit config)
- [ ] `.npmignore` or `files` field to control published package size
- [ ] Vitest configuration for component unit tests
- [ ] Storybook 8 with Vite builder configured
- [ ] Component template/generator script for scaffolding new components
- [x] `@orbit-ui/react` added as `file:` dependency in Atlas
- [x] `@orbit-ui/react` added as `file:` dependency in Mail
- [x] `@orbit-ui/react` added as `file:` dependency in Connect
- [x] `@orbit-ui/react` added as `file:` dependency in Meet
- [x] `@orbit-ui/react` added as `file:` dependency in Calendar
- [x] `@orbit-ui/react` added as `file:` dependency in Writer
- [x] `@orbit-ui/react` added as `file:` dependency in Planet
- [x] `@orbit-ui/react` added as `file:` dependency in Secure
- [x] `@orbit-ui/react` added as `file:` dependency in Capital Hub
- [ ] `@orbit-ui/react` added as `file:` dependency in Control Center
- [ ] `@orbit-ui/react` added as `file:` dependency in TurboTick
- [ ] `@orbit-ui/react` added as `file:` dependency in Dock
- [ ] `@orbit-ui/react` added as `file:` dependency in Wallet
- [ ] `@orbit-ui/react` added as `file:` dependency in FitterMe
- [ ] `@orbit-ui/react` added as `file:` dependency in Learn

---

## 2. Design Tokens

### 2.1 colors.json
- [x] File exists at `/orbit-ui/tokens/colors.json`
- [x] Primary blue scale: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
- [x] Standardized primary blue: `#2b7cee`
- [x] Neutral/gray scale (slate-based) full range
- [x] Success color scale (green)
- [x] Warning color scale (amber)
- [x] Danger/error color scale (red)
- [x] Info color scale (cyan/sky)
- [x] Surface colors (light mode): background, card, elevated, overlay
- [x] Surface colors (dark mode): background, card, elevated, overlay
- [x] Text colors: primary, secondary, muted, disabled, inverse
- [x] Border colors: default, subtle, strong, focus
- [x] Glass colors: bg, border (light + dark)
- [ ] Brand accent colors (secondary accent palette)
- [ ] Chart-specific color palette (8+ distinguishable data colors)
- [ ] Gradient presets (brand gradients for hero sections)
- [ ] Social media brand colors (Google, GitHub, Microsoft)
- [ ] Validation: ensure all color values are valid hex/hsl/rgb
- [ ] Contrast validation: all text/bg combos meet WCAG AA (4.5:1)
- [ ] Documentation: color usage guidelines (when to use which token)

### 2.2 typography.json
- [x] File exists at `/orbit-ui/tokens/typography.json`
- [x] Font families: display (RM Samplet), sans (RM Forma), mono (JetBrains Mono)
- [x] Font sizes: 2xs through 6xl with matching line heights
- [x] Font weights: light, normal, medium, semibold, bold, extrabold
- [x] Line heights: none, tight, snug, normal, relaxed, loose
- [x] Letter spacing: tighter, tight, normal, wide, wider, widest
- [ ] Heading presets: h1-h6 with size + weight + line-height + letter-spacing combos
- [ ] Body text presets: body-sm, body-md, body-lg
- [ ] Caption/overline presets
- [ ] Code text presets (mono font + specific size)
- [ ] Documentation: when to use RM Samplet vs RM Forma vs JetBrains Mono

### 2.3 radius.json
- [x] File exists at `/orbit-ui/tokens/radius.json`
- [x] Scale: none, xs, sm, md, lg, xl, 2xl, 3xl, full
- [x] Component-specific: button, input, card, modal, badge, panel, chip
- [ ] Ensure component-specific radii match the scale (no orphan values)
- [ ] Documentation: which radius for which component type

### 2.4 shadows.json
- [x] File exists at `/orbit-ui/tokens/shadows.json`
- [x] Scale: sm, md, lg, xl, 2xl, inner, none
- [x] Glass shadows: glass, glass-sm
- [x] Focus shadows: focus, focus-danger, focus-success
- [x] Component shadows: card, card-hover, modal, dropdown, tooltip
- [x] Glow effects: glow, glow-lg, glow-pulse
- [ ] Dark mode shadow adjustments (darker/subtler shadows)
- [ ] Validation: ensure all shadow values are valid CSS box-shadow syntax

### 2.5 z-index.json
- [x] File exists at `/orbit-ui/tokens/z-index.json`
- [x] Named layers: base through max, all overlay layers
- [ ] Ensure z-index values do not conflict across apps
- [ ] Documentation: layer stacking order diagram

### 2.6 motion.json
- [x] File exists at `/orbit-ui/tokens/motion.json`
- [x] Durations: instant (0ms), fast (100ms), normal (200ms), slow (300ms), slower (500ms), slowest (700ms)
- [x] Easings: ease-in, ease-out, ease-in-out, spring, spring-soft, overshoot
- [x] Keyframes: fade-in/out, slide-up/down/left/right, scale-in/out, shimmer, pulse-ring, float, spin, bounce-soft
- [ ] Reduced motion fallback values (instant duration, no transform)
- [ ] Documentation: which easing for which interaction type

### 2.7 Token Versioning
- [ ] Token version number in each JSON file
- [ ] Token changelog tracking all changes with dates
- [ ] Semantic versioning for token packages
- [ ] Breaking change detection when tokens are modified
- [ ] Token deprecation workflow (mark old tokens, provide migration path)
- [ ] Visual regression tests for token CSS output
- [ ] Figma token sync (Figma Tokens plugin export → JSON)
- [ ] Figma token import (JSON → Figma Tokens plugin)

---

## 3. orbit-tokens.css (CSS Custom Properties)

### 3.1 Static Palette Tokens
- [x] All primary-* color custom properties
- [x] All neutral-* color custom properties
- [x] All success-* color custom properties
- [x] All warning-* color custom properties
- [x] All danger-* color custom properties
- [x] All info-* color custom properties
- [ ] Validate every custom property resolves correctly in browser

### 3.2 Light Mode Semantic Tokens (`:root`)
- [x] `--color-bg-*` surface tokens (base, subtle, muted, elevated, overlay)
- [x] `--color-text-*` content tokens (primary, secondary, muted, disabled, inverse)
- [x] `--color-border-*` tokens (default, subtle, strong, focus)
- [x] `--color-surface-*` tokens
- [ ] Validate all semantic tokens map to palette tokens correctly
- [ ] Ensure no orphan tokens (every defined token is used somewhere)

### 3.3 Dark Mode Semantic Tokens (`.dark`)
- [x] All surface tokens adjusted for dark backgrounds
- [x] All text tokens adjusted for dark backgrounds
- [x] All border tokens adjusted for dark backgrounds
- [x] Glass tokens adjusted for dark mode
- [ ] Contrast validation: all dark mode combos meet WCAG AA
- [ ] Test in Chrome, Firefox, Safari, Edge

### 3.4 Font Face Declarations
- [x] RM Forma font-face (woff2)
- [x] RM Samplet font-face (woff2)
- [x] JetBrains Mono font-face (woff2)
- [ ] `font-display: swap` on all font-face declarations
- [ ] Preload critical font files in HTML `<head>`
- [ ] Subset fonts for Latin characters only (reduce file size)
- [ ] Test font rendering on Windows, macOS, Linux
- [ ] Test font rendering in Chrome, Firefox, Safari, Edge

### 3.5 Base Reset & Defaults
- [x] CSS reset / normalize styles
- [x] Box-sizing: border-box global
- [x] Base font family applied to body
- [x] Base text color applied to body
- [x] Base background color applied to body
- [ ] Scrollbar width standardization across browsers
- [ ] Selection color styling (::selection)

### 3.6 Theme Transition
- [x] Smooth transition on dark/light switch (background, color, border)
- [ ] Ensure transition does not cause layout shift
- [ ] Respect `prefers-reduced-motion` (disable transition)

### 3.7 Global Focus Styles
- [x] `focus-visible` outline/ring style defined globally
- [x] Skip link component styles
- [x] Global thin scrollbar style (`.scrollbar-thin`)
- [ ] High contrast mode support (`prefers-contrast: more`)
- [ ] Forced colors mode support (`forced-colors: active`)

---

## 4. Tailwind Preset

### 4.1 Core Configuration
- [x] File exists at `/orbit-ui/tailwind-preset.js`
- [x] `darkMode: "class"` configured
- [x] All color tokens wired into Tailwind `theme.extend.colors`
- [x] Font families wired into `theme.extend.fontFamily`
- [x] Font sizes wired into `theme.extend.fontSize`
- [x] Spacing scale wired into `theme.extend.spacing`
- [x] Border radius wired into `theme.extend.borderRadius`
- [x] Shadows wired into `theme.extend.boxShadow`
- [x] Z-index scale wired into `theme.extend.zIndex`
- [x] Animations wired into `theme.extend.animation`
- [x] Keyframes wired into `theme.extend.keyframes`
- [x] Breakpoints defined in `theme.extend.screens`
- [ ] Ring color defaults for focus-visible
- [ ] Ring offset defaults
- [ ] Ensure no conflicts with Tailwind defaults

### 4.2 Custom Plugins
- [x] Glass utility plugin (`.glass`, `.glass-sm`, `.glass-subtle`)
- [x] Focus ring plugin (`.focus-ring`, `.focus-ring-inset`)
- [x] Scrollbar plugin (`.scrollbar-thin`, `.scrollbar-none`)
- [x] Skeleton/shimmer plugin (`.skeleton`)
- [ ] Text balance plugin (`.text-balance`)
- [ ] Container query plugin
- [ ] Line-clamp plugin (multi-line ellipsis)
- [ ] Aspect ratio plugin (if not using native CSS)

### 4.3 App Migration Status
- [x] Atlas `tailwind.config.js` uses orbit preset
- [x] Mail `tailwind.config.js` uses orbit preset
- [x] Connect `tailwind.config.js` uses orbit preset
- [x] Meet `tailwind.config.js` uses orbit preset
- [x] Calendar `tailwind.config.js` uses orbit preset
- [x] Writer `tailwind.config.js` uses orbit preset
- [x] Planet `tailwind.config.js` uses orbit preset
- [x] Secure `tailwind.config.js` uses orbit preset
- [x] Capital Hub `tailwind.config.js` uses orbit preset
- [ ] Control Center `tailwind.config.js` uses orbit preset
- [ ] TurboTick `tailwind.config.js` uses orbit preset
- [ ] Dock `tailwind.config.js` uses orbit preset
- [ ] Wallet `tailwind.config.js` uses orbit preset
- [ ] FitterMe `tailwind.config.js` uses orbit preset
- [ ] Learn `tailwind.config.js` uses orbit preset
- [x] Remove all app-specific color overrides conflicting with shared palette
- [ ] Visual consistency verification after migration (each app)

---

## 5. Tailwind v4 Integration

- [x] `orbit-tailwind-v4.css` file created
- [x] `@theme` integration for Tailwind v4 apps
- [x] Token sync script syncs `orbit-tailwind-v4.css` to all apps
- [ ] Verify v4 theme file covers all tokens from v3 preset
- [ ] Document migration path from v3 preset to v4 `@theme`
- [ ] Test v4 apps (Connect, Meet) render identically to v3 apps
- [ ] Container queries support in v4 theme

---

## 6. orbit-bar Shell Web Component

### 6.1 Core Structure
- [x] Web component registered as `<orbit-bar>`
- [x] Shadow DOM encapsulation
- [x] Renders top shell bar across all 16 apps
- [ ] Lazy-loads orbit-bar.js (script defer or dynamic import)
- [ ] Graceful fallback if orbit-bar.js fails to load

### 6.2 App Launcher Panel
- [x] App launcher panel renders with all 14 apps
- [x] Each app has icon, name, and link to correct URL/port
- [ ] Active app highlight (current app visually distinct)
- [ ] Keyboard navigation within app launcher panel (arrow keys, Enter to select)
- [ ] App launcher search/filter for quick access
- [ ] Notification badge on app icons (unread counts from EventBus)
- [ ] App launcher opens on click, closes on outside-click
- [ ] App launcher opens on keyboard shortcut (Cmd+K or configurable)
- [ ] App launcher grid layout (responsive: 3-col on small, 4-col on large)
- [ ] App launcher shows recently used apps first
- [ ] App launcher drag-to-reorder (user preference, persisted)
- [ ] App launcher category grouping (Productivity, Communication, Business, etc.)
- [ ] App launcher accessible: role="menu", aria-label on items

### 6.3 Org Switcher
- [x] Reads current org from localStorage
- [x] Writes selected org to localStorage
- [x] Emits `orbit:org-change` custom event on switch
- [ ] Org switcher: dropdown with org list
- [ ] Org switcher: org logo/avatar display
- [ ] Org switcher: search/filter for many orgs
- [ ] Org switcher: "Create new organization" action
- [ ] Org switcher: visual indicator of current org
- [ ] Org switcher: keyboard navigable (arrow keys, Enter)
- [ ] Org switcher: loads org list from Gate API (not just localStorage)
- [ ] Org switcher: graceful handling of 0 orgs (redirect to create)

### 6.4 Identity Panel
- [x] User avatar display
- [x] User name display
- [x] Sign-out button
- [ ] User email display
- [ ] User role/title display
- [ ] Link to profile settings (opens Gate profile page)
- [ ] Status indicator (online/away/busy)
- [ ] Custom status display
- [ ] Sign-out: clears all auth cookies and localStorage tokens
- [ ] Sign-out: redirects to Gate login page
- [ ] Sign-out: calls Gate `/auth/logout` endpoint

### 6.5 Theme Toggle
- [x] Theme toggle button (sun/moon SVG)
- [x] Cycles: light -> dark -> system
- [x] `orbit:theme-change` custom event dispatch
- [x] CSS for theme toggle button (`.orbit-shell__theme-toggle`)
- [ ] Tooltip showing current theme state
- [ ] Accessible label: "Switch to dark mode" / "Switch to light mode"
- [ ] Animation: smooth icon transition (sun -> moon)
- [ ] Persist preference to Gate user settings (server-synced)

### 6.6 Search
- [ ] Search hotkey (`/`) opens global search overlay
- [ ] Global search: searches across all Orbit apps
- [ ] Global search: shows results grouped by app
- [ ] Global search: keyboard navigation in results
- [ ] Global search: recent searches history
- [ ] Global search: result type indicators (task, email, message, document, etc.)
- [ ] Global search: "Search in [current app]" vs "Search everywhere" toggle

### 6.7 Notifications
- [ ] Notification bell icon with unread count badge
- [ ] Notification dropdown panel
- [ ] Notification list: grouped by app
- [ ] Notification list: mark as read
- [ ] Notification list: mark all as read
- [ ] Notification list: click to navigate to source
- [ ] Notification list: infinite scroll / pagination
- [ ] Desktop push notification permission request
- [ ] Notification sound (configurable)
- [ ] Notification preferences link (opens settings)

### 6.8 Breadcrumb Slot
- [ ] Apps can inject current page path into orbit-bar breadcrumb slot
- [ ] Breadcrumb slot uses `<slot name="breadcrumb">` in shadow DOM
- [ ] Breadcrumb renders with `>` separator
- [ ] Breadcrumb: clickable segments navigate to parent pages

### 6.9 Mobile Responsiveness
- [ ] Orbit bar collapses to icon-only below 768px
- [ ] Hamburger menu replaces full nav on mobile
- [ ] App launcher becomes fullscreen drawer on mobile
- [ ] Touch-friendly tap targets (min 44x44px)
- [ ] Swipe-to-dismiss on mobile panels

### 6.10 Accessibility
- [ ] All interactive elements have `aria-label`
- [ ] Keyboard shortcut guide button (press `?` to show)
- [ ] Focus management: Escape closes any open panel
- [ ] Focus management: panel open -> focus first item, panel close -> focus trigger
- [ ] Screen reader announcements for panel open/close
- [ ] `role="banner"` on orbit-bar root
- [ ] `role="navigation"` on app launcher
- [ ] Skip link: "Skip to main content" before orbit-bar

---

## 7. orbit-theme-init.js (Anti-FOUC)

- [x] Reads `localStorage["orbit-theme"]` before DOM renders
- [x] Checks `prefers-color-scheme: dark` media query
- [x] Applies `.dark` class to `<html>` before CSS loads
- [ ] Minified/inlined version for production builds (< 500 bytes)
- [ ] Handles `"system"` preference (reads OS preference)
- [ ] Handles missing localStorage gracefully (no errors)
- [ ] Script tag placed in `<head>` (blocking) to prevent FOUC
- [x] Synced to all 16 app `public/orbit-ui/` dirs via token sync
- [ ] Test: no visible flash on page load in dark mode
- [ ] Test: no visible flash on page load in light mode
- [ ] Test: no visible flash when system preference is used

---

## 8. @orbit-ui/react Component Library -- Setup

- [x] Package directory at `/orbit-ui/react/`
- [x] `package.json` with correct name and version
- [x] TypeScript configured
- [x] Vite library build mode
- [x] Tree-shakeable ESM exports
- [x] `cn()` utility exported
- [x] `src/index.ts` barrel export with all 36 components
- [ ] Storybook 8 configured and running
- [ ] Vitest configured for component testing
- [ ] Component generator script (scaffold new component: dir + tsx + test + story)
- [ ] Lint rules: no `any` types in component props
- [ ] Lint rules: all props have JSDoc comments
- [ ] Bundle size budget: < 100KB gzipped for full library
- [ ] Tree-shaking verification: unused components excluded from app bundles

---

## 9. @orbit-ui/react -- Button

### 9.1 Implementation
- [x] Component file exists at `components/Button/Button.tsx`
- [x] Exported from `src/index.ts`
- [x] `ButtonProps` type exported

### 9.2 Variants
- [x] `primary` variant (solid blue)
- [x] `secondary` variant (muted/gray)
- [x] `outline` variant (bordered)
- [x] `ghost` variant (transparent bg)
- [x] `danger` variant (red/destructive)
- [x] `success` variant (green)
- [x] `warning` variant (amber)

### 9.3 Sizes
- [x] `xs` size
- [x] `sm` size
- [x] `md` size (default)
- [x] `lg` size
- [x] `xl` size

### 9.4 States
- [x] Default state
- [x] Hover state
- [x] Active/pressed state
- [x] Focus-visible state (ring)
- [x] Disabled state (opacity + pointer-events)
- [x] Loading state (spinner + disabled interaction)

### 9.5 Features
- [x] Left icon slot (`leftIcon` prop)
- [x] Right icon slot (`rightIcon` prop)
- [x] Icon-only mode (when only icon, no text)
- [x] Loading spinner integration (replaces icon or inline)
- [x] Polymorphic `as` prop (render as `<button>`, `<a>`, `<Link>`)
- [x] Full keyboard accessibility (Enter + Space activate)
- [ ] Tooltip on hover (when `title` prop provided)
- [ ] Ripple effect on click (optional prop)
- [ ] Full-width variant (`fullWidth` prop)

### 9.6 Dark Mode
- [x] All variants render correctly in dark mode
- [ ] Verified contrast ratio in dark mode for all variants

### 9.7 Testing
- [ ] Storybook story: all variants rendered
- [ ] Storybook story: all sizes rendered
- [ ] Storybook story: loading state
- [ ] Storybook story: disabled state
- [ ] Storybook story: with icons
- [ ] Storybook story: polymorphic as anchor
- [ ] Vitest: renders correctly with default props
- [ ] Vitest: applies variant class correctly
- [ ] Vitest: applies size class correctly
- [ ] Vitest: calls onClick handler
- [ ] Vitest: does not call onClick when disabled
- [ ] Vitest: does not call onClick when loading
- [ ] Vitest: renders loading spinner when loading=true
- [ ] Vitest: renders as anchor when as="a"
- [ ] Vitest: forwards ref correctly
- [ ] Vitest: renders left/right icons
- [ ] Accessibility test: button has role="button"
- [ ] Accessibility test: disabled button has aria-disabled
- [ ] Accessibility test: loading button has aria-busy

### 9.8 Documentation
- [ ] Props table in Storybook
- [ ] Usage examples: primary action, secondary action, danger action
- [ ] Do's and don'ts: when to use each variant
- [ ] Migration guide: replacing custom button classes

---

## 10. @orbit-ui/react -- IconButton

### 10.1 Implementation
- [x] Component file exists at `components/Button/IconButton.tsx`
- [x] Exported from `src/index.ts`
- [x] `IconButtonProps` type exported

### 10.2 Features
- [x] Square form factor for all sizes
- [x] All size variants from Button (xs through xl)
- [x] Loading spinner support
- [x] `aria-label` required (enforced via TypeScript)
- [ ] Tooltip on hover showing aria-label text
- [ ] Badge overlay (notification dot)

### 10.3 Testing
- [ ] Storybook story: all sizes
- [ ] Storybook story: all variants
- [ ] Storybook story: loading state
- [ ] Vitest: renders icon correctly
- [ ] Vitest: requires aria-label prop
- [ ] Vitest: click handler fires
- [ ] Vitest: disabled state prevents interaction
- [ ] Accessibility test: has accessible name via aria-label

---

## 11. @orbit-ui/react -- ButtonGroup

### 11.1 Implementation
- [x] Component file exists at `components/Button/ButtonGroup.tsx`
- [x] Exported from `src/index.ts`
- [x] `ButtonGroupProps` type exported

### 11.2 Features
- [x] Horizontal grouping with connected borders (rounded ends only)
- [x] Vertical grouping option
- [x] Active state management (tracks which button is active)
- [ ] Size prop (applies to all children uniformly)
- [ ] Variant prop (applies to all children uniformly)
- [ ] Spacing between buttons (attached vs separated)

### 11.3 Testing
- [ ] Storybook story: horizontal group
- [ ] Storybook story: vertical group
- [ ] Storybook story: with active state
- [ ] Vitest: renders children correctly
- [ ] Vitest: active button has correct styling
- [ ] Vitest: keyboard navigation between buttons

---

## 12. @orbit-ui/react -- Input

### 12.1 Implementation
- [x] Component file exists at `components/Input/Input.tsx`
- [x] Exported from `src/index.ts`
- [x] `InputProps` type exported

### 12.2 Sizes
- [x] `sm` size
- [x] `md` size (default)
- [x] `lg` size

### 12.3 States
- [x] Default state
- [x] Focus state (ring highlight)
- [x] Error state (red border + error message)
- [x] Disabled state (grayed out, non-interactive)

### 12.4 Features
- [x] Prefix element (icon or text before input)
- [x] Suffix element (icon or text after input)
- [x] Error message display below input
- [x] Helper text display below input
- [x] Auto-generated accessible `id` + `aria-describedby`
- [ ] Clear button option (X icon to clear value)
- [ ] Character count display (current/max)
- [ ] Password visibility toggle (for type="password")
- [ ] Input mask support (phone, currency, date)
- [ ] Debounced onChange (configurable delay)

### 12.5 Dark Mode
- [x] Background, border, text colors adapt in dark mode
- [ ] Placeholder text color verified in dark mode
- [ ] Error state colors verified in dark mode

### 12.6 Testing
- [ ] Storybook story: all sizes
- [ ] Storybook story: with prefix/suffix
- [ ] Storybook story: error state
- [ ] Storybook story: disabled state
- [ ] Storybook story: helper text
- [ ] Vitest: renders with placeholder
- [ ] Vitest: controlled value updates
- [ ] Vitest: error message displays
- [ ] Vitest: aria-describedby links to error/helper
- [ ] Vitest: disabled input cannot be focused
- [ ] Vitest: prefix/suffix render correctly
- [ ] Accessibility test: label association (aria-labelledby or htmlFor)
- [ ] Accessibility test: error announced to screen readers

---

## 13. @orbit-ui/react -- Textarea

### 13.1 Implementation
- [x] Component file exists at `components/Input/Textarea.tsx`
- [x] Exported from `src/index.ts`
- [x] `TextareaProps` type exported

### 13.2 Features
- [x] Base textarea rendering
- [ ] Auto-resize option (grows with content)
- [ ] Character count display (current/max)
- [ ] Min/max rows configuration
- [ ] Error message display
- [ ] Helper text display
- [ ] Disabled state styling

### 13.3 Testing
- [ ] Storybook story: default, with placeholder
- [ ] Storybook story: auto-resize
- [ ] Storybook story: character count
- [ ] Storybook story: error state
- [ ] Vitest: renders textarea element
- [ ] Vitest: auto-resize adjusts height
- [ ] Vitest: character count updates on input
- [ ] Accessibility test: label association

---

## 14. @orbit-ui/react -- Select

### 14.1 Implementation
- [x] Component file exists at `components/Input/Select.tsx`
- [x] Exported from `src/index.ts`
- [x] `SelectProps` type exported

### 14.2 Features
- [x] Native select wrapper (basic)
- [ ] Custom dropdown select (styled, searchable)
- [ ] Multi-select variant (tags in input)
- [ ] Option groups support
- [ ] Clear button (remove selection)
- [ ] Loading state (fetching options)
- [ ] Async option loading (search-as-you-type)
- [ ] Creatable (add new options on the fly)
- [ ] Disabled state
- [ ] Error state with message

### 14.3 Testing
- [ ] Storybook story: native select
- [ ] Storybook story: custom dropdown
- [ ] Storybook story: multi-select
- [ ] Storybook story: searchable
- [ ] Vitest: renders options correctly
- [ ] Vitest: selection changes value
- [ ] Vitest: keyboard navigation (arrow keys, Enter)
- [ ] Accessibility test: select has label
- [ ] Accessibility test: custom dropdown has role="listbox"

---

## 15. @orbit-ui/react -- Checkbox

### 15.1 Implementation
- [x] Component file exists at `components/Checkbox/Checkbox.tsx`
- [x] Exported from `src/index.ts`
- [x] `CheckboxProps` type exported

### 15.2 Features
- [x] Checked state
- [x] Unchecked state
- [x] Indeterminate state
- [x] Label support
- [x] Description text support
- [x] Disabled state
- [ ] Checkbox group component (CheckboxGroup)
- [ ] Error state with message
- [ ] Required indicator

### 15.3 Testing
- [ ] Storybook story: all states (checked, unchecked, indeterminate)
- [ ] Storybook story: with label and description
- [ ] Storybook story: disabled
- [ ] Vitest: toggles on click
- [ ] Vitest: indeterminate renders correctly
- [ ] Vitest: disabled prevents toggle
- [ ] Vitest: label click toggles checkbox
- [ ] Accessibility test: checkbox role
- [ ] Accessibility test: aria-checked state

---

## 16. @orbit-ui/react -- Radio & RadioGroup

### 16.1 Implementation
- [x] Component files exist at `components/Radio/Radio.tsx`
- [x] `Radio` and `RadioGroup` exported from `src/index.ts`
- [x] `RadioProps` and `RadioGroupProps` types exported

### 16.2 Features
- [x] Radio button component
- [x] RadioGroup with vertical layout
- [x] RadioGroup with horizontal layout
- [ ] Card-style radio (selectable cards)
- [ ] Disabled individual radio options
- [ ] Error state on RadioGroup
- [ ] Description text per radio option

### 16.3 Testing
- [ ] Storybook story: vertical group
- [ ] Storybook story: horizontal group
- [ ] Storybook story: card-style
- [ ] Storybook story: disabled
- [ ] Vitest: selection changes on click
- [ ] Vitest: only one option selected at a time
- [ ] Vitest: keyboard navigation (arrow keys cycle options)
- [ ] Accessibility test: role="radiogroup"
- [ ] Accessibility test: aria-checked on selected radio

---

## 17. @orbit-ui/react -- Switch

### 17.1 Implementation
- [x] Component file exists at `components/Switch/Switch.tsx`
- [x] Exported from `src/index.ts`
- [x] `SwitchProps` type exported

### 17.2 Features
- [x] Sizes: sm, md
- [x] Label support
- [x] Description text support
- [x] Disabled state
- [x] Color variants
- [ ] Loading state (toggling)
- [ ] On/off text labels inside track

### 17.3 Testing
- [ ] Storybook story: both sizes
- [ ] Storybook story: with label/description
- [ ] Storybook story: disabled
- [ ] Vitest: toggles on click
- [ ] Vitest: keyboard toggle (Space key)
- [ ] Vitest: disabled prevents toggle
- [ ] Accessibility test: role="switch"
- [ ] Accessibility test: aria-checked state

---

## 18. @orbit-ui/react -- Slider

### 18.1 Implementation
- [x] Component file exists at `components/Slider/Slider.tsx`
- [x] Exported from `src/index.ts`
- [x] `SliderProps` type exported

### 18.2 Features
- [x] Single value slider
- [x] Range slider (two thumbs)
- [x] Value tooltip on hover/drag
- [ ] Step markers (visual tick marks)
- [ ] Custom marks with labels
- [ ] Disabled state
- [ ] Vertical orientation
- [ ] Color variants

### 18.3 Testing
- [ ] Storybook story: single value
- [ ] Storybook story: range
- [ ] Storybook story: with step markers
- [ ] Storybook story: disabled
- [ ] Vitest: value changes on drag
- [ ] Vitest: keyboard: arrow keys adjust value
- [ ] Vitest: min/max constraints enforced
- [ ] Vitest: step increments correctly
- [ ] Accessibility test: role="slider"
- [ ] Accessibility test: aria-valuemin/max/now

---

## 19. @orbit-ui/react -- NumberInput

### 19.1 Implementation
- [x] Component file exists at `components/NumberInput/NumberInput.tsx`
- [x] Exported from `src/index.ts`
- [x] `NumberInputProps` type exported

### 19.2 Features
- [x] Increment/decrement buttons
- [x] Min/max constraints
- [x] Step value
- [ ] Keyboard: arrow up/down adjusts value
- [ ] Keyboard: Shift+arrow for larger step
- [ ] Format display value (comma separators, decimal places)
- [ ] Prefix/suffix (currency symbol, unit)
- [ ] Disabled state
- [ ] Error state

### 19.3 Testing
- [ ] Storybook story: basic number input
- [ ] Storybook story: with min/max
- [ ] Storybook story: with step
- [ ] Vitest: increment button increases value
- [ ] Vitest: decrement button decreases value
- [ ] Vitest: min/max constraints enforced
- [ ] Vitest: keyboard arrow keys work
- [ ] Accessibility test: spinbutton role
- [ ] Accessibility test: aria-valuemin/max/now

---

## 20. @orbit-ui/react -- DatePicker

### 20.1 Implementation
- [x] Component file exists at `components/DatePicker/DatePicker.tsx`
- [x] Exported from `src/index.ts`
- [x] `DatePickerProps`, `DatePickerMode`, `DateRange` types exported

### 20.2 Features
- [x] Single date selection
- [x] Date range selection
- [x] Month/year navigation
- [x] Min/max date constraints
- [x] Locale support
- [ ] Keyboard navigation (arrow keys navigate days, Enter selects)
- [ ] Today button (jump to today)
- [ ] Clear button
- [ ] Custom date formatting
- [ ] Disabled specific dates (e.g., weekends, holidays)
- [ ] Week number display
- [ ] Multiple calendar months visible

### 20.3 Testing
- [ ] Storybook story: single date
- [ ] Storybook story: date range
- [ ] Storybook story: with min/max
- [ ] Storybook story: different locales
- [ ] Vitest: selecting a date updates value
- [ ] Vitest: range selection start/end
- [ ] Vitest: min/max constraints prevent selection
- [ ] Vitest: month navigation works
- [ ] Vitest: year navigation works
- [ ] Accessibility test: calendar grid role
- [ ] Accessibility test: selected date announced
- [ ] Accessibility test: keyboard navigation through days

---

## 21. @orbit-ui/react -- TimePicker

### 21.1 Implementation
- [x] Component file exists at `components/TimePicker/TimePicker.tsx`
- [x] Exported from `src/index.ts`
- [x] `TimePickerProps`, `TimeValue` types exported

### 21.2 Features
- [x] 12-hour format (AM/PM)
- [x] 24-hour format
- [x] Minute intervals (5, 10, 15, 30)
- [ ] Keyboard input support (type time directly)
- [ ] Min/max time constraints
- [ ] Clear button
- [ ] Second selection (optional)
- [ ] Timezone display

### 21.3 Testing
- [ ] Storybook story: 12h format
- [ ] Storybook story: 24h format
- [ ] Storybook story: minute intervals
- [ ] Vitest: selecting time updates value
- [ ] Vitest: format toggle works
- [ ] Accessibility test: time picker has label
- [ ] Accessibility test: keyboard navigable

---

## 22. @orbit-ui/react -- Badge

### 22.1 Implementation
- [x] Component file exists at `components/Badge/Badge.tsx`
- [x] Exported from `src/index.ts`
- [x] `BadgeProps` type exported

### 22.2 Features
- [x] Variants: solid, subtle, outline
- [x] Colors: primary, success, warning, danger, info, neutral
- [x] Sizes: sm, md, lg
- [x] Dot indicator (no text, just colored dot)
- [x] Removable (with X/close button)
- [ ] Badge with icon (left icon slot)
- [ ] Pulsing animation variant (for notifications)
- [ ] Max count (e.g., "99+")

### 22.3 Testing
- [ ] Storybook story: all variants x all colors
- [ ] Storybook story: all sizes
- [ ] Storybook story: dot indicator
- [ ] Storybook story: removable
- [ ] Vitest: renders text content
- [ ] Vitest: removable badge fires onRemove callback
- [ ] Vitest: dot variant renders without text
- [ ] Accessibility test: badge has role or aria description

---

## 23. @orbit-ui/react -- Card

### 23.1 Implementation
- [x] Component file exists at `components/Card/Card.tsx`
- [x] Exported from `src/index.ts`
- [x] `CardProps` type exported

### 23.2 Variants
- [x] Default card (border + shadow)
- [x] Elevated card (larger shadow)
- [x] Glass card (glassmorphism effect)
- [x] Flat card (no shadow, subtle border)
- [x] Interactive card (hover/click states with scale/shadow change)

### 23.3 Compound Components
- [x] `Card.Header`
- [x] `Card.Title`
- [x] `Card.Description`
- [x] `Card.Body`
- [x] `Card.Footer`
- [x] `Card.Divider`
- [ ] `Card.Media` / image slot
- [ ] `Card.Actions` (footer actions alignment)

### 23.4 Testing
- [ ] Storybook story: all variants
- [ ] Storybook story: with header/body/footer
- [ ] Storybook story: interactive (clickable)
- [ ] Storybook story: glass variant in dark mode
- [ ] Vitest: renders children correctly
- [ ] Vitest: interactive card fires onClick
- [ ] Vitest: compound components render in correct order
- [ ] Accessibility test: interactive card has role="button" or "link"
- [ ] Accessibility test: non-interactive card is semantic `<div>`

---

## 24. @orbit-ui/react -- Avatar & AvatarGroup

### 24.1 Implementation
- [x] Component file exists at `components/Avatar/Avatar.tsx`
- [x] `Avatar` and `AvatarGroup` exported from `src/index.ts`
- [x] `AvatarProps` and `AvatarGroupProps` types exported

### 24.2 Avatar Features
- [x] Image avatar with error fallback (initials)
- [x] Initials fallback with deterministic color from name
- [x] Sizes: xs, sm, md, lg, xl
- [x] Status indicator: online, offline, busy, away
- [ ] Square variant (rounded-lg instead of full circle)
- [ ] Ring/border variant (colored ring around avatar)
- [ ] Clickable avatar (link to profile)
- [ ] Lazy loading of avatar images

### 24.3 AvatarGroup Features
- [x] Overlapping layout
- [x] +N counter for overflow
- [ ] Max visible count (configurable)
- [ ] Tooltip on hover showing all names
- [ ] Click to expand full list

### 24.4 Testing
- [ ] Storybook story: image avatar
- [ ] Storybook story: initials fallback
- [ ] Storybook story: all sizes
- [ ] Storybook story: with status indicator
- [ ] Storybook story: avatar group
- [ ] Vitest: image loads and displays
- [ ] Vitest: fallback to initials on image error
- [ ] Vitest: deterministic color from name
- [ ] Vitest: AvatarGroup renders +N counter
- [ ] Accessibility test: avatar has alt text or aria-label

---

## 25. @orbit-ui/react -- Tag & TagInput

### 25.1 Implementation
- [x] Component file exists at `components/Tag/Tag.tsx`
- [x] `Tag` and `TagInput` exported from `src/index.ts`
- [x] `TagProps`, `TagInputProps`, `TagVariant`, `TagSize` types exported

### 25.2 Features
- [x] Color variants
- [x] Removable (X button)
- [x] With icon
- [x] TagInput component (type to add tags)
- [ ] Tag click handler
- [ ] Tag max width with ellipsis
- [ ] TagInput: autocomplete suggestions
- [ ] TagInput: max tags limit
- [ ] TagInput: paste comma-separated values

### 25.3 Testing
- [ ] Storybook story: all color variants
- [ ] Storybook story: removable
- [ ] Storybook story: with icon
- [ ] Storybook story: TagInput
- [ ] Vitest: Tag renders text
- [ ] Vitest: removable tag fires onRemove
- [ ] Vitest: TagInput adds tag on Enter
- [ ] Vitest: TagInput removes tag on Backspace
- [ ] Accessibility test: removable tag has dismiss button label

---

## 26. @orbit-ui/react -- Table

### 26.1 Implementation
- [x] Component file exists at `components/Table/Table.tsx`
- [x] Exported from `src/index.ts`
- [x] `TableProps`, `Column`, `SortDir` types exported

### 26.2 Features
- [x] Sortable headers (click to sort)
- [x] Sticky header option
- [x] Striped rows option
- [x] Hover highlight on rows
- [x] Empty state display
- [ ] Row selection (single select)
- [ ] Row selection (multi select with checkboxes)
- [ ] Sticky first column option
- [ ] Loading skeleton rows
- [ ] Pagination integration
- [ ] Resizable columns
- [ ] Column visibility toggle
- [ ] Expandable rows (detail view)
- [ ] Cell-level custom renderers
- [ ] Footer row (totals/summary)

### 26.3 Testing
- [ ] Storybook story: basic table with data
- [ ] Storybook story: sortable columns
- [ ] Storybook story: selectable rows
- [ ] Storybook story: empty state
- [ ] Storybook story: sticky header
- [ ] Storybook story: striped rows
- [ ] Vitest: renders columns and rows correctly
- [ ] Vitest: sort changes order
- [ ] Vitest: row selection fires callback
- [ ] Accessibility test: table has caption or aria-label
- [ ] Accessibility test: sortable headers have aria-sort

---

## 27. @orbit-ui/react -- EmptyState

### 27.1 Implementation
- [x] Component file exists at `components/EmptyState/EmptyState.tsx`
- [x] Exported from `src/index.ts`
- [x] `EmptyStateProps` type exported

### 27.2 Features
- [x] Title text
- [x] Description text
- [x] Illustration/icon slot
- [x] Action button slot
- [ ] Different sizes (sm, md, lg)
- [ ] Compact variant (inline, not full-page)
- [ ] Animated illustration option

### 27.3 Testing
- [ ] Storybook story: with illustration + title + description + action
- [ ] Storybook story: minimal (title only)
- [ ] Vitest: renders all content slots
- [ ] Vitest: action button fires callback
- [ ] Accessibility test: semantically grouped content

---

## 28. @orbit-ui/react -- Skeleton

### 28.1 Implementation
- [x] Component file exists at `components/Skeleton/Skeleton.tsx`
- [x] `Skeleton`, `SkeletonText`, `SkeletonCard` exported
- [x] `SkeletonProps` type exported

### 28.2 Features
- [x] Basic rectangle skeleton
- [x] `SkeletonText` — multi-line text placeholder
- [x] `SkeletonCard` — card-shaped placeholder
- [ ] Circle skeleton (avatar placeholder)
- [ ] Custom width/height props
- [ ] Pulse animation (default)
- [ ] Wave/shimmer animation option
- [ ] Table row skeleton preset

### 28.3 Testing
- [ ] Storybook story: basic skeleton shapes
- [ ] Storybook story: SkeletonText
- [ ] Storybook story: SkeletonCard
- [ ] Storybook story: composition (page-level loading state)
- [ ] Vitest: renders with correct dimensions
- [ ] Vitest: animation class applied
- [ ] Accessibility test: aria-busy="true" on loading container

---

## 29. @orbit-ui/react -- Spinner & PageLoader

### 29.1 Implementation
- [x] Component file exists at `components/Spinner/Spinner.tsx`
- [x] `Spinner` and `PageLoader` exported
- [x] `SpinnerProps` type exported

### 29.2 Features
- [x] Color variants
- [ ] Sizes: sm, md, lg
- [ ] Inline spinner (next to text)
- [ ] Full-page overlay loader (PageLoader)
- [ ] Custom spinner SVG/animation
- [ ] Label/text below spinner

### 29.3 Testing
- [ ] Storybook story: all sizes
- [ ] Storybook story: all colors
- [ ] Storybook story: PageLoader overlay
- [ ] Vitest: renders SVG spinner
- [ ] Vitest: applies size class
- [ ] Accessibility test: role="status"
- [ ] Accessibility test: aria-label="Loading"

---

## 30. @orbit-ui/react -- Progress & ProgressStacked

### 30.1 Implementation
- [x] Component file exists at `components/Progress/Progress.tsx`
- [x] `Progress` and `ProgressStacked` exported
- [x] `ProgressProps`, `ProgressStackedProps`, `ProgressSegment` types exported

### 30.2 Features
- [x] Linear progress bar
- [x] Sizes: xs, sm, md, lg
- [x] Color variants: default, success, warning, danger
- [x] Label/percentage display
- [x] Stacked/segmented progress bar
- [ ] Circular/ring progress variant
- [ ] Indeterminate/animated state (unknown progress)
- [ ] Striped animation variant

### 30.3 Testing
- [ ] Storybook story: determinate progress (0-100%)
- [ ] Storybook story: indeterminate
- [ ] Storybook story: all sizes
- [ ] Storybook story: all colors
- [ ] Storybook story: stacked segments
- [ ] Vitest: renders with correct width percentage
- [ ] Vitest: label displays correct percentage
- [ ] Accessibility test: role="progressbar"
- [ ] Accessibility test: aria-valuenow/min/max

---

## 31. @orbit-ui/react -- Divider

### 31.1 Implementation
- [x] Component file exists at `components/Divider/Divider.tsx`
- [x] Exported from `src/index.ts`
- [x] `DividerProps` type exported

### 31.2 Features
- [x] Horizontal orientation (default)
- [x] Vertical orientation
- [x] With label/text in center
- [x] Color variants: default, strong, subtle
- [ ] Dashed/dotted style variants
- [ ] Custom spacing (margin)

### 31.3 Testing
- [ ] Storybook story: horizontal
- [ ] Storybook story: vertical
- [ ] Storybook story: with label
- [ ] Vitest: renders hr element
- [ ] Vitest: vertical renders with correct class
- [ ] Accessibility test: role="separator"

---

## 32. @orbit-ui/react -- Alert

### 32.1 Implementation
- [x] Component file exists at `components/Alert/Alert.tsx`
- [x] Exported from `src/index.ts`
- [x] `AlertProps` type exported

### 32.2 Features
- [x] With icon
- [ ] Variants: info, success, warning, error
- [ ] Dismissible option (X close button)
- [ ] Title + description layout
- [ ] Action buttons
- [ ] Compact variant (single line)
- [ ] Banner variant (full width, no border-radius)

### 32.3 Testing
- [ ] Storybook story: all variants
- [ ] Storybook story: dismissible
- [ ] Storybook story: with title + description
- [ ] Storybook story: with action buttons
- [ ] Vitest: renders correct variant
- [ ] Vitest: dismiss button fires callback
- [ ] Accessibility test: role="alert"
- [ ] Accessibility test: dismissible alert has close button label

---

## 33. @orbit-ui/react -- Tooltip

### 33.1 Implementation
- [x] Component file exists at `components/Tooltip/Tooltip.tsx`
- [x] Exported from `src/index.ts`
- [x] `TooltipProps` type exported

### 33.2 Features
- [x] 4 placements: top, bottom, left, right
- [x] Configurable delay
- [x] Disabled state (hide tooltip)
- [ ] Arrow/pointer option
- [ ] Rich content (not just text — HTML/components)
- [ ] Touch device support (long press to show)
- [ ] Custom trigger (hover, focus, click)
- [ ] Max width constraint
- [ ] Portal rendering (escape overflow containers)

### 33.3 Testing
- [ ] Storybook story: all 4 placements
- [ ] Storybook story: with delay
- [ ] Storybook story: disabled
- [ ] Vitest: tooltip appears on hover
- [ ] Vitest: tooltip disappears on mouse leave
- [ ] Vitest: tooltip appears on focus
- [ ] Vitest: disabled tooltip does not appear
- [ ] Accessibility test: tooltip content linked via aria-describedby
- [ ] Accessibility test: Escape key dismisses tooltip

---

## 34. @orbit-ui/react -- Toast & ToastProvider

### 34.1 Implementation
- [x] Component file exists at `components/Toast/Toast.tsx`
- [x] `ToastProvider` and `useToast` exported
- [x] `ToastItem` and `ToastVariant` types exported

### 34.2 Features
- [x] Toast provider context wrapping app
- [x] `useToast()` hook for imperative toast creation
- [ ] Variants: info, success, warning, error
- [ ] Positions: top-right, top-center, top-left, bottom-right, bottom-center, bottom-left
- [ ] Auto-dismiss with configurable duration
- [ ] Action button support in toast
- [ ] Stackable with max visible limit
- [ ] Progress bar on toast (countdown to dismiss)
- [ ] Swipe-to-dismiss on mobile
- [ ] Pause auto-dismiss on hover
- [ ] Toast queue (show next after current dismissed)

### 34.3 Testing
- [ ] Storybook story: all variants
- [ ] Storybook story: all positions
- [ ] Storybook story: with action button
- [ ] Storybook story: stacked toasts
- [ ] Vitest: useToast creates toast
- [ ] Vitest: toast auto-dismisses after duration
- [ ] Vitest: toast dismiss button works
- [ ] Vitest: max visible limit enforced
- [ ] Accessibility test: role="alert" or aria-live="polite"
- [ ] Accessibility test: toast announced to screen readers

---

## 35. @orbit-ui/react -- Modal

### 35.1 Implementation
- [x] Component file exists at `components/Modal/Modal.tsx`
- [x] Exported from `src/index.ts`
- [x] `ModalProps` type exported

### 35.2 Features
- [x] Accessible dialog (focus trap, scroll lock)
- [ ] Sizes: sm, md, lg, xl, full
- [ ] Centered variant
- [ ] Slide-in variant (from top/bottom)
- [ ] Header, body, footer sections
- [ ] Close on backdrop click (configurable)
- [ ] Close on Escape key
- [ ] Focus trap (tab cycles within modal)
- [ ] Scroll locking (body scroll disabled)
- [ ] Nested modal support
- [ ] Transition animations (enter/exit)
- [ ] AlertDialog variant (confirm/cancel pattern)
- [ ] Render in portal (escape parent z-index)

### 35.3 Testing
- [ ] Storybook story: all sizes
- [ ] Storybook story: with header/body/footer
- [ ] Storybook story: nested modal
- [ ] Storybook story: alert dialog (confirm/cancel)
- [ ] Vitest: opens and closes correctly
- [ ] Vitest: Escape key closes modal
- [ ] Vitest: backdrop click closes modal (when enabled)
- [ ] Vitest: focus trapped within modal
- [ ] Vitest: body scroll locked when open
- [ ] Accessibility test: role="dialog"
- [ ] Accessibility test: aria-modal="true"
- [ ] Accessibility test: focus returns to trigger on close

---

## 36. @orbit-ui/react -- Drawer / Sheet

### 36.1 Implementation
- [x] Component file exists at `components/Drawer/Drawer.tsx`
- [x] Exported from `src/index.ts`
- [x] `DrawerProps`, `DrawerSide`, `DrawerSize` types exported

### 36.2 Features
- [x] Positions: left, right, top, bottom
- [x] Sizes: sm, md, lg, xl, full
- [x] Overlay backdrop
- [ ] Swipe-to-close on mobile
- [ ] Focus trap within drawer
- [ ] Scroll locking
- [ ] Close on Escape
- [ ] Close on backdrop click
- [ ] Transition animation (slide in/out)
- [ ] Header with close button
- [ ] Body with scrolling
- [ ] Footer with actions

### 36.3 Testing
- [ ] Storybook story: all positions
- [ ] Storybook story: all sizes
- [ ] Storybook story: with content sections
- [ ] Vitest: opens from correct side
- [ ] Vitest: closes on Escape
- [ ] Vitest: closes on backdrop click
- [ ] Accessibility test: role="dialog"
- [ ] Accessibility test: focus trapped

---

## 37. @orbit-ui/react -- Popover

### 37.1 Implementation
- [x] Component file exists at `components/Popover/Popover.tsx`
- [x] `Popover`, `PopoverHeader`, `PopoverBody`, `PopoverFooter` exported
- [x] `PopoverProps`, `PopoverAlign`, `PopoverSide` types exported

### 37.2 Features
- [x] Trigger element
- [x] Placement: top, bottom, left, right
- [x] Click trigger
- [ ] Arrow/pointer option
- [ ] Focus management (focus first focusable on open)
- [ ] Close on outside click
- [ ] Close on Escape
- [ ] Hover trigger option
- [ ] Nested popover support
- [ ] Portal rendering

### 37.3 Testing
- [ ] Storybook story: all placements
- [ ] Storybook story: with header/body/footer
- [ ] Storybook story: complex content
- [ ] Vitest: opens on trigger click
- [ ] Vitest: closes on outside click
- [ ] Vitest: closes on Escape
- [ ] Accessibility test: popover linked via aria-controls
- [ ] Accessibility test: trigger has aria-expanded

---

## 38. @orbit-ui/react -- Dropdown Menu

### 38.1 Implementation
- [x] Component files exist at `components/Dropdown/Dropdown.tsx`
- [x] `Dropdown`, `DropdownTrigger`, `DropdownContent`, `DropdownItem`, `DropdownSubTrigger`, `DropdownSeparator`, `DropdownLabel` exported
- [x] `DropdownProps`, `DropdownContentProps`, `DropdownItemProps` types exported

### 38.2 Features
- [x] Menu items with left and right icons
- [x] Sub-trigger with ChevronRight indicator (nested menus)
- [x] Dividers between groups
- [x] Labels/group headers
- [x] Keyboard: Escape to close
- [x] Outside-click to close
- [x] Disabled items
- [x] Checked menu items (checkbox-style)
- [x] Destructive item style (red text)
- [ ] Keyboard: arrow keys navigate items
- [ ] Keyboard: Enter/Space activates item
- [ ] Keyboard: typing jumps to matching item
- [ ] Search/filter within dropdown
- [ ] Multi-select mode
- [ ] Portal rendering

### 38.3 Testing
- [ ] Storybook story: basic menu
- [ ] Storybook story: with icons
- [ ] Storybook story: with submenus
- [ ] Storybook story: with checkbox items
- [ ] Storybook story: with destructive item
- [ ] Vitest: opens on trigger click
- [ ] Vitest: item click fires callback
- [ ] Vitest: Escape closes menu
- [ ] Vitest: disabled item not clickable
- [ ] Vitest: submenu opens on hover
- [ ] Accessibility test: role="menu"
- [ ] Accessibility test: items have role="menuitem"
- [ ] Accessibility test: active item has aria-selected

---

## 39. @orbit-ui/react -- ContextMenu

### 39.1 Implementation
- [x] Component file exists at `components/ContextMenu/ContextMenu.tsx`
- [x] Exported from `src/index.ts`
- [x] `ContextMenuProps`, `ContextMenuItemProps` types exported

### 39.2 Features
- [x] Right-click trigger
- [x] Same API as Dropdown Menu
- [x] Nested submenus
- [ ] Keyboard activation (Shift+F10 or context menu key)
- [ ] Position at cursor location
- [ ] Items with icons
- [ ] Disabled items
- [ ] Destructive items

### 39.3 Testing
- [ ] Storybook story: right-click trigger
- [ ] Storybook story: with submenus
- [ ] Vitest: opens on right-click (contextmenu event)
- [ ] Vitest: items clickable
- [ ] Vitest: closes on outside click
- [ ] Accessibility test: role="menu"

---

## 40. @orbit-ui/react -- CommandPalette

### 40.1 Implementation
- [x] Component file exists at `components/CommandPalette/CommandPalette.tsx`
- [x] `CommandPalette` and `useCommandPalette` exported
- [x] `CommandPaletteProps`, `CommandItem` types exported

### 40.2 Features
- [x] Search input with instant filtering
- [x] Categorized results
- [x] Keyboard navigation (arrow keys, Enter to select)
- [x] Shortcut display (e.g., Cmd+K)
- [x] Action execution on select
- [ ] Recent items section
- [ ] Extensible command registry (apps can register commands)
- [ ] Fuzzy search matching
- [ ] Result icons/avatars
- [ ] Loading state for async search
- [ ] Empty state message
- [ ] Nested pages (drill into category)

### 40.3 Testing
- [ ] Storybook story: with categories
- [ ] Storybook story: with shortcuts
- [ ] Storybook story: search filtering
- [ ] Vitest: search filters results
- [ ] Vitest: arrow keys navigate results
- [ ] Vitest: Enter selects result
- [ ] Vitest: Escape closes palette
- [ ] Accessibility test: role="dialog" or role="combobox"
- [ ] Accessibility test: search input has label
- [ ] Accessibility test: results linked via aria-activedescendant

---

## 41. @orbit-ui/react -- Sidebar

### 41.1 Implementation
- [x] Component file exists at `components/Sidebar/Sidebar.tsx`
- [x] `Sidebar` and `useSidebar` exported
- [x] `SidebarProps`, `SidebarItemProps` types exported

### 41.2 Features
- [x] Collapsible (icon-only mode)
- [x] Sections with headers
- [x] Navigation items with icons
- [ ] Expandable on hover (collapsed -> expanded on mouse enter)
- [ ] Active state indicator
- [ ] Badge/count indicators on items
- [ ] Footer section (settings, profile)
- [ ] Mobile: drawer overlay mode
- [ ] Keyboard shortcut to toggle collapse
- [ ] Nested item groups (expandable sub-items)
- [ ] Resize handle (user can drag width)

### 41.3 Testing
- [ ] Storybook story: expanded sidebar
- [ ] Storybook story: collapsed sidebar
- [ ] Storybook story: with sections and items
- [ ] Storybook story: mobile drawer mode
- [ ] Vitest: collapses on toggle
- [ ] Vitest: useSidebar hook returns correct state
- [ ] Vitest: items render with icons and labels
- [ ] Accessibility test: role="navigation"
- [ ] Accessibility test: collapse button has aria-expanded

---

## 42. @orbit-ui/react -- Tabs

### 42.1 Implementation
- [x] Component file exists at `components/Tabs/Tabs.tsx`
- [x] Exported from `src/index.ts`
- [x] `TabsProps`, `TabProps` types exported

### 42.2 Features
- [x] 3 variants (underline, pill/segment, boxed)
- [x] Controlled and uncontrolled modes
- [x] Lazy panel rendering
- [ ] Horizontal tabs (default)
- [ ] Vertical tabs
- [ ] With icons
- [ ] With badge counts
- [ ] Overflow scrolling for many tabs
- [ ] Closeable tabs (X button per tab)
- [ ] Draggable tab reordering

### 42.3 Testing
- [ ] Storybook story: all 3 variants
- [ ] Storybook story: with icons and badges
- [ ] Storybook story: controlled mode
- [ ] Storybook story: many tabs with overflow
- [ ] Vitest: switching tabs shows correct panel
- [ ] Vitest: lazy rendering only mounts active panel
- [ ] Vitest: keyboard: arrow keys switch tabs
- [ ] Accessibility test: role="tablist"
- [ ] Accessibility test: role="tab" on each tab
- [ ] Accessibility test: role="tabpanel" on content
- [ ] Accessibility test: aria-selected on active tab

---

## 43. @orbit-ui/react -- Breadcrumb

### 43.1 Implementation
- [x] Component file exists at `components/Breadcrumb/Breadcrumb.tsx`
- [x] Exported from `src/index.ts`
- [x] `BreadcrumbProps`, `BreadcrumbItem` types exported

### 43.2 Features
- [x] Auto-truncation with ellipsis for long paths
- [x] Custom separator
- [ ] Dropdown for truncated items (click ellipsis to see full path)
- [ ] Last item is text (not link)
- [ ] Custom item renderer

### 43.3 Testing
- [ ] Storybook story: basic breadcrumb
- [ ] Storybook story: with truncation
- [ ] Storybook story: custom separator
- [ ] Vitest: renders items as links
- [ ] Vitest: last item is not a link
- [ ] Accessibility test: nav with aria-label="Breadcrumb"
- [ ] Accessibility test: current page has aria-current="page"

---

## 44. @orbit-ui/react -- Pagination

### 44.1 Implementation
- [x] Component file exists at `components/Pagination/Pagination.tsx`
- [x] Exported from `src/index.ts`
- [x] `PaginationProps` type exported

### 44.2 Features
- [x] Page numbers
- [x] Previous/next buttons
- [x] First/last buttons
- [ ] Items per page selector
- [ ] Total count display
- [ ] Compact mode for mobile
- [ ] Ellipsis for large page counts
- [ ] Controlled page state

### 44.3 Testing
- [ ] Storybook story: basic pagination
- [ ] Storybook story: many pages with ellipsis
- [ ] Storybook story: compact mobile mode
- [ ] Vitest: page click fires callback with page number
- [ ] Vitest: previous/next navigate correctly
- [ ] Vitest: first/last buttons go to extremes
- [ ] Accessibility test: nav with aria-label="Pagination"
- [ ] Accessibility test: current page has aria-current="page"

---

## 45. @orbit-ui/react -- Steps / Stepper

### 45.1 Implementation
- [x] Component file exists at `components/Steps/Steps.tsx`
- [x] Exported from `src/index.ts`
- [x] `StepsProps`, `StepItem`, `StepStatus` types exported

### 45.2 Features
- [x] Horizontal steps
- [x] Vertical steps
- [x] States: completed, active, upcoming, error
- [x] With descriptions
- [ ] Clickable navigation (jump to step)
- [ ] Icon customization per step
- [ ] Connector line style variants
- [ ] Compact variant (numbers only, no labels)

### 45.3 Testing
- [ ] Storybook story: horizontal stepper
- [ ] Storybook story: vertical stepper
- [ ] Storybook story: all states
- [ ] Storybook story: clickable navigation
- [ ] Vitest: renders correct number of steps
- [ ] Vitest: active step highlighted
- [ ] Vitest: completed steps show check icon
- [ ] Accessibility test: step list has role
- [ ] Accessibility test: current step announced

---

## 46. @orbit-ui/react -- Accordion

### 46.1 Implementation
- [x] Component file exists at `components/Accordion/Accordion.tsx`
- [x] Exported from `src/index.ts`
- [x] `AccordionProps`, `AccordionItem` types exported

### 46.2 Features
- [x] Single expand mode (only one item open)
- [x] Multi expand mode (multiple items open)
- [ ] Default expanded items
- [ ] Controlled expand state
- [ ] Custom header renderer
- [ ] Icon customization (chevron, plus/minus)
- [ ] Bordered variant
- [ ] Flush variant (no borders/padding)

### 46.3 Testing
- [ ] Storybook story: single expand
- [ ] Storybook story: multi expand
- [ ] Storybook story: default expanded
- [ ] Vitest: clicking header toggles content
- [ ] Vitest: single mode collapses others
- [ ] Vitest: multi mode keeps others open
- [ ] Accessibility test: button trigger with aria-expanded
- [ ] Accessibility test: content region with role="region"
- [ ] Accessibility test: keyboard Enter/Space toggles

---

## 47. @orbit-ui/react -- FileUpload

### 47.1 Implementation
- [x] Component file exists at `components/FileUpload/FileUpload.tsx`
- [x] Exported from `src/index.ts`
- [x] `FileUploadProps`, `FileItem`, `FileUploadStatus` types exported

### 47.2 Features
- [x] Drag-and-drop zone
- [x] Upload progress indicator
- [ ] Click to browse files
- [ ] File type restrictions (accept prop)
- [ ] File size limit validation
- [ ] Multiple file upload
- [ ] File preview (image thumbnails)
- [ ] Remove uploaded file
- [ ] Retry failed upload
- [ ] Cancel in-progress upload

### 47.3 Testing
- [ ] Storybook story: drag-and-drop zone
- [ ] Storybook story: with file list and progress
- [ ] Storybook story: error state
- [ ] Vitest: file drop triggers upload callback
- [ ] Vitest: file click triggers upload callback
- [ ] Vitest: progress updates correctly
- [ ] Vitest: file type restriction works
- [ ] Accessibility test: drop zone has role and label
- [ ] Accessibility test: upload status announced

---

## 48. @orbit-ui/react -- ThemeProvider & ThemeToggle

### 48.1 Implementation
- [x] Component file exists at `components/ThemeToggle/ThemeToggle.tsx`
- [x] `ThemeProvider`, `ThemeToggle`, `useTheme` exported

### 48.2 Features
- [x] ThemeProvider wraps app, provides theme context
- [x] ThemeToggle renders toggle button
- [x] useTheme hook returns current theme + setTheme function
- [x] Persists to localStorage
- [x] Respects OS `prefers-color-scheme`
- [ ] System theme option (auto based on OS)
- [ ] Theme change animation (smooth transition)
- [ ] `onThemeChange` callback prop
- [ ] Server-side theme sync (persist to Gate user settings)

### 48.3 Testing
- [ ] Storybook story: theme toggle
- [ ] Vitest: ThemeProvider applies .dark class
- [ ] Vitest: useTheme returns correct theme
- [ ] Vitest: theme persists across renders
- [ ] Vitest: OS preference respected as default

---

## 49. @orbit-ui/react -- Planned / Missing Components

### 49.1 Not Yet Built
- [ ] `DataGrid` — virtual scroll, column resize, inline editing
- [ ] `Form` wrapper with field-level validation
- [ ] `RichTextEditor` — wrapper for Tiptap
- [ ] `Tree` — nested list with expand/collapse, drag-and-drop
- [ ] `ColorPicker` — preset palette, custom input, opacity
- [ ] `Box` — polymorphic base layout component
- [ ] `Flex` — direction, align, justify, wrap, gap props
- [ ] `Grid` — responsive columns, auto-fit/fill
- [ ] `Stack` (VStack, HStack) — vertical/horizontal with spacing
- [ ] `Container` — max-width, centered
- [ ] `Spacer` — flexible space filler
- [ ] `AspectRatio` — 1:1, 4:3, 16:9, 21:9
- [ ] `ScrollArea` — custom scrollbar, auto-hide
- [ ] `Timeline` — vertical/horizontal with icons/colors
- [ ] `Stat / KPI` — value, label, trend indicator
- [ ] `Code` — inline + code block with syntax highlighting
- [ ] `Banner` — full-width sticky, variants
- [ ] `List` — simple, with icons, with avatars, interactive
- [ ] `NavigationMenu` — horizontal with dropdowns, mega menu
- [ ] `Portal` — render children in document.body
- [ ] `VisuallyHidden` — screen reader only content
- [ ] `FocusTrap` — trap focus within container
- [ ] `ClickOutside` — detect clicks outside container
- [ ] `ResizeObserver` hook
- [ ] `IntersectionObserver` hook
- [ ] `Transition / AnimatePresence` — enter/exit animations

---

## 50. @orbit-ui/react -- Shared Hooks Library

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

---

## 51. Token Sync Script

### 51.1 Current Functionality
- [x] Script exists at `/orbit-ui/scripts/sync-tokens.sh`
- [x] Syncs `orbit-tokens.css` to all 16 app `public/orbit-ui/` dirs
- [x] Syncs `orbit-bar.js` to all 16 app `public/orbit-ui/` dirs
- [x] Syncs `orbit-ui.css` to all 16 app `public/orbit-ui/` dirs
- [x] Syncs `orbit-theme-init.js` to all 16 app `public/orbit-ui/` dirs
- [x] Syncs `orbit-tailwind-v4.css` to all 16 app `public/orbit-ui/` dirs

### 51.2 Missing Functionality
- [ ] Pre-commit hook that auto-runs sync on token file changes
- [ ] CI step that verifies all apps have latest tokens (diff check)
- [ ] Dry-run mode (show what would change without writing)
- [ ] Verbose logging (which files synced, which apps updated)
- [ ] Error handling (skip missing app dirs, report warnings)
- [ ] Checksum verification (only copy if content changed)
- [ ] Notification/log when sync completes
- [ ] Sync verification test (compare checksums across all apps)

---

## 52. App-by-App Token Integration Status

### 52.1 Atlas
- [x] `index.css` imports `orbit-tokens.css`
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root in `main.jsx`
- [x] Anti-FOUC script in `index.html`
- [x] Bulk semantic token migration (bg-gray -> bg-surface, text-gray -> text-content, border-gray -> border-border)
- [ ] Remove remaining hardcoded hex colors
- [ ] Visual consistency verified

### 52.2 Mail
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [x] `styles.css` imports `orbit-tokens.css`
- [ ] Anti-FOUC script in `index.html`
- [ ] Bulk semantic token migration
- [ ] Visual consistency verified

### 52.3 Connect
- [x] `ThemeProvider` wraps root
- [x] Anti-FOUC script in `index.html`
- [x] `index.css` imports `orbit-tokens.css`
- [x] `index.css` imports `orbit-tailwind-v4.css`
- [ ] Bulk semantic token migration
- [ ] Visual consistency verified

### 52.4 Meet
- [x] Anti-FOUC script in `index.html`
- [x] `ThemeProvider` wraps root
- [ ] `index.css` imports orbit-tokens.css
- [ ] Tailwind configured with orbit preset
- [ ] Bulk semantic token migration
- [ ] Visual consistency verified

### 52.5 Calendar
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Anti-FOUC script in `index.html`
- [ ] Visual consistency verified

### 52.6 Writer
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Visual consistency verified

### 52.7 Planet
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Visual consistency verified

### 52.8 Secure
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Visual consistency verified

### 52.9 Capital Hub
- [x] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Visual consistency verified

### 52.10 Control Center
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `ThemeProvider` wraps root
- [ ] Token integration
- [ ] Visual consistency verified

### 52.11 TurboTick
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `ThemeProvider` wraps root
- [x] Anti-FOUC script added
- [x] `orbit-tokens.css` imported
- [ ] Visual consistency verified

### 52.12 Dock
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `ThemeProvider` wraps root
- [x] Anti-FOUC script added
- [x] `orbit-tokens.css` imported
- [ ] Visual consistency verified

### 52.13 Wallet
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `ThemeProvider` wraps root
- [x] Anti-FOUC script added
- [x] `orbit-tokens.css` imported
- [ ] Visual consistency verified

### 52.14 FitterMe
- [ ] `tailwind.config.js` uses orbit preset
- [ ] `ThemeProvider` wraps root
- [x] Anti-FOUC script added
- [x] `orbit-tokens.css` imported
- [ ] Visual consistency verified

### 52.15 Learn
- [ ] `tailwind.config.js` uses orbit preset
- [x] `ThemeProvider` wraps root
- [ ] Visual consistency verified

---

## 53. EventBus Service

### 53.1 Core Service
- [ ] EventBus service running on port 6005
- [ ] Framework/runtime chosen (Node.js, Python FastAPI, Go)
- [ ] SSE stream endpoint (`GET /stream?token=&org_id=`)
- [ ] Publish endpoint (`POST /publish`)
- [ ] Health endpoint (`GET /health`)
- [ ] Metrics endpoint (`GET /metrics`)
- [ ] Readiness endpoint (`GET /ready`)

### 53.2 Event Types
- [ ] Event types documented: project, deal, calendar, mail, planet, connect, meet, writer, secure
- [ ] Event schema validation (JSON Schema or Pydantic/Zod)
- [ ] Event schema versioning
- [ ] Event type registry (catalog of all event types)
- [ ] Event payload size limit enforcement
- [ ] Event timestamp (server-side, UTC)
- [ ] Event correlation ID (trace across services)

### 53.3 Delivery & Reliability
- [ ] Dead-letter queue for failed deliveries
- [ ] Replay last N events on reconnect
- [ ] Event ordering guarantees (per-channel FIFO)
- [ ] At-least-once delivery guarantee
- [ ] Duplicate detection (idempotency key)
- [ ] Retry with exponential backoff for failed deliveries
- [ ] Event persistence (store events for replay window)
- [ ] Event TTL (auto-purge old events)

### 53.4 Security & Isolation
- [ ] Per-org event isolation (no cross-tenant leakage)
- [ ] Auth: Gate JWT token required to subscribe
- [ ] Auth: Gate JWT token required to publish
- [ ] Token validation on every connection
- [ ] Rate limiting per client
- [ ] Rate limiting per org
- [ ] Event payload sanitization (XSS prevention)

### 53.5 Transport
- [ ] SSE as primary transport
- [ ] WebSocket fallback for SSE-blocked environments
- [ ] HTTP long-polling fallback as last resort
- [ ] Connection keepalive (heartbeat every 30s)
- [ ] Auto-reconnect with exponential backoff (client-side)
- [ ] Connection count limits per org

### 53.6 Client SDK
- [ ] JavaScript/TypeScript client library
- [ ] `subscribe(channel, handler)` method
- [ ] `publish(channel, event)` method
- [ ] Auto-reconnect built into client
- [ ] React hook: `useOrbitEventBus(channel, handler)`
- [ ] Connection status events (connected, disconnected, reconnecting)
- [ ] Client-side event buffering during disconnection

### 53.7 Monitoring
- [ ] Connection count metrics (gauge)
- [ ] Events published per second (rate)
- [ ] Events delivered per second (rate)
- [ ] Event delivery latency (histogram)
- [ ] Dead letter queue depth (gauge)
- [ ] Error rate (counter)
- [ ] Dashboard for EventBus monitoring

### 53.8 Testing
- [ ] Unit test: event schema validation
- [ ] Unit test: per-org isolation
- [ ] Integration test: publish event → SSE client receives
- [ ] Integration test: reconnect replays missed events
- [ ] Load test: 1000 concurrent SSE connections
- [ ] Load test: 100 events/second throughput

---

## 54. Gate Authentication (AuthX)

### 54.1 OAuth2/OIDC Core
- [ ] OIDC discovery endpoint (`/.well-known/openid-configuration`)
- [ ] JWKS endpoint (`/.well-known/jwks.json`) production-ready
- [ ] PKCE OAuth2 flow fully tested end-to-end
- [ ] Authorization code flow for server-side apps
- [ ] Client credentials flow for service-to-service
- [ ] Token introspection endpoint
- [ ] Token revocation endpoint
- [ ] Refresh token rotation with reuse detection
- [ ] Token expiration (configurable: access=15m, refresh=7d)

### 54.2 Session Management
- [ ] Concurrent sessions per user (configurable limit)
- [ ] Session listing UI (show all active sessions)
- [ ] Remote session kill (invalidate from settings page)
- [ ] Session device fingerprint (browser, OS, IP)
- [ ] Step-up authentication for sensitive operations
- [ ] Remember device / trusted device management

### 54.3 JWT Claims
- [ ] Org-scoped claims in JWT (`org_id`, `roles`, `permissions`)
- [ ] User claims: `sub`, `email`, `name`, `picture`
- [ ] Custom claims support (app-specific)
- [ ] Claim refresh on org/role change

### 54.4 Multi-Factor Authentication
- [ ] TOTP (Google Authenticator / Authy) support
- [ ] WebAuthn / FIDO2 (hardware keys, biometrics)
- [ ] SMS OTP (Twilio integration)
- [ ] Email OTP
- [ ] Recovery codes generation and management
- [ ] Enforce MFA per organization policy
- [ ] Enforce MFA per role
- [ ] MFA challenge on new device/location
- [ ] Backup MFA method requirement

### 54.5 Social SSO
- [ ] Google OAuth
- [ ] GitHub OAuth
- [ ] Microsoft Entra (Azure AD)
- [ ] SAML 2.0 IdP support (enterprise)

### 54.6 Directory & User Management
- [ ] SCIM 2.0 provisioning endpoint
- [ ] User create/update/delete/disable
- [ ] Group create/update/delete
- [ ] Bulk operations
- [ ] JIT provisioning from SAML
- [ ] User profile fields (name, avatar, bio, timezone, locale)
- [ ] User status (active, suspended, invited, deactivated)
- [ ] User search and filtering
- [ ] Bulk user import (CSV)
- [ ] Bulk user export

### 54.7 Organization & Tenant Management
- [ ] Organization CRUD
- [ ] Organization settings (name, logo, domain, billing plan)
- [ ] Custom branding per org (logo, colors, favicon, login background)
- [ ] Custom domain per org (CNAME mapping)
- [ ] Organization member management (invite, remove, role change)
- [ ] Organization-level feature flags
- [ ] Organization data export (GDPR)
- [ ] Organization data deletion (GDPR right to erasure)
- [ ] Multi-org membership for users

### 54.8 Roles & Permissions
- [ ] RBAC: Owner, Admin, Member, Guest, Billing built-in roles
- [ ] Custom roles with granular permissions
- [ ] Permission inheritance (org -> project -> resource)
- [ ] ABAC for advanced policies
- [ ] Permission check API for all apps
- [ ] Role assignment UI
- [ ] Permission audit view

### 54.9 API Keys & Service Accounts
- [ ] Personal API key generation
- [ ] Org-level API key management
- [ ] API key scoping (per-app, per-permission)
- [ ] API key expiration
- [ ] API key usage tracking
- [ ] Service account creation
- [ ] Service account key rotation

### 54.10 Security
- [ ] Rate limiting on auth endpoints
- [ ] Brute force protection (lockout after N failures)
- [ ] Email verification flow
- [ ] Password strength enforcement
- [ ] Password breach check (HaveIBeenPwned API)
- [ ] Account lockout with admin unlock
- [ ] IP allowlist/denylist per org
- [ ] Suspicious activity detection (impossible travel, etc.)

### 54.11 Audit Log
- [ ] Authentication event logging (login, logout, MFA, failed attempts)
- [ ] Admin action logging
- [ ] Permission change logging
- [ ] Audit log search and filtering
- [ ] Audit log export (CSV, JSON)
- [ ] Audit log retention policies
- [ ] Real-time audit stream to external SIEM

### 54.12 Gate UI
- [ ] Login page with org branding
- [ ] Registration page
- [ ] Forgot password flow
- [ ] Reset password flow
- [ ] MFA enrollment flow
- [ ] MFA challenge flow
- [ ] Profile settings page
- [ ] Security settings page (sessions, MFA, API keys)
- [ ] Organization settings page
- [ ] User management page (admin)
- [ ] Role management page (admin)
- [ ] Audit log viewer (admin)
- [ ] Branding customization page (admin)
- [ ] Developer dashboard (token inspector, key manager)

### 54.13 Testing
- [ ] Unit tests: token generation and validation
- [ ] Unit tests: password hashing
- [ ] Unit tests: PKCE flow
- [ ] Integration tests: full login flow (register -> login -> token -> API call)
- [ ] Integration tests: MFA enrollment and challenge
- [ ] Integration tests: refresh token rotation
- [ ] E2E tests: SSO flow with Gate
- [ ] Security tests: brute force protection
- [ ] Security tests: token expiration enforcement
- [ ] Load tests: concurrent login attempts

---

## 55. Gateway / Reverse Proxy

### 55.1 Core Setup
- [ ] Gateway/proxy service chosen (Nginx, Traefik, Caddy, custom)
- [ ] Routes all app frontends under single domain
- [ ] Routes all API backends under `/api/{app}/` path
- [ ] SSL/TLS termination
- [ ] HTTP/2 support
- [ ] gzip/brotli compression

### 55.2 Routing
- [ ] `atlas.freedomlabs.in` -> Atlas frontend
- [ ] `mail.freedomlabs.in` -> Mail frontend
- [ ] `chat.freedomlabs.in` -> Connect frontend
- [ ] `meet.freedomlabs.in` -> Meet frontend
- [ ] `calendar.freedomlabs.in` -> Calendar frontend
- [ ] `docs.freedomlabs.in` -> Writer frontend
- [ ] `planet.freedomlabs.in` -> Planet frontend
- [ ] `secure.freedomlabs.in` -> Secure frontend
- [ ] `capital.freedomlabs.in` -> Capital Hub frontend
- [ ] `center.freedomlabs.in` -> Control Center frontend
- [ ] API routing: `/api/mail/*` -> Mail backend
- [ ] API routing: `/api/atlas/*` -> Atlas backend
- [ ] API routing: `/api/gate/*` -> Gate backend

### 55.3 Security
- [ ] Rate limiting per IP
- [ ] Rate limiting per authenticated user
- [ ] CORS configuration (allow Orbit domains only)
- [ ] Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] WAF rules (SQL injection, XSS protection)
- [ ] DDoS protection
- [ ] Request body size limit

### 55.4 Performance
- [ ] Static asset caching (immutable fingerprinted files: 1 year)
- [ ] API response caching (where appropriate)
- [ ] CDN integration for static assets
- [ ] Connection pooling to backends
- [ ] Health check routing (remove unhealthy backends)
- [ ] Load balancing across backend replicas

### 55.5 Monitoring
- [ ] Access logs (structured JSON)
- [ ] Error logs
- [ ] Request latency metrics
- [ ] Upstream error rate metrics
- [ ] Active connection count
- [ ] Dashboard for gateway monitoring

---

## 56. Storybook & Documentation

### 56.1 Storybook Setup
- [ ] Storybook 8 installed with Vite builder
- [ ] Storybook configured with orbit design tokens (CSS import)
- [ ] Storybook dark mode toggle addon
- [ ] Storybook accessibility addon (a11y)
- [ ] Storybook viewport addon (responsive testing)
- [ ] Storybook actions addon (event logging)
- [ ] Storybook controls addon (prop playground)
- [ ] Storybook docs addon (auto-generated docs)

### 56.2 Stories (per component — all 36)
- [ ] Button stories (all variants, sizes, states)
- [ ] IconButton stories
- [ ] ButtonGroup stories
- [ ] Input stories (all sizes, states, prefix/suffix)
- [ ] Textarea stories
- [ ] Select stories
- [ ] Checkbox stories
- [ ] Radio/RadioGroup stories
- [ ] Switch stories
- [ ] Slider stories
- [ ] NumberInput stories
- [ ] DatePicker stories
- [ ] TimePicker stories
- [ ] Badge stories
- [ ] Card stories
- [ ] Avatar/AvatarGroup stories
- [ ] Tag/TagInput stories
- [ ] Table stories
- [ ] EmptyState stories
- [ ] Skeleton stories
- [ ] Spinner/PageLoader stories
- [ ] Progress stories
- [ ] Divider stories
- [ ] Alert stories
- [ ] Tooltip stories
- [ ] Toast stories
- [ ] Modal stories
- [ ] Drawer stories
- [ ] Popover stories
- [ ] Dropdown stories
- [ ] ContextMenu stories
- [ ] CommandPalette stories
- [ ] Sidebar stories
- [ ] Tabs stories
- [ ] Breadcrumb stories
- [ ] Pagination stories
- [ ] Steps stories
- [ ] Accordion stories
- [ ] FileUpload stories
- [ ] ThemeToggle stories

### 56.3 Interaction Tests
- [ ] Button click interaction test
- [ ] Modal open/close interaction test
- [ ] Dropdown open/select/close interaction test
- [ ] Tabs switching interaction test
- [ ] Form submission interaction test
- [ ] Drag-and-drop interaction test (FileUpload)

### 56.4 Deployment
- [ ] Storybook deployed to URL for team access
- [ ] Storybook auto-deploys on merge to main
- [ ] Storybook URL documented in README

### 56.5 Component Documentation
- [ ] Component usage guidelines (each component)
- [ ] Do's and don'ts for each component
- [ ] Page-level composition examples (login, dashboard, settings, list, detail)
- [ ] Token usage guidelines (color, typography, spacing, shadows)
- [ ] Migration guide: replacing app-specific components with @orbit-ui/react
- [ ] Contributing guide: how to add new components

---

## 57. CI/CD & Build Pipeline

### 57.1 Build
- [ ] orbit-ui/react builds on every PR
- [ ] TypeScript type-checking passes on every PR
- [ ] ESLint passes on every PR
- [ ] Bundle size check on every PR (fail if over budget)
- [ ] Token sync verification on every PR

### 57.2 Tests
- [ ] Vitest runs on every PR
- [ ] Storybook build succeeds on every PR
- [ ] Accessibility audit runs on every PR
- [ ] Visual regression tests on every PR (Chromatic or similar)

### 57.3 Deployment
- [ ] Storybook auto-deploys on merge to main
- [ ] npm publish (or workspace link update) on version bump
- [ ] All consuming apps rebuild when orbit-ui changes
- [ ] Canary/preview deployments for PRs

### 57.4 Quality Gates
- [ ] Minimum test coverage requirement (80%+)
- [ ] No type errors gate
- [ ] No lint errors gate
- [ ] Bundle size budget gate
- [ ] Accessibility score gate

---

## 58. Testing -- Shared Infrastructure

### 58.1 Unit Tests
- [ ] Vitest configured for @orbit-ui/react
- [ ] Tests for every exported component (36 components)
- [ ] Tests for every exported hook
- [ ] Tests for cn() utility
- [ ] Tests for ThemeProvider context
- [ ] Code coverage report generation
- [ ] Coverage threshold: 80% minimum

### 58.2 Integration Tests
- [ ] Component composition tests (e.g., Modal with Form inside)
- [ ] Theme switching tests (light -> dark -> system)
- [ ] Responsive rendering tests

### 58.3 Visual Regression Tests
- [ ] Chromatic or Percy configured
- [ ] Snapshot for every Storybook story
- [ ] Dark mode snapshots
- [ ] Mobile viewport snapshots

### 58.4 Accessibility Tests
- [ ] axe-core integration in Storybook
- [ ] Automated a11y audit for every component
- [ ] Screen reader testing checklist
- [ ] Keyboard navigation testing checklist

---

## 59. Security -- Shared Infrastructure

### 59.1 Supply Chain
- [ ] Dependency audit (npm audit) on every build
- [ ] Dependabot or Renovate for automated dependency updates
- [ ] Lock file committed (package-lock.json or pnpm-lock.yaml)
- [ ] No known high/critical vulnerabilities in dependencies

### 59.2 Code Security
- [ ] No inline styles with user-provided content (XSS vector)
- [ ] All user-facing strings sanitized
- [ ] No eval() or Function() usage
- [ ] Content Security Policy compatible

### 59.3 Auth Security
- [ ] All API calls use httpOnly cookies (not localStorage tokens)
- [ ] CSRF protection on all state-changing endpoints
- [ ] Token refresh handled transparently
- [ ] Logout clears all auth state

---

## 60. Performance -- Shared Infrastructure

### 60.1 Bundle
- [ ] Tree-shaking verified (unused components not in app bundles)
- [ ] Component code splitting (dynamic imports)
- [ ] CSS purging (unused utility classes removed)
- [ ] Total @orbit-ui/react bundle < 100KB gzipped
- [ ] Per-component bundle size tracked

### 60.2 Runtime
- [ ] Components use React.memo where appropriate
- [ ] Context providers avoid unnecessary re-renders
- [ ] Event listeners cleaned up on unmount
- [ ] No memory leaks in overlay components (modal, drawer, popover)

### 60.3 CSS
- [ ] Token CSS file < 10KB gzipped
- [ ] No duplicate CSS declarations across token files
- [ ] CSS custom properties used for theme switching (no class duplication)

---

## 61. Accessibility -- Cross-Cutting

- [ ] Skip links in all 16 apps (standardized from shared component)
- [ ] All interactive elements keyboard accessible
- [ ] All icon buttons have aria-labels
- [ ] Color contrast meets WCAG 2.1 AA in light mode
- [ ] Color contrast meets WCAG 2.1 AA in dark mode
- [ ] Focus-visible ring on all interactive elements (standardized)
- [ ] Roving tabindex in all list/grid components
- [ ] All modals trap focus
- [ ] All modals return focus on close
- [ ] Screen reader announcements for toasts/notifications
- [ ] `role` attributes on all landmark regions
- [ ] `prefers-reduced-motion` support
- [ ] `prefers-contrast` support (high contrast mode)
- [ ] `forced-colors` mode support
- [ ] Tested with VoiceOver (macOS)
- [ ] Tested with NVDA (Windows)
- [ ] Tested with keyboard-only navigation (all apps)

---

## 62. Typography Consistency

- [ ] Audit all apps for font-family declarations — remove non-standard fonts
- [ ] RM Forma used for all body text in all apps
- [ ] RM Samplet used for all display/hero text
- [ ] JetBrains Mono used for all code/monospace
- [ ] Standardize heading sizes (h1-h6) across all apps
- [ ] Standardize body text size (16px base) across all apps
- [ ] Standardize line-height across all apps
- [ ] Remove all inline font-size overrides that break the scale
- [ ] Font files loaded consistently (woff2 preferred)
- [ ] `font-display: swap` on all font-face
- [ ] Test font rendering on Windows, macOS, Linux
- [ ] Test font rendering in Chrome, Firefox, Safari, Edge

---

## 63. Icon System Consistency

- [ ] Pin `lucide-react` version across all apps (latest stable)
- [ ] Create icon usage guide (which icons for which actions)
- [ ] Standardize icon sizes: sm (16px), md (20px), lg (24px), xl (32px)
- [ ] Remove Material Symbols dependency from Meet
- [ ] Replace Material Symbols with Lucide equivalents in Meet
- [ ] Audit all apps for inconsistent icon usage
- [ ] Ensure all interactive icons have aria-labels or aria-hidden
- [ ] Verify icon color follows text color tokens

---

## 64. Animation & Motion Language

- [ ] Standardize on `motion` (Framer Motion successor) as animation library
- [ ] Remove `framer-motion` dependency (upgrade to `motion`)
- [ ] Shared animation presets in `@orbit-ui/react`:
  - [ ] `fadeIn` / `fadeOut`
  - [ ] `slideUp` / `slideDown` / `slideLeft` / `slideRight`
  - [ ] `scaleIn` / `scaleOut`
  - [ ] `stagger` (children animation)
  - [ ] `skeleton` (shimmer/pulse)
  - [ ] `spring` (interactive feedback)
- [ ] `prefers-reduced-motion` respected across all animations
- [ ] Document motion principles (when to animate, duration guidelines)
- [ ] Maximum animation duration: 500ms for UI feedback
- [ ] No animations on essential state changes (data load, navigation)

---

## 65. Glassmorphism Design Language

- [ ] Glassmorphism token set defined:
  - [ ] `glass-bg`: light and dark values
  - [ ] `glass-blur`: `blur(12px)`
  - [ ] `glass-border`: rgba-based border
  - [ ] `glass-shadow`: from shadow tokens
- [x] `.glass` Tailwind utility class via plugin
- [x] `.glass-sm` Tailwind utility class
- [x] `.glass-subtle` Tailwind utility class
- [ ] Applied consistently to: modals, sidebars, floating panels, dropdowns
- [ ] Degrades gracefully on non-supporting browsers (no backdrop-filter)
- [ ] Tested on low-performance devices (disable if FPS drops)
- [ ] Tested in both light and dark modes
- [ ] `prefers-reduced-transparency` support

---

## 66. Responsive Design Standards

- [ ] Responsive breakpoint strategy documented:
  - [ ] sm: 640px
  - [ ] md: 768px
  - [ ] lg: 1024px
  - [ ] xl: 1280px
  - [ ] 2xl: 1536px
- [ ] Mobile-first design patterns defined for each component
- [ ] Sidebar collapse behavior at tablet breakpoint (all apps)
- [ ] Navigation switch to hamburger at mobile breakpoint
- [ ] Test all apps at 320px viewport
- [ ] Test all apps at 375px viewport
- [ ] Test all apps at 768px viewport
- [ ] Test all apps at 1024px viewport
- [ ] Test all apps at 1440px viewport
- [ ] Test all apps at 1920px viewport
- [ ] Test with touch interactions on mobile viewport
- [ ] Touch targets minimum 44x44px on mobile
- [ ] No horizontal scroll on any viewport

---

## Summary

| Section | Done | Todo | Total |
|---------|------|------|-------|
| Design Tokens | ~45 | ~25 | ~70 |
| orbit-tokens.css | ~25 | ~15 | ~40 |
| Tailwind Preset | ~25 | ~12 | ~37 |
| orbit-bar | ~10 | ~40 | ~50 |
| Anti-FOUC | ~5 | ~6 | ~11 |
| @orbit-ui/react (36 components) | ~120 | ~350 | ~470 |
| Shared Hooks | 0 | ~21 | ~21 |
| Token Sync | ~6 | ~8 | ~14 |
| App Integration | ~25 | ~20 | ~45 |
| EventBus | 0 | ~55 | ~55 |
| Gate Auth | 0 | ~95 | ~95 |
| Gateway | 0 | ~35 | ~35 |
| Storybook & Docs | 0 | ~55 | ~55 |
| CI/CD | 0 | ~15 | ~15 |
| Testing | 0 | ~20 | ~20 |
| Security | 0 | ~10 | ~10 |
| Performance | 0 | ~12 | ~12 |
| Accessibility | 0 | ~17 | ~17 |
| Typography | 0 | ~12 | ~12 |
| Icons | 0 | ~8 | ~8 |
| Animation | 0 | ~14 | ~14 |
| Glass | ~3 | ~8 | ~11 |
| Responsive | 0 | ~15 | ~15 |
| **TOTAL** | **~264** | **~868** | **~1132** |
