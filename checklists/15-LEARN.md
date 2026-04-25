# 15 Learn -- Documentation Portal

> **Full-Name:** RM Orbit Learn
> **Purpose:** Documentation Portal (comparable to Docusaurus / GitBook) for the entire RM Orbit ecosystem
> **Stack:** React 18.2.0, Vite 5.0.0, React Router v6, Zustand, Tailwind CSS v3, Axios
> **Source:** `/Learn/frontend/src/`
> **Pages:** Home.tsx, Quickstart.tsx, ApiReference.tsx
> **Components:** Layout.tsx (header, sidebar, footer, mobile drawer)
> **Status:** ~50% feature complete -- Design system integrated, 3 pages built, basic nav done
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

### 1.1 Vite Configuration
- [x] Vite 5 project initialized with React 18 template
- [x] `vite.config.ts` present and configured
- [ ] Path aliases configured (`@/` -> `src/`)
- [ ] Path alias for `@components/` -> `src/components/`
- [ ] Path alias for `@pages/` -> `src/pages/`
- [ ] Path alias for `@hooks/` -> `src/hooks/`
- [ ] Path alias for `@stores/` -> `src/stores/`
- [ ] Path alias for `@utils/` -> `src/utils/`
- [ ] Path alias for `@types/` -> `src/types/`
- [ ] Path alias for `@assets/` -> `src/assets/`
- [ ] Vite chunk splitting strategy (vendor, router, markdown renderer)
- [ ] Vite manual chunk config for `react`, `react-dom`, `react-router-dom`
- [ ] Vite manual chunk config for markdown/highlight libraries
- [ ] Vite build target set to `es2020`
- [ ] Vite preview server configured for local testing
- [ ] Vite env variable prefix set to `VITE_`
- [ ] Source maps enabled for development, disabled for production
- [ ] Vite CSS PostCSS config with Tailwind and autoprefixer
- [ ] Vite dev server proxy for backend API calls
- [ ] Vite HMR (Hot Module Replacement) confirmed working
- [ ] Vite plugin: `@vitejs/plugin-react` installed and configured
- [ ] Vite plugin: `vite-plugin-svgr` for SVG as React components
- [ ] Vite plugin: `vite-plugin-compression` for gzip/brotli
- [ ] Vite plugin: `rollup-plugin-visualizer` for bundle analysis

### 1.2 TypeScript Configuration
- [ ] `tsconfig.json` with strict mode enabled
- [ ] `tsconfig.json` path aliases match Vite aliases
- [ ] `tsconfig.json` `jsx` set to `react-jsx`
- [ ] `tsconfig.json` `target` set to `ES2020`
- [ ] `tsconfig.json` `moduleResolution` set to `bundler`
- [ ] `tsconfig.json` `skipLibCheck` enabled
- [ ] `tsconfig.json` `forceConsistentCasingInFileNames` enabled
- [ ] `tsconfig.json` `noUnusedLocals` enabled
- [ ] `tsconfig.json` `noUnusedParameters` enabled
- [ ] `tsconfig.json` `noFallthroughCasesInSwitch` enabled
- [ ] Type definitions for global env variables (`ImportMetaEnv`)
- [ ] Shared type definitions barrel file `src/types/index.ts`
- [ ] Types for documentation content (DocPage, DocSection, TOCItem)
- [ ] Types for search results (SearchResult, SearchIndex)
- [ ] Types for API reference (ApiGroup, Endpoint, Param)
- [ ] Types for feedback (FeedbackPayload, FeedbackResponse)
- [ ] Types for forum (ForumPost, ForumComment, ForumThread)
- [ ] Types for user preferences (UserPrefs, ThemeChoice)

### 1.3 Package Configuration
- [x] `package.json` present with correct dependencies
- [x] React 18 installed
- [x] React Router v6 installed
- [x] Tailwind CSS v3 installed
- [ ] Zustand installed and configured
- [ ] Axios installed and configured
- [ ] `lucide-react` icon library (confirmed in codebase)
- [ ] ESLint configuration with React rules
- [ ] ESLint plugin: `eslint-plugin-react`
- [ ] ESLint plugin: `eslint-plugin-react-hooks`
- [ ] ESLint plugin: `eslint-plugin-jsx-a11y`
- [ ] ESLint plugin: `eslint-plugin-import`
- [ ] Prettier configuration (`.prettierrc`)
- [ ] Prettier + ESLint integration (no conflicts)
- [ ] Husky pre-commit hook for linting
- [ ] lint-staged configuration
- [ ] `.nvmrc` specifying Node version (18+)
- [ ] `.gitignore` covering `node_modules`, `dist`, `.env`
- [ ] `engines` field in package.json requiring Node 18+
- [ ] `browserslist` field or `.browserslistrc`
- [ ] Lock file committed (`package-lock.json`)

### 1.4 Tailwind Configuration
- [x] `tailwind.config.js` uses orbit preset
- [ ] `tailwind.config.js` content paths include all TSX/TS files
- [ ] `tailwind.config.js` extends theme with Learn-specific tokens
- [ ] `tailwind.config.js` prose plugin for markdown rendering
- [ ] `tailwind.config.js` typography plugin (`@tailwindcss/typography`)
- [ ] `tailwind.config.js` forms plugin (`@tailwindcss/forms`)
- [ ] `tailwind.config.js` scrollbar-thin plugin configured
- [ ] `tailwind.config.js` container-queries plugin
- [ ] Custom animation keyframes: `fade-in`, `slide-in-left`, `slide-in-right`
- [ ] Custom animation keyframes: `scale-in`, `skeleton-pulse`
- [ ] Custom animation: `accordion-expand`, `accordion-collapse`
- [ ] Custom color aliases for doc-specific needs (callout colors)

### 1.5 Entry Points
- [x] `main.tsx` renders `<App />` into `#root`
- [x] `index.css` imports orbit tokens CSS
- [x] `index.css` Tailwind directives (`@tailwind base; components; utilities`)
- [x] `index.html` present
- [x] Anti-FOUC script in `index.html`
- [ ] `index.html` meta tags: charset, viewport, description
- [ ] `index.html` Open Graph meta tags (og:title, og:description, og:image)
- [ ] `index.html` Twitter Card meta tags
- [ ] `index.html` canonical URL tag
- [ ] `index.html` favicon (SVG + PNG fallback)
- [ ] `index.html` Apple touch icon
- [ ] `index.html` manifest.json link for PWA
- [ ] Web app manifest with name, icons, theme_color
- [ ] Robots.txt configured
- [ ] Sitemap.xml generation (build-time or runtime)

### 1.6 Environment Variables
- [ ] `VITE_API_URL` -- backend API base URL
- [ ] `VITE_GATE_URL` -- Gate auth service URL
- [ ] `VITE_GATE_CLIENT_ID` -- OAuth client ID for Learn
- [ ] `VITE_SEARCH_API_URL` -- search service endpoint
- [ ] `VITE_ANALYTICS_ID` -- analytics tracking ID
- [ ] `VITE_ALGOLIA_APP_ID` -- Algolia application ID (if used)
- [ ] `VITE_ALGOLIA_SEARCH_KEY` -- Algolia public search key (if used)
- [ ] `VITE_DOCS_VERSION` -- current docs version
- [ ] `VITE_GITHUB_REPO_URL` -- repo URL for "Edit this page" links
- [ ] `VITE_FORUM_API_URL` -- forum backend URL
- [ ] `.env.example` file with all required variables documented
- [ ] `.env.development` with sensible development defaults
- [ ] `.env.production` template
- [ ] Environment variable validation at startup

---

## 2. Design System Integration

### 2.1 Orbit UI Core
- [x] `@orbit-ui/react` installed as dependency
- [x] `ThemeProvider` wraps root in `App.tsx`
- [x] `ThemeToggle` component used in Layout header
- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css";`
- [ ] Replace hardcoded sidebar bg with `bg-surface-subtle`
- [ ] Replace hardcoded nav active state with `bg-primary-50 text-primary-600`
- [ ] Replace hardcoded `text-slate-400` instances with `text-content-muted`
- [ ] Replace hardcoded `text-slate-700` instances with `text-content-primary`
- [ ] Replace hardcoded `bg-slate-700` instances with `bg-surface-muted`
- [ ] Replace hardcoded `ring-slate-200` instances with `ring-border-default`
- [ ] Replace hardcoded `ring-slate-600` instances with `ring-border-subtle`
- [ ] Replace hardcoded `text-slate-200` instances with `text-content-secondary`
- [ ] Replace hardcoded `dark:bg-slate-900` in Layout footer with `dark:bg-surface-base`
- [ ] Replace hardcoded `dark:bg-neutral-900` in sidebar with `dark:bg-surface-base`
- [ ] Replace `dark:bg-slate-700` in Cmd+K badge with `dark:bg-surface-muted`
- [ ] Consistent use of `border-border-default` on all borders

### 2.2 Orbit UI Component Adoption
- [ ] Adopt `<Badge>` for "New" labels on doc pages
- [ ] Adopt `<Badge>` for "Updated" labels on doc pages
- [ ] Adopt `<Badge>` for "Beta" labels on doc pages
- [ ] Adopt `<Badge>` for "Deprecated" labels on doc pages
- [ ] Adopt `<Badge>` for version indicators
- [ ] Adopt `<Badge>` for HTTP method badges (GET, POST, PUT, DELETE, PATCH)
- [ ] Adopt `<Tabs>` for API reference sections (endpoint / parameters / response / examples)
- [ ] Adopt `<Tabs>` for code block language switcher (bash / JS / Python / curl)
- [ ] Adopt `<Tabs>` for installation method (npm / yarn / pnpm)
- [ ] Adopt `<Alert>` for info callout boxes
- [ ] Adopt `<Alert>` for warning callout boxes
- [ ] Adopt `<Alert>` for error/danger callout boxes
- [ ] Adopt `<Alert>` for deprecation notices
- [ ] Adopt `<Alert>` for "tip" callout boxes
- [ ] Adopt `<Alert>` for "note" callout boxes
- [ ] Adopt `<Divider>` between doc sections
- [ ] Adopt `<Divider>` between sidebar nav groups
- [ ] Adopt `<EmptyState>` for empty search results
- [ ] Adopt `<EmptyState>` for empty forum boards
- [ ] Adopt `<EmptyState>` for no matching API endpoints
- [ ] Adopt `<Button>` for primary actions (CTA, submit feedback)
- [ ] Adopt `<Button>` for secondary actions (copy code, share)
- [ ] Adopt `<Button>` for ghost actions (expand/collapse)
- [ ] Adopt `<Input>` for search fields
- [ ] Adopt `<Input>` for feedback text areas
- [ ] Adopt `<Avatar>` for forum user avatars
- [ ] Adopt `<Tooltip>` for icon-only buttons
- [ ] Adopt `<Modal>` for search overlay (Cmd+K)
- [ ] Adopt `<Modal>` for feedback submission confirmation
- [ ] Adopt `<Skeleton>` for page loading states
- [ ] Adopt `<Spinner>` for in-progress states (search loading)
- [ ] Adopt `<Toast>` for success messages (code copied, feedback sent)
- [ ] Adopt `<Breadcrumb>` orbit-ui component if available
- [ ] Adopt `<Select>` for version selector dropdown
- [ ] Adopt `<Dropdown>` for settings menu
- [ ] Adopt `<Card>` for feature/category grid cards
- [ ] Adopt `<Accordion>` for FAQ sections
- [ ] Adopt `<Pagination>` for forum and search results

### 2.3 Custom Scrollbar
- [ ] Replace browser default scrollbar with `.scrollbar-thin` plugin
- [ ] Custom scrollbar on sidebar navigation
- [ ] Custom scrollbar on code blocks
- [ ] Custom scrollbar on TOC sidebar
- [ ] Custom scrollbar on search results dropdown
- [ ] Custom scrollbar on mobile sidebar drawer

### 2.4 Typography System
- [ ] `font-display` applied to headings
- [ ] `font-body` applied to body text
- [ ] `font-mono` applied to code blocks and inline code
- [ ] Consistent heading scale: h1=4xl, h2=2xl, h3=xl, h4=lg
- [ ] Consistent paragraph spacing: `mb-4` or `mb-6`
- [ ] Line height: body text `leading-relaxed`, headings `leading-tight`
- [ ] Letter spacing: headings `tracking-tight`
- [ ] Max prose width: content constrained to `max-w-3xl` or `max-w-prose`

---

## 3. Dark Mode

### 3.1 Layout Shell
- [ ] Header background: dark mode `bg-surface-base/80` -- verified working
- [ ] Header border: dark mode `border-border-subtle` -- verified
- [ ] Header logo text: dark mode `text-content-primary`
- [ ] Header nav links: dark mode hover states
- [ ] Header search input: dark mode `bg-surface-muted`
- [ ] Header search placeholder: dark mode text color
- [ ] Header Cmd+K badge: dark mode background
- [ ] Header login/signup buttons: dark mode contrast
- [ ] Header divider: dark mode `bg-border-default`

### 3.2 Sidebar Navigation
- [ ] Sidebar background: dark mode full coverage
- [ ] Sidebar section headers: dark mode `text-content-muted`
- [ ] Sidebar nav links: dark mode default state
- [ ] Sidebar nav links: dark mode hover state `hover:bg-surface-muted`
- [ ] Sidebar nav links: dark mode active state `bg-primary/10 text-primary`
- [ ] Sidebar nav link icons: dark mode color
- [ ] Sidebar version selector button: dark mode border and background
- [ ] Sidebar version selector dropdown: dark mode
- [ ] Sidebar scroll area: dark mode scrollbar styling
- [ ] Sidebar border-right: dark mode `border-border-subtle`
- [ ] Sidebar mobile overlay: dark mode backdrop
- [ ] Sidebar mobile close button: dark mode

### 3.3 Main Content Area
- [ ] Main content background: `dark:bg-surface-base`
- [ ] Breadcrumb trail: dark mode text colors
- [ ] Breadcrumb separator: dark mode color
- [ ] Breadcrumb active item: dark mode `text-content-primary`
- [ ] Page title (h1): dark mode `text-content-primary`
- [ ] Page subtitle/description: dark mode `text-content-secondary`
- [ ] Section headings (h2, h3, h4): dark mode
- [ ] Body paragraph text: dark mode
- [ ] Inline code: dark mode `bg-surface-muted text-content-primary`
- [ ] Blockquotes: dark mode border and background
- [ ] Horizontal rules: dark mode
- [ ] Ordered and unordered lists: dark mode
- [ ] Link text: dark mode `text-primary hover:text-primary-400`
- [ ] Tables: dark mode header, rows, alternating rows, borders
- [ ] Images: dark mode border or shadow
- [ ] Callout boxes (info): dark mode `bg-blue-900/20 border-blue-800`
- [ ] Callout boxes (warning): dark mode `bg-amber-900/20 border-amber-800`
- [ ] Callout boxes (danger): dark mode `bg-red-900/20 border-red-800`
- [ ] Callout boxes (tip): dark mode `bg-green-900/20 border-green-800`
- [ ] Callout boxes (note): dark mode `bg-surface-muted border-border-default`

### 3.4 Code Blocks
- [ ] Code block container: dark mode `bg-neutral-900` (confirmed in Quickstart)
- [ ] Code block filename bar: dark mode border and text
- [ ] Code block syntax highlighting: dark theme (e.g., One Dark, Tokyo Night)
- [ ] Code block copy button: dark mode hover state
- [ ] Code block copy button: dark mode tooltip
- [ ] Code block line numbers: dark mode
- [ ] Code block highlighted lines: dark mode accent
- [ ] Code block language badge: dark mode
- [ ] Code block diff highlighting: dark mode (added/removed lines)
- [ ] Code block terminal/bash prompt: dark mode
- [ ] Inline code spans: dark mode `bg-surface-muted`

### 3.5 API Reference Page
- [ ] API group headers: dark mode
- [ ] API group description: dark mode
- [ ] API group base URL: dark mode mono text
- [ ] Endpoint row: dark mode hover `hover:bg-surface-muted`
- [ ] Endpoint method badge: dark mode variants for GET/POST/PUT/PATCH/DELETE
- [ ] Endpoint path: dark mode mono text
- [ ] Endpoint summary: dark mode muted text
- [ ] Endpoint auth lock icon: dark mode
- [ ] Endpoint expand/collapse chevron: dark mode
- [ ] Endpoint detail panel: dark mode `bg-surface-muted/30`
- [ ] Endpoint detail panel border: dark mode
- [ ] Query parameters table: dark mode
- [ ] Request body parameters table: dark mode
- [ ] Response code block: dark mode
- [ ] Response copy button: dark mode
- [ ] Auth notice banner: dark mode `bg-blue-900/20 border-blue-800`
- [ ] Search endpoints input: dark mode
- [ ] No results message: dark mode

### 3.6 Home Page
- [ ] Hero title: dark mode `text-content-primary`
- [ ] Hero description: dark mode `text-content-secondary`
- [ ] Hero AI search input: dark mode background, border, placeholder
- [ ] Hero search submit button: dark mode
- [ ] Category grid cards: dark mode background, border, shadow
- [ ] Category card icons (colored backgrounds): dark mode variants
- [ ] Category card title: dark mode
- [ ] Category card description: dark mode
- [ ] Category card CTA link: dark mode
- [ ] Popular topics section title: dark mode
- [ ] Popular topic links: dark mode background, border, text, hover
- [ ] Popular topic chevron icon: dark mode

### 3.7 Quickstart Page
- [ ] Breadcrumb: dark mode (verified partially in code)
- [ ] Getting Started badge: dark mode `bg-primary/10`
- [ ] Read time indicator: dark mode
- [ ] Step number circles: dark mode `bg-primary text-white`
- [ ] Step connector line: dark mode `bg-border-default`
- [ ] Step title: dark mode
- [ ] Step description text: dark mode
- [ ] Prerequisites card: dark mode border and background
- [ ] Prerequisite checkmarks: dark mode
- [ ] Success/done card: dark mode `bg-success-900/20 border-success-800`
- [ ] Previous/Next navigation: dark mode border and text

### 3.8 Search Overlay
- [ ] Search overlay backdrop: dark mode `bg-black/60`
- [ ] Search modal container: dark mode `bg-surface-base border-border-subtle`
- [ ] Search input field: dark mode
- [ ] Search results list: dark mode
- [ ] Search result item: dark mode hover state
- [ ] Search result title: dark mode
- [ ] Search result snippet: dark mode
- [ ] Search result keyword highlight: dark mode
- [ ] Search result breadcrumb/path: dark mode
- [ ] Recent searches section: dark mode
- [ ] No results state: dark mode
- [ ] Search keyboard shortcut hints: dark mode

### 3.9 TOC (Table of Contents) Sidebar
- [ ] TOC container background: dark mode
- [ ] TOC heading: dark mode
- [ ] TOC link items: dark mode default
- [ ] TOC link items: dark mode hover
- [ ] TOC link items: dark mode active (current section)
- [ ] TOC active indicator bar: dark mode
- [ ] TOC scroll tracking: dark mode

### 3.10 Footer
- [ ] Footer background: dark mode (verified `dark:bg-neutral-900`)
- [ ] Footer border-top: dark mode `border-border-subtle`
- [ ] Footer logo/brand text: dark mode
- [ ] Footer copyright text: dark mode
- [ ] Footer links (Privacy, Terms, Twitter, GitHub): dark mode hover
- [ ] Footer social icons: dark mode

### 3.11 Miscellaneous Components
- [ ] Feedback widget: dark mode
- [ ] Version selector dropdown: dark mode
- [ ] "Edit this page" link: dark mode
- [ ] External link indicator icon: dark mode
- [ ] Link hover preview popover: dark mode
- [ ] Loading spinner: dark mode
- [ ] Skeleton loaders: dark mode
- [ ] Toast notifications: dark mode
- [ ] Error boundary fallback: dark mode
- [ ] Offline banner: dark mode `bg-danger-500` (confirmed)
- [ ] 404 page: dark mode
- [ ] Scroll-to-top button: dark mode

---

## 4. Core Features

### 4.1 Documentation Structure -- Getting Started

#### 4.1.1 Getting Started Guide
- [ ] Getting Started guide: complete end-to-end setup walkthrough
- [ ] Getting Started: system requirements section
- [ ] Getting Started: prerequisites checklist (Node, Docker, Git)
- [ ] Getting Started: clone repository step
- [ ] Getting Started: install dependencies step
- [ ] Getting Started: environment variable configuration
- [ ] Getting Started: start backend services (Docker Compose)
- [ ] Getting Started: build shared orbit-ui library
- [ ] Getting Started: launch first app step
- [ ] Getting Started: verify installation step
- [ ] Getting Started: troubleshooting common issues section
- [ ] Getting Started: next steps / where to go from here

#### 4.1.2 Quick Start Page (existing)
- [x] Quick Start page component (`Quickstart.tsx`)
- [x] Quick Start: breadcrumb navigation
- [x] Quick Start: "Getting Started" badge label
- [x] Quick Start: reading time indicator
- [x] Quick Start: hero title and description
- [x] Quick Start: prerequisites card with checkmarks
- [x] Quick Start: Step 1 -- Clone repository with code block
- [x] Quick Start: Step 2 -- Install dependencies with code block
- [x] Quick Start: Step 3 -- Configure env variables with code block
- [x] Quick Start: Step 4 -- Docker compose up
- [x] Quick Start: Step 5 -- Build orbit-ui
- [x] Quick Start: Step 6 -- Launch app
- [x] Quick Start: success/done card
- [x] Quick Start: previous/next navigation links
- [x] Quick Start: CodeBlock component with copy-to-clipboard
- [x] Quick Start: Step component with numbered circles and connectors
- [ ] Quick Start: syntax highlighting in code blocks (currently plain text)
- [ ] Quick Start: multiple language tabs in code blocks (npm/yarn/pnpm)
- [ ] Quick Start: interactive code playground (optional)
- [ ] Quick Start: video walkthrough embed

#### 4.1.3 Installation Guide
- [ ] Installation page: dedicated route `/docs/install`
- [ ] Installation: macOS setup instructions
- [ ] Installation: Windows setup instructions (WSL2)
- [ ] Installation: Linux (Ubuntu/Debian) setup instructions
- [ ] Installation: Docker Desktop setup
- [ ] Installation: Node.js version manager (nvm) setup
- [ ] Installation: IDE setup (VS Code with recommended extensions)
- [ ] Installation: Git configuration
- [ ] Installation: SSH key setup for repository access
- [ ] Installation: troubleshooting section

#### 4.1.4 Architecture Overview
- [ ] Architecture page: dedicated route `/docs/architecture`
- [ ] Architecture: high-level system diagram (all 16 apps)
- [ ] Architecture: microservices communication patterns
- [ ] Architecture: Gate as central auth service diagram
- [ ] Architecture: EventBus real-time architecture
- [ ] Architecture: database per service strategy
- [ ] Architecture: shared orbit-ui component library architecture
- [ ] Architecture: monorepo structure explanation
- [ ] Architecture: frontend-backend communication (REST + WebSocket)
- [ ] Architecture: deployment topology diagram
- [ ] Architecture: data flow diagrams
- [ ] Architecture: technology stack overview table
- [ ] Architecture: port allocation table (all 16 apps)

#### 4.1.5 Authentication Guide
- [ ] Auth guide: dedicated route `/docs/security` or `/docs/authentication`
- [ ] Auth guide: Gate OAuth2 PKCE flow explanation with diagram
- [ ] Auth guide: step-by-step PKCE integration code example
- [ ] Auth guide: token lifecycle (access, refresh, ID tokens)
- [ ] Auth guide: JWT structure and claims documentation
- [ ] Auth guide: JWKS verification example
- [ ] Auth guide: session management explanation
- [ ] Auth guide: MFA integration guide
- [ ] Auth guide: social SSO setup (Google, GitHub, Microsoft)
- [ ] Auth guide: SAML 2.0 integration
- [ ] Auth guide: SCIM provisioning guide
- [ ] Auth guide: API key authentication for service accounts
- [ ] Auth guide: webhook events for auth state changes
- [ ] Auth guide: error handling and token refresh flow
- [ ] Auth guide: security best practices

#### 4.1.6 API Reference (existing)
- [x] API Reference page component (`ApiReference.tsx`)
- [x] API Reference: breadcrumb
- [x] API Reference: "Reference" badge label
- [x] API Reference: hero title and description
- [x] API Reference: auth notice banner (Bearer token)
- [x] API Reference: search/filter input for endpoints
- [x] API Reference: Gate (AuthX) API group with endpoints
- [x] API Reference: Atlas API group with endpoints
- [x] API Reference: Capital Hub API group with endpoints
- [x] API Reference: endpoint expand/collapse interaction
- [x] API Reference: HTTP method color-coded badges
- [x] API Reference: auth lock icon for protected endpoints
- [x] API Reference: query parameters section per endpoint
- [x] API Reference: request body section per endpoint
- [x] API Reference: response preview section per endpoint
- [x] API Reference: copy button on response code blocks
- [x] API Reference: "No endpoints match" empty state
- [ ] API Reference: Mail API group
- [ ] API Reference: Connect API group
- [ ] API Reference: Meet API group
- [ ] API Reference: Calendar API group
- [ ] API Reference: Writer API group
- [ ] API Reference: Planet (CRM) API group
- [ ] API Reference: Secure API group
- [ ] API Reference: Control Center API group
- [ ] API Reference: TurboTick API group
- [ ] API Reference: Dock API group
- [ ] API Reference: Wallet API group
- [ ] API Reference: FitterMe API group
- [ ] API Reference: Learn API group (search, feedback)
- [ ] API Reference: EventBus API group
- [ ] API Reference: auto-generated from OpenAPI specs
- [ ] API Reference: "Try it" interactive request builder
- [ ] API Reference: response status code tabs (200, 400, 401, 403, 404, 500)
- [ ] API Reference: request/response headers documentation
- [ ] API Reference: rate limit documentation per endpoint
- [ ] API Reference: pagination documentation
- [ ] API Reference: error response format documentation
- [ ] API Reference: webhook events documentation
- [ ] API Reference: SDK code generation links
- [ ] API Reference: download OpenAPI spec button

#### 4.1.7 Design System Guide
- [ ] Design system guide: dedicated route `/docs/design-system`
- [ ] Design system: orbit-tokens overview (colors, typography, radius, shadows)
- [ ] Design system: tailwind preset usage
- [ ] Design system: CSS custom properties reference
- [ ] Design system: color palette visualization
- [ ] Design system: typography scale visualization
- [ ] Design system: spacing scale visualization
- [ ] Design system: shadow scale visualization
- [ ] Design system: border-radius scale visualization
- [ ] Design system: z-index layer documentation
- [ ] Design system: motion/animation tokens
- [ ] Design system: dark mode implementation guide
- [ ] Design system: anti-FOUC setup instructions

#### 4.1.8 Component Reference
- [ ] Component reference: dedicated route `/docs/components`
- [ ] Component reference: all `@orbit-ui/react` components listed
- [ ] Component reference: per-component props table
- [ ] Component reference: per-component live preview
- [ ] Component reference: per-component code example
- [ ] Component reference: per-component accessibility notes
- [ ] Component reference: Button variants (primary, secondary, ghost, danger)
- [ ] Component reference: Input variants (text, password, search, textarea)
- [ ] Component reference: Badge variants (default, info, success, warning, danger)
- [ ] Component reference: Alert variants
- [ ] Component reference: Tabs component
- [ ] Component reference: Modal component
- [ ] Component reference: Tooltip component
- [ ] Component reference: Avatar component
- [ ] Component reference: Card component
- [ ] Component reference: Select component
- [ ] Component reference: Dropdown component
- [ ] Component reference: Accordion component
- [ ] Component reference: Pagination component
- [ ] Component reference: Skeleton component
- [ ] Component reference: Spinner component
- [ ] Component reference: Toast component
- [ ] Component reference: ThemeToggle component
- [ ] Component reference: ThemeProvider component
- [ ] Component reference: EmptyState component
- [ ] Component reference: Divider component

#### 4.1.9 Deployment Guide
- [ ] Deployment guide: dedicated route `/docs/deployment`
- [ ] Deployment: Docker production setup
- [ ] Deployment: Docker Compose production config
- [ ] Deployment: Kubernetes deployment manifests
- [ ] Deployment: Helm chart documentation
- [ ] Deployment: environment variable reference (all apps)
- [ ] Deployment: database migration process
- [ ] Deployment: Redis configuration
- [ ] Deployment: Nginx/reverse proxy configuration
- [ ] Deployment: TLS/SSL certificate setup
- [ ] Deployment: domain/DNS configuration
- [ ] Deployment: health check endpoints reference
- [ ] Deployment: monitoring setup (Prometheus + Grafana)
- [ ] Deployment: logging configuration (structured JSON)
- [ ] Deployment: backup and disaster recovery
- [ ] Deployment: scaling strategy (horizontal/vertical)
- [ ] Deployment: CI/CD pipeline setup
- [ ] Deployment: production checklist (security, performance, monitoring)
- [ ] Deployment: rollback procedures

#### 4.1.10 Changelog / Release Notes
- [ ] Changelog page: dedicated route `/changelog`
- [ ] Changelog: versioned entries (newest first)
- [ ] Changelog: per-version sections (Added, Changed, Fixed, Removed, Deprecated)
- [ ] Changelog: date stamps on each version
- [ ] Changelog: links to related pull requests / commits
- [ ] Changelog: breaking changes highlighted
- [ ] Changelog: migration guides for breaking changes
- [ ] Changelog: semantic versioning explanation
- [ ] Changelog: subscribe to release notes via email (form)
- [ ] Changelog: RSS feed for release notes
- [ ] Changelog: version badge/tag components
- [ ] Changelog: filter by type (feature, bugfix, breaking)
- [ ] Changelog: search within changelog

### 4.2 Search

#### 4.2.1 Search UI
- [ ] Search input in header (existing basic input)
- [ ] Search: `Cmd+K` / `Ctrl+K` keyboard shortcut opens search overlay
- [ ] Search: modal overlay with large search input
- [ ] Search: autofocus on search input when opened
- [ ] Search: `Escape` closes search overlay
- [ ] Search: click outside closes search overlay
- [ ] Search: debounced input (300ms)
- [ ] Search: loading spinner while searching
- [ ] Search: results list with title, snippet, breadcrumb path
- [ ] Search: keyword highlight in result snippets
- [ ] Search: keyboard navigation (arrow up/down to select, Enter to open)
- [ ] Search: result grouping by section (Guides, API, Components, Changelog)
- [ ] Search: result count displayed
- [ ] Search: relevance ranking
- [ ] Search: recent searches stored in localStorage
- [ ] Search: recent searches displayed when input is empty
- [ ] Search: clear recent searches button
- [ ] Search: "No results" state with suggestions
- [ ] Search: "No results" state with alternative search tips
- [ ] Search: search result snippet truncation with ellipsis
- [ ] Search: mobile-optimized search overlay (full screen)
- [ ] Search: search analytics (log search queries)
- [ ] Search: typo tolerance / fuzzy matching
- [ ] Search: search filters (by section, by version, by date)
- [ ] Search: shortcut hint displayed in search input (`Cmd+K`)

#### 4.2.2 AI-Powered Search / Q&A
- [ ] AI search: toggle between classic search and AI Q&A mode
- [ ] AI search: natural language question input
- [ ] AI search: streaming response display
- [ ] AI search: source citations with links to doc pages
- [ ] AI search: follow-up question support
- [ ] AI search: conversation history within session
- [ ] AI search: "Ask AI" button in hero search (existing placeholder)
- [ ] AI search: loading animation (typing indicator)
- [ ] AI search: rate limiting (queries per minute per user)
- [ ] AI search: error state (service unavailable)
- [ ] AI search: feedback on AI response (helpful/not helpful)
- [ ] AI search: contextual awareness (knows current page)

### 4.3 Navigation

#### 4.3.1 Sidebar Navigation
- [x] Sidebar: persistent left sidebar on desktop
- [x] Sidebar: links to Home, Quick Start, Installation
- [x] Sidebar: links to Architecture, Security, Data Models
- [x] Sidebar: links to REST API, CLI Commands, Release Notes
- [x] Sidebar: section headers ("Getting Started", "Core Concepts", "Reference")
- [x] Sidebar: icons for each nav item (lucide-react icons)
- [x] Sidebar: active page highlight `bg-primary/10 text-primary`
- [x] Sidebar: hover state on nav items
- [x] Sidebar: version selector button (v2.4.0)
- [ ] Sidebar: nested sections with expand/collapse
- [ ] Sidebar: expand/collapse state persisted across navigation
- [ ] Sidebar: expand/collapse animation (smooth height transition)
- [ ] Sidebar: indent level for nested items
- [ ] Sidebar: collapse all / expand all button
- [ ] Sidebar: scroll position preserved on navigation
- [ ] Sidebar: current section auto-expanded on page load
- [ ] Sidebar: keyboard navigation (Tab, Enter, ArrowUp, ArrowDown)
- [ ] Sidebar: search within sidebar (filter nav items)
- [ ] Sidebar: resize handle (adjustable width)
- [ ] Sidebar: "New" badge on recently added docs
- [ ] Sidebar: "Updated" badge on recently modified docs

#### 4.3.2 TOC (Table of Contents) -- Right Sidebar
- [ ] TOC: auto-generated from page headings (h2, h3)
- [ ] TOC: displayed on right side of content area
- [ ] TOC: scroll spy (highlight current section as user scrolls)
- [ ] TOC: smooth scroll to section on click
- [ ] TOC: nested indentation for h3 under h2
- [ ] TOC: sticky positioning (follows viewport)
- [ ] TOC: hidden on mobile (screen width < lg)
- [ ] TOC: collapsible on medium screens
- [ ] TOC: "On this page" heading
- [ ] TOC: active indicator bar/line
- [ ] TOC: intersection observer for scroll tracking
- [ ] TOC: handles dynamic content (updates when DOM changes)

#### 4.3.3 Breadcrumbs
- [x] Breadcrumbs: shown on Quick Start page
- [x] Breadcrumbs: shown on API Reference page
- [x] Breadcrumbs: Home link
- [x] Breadcrumbs: section name
- [x] Breadcrumbs: current page name (non-clickable)
- [x] Breadcrumbs: separator icon (ChevronRight)
- [ ] Breadcrumbs: shown on all documentation pages
- [ ] Breadcrumbs: auto-generated from route hierarchy
- [ ] Breadcrumbs: truncation for deep nesting (show first + last + ellipsis)
- [ ] Breadcrumbs: mobile-friendly (horizontal scroll or dropdown)
- [ ] Breadcrumbs: schema.org structured data (BreadcrumbList)
- [ ] Breadcrumbs: dark mode styling

#### 4.3.4 Previous / Next Navigation
- [x] Prev/Next: shown on Quick Start page (previous: Home, next: Installation Guide)
- [ ] Prev/Next: shown on all doc pages
- [ ] Prev/Next: auto-determined from sidebar order
- [ ] Prev/Next: display page title, not just direction arrow
- [ ] Prev/Next: hover preview of destination page
- [ ] Prev/Next: keyboard shortcut (Alt+Left, Alt+Right)
- [ ] Prev/Next: border-top separator
- [ ] Prev/Next: dark mode styling
- [ ] Prev/Next: loading state while navigating

#### 4.3.5 Header Navigation
- [x] Header: Guides link
- [x] Header: API Reference link
- [x] Header: Community link
- [x] Header: Changelog link
- [ ] Header: active link indicator (underline or color)
- [ ] Header: dropdown menus for nested sections
- [ ] Header: notification bell (new docs, announcements)
- [ ] Header: user avatar/profile menu (when logged in)
- [ ] Header: mobile nav: hidden on small screens
- [ ] Header: mobile: hamburger opens mobile sidebar

### 4.4 Content Features

#### 4.4.1 Markdown Rendering
- [ ] Markdown renderer: library chosen (react-markdown, MDX, or similar)
- [ ] Markdown: heading rendering (h1-h6) with anchor IDs
- [ ] Markdown: paragraph rendering
- [ ] Markdown: bold and italic text
- [ ] Markdown: strikethrough text
- [ ] Markdown: ordered lists
- [ ] Markdown: unordered lists
- [ ] Markdown: nested lists
- [ ] Markdown: task lists (checkboxes)
- [ ] Markdown: blockquotes
- [ ] Markdown: horizontal rules
- [ ] Markdown: links (internal and external)
- [ ] Markdown: images with alt text
- [ ] Markdown: image captions
- [ ] Markdown: image zoom on click
- [ ] Markdown: tables with header and alignment
- [ ] Markdown: table responsive scrolling
- [ ] Markdown: inline code
- [ ] Markdown: fenced code blocks
- [ ] Markdown: footnotes
- [ ] Markdown: definition lists
- [ ] Markdown: abbreviations
- [ ] Markdown: emoji support (:rocket:)
- [ ] Markdown: HTML passthrough (limited, sanitized)
- [ ] Markdown: math/KaTeX rendering
- [ ] Markdown: Mermaid diagram rendering
- [ ] Markdown: custom containers (:::info, :::warning, :::tip)
- [ ] Markdown: GFM (GitHub Flavored Markdown) support
- [ ] Markdown: heading links (click to copy anchor URL)

#### 4.4.2 Code Blocks
- [x] Code blocks: container with dark background
- [x] Code blocks: filename header bar
- [x] Code blocks: language indicator
- [x] Code blocks: copy-to-clipboard button
- [x] Code blocks: copy success state (check icon, 2s timeout)
- [x] Code blocks: horizontal scroll for long lines
- [x] Code blocks: monospace font
- [ ] Code blocks: syntax highlighting (Prism.js or Shiki)
- [ ] Code blocks: syntax highlighting themes (light + dark)
- [ ] Code blocks: language detection from fence info string
- [ ] Code blocks: supported languages: JavaScript/TypeScript
- [ ] Code blocks: supported languages: Python
- [ ] Code blocks: supported languages: Bash/Shell
- [ ] Code blocks: supported languages: JSON
- [ ] Code blocks: supported languages: YAML
- [ ] Code blocks: supported languages: SQL
- [ ] Code blocks: supported languages: HTML/CSS
- [ ] Code blocks: supported languages: Docker/Dockerfile
- [ ] Code blocks: supported languages: Markdown
- [ ] Code blocks: supported languages: Go
- [ ] Code blocks: supported languages: Rust
- [ ] Code blocks: supported languages: env files
- [ ] Code blocks: supported languages: GraphQL
- [ ] Code blocks: supported languages: diff
- [ ] Code blocks: line numbers (optional toggle)
- [ ] Code blocks: line highlighting (specific lines emphasized)
- [ ] Code blocks: line range display (show lines 5-15 of file)
- [ ] Code blocks: word wrap toggle
- [ ] Code blocks: multi-tab code blocks (show same example in multiple languages)
- [ ] Code blocks: diff view (added/removed lines with +/- indicators)
- [ ] Code blocks: collapsible long code blocks (show first N lines)
- [ ] Code blocks: "Open in playground" link
- [ ] Code blocks: terminal/shell output styling
- [ ] Code blocks: prompt indicator ($ for bash, >>> for Python)

#### 4.4.3 Version Selector
- [x] Version selector: button in sidebar showing current version (v2.4.0)
- [ ] Version selector: dropdown with available versions
- [ ] Version selector: version list from backend API
- [ ] Version selector: URL changes on version switch (/v2.3/docs/quickstart)
- [ ] Version selector: "Latest" indicator on current version
- [ ] Version selector: deprecated version warning banner
- [ ] Version selector: version comparison diff view
- [ ] Version selector: persist selected version in localStorage
- [ ] Version selector: deep link with version in URL

#### 4.4.4 "Edit This Page" Link
- [ ] Edit link: "Edit this page on GitHub" button at bottom of each page
- [ ] Edit link: opens correct file in GitHub repository
- [ ] Edit link: correct branch (main or docs branch)
- [ ] Edit link: pencil icon
- [ ] Edit link: configurable repo URL via env variable
- [ ] Edit link: hidden for auto-generated pages (API reference)

#### 4.4.5 Feedback Widget
- [ ] Feedback: "Was this page helpful?" at bottom of each page
- [ ] Feedback: thumbs up / thumbs down buttons
- [ ] Feedback: optional text comment field (appears after thumbs down)
- [ ] Feedback: submit button
- [ ] Feedback: success confirmation ("Thanks for your feedback!")
- [ ] Feedback: one submission per page per session (prevent spam)
- [ ] Feedback: data sent to backend API
- [ ] Feedback: loading state during submission
- [ ] Feedback: error state with retry
- [ ] Feedback: analytics dashboard for team to review feedback
- [ ] Feedback: dark mode styling

#### 4.4.6 External Link Indicators
- [ ] External links: arrow/external icon appended to links pointing outside docs
- [ ] External links: `target="_blank"` and `rel="noopener noreferrer"`
- [ ] External links: visual distinction from internal links
- [ ] External links: tooltip showing destination domain

#### 4.4.7 Internal Link Hover Preview
- [ ] Link preview: popover on hover showing destination page title + excerpt
- [ ] Link preview: delay before showing (200ms)
- [ ] Link preview: dismiss on mouse leave
- [ ] Link preview: loading state
- [ ] Link preview: prefetch destination page on hover
- [ ] Link preview: dark mode styling

### 4.5 Community & Feedback

#### 4.5.1 Forum / Discussion Boards
- [ ] Forum: dedicated route `/community`
- [ ] Forum: board/category list (General, Bug Reports, Feature Requests, Show & Tell)
- [ ] Forum: thread list per board (title, author, reply count, last activity)
- [ ] Forum: create new thread (title, body with markdown, category)
- [ ] Forum: thread detail view with replies
- [ ] Forum: threaded/nested replies (at least 2 levels)
- [ ] Forum: reply to thread (markdown editor)
- [ ] Forum: edit own post/reply
- [ ] Forum: delete own post/reply
- [ ] Forum: upvote/downvote on posts and replies
- [ ] Forum: sort threads (newest, most active, most upvoted)
- [ ] Forum: search within forum
- [ ] Forum: filter by category
- [ ] Forum: filter by status (open, resolved, closed)
- [ ] Forum: user avatar and display name
- [ ] Forum: user profile link
- [ ] Forum: time-ago timestamps
- [ ] Forum: rich text preview in thread list
- [ ] Forum: pagination for thread list
- [ ] Forum: pagination for replies
- [ ] Forum: loading states
- [ ] Forum: empty states
- [ ] Forum: error states
- [ ] Forum: Gate auth required to post
- [ ] Forum: read-only for unauthenticated users

#### 4.5.2 Forum Moderation
- [ ] Moderation: pin thread to top
- [ ] Moderation: lock thread (no new replies)
- [ ] Moderation: close thread (mark as resolved)
- [ ] Moderation: delete thread
- [ ] Moderation: delete reply
- [ ] Moderation: edit any post (admin)
- [ ] Moderation: ban user from forum
- [ ] Moderation: report post (flag for review)
- [ ] Moderation: moderation queue for flagged posts
- [ ] Moderation: role-based access (admin, moderator, member)

### 4.6 Offline Support
- [x] Offline: network status detection (`navigator.onLine`)
- [x] Offline: offline banner displayed when connection lost
- [x] Offline: banner auto-dismisses when connection restored
- [ ] Offline: service worker for caching static assets
- [ ] Offline: cached pages available offline
- [ ] Offline: offline indicator in sidebar/header
- [ ] Offline: queue search queries for when back online
- [ ] Offline: graceful degradation (hide features requiring network)

---

## 5. API Integration

### 5.1 HTTP Client Setup
- [ ] Axios instance created with base URL from env
- [ ] Axios request interceptor: attach Bearer token
- [ ] Axios response interceptor: handle 401 (redirect to login)
- [ ] Axios response interceptor: handle 403 (show forbidden message)
- [ ] Axios response interceptor: handle 429 (rate limit with retry-after)
- [ ] Axios response interceptor: handle 500 (generic error)
- [ ] Axios timeout configuration (30s default)
- [ ] Axios request/response logging in development
- [ ] API error types defined (ApiError, ValidationError)
- [ ] API response wrapper type (ApiResponse<T>)

### 5.2 Auth Integration (Gate)
- [ ] OAuth2 PKCE flow: authorization URL construction
- [ ] OAuth2 PKCE flow: code verifier/challenge generation
- [ ] OAuth2 PKCE flow: authorization code exchange
- [ ] Token storage: access token in memory (not localStorage)
- [ ] Token storage: refresh token in httpOnly cookie (via Gate)
- [ ] Token refresh: automatic refresh before expiry
- [ ] Token refresh: retry failed requests after refresh
- [ ] Logout: token revocation API call
- [ ] Logout: clear local state
- [ ] Auth callback page: `/auth/callback`
- [ ] Auth guard: protect routes requiring authentication (forum, feedback)
- [ ] Auth state: loading, authenticated, unauthenticated
- [ ] User profile: fetch from Gate `/api/v1/oidc/userinfo`

### 5.3 Search API
- [ ] Search: `GET /api/search?q=<query>&version=<version>&section=<section>`
- [ ] Search: response type definition
- [ ] Search: debounced requests
- [ ] Search: abort previous request on new query
- [ ] Search: cache recent search results
- [ ] Search: error handling

### 5.4 Feedback API
- [ ] Feedback: `POST /api/feedback` with page URL, rating, comment
- [ ] Feedback: response handling
- [ ] Feedback: error handling

### 5.5 Forum API
- [ ] Forum: `GET /api/forum/boards` -- list boards
- [ ] Forum: `GET /api/forum/boards/:id/threads` -- list threads
- [ ] Forum: `POST /api/forum/threads` -- create thread
- [ ] Forum: `GET /api/forum/threads/:id` -- get thread with replies
- [ ] Forum: `POST /api/forum/threads/:id/replies` -- reply to thread
- [ ] Forum: `PUT /api/forum/threads/:id` -- edit thread
- [ ] Forum: `DELETE /api/forum/threads/:id` -- delete thread
- [ ] Forum: `POST /api/forum/posts/:id/vote` -- upvote/downvote
- [ ] Forum: `POST /api/forum/posts/:id/report` -- report post

### 5.6 Analytics API
- [ ] Analytics: page view tracking on route change
- [ ] Analytics: search query logging
- [ ] Analytics: feedback event logging
- [ ] Analytics: time on page tracking
- [ ] Analytics: scroll depth tracking

---

## 6. State Management

### 6.1 Zustand Stores
- [ ] `useThemeStore` -- dark/light mode preference (may use orbit-ui ThemeProvider)
- [ ] `useAuthStore` -- authentication state (user, tokens, isAuthenticated)
- [ ] `useSearchStore` -- search query, results, recent searches, loading state
- [ ] `useSidebarStore` -- sidebar open/close, expand/collapse state per section
- [ ] `useVersionStore` -- selected docs version
- [ ] `useTocStore` -- current active heading ID (scroll spy)
- [ ] `useFeedbackStore` -- feedback submission state per page
- [ ] `useForumStore` -- forum threads, replies, pagination state
- [ ] `usePreferencesStore` -- user preferences (font size, code theme)

### 6.2 State Persistence
- [ ] Theme preference persisted to localStorage
- [ ] Sidebar state persisted to localStorage
- [ ] Selected version persisted to localStorage
- [ ] Recent searches persisted to localStorage
- [ ] User preferences persisted to localStorage
- [ ] Auth tokens handled securely (memory only)

### 6.3 State Hydration
- [ ] Theme hydrated from localStorage before first paint (anti-FOUC)
- [ ] Sidebar state hydrated on mount
- [ ] Version hydrated from URL or localStorage
- [ ] Auth state hydrated from token/session check on mount

---

## 7. Performance

### 7.1 Code Splitting & Lazy Loading
- [x] Route-based code splitting with `React.lazy()` (Home, Quickstart, ApiReference)
- [x] Suspense fallback with loading spinner
- [ ] Lazy load: all documentation pages (Architecture, Security, Data Models, etc.)
- [ ] Lazy load: forum pages
- [ ] Lazy load: changelog page
- [ ] Lazy load: search modal component
- [ ] Lazy load: markdown renderer
- [ ] Lazy load: syntax highlighting library
- [ ] Lazy load: Mermaid diagram renderer
- [ ] Prefetch: next/previous page on hover

### 7.2 Bundle Optimization
- [ ] Bundle size analysis performed (rollup-plugin-visualizer)
- [ ] Total initial bundle < 200KB gzipped
- [ ] Tree-shaking verified for lucide-react icons
- [ ] Tree-shaking verified for orbit-ui components
- [ ] No duplicate React instances in bundle
- [ ] Dynamic imports for heavy libraries (syntax highlighter, markdown parser)
- [ ] Image optimization: WebP format with fallbacks
- [ ] Image optimization: responsive srcset
- [ ] Image optimization: lazy loading (`loading="lazy"`)
- [ ] Font optimization: WOFF2 format
- [ ] Font optimization: font-display: swap
- [ ] Font optimization: preload critical fonts
- [ ] CSS: purge unused styles (Tailwind purge)
- [ ] CSS: minification in production

### 7.3 Caching
- [ ] Service worker: cache static assets (SW)
- [ ] Service worker: cache documentation content
- [ ] Service worker: stale-while-revalidate strategy
- [ ] HTTP caching headers: immutable for hashed assets
- [ ] HTTP caching headers: stale-while-revalidate for HTML
- [ ] API response caching: search results (in-memory, 5 min TTL)
- [ ] API response caching: documentation content (in-memory, 10 min TTL)

### 7.4 Core Web Vitals
- [ ] First Contentful Paint (FCP) < 1.5s
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] First Input Delay (FID) < 100ms
- [ ] Cumulative Layout Shift (CLS) < 0.1
- [ ] Interaction to Next Paint (INP) < 200ms
- [ ] Time to First Byte (TTFB) < 800ms
- [ ] Total Blocking Time (TBT) < 300ms
- [ ] Performance budget defined and enforced in CI

### 7.5 Rendering Performance
- [ ] Virtual scrolling for long lists (forum threads, search results)
- [ ] `React.memo` on heavy components (code blocks, markdown sections)
- [ ] `useMemo` for expensive computations (search filtering, TOC generation)
- [ ] `useCallback` for event handlers passed to child components
- [ ] Intersection Observer for lazy rendering (below-fold content)
- [ ] Debounced scroll handlers (TOC scroll spy)
- [ ] No unnecessary re-renders (React DevTools Profiler verified)

---

## 8. Accessibility

### 8.1 Semantic HTML
- [ ] Pages use `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>` landmarks
- [x] Layout uses semantic `<header>` for top bar
- [x] Layout uses semantic `<aside>` for sidebar
- [x] Layout uses semantic `<main>` for content
- [x] Layout uses semantic `<footer>` for footer
- [ ] Headings follow correct hierarchy (no skipped levels)
- [ ] Lists use `<ul>`, `<ol>`, `<li>` correctly
- [ ] Tables use `<thead>`, `<tbody>`, `<th>` with `scope`
- [ ] Code blocks use `<pre>` and `<code>`
- [ ] Navigation uses `<nav>` with `aria-label`

### 8.2 ARIA Attributes
- [x] Sidebar toggle: `aria-expanded` state (in endpoint items)
- [ ] Sidebar: `aria-label="Documentation navigation"`
- [ ] TOC: `aria-label="Table of contents"`
- [ ] Search input: `aria-label="Search documentation"`
- [ ] Search overlay: `role="dialog"` with `aria-modal="true"`
- [ ] Search results: `role="listbox"` with `aria-activedescendant`
- [ ] Code block copy button: `aria-label="Copy code"` (confirmed)
- [ ] Version selector: `aria-haspopup="listbox"`
- [ ] Breadcrumb: `aria-label="Breadcrumb"` with `aria-current="page"`
- [ ] Loading spinner: `aria-live="polite"` with `aria-label="Loading"`
- [ ] Toast notifications: `aria-live="assertive"`
- [ ] Expandable sections: `aria-expanded` attribute
- [ ] Tabs: `role="tablist"`, `role="tab"`, `role="tabpanel"`
- [ ] Modal: focus trap implemented
- [ ] Modal: return focus to trigger on close

### 8.3 Keyboard Navigation
- [ ] All interactive elements reachable via Tab
- [ ] Tab order follows visual layout
- [ ] Focus indicators visible on all interactive elements
- [ ] `Escape` closes modals and overlays
- [ ] `Enter` activates buttons and links
- [ ] Arrow keys navigate sidebar items
- [ ] Arrow keys navigate search results
- [ ] Arrow keys navigate tabs
- [ ] Skip-to-content link at top of page
- [ ] Keyboard shortcut help dialog (Shift+?)
- [ ] All keyboard shortcuts documented

### 8.4 Color & Contrast
- [ ] Color contrast ratio >= 4.5:1 for normal text (WCAG AA)
- [ ] Color contrast ratio >= 3:1 for large text (WCAG AA)
- [ ] Color contrast ratio >= 3:1 for UI components and graphical objects
- [ ] Color is not the only means of conveying information
- [ ] HTTP method badges accessible without color (text labels present)
- [ ] Focus indicators have sufficient contrast
- [ ] Dark mode meets same contrast requirements

### 8.5 Screen Reader Support
- [ ] All images have descriptive alt text
- [ ] Decorative images have `alt=""`
- [ ] Icon-only buttons have accessible labels
- [ ] Page title updates on route change (`document.title`)
- [ ] Route announcements for screen readers (live region)
- [ ] Code blocks announced with language info
- [ ] Tables announced with caption or summary

### 8.6 Motion & Preferences
- [ ] `prefers-reduced-motion` respected for animations
- [ ] `prefers-color-scheme` used for initial theme detection
- [ ] `prefers-contrast` support (high contrast mode)
- [ ] Animations can be disabled globally
- [ ] No content relies solely on animation to be understood

---

## 9. Mobile & Responsive

### 9.1 Breakpoint Strategy
- [ ] Mobile first design (base styles for mobile)
- [ ] sm (640px): minor layout adjustments
- [ ] md (768px): header nav visible, two-column grid
- [ ] lg (1024px): sidebar visible, three-column layout (sidebar + content + TOC)
- [ ] xl (1280px): wider content area
- [ ] 2xl (1536px): max-width container

### 9.2 Mobile Layout
- [x] Mobile: header with hamburger menu button
- [x] Mobile: hamburger opens sidebar as overlay drawer
- [x] Mobile: overlay backdrop (`bg-black/50`)
- [x] Mobile: close button in sidebar drawer
- [x] Mobile: sidebar slides in from left
- [x] Mobile: nav links close sidebar on click (`setMobileMenuOpen(false)`)
- [ ] Mobile: bottom navigation bar (optional)
- [ ] Mobile: sticky header on scroll
- [ ] Mobile: content fills full width
- [ ] Mobile: code blocks horizontally scrollable
- [ ] Mobile: tables horizontally scrollable
- [ ] Mobile: images scale to container width
- [ ] Mobile: touch-friendly tap targets (min 44px)
- [ ] Mobile: swipe gesture to open/close sidebar
- [ ] Mobile: pull-to-refresh (optional)

### 9.3 Tablet Layout
- [ ] Tablet: sidebar hidden by default, toggle button visible
- [ ] Tablet: content uses full width when sidebar hidden
- [ ] Tablet: TOC hidden (available via button/dropdown)
- [ ] Tablet: header search visible
- [ ] Tablet: cards in 2-column grid

### 9.4 Desktop Layout
- [x] Desktop: sidebar always visible
- [x] Desktop: content in center
- [ ] Desktop: TOC on right side
- [ ] Desktop: three-column layout (sidebar 256px + content + TOC 200px)
- [ ] Desktop: content max-width `max-w-3xl` or `max-w-prose`
- [x] Desktop: header search bar visible

### 9.5 Responsive Components
- [ ] Category grid: 1 col mobile, 2 col tablet, 2 col desktop (confirmed in Home)
- [ ] Popular topics: 1 col mobile, 2 col tablet, 3 col desktop (confirmed in Home)
- [ ] API endpoint list: full width on all sizes
- [ ] Code blocks: horizontal scroll on overflow
- [ ] Tables: horizontal scroll wrapper on mobile
- [ ] Footer: stacked on mobile, row on desktop (confirmed in Layout)
- [ ] Breadcrumbs: horizontal scroll on mobile if too long
- [ ] Search: full-screen overlay on mobile

---

## 10. Internationalization

### 10.1 i18n Infrastructure
- [ ] i18n library chosen (react-intl, react-i18next, or similar)
- [ ] Language files: English (`en.json`)
- [ ] Language files: Spanish (`es.json`)
- [ ] Language files: French (`fr.json`)
- [ ] Language files: German (`de.json`)
- [ ] Language files: Japanese (`ja.json`)
- [ ] Language files: Chinese Simplified (`zh-CN.json`)
- [ ] Language files: Portuguese (`pt-BR.json`)
- [ ] Language files: Arabic (`ar.json`) -- RTL support
- [ ] Language selector in header or footer
- [ ] Language preference persisted to localStorage
- [ ] Language preference from browser `Accept-Language` header

### 10.2 Translatable Content
- [ ] All UI strings extracted to translation files
- [ ] Header navigation labels
- [ ] Sidebar section headers
- [ ] Search placeholder text
- [ ] Button labels (Copy, Submit, Cancel)
- [ ] Error messages
- [ ] Empty state messages
- [ ] Loading messages
- [ ] Footer text and links
- [ ] Accessibility labels (aria-label)
- [ ] Date/time formatting (locale-aware)
- [ ] Number formatting (locale-aware)

### 10.3 RTL Support
- [ ] `dir="rtl"` attribute set for Arabic/Hebrew
- [ ] Layout mirrors for RTL (sidebar on right)
- [ ] Icons flip for RTL (arrows, chevrons)
- [ ] Text alignment adapts for RTL
- [ ] CSS logical properties used (`margin-inline-start` vs `margin-left`)

---

## 11. Security

### 11.1 Authentication & Authorization
- [ ] Gate OAuth2 PKCE flow implemented
- [ ] Tokens stored securely (not in localStorage for access tokens)
- [ ] CSRF protection for state-changing operations
- [ ] Session timeout handling
- [ ] Automatic logout on token expiry
- [ ] Protected routes: forum posting requires auth
- [ ] Protected routes: feedback submission requires auth (or allows anonymous)
- [ ] Role-based access: admin features (moderation) restricted

### 11.2 Content Security
- [ ] Content Security Policy (CSP) headers
- [ ] XSS prevention: markdown sanitization (no raw HTML passthrough)
- [ ] XSS prevention: user-generated content escaped
- [ ] XSS prevention: `dangerouslySetInnerHTML` avoided or sanitized
- [ ] Subresource Integrity (SRI) for CDN resources
- [ ] No sensitive data in client-side code
- [ ] No API keys in client-side code
- [ ] Environment variables validated (no secrets in VITE_ prefixed vars)

### 11.3 Input Validation
- [ ] Search input: max length enforced
- [ ] Search input: special characters handled
- [ ] Feedback form: input validation
- [ ] Forum: markdown input sanitized
- [ ] URL parameters validated
- [ ] Rate limiting awareness (handle 429 gracefully)

### 11.4 Dependency Security
- [ ] `npm audit` run regularly
- [ ] No known high/critical vulnerabilities
- [ ] Dependabot or Renovate configured
- [ ] Lock file integrity verified

---

## 12. Testing

### 12.1 Unit Tests
- [ ] Test runner configured (Vitest)
- [ ] Test utilities: React Testing Library
- [ ] Unit test: `CodeBlock` component renders code content
- [ ] Unit test: `CodeBlock` copy-to-clipboard functionality
- [ ] Unit test: `CodeBlock` filename header display
- [ ] Unit test: `Step` component renders number and title
- [ ] Unit test: `CopyButton` component copy and success state
- [ ] Unit test: `EndpointItem` component expand/collapse
- [ ] Unit test: `EndpointItem` method badge color mapping
- [ ] Unit test: `EndpointItem` auth lock icon display
- [ ] Unit test: `GroupSection` component expand/collapse
- [ ] Unit test: API reference search filtering logic
- [ ] Unit test: search debounce logic
- [ ] Unit test: sidebar navigation state management
- [ ] Unit test: version selector logic
- [ ] Unit test: breadcrumb generation from route
- [ ] Unit test: TOC generation from headings
- [ ] Unit test: feedback submission logic
- [ ] Unit test: forum thread list sorting
- [ ] Unit test: forum reply nesting
- [ ] Unit test: auth token refresh logic
- [ ] Unit test: theme toggle logic
- [ ] Unit test: offline detection logic
- [ ] Unit test: keyboard shortcut handlers

### 12.2 Component Tests
- [ ] Component test: `Layout` renders header, sidebar, main, footer
- [ ] Component test: `Layout` mobile menu toggle
- [ ] Component test: `Layout` sidebar nav links navigate correctly
- [ ] Component test: `Layout` theme toggle works
- [ ] Component test: `Home` renders category grid
- [ ] Component test: `Home` popular topics rendered
- [ ] Component test: `Home` hero search input renders
- [ ] Component test: `Quickstart` renders all 6 steps
- [ ] Component test: `Quickstart` breadcrumb displays correctly
- [ ] Component test: `Quickstart` prev/next links work
- [ ] Component test: `ApiReference` renders all API groups
- [ ] Component test: `ApiReference` search filters endpoints
- [ ] Component test: `ApiReference` empty state on no match
- [ ] Component test: search overlay opens on Cmd+K
- [ ] Component test: search overlay closes on Escape
- [ ] Component test: search results navigate to page
- [ ] Component test: version selector changes active version
- [ ] Component test: feedback widget submit flow
- [ ] Component test: forum thread creation flow
- [ ] Component test: forum reply flow

### 12.3 Integration Tests
- [ ] Integration: route navigation (Home -> Quickstart -> API Reference)
- [ ] Integration: search flow (open, type, select result, navigate)
- [ ] Integration: auth flow (login, protected content access, logout)
- [ ] Integration: feedback flow (rate page, submit comment, confirmation)
- [ ] Integration: forum flow (browse, create thread, reply, upvote)
- [ ] Integration: version switch (select version, content updates)
- [ ] Integration: dark mode toggle (all pages update)
- [ ] Integration: offline/online transition

### 12.4 E2E Tests
- [ ] E2E framework configured (Playwright or Cypress)
- [ ] E2E: homepage loads with all sections
- [ ] E2E: navigate through Getting Started guide
- [ ] E2E: API reference search and expand endpoint
- [ ] E2E: mobile sidebar toggle
- [ ] E2E: dark mode toggle
- [ ] E2E: search with Cmd+K
- [ ] E2E: copy code block
- [ ] E2E: forum thread creation (with auth)
- [ ] E2E: cross-browser: Chrome
- [ ] E2E: cross-browser: Firefox
- [ ] E2E: cross-browser: Safari
- [ ] E2E: mobile viewport tests

### 12.5 Visual Regression Tests
- [ ] Visual regression: homepage (light + dark)
- [ ] Visual regression: quickstart page (light + dark)
- [ ] Visual regression: API reference page (light + dark)
- [ ] Visual regression: search overlay (light + dark)
- [ ] Visual regression: mobile layout
- [ ] Visual regression: code blocks with syntax highlighting
- [ ] Visual regression: forum pages

### 12.6 Accessibility Tests
- [ ] aXe automated accessibility audit: zero violations
- [ ] Lighthouse accessibility score >= 95
- [ ] Manual screen reader testing (VoiceOver, NVDA)
- [ ] Manual keyboard-only navigation testing
- [ ] Color contrast verified with automated tool

### 12.7 Performance Tests
- [ ] Lighthouse performance score >= 90
- [ ] Bundle size regression test in CI
- [ ] First load time < 3s on slow 3G
- [ ] Search response time < 500ms

---

## 13. Documentation

### 13.1 Developer Documentation
- [ ] README.md: project overview and purpose
- [ ] README.md: tech stack summary
- [ ] README.md: local development setup instructions
- [ ] README.md: environment variables reference
- [ ] README.md: project structure / folder overview
- [ ] README.md: available npm scripts
- [ ] README.md: deployment instructions
- [ ] CONTRIBUTING.md: contribution guidelines
- [ ] CONTRIBUTING.md: code style guide
- [ ] CONTRIBUTING.md: PR template
- [ ] CONTRIBUTING.md: issue template
- [ ] ARCHITECTURE.md: component architecture diagram
- [ ] ARCHITECTURE.md: state management overview
- [ ] ARCHITECTURE.md: routing structure
- [ ] ARCHITECTURE.md: API integration layer

### 13.2 Code Documentation
- [ ] JSDoc comments on exported functions
- [ ] JSDoc comments on component props interfaces
- [ ] JSDoc comments on Zustand store slices
- [ ] JSDoc comments on utility functions
- [ ] JSDoc comments on API client methods
- [ ] Inline comments for complex logic
- [ ] TypeScript types self-documenting with descriptive names

---

## 14. Deployment & CI/CD

### 14.1 Build Pipeline
- [ ] GitHub Actions workflow for CI
- [ ] CI: install dependencies
- [ ] CI: lint check (ESLint)
- [ ] CI: type check (tsc --noEmit)
- [ ] CI: unit tests (Vitest)
- [ ] CI: build production bundle
- [ ] CI: bundle size check (fail if over budget)
- [ ] CI: E2E tests on PR
- [ ] CI: visual regression tests on PR
- [ ] CI: accessibility audit on PR
- [ ] CI: security audit (npm audit)
- [ ] CI: deploy preview on PR (Vercel/Netlify preview)

### 14.2 Production Build
- [ ] Production build outputs to `/dist`
- [ ] HTML minification
- [ ] CSS minification and purging
- [ ] JavaScript minification and tree-shaking
- [ ] Asset hashing for cache busting
- [ ] Gzip compression
- [ ] Brotli compression
- [ ] Source maps uploaded to error tracking (Sentry)
- [ ] Build metadata (version, commit hash, build date)

### 14.3 Hosting & CDN
- [ ] Static site hosting configured (Vercel, Netlify, S3+CloudFront, or Docker)
- [ ] CDN for static assets
- [ ] Custom domain configured
- [ ] SSL/TLS certificate
- [ ] HTTP/2 enabled
- [ ] Cache headers configured for assets
- [ ] 301 redirects for old URLs
- [ ] 404 page configured for client-side routing (SPA fallback)
- [ ] CORS headers for API calls

### 14.4 Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (Real User Monitoring)
- [ ] Uptime monitoring
- [ ] Analytics (page views, search queries, popular docs)
- [ ] Core Web Vitals tracking
- [ ] Alerting on error rate spikes

---

## 15. Backend

### 15.1 Search Backend
- [ ] Search engine chosen (Elasticsearch, Algolia, Meilisearch, or Typesense)
- [ ] Search index schema defined (title, body, section, version, URL, tags)
- [ ] Indexing pipeline: markdown files parsed and indexed
- [ ] Indexing pipeline: API reference auto-indexed from OpenAPI specs
- [ ] Indexing pipeline: changelog entries indexed
- [ ] Indexing pipeline: forum posts indexed
- [ ] Search API: `GET /api/search` with query, filters, pagination
- [ ] Search API: relevance scoring tuned
- [ ] Search API: typo tolerance configured
- [ ] Search API: synonym support
- [ ] Search API: result highlighting
- [ ] Search API: faceted search (by section, version)
- [ ] Search API: rate limiting
- [ ] Search index: automatic re-indexing on content change
- [ ] Search index: version-specific indexes

### 15.2 AI Search Backend
- [ ] AI service: LLM integration (Claude API or OpenAI)
- [ ] AI service: RAG (Retrieval-Augmented Generation) pipeline
- [ ] AI service: documentation embeddings generated and stored
- [ ] AI service: vector database (Pinecone, Qdrant, pgvector)
- [ ] AI service: streaming response endpoint
- [ ] AI service: source citation extraction
- [ ] AI service: conversation context management
- [ ] AI service: rate limiting and cost controls
- [ ] AI service: response quality monitoring
- [ ] AI service: feedback loop (user ratings improve responses)

### 15.3 Forum Backend
- [ ] Forum database: PostgreSQL schema (boards, threads, replies, votes)
- [ ] Forum API: CRUD for threads
- [ ] Forum API: CRUD for replies
- [ ] Forum API: voting endpoints
- [ ] Forum API: search endpoint
- [ ] Forum API: moderation endpoints
- [ ] Forum API: pagination
- [ ] Forum API: authentication via Gate JWT
- [ ] Forum API: authorization (role-based)
- [ ] Forum API: rate limiting
- [ ] Forum API: email notifications (new reply to subscribed thread)
- [ ] Forum: markdown sanitization on input

### 15.4 Feedback Backend
- [ ] Feedback database: schema (page_url, rating, comment, user_id, timestamp)
- [ ] Feedback API: `POST /api/feedback`
- [ ] Feedback API: `GET /api/feedback/stats` (admin)
- [ ] Feedback API: rate limiting (1 per page per session)
- [ ] Feedback: aggregate reports for team dashboard

### 15.5 Analytics Backend
- [ ] Analytics: page view events stored
- [ ] Analytics: search query events stored
- [ ] Analytics: popular pages report
- [ ] Analytics: search query trends report
- [ ] Analytics: user journey analysis
- [ ] Analytics: time-on-page tracking
- [ ] Analytics: scroll depth tracking
- [ ] Analytics: dashboard for team

### 15.6 Content Management
- [ ] Docs content: stored as markdown files in Git
- [ ] Docs content: build-time processing (frontmatter, slug generation)
- [ ] Docs content: versioning (Git branches or tags)
- [ ] Docs content: CI/CD deploys on content change
- [ ] Docs content: automated link checking (no broken internal links)
- [ ] Docs content: spell check in CI
- [ ] Docs content: style guide enforcement (Vale or similar)

---

## Summary

| Section | Done | Todo | Total |
|---------|------|------|-------|
| 1. Project Setup & Configuration | ~12 | ~80 | ~92 |
| 2. Design System Integration | ~4 | ~65 | ~69 |
| 3. Dark Mode | ~1 | ~95 | ~96 |
| 4. Core Features | ~35 | ~200 | ~235 |
| 5. API Integration | 0 | ~45 | ~45 |
| 6. State Management | 0 | ~20 | ~20 |
| 7. Performance | ~2 | ~45 | ~47 |
| 8. Accessibility | ~5 | ~50 | ~55 |
| 9. Mobile & Responsive | ~8 | ~30 | ~38 |
| 10. Internationalization | 0 | ~25 | ~25 |
| 11. Security | 0 | ~20 | ~20 |
| 12. Testing | 0 | ~65 | ~65 |
| 13. Documentation | 0 | ~20 | ~20 |
| 14. Deployment & CI/CD | 0 | ~30 | ~30 |
| 15. Backend | 0 | ~55 | ~55 |
| **TOTAL** | **~67** | **~845** | **~912** |

---

> Generated: 2026-04-06
> Source: `/Learn/frontend/src/` codebase analysis + PER_APP_CHECKLIST.md sections 15-A through 15-H
