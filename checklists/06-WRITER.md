# 06 — Writer: Document Editor — Comprehensive Checklist

> **App:** RM Orbit Writer
> **Stack:** React 19.2.0 · Vite 7.3.1 · React Router v7 · Zustand · FastAPI backend · Tailwind v3 · SQLAlchemy · Alembic
> **Frontend Pages:** Dashboard (`Dashboard.tsx`), Document (`Document.tsx`), Sheets (`Sheets.tsx`)
> **Frontend Components:** Layout (`Layout.tsx`), Sidebar (`Sidebar.tsx`)
> **Backend Modules:** `main.py`, `models.py`, `schemas.py`, `auth.py`, `database.py`, `eventbus.py`
> **Backend Models:** Document, Block, BlockRelation, BlockVersion
> **Block Types (schema):** text, table, chart, slide, code, sticky, ai
> **Render Modes:** document, data, slide, notes
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

### 1.1 Frontend Project Structure
- [ ] Verify `package.json` has correct name (`@orbit/writer`)
- [ ] Verify React 19 is installed and configured
- [ ] Verify Vite 7 is installed with correct plugins
- [ ] Verify React Router v7 is configured with all routes
- [ ] Verify Zustand is installed for state management
- [ ] Verify Tailwind v3 is installed and configured
- [ ] Verify `@orbit-ui/react` is listed as a dependency
- [ ] Verify `lucide-react` is installed for icons
- [ ] Verify TypeScript is configured (`tsconfig.json`)
- [ ] Verify path aliases (`@/` mapping) in `vite.config.ts`
- [ ] Verify ESLint is configured with consistent rules
- [ ] Verify Prettier is configured with consistent rules
- [ ] Verify `.env` / `.env.example` files exist with required variables
- [ ] Verify `VITE_API_BASE` environment variable is set
- [ ] Verify `VITE_WRITER_BACKEND` environment variable is set
- [ ] Verify `VITE_WS_URL` environment variable for WebSocket endpoint
- [ ] Add `.env.example` with all required variables documented
- [ ] Configure Vite proxy for `/api` to FastAPI backend
- [ ] Configure Vite proxy for `/ws` WebSocket connections
- [ ] Verify `index.html` has correct meta tags (charset, viewport)
- [ ] Verify `index.html` has Anti-FOUC script
- [ ] Verify `index.html` has correct title and favicon
- [ ] Remove any unused dependencies from `package.json`
- [ ] Verify all dev dependencies are correctly categorized
- [ ] Add `engines` field to `package.json` (Node >= 20)

### 1.2 Backend Project Structure
- [ ] Verify `requirements.txt` lists all Python dependencies
- [ ] Verify FastAPI is installed and configured
- [ ] Verify SQLAlchemy is installed and configured
- [ ] Verify Alembic is installed for database migrations
- [ ] Verify `alembic.ini` is configured with correct database URL
- [ ] Verify `app/__init__.py` exists
- [ ] Verify `app/main.py` creates FastAPI app instance
- [ ] Verify `app/models.py` defines all ORM models
- [ ] Verify `app/schemas.py` defines all Pydantic schemas
- [ ] Verify `app/auth.py` handles authentication
- [ ] Verify `app/database.py` handles DB connection
- [ ] Verify `app/eventbus.py` handles event publishing
- [ ] Verify `tests/conftest.py` sets up test fixtures
- [ ] Verify `tests/test_api.py` has API test cases
- [ ] Verify `tests/test_eventbus_contract.py` has EventBus tests
- [ ] Add `pyproject.toml` or `setup.cfg` for linting config
- [ ] Add `mypy.ini` or `[mypy]` section for type checking
- [ ] Add `ruff.toml` for Python linting
- [ ] Verify `migrate.sh` script works correctly

### 1.3 Routing Configuration
- [ ] Route: `/` — Dashboard page (document list)
- [ ] Route: `/document` — Document editor page
- [ ] Route: `/document/:id` — Document editor with specific document
- [ ] Route: `/sheets` — Spreadsheet/Sheets page
- [ ] Route: `/sheets/:id` — Specific sheet
- [ ] Route: `/templates` — Template gallery page
- [ ] Route: `/presentations` — Presentation/slides mode
- [ ] Route: `/canvas` — Infinite canvas mode
- [ ] Route: `/knowledge-graph` — Knowledge graph view
- [ ] Route: `/trash` — Trashed documents
- [ ] Route: `/shared` — Shared with me documents
- [ ] Route: `/favorites` — Starred/favorited documents
- [ ] Route: `/settings` — Writer settings page
- [ ] 404 catch-all route with custom not-found page
- [ ] All routes wrapped in `Layout` component
- [ ] All routes lazy-loaded with `React.lazy()`
- [ ] Route guards for authenticated-only pages
- [ ] Breadcrumb navigation reflects current route

---

## 2. Design System Integration

### 2.1 Token & Theme Setup
- [x] Anti-FOUC script in `index.html`
- [x] `ThemeProvider` wraps root component
- [x] Material Symbols icon font removed
- [x] `index.css` imports `@import "/orbit-ui/orbit-tokens.css";`
- [ ] `tailwind.config.js` uses shared orbit preset
- [ ] Remove all hardcoded color values (grep for `#` hex codes)
- [ ] Remove all hardcoded `bg-gray-*` / `text-gray-*` classes
- [ ] Replace all `border-gray-*` with `border-border-default` / `border-border-subtle`
- [ ] Replace all `bg-white` with `bg-surface-base`
- [ ] Replace all `bg-gray-50` / `bg-slate-50` with `bg-surface-subtle`
- [ ] Replace all `bg-gray-100` / `bg-slate-100` with `bg-surface-muted`
- [ ] Replace all `text-gray-900` with `text-content-primary`
- [ ] Replace all `text-gray-500` / `text-gray-600` with `text-content-secondary`
- [ ] Replace all `text-gray-400` with `text-content-muted`
- [ ] Replace `focus:ring-blue-*` with `focus-ring` utility
- [ ] Replace all `shadow-sm` / `shadow-md` with orbit shadow tokens
- [ ] Replace all hardcoded `rounded-*` with orbit radius tokens
- [ ] Replace all `font-sans` with orbit font-sans (RM Forma)
- [ ] Replace all `font-mono` with orbit font-mono (JetBrains Mono)
- [ ] Verify CSS custom properties are used in all component styles

### 2.2 Replace Custom Components with @orbit-ui/react

#### Button
- [ ] Replace custom Dashboard "New Document" button with `<Button>`
- [ ] Replace custom Dashboard "Create" button with `<Button variant="primary">`
- [ ] Replace custom Document toolbar buttons with `<Button variant="ghost" size="sm">`
- [ ] Replace custom Sheets toolbar buttons with `<Button>`
- [ ] Replace custom Sidebar action buttons with `<Button>`
- [ ] Replace custom modal confirm/cancel buttons with `<Button>`
- [ ] Replace custom "Save" button with `<Button variant="primary">`
- [ ] Replace custom "Delete" button with `<Button variant="danger">`
- [ ] Replace custom "Export" buttons with `<Button variant="outline">`
- [ ] Replace custom icon-only buttons with `<IconButton>`
- [ ] Ensure all buttons use consistent sizing (sm for toolbar, md for actions)

#### Input
- [ ] Replace custom search input on Dashboard with `<Input>` from orbit-ui
- [ ] Replace custom workspace ID input with `<Input>`
- [ ] Replace custom document title input with `<Input>`
- [ ] Replace custom rename input with `<Input>`
- [ ] Replace custom Sheets cell edit input with `<Input>`
- [ ] Replace custom filter/search inputs with `<Input prefix={<SearchIcon />}>`
- [ ] Replace custom formula bar input with `<Input>`

#### Modal
- [ ] Replace custom modal component with `<Modal>` from orbit-ui
- [ ] Replace custom document creation dialog with `<Modal>`
- [ ] Replace custom document deletion confirmation with `<Modal>` (AlertDialog variant)
- [ ] Replace custom version history modal with `<Modal size="lg">`
- [ ] Replace custom share/permissions modal with `<Modal>`
- [ ] Replace custom template selection modal with `<Modal size="xl">`
- [ ] Replace custom export options modal with `<Modal>`
- [ ] Replace custom import modal with `<Modal>`
- [ ] Replace custom settings dialog with `<Modal>`
- [ ] Replace custom keyboard shortcuts overlay with `<Modal>`

#### Badge
- [ ] Replace custom document status badge (draft/published) with `<Badge>`
- [ ] Replace custom word count indicator with `<Badge variant="subtle">`
- [ ] Replace custom block type indicator with `<Badge>`
- [ ] Replace custom version number badge with `<Badge>`
- [ ] Replace custom "Saved" / "Saving..." indicator with `<Badge>`
- [ ] Replace custom collaboration user count with `<Badge>`
- [ ] Replace custom sheet tab count with `<Badge>`
- [ ] Replace custom comment count badge with `<Badge>`

#### Avatar
- [ ] Replace custom user avatar in sidebar with `<Avatar>`
- [ ] Replace custom collaborator avatars with `<Avatar>`
- [ ] Replace custom cursor presence labels with `<Avatar size="xs">`
- [ ] Replace custom comment author avatars with `<Avatar>`
- [ ] Replace custom sharing/permissions user avatars with `<Avatar>`
- [ ] Replace custom mention suggestion avatars with `<Avatar>`

#### Card
- [ ] Replace custom document card on Dashboard with `<Card interactive>`
- [ ] Replace custom template card with `<Card>`
- [ ] Replace custom recent documents card with `<Card>`
- [ ] Replace custom folder card with `<Card>`
- [ ] Replace custom KPI/stats card (Sheets) with `<Card>`

#### Tabs
- [ ] Replace custom Sheets tab bar with `<Tabs>`
- [ ] Replace custom document view mode tabs (doc/slides/data) with `<Tabs>`
- [ ] Replace custom sidebar section tabs with `<Tabs>`
- [ ] Replace custom version history tabs with `<Tabs>`
- [ ] Replace custom settings tabs with `<Tabs>`
- [ ] Replace custom comment/activity tabs with `<Tabs>`

#### Dropdown
- [ ] Replace custom block type selector dropdown with `<Dropdown>`
- [ ] Replace custom document actions menu (rename/delete/export) with `<Dropdown>`
- [ ] Replace custom Sheets column type selector with `<Dropdown>`
- [ ] Replace custom toolbar "more actions" menu with `<Dropdown>`
- [ ] Replace custom right-click context menu with `<ContextMenu>`
- [ ] Replace custom sort/filter dropdowns with `<Dropdown>`
- [ ] Replace custom share permissions dropdown with `<Dropdown>`
- [ ] Replace custom export format selector with `<Dropdown>`

#### Tooltip
- [ ] Add `<Tooltip>` to all toolbar buttons (Bold, Italic, etc.)
- [ ] Add `<Tooltip>` to sidebar action icons
- [ ] Add `<Tooltip>` to document card actions
- [ ] Add `<Tooltip>` to Sheets column header actions
- [ ] Add `<Tooltip>` to collaboration presence indicators
- [ ] Add `<Tooltip>` to version history items
- [ ] Add `<Tooltip>` to keyboard shortcut hints
- [ ] Add `<Tooltip>` to slash command menu items

#### Sidebar
- [ ] Replace custom `Sidebar.tsx` with `<Sidebar>` from orbit-ui
- [ ] Use `<SidebarItem>` for each navigation entry
- [ ] Implement collapsible sidebar (icon-only mode)
- [ ] Implement sidebar sections (Documents, Favorites, Shared, Trash)
- [ ] Add sidebar footer with settings and user profile
- [ ] Add keyboard shortcut to toggle sidebar (`Cmd+\`)

#### Skeleton
- [ ] Replace loading states on Dashboard with `<Skeleton>` cards
- [ ] Add `<Skeleton>` for document list loading
- [ ] Add `<Skeleton>` for document editor loading
- [ ] Add `<Skeleton>` for Sheets grid loading
- [ ] Add `<Skeleton>` for version history loading
- [ ] Add `<Skeleton>` for template gallery loading
- [ ] Add `<Skeleton>` for sidebar loading

#### Spinner
- [ ] Replace custom loading spinner with `<Spinner>`
- [ ] Use `<Spinner>` for document save indicator
- [ ] Use `<Spinner>` for block creation loading
- [ ] Use `<Spinner>` for export processing
- [ ] Use `<Spinner>` for import processing
- [ ] Use `<Spinner>` for version restore loading

#### EmptyState
- [ ] Add `<EmptyState>` for no documents in Dashboard
- [ ] Add `<EmptyState>` for no search results
- [ ] Add `<EmptyState>` for empty document (no blocks)
- [ ] Add `<EmptyState>` for no versions in history
- [ ] Add `<EmptyState>` for no templates available
- [ ] Add `<EmptyState>` for no comments on document
- [ ] Add `<EmptyState>` for empty trash
- [ ] Add `<EmptyState>` for no shared documents
- [ ] Add `<EmptyState>` for empty Sheets view

#### Alert
- [ ] Replace custom error messages with `<Alert variant="error">`
- [ ] Replace custom success messages with `<Alert variant="success">`
- [ ] Replace custom warning messages with `<Alert variant="warning">`
- [ ] Add `<Alert>` for unsaved changes warning
- [ ] Add `<Alert>` for offline mode notification
- [ ] Add `<Alert>` for collaboration conflict notification

#### DatePicker
- [ ] Add `<DatePicker>` for document creation date filter
- [ ] Add `<DatePicker>` for version history date filter
- [ ] Add `<DatePicker>` for Sheets date column cells
- [ ] Add `<DatePicker>` for scheduled publish date

#### FileUpload
- [ ] Add `<FileUpload>` for image block insertion
- [ ] Add `<FileUpload>` for file attachment to documents
- [ ] Add `<FileUpload>` for CSV import in Sheets
- [ ] Add `<FileUpload>` for template import
- [ ] Add `<FileUpload>` for document import (DOCX/MD)

#### Table
- [ ] Replace custom document list table with `<Table>` from orbit-ui
- [ ] Replace custom version history table with `<Table>`
- [ ] Replace custom Sheets grid with enhanced `<Table>` or custom DataGrid
- [ ] Add sortable headers to document list table
- [ ] Add row selection to document list table
- [ ] Add pagination to document list table

#### Progress
- [ ] Add `<Progress>` for export progress
- [ ] Add `<Progress>` for import progress
- [ ] Add `<Progress>` for file upload progress
- [ ] Add `<Progress>` for sync progress indicator

#### Breadcrumb
- [ ] Add `<Breadcrumb>` for document path (workspace > folder > document)
- [ ] Add `<Breadcrumb>` for Sheets navigation
- [ ] Add `<Breadcrumb>` for nested folder navigation

#### Tag
- [ ] Add `<Tag>` for document tags/labels
- [ ] Add `<Tag>` for document categories
- [ ] Add `<Tag>` for block type indicators
- [ ] Add `<Tag>` input for tagging documents

---

## 3. Dark Mode

### 3.1 Dashboard Page
- [x] Dashboard: document card list — uses semantic tokens
- [x] Dashboard: sidebar — uses semantic tokens
- [x] Dashboard: search bar — uses semantic tokens
- [ ] Dashboard: workspace selector input in dark mode
- [ ] Dashboard: "New Document" button states in dark mode
- [ ] Dashboard: document card hover state in dark mode
- [ ] Dashboard: document card selected state in dark mode
- [ ] Dashboard: document grid/list toggle in dark mode
- [ ] Dashboard: sort/filter controls in dark mode
- [ ] Dashboard: pagination controls in dark mode
- [ ] Dashboard: loading skeleton in dark mode
- [ ] Dashboard: empty state illustration in dark mode
- [ ] Dashboard: error state in dark mode
- [ ] Dashboard: folder tree in dark mode
- [ ] Dashboard: recent documents section in dark mode
- [ ] Dashboard: favorites section in dark mode
- [ ] Dashboard: breadcrumb navigation in dark mode

### 3.2 Document Editor Page
- [ ] Editor: text body background in dark mode
- [ ] Editor: toolbar background and border in dark mode
- [ ] Editor: toolbar button default state in dark mode
- [ ] Editor: toolbar button hover state in dark mode
- [ ] Editor: toolbar button active/pressed state in dark mode
- [ ] Editor: toolbar button disabled state in dark mode
- [ ] Editor: toolbar separator/divider in dark mode
- [ ] Editor: editor margins and padding in dark mode
- [ ] Editor: cursor color in dark mode
- [ ] Editor: text selection highlight in dark mode
- [ ] Editor: paragraph text color in dark mode
- [ ] Editor: heading text color (H1, H2, H3) in dark mode
- [ ] Editor: placeholder text color in dark mode
- [ ] Editor: link text color and underline in dark mode
- [ ] Editor: inline code background in dark mode
- [ ] Editor: code block background and border in dark mode
- [ ] Editor: code block syntax highlighting in dark mode
- [ ] Editor: blockquote border and background in dark mode
- [ ] Editor: horizontal divider color in dark mode
- [ ] Editor: list bullet/number color in dark mode
- [ ] Editor: checkbox (todo) checked/unchecked in dark mode
- [ ] Editor: callout block background (info/warning/tip) in dark mode
- [ ] Editor: image block border and caption in dark mode
- [ ] Editor: table cell borders and header row in dark mode
- [ ] Editor: table selected cell highlight in dark mode
- [ ] Editor: embed block border and placeholder in dark mode
- [ ] Editor: math equation rendering in dark mode

### 3.3 Block Handles & Menus
- [ ] Block handles: drag handle icon color in dark mode
- [ ] Block handles: hover state in dark mode
- [ ] Slash command menu: background in dark mode
- [ ] Slash command menu: item hover state in dark mode
- [ ] Slash command menu: item selected state in dark mode
- [ ] Slash command menu: category header color in dark mode
- [ ] Slash command menu: search input in dark mode
- [ ] Slash command menu: icon colors in dark mode
- [ ] Inline formatting toolbar: background in dark mode
- [ ] Inline formatting toolbar: button states in dark mode
- [ ] Block type selector dropdown in dark mode
- [ ] Color picker for text/highlight in dark mode

### 3.4 Panels & Overlays
- [ ] Inline comments panel: background in dark mode
- [ ] Inline comments panel: comment bubble in dark mode
- [ ] Inline comments panel: input field in dark mode
- [ ] Inline comments panel: resolved state in dark mode
- [ ] Version history panel: background in dark mode
- [ ] Version history panel: version item in dark mode
- [ ] Version history panel: diff highlighting in dark mode
- [ ] Version history panel: restore button in dark mode
- [ ] Share/permissions dialog in dark mode
- [ ] Template selection modal in dark mode
- [ ] Export options modal in dark mode
- [ ] Keyboard shortcuts overlay in dark mode
- [ ] Document info/properties panel in dark mode

### 3.5 Sheets View
- [x] Sheets: cell backgrounds and borders — uses semantic tokens
- [ ] Sheets: column header background in dark mode
- [ ] Sheets: row header background in dark mode
- [ ] Sheets: selected cell highlight in dark mode
- [ ] Sheets: selected range highlight in dark mode
- [ ] Sheets: cell edit mode background in dark mode
- [ ] Sheets: formula bar in dark mode
- [ ] Sheets: sheet tab bar in dark mode
- [ ] Sheets: sheet tab active state in dark mode
- [ ] Sheets: sheet tab hover state in dark mode
- [ ] Sheets: add sheet button in dark mode
- [ ] Sheets: toolbar buttons in dark mode
- [ ] Sheets: filter/sort controls in dark mode
- [ ] Sheets: column resize handle in dark mode
- [ ] Sheets: frozen row/column divider in dark mode
- [ ] Sheets: badge cells (status, category) in dark mode
- [ ] Sheets: currency cells in dark mode
- [ ] Sheets: date cells in dark mode
- [ ] Sheets: empty rows in dark mode
- [ ] Sheets: scrollbar in dark mode
- [ ] Sheets: context menu in dark mode
- [ ] Sheets: search/filter overlay in dark mode

### 3.6 Collaboration UI
- [ ] Cursor presence labels in dark mode
- [ ] Collaborator avatar bar in dark mode
- [ ] "X users editing" indicator in dark mode
- [ ] Conflict resolution banner in dark mode
- [ ] Online/offline status indicator in dark mode

### 3.7 AI Features UI
- [ ] AI writing assistant panel in dark mode
- [ ] AI suggestion highlights in dark mode
- [ ] AI lasso selection overlay in dark mode
- [ ] AI generation loading state in dark mode
- [ ] AI prompt input in dark mode

### 3.8 Global Dark Mode Verification
- [ ] Verify color contrast ratios meet WCAG AA in dark mode (4.5:1 for text)
- [ ] Verify all focus rings are visible in dark mode
- [ ] Verify all icons are visible against dark backgrounds
- [ ] Verify all charts/visualizations adapt to dark mode
- [ ] Verify all scrollbar styles in dark mode
- [ ] Verify dark mode toggle persists across sessions
- [ ] Verify dark mode applies immediately without flash
- [ ] Test dark mode on all routes simultaneously

---

## 4. Core Features

### 4.1 Document Dashboard
- [ ] Document list: display documents as cards with title, preview, modified date
- [ ] Document list: grid view layout
- [ ] Document list: list view layout
- [ ] Document list: grid/list view toggle with persistence
- [ ] Document list: sort by name (A-Z, Z-A)
- [ ] Document list: sort by date modified (newest, oldest)
- [ ] Document list: sort by date created (newest, oldest)
- [ ] Document list: sort by word count
- [ ] Document list: filter by status (draft, published, archived)
- [ ] Document list: filter by tag/label
- [ ] Document list: filter by author/owner
- [ ] Document list: filter by date range
- [ ] Document list: search by title (debounced, 300ms)
- [ ] Document list: search by content (full-text)
- [ ] Document list: search result highlighting
- [ ] Document list: pagination (load more / infinite scroll)
- [ ] Document list: bulk select with checkboxes
- [ ] Document list: bulk actions (delete, archive, move, tag)
- [ ] Document creation: create blank document
- [ ] Document creation: create from template
- [ ] Document creation: default title with timestamp ("Untitled HH:MM")
- [ ] Document creation: navigate to editor after creation
- [ ] Document duplication: duplicate existing document with all blocks
- [ ] Document archiving: move to archive (soft delete)
- [ ] Document deletion: move to trash with confirmation
- [ ] Document deletion: permanent delete from trash
- [ ] Document restore: restore from trash
- [ ] Folder organization: create folders
- [ ] Folder organization: nested folders (multi-level)
- [ ] Folder organization: move documents between folders
- [ ] Folder organization: rename folders
- [ ] Folder organization: delete folders (with contents warning)
- [ ] Folder organization: drag-and-drop documents into folders
- [ ] Favorites: star/unstar documents
- [ ] Favorites: dedicated favorites view
- [ ] Recent documents: show last 10 opened documents
- [ ] Recent documents: widget on dashboard
- [ ] Shared documents: "Shared with me" section
- [ ] Shared documents: show who shared and permission level
- [ ] All documents: toggle between "My documents" and "All workspace documents"
- [ ] Workspace selector: switch between workspaces
- [ ] Workspace selector: persist selected workspace to localStorage

### 4.2 Block Editor — Block Types

#### Paragraph Block
- [ ] Create paragraph block on Enter
- [ ] Paragraph text input and editing
- [ ] Paragraph text wrapping
- [ ] Convert paragraph to other block types
- [ ] Empty paragraph placeholder text ("Type '/' for commands")
- [ ] Auto-merge adjacent empty paragraphs

#### Heading Blocks
- [ ] Heading 1 block (H1) with large font
- [ ] Heading 2 block (H2) with medium font
- [ ] Heading 3 block (H3) with small font
- [ ] Heading 4 block (H4)
- [ ] Convert heading to paragraph (Backspace at start)
- [ ] Heading auto-detection (type `# ` for H1, `## ` for H2, `### ` for H3)
- [ ] Heading anchor links for table of contents
- [ ] Heading numbering option

#### List Blocks
- [ ] Bulleted list: create with `- ` or `* ` prefix
- [ ] Bulleted list: nested items (indent with Tab)
- [ ] Bulleted list: outdent with Shift+Tab
- [ ] Bulleted list: continue list on Enter
- [ ] Bulleted list: exit list on double Enter
- [ ] Numbered list: create with `1. ` prefix
- [ ] Numbered list: auto-increment numbers
- [ ] Numbered list: nested items with sub-numbering
- [ ] Numbered list: continue on Enter
- [ ] Numbered list: exit on double Enter
- [ ] Checkbox list (todo): create with `[] ` prefix
- [ ] Checkbox list: toggle check on click
- [ ] Checkbox list: strikethrough completed items
- [ ] Checkbox list: completion count display
- [ ] Toggle list: collapsible content sections
- [ ] Toggle list: expand/collapse animation

#### Code Block
- [ ] Code block creation (``` prefix or slash command)
- [ ] Code block: syntax highlighting (multi-language)
- [ ] Code block: language selector dropdown
- [ ] Code block: line numbers toggle
- [ ] Code block: copy code button
- [ ] Code block: word wrap toggle
- [ ] Code block: tab indentation support
- [ ] Code block: auto-indent on Enter
- [ ] Code block: bracket matching
- [ ] Code block: supported languages (JavaScript, TypeScript, Python, Go, Rust, Java, C++, HTML, CSS, SQL, JSON, YAML, Markdown, Bash, etc.)

#### Image Block
- [ ] Image upload from local file
- [ ] Image paste from clipboard
- [ ] Image from URL
- [ ] Image drag-and-drop into editor
- [ ] Image resize handles (drag corners)
- [ ] Image alignment (left, center, right, full-width)
- [ ] Image caption text
- [ ] Image alt text (accessibility)
- [ ] Image loading placeholder/skeleton
- [ ] Image error state (broken image fallback)
- [ ] Image lightbox on click (full-screen preview)
- [ ] Image download option

#### Table Block
- [ ] Table creation (specify rows x columns)
- [ ] Table: add row (above/below)
- [ ] Table: add column (left/right)
- [ ] Table: delete row
- [ ] Table: delete column
- [ ] Table: merge cells
- [ ] Table: split cells
- [ ] Table: cell text editing
- [ ] Table: cell alignment (left/center/right)
- [ ] Table: header row toggle
- [ ] Table: header column toggle
- [ ] Table: cell background color
- [ ] Table: border visibility toggle
- [ ] Table: resize columns by dragging
- [ ] Table: resize rows by dragging
- [ ] Table: tab navigation between cells
- [ ] Table: copy/paste within table

#### Embed Block
- [ ] YouTube video embed (paste URL)
- [ ] Vimeo video embed
- [ ] Twitter/X embed
- [ ] CodePen embed
- [ ] Figma embed
- [ ] Google Maps embed
- [ ] Generic iFrame embed with URL input
- [ ] Embed responsive sizing
- [ ] Embed loading state
- [ ] Embed error state (invalid URL)

#### Callout Block
- [ ] Info callout (blue icon + background)
- [ ] Warning callout (yellow icon + background)
- [ ] Tip/success callout (green icon + background)
- [ ] Error/danger callout (red icon + background)
- [ ] Custom callout (choose icon and color)
- [ ] Callout text editing
- [ ] Callout icon selector

#### Quote Block
- [ ] Blockquote creation (`> ` prefix)
- [ ] Blockquote left border styling
- [ ] Blockquote italic text option
- [ ] Blockquote attribution line
- [ ] Nested blockquotes

#### Divider Block
- [ ] Horizontal rule creation (`---` prefix)
- [ ] Divider styling (thin/thick/dotted/dashed)
- [ ] Divider with spacing control

#### Math/Equation Block
- [ ] LaTeX equation input
- [ ] Live equation preview
- [ ] Inline math (wrapped in `$...$`)
- [ ] Block math (wrapped in `$$...$$`)
- [ ] Equation numbering
- [ ] Common equation templates

#### Sticky Note Block
- [ ] Sticky note creation with color selection
- [ ] Sticky note text editing
- [ ] Sticky note resize
- [ ] Sticky note color options (yellow, pink, blue, green, purple)
- [ ] Sticky note on infinite canvas

#### AI Block
- [ ] AI content generation block
- [ ] AI prompt input field
- [ ] AI response streaming display
- [ ] AI response accept/reject actions
- [ ] AI response editing before accepting
- [ ] AI block loading state

#### Slide/Presentation Block
- [ ] Slide block creation
- [ ] Slide title field
- [ ] Slide content area
- [ ] Slide background options
- [ ] Slide layout templates (title, title+content, two-column, image+text)
- [ ] Slide speaker notes area
- [ ] Slide number display

### 4.3 Block Editor — Slash Commands
- [ ] Slash command palette: opens on typing `/`
- [ ] Slash command: search/filter by typing after `/`
- [ ] Slash command: keyboard navigation (up/down arrows)
- [ ] Slash command: select with Enter
- [ ] Slash command: dismiss with Escape
- [ ] Slash command: "Paragraph" option
- [ ] Slash command: "Heading 1" option
- [ ] Slash command: "Heading 2" option
- [ ] Slash command: "Heading 3" option
- [ ] Slash command: "Bulleted List" option
- [ ] Slash command: "Numbered List" option
- [ ] Slash command: "To-do List" option
- [ ] Slash command: "Toggle List" option
- [ ] Slash command: "Quote" option
- [ ] Slash command: "Divider" option
- [ ] Slash command: "Code" option
- [ ] Slash command: "Image" option
- [ ] Slash command: "Table" option
- [ ] Slash command: "Embed" option
- [ ] Slash command: "Callout" option
- [ ] Slash command: "Math Equation" option
- [ ] Slash command: "Sticky Note" option
- [ ] Slash command: "AI Write" option
- [ ] Slash command: "Slide" option
- [ ] Slash command: "Chart" option
- [ ] Slash command: "File Attachment" option
- [ ] Slash command: "Table of Contents" option
- [ ] Slash command: "Columns" option (2-column, 3-column layout)
- [ ] Slash command: category grouping (Basic, Media, Advanced, AI)
- [ ] Slash command: recently used items at top
- [ ] Slash command: keyboard shortcut hints per item

### 4.4 Block Editor — Inline Formatting
- [ ] Bold text: `Cmd+B` / `**text**`
- [ ] Italic text: `Cmd+I` / `*text*`
- [ ] Underline text: `Cmd+U`
- [ ] Strikethrough text: `Cmd+Shift+S` / `~~text~~`
- [ ] Inline code: `Cmd+E` / `` `text` ``
- [ ] Text color picker
- [ ] Text background/highlight color picker
- [ ] Superscript
- [ ] Subscript
- [ ] Inline link: `Cmd+K` — create/edit/remove
- [ ] Inline link: auto-detect URLs on paste
- [ ] Inline link: open in new tab
- [ ] Inline link: link preview tooltip
- [ ] Inline mention: `@` to mention users
- [ ] Inline mention: autocomplete dropdown
- [ ] Inline mention: notification to mentioned user
- [ ] Inline page link: `@` to link other documents
- [ ] Inline page link: autocomplete with document search
- [ ] Inline comment: highlight text and add comment
- [ ] Inline comment: comment indicator in margin
- [ ] Inline comment: reply to comment
- [ ] Inline comment: resolve comment
- [ ] Inline comment: delete comment
- [ ] Inline comment: edit comment
- [ ] Floating formatting toolbar on text selection
- [ ] Floating toolbar: positioned above selection
- [ ] Floating toolbar: all formatting options available

### 4.5 Block Editor — Block Operations
- [ ] Block drag-and-drop reordering
- [ ] Block drag handle (left side of block)
- [ ] Block drag: visual drop indicator
- [ ] Block drag: smooth animation
- [ ] Block selection: click to select single block
- [ ] Block selection: Shift+click for range selection
- [ ] Block selection: Cmd+click for multi-select
- [ ] Block multi-select: change type of selected blocks
- [ ] Block multi-select: delete selected blocks
- [ ] Block multi-select: indent/outdent selected blocks
- [ ] Block copy (Cmd+C)
- [ ] Block cut (Cmd+X)
- [ ] Block paste (Cmd+V)
- [ ] Block duplicate (Cmd+D)
- [ ] Block delete (Backspace at start, or Delete)
- [ ] Block turn into (convert block type)
- [ ] Block move up (Cmd+Shift+Up)
- [ ] Block move down (Cmd+Shift+Down)
- [ ] Block color/background change
- [ ] Block add comment
- [ ] Block context menu (right-click)
- [ ] Undo: `Cmd+Z` — undo last action (50+ levels)
- [ ] Redo: `Cmd+Shift+Z` — redo
- [ ] Undo/redo stack persistence per session

### 4.6 Block Editor — Keyboard Shortcuts
- [ ] `Cmd+B` — Bold
- [ ] `Cmd+I` — Italic
- [ ] `Cmd+U` — Underline
- [ ] `Cmd+E` — Inline code
- [ ] `Cmd+K` — Insert/edit link
- [ ] `Cmd+Z` — Undo
- [ ] `Cmd+Shift+Z` — Redo
- [ ] `Cmd+D` — Duplicate block
- [ ] `Cmd+Shift+Up` — Move block up
- [ ] `Cmd+Shift+Down` — Move block down
- [ ] `Cmd+Enter` — Create new block below
- [ ] `Cmd+Shift+Enter` — Create new block above
- [ ] `Tab` — Indent list item / move to next cell
- [ ] `Shift+Tab` — Outdent list item / move to previous cell
- [ ] `Cmd+/` — Toggle slash command
- [ ] `Cmd+Shift+1` — Heading 1
- [ ] `Cmd+Shift+2` — Heading 2
- [ ] `Cmd+Shift+3` — Heading 3
- [ ] `Cmd+Shift+4` — Bulleted list
- [ ] `Cmd+Shift+5` — Numbered list
- [ ] `Cmd+Shift+6` — To-do list
- [ ] `Cmd+Shift+7` — Code block
- [ ] `Cmd+Shift+8` — Quote
- [ ] `Cmd+Shift+9` — Toggle list
- [ ] `Cmd+S` — Manual save
- [ ] `Cmd+P` — Print / export PDF
- [ ] `Cmd+\` — Toggle sidebar
- [ ] `Cmd+Shift+F` — Full-screen mode
- [ ] `Escape` — Deselect / close menus
- [ ] Keyboard shortcut overlay: `Cmd+/` or `?`

### 4.7 Block Editor — Auto-save & Status
- [ ] Auto-save: debounced 1s after last keystroke
- [ ] Auto-save: save on focus loss (blur)
- [ ] Auto-save: save on route navigation
- [ ] Save indicator: "Saved" state
- [ ] Save indicator: "Saving..." state with spinner
- [ ] Save indicator: "Unsaved changes" state
- [ ] Save indicator: "Error saving" state with retry
- [ ] Save indicator: last saved timestamp
- [ ] Offline detection: show offline banner
- [ ] Offline queue: buffer changes locally
- [ ] Offline sync: replay queued changes on reconnect
- [ ] Conflict detection: warn if another user changed the same block

### 4.8 Collaboration Features
- [ ] Real-time collaborative editing with Yjs
- [ ] WebSocket connection for Yjs sync
- [ ] Cursor presence: show remote user cursors
- [ ] Cursor labels: name badge next to each cursor
- [ ] Cursor colors: unique color per collaborator
- [ ] User presence bar: show who's currently viewing
- [ ] User presence: online/away/offline status
- [ ] CRDT-based conflict resolution (Yjs)
- [ ] Offline editing: local buffer with CRDT merge
- [ ] Reconnection: auto-reconnect WebSocket on disconnect
- [ ] Reconnection: exponential backoff
- [ ] Reconnection: merge local changes with server state

### 4.9 Version History
- [ ] Version history panel: accessible from toolbar
- [ ] Version history: auto-save versions every hour
- [ ] Version history: manual named versions ("Version 1.0")
- [ ] Version history: list all versions with timestamps
- [ ] Version history: version author name
- [ ] Version history: version comment/description
- [ ] Version diff: side-by-side comparison
- [ ] Version diff: inline diff with additions/deletions highlighted
- [ ] Version diff: block-level diffing
- [ ] Version restore: restore document to selected version
- [ ] Version restore: confirmation dialog before restore
- [ ] Version branching: create branch from version
- [ ] Version history: search versions by date or name
- [ ] Version history: pagination for many versions

### 4.10 Templates
- [ ] Template gallery: browse available templates
- [ ] Template gallery: categories (Meeting notes, Project brief, Report, etc.)
- [ ] Template gallery: search templates
- [ ] Template gallery: preview template before using
- [ ] Template creation: save current document as template
- [ ] Template creation: name and description
- [ ] Template creation: category assignment
- [ ] Template application: create new document from template
- [ ] Built-in templates: Meeting Notes
- [ ] Built-in templates: Project Brief
- [ ] Built-in templates: Weekly Report
- [ ] Built-in templates: Product Requirements Document
- [ ] Built-in templates: Design Spec
- [ ] Built-in templates: Bug Report
- [ ] Built-in templates: One-on-One Agenda
- [ ] Built-in templates: Sprint Retrospective
- [ ] Built-in templates: Technical RFC
- [ ] Built-in templates: Blank Document
- [ ] Custom templates: user-created templates
- [ ] Template sharing: share templates with workspace

### 4.11 Export
- [ ] Export to PDF
- [ ] Export to PDF: page size options (A4, Letter)
- [ ] Export to PDF: margin options
- [ ] Export to PDF: header/footer options
- [ ] Export to PDF: include/exclude images
- [ ] Export to PDF: progress indicator
- [ ] Export to DOCX (Microsoft Word)
- [ ] Export to DOCX: formatting preservation
- [ ] Export to Markdown (.md)
- [ ] Export to Markdown: GitHub-flavored markdown
- [ ] Export to HTML
- [ ] Export to HTML: styled or clean HTML option
- [ ] Export to plain text (.txt)
- [ ] Export to JSON (structured blocks)
- [ ] Sheets export to CSV
- [x] Sheets: export to CSV (implemented)
- [ ] Sheets export to Excel (.xlsx)
- [ ] Bulk export: export multiple documents at once
- [ ] Export download notification

### 4.12 Import
- [ ] Import from Markdown (.md)
- [ ] Import from DOCX (Microsoft Word)
- [ ] Import from HTML
- [ ] Import from plain text (.txt)
- [ ] Import from Google Docs (paste)
- [ ] Import from Notion export (JSON/MD)
- [ ] Import: drag-and-drop file to import
- [ ] Import: preview before confirming
- [ ] Import: progress indicator
- [ ] Import: error handling with details

### 4.13 Sheets (Spreadsheet View)
- [x] Grid: column headers (A, B, C, ...) and row numbers
- [x] Grid: multi-sheet tabs at bottom
- [x] Cell editing: double-click to edit
- [x] Cell editing: text, numbers, dates
- [x] Multi-cell select with click-drag
- [x] Multi-cell bulk delete
- [x] Export to CSV
- [ ] Formula support: basic arithmetic (`=A1+B1`)
- [ ] Formula support: `SUM(range)`
- [ ] Formula support: `AVERAGE(range)`
- [ ] Formula support: `COUNT(range)`
- [ ] Formula support: `MIN(range)` / `MAX(range)`
- [ ] Formula support: `IF(condition, true, false)`
- [ ] Formula support: `VLOOKUP(value, range, col, exact)`
- [ ] Formula support: `CONCATENATE(...)` / `&` operator
- [ ] Formula support: cell references (relative and absolute `$A$1`)
- [ ] Formula support: cross-sheet references (`Sheet2!A1`)
- [ ] Formula bar: display/edit current cell formula
- [ ] Cell formatting: bold text
- [ ] Cell formatting: italic text
- [ ] Cell formatting: text alignment (left/center/right)
- [ ] Cell formatting: background color
- [ ] Cell formatting: text color
- [ ] Cell formatting: number format (decimal places)
- [ ] Cell formatting: currency format
- [ ] Cell formatting: percentage format
- [ ] Cell formatting: date format
- [ ] Column operations: insert column left/right
- [ ] Column operations: delete column
- [ ] Column operations: resize column width (drag)
- [ ] Column operations: auto-fit column width
- [ ] Column operations: hide/show column
- [ ] Column operations: sort ascending/descending
- [ ] Column operations: filter by value
- [ ] Row operations: insert row above/below
- [ ] Row operations: delete row
- [ ] Row operations: resize row height (drag)
- [ ] Row operations: hide/show row
- [ ] Row operations: freeze rows (keep header visible on scroll)
- [ ] Column operations: freeze columns
- [ ] Cell merge: merge selected cells
- [ ] Cell merge: unmerge cells
- [ ] Copy/paste: copy cells
- [ ] Copy/paste: cut cells
- [ ] Copy/paste: paste cells
- [ ] Copy/paste: paste from Excel/Google Sheets
- [ ] Fill handle: drag to auto-fill series
- [ ] Undo/redo for all sheet operations
- [ ] Sheet operations: add new sheet
- [ ] Sheet operations: rename sheet
- [ ] Sheet operations: delete sheet (with confirmation)
- [ ] Sheet operations: duplicate sheet
- [ ] Sheet operations: reorder sheets (drag tabs)
- [ ] Import CSV into sheet
- [ ] Import Excel (.xlsx) into sheet
- [ ] Conditional formatting: highlight cells based on rules
- [ ] Charts: create chart from selected data
- [ ] Charts: bar chart
- [ ] Charts: line chart
- [ ] Charts: pie chart
- [ ] Charts: scatter plot
- [ ] Find and replace in sheet (`Cmd+F`)
- [ ] Print sheet / export to PDF
- [ ] Collaborative editing in sheets (multi-user)
- [ ] Cell comments: add comment to cell
- [ ] Cell validation: restrict input type per column

### 4.14 Split Editor
- [ ] Split editor: side-by-side view of two documents
- [ ] Split editor: vertical split
- [ ] Split editor: horizontal split
- [ ] Split editor: resize split pane (drag divider)
- [ ] Split editor: independent scrolling per pane
- [ ] Split editor: toggle split mode on/off
- [ ] Split editor: open different document in each pane
- [ ] Split editor: copy blocks between panes

### 4.15 Infinite Canvas
- [ ] Infinite canvas: zoomable workspace
- [ ] Infinite canvas: pan with mouse drag
- [ ] Infinite canvas: zoom with scroll wheel
- [ ] Infinite canvas: zoom controls (zoom in/out/fit)
- [ ] Infinite canvas: place document blocks as cards
- [ ] Infinite canvas: place sticky notes
- [ ] Infinite canvas: draw connections between cards
- [ ] Infinite canvas: freehand drawing tool
- [ ] Infinite canvas: shape tools (rectangle, circle, arrow)
- [ ] Infinite canvas: text annotations
- [ ] Infinite canvas: color/style options for shapes
- [ ] Infinite canvas: grid snap option
- [ ] Infinite canvas: minimap navigation
- [ ] Infinite canvas: export canvas as image

### 4.16 Knowledge Graph
- [ ] Knowledge graph: visualize document relationships
- [ ] Knowledge graph: nodes represent documents
- [ ] Knowledge graph: edges represent links/references between documents
- [ ] Knowledge graph: interactive node dragging
- [ ] Knowledge graph: zoom and pan
- [ ] Knowledge graph: click node to open document
- [ ] Knowledge graph: search/filter nodes
- [ ] Knowledge graph: cluster by folder/tag
- [ ] Knowledge graph: relationship type labels on edges
- [ ] Knowledge graph: node size based on link count
- [ ] Knowledge graph: highlight connected nodes on hover
- [ ] Knowledge graph: add relationships from graph view

### 4.17 AI Writing Assistant
- [ ] AI assistant panel: accessible from toolbar
- [ ] AI assistant: "Continue writing" — generate next paragraph
- [ ] AI assistant: "Summarize" — summarize selected text
- [ ] AI assistant: "Expand" — elaborate on selected text
- [ ] AI assistant: "Simplify" — simplify complex text
- [ ] AI assistant: "Fix grammar" — correct grammar and spelling
- [ ] AI assistant: "Change tone" — formal/casual/friendly/professional
- [ ] AI assistant: "Translate" — translate selected text
- [ ] AI assistant: "Explain" — explain technical concept
- [ ] AI assistant: "Generate outline" — create document outline
- [ ] AI assistant: "Brainstorm" — generate ideas
- [ ] AI assistant: "Write from prompt" — generate content from description
- [ ] AI assistant: streaming response display
- [ ] AI assistant: accept/reject generated content
- [ ] AI assistant: edit before accepting
- [ ] AI assistant: undo AI changes
- [ ] AI assistant: keyboard shortcut to invoke (`Cmd+J`)
- [ ] AI assistant: context-aware (uses surrounding blocks)
- [ ] AI assistant: token/usage display

### 4.18 AI Lasso
- [ ] AI lasso: select region of document with lasso tool
- [ ] AI lasso: visual selection outline
- [ ] AI lasso: action menu after selection (summarize, rewrite, etc.)
- [ ] AI lasso: apply AI action to selected region
- [ ] AI lasso: preview changes before applying
- [ ] AI lasso: undo lasso changes

### 4.19 Presentations/Slides
- [ ] Presentation mode: enter full-screen presentation
- [ ] Presentation mode: navigate slides with arrow keys
- [ ] Presentation mode: slide counter (current/total)
- [ ] Presentation mode: presenter notes panel (on second screen)
- [ ] Presentation mode: pointer/laser tool
- [ ] Presentation mode: slide transitions
- [ ] Presentation mode: exit with Escape
- [ ] Slide editor: visual slide builder
- [ ] Slide editor: drag-and-drop elements on slide
- [ ] Slide editor: text boxes with rich formatting
- [ ] Slide editor: image placement
- [ ] Slide editor: shape tools
- [ ] Slide editor: slide background options (color, gradient, image)
- [ ] Slide editor: master/template layouts
- [ ] Slide editor: slide sorter view (thumbnail grid)
- [ ] Slide editor: reorder slides with drag-and-drop
- [ ] Slide editor: duplicate/delete slides
- [ ] Export slides to PDF
- [ ] Export slides to PPTX
- [ ] Collaborative slide editing

### 4.20 Table of Contents
- [ ] Auto-generated table of contents from headings
- [ ] Table of contents: update on heading changes
- [ ] Table of contents: click to jump to heading
- [ ] Table of contents: collapsible/expandable
- [ ] Table of contents: sidebar widget
- [ ] Table of contents: depth level configuration (H1 only, H1-H2, H1-H3)
- [ ] Table of contents: highlight current section on scroll

### 4.21 Find and Replace
- [ ] Find: `Cmd+F` opens search bar
- [ ] Find: highlight all matches in document
- [ ] Find: navigate between matches (next/previous)
- [ ] Find: match count display
- [ ] Find: case-sensitive toggle
- [ ] Find: whole word toggle
- [ ] Find: regex toggle
- [ ] Replace: replace current match
- [ ] Replace: replace all matches
- [ ] Replace: preview replacements
- [ ] Find: close with Escape

### 4.22 Print
- [ ] Print preview (Cmd+P)
- [ ] Print: page size selection
- [ ] Print: margin configuration
- [ ] Print: header/footer options
- [ ] Print: page break control
- [ ] Print: hide UI elements (toolbar, sidebar)

### 4.23 Document Properties & Metadata
- [ ] Document title: inline editing
- [ ] Document icon/emoji: picker
- [ ] Document cover image: upload/select
- [ ] Document description/subtitle
- [ ] Document tags: add/remove/create tags
- [ ] Document author: display and edit
- [ ] Document created date
- [ ] Document modified date
- [ ] Document word count
- [ ] Document character count
- [ ] Document reading time estimate
- [ ] Document language setting
- [ ] Document sharing permissions

---

## 5. API Integration

### 5.1 Frontend API Layer
- [ ] Centralized API client (`writerApi` in `utils/api.ts`)
- [ ] All API calls use auth token from localStorage
- [ ] `X-Workspace-Id` header on all requests
- [ ] `X-Org-Id` header on all requests
- [ ] `Authorization: Bearer <token>` header on all requests
- [ ] Token refresh interceptor (401 -> refresh -> retry)
- [ ] Error handling: parse backend error messages
- [ ] Error handling: show user-friendly error toasts
- [ ] Request timeout configuration (30s default)
- [ ] Request retry logic (3 retries with exponential backoff)
- [ ] Request cancellation on component unmount (AbortController)
- [ ] Loading state management per request
- [ ] Optimistic updates for quick-save operations

### 5.2 Document Endpoints
- [ ] `GET /api/documents` — list documents (with pagination)
- [ ] `GET /api/documents?limit=24` — paginated document list
- [ ] `GET /api/documents/:id` — get single document
- [ ] `POST /api/documents` — create document
- [ ] `PUT /api/documents/:id` — update document (title, etc.)
- [ ] `DELETE /api/documents/:id` — delete document
- [ ] `POST /api/documents/:id/duplicate` — duplicate document
- [ ] `POST /api/documents/:id/archive` — archive document
- [ ] `POST /api/documents/:id/restore` — restore from archive
- [ ] `GET /api/documents/search?q=term` — search documents
- [ ] `GET /api/documents/recent` — recent documents
- [ ] `GET /api/documents/favorites` — favorite documents
- [ ] `POST /api/documents/:id/favorite` — toggle favorite
- [ ] `GET /api/documents/shared` — shared documents
- [ ] `POST /api/documents/:id/share` — share document

### 5.3 Block Endpoints
- [ ] `GET /api/documents/:id/blocks` — list blocks for document
- [ ] `POST /api/documents/:id/blocks` — create block
- [ ] `PUT /api/blocks/:id` — update block content
- [ ] `DELETE /api/blocks/:id` — delete block
- [ ] `PUT /api/blocks/:id/move` — reorder/move block
- [ ] `POST /api/blocks/:id/duplicate` — duplicate block
- [ ] `GET /api/blocks/:id/versions` — block version history
- [ ] `POST /api/blocks/:id/relations` — create block relation
- [ ] `GET /api/blocks/:id/relations` — list block relations
- [ ] `DELETE /api/block-relations/:id` — delete block relation

### 5.4 Version Endpoints
- [ ] `GET /api/documents/:id/versions` — list document versions
- [ ] `POST /api/documents/:id/versions` — create named version
- [ ] `GET /api/versions/:id` — get specific version
- [ ] `POST /api/versions/:id/restore` — restore to version
- [ ] `GET /api/versions/:id/diff` — diff between versions

### 5.5 Collaboration Endpoints
- [ ] `WebSocket /ws/documents/:id` — collaborative editing room
- [ ] WebSocket: Yjs sync protocol
- [ ] WebSocket: presence updates (cursor position, user info)
- [ ] WebSocket: auto-reconnect with exponential backoff
- [ ] WebSocket: connection status indicator

### 5.6 File Upload Endpoints
- [ ] `POST /api/uploads` — upload file (image, attachment)
- [ ] `POST /api/uploads` — multipart/form-data support
- [ ] `GET /api/uploads/:id` — download/serve file
- [ ] File upload: progress tracking
- [ ] File upload: size limit validation (client-side)
- [ ] File upload: type validation (client-side)

### 5.7 Template Endpoints
- [ ] `GET /api/templates` — list templates
- [ ] `POST /api/templates` — create template from document
- [ ] `GET /api/templates/:id` — get template
- [ ] `DELETE /api/templates/:id` — delete template
- [ ] `POST /api/templates/:id/apply` — create document from template

### 5.8 Export Endpoints
- [ ] `POST /api/documents/:id/export/pdf` — export to PDF
- [ ] `POST /api/documents/:id/export/docx` — export to DOCX
- [ ] `POST /api/documents/:id/export/md` — export to Markdown
- [ ] `POST /api/documents/:id/export/html` — export to HTML

### 5.9 AI Endpoints
- [ ] `POST /api/ai/generate` — generate content from prompt
- [ ] `POST /api/ai/summarize` — summarize text
- [ ] `POST /api/ai/rewrite` — rewrite text
- [ ] `POST /api/ai/grammar` — fix grammar
- [ ] `POST /api/ai/translate` — translate text
- [ ] AI endpoints: streaming response (SSE)
- [ ] AI endpoints: token usage tracking

### 5.10 EventBus Integration
- [ ] Publish event on document creation
- [ ] Publish event on document update
- [ ] Publish event on document deletion
- [ ] Publish event on document sharing
- [ ] Publish event on comment creation
- [ ] EventBus event format matches Orbit standard

---

## 6. State Management

### 6.1 Zustand Store Architecture
- [ ] Create `useDocumentStore` — document list and selection state
- [ ] Create `useEditorStore` — editor state (blocks, selection, formatting)
- [ ] Create `useSheetsStore` — spreadsheet state (cells, formulas, selection)
- [ ] Create `useCollaborationStore` — real-time presence state
- [ ] Create `useUIStore` — UI state (sidebar, panels, modals)
- [ ] Create `useSettingsStore` — user settings and preferences

### 6.2 Document Store
- [ ] State: `documents[]` — list of all documents
- [ ] State: `currentDocument` — currently open document
- [ ] State: `loading` — loading state
- [ ] State: `error` — error state
- [ ] State: `searchQuery` — current search term
- [ ] State: `sortBy` — current sort field
- [ ] State: `sortOrder` — asc/desc
- [ ] State: `filterStatus` — status filter
- [ ] State: `viewMode` — grid/list
- [ ] Action: `fetchDocuments()`
- [ ] Action: `createDocument()`
- [ ] Action: `updateDocument()`
- [ ] Action: `deleteDocument()`
- [ ] Action: `duplicateDocument()`
- [ ] Action: `searchDocuments(query)`
- [ ] Action: `toggleFavorite(docId)`
- [ ] Selector: `filteredDocuments` — computed filtered/sorted list

### 6.3 Editor Store
- [ ] State: `blocks[]` — all blocks in current document
- [ ] State: `selectedBlockId` — currently selected block
- [ ] State: `activeFormatting` — current inline formatting state
- [ ] State: `undoStack[]` — undo history
- [ ] State: `redoStack[]` — redo history
- [ ] State: `isSaving` — save in progress
- [ ] State: `lastSavedAt` — last save timestamp
- [ ] State: `isDirty` — unsaved changes flag
- [ ] Action: `addBlock(type, position)`
- [ ] Action: `updateBlock(blockId, content)`
- [ ] Action: `deleteBlock(blockId)`
- [ ] Action: `moveBlock(blockId, newPosition)`
- [ ] Action: `selectBlock(blockId)`
- [ ] Action: `undo()`
- [ ] Action: `redo()`
- [ ] Action: `save()`

### 6.4 Sheets Store
- [ ] State: `sheets[]` — all sheets in workbook
- [ ] State: `activeSheetId` — currently active sheet
- [ ] State: `selectedCell` — current cell coordinates
- [ ] State: `selectedRange` — current selection range
- [ ] State: `editingCell` — cell being edited
- [ ] State: `clipboardCells` — cut/copied cells
- [ ] Action: `updateCell(row, col, value)`
- [ ] Action: `selectCell(row, col)`
- [ ] Action: `selectRange(startRow, startCol, endRow, endCol)`
- [ ] Action: `addRow(position)`
- [ ] Action: `addColumn(position)`
- [ ] Action: `deleteRow(index)`
- [ ] Action: `deleteColumn(index)`
- [ ] Action: `addSheet(name)`
- [ ] Action: `deleteSheet(sheetId)`
- [ ] Action: `renameSheet(sheetId, name)`

### 6.5 Collaboration Store
- [ ] State: `connectedUsers[]` — users in current document
- [ ] State: `remoteCursors{}` — cursor positions per user
- [ ] State: `connectionStatus` — connected/disconnected/reconnecting
- [ ] Action: `updateCursor(position)`
- [ ] Action: `addUser(user)`
- [ ] Action: `removeUser(userId)`

### 6.6 State Persistence
- [ ] Persist sidebar collapsed state to localStorage
- [ ] Persist view mode (grid/list) to localStorage
- [ ] Persist sort preferences to localStorage
- [ ] Persist workspace ID to localStorage
- [ ] Persist theme preference to localStorage
- [ ] Persist recent documents list to localStorage
- [ ] Persist editor preferences (font size, line spacing) to localStorage

---

## 7. Performance

### 7.1 Bundle & Loading
- [ ] Route-level code splitting: Dashboard lazy loaded
- [ ] Route-level code splitting: Document editor lazy loaded
- [ ] Route-level code splitting: Sheets lazy loaded
- [ ] Route-level code splitting: Templates lazy loaded
- [ ] Route-level code splitting: Presentations lazy loaded
- [ ] Route-level code splitting: Infinite Canvas lazy loaded
- [ ] Route-level code splitting: Knowledge Graph lazy loaded
- [ ] Suspense fallback with skeleton for each route
- [ ] Bundle size audit: tree-shake unused dependencies
- [ ] Bundle analyzer: verify no duplicate dependencies
- [ ] Preload critical routes on idle
- [ ] First meaningful paint < 1.5s on fast 3G

### 7.2 Editor Performance
- [ ] Block renderer: only re-render changed blocks (`React.memo`)
- [ ] Block renderer: stable keys for block list
- [ ] Virtual scroll for documents with 500+ blocks
- [ ] Lazy load code block syntax highlighter (dynamic import)
- [ ] Lazy load math equation renderer (dynamic import)
- [ ] Lazy load image blocks (intersection observer)
- [ ] Lazy load embed blocks (intersection observer)
- [ ] Debounce auto-save (1000ms)
- [ ] Debounce search input (300ms)
- [ ] Throttle cursor position broadcasts (100ms)
- [ ] Memoize block tree computation
- [ ] Memoize table of contents generation
- [ ] Batch block updates (group multiple changes)

### 7.3 Sheets Performance
- [ ] Virtual scroll for large sheets (1000+ rows)
- [ ] Only render visible cells in viewport
- [ ] Lazy compute formulas (recalculate only affected cells)
- [ ] Memoize formula results (cache until dependency changes)
- [ ] Web Worker for heavy formula computation
- [ ] Batch cell update operations

### 7.4 Network Performance
- [ ] HTTP request caching (SWR/React Query or custom cache)
- [ ] Document list: cache and revalidate on focus
- [ ] Image CDN with responsive sizes (srcset)
- [ ] WebSocket connection pooling
- [ ] Compress WebSocket messages
- [ ] Gzip/Brotli compression for API responses

### 7.5 Memory Management
- [ ] Clean up WebSocket connections on component unmount
- [ ] Clean up event listeners on unmount
- [ ] Clean up Yjs providers on unmount
- [ ] Limit undo/redo stack size (100 entries max)
- [ ] Garbage collect unused block data

---

## 8. Accessibility (WCAG 2.1 AA)

### 8.1 Global Accessibility
- [ ] Skip-to-main-content link at top of page
- [ ] Landmark regions: header, nav, main, aside, footer
- [ ] Page titles update per route (`<title>` tag)
- [ ] Language attribute on `<html>` element
- [ ] Visible focus indicators on all interactive elements
- [ ] Focus indicators meet 3:1 contrast ratio
- [ ] No content relies solely on color to convey meaning
- [ ] Text resizable up to 200% without loss of content

### 8.2 Editor Accessibility
- [ ] Editor region: `role="textbox"` with `aria-multiline="true"`
- [ ] Editor region: `aria-label="Document editor"`
- [ ] Block list: `role="list"` with `role="listitem"` per block
- [ ] Block focus: navigate between blocks with arrow keys
- [ ] Block focus: Enter to edit block content
- [ ] Block focus: Escape to exit block editing
- [ ] Toolbar: `role="toolbar"` with `aria-label`
- [ ] Toolbar buttons: all have `aria-label` or visible text
- [ ] Toolbar buttons: `aria-pressed` for toggle buttons (bold, italic)
- [ ] Slash command menu: `role="listbox"` with `aria-activedescendant`
- [ ] Slash command menu: `aria-expanded` on trigger
- [ ] Inline formatting toolbar: `role="toolbar"`
- [ ] Drag-and-drop: keyboard alternative (cut/paste blocks)
- [ ] Block type change: screen reader announces new type
- [ ] Save status: `aria-live="polite"` region for save indicator
- [ ] Error messages: `aria-live="assertive"` for errors

### 8.3 Form Accessibility
- [ ] All form inputs have associated `<label>` elements
- [ ] All form inputs have visible labels
- [ ] Required fields marked with `aria-required="true"`
- [ ] Error messages linked to inputs with `aria-describedby`
- [ ] Form validation errors announced to screen readers

### 8.4 Modal Accessibility
- [ ] All modals trap focus within modal
- [ ] All modals return focus to trigger on close
- [ ] All modals have `aria-modal="true"`
- [ ] All modals have `role="dialog"` or `role="alertdialog"`
- [ ] All modals have `aria-labelledby` pointing to title
- [ ] Close on Escape key
- [ ] Close on backdrop click (configurable)

### 8.5 Sheets Accessibility
- [ ] Sheets grid: `role="grid"` with `aria-label`
- [ ] Sheets cells: `role="gridcell"`
- [ ] Sheets row headers: `role="rowheader"`
- [ ] Sheets column headers: `role="columnheader"`
- [ ] Arrow key navigation between cells
- [ ] Enter to edit cell, Escape to cancel
- [ ] Screen reader: announce cell value and position
- [ ] Screen reader: announce formula results

### 8.6 Image Accessibility
- [ ] All images have `alt` text
- [ ] Decorative images have `alt=""`
- [ ] Image upload prompt includes alt text field
- [ ] Image block: alt text editor accessible

### 8.7 Screen Reader Testing
- [ ] Test with VoiceOver (macOS)
- [ ] Test with NVDA (Windows)
- [ ] Test with JAWS (Windows)
- [ ] Verify all dynamic content updates are announced
- [ ] Verify heading structure is logical (no skipped levels)
- [ ] Verify link text is descriptive (no "click here")

---

## 9. Mobile & Responsive

### 9.1 Layout Responsiveness
- [ ] Mobile (< 640px): full-screen editor, sidebar hidden
- [ ] Mobile: hamburger menu to open sidebar
- [ ] Mobile: bottom sheet for sidebar on mobile
- [ ] Tablet (640-1024px): collapsible sidebar
- [ ] Desktop (> 1024px): persistent sidebar
- [ ] Editor: responsive padding/margins
- [ ] Document cards: responsive grid (1 col mobile, 2 col tablet, 3-4 col desktop)

### 9.2 Mobile Editor
- [ ] Mobile: floating toolbar on text selection (bottom of screen)
- [ ] Mobile: simplified toolbar with most-used actions
- [ ] Mobile: full toolbar accessible via "more" menu
- [ ] Mobile: touch-friendly block handles (larger hit area)
- [ ] Mobile: swipe to reveal block actions
- [ ] Mobile: long-press for context menu
- [ ] Mobile: pinch-to-zoom in canvas mode
- [ ] Mobile: scroll-based toolbar hide/show (hide on scroll down)
- [ ] Mobile: keyboard avoidance (editor scrolls above keyboard)

### 9.3 Mobile Sheets
- [ ] Mobile: horizontal scroll for wide sheets
- [ ] Mobile: touch-friendly cell selection
- [ ] Mobile: cell editing with on-screen keyboard
- [ ] Mobile: freeze header row on scroll
- [ ] Mobile: simplified column/row operations

### 9.4 Mobile Navigation
- [ ] Mobile: bottom tab navigation
- [ ] Mobile: swipe navigation between documents
- [ ] Mobile: pull-to-refresh on document list
- [ ] Mobile: back gesture support

### 9.5 Touch Interactions
- [ ] Touch: tap to select block
- [ ] Touch: double-tap to edit block
- [ ] Touch: long-press to start drag-and-drop
- [ ] Touch: pinch to zoom (canvas, slides)
- [ ] Touch: swipe gestures for undo/redo

### 9.6 Responsive Testing
- [ ] Test on iPhone 14 / 15 (Safari)
- [ ] Test on Samsung Galaxy S23 (Chrome)
- [ ] Test on iPad Air (Safari)
- [ ] Test on iPad Pro (Safari)
- [ ] Test on Galaxy Tab (Chrome)
- [ ] Test in Chrome DevTools responsive mode at all breakpoints

---

## 10. Internationalization

### 10.1 i18n Framework Setup
- [ ] Install and configure i18n library (react-intl or i18next)
- [ ] Set up translation file structure (`locales/en.json`, `locales/es.json`, etc.)
- [ ] Wrap app in i18n provider
- [ ] Configure default locale (English)
- [ ] Configure locale detection from browser settings
- [ ] Configure locale persistence (localStorage)
- [ ] Add language switcher in settings

### 10.2 UI String Extraction
- [ ] Extract all Dashboard UI strings to translation files
- [ ] Extract all Document editor UI strings to translation files
- [ ] Extract all Sheets UI strings to translation files
- [ ] Extract all Sidebar UI strings to translation files
- [ ] Extract all modal/dialog UI strings to translation files
- [ ] Extract all toolbar button labels to translation files
- [ ] Extract all menu item labels to translation files
- [ ] Extract all error messages to translation files
- [ ] Extract all success messages to translation files
- [ ] Extract all placeholder texts to translation files
- [ ] Extract all tooltip texts to translation files
- [ ] Extract all empty state messages to translation files

### 10.3 RTL Support
- [ ] Support `dir="rtl"` attribute on `<html>`
- [ ] Mirror layout for RTL languages (Arabic, Hebrew)
- [ ] Sidebar on right side for RTL
- [ ] Toolbar alignment for RTL
- [ ] Editor text direction for RTL
- [ ] Test with Arabic locale
- [ ] Test with Hebrew locale

### 10.4 Date & Number Formatting
- [ ] Use `Intl.DateTimeFormat` for all date displays
- [ ] Use `Intl.NumberFormat` for all number displays
- [ ] Currency formatting with locale
- [ ] Relative time formatting ("2 hours ago")
- [ ] Date picker: locale-aware month/day names
- [ ] Date picker: locale-aware first day of week

### 10.5 Content Localization
- [ ] Template names and descriptions translatable
- [ ] Built-in template content in multiple languages
- [ ] AI writing assistant: language-aware prompts
- [ ] Spell check: language-aware

---

## 11. Security

### 11.1 Authentication & Authorization
- [ ] All API requests include JWT Bearer token
- [ ] JWT token validation on backend
- [ ] JWT token expiration handling (auto-refresh)
- [ ] 401 response: redirect to login
- [ ] 403 response: show forbidden message
- [ ] Gate SSO integration for login
- [ ] Role-based access: document owner vs editor vs viewer
- [ ] Document sharing: permission levels (view, comment, edit, admin)
- [ ] API rate limiting per user
- [ ] Session timeout with warning

### 11.2 Data Protection
- [ ] XSS prevention: sanitize all user-generated HTML
- [ ] XSS prevention: sanitize block content before rendering
- [ ] XSS prevention: sanitize inline HTML in markdown
- [ ] CSRF protection on all state-changing requests
- [ ] Input validation: block content size limits
- [ ] Input validation: document title length limits
- [ ] Input validation: file upload type restrictions
- [ ] Input validation: file upload size limits (10MB default)
- [ ] Content Security Policy headers
- [ ] Embed iFrame: sandbox attribute for security
- [ ] Embed iFrame: only allow whitelisted domains
- [ ] No sensitive data in localStorage (only tokens)
- [ ] Clear sensitive data on logout

### 11.3 File Upload Security
- [ ] File type validation (server-side, not just extension)
- [ ] File size limit enforcement (server-side)
- [ ] Virus/malware scanning on uploaded files
- [ ] Signed URL for file access (time-limited)
- [ ] File storage isolation per workspace

### 11.4 Collaboration Security
- [ ] WebSocket authentication (JWT on upgrade)
- [ ] WebSocket authorization (verify document access)
- [ ] Rate limit WebSocket messages
- [ ] Validate all incoming WebSocket data
- [ ] Prevent unauthorized cursor position tracking

### 11.5 Backend Security
- [ ] SQL injection prevention (parameterized queries via SQLAlchemy)
- [ ] API input validation (Pydantic schemas)
- [ ] Org/workspace isolation on all queries
- [ ] Audit logging for all document operations
- [ ] Secrets not hardcoded (use environment variables)
- [ ] Database connection encryption (TLS)
- [ ] CORS: restrict allowed origins

---

## 12. Testing

### 12.1 Unit Tests — Frontend

#### Block Editor Logic
- [ ] Unit test: create paragraph block
- [ ] Unit test: create heading block (H1, H2, H3)
- [ ] Unit test: create bulleted list block
- [ ] Unit test: create numbered list block
- [ ] Unit test: create todo/checkbox list block
- [ ] Unit test: create code block
- [ ] Unit test: create image block
- [ ] Unit test: create table block
- [ ] Unit test: create embed block
- [ ] Unit test: create callout block
- [ ] Unit test: create divider block
- [ ] Unit test: block drag-and-drop reorder logic
- [ ] Unit test: block deletion
- [ ] Unit test: block duplication
- [ ] Unit test: block type conversion
- [ ] Unit test: undo/redo stack operations
- [ ] Unit test: auto-save debouncing logic

#### Slash Command
- [ ] Unit test: slash command menu opens on `/`
- [ ] Unit test: slash command filtering by text
- [ ] Unit test: slash command keyboard navigation
- [ ] Unit test: slash command selection creates correct block

#### Inline Formatting
- [ ] Unit test: bold toggle
- [ ] Unit test: italic toggle
- [ ] Unit test: underline toggle
- [ ] Unit test: strikethrough toggle
- [ ] Unit test: inline code toggle
- [ ] Unit test: link creation and editing
- [ ] Unit test: mention autocomplete

#### Sheets Logic
- [ ] Unit test: cell value update
- [ ] Unit test: cell selection (single)
- [ ] Unit test: cell range selection
- [ ] Unit test: formula parsing (SUM)
- [ ] Unit test: formula parsing (AVERAGE)
- [ ] Unit test: formula parsing (IF)
- [ ] Unit test: formula cell reference resolution
- [ ] Unit test: formula circular reference detection
- [ ] Unit test: column insert/delete
- [ ] Unit test: row insert/delete
- [ ] Unit test: sheet add/delete/rename
- [ ] Unit test: CSV export formatting
- [ ] Unit test: CSV import parsing

#### API Layer
- [ ] Unit test: `writerApi` function with success response
- [ ] Unit test: `writerApi` function with error response
- [ ] Unit test: `writerApi` function with auth headers
- [ ] Unit test: `writerApi` function with workspace header
- [ ] Unit test: `getWorkspaceId` returns correct value
- [ ] Unit test: `getAuthToken` returns correct value

#### Zustand Stores
- [ ] Unit test: document store — fetch documents
- [ ] Unit test: document store — create document
- [ ] Unit test: document store — delete document
- [ ] Unit test: document store — search filter
- [ ] Unit test: editor store — add block
- [ ] Unit test: editor store — update block
- [ ] Unit test: editor store — move block
- [ ] Unit test: editor store — undo/redo
- [ ] Unit test: sheets store — update cell
- [ ] Unit test: sheets store — add/delete sheet

### 12.2 Integration Tests — Frontend
- [ ] Integration: create document -> navigate to editor -> add blocks
- [ ] Integration: document list -> search -> open result
- [ ] Integration: editor -> add multiple block types -> save -> reload -> verify
- [ ] Integration: sheets -> add data -> calculate formula -> verify
- [ ] Integration: version history -> create version -> restore
- [ ] Integration: share document -> set permissions -> verify access
- [ ] Integration: export document -> download file -> verify content

### 12.3 E2E Tests (Playwright)
- [ ] E2E: login -> dashboard -> create document -> open editor
- [ ] E2E: editor -> type text -> bold -> save -> reload -> verify
- [ ] E2E: editor -> slash command -> create heading -> verify
- [ ] E2E: editor -> drag block -> reorder -> verify
- [ ] E2E: editor -> add image block -> upload -> verify
- [ ] E2E: editor -> add code block -> type code -> verify syntax highlighting
- [ ] E2E: sheets -> create sheet -> add data -> export CSV
- [ ] E2E: sheets -> add formula -> verify result
- [ ] E2E: dashboard -> search documents -> verify results
- [ ] E2E: dashboard -> delete document -> verify removal
- [ ] E2E: version history -> create version -> restore -> verify
- [ ] E2E: collaboration -> two sessions -> verify cursors visible
- [ ] E2E: mobile viewport -> verify responsive layout
- [ ] E2E: dark mode toggle -> verify theme applies

### 12.4 Visual Regression Tests
- [ ] Visual: dashboard document grid (light mode)
- [ ] Visual: dashboard document grid (dark mode)
- [ ] Visual: document editor with toolbar (light mode)
- [ ] Visual: document editor with toolbar (dark mode)
- [ ] Visual: sheets grid (light mode)
- [ ] Visual: sheets grid (dark mode)
- [ ] Visual: slash command menu (light mode)
- [ ] Visual: slash command menu (dark mode)
- [ ] Visual: inline formatting toolbar
- [ ] Visual: version history panel
- [ ] Visual: empty states (all variants)
- [ ] Visual: mobile layouts

### 12.5 Unit Tests — Backend
- [ ] Unit test: Document model CRUD operations
- [ ] Unit test: Block model CRUD operations
- [ ] Unit test: BlockRelation model operations
- [ ] Unit test: BlockVersion model operations
- [ ] Unit test: schema validation (DocumentCreate)
- [ ] Unit test: schema validation (BlockCreate)
- [ ] Unit test: schema validation (BlockUpdate)
- [ ] Unit test: auth token verification
- [ ] Unit test: workspace claim validation
- [ ] Unit test: org header validation
- [ ] Unit test: eventbus event publishing

### 12.6 Integration Tests — Backend
- [ ] Integration: POST /documents -> GET /documents -> verify
- [ ] Integration: POST /documents/:id/blocks -> GET blocks -> verify
- [ ] Integration: PUT /blocks/:id -> GET block -> verify update
- [ ] Integration: DELETE /blocks/:id -> GET blocks -> verify removal
- [ ] Integration: version creation on block update
- [ ] Integration: block relations CRUD
- [ ] Integration: document search
- [ ] Integration: pagination on all list endpoints
- [ ] Integration: auth middleware rejects invalid tokens
- [ ] Integration: workspace isolation (can't access other workspace docs)

### 12.7 Performance Tests
- [ ] Performance: document load time with 100 blocks
- [ ] Performance: document load time with 500 blocks
- [ ] Performance: document load time with 1000 blocks
- [ ] Performance: auto-save latency measurement
- [ ] Performance: sheets performance with 1000 rows
- [ ] Performance: sheets formula recalculation time
- [ ] Performance: bundle size < 500KB gzipped
- [ ] Performance: LCP < 2.5s
- [ ] Performance: FID < 100ms
- [ ] Performance: CLS < 0.1

---

## 13. Documentation

### 13.1 Code Documentation
- [ ] JSDoc comments on all exported functions
- [ ] JSDoc comments on all React components (props interface)
- [ ] JSDoc comments on all Zustand stores
- [ ] JSDoc comments on all utility functions
- [ ] Python docstrings on all FastAPI endpoints
- [ ] Python docstrings on all service functions
- [ ] Python docstrings on all model classes
- [ ] Inline comments for complex logic

### 13.2 API Documentation
- [ ] OpenAPI/Swagger auto-generated from FastAPI
- [ ] API documentation accessible at `/docs`
- [ ] All endpoints documented with request/response schemas
- [ ] All endpoints documented with example payloads
- [ ] Error response schemas documented
- [ ] Authentication requirements documented per endpoint
- [ ] WebSocket protocol documented

### 13.3 User Documentation
- [ ] Getting started guide for Writer
- [ ] Block types reference
- [ ] Keyboard shortcuts reference
- [ ] Sheets formulas reference
- [ ] Template usage guide
- [ ] Collaboration guide
- [ ] Export/import formats guide
- [ ] AI features guide

### 13.4 Developer Documentation
- [ ] README with setup instructions
- [ ] Architecture overview (frontend + backend)
- [ ] Data model diagram (Document, Block, BlockRelation, BlockVersion)
- [ ] State management architecture diagram
- [ ] WebSocket protocol documentation
- [ ] Contributing guidelines
- [ ] Environment variables reference

---

## 14. Deployment & CI/CD

### 14.1 Frontend Build
- [ ] Production build succeeds (`vite build`)
- [ ] No TypeScript errors in build
- [ ] No ESLint warnings in build
- [ ] Source maps generated for production debugging
- [ ] Build output optimized (minified, tree-shaken)
- [ ] Assets hashed for cache busting
- [ ] Environment variables injected at build time

### 14.2 Backend Build
- [ ] Python dependencies installable (`pip install -r requirements.txt`)
- [ ] Database migrations run successfully (`alembic upgrade head`)
- [ ] Health endpoint responds (`GET /health`)
- [ ] All tests pass in CI

### 14.3 CI Pipeline
- [ ] GitHub Actions workflow for frontend (lint, test, build)
- [ ] GitHub Actions workflow for backend (lint, test)
- [ ] Frontend lint step (ESLint)
- [ ] Frontend type check step (TypeScript)
- [ ] Frontend unit test step (Vitest)
- [ ] Frontend E2E test step (Playwright)
- [ ] Frontend build step
- [ ] Backend lint step (ruff)
- [ ] Backend type check step (mypy)
- [ ] Backend unit test step (pytest)
- [ ] Backend integration test step (pytest)
- [ ] Code coverage report generation
- [ ] Code coverage threshold enforcement (>80%)
- [ ] Bundle size check (fail if exceeds threshold)
- [ ] Dependency vulnerability scan
- [ ] PR preview deployments

### 14.4 Deployment
- [ ] Docker image for frontend (multi-stage build)
- [ ] Docker image for backend (multi-stage build)
- [ ] Docker Compose for local development
- [ ] Kubernetes manifests for production
- [ ] Health check endpoint for load balancer
- [ ] Graceful shutdown handling
- [ ] Environment-specific configuration (dev, staging, prod)
- [ ] Database migration on deployment
- [ ] Zero-downtime deployment strategy
- [ ] Rollback procedure documented

### 14.5 Monitoring
- [ ] Application error tracking (Sentry or equivalent)
- [ ] API response time monitoring
- [ ] WebSocket connection monitoring
- [ ] Database query performance monitoring
- [ ] Frontend Core Web Vitals monitoring
- [ ] Uptime monitoring and alerting
- [ ] Log aggregation (structured JSON logs)

---

## 15. Backend

### 15.1 Database Schema
- [ ] `documents` table: id, workspace_id, title, root_block_id, created_at, updated_at
- [ ] `documents` table: index on (workspace_id, updated_at)
- [ ] `blocks` table: id, document_id, parent_block_id, type, content, metadata, position_index, version, created_at, updated_at
- [ ] `blocks` table: index on (document_id, parent_block_id, position_index)
- [ ] `block_relations` table: id, document_id, source_block_id, target_block_id, relation_type
- [ ] `block_versions` table: id, block_id, version, content, metadata, created_at
- [ ] `templates` table: id, workspace_id, name, description, category, content, created_at
- [ ] `comments` table: id, document_id, block_id, user_id, content, resolved, created_at
- [ ] `shares` table: id, document_id, user_id, permission_level, created_at
- [ ] `folders` table: id, workspace_id, parent_folder_id, name, created_at
- [ ] `document_folders` table: document_id, folder_id
- [ ] `favorites` table: user_id, document_id, created_at
- [ ] `tags` table: id, workspace_id, name, color
- [ ] `document_tags` table: document_id, tag_id
- [ ] Run initial migration (`0001_initial.py`) successfully

### 15.2 API Endpoints Implementation
- [ ] `GET /health` — health check with DB status
- [ ] `GET /api/documents` — list documents with pagination and filters
- [ ] `GET /api/documents/:id` — get document detail
- [ ] `POST /api/documents` — create document with initial block
- [ ] `PUT /api/documents/:id` — update document metadata
- [ ] `DELETE /api/documents/:id` — soft delete document
- [ ] `GET /api/documents/:id/blocks` — list blocks for document
- [ ] `POST /api/documents/:id/blocks` — create block in document
- [ ] `PUT /api/blocks/:id` — update block content
- [ ] `DELETE /api/blocks/:id` — delete block
- [ ] `PUT /api/blocks/:id/move` — move/reorder block
- [ ] `GET /api/blocks/:id/versions` — list block versions
- [ ] `POST /api/blocks/:id/relations` — create block relation
- [ ] `GET /api/blocks/:id/relations` — list block relations
- [ ] `DELETE /api/block-relations/:id` — delete block relation
- [ ] `GET /api/documents/:id/graph` — document knowledge graph data
- [ ] `POST /api/documents/:id/export/:format` — export document

### 15.3 Authentication & Middleware
- [ ] Gate token verification (`verify_gate_token`)
- [ ] Org header validation (`validate_org_header`)
- [ ] Workspace claim validation (`validate_workspace_claim`)
- [ ] CORS middleware configured
- [ ] Request logging middleware
- [ ] Rate limiting middleware
- [ ] Request ID middleware (for tracing)

### 15.4 EventBus Integration
- [ ] `publish_writer_event` function implemented
- [ ] Event: `document.created`
- [ ] Event: `document.updated`
- [ ] Event: `document.deleted`
- [ ] Event: `document.shared`
- [ ] Event: `block.created`
- [ ] Event: `block.updated`
- [ ] Event: `block.deleted`
- [ ] Event: `comment.created`
- [ ] Events include org_id, user_id, timestamp, entity data
- [ ] EventBus contract tests pass

### 15.5 Audit Logging
- [ ] Audit: document creation logged
- [ ] Audit: document update logged
- [ ] Audit: document deletion logged
- [ ] Audit: block creation logged
- [ ] Audit: block update logged
- [ ] Audit: block deletion logged
- [ ] Audit: sharing changes logged
- [ ] Audit records include: actor, action, entity_type, entity_id, timestamp, metadata
- [ ] Audit logger configured (`orbit.audit.writer`)

### 15.6 WebSocket Server
- [ ] WebSocket endpoint: `/ws/documents/:id`
- [ ] WebSocket: JWT authentication on upgrade
- [ ] WebSocket: Yjs sync protocol implementation
- [ ] WebSocket: presence updates (cursor, selection)
- [ ] WebSocket: room management (join/leave)
- [ ] WebSocket: heartbeat/ping-pong
- [ ] WebSocket: auto-disconnect on timeout
- [ ] WebSocket: max connections per document limit

### 15.7 File Storage
- [ ] MinIO/S3 integration for file uploads
- [ ] File upload: validate type and size
- [ ] File upload: generate unique filename
- [ ] File upload: store in workspace-scoped path
- [ ] File download: signed URL generation
- [ ] File deletion: clean up on document/block deletion
- [ ] Image processing: generate thumbnails
- [ ] Image processing: optimize file size

### 15.8 AI Integration
- [ ] AI service: integration with LLM provider
- [ ] AI service: streaming response support
- [ ] AI service: context extraction from document blocks
- [ ] AI service: rate limiting per user
- [ ] AI service: token usage tracking
- [ ] AI service: prompt templates for each operation
- [ ] AI service: error handling and fallbacks

### 15.9 Search
- [ ] Full-text search across document titles
- [ ] Full-text search across block content
- [ ] Search: relevance ranking
- [ ] Search: result highlighting
- [ ] Search: workspace scoping
- [ ] Search indexing (PostgreSQL full-text or Elasticsearch)

### 15.10 Background Tasks
- [ ] Version auto-creation (hourly snapshots)
- [ ] Document analytics aggregation
- [ ] File cleanup (orphaned uploads)
- [ ] Search index updates
- [ ] EventBus event publishing (async)

---

_End of Writer Checklist — Total items: 2000+_
