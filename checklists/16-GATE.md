# 16 Gate -- Authentication & Identity (AuthX)

> **Full-Name:** RM Orbit Gate (AuthX)
> **Purpose:** Central Authentication & Identity Service for all 16 RM Orbit apps (comparable to Auth0 / Keycloak)
> **Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, Redis, Alembic, Celery, Pydantic v2
> **Source:** `/Gate/authx/`
> **Backend:** `app/` -- main.py, api/v1/ (auth, oauth, mfa, oidc, users, admin, audit), services/, models/, schemas/, core/, middleware/
> **Status:** Backend ~80% complete, Admin Portal UI 0%, Developer Dashboard 0%
> **Last updated:** 2026-04-06
>
> Legend: `[x]` = done | `[ ]` = todo | `[~]` = in progress | `[-]` = N/A / skipped

---

## Table of Contents

1. [Project Setup & Configuration](#1-project-setup--configuration)
2. [Design System Integration (Admin UI)](#2-design-system-integration-admin-ui)
3. [Dark Mode (Admin UI)](#3-dark-mode-admin-ui)
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

### 1.1 Python Backend Setup
- [x] FastAPI application created (`app/main.py`)
- [x] Pydantic v2 settings with `BaseSettings` (`app/config.py`)
- [x] SQLAlchemy 2.0 async engine configured (`app/database.py`)
- [x] Alembic migrations directory (`alembic/`)
- [x] Initial migration: `001_initial_auth_schema_with_mfa.py`
- [x] Docker Compose for local development (`docker-compose.yml`)
- [x] `registered_apps.json` for pre-registered OAuth clients
- [x] Seed scripts: `seed_hmalla_gate.py`, `seed_hmalla_all.py`
- [x] Application registration script: `register_internal_apps.py`
- [ ] `pyproject.toml` or `requirements.txt` with pinned dependencies
- [ ] `Dockerfile` for production container
- [ ] `Dockerfile.dev` for development container
- [ ] `.dockerignore` file
- [ ] Python version specified (`.python-version`)
- [ ] Virtual environment setup instructions
- [ ] `Makefile` with common commands (install, run, test, lint, migrate)
- [ ] Pre-commit hooks configuration (`.pre-commit-config.yaml`)
- [ ] Ruff or Black formatter configuration
- [ ] Ruff or Flake8 linter configuration
- [ ] MyPy type checking configuration (`mypy.ini`)
- [ ] pytest configuration (`pytest.ini` or `pyproject.toml`)
- [ ] `.env.example` with all required environment variables
- [ ] `.env.development` with sensible defaults
- [ ] `.env.test` for test environment
- [ ] `.gitignore` covering `__pycache__`, `.env`, `*.pyc`, virtual envs

### 1.2 Environment Configuration
- [x] `APP_NAME` config (default: "AuthX")
- [x] `ENVIRONMENT` config with enum (development, staging, production, testing)
- [x] `DEBUG` config (auto-disabled in production)
- [x] `BASE_URL` config (default: http://localhost:8000)
- [x] `API_V1_PREFIX` config (default: /api/v1)
- [x] `ALLOWED_ORIGINS` config with CORS parsing
- [x] `DATABASE_URL` config with asyncpg driver
- [x] `DATABASE_POOL_SIZE` config (default: 20)
- [x] `DATABASE_MAX_OVERFLOW` config (default: 10)
- [x] `DATABASE_POOL_TIMEOUT` config (default: 30)
- [x] `REDIS_URL` config
- [x] `SECRET_KEY` config (auto-generated if not set)
- [x] `ENCRYPTION_KEY` config (Fernet 32-byte key)
- [x] `ALGORITHM` config (default: RS256)
- [x] `ACCESS_TOKEN_EXPIRE_MINUTES` config (default: 15)
- [x] `REFRESH_TOKEN_EXPIRE_DAYS` config (default: 30)
- [x] `SESSION_EXPIRE_HOURS` config (default: 24)
- [x] `PASSWORD_MIN_LENGTH` config (default: 12)
- [x] `PASSWORD_REQUIRE_UPPERCASE` config
- [x] `PASSWORD_REQUIRE_LOWERCASE` config
- [x] `PASSWORD_REQUIRE_DIGIT` config
- [x] `PASSWORD_REQUIRE_SPECIAL` config
- [x] `MAX_LOGIN_ATTEMPTS` config (default: 5)
- [x] `LOCKOUT_DURATION_MINUTES` config (default: 30)
- [x] `JWT_PRIVATE_KEY_PATH` and `JWT_PUBLIC_KEY_PATH` config
- [x] `JWT_PRIVATE_KEY` and `JWT_PUBLIC_KEY` config (auto-generated RSA 2048 in dev)
- [x] `TOTP_ISSUER` config
- [x] `TOTP_DIGITS` config (default: 6)
- [x] `TOTP_INTERVAL` config (default: 30s)
- [x] `TOTP_VALID_WINDOW` config (default: 1)
- [x] `BACKUP_CODES_COUNT` config (default: 10)
- [x] SMTP configuration (host, port, user, password, TLS, from address)
- [x] Twilio SMS configuration (SID, token, phone)
- [x] Firebase push notification configuration (FCM key, credentials path)
- [x] SAML certificate and key path configuration
- [x] Rate limit configuration (default, auth, MFA)
- [x] Sentry DSN configuration
- [x] GeoIP database path configuration

### 1.3 Database Setup
- [x] PostgreSQL with `asyncpg` driver
- [x] Connection pooling configured (pool_size, max_overflow, pool_timeout)
- [x] Schema namespace: `authx`
- [x] Database health check function (`check_db_health`)
- [x] Database repair function for indexes (`repair_users_email_lower_index`)
- [x] `get_db` dependency for request-scoped sessions
- [ ] Database connection retry on startup
- [ ] Database read replica support
- [ ] Database query logging in development
- [ ] Database slow query detection
- [ ] Database migration validation in CI
- [ ] Alembic autogenerate diff check in CI
- [ ] Database backup scheduled job
- [ ] Database connection pool monitoring

### 1.4 Redis Setup
- [x] Redis URL configuration
- [x] Redis used for token blacklisting
- [x] Redis used for rate limiting
- [ ] Redis connection pooling
- [ ] Redis health check endpoint
- [ ] Redis Sentinel or Cluster support for HA
- [ ] Redis key namespace prefixing (`authx:`)
- [ ] Redis key TTL policies documented
- [ ] Redis memory limits and eviction policy configured
- [ ] Redis persistence configuration (RDB/AOF)

### 1.5 Admin Portal Frontend Setup (To Be Built)
- [ ] Admin portal: Vite + React 19 + TypeScript project initialized
- [ ] Admin portal: `package.json` with dependencies
- [ ] Admin portal: `tsconfig.json` with strict mode
- [ ] Admin portal: `vite.config.ts` configured
- [ ] Admin portal: Tailwind CSS v3 or v4 configured
- [ ] Admin portal: orbit-ui preset imported
- [ ] Admin portal: React Router v6 configured
- [ ] Admin portal: Zustand state management
- [ ] Admin portal: Axios HTTP client configured
- [ ] Admin portal: ESLint + Prettier configured
- [ ] Admin portal: environment variables defined
- [ ] Admin portal: route structure planned
- [ ] Admin portal: authenticated routes with Gate session

### 1.6 Developer Dashboard Frontend Setup (To Be Built)
- [ ] Dev dashboard: Vite + React 19 + TypeScript project initialized
- [ ] Dev dashboard: `package.json` with dependencies
- [ ] Dev dashboard: `tsconfig.json` with strict mode
- [ ] Dev dashboard: Tailwind CSS configured with orbit preset
- [ ] Dev dashboard: React Router configured
- [ ] Dev dashboard: Zustand state management
- [ ] Dev dashboard: Axios HTTP client
- [ ] Dev dashboard: ESLint + Prettier configured
- [ ] Dev dashboard: environment variables defined

---

## 2. Design System Integration (Admin UI)

### 2.1 Admin Portal UI -- Orbit UI Core
- [ ] `@orbit-ui/react` installed as dependency
- [ ] `ThemeProvider` wraps root
- [ ] `ThemeToggle` in admin header
- [ ] `index.css` imports orbit-tokens.css
- [ ] Anti-FOUC script in index.html
- [ ] `tailwind.config.js` uses orbit preset
- [ ] All color tokens used (no hardcoded colors)
- [ ] All typography tokens used
- [ ] All spacing tokens used
- [ ] All shadow tokens used
- [ ] All border-radius tokens used

### 2.2 Admin Portal -- Orbit UI Component Adoption
- [ ] `<Button>` for all actions (primary, secondary, danger, ghost)
- [ ] `<Input>` for all form fields
- [ ] `<Select>` for dropdowns (role select, status select)
- [ ] `<Badge>` for user status (active, suspended, locked, pending)
- [ ] `<Badge>` for role indicators (owner, admin, member, superadmin)
- [ ] `<Badge>` for MFA status (enabled, disabled, enforced)
- [ ] `<Table>` for user list, org list, audit log, session list
- [ ] `<Pagination>` for table pagination
- [ ] `<Modal>` for confirmations (delete user, revoke session)
- [ ] `<Modal>` for create/edit forms
- [ ] `<Alert>` for success/error/warning messages
- [ ] `<Toast>` for transient notifications
- [ ] `<Avatar>` for user avatars
- [ ] `<Card>` for dashboard stats and detail panels
- [ ] `<Tabs>` for detail views (user profile, org settings, audit)
- [ ] `<Tooltip>` for icon-only actions
- [ ] `<Dropdown>` for action menus (per-row actions)
- [ ] `<Skeleton>` for loading states
- [ ] `<Spinner>` for in-progress operations
- [ ] `<EmptyState>` for empty tables and search results
- [ ] `<Divider>` between sections
- [ ] `<Breadcrumb>` for navigation hierarchy
- [ ] `<Switch>` for boolean toggles (MFA enforced, active/disabled)
- [ ] `<Accordion>` for advanced settings sections

### 2.3 Developer Dashboard -- Orbit UI Component Adoption
- [ ] All components from Admin Portal list
- [ ] `<CodeBlock>` for displaying client secrets, API keys, JWTs
- [ ] `<Tabs>` for OAuth flow test panels
- [ ] `<Card>` for application cards
- [ ] `<Badge>` for application status
- [ ] `<Input>` for redirect URI management
- [ ] `<Select>` for grant type selection
- [ ] `<Textarea>` for webhook payload display

---

## 3. Dark Mode (Admin UI)

### 3.1 Admin Portal -- Login / Auth Pages
- [ ] Login page: dark mode background
- [ ] Login page: dark mode form card
- [ ] Login page: dark mode input fields
- [ ] Login page: dark mode labels and helper text
- [ ] Login page: dark mode error messages
- [ ] Login page: dark mode submit button
- [ ] Login page: dark mode logo and branding
- [ ] Login page: dark mode "forgot password" link
- [ ] Login page: dark mode footer text
- [ ] Support page: dark mode form
- [ ] Support page: dark mode success state
- [ ] Password reset page: dark mode
- [ ] Email verification page: dark mode
- [ ] MFA challenge page: dark mode

### 3.2 Admin Portal -- Dashboard
- [ ] Dashboard: dark mode stat cards
- [ ] Dashboard: dark mode charts/graphs
- [ ] Dashboard: dark mode recent activity feed
- [ ] Dashboard: dark mode system health indicators
- [ ] Dashboard: dark mode quick action buttons

### 3.3 Admin Portal -- User Management Pages
- [ ] User list: dark mode table (header, rows, alternating colors)
- [ ] User list: dark mode search bar
- [ ] User list: dark mode status badges
- [ ] User list: dark mode action buttons
- [ ] User list: dark mode pagination
- [ ] User list: dark mode empty state
- [ ] User detail: dark mode profile card
- [ ] User detail: dark mode sessions list
- [ ] User detail: dark mode MFA devices list
- [ ] User detail: dark mode audit log entries
- [ ] User detail: dark mode edit form
- [ ] User detail: dark mode status toggle
- [ ] Create user modal: dark mode form
- [ ] Reset password modal: dark mode

### 3.4 Admin Portal -- Organization Management Pages
- [ ] Org list: dark mode table
- [ ] Org list: dark mode search bar
- [ ] Org list: dark mode badges
- [ ] Org list: dark mode action buttons
- [ ] Org list: dark mode pagination
- [ ] Org detail: dark mode info card
- [ ] Org detail: dark mode member list
- [ ] Org detail: dark mode settings form
- [ ] Org detail: dark mode policy configuration
- [ ] Create org modal: dark mode
- [ ] Org invite members modal: dark mode
- [ ] Org roles configuration: dark mode

### 3.5 Admin Portal -- OAuth Client Management
- [ ] Client list: dark mode table
- [ ] Client detail: dark mode info panel
- [ ] Client detail: dark mode redirect URIs list
- [ ] Client detail: dark mode secret display (masked)
- [ ] Client create/edit form: dark mode
- [ ] Rotate secret confirmation: dark mode

### 3.6 Admin Portal -- Token & Key Management
- [ ] Token inspector: dark mode input field
- [ ] Token inspector: dark mode decoded JWT display
- [ ] Token inspector: dark mode claims table
- [ ] Token inspector: dark mode validation result
- [ ] JWKS viewer: dark mode key display
- [ ] JWKS key rotation confirmation: dark mode

### 3.7 Admin Portal -- Audit Log
- [ ] Audit log list: dark mode table
- [ ] Audit log: dark mode filter controls (date range, action, status)
- [ ] Audit log: dark mode search bar
- [ ] Audit log: dark mode detail panel
- [ ] Audit log: dark mode export button
- [ ] Audit log: dark mode pagination
- [ ] Audit log: dark mode status badges (success/failure)

### 3.8 Admin Portal -- Session Management
- [ ] Session list: dark mode table
- [ ] Session detail: dark mode device info
- [ ] Session detail: dark mode location info
- [ ] Session detail: dark mode revoke button
- [ ] Bulk revoke confirmation: dark mode

### 3.9 Admin Portal -- MFA Management
- [ ] MFA enrollment list: dark mode table
- [ ] MFA device detail: dark mode
- [ ] Force MFA enrollment modal: dark mode
- [ ] Disable MFA confirmation: dark mode

### 3.10 Admin Portal -- Shell / Layout
- [ ] Admin sidebar: dark mode
- [ ] Admin header: dark mode
- [ ] Admin footer: dark mode
- [ ] Admin breadcrumbs: dark mode
- [ ] Admin loading states: dark mode
- [ ] Admin error pages (403, 404, 500): dark mode
- [ ] Admin settings page: dark mode

### 3.11 Developer Dashboard Dark Mode
- [ ] App list: dark mode
- [ ] App detail: dark mode
- [ ] OAuth flow tester: dark mode
- [ ] API key display: dark mode
- [ ] Webhook configuration: dark mode
- [ ] Quick start embed: dark mode
- [ ] Code examples: dark mode code blocks
- [ ] Request/response viewer: dark mode

### 3.12 Server-Rendered Login Pages Dark Mode
- [ ] Jinja2 login template: dark mode support via CSS class toggle
- [ ] Jinja2 support template: dark mode
- [ ] Jinja2 templates: orbit-tokens CSS imported
- [ ] Jinja2 templates: anti-FOUC script
- [ ] Jinja2 templates: theme toggle button

---

## 4. Core Features

### 4.1 User Registration
- [x] `POST /api/v1/auth/register` endpoint
- [x] Rate limited: 5/minute
- [x] Input: email, password, username, first_name, last_name
- [x] Input: organization_id (optional, join existing org)
- [x] Input: enrollment_type (optional)
- [x] Input: organization_name, organization_slug, organization_domain (create new org)
- [x] Password hashing with bcrypt
- [x] User status set to `pending_verification` on creation
- [x] Response: `UserResponse` (201 Created)
- [x] Error: 400 on duplicate email or invalid input
- [ ] Email validation: RFC 5322 compliant regex
- [ ] Email validation: disposable email domain rejection
- [ ] Email validation: MX record check
- [ ] Password validation: minimum length enforcement (12 chars)
- [ ] Password validation: uppercase requirement
- [ ] Password validation: lowercase requirement
- [ ] Password validation: digit requirement
- [ ] Password validation: special character requirement
- [ ] Password validation: common password dictionary check
- [ ] Password validation: HaveIBeenPwned API check (k-anonymity)
- [ ] Username validation: allowed characters (alphanumeric, underscore, hyphen)
- [ ] Username validation: minimum length (3 chars)
- [ ] Username validation: maximum length (150 chars)
- [ ] Username validation: reserved word check (admin, root, system)
- [ ] CAPTCHA verification on registration (hCaptcha or reCAPTCHA)
- [ ] Registration email confirmation sent automatically
- [ ] Welcome email sent after verification
- [ ] Registration webhook event emitted
- [ ] Registration audit log entry created
- [ ] Invite-only registration mode (org admin sends invite link)
- [ ] Self-service organization creation during registration
- [ ] Terms of Service acceptance checkbox tracked

### 4.2 User Login
- [x] `POST /api/v1/auth/login` endpoint
- [x] Rate limited: 10/minute
- [x] Input: username (email), password
- [x] Returns `LoginResponse` with access_token, refresh_token, expires_in
- [x] Returns MFA challenge if MFA enabled (mfa_required, mfa_token, mfa_methods)
- [x] Error: 401 on invalid credentials
- [x] Error: 403 on locked/suspended account
- [x] Client IP extraction from `X-Forwarded-For` header
- [x] User-Agent captured
- [x] Server-rendered login page (`GET /login`, Jinja2 template)
- [x] Server-rendered login form submission (`POST /login`)
- [x] Session cookie set on successful form login
- [ ] Account lockout after MAX_LOGIN_ATTEMPTS failed attempts
- [ ] Lockout duration: LOCKOUT_DURATION_MINUTES (30 min default)
- [ ] Lockout: reset failed attempts on successful login
- [ ] Lockout: admin can manually unlock
- [ ] Email notification on successful login from new device
- [ ] Email notification on successful login from new location
- [ ] Email notification on account lockout
- [ ] Login audit log entry: success with IP, user-agent, country
- [ ] Login audit log entry: failure with IP, user-agent, reason
- [ ] Login: check email_verified before allowing login
- [ ] Login: remember me option (extends refresh token lifetime)
- [ ] Login: CAPTCHA after 3 failed attempts
- [ ] Login: adaptive MFA (policy engine triggers MFA on risk)
- [ ] Login: device fingerprinting
- [ ] Login: login history endpoint (list recent logins)

### 4.3 Token Management
- [x] Access token: JWT with RS256 signing
- [x] Access token: claims include sub, iat, exp, nbf, jti, iss, type
- [x] Access token: additional claims support (org_id, roles, permissions)
- [x] Access token: default expiry 15 minutes
- [x] Refresh token: JWT with RS256 signing
- [x] Refresh token: claims include sub, iat, exp, jti, iss, type
- [x] Refresh token: default expiry 30 days
- [x] ID token: JWT for OIDC (sub, iss, aud, iat, exp, auth_time, nonce)
- [x] MFA token: short-lived JWT (5 min) for MFA challenge step
- [x] `POST /api/v1/auth/token/refresh` endpoint
- [x] Token manager: `issue_tokens()` method
- [x] Token manager: `rotate_refresh_token()` method (blacklists old, issues new)
- [x] Token manager: `revoke_token()` method (blacklist in Redis with TTL)
- [x] Token manager: `is_blacklisted()` check (Redis lookup by hash)
- [x] `POST /api/v1/auth/revoke` endpoint
- [x] Token decode: validates signature, issuer, expiry, and type
- [ ] Token: access token expiry configurable per client application
- [ ] Token: refresh token rotation enforced (single-use refresh tokens)
- [ ] Token: refresh token family tracking (detect token reuse attacks)
- [ ] Token: on token reuse detected, revoke entire family
- [ ] Token: token binding (bind to client IP or device)
- [ ] Token: audience claim (`aud`) validation per client
- [ ] Token: scope claim enforcement
- [ ] Token: custom claims per organization
- [ ] Token: token metadata endpoint (list active tokens for user)
- [ ] Token: bulk revocation (revoke all tokens for user)
- [ ] Token: revocation event notification to dependent services

### 4.4 Session Management
- [x] Session model: `UserSession` in database
- [x] `GET /api/v1/auth/sessions` -- list active sessions for user
- [x] `DELETE /api/v1/auth/sessions/{session_id}` -- revoke specific session
- [x] `POST /api/v1/auth/logout` -- revoke current session
- [x] `POST /api/v1/auth/logout/all` -- revoke all sessions
- [x] `GET /api/v1/users/me/sessions` -- list own sessions
- [x] `DELETE /api/v1/users/me/sessions/{session_id}` -- revoke own session
- [x] Session cookie set on server-rendered login
- [x] Logout: delete session cookie (`GET /logout`)
- [ ] Session: store IP address per session
- [ ] Session: store user agent per session
- [ ] Session: store device type (desktop, mobile, tablet)
- [ ] Session: store browser name and version
- [ ] Session: store OS name and version
- [ ] Session: store country/city from GeoIP
- [ ] Session: last active timestamp updated on API use
- [ ] Session: idle timeout (expire if no activity for N hours)
- [ ] Session: absolute timeout (max session duration)
- [ ] Session: concurrent session limit per user (configurable)
- [ ] Session: "This is you" indicator for current session
- [ ] Session: push notification to user when session created on new device

### 4.5 Password Management
- [x] `POST /api/v1/auth/password/forgot` -- request password reset email
- [x] `POST /api/v1/auth/password/reset` -- reset password with token
- [x] `PUT /api/v1/auth/password/change` -- change password (authenticated)
- [x] Forgot password: rate limited 5/minute
- [x] Reset password: rate limited 10/minute
- [x] Forgot password: "If account exists" response (timing-safe)
- [x] Password hashing: bcrypt with cost factor 12
- [ ] Password reset token: secure random, single-use
- [ ] Password reset token: expiry (1 hour)
- [ ] Password reset token: hashed in database (not stored plaintext)
- [ ] Password reset: invalidate all sessions after reset
- [ ] Password change: verify current password before change
- [ ] Password change: invalidate other sessions after change
- [ ] Password change: email notification sent
- [ ] Password history: prevent reuse of last N passwords
- [ ] Password expiry: configurable per organization
- [ ] Password expiry: force change on next login
- [ ] Password strength meter: zxcvbn scoring
- [ ] Password: breached password check (HaveIBeenPwned)

### 4.6 Email Verification
- [x] `POST /api/v1/auth/verify-email` endpoint
- [x] Input: verification token
- [x] Success response: "Email verified successfully"
- [x] Error: 400 on invalid/expired token
- [ ] Verification email: sent on registration
- [ ] Verification email: resend endpoint
- [ ] Verification email: rate limited (1 per 5 minutes)
- [ ] Verification token: secure random, single-use
- [ ] Verification token: expiry (24 hours)
- [ ] Verification token: hashed in database
- [ ] Verification: update user status from `pending_verification` to `active`
- [ ] Verification: audit log entry
- [ ] Verification: block login until verified (configurable per org)

### 4.7 OAuth2 Authorization Server

#### 4.7.1 Authorization Endpoint
- [x] `GET /api/v1/oauth/authorize` endpoint
- [x] Input: response_type, client_id, redirect_uri, scope, state, nonce
- [x] Input: code_challenge, code_challenge_method (PKCE)
- [x] Redirect to login if user not authenticated (via cookie check)
- [x] Return redirect with authorization code on success
- [x] Error: 400 on invalid client or redirect URI
- [ ] Authorization: consent screen (show requested scopes)
- [ ] Authorization: remember consent (skip screen on subsequent logins)
- [ ] Authorization: deny button (redirect with error=access_denied)
- [ ] Authorization: scope validation against client's allowed scopes
- [ ] Authorization: redirect_uri validation (exact match or pattern)
- [ ] Authorization: code lifetime (10 minutes max)
- [ ] Authorization: code single-use enforcement
- [ ] Authorization: state parameter validation (CSRF protection)

#### 4.7.2 Token Endpoint
- [x] `POST /api/v1/oauth/token` endpoint
- [x] Grant type: `authorization_code` with PKCE code_verifier
- [x] Grant type: `refresh_token`
- [x] Input: grant_type, code, redirect_uri, client_id, client_secret, code_verifier
- [x] Returns: access_token, refresh_token, id_token (OIDC), expires_in, token_type
- [x] Error: 400 with `invalid_grant` error description
- [ ] Grant type: `client_credentials` (machine-to-machine)
- [ ] Client authentication: `client_secret_post` (form body)
- [ ] Client authentication: `client_secret_basic` (Authorization header)
- [ ] Client authentication: `private_key_jwt`
- [ ] PKCE: code_challenge_method S256 enforced for public clients
- [ ] PKCE: minimum entropy validation on code_verifier (43-128 chars)
- [ ] Token endpoint: audience parameter support
- [ ] Token endpoint: scope downscoping on refresh

#### 4.7.3 Token Revocation (RFC 7009)
- [x] `POST /api/v1/oauth/revoke` endpoint
- [x] Input: token, token_type_hint, client_id, client_secret
- [x] Always returns 200 (per spec)
- [ ] Revocation: validate client owns the token
- [ ] Revocation: cascade revoke (revoke refresh also revokes related access tokens)
- [ ] Revocation: notification to resource servers

#### 4.7.4 Token Introspection (RFC 7662)
- [x] `POST /api/v1/oauth/introspect` endpoint
- [x] Input: token, token_type_hint, client_id, client_secret
- [ ] Introspection: return active/inactive status
- [ ] Introspection: return token metadata (sub, scope, exp, iat, client_id)
- [ ] Introspection: validate requesting client is authorized to introspect
- [ ] Introspection: check blacklist
- [ ] Introspection: rate limited

#### 4.7.5 OAuth Client Management
- [x] `POST /api/v1/admin/applications` -- create OAuth application (superadmin)
- [x] Input: ApplicationCreate schema
- [x] Response: ApplicationWithSecret (includes generated secret)
- [ ] Client: list all applications
- [ ] Client: get application by ID
- [ ] Client: update application (name, redirect URIs, scopes)
- [ ] Client: delete application (soft delete)
- [ ] Client: rotate client secret
- [ ] Client: client types (public, confidential)
- [ ] Client: allowed grant types per client
- [ ] Client: allowed scopes per client
- [ ] Client: allowed redirect URIs per client
- [ ] Client: token lifetime overrides per client
- [ ] Client: CORS origin whitelist per client
- [ ] Client: rate limit overrides per client
- [ ] Client: logo URL for consent screen
- [ ] Client: Terms of Service URL
- [ ] Client: Privacy Policy URL
- [ ] Client: client_credentials grant scope restrictions

### 4.8 OpenID Connect (OIDC)

#### 4.8.1 Discovery
- [x] `GET /.well-known/openid-configuration` (root level)
- [x] `GET /api/v1/oidc/.well-known/openid-configuration` (API level)
- [x] Discovery: issuer
- [x] Discovery: authorization_endpoint
- [x] Discovery: token_endpoint
- [x] Discovery: userinfo_endpoint
- [x] Discovery: jwks_uri
- [x] Discovery: revocation_endpoint
- [x] Discovery: introspection_endpoint
- [x] Discovery: registration_endpoint
- [x] Discovery: scopes_supported (openid, profile, email, phone, address, offline_access)
- [x] Discovery: response_types_supported (code, token, id_token, code id_token)
- [x] Discovery: grant_types_supported (authorization_code, refresh_token, client_credentials)
- [x] Discovery: subject_types_supported (public)
- [x] Discovery: id_token_signing_alg_values_supported (RS256)
- [x] Discovery: token_endpoint_auth_methods_supported
- [x] Discovery: claims_supported (full list including org_id, org_role, roles, permissions)
- [x] Discovery: code_challenge_methods_supported (S256, plain)
- [ ] Discovery: end_session_endpoint
- [ ] Discovery: check_session_iframe
- [ ] Discovery: backchannel_logout_supported
- [ ] Discovery: frontchannel_logout_supported

#### 4.8.2 JWKS Endpoint
- [x] `GET /api/v1/oidc/jwks` endpoint
- [x] Returns RSA public key in JWK format
- [x] JWK: kty, use, alg, kid, n, e fields
- [x] kid: derived from SHA-256 hash of public key
- [ ] JWKS: multiple keys support (for rotation)
- [ ] JWKS: key rotation endpoint (generate new key, keep old for validation)
- [ ] JWKS: key rotation: new tokens signed with new key
- [ ] JWKS: key rotation: old key kept for grace period
- [ ] JWKS: cache headers (max-age for clients to cache)
- [ ] JWKS: EC key support (ES256) in addition to RSA

#### 4.8.3 UserInfo Endpoint
- [x] `GET /api/v1/oidc/userinfo` endpoint
- [x] Requires Bearer token in Authorization header
- [x] Returns user info based on token scopes
- [x] Response model: OIDCUserInfo
- [ ] UserInfo: `openid` scope returns `sub`
- [ ] UserInfo: `profile` scope returns name, family_name, given_name, preferred_username, picture, locale, zoneinfo, updated_at
- [ ] UserInfo: `email` scope returns email, email_verified
- [ ] UserInfo: `phone` scope returns phone_number, phone_number_verified
- [ ] UserInfo: `address` scope returns address object
- [ ] UserInfo: custom claims (org_id, org_role, roles, permissions)
- [ ] UserInfo: POST method support (alternative to GET)

### 4.9 Multi-Factor Authentication (MFA)

#### 4.9.1 TOTP (Time-based One-Time Password)
- [x] `POST /api/v1/mfa/totp/enroll` -- enroll new TOTP device
- [x] Input: device_name
- [x] Response: TOTPEnrollResponse (secret, QR code URI, backup codes)
- [x] `POST /api/v1/mfa/totp/verify-enrollment` -- verify TOTP setup
- [x] Input: device_id, code
- [x] `POST /api/v1/mfa/totp/verify` -- verify TOTP during login
- [x] Input: mfa_token, code, device_id
- [x] Rate limited: 5/minute
- [x] Response: LoginResponse (tokens on success)
- [ ] TOTP: RFC 6238 compliance verified
- [ ] TOTP: secret generation (base32 encoded, 160-bit minimum)
- [ ] TOTP: QR code generation (otpauth:// URI)
- [ ] TOTP: valid window configurable (1 by default = current + 1 adjacent)
- [ ] TOTP: code reuse prevention (same code cannot be used twice)
- [ ] TOTP: multiple TOTP devices per user
- [ ] TOTP: device naming
- [ ] TOTP: device listing with last_used timestamp
- [ ] TOTP: device removal with re-authentication
- [ ] TOTP: encrypted secret storage (Fernet)

#### 4.9.2 SMS MFA
- [x] `POST /api/v1/mfa/sms/enroll` -- enroll SMS device
- [x] Input: phone_number, device_name
- [x] Response: device_id, "Verification code sent"
- [x] `POST /api/v1/mfa/sms/send` -- send SMS OTP during login
- [x] Input: mfa_token, device_id
- [x] `POST /api/v1/mfa/sms/verify` -- verify SMS code during login
- [x] Input: mfa_token, device_id, code
- [x] Rate limited: 5/minute
- [ ] SMS: OTP generation (6 digits)
- [ ] SMS: OTP expiry (5 minutes)
- [ ] SMS: OTP single-use
- [ ] SMS: Twilio integration for sending
- [ ] SMS: phone number validation (E.164 format)
- [ ] SMS: phone number verification during enrollment
- [ ] SMS: rate limit on send (max 5 SMS per hour)
- [ ] SMS: fallback to voice call
- [ ] SMS: encrypted phone number storage
- [ ] SMS: country code validation

#### 4.9.3 Push Notification MFA
- [x] `POST /api/v1/mfa/push/send` -- send push challenge
- [x] Input: mfa_token, device_id
- [x] Response: challenge_id, status, expires_in (120s)
- [x] `POST /api/v1/mfa/push/respond` -- approve/deny from mobile
- [x] Input: challenge_token, approved (boolean)
- [x] `GET /api/v1/mfa/push/status/{challenge_token}` -- poll status
- [ ] Push: Firebase Cloud Messaging (FCM) integration
- [ ] Push: Apple Push Notification Service (APNs) support
- [ ] Push: challenge expiry (2 minutes)
- [ ] Push: challenge single-use
- [ ] Push: display login details in push (IP, location, browser)
- [ ] Push: deny with report (flag suspicious attempt)
- [ ] Push: number matching (display random number, user confirms on phone)

#### 4.9.4 Backup Codes
- [x] `POST /api/v1/mfa/backup/verify` -- use backup code during login
- [x] Input: mfa_token, code
- [x] Rate limited: 5/minute
- [x] Response: LoginResponse on success
- [ ] Backup codes: generate N codes on MFA enrollment (10 by default)
- [ ] Backup codes: each code is single-use
- [ ] Backup codes: codes hashed in database (not stored plaintext)
- [ ] Backup codes: regenerate codes endpoint
- [ ] Backup codes: show remaining count to user
- [ ] Backup codes: warning when few remaining (< 3)
- [ ] Backup codes: email notification when backup code used
- [ ] Backup codes: all codes invalidated on MFA re-enrollment
- [ ] Backup codes: format: XXXX-XXXX (8 alphanumeric chars)

#### 4.9.5 MFA Device Management
- [x] `GET /api/v1/mfa/devices` -- list enrolled MFA devices
- [x] `DELETE /api/v1/mfa/devices/{device_id}` -- remove MFA device
- [x] Response: MFADeviceResponse model
- [ ] Device management: require re-authentication to remove device
- [ ] Device management: prevent removing last MFA device if MFA enforced
- [ ] Device management: device types (totp, sms, push, webauthn)
- [ ] Device management: set default/preferred device
- [ ] Device management: last_used_at timestamp per device
- [ ] Device management: created_at timestamp per device
- [ ] Device management: admin can view user's MFA enrollment status

#### 4.9.6 WebAuthn / Passkeys
- [ ] WebAuthn: registration ceremony endpoint
- [ ] WebAuthn: authentication ceremony endpoint
- [ ] WebAuthn: platform authenticator support (Touch ID, Windows Hello)
- [ ] WebAuthn: roaming authenticator support (YubiKey)
- [ ] WebAuthn: credential storage (public key, credential ID, sign count)
- [ ] WebAuthn: resident key support (passkeys)
- [ ] WebAuthn: attestation validation
- [ ] WebAuthn: multiple credentials per user

### 4.10 Magic Link (Passwordless)
- [ ] Magic link: `POST /api/v1/auth/magic-link` -- request magic link
- [ ] Magic link: email sent with one-time login URL
- [ ] Magic link: token generation (secure random, 64 chars)
- [ ] Magic link: token expiry (15 minutes)
- [ ] Magic link: token single-use
- [ ] Magic link: token hashed in database
- [ ] Magic link: `GET /api/v1/auth/magic-link/verify?token=X` -- verify and login
- [ ] Magic link: rate limited (3 per 15 minutes)
- [ ] Magic link: IP/device binding (optional)
- [ ] Magic link: redirect to original destination after login
- [ ] Magic link: audit log entry

### 4.11 Social SSO

#### 4.11.1 Google OAuth SSO
- [ ] Google: OAuth2 client registration
- [ ] Google: authorization URL construction
- [ ] Google: callback endpoint
- [ ] Google: token exchange
- [ ] Google: user profile fetch
- [ ] Google: account linking (connect Google to existing account)
- [ ] Google: auto-registration on first login (configurable)
- [ ] Google: email domain restriction (only allow company domain)
- [ ] Google: Google Workspace SSO support
- [ ] Google: profile picture sync
- [ ] Google: ID token verification (Google's JWKS)

#### 4.11.2 GitHub OAuth SSO
- [ ] GitHub: OAuth2 client registration
- [ ] GitHub: authorization URL construction
- [ ] GitHub: callback endpoint
- [ ] GitHub: token exchange
- [ ] GitHub: user profile fetch (including email from /user/emails)
- [ ] GitHub: account linking
- [ ] GitHub: auto-registration
- [ ] GitHub: organization membership check
- [ ] GitHub: team membership check

#### 4.11.3 Microsoft Entra SSO
- [ ] Microsoft: OAuth2/OIDC client registration
- [ ] Microsoft: authorization URL with tenant ID
- [ ] Microsoft: callback endpoint
- [ ] Microsoft: token exchange
- [ ] Microsoft: user profile fetch (Microsoft Graph)
- [ ] Microsoft: account linking
- [ ] Microsoft: auto-registration
- [ ] Microsoft: tenant restriction (single-tenant vs multi-tenant)
- [ ] Microsoft: group/role mapping from Azure AD groups

#### 4.11.4 Social SSO General
- [ ] SSO: provider configuration in database (not hardcoded)
- [ ] SSO: admin UI to configure providers (client ID, secret, scopes)
- [ ] SSO: state parameter with CSRF protection
- [ ] SSO: nonce parameter for OIDC providers
- [ ] SSO: account linking UI (user can connect/disconnect providers)
- [ ] SSO: handle email conflicts (same email from different providers)
- [ ] SSO: JIT (Just-In-Time) provisioning
- [ ] SSO: configurable per organization

### 4.12 SAML 2.0
- [ ] SAML: SP metadata generation endpoint
- [ ] SAML: SP metadata: entity ID, ACS URL, SLO URL, certificate
- [ ] SAML: IdP-initiated SSO (receive SAML response)
- [ ] SAML: SP-initiated SSO (send SAML request)
- [ ] SAML: SAML response validation (signature, conditions, assertions)
- [ ] SAML: attribute mapping (email, name, groups, roles)
- [ ] SAML: NameID format support (emailAddress, persistent, transient)
- [ ] SAML: relay state support
- [ ] SAML: Single Logout (SLO) support
- [ ] SAML: certificate management (upload IdP cert, rotate SP cert)
- [ ] SAML: multiple IdP support per organization
- [ ] SAML: admin UI for SAML configuration
- [ ] SAML: SAML metadata import from IdP URL
- [ ] SAML: signed authentication requests
- [ ] SAML: encrypted assertions support

### 4.13 SCIM 2.0 Provisioning
- [ ] SCIM: `GET /scim/v2/Users` -- list users
- [ ] SCIM: `GET /scim/v2/Users/{id}` -- get user
- [ ] SCIM: `POST /scim/v2/Users` -- create user
- [ ] SCIM: `PUT /scim/v2/Users/{id}` -- replace user
- [ ] SCIM: `PATCH /scim/v2/Users/{id}` -- update user
- [ ] SCIM: `DELETE /scim/v2/Users/{id}` -- deactivate user
- [ ] SCIM: `GET /scim/v2/Groups` -- list groups
- [ ] SCIM: `POST /scim/v2/Groups` -- create group
- [ ] SCIM: `PATCH /scim/v2/Groups/{id}` -- update group membership
- [ ] SCIM: `DELETE /scim/v2/Groups/{id}` -- delete group
- [ ] SCIM: `GET /scim/v2/ServiceProviderConfig` -- capabilities
- [ ] SCIM: `GET /scim/v2/Schemas` -- schema discovery
- [ ] SCIM: `GET /scim/v2/ResourceTypes` -- resource types
- [ ] SCIM: bearer token authentication for SCIM requests
- [ ] SCIM: pagination (startIndex, count, totalResults)
- [ ] SCIM: filtering (filter=userName eq "john@example.com")
- [ ] SCIM: error response format per SCIM spec
- [ ] SCIM: ETags for conflict detection
- [ ] SCIM: bulk operations endpoint

### 4.14 API Keys
- [ ] API keys: `POST /api/v1/auth/api-keys` -- generate API key
- [ ] API keys: `GET /api/v1/auth/api-keys` -- list API keys
- [ ] API keys: `DELETE /api/v1/auth/api-keys/{id}` -- revoke API key
- [ ] API keys: key format (prefix + random, e.g., `orbt_live_xxxx`)
- [ ] API keys: hashed storage (only shown once on creation)
- [ ] API keys: scopes/permissions per key
- [ ] API keys: expiry date (optional)
- [ ] API keys: last used timestamp
- [ ] API keys: rate limiting per key
- [ ] API keys: IP allowlist per key
- [ ] API keys: organization-scoped
- [ ] API keys: audit log on creation, use, and revocation

### 4.15 Organization Management

#### 4.15.1 Organization CRUD
- [x] `POST /api/v1/admin/organizations` -- create org (superadmin)
- [x] `GET /api/v1/admin/organizations` -- list orgs (superadmin)
- [x] `PATCH /api/v1/admin/organizations/{org_id}` -- update org (superadmin)
- [x] `DELETE /api/v1/admin/organizations/{org_id}` -- delete org (superadmin)
- [x] Organization model: id, name, slug, domain, metadata, created_at, updated_at
- [x] Organization: slug uniqueness validation
- [x] Organization: search by name or domain
- [x] Organization: pagination
- [ ] Organization: domain verification (DNS TXT record)
- [ ] Organization: multiple domains per org
- [ ] Organization: logo URL
- [ ] Organization: billing plan/tier
- [ ] Organization: seat limit enforcement
- [ ] Organization: audit log per organization

#### 4.15.2 Organization Membership
- [x] User model: `organization_id` field
- [x] `POST /api/v1/admin/organizations/{org_id}/bulk-onboard` -- bulk create users
- [ ] Membership: invite user to org (send email invitation)
- [ ] Membership: accept/decline invitation
- [ ] Membership: remove user from org
- [ ] Membership: transfer ownership
- [ ] Membership: list org members with roles
- [ ] Membership: role assignment (owner, admin, member, readonly)
- [ ] Membership: role change requires admin or owner
- [ ] Membership: maximum members per org (configurable)

#### 4.15.3 Organization Policies
- [ ] Policy: require MFA for all members
- [ ] Policy: require SSO for all members
- [ ] Policy: password complexity overrides
- [ ] Policy: session duration overrides
- [ ] Policy: IP allowlist for org
- [ ] Policy: country/geo-blocking for org
- [ ] Policy: allowed authentication methods (password, SSO, magic link)
- [ ] Policy: data residency region
- [ ] Policy: custom branding (logo, colors on login page)

### 4.16 Role-Based Access Control (RBAC)

#### 4.16.1 Role System
- [x] Predefined roles: owner, admin, member, readonly, superadmin
- [x] Role permissions mapping (`core/roles.py`)
- [x] `owner` permissions: org.manage, org.members.manage, apps.manage, identity.read, identity.write
- [x] `admin` permissions: org.members.manage, apps.manage, identity.read, identity.write
- [x] `member` permissions: identity.read
- [x] `readonly` permissions: identity.read
- [x] `superadmin` permissions: `*` (wildcard)
- [x] `normalize_role()` utility
- [x] `primary_role()` utility with superadmin check
- [x] `effective_roles()` utility
- [x] `role_permissions()` utility
- [ ] Custom roles: create custom role with specific permissions
- [ ] Custom roles: assign custom role to user
- [ ] Custom roles: edit permissions of custom role
- [ ] Custom roles: delete custom role (reassign users first)
- [ ] Permission: fine-grained resource-level permissions
- [ ] Permission: scope-based permissions (per-app access)
- [ ] Permission: hierarchical roles (admin inherits member permissions)
- [ ] Permission: role claims in JWT
- [ ] Permission: middleware to check permissions on API endpoints
- [ ] Permission: UI-level permission checks (feature flags based on role)

#### 4.16.2 Admin Access Control
- [x] `require_superadmin` dependency (FastAPI)
- [x] `get_current_user` dependency
- [x] `get_current_user_id` dependency
- [x] `get_current_user_id_from_cookie` dependency (for OAuth flow)
- [ ] Admin: org-admin can manage their own org only
- [ ] Admin: superadmin can manage all orgs
- [ ] Admin: endpoint-level permission checks
- [ ] Admin: row-level security (users see only their org's data)

### 4.17 Audit Logging

#### 4.17.1 Audit Log Model & Storage
- [x] AuditLog model in database
- [x] AuditLog fields: id, action, user_id, user_email, ip_address, status, description, created_at
- [x] Audit logging middleware (`middleware/audit_logging.py`)
- [x] Middleware: auto-logs all auth and admin endpoints
- [x] Middleware: extracts user info from JWT
- [x] Middleware: captures IP, user-agent, duration
- [x] Middleware: determines action from request path and method
- [x] Middleware: determines resource type from path
- [x] Middleware: does not fail request if logging fails
- [x] Audit logger service (`services/audit_logger.py`)
- [x] Core audit logger (`core/audit_logger.py`)
- [ ] Audit log: organization_id field for org-scoped queries
- [ ] Audit log: resource_id field (which user/org was affected)
- [ ] Audit log: request_data (method, path, query params, sanitized body)
- [ ] Audit log: response_data (status code, error detail)
- [ ] Audit log: geo-location from IP
- [ ] Audit log: session ID reference
- [ ] Audit log: retention policy (auto-delete after N days)
- [ ] Audit log: immutable storage (append-only, no updates/deletes)
- [ ] Audit log: integrity verification (hash chain)

#### 4.17.2 Audit Log Querying
- [x] `GET /api/v1/admin/audit-logs` -- paginated log query (superadmin)
- [x] Filter: by user_id
- [x] Filter: by action
- [x] Filter: by status (success/failure)
- [x] Filter: by date range (start_date, end_date)
- [x] Response: paginated with total count
- [x] `GET /api/v1/admin/audit-logs/export` -- CSV export (superadmin)
- [x] `GET /api/v1/audit/export` -- CSV export per org
- [ ] Query: full-text search on description
- [ ] Query: filter by IP address
- [ ] Query: filter by resource type
- [ ] Query: filter by organization
- [ ] Query: sort by any field
- [ ] Export: JSON format option
- [ ] Export: streaming for large datasets
- [ ] Dashboard: audit log summary (top actions, failure rate, active users)

### 4.18 User Management (Admin)

#### 4.18.1 User CRUD
- [x] `GET /api/v1/admin/users` -- list users (superadmin)
- [x] Filter: by status
- [x] Filter: search by email or first name
- [x] Pagination: page, per_page
- [x] Sort: by created_at desc
- [x] Response: UserListResponse
- [x] `PATCH /api/v1/admin/users/{user_id}/status` -- update status (superadmin)
- [x] Status options: active, inactive, suspended, locked
- [x] Activate: clears locked_until and failed_login_attempts
- [x] `DELETE /api/v1/admin/users/{user_id}` -- soft delete (superadmin)
- [x] Soft delete: sets deleted_at and status=inactive
- [ ] Admin: create user endpoint
- [ ] Admin: update user profile (name, email, phone)
- [ ] Admin: force password reset
- [ ] Admin: force email verification
- [ ] Admin: impersonate user (create admin session as user)
- [ ] Admin: export users CSV
- [ ] Admin: filter by organization
- [ ] Admin: filter by MFA status
- [ ] Admin: filter by last login date
- [ ] Admin: bulk status update
- [ ] Admin: user detail view with full profile

#### 4.18.2 User Profile (Self-Service)
- [x] `GET /api/v1/users/me` -- get own profile
- [x] `PATCH /api/v1/users/me` -- update own profile
- [x] Response: UserResponse
- [ ] Profile: update display name
- [ ] Profile: update phone number (with verification)
- [ ] Profile: update avatar (upload or URL)
- [ ] Profile: update locale
- [ ] Profile: update timezone
- [ ] Profile: view linked social accounts
- [ ] Profile: link/unlink social accounts
- [ ] Profile: download personal data (GDPR data export)
- [ ] Profile: delete account request (GDPR right to be forgotten)

### 4.19 Adaptive Authentication & Risk Engine

#### 4.19.1 Policy Engine
- [x] `PolicyEngine` class (`core/policy_engine.py`)
- [x] `AuthContext` dataclass: user_id, email, ip, user_agent, country, device flags
- [x] `PolicyDecision` dataclass: allow, require_mfa, require_captcha, risk_level, reasons
- [x] Policy: org-level MFA enforcement
- [x] Policy: geo-blocking (org allowed countries)
- [x] Policy: account lockout on 5+ failed attempts
- [x] Policy: CAPTCHA + MFA required on 3+ failed attempts
- [x] Policy: new device triggers MFA
- [x] Policy: new location triggers MFA
- [x] Policy: Tor exit node triggers MFA + HIGH risk
- [x] Risk levels: LOW, MEDIUM, HIGH, CRITICAL
- [x] Structured logging of policy decisions
- [ ] Policy: VPN detection integration
- [ ] Policy: time-of-day anomaly (login at unusual hour)
- [ ] Policy: impossible travel detection (two logins from far-apart locations)
- [ ] Policy: credential stuffing detection (many failed logins across accounts)
- [ ] Policy: rate anomaly (sudden spike in API calls)
- [ ] Policy: configurable thresholds per organization
- [ ] Policy: admin override (skip policy for specific users)

#### 4.19.2 Risk Service
- [x] `RiskService` class (`services/risk_service.py`)
- [x] GeoIP: MaxMind database reader initialization
- [x] GeoIP: `get_country_code()` method
- [x] Tor: `is_tor_exit_node()` method (placeholder)
- [x] VPN: `is_vpn()` method (placeholder)
- [ ] GeoIP: city-level geolocation
- [ ] GeoIP: ASN lookup (ISP info)
- [ ] GeoIP: automatic database updates (MaxMind GeoLite2)
- [ ] Tor: periodic Tor exit node list update (from torproject.org)
- [ ] Tor: cache in Redis
- [ ] VPN: IP reputation service integration (IPQualityScore, ip-api)
- [ ] VPN: ASN-based VPN detection
- [ ] Device fingerprinting: browser fingerprint collection
- [ ] Device fingerprinting: device trust scoring
- [ ] Device fingerprinting: known device database per user

### 4.20 Security Notifications
- [ ] Email: new login from unrecognized device
- [ ] Email: new login from new location/country
- [ ] Email: password changed
- [ ] Email: email address changed
- [ ] Email: MFA device enrolled
- [ ] Email: MFA device removed
- [ ] Email: account locked due to failed attempts
- [ ] Email: account suspended by admin
- [ ] Email: password reset requested
- [ ] Email: security alert template (consistent branding)
- [ ] Push notification: login approval request (for push MFA)
- [ ] Push notification: suspicious login detected
- [ ] Webhook: auth events to application endpoints (configurable per app)

### 4.21 Admin Portal UI (To Be Built)

#### 4.21.1 Admin Login
- [ ] Admin portal: login page
- [ ] Admin portal: super-admin credential authentication
- [ ] Admin portal: MFA challenge during admin login
- [ ] Admin portal: session management for admin sessions
- [ ] Admin portal: idle timeout (15 minutes)
- [ ] Admin portal: remember me (cookie-based session)

#### 4.21.2 Admin Dashboard
- [ ] Dashboard: total users count (active, pending, suspended, locked)
- [ ] Dashboard: total organizations count
- [ ] Dashboard: active sessions count
- [ ] Dashboard: logins today / this week (chart)
- [ ] Dashboard: failed logins today (chart)
- [ ] Dashboard: MFA adoption rate
- [ ] Dashboard: recent audit events feed
- [ ] Dashboard: system health status (DB, Redis, email)
- [ ] Dashboard: quick action buttons (create user, create org)

#### 4.21.3 Admin User Management UI
- [ ] User list: paginated table
- [ ] User list: search by email, name, username
- [ ] User list: filter by status
- [ ] User list: filter by organization
- [ ] User list: filter by MFA status
- [ ] User list: sort by name, email, created_at, last_login
- [ ] User list: per-row actions (view, edit, suspend, delete)
- [ ] User list: bulk actions (suspend, activate, delete)
- [ ] User detail: profile information
- [ ] User detail: organization membership
- [ ] User detail: role and permissions
- [ ] User detail: MFA devices list
- [ ] User detail: active sessions list
- [ ] User detail: recent audit log entries
- [ ] User detail: edit profile form
- [ ] User detail: change status
- [ ] User detail: force password reset button
- [ ] User detail: impersonate user button
- [ ] Create user: form with email, name, org, role
- [ ] Create user: send invite email option

#### 4.21.4 Admin Organization Management UI
- [ ] Org list: paginated table
- [ ] Org list: search by name, domain
- [ ] Org list: per-row actions (view, edit, delete)
- [ ] Org detail: general info (name, slug, domain, logo)
- [ ] Org detail: member list with roles
- [ ] Org detail: invite member form
- [ ] Org detail: remove member
- [ ] Org detail: change member role
- [ ] Org detail: settings (MFA policy, SSO config, IP allowlist)
- [ ] Org detail: audit log (org-scoped)
- [ ] Org detail: OAuth applications for this org
- [ ] Create org: form with name, slug, domain

#### 4.21.5 Admin OAuth Client Management UI
- [ ] Client list: all registered OAuth applications
- [ ] Client detail: client_id display
- [ ] Client detail: client_secret (masked, reveal button)
- [ ] Client detail: redirect URIs list (add/remove)
- [ ] Client detail: allowed scopes
- [ ] Client detail: allowed grant types
- [ ] Client detail: token lifetime settings
- [ ] Client detail: rotate secret button with confirmation
- [ ] Create client: form with name, type, redirect URIs, scopes

#### 4.21.6 Admin Token Inspector
- [ ] Token inspector: paste JWT to decode
- [ ] Token inspector: decoded header display
- [ ] Token inspector: decoded payload display (formatted JSON)
- [ ] Token inspector: signature verification result
- [ ] Token inspector: expiry status (valid / expired)
- [ ] Token inspector: claims validation (issuer, audience, type)
- [ ] Token inspector: blacklist check
- [ ] Token inspector: copy decoded payload button

#### 4.21.7 Admin JWKS Management
- [ ] JWKS: view current public keys
- [ ] JWKS: view key metadata (kid, algorithm, created_at)
- [ ] JWKS: rotate key button with confirmation
- [ ] JWKS: key rotation history
- [ ] JWKS: download public key (PEM / JWK format)

#### 4.21.8 Admin Audit Log Viewer
- [ ] Audit log: paginated table
- [ ] Audit log: filter by user
- [ ] Audit log: filter by action type
- [ ] Audit log: filter by status (success/failure)
- [ ] Audit log: filter by date range (date picker)
- [ ] Audit log: filter by IP address
- [ ] Audit log: filter by organization
- [ ] Audit log: search by description
- [ ] Audit log: sort by timestamp
- [ ] Audit log: detail panel (click to expand)
- [ ] Audit log: export CSV button
- [ ] Audit log: export JSON button
- [ ] Audit log: auto-refresh toggle (live tail)

#### 4.21.9 Admin Rate Limit Configuration
- [ ] Rate limit: view current settings per endpoint group
- [ ] Rate limit: edit limits (requests per time window)
- [ ] Rate limit: per-IP overrides
- [ ] Rate limit: per-client overrides
- [ ] Rate limit: view current rate limit usage/stats
- [ ] Rate limit: blocked requests log

#### 4.21.10 Admin Session Management
- [ ] Sessions: list all active sessions (global)
- [ ] Sessions: filter by user
- [ ] Sessions: filter by device type
- [ ] Sessions: filter by location
- [ ] Sessions: revoke individual session
- [ ] Sessions: bulk revoke (by user, by org, by age)
- [ ] Sessions: session detail (device, browser, OS, IP, location, created, last active)

#### 4.21.11 Admin MFA Management
- [ ] MFA: list users with MFA enrollment status
- [ ] MFA: filter by MFA method (TOTP, SMS, push, webauthn)
- [ ] MFA: force MFA enrollment for user
- [ ] MFA: force MFA enrollment for organization
- [ ] MFA: disable MFA for user (admin override)
- [ ] MFA: view MFA devices for user
- [ ] MFA: remove MFA device for user

### 4.22 Developer Dashboard (To Be Built)
- [ ] Dev dashboard: list own OAuth applications
- [ ] Dev dashboard: create new OAuth application
- [ ] Dev dashboard: application detail/edit
- [ ] Dev dashboard: view client_id, masked client_secret
- [ ] Dev dashboard: manage redirect URIs
- [ ] Dev dashboard: manage allowed scopes
- [ ] Dev dashboard: rotate client secret
- [ ] Dev dashboard: OAuth flow tester (step-by-step walkthrough)
- [ ] Dev dashboard: view token example (decoded JWT)
- [ ] Dev dashboard: API key generation for service accounts
- [ ] Dev dashboard: API key list with last used
- [ ] Dev dashboard: API key revocation
- [ ] Dev dashboard: webhook configuration (endpoint URL, events, secret)
- [ ] Dev dashboard: webhook event log (recent deliveries)
- [ ] Dev dashboard: webhook test button (send test event)
- [ ] Dev dashboard: quickstart documentation embedded
- [ ] Dev dashboard: SDK download links
- [ ] Dev dashboard: code examples (JavaScript, Python, Go, curl)
- [ ] Dev dashboard: rate limit information
- [ ] Dev dashboard: usage analytics (API calls, token issuances)

---

## 5. API Integration

### 5.1 Internal Service Communication
- [x] All 16 apps authenticate via Gate JWT tokens
- [ ] Service-to-service auth: client_credentials grant
- [ ] Service-to-service auth: internal API keys
- [ ] Token validation: each app validates JWT with Gate's JWKS
- [ ] Token validation: JWKS caching with periodic refresh
- [ ] Token validation: middleware library shared across apps
- [ ] Token validation: audience validation per app
- [ ] Token validation: scope enforcement per endpoint

### 5.2 Integration Health Per App
- [ ] Atlas: PKCE login tested end-to-end
- [ ] Atlas: token refresh tested
- [ ] Atlas: role-based access verified
- [ ] Mail: PKCE login tested
- [ ] Mail: token refresh tested
- [ ] Connect: WebSocket auth via Gate token tested
- [ ] Connect: token expiry during WebSocket session handled
- [ ] Meet: meeting room auth via Gate token tested
- [ ] Meet: anonymous guest access flow tested
- [ ] Calendar: PKCE login tested
- [ ] Calendar: org-scoped calendar access verified
- [ ] Writer: PKCE login tested
- [ ] Writer: collaborative editing auth verified
- [ ] Planet: org-scoped CRM API with Gate JWT verified
- [ ] Planet: role-based data access tested
- [ ] Secure: admin role claim in Gate JWT respected
- [ ] Secure: device enrollment auth tested
- [ ] Control Center: admin-only access enforced
- [ ] Capital Hub: financial data access restricted by role
- [ ] TurboTick: auth flow implemented and tested
- [ ] Dock: auth flow implemented and tested
- [ ] Dock: SSO login across all apps from Dock hub
- [ ] Wallet: auth flow + security hardening tested
- [ ] FitterMe: auth flow implemented and tested
- [ ] Learn: forum auth tested
- [ ] Learn: feedback submission auth tested

### 5.3 Webhook Events
- [ ] Webhook: `user.created` event
- [ ] Webhook: `user.updated` event
- [ ] Webhook: `user.deleted` event
- [ ] Webhook: `user.login` event
- [ ] Webhook: `user.logout` event
- [ ] Webhook: `user.mfa_enrolled` event
- [ ] Webhook: `user.password_changed` event
- [ ] Webhook: `session.created` event
- [ ] Webhook: `session.revoked` event
- [ ] Webhook: `org.created` event
- [ ] Webhook: `org.member_added` event
- [ ] Webhook: `org.member_removed` event
- [ ] Webhook: `org.role_changed` event
- [ ] Webhook: delivery with HMAC signature for verification
- [ ] Webhook: retry on failure (exponential backoff)
- [ ] Webhook: delivery log (success, failure, response code)
- [ ] Webhook: configurable per application

---

## 6. State Management

### 6.1 Admin Portal State (Zustand -- To Be Built)
- [ ] `useAuthStore` -- admin session state
- [ ] `useUsersStore` -- user list, filters, pagination, selected user
- [ ] `useOrgsStore` -- org list, filters, pagination, selected org
- [ ] `useAuditStore` -- audit log entries, filters, pagination
- [ ] `useSessionsStore` -- active sessions list
- [ ] `useClientsStore` -- OAuth client list
- [ ] `useThemeStore` -- dark/light mode
- [ ] `useMfaStore` -- MFA enrollment data
- [ ] `useDashboardStore` -- dashboard stats and charts

### 6.2 Backend State
- [x] Database: PostgreSQL for persistent state
- [x] Redis: token blacklist (in-memory)
- [x] Redis: rate limit counters (in-memory)
- [ ] Redis: session cache
- [ ] Redis: JWKS cache
- [ ] Celery: async task queue state (Redis broker)
- [ ] State: database transaction isolation level configured
- [ ] State: optimistic locking for concurrent updates

---

## 7. Performance

### 7.1 Backend Performance
- [x] Async FastAPI with asyncpg (non-blocking I/O)
- [x] Database connection pooling
- [x] ORJSONResponse as default (faster JSON serialization)
- [x] Prometheus metrics: request count, latency histogram
- [x] Metrics endpoint: `GET /metrics`
- [ ] Database: query optimization (explain analyze on critical queries)
- [ ] Database: indexes on frequently queried fields
- [ ] Database: composite indexes for common filter combinations
- [ ] Database: connection pool monitoring and tuning
- [ ] Redis: pipeline commands for batch operations
- [ ] Redis: connection pooling
- [ ] API: response compression (gzip/brotli)
- [ ] API: pagination defaults and max limits enforced
- [ ] API: selective field loading (avoid SELECT *)
- [ ] API: N+1 query prevention (eager loading relationships)
- [ ] API: response time target < 200ms for auth endpoints
- [ ] API: response time target < 500ms for admin list endpoints
- [ ] Caching: user profile cache (Redis, 5 min TTL)
- [ ] Caching: JWKS cache (in-memory, 1 hour TTL)
- [ ] Caching: OIDC discovery cache (in-memory)
- [ ] Caching: role permissions cache (in-memory)

### 7.2 Token Performance
- [ ] Token creation: < 5ms
- [ ] Token validation: < 2ms (local validation, no DB call)
- [ ] Token blacklist check: < 1ms (Redis)
- [ ] JWKS endpoint: cached, < 1ms response
- [ ] Token introspection: < 10ms

### 7.3 Admin Portal Performance (Frontend)
- [ ] Route-based code splitting
- [ ] Lazy load admin pages
- [ ] Bundle size < 300KB gzipped
- [ ] Table virtualization for large datasets
- [ ] Debounced search inputs
- [ ] Optimistic UI updates
- [ ] FCP < 1.5s
- [ ] LCP < 2.5s

### 7.4 Load Testing
- [ ] Load test: 1000 concurrent login requests
- [ ] Load test: 5000 concurrent token validations
- [ ] Load test: 500 concurrent registration requests
- [ ] Load test: token refresh under load
- [ ] Load test: JWKS endpoint under load
- [ ] Load test: admin list endpoints with large datasets
- [ ] Tool: k6 or Locust scripts committed to repo

---

## 8. Accessibility

### 8.1 Server-Rendered Pages (Login, Support)
- [ ] Login page: semantic form with labels
- [ ] Login page: error messages associated with fields (aria-describedby)
- [ ] Login page: focus management on error
- [ ] Login page: keyboard-navigable
- [ ] Login page: screen reader friendly
- [ ] Login page: sufficient color contrast
- [ ] Support page: same as login page accessibility
- [ ] All forms: `autocomplete` attributes for browser autofill
- [ ] All forms: visible focus indicators

### 8.2 Admin Portal Accessibility (To Be Built)
- [ ] Semantic HTML structure
- [ ] ARIA landmarks (main, nav, aside, header)
- [ ] Tables: proper th/scope attributes
- [ ] Tables: sortable columns keyboard accessible
- [ ] Modals: focus trap
- [ ] Modals: return focus on close
- [ ] Toasts: aria-live announcements
- [ ] Forms: label associations
- [ ] Forms: validation error messages linked
- [ ] All interactive elements keyboard accessible
- [ ] Skip to main content link
- [ ] Color contrast WCAG AA compliance
- [ ] prefers-reduced-motion respected

---

## 9. Mobile & Responsive

### 9.1 Server-Rendered Pages
- [ ] Login page: responsive layout
- [ ] Login page: mobile-friendly form (large touch targets)
- [ ] Login page: scales from 320px to 1920px
- [ ] Support page: responsive layout

### 9.2 Admin Portal Responsive (To Be Built)
- [ ] Admin sidebar: collapsible on mobile
- [ ] Admin tables: horizontal scroll on mobile
- [ ] Admin tables: card view alternative on mobile
- [ ] Admin forms: single column on mobile
- [ ] Admin dashboard: stacked cards on mobile
- [ ] Admin modals: full-screen on mobile
- [ ] Admin: touch-friendly tap targets (44px min)
- [ ] Admin: mobile breakpoint (< 768px)
- [ ] Admin: tablet breakpoint (768-1024px)

---

## 10. Internationalization

### 10.1 Backend i18n
- [ ] Error messages: externalized to translation files
- [ ] Email templates: localized (registration, reset, notifications)
- [ ] Audit log actions: translatable
- [ ] API responses: Accept-Language header support
- [ ] User locale stored in profile
- [ ] Date/time: UTC storage, locale-aware display

### 10.2 Admin Portal i18n (To Be Built)
- [ ] i18n library configured
- [ ] English (en) language file
- [ ] All UI strings externalized
- [ ] Date/time locale-aware formatting
- [ ] Number formatting
- [ ] RTL layout support

### 10.3 Login Pages i18n
- [ ] Login page: language selector
- [ ] Login page: translated labels and messages
- [ ] Support page: translated labels and messages
- [ ] Email templates: per-user locale

---

## 11. Security

### 11.1 Transport Security
- [x] HSTS header: `max-age=63072000; includeSubDomains; preload`
- [x] X-Content-Type-Options: `nosniff`
- [x] X-Frame-Options: `DENY`
- [x] X-XSS-Protection: `1; mode=block`
- [x] Referrer-Policy: `strict-origin-when-cross-origin`
- [x] Permissions-Policy: `camera=(), microphone=(), geolocation=()`
- [x] Cache-Control: `no-store, no-cache, must-revalidate`
- [x] Pragma: `no-cache`
- [x] Content-Security-Policy configured
- [x] Server header removed
- [x] CORS configured with explicit allowed origins
- [x] CORS: credentials allowed
- [x] CORS: max-age 600
- [x] CORS: expose X-Request-ID and rate limit headers
- [ ] TLS 1.2+ enforced (server-level config)
- [ ] Certificate pinning for internal service-to-service calls
- [ ] OCSP stapling
- [ ] HTTP/2 enabled

### 11.2 Authentication Security
- [x] Password hashing: bcrypt with cost factor 12
- [x] JWT signing: RS256 (asymmetric, private key signs, public key verifies)
- [x] RSA key size: 2048-bit
- [x] Token blacklisting via Redis
- [x] Rate limiting on auth endpoints (login, register, MFA)
- [x] Rate limiting middleware (sliding window with Redis)
- [x] Account lockout mechanism
- [x] MFA support (TOTP, SMS, push, backup codes)
- [x] Request ID middleware for request tracing
- [ ] Password: Argon2id as alternative/upgrade to bcrypt
- [ ] JWT: RSA 4096-bit keys for production
- [ ] JWT: EC P-256 key support (smaller tokens)
- [ ] PKCE: reject "plain" challenge method for public clients
- [ ] PKCE: enforce minimum code_verifier length (43 chars)
- [ ] Token: bind to client fingerprint
- [ ] Token: maximum token lifetime enforcement
- [ ] Brute force: IP-based rate limiting + account-based rate limiting
- [ ] Brute force: progressive delays between attempts
- [ ] Brute force: CAPTCHA escalation
- [ ] Credential stuffing: detection and mitigation

### 11.3 Data Security
- [x] Encryption at rest: Fernet symmetric encryption for sensitive fields
- [x] `encrypt_value()` / `decrypt_value()` utility functions
- [ ] Database: TLS connection to PostgreSQL
- [ ] Database: encrypted at-rest (PostgreSQL TDE or disk encryption)
- [ ] Redis: TLS connection
- [ ] Redis: password authentication
- [ ] Secrets: rotatable encryption keys
- [ ] Secrets: key management service (AWS KMS, HashiCorp Vault)
- [ ] PII: minimize logging of PII (email, IP masked in non-audit logs)
- [ ] PII: field-level encryption for phone numbers
- [ ] Backup: encrypted backups
- [ ] Data retention: configurable per data type

### 11.4 Input Validation & Sanitization
- [x] Pydantic v2 schema validation on all request bodies
- [ ] SQL injection: parameterized queries (SQLAlchemy ORM)
- [ ] NoSQL injection: Redis command sanitization
- [ ] Path traversal: URL path validation
- [ ] Request size limits
- [ ] JSON depth limits
- [ ] Header size limits
- [ ] File upload restrictions (if any)

### 11.5 Security Monitoring
- [x] Sentry error tracking (optional DSN)
- [x] Structured logging with structlog
- [x] Prometheus metrics for request monitoring
- [ ] Security events: real-time alerting (PagerDuty, Slack)
- [ ] Security events: login anomaly detection
- [ ] Security events: brute force attempt alerting
- [ ] Security events: token abuse detection
- [ ] Security events: SIEM integration (Splunk, ELK)
- [ ] Penetration testing: OWASP Top 10 checklist
- [ ] Penetration testing: scheduled security audit
- [ ] Vulnerability scanning: dependency scanning in CI
- [ ] Vulnerability scanning: SAST (static application security testing)
- [ ] Vulnerability scanning: DAST (dynamic application security testing)

### 11.6 Compliance
- [ ] GDPR: data export (user data download)
- [ ] GDPR: data deletion (right to be forgotten)
- [ ] GDPR: consent management
- [ ] GDPR: data processing records
- [ ] SOC 2: access control evidence
- [ ] SOC 2: audit log evidence
- [ ] SOC 2: change management evidence
- [ ] HIPAA: PHI handling (if applicable)
- [ ] PCI DSS: cardholder data protection (if applicable)

---

## 12. Testing

### 12.1 Unit Tests (Backend)
- [x] Test directory: `tests/`
- [x] conftest.py with test fixtures
- [x] `test_auth.py` -- authentication tests
- [x] `test_oauth.py` -- OAuth flow tests
- [x] `test_mfa.py` -- MFA tests
- [x] `test_totp_backup_codes.py` -- TOTP and backup code tests
- [x] `test_oauth_org_claims.py` -- OAuth organization claims tests
- [x] `test_database_repair.py` -- database repair utility tests
- [ ] Test: user registration with valid data
- [ ] Test: user registration with duplicate email
- [ ] Test: user registration with weak password
- [ ] Test: user registration with invalid email format
- [ ] Test: user login with correct credentials
- [ ] Test: user login with incorrect password
- [ ] Test: user login with non-existent email
- [ ] Test: user login with locked account
- [ ] Test: user login with suspended account
- [ ] Test: user login with unverified email
- [ ] Test: account lockout after N failed attempts
- [ ] Test: account lockout expiry
- [ ] Test: token creation (access, refresh, ID, MFA)
- [ ] Test: token validation (valid signature)
- [ ] Test: token validation (expired token)
- [ ] Test: token validation (wrong issuer)
- [ ] Test: token validation (wrong type)
- [ ] Test: token refresh with valid refresh token
- [ ] Test: token refresh with expired refresh token
- [ ] Test: token refresh with blacklisted refresh token
- [ ] Test: token revocation
- [ ] Test: token blacklist check
- [ ] Test: password hashing and verification
- [ ] Test: password strength validation
- [ ] Test: PKCE code challenge verification (S256)
- [ ] Test: PKCE code challenge verification (plain)
- [ ] Test: OAuth authorization code generation
- [ ] Test: OAuth authorization code exchange
- [ ] Test: OAuth authorization code single-use
- [ ] Test: OAuth authorization code expiry
- [ ] Test: OAuth client validation (client_id, redirect_uri)
- [ ] Test: OIDC discovery document contents
- [ ] Test: OIDC JWKS endpoint returns valid JWK
- [ ] Test: OIDC userinfo returns correct claims per scope
- [ ] Test: TOTP enrollment (secret generation, QR URI)
- [ ] Test: TOTP verification (valid code)
- [ ] Test: TOTP verification (invalid code)
- [ ] Test: TOTP verification (expired code)
- [ ] Test: SMS OTP generation and verification
- [ ] Test: backup code generation (correct count, format)
- [ ] Test: backup code verification (valid code)
- [ ] Test: backup code single-use (cannot reuse)
- [ ] Test: push challenge creation
- [ ] Test: push challenge approval
- [ ] Test: push challenge denial
- [ ] Test: push challenge expiry
- [ ] Test: session creation on login
- [ ] Test: session listing for user
- [ ] Test: session revocation
- [ ] Test: session revoke all
- [ ] Test: password forgot (email sent check)
- [ ] Test: password reset with valid token
- [ ] Test: password reset with expired token
- [ ] Test: password change with correct current password
- [ ] Test: password change with incorrect current password
- [ ] Test: email verification with valid token
- [ ] Test: email verification with expired token
- [ ] Test: admin list users (pagination, filters)
- [ ] Test: admin update user status
- [ ] Test: admin soft delete user
- [ ] Test: admin create organization
- [ ] Test: admin list organizations
- [ ] Test: admin update organization
- [ ] Test: admin delete organization
- [ ] Test: admin bulk onboard users
- [ ] Test: admin audit log query
- [ ] Test: admin audit log export
- [ ] Test: role permission lookups
- [ ] Test: policy engine: low risk scenario
- [ ] Test: policy engine: new device scenario
- [ ] Test: policy engine: new location scenario
- [ ] Test: policy engine: failed attempts lockout
- [ ] Test: policy engine: geo-blocking
- [ ] Test: policy engine: Tor exit node
- [ ] Test: policy engine: org MFA enforcement
- [ ] Test: rate limiting middleware (allow and block)
- [ ] Test: security headers middleware
- [ ] Test: request ID middleware
- [ ] Test: audit logging middleware
- [ ] Test: CORS configuration
- [ ] Test: health check endpoints
- [ ] Test: Fernet encryption/decryption
- [ ] Test: secure token generation
- [ ] Test: OTP generation

### 12.2 Integration Tests
- [ ] Integration: full registration -> email verification -> login flow
- [ ] Integration: login -> MFA challenge -> TOTP verify -> tokens
- [ ] Integration: login -> MFA challenge -> SMS verify -> tokens
- [ ] Integration: login -> MFA challenge -> backup code -> tokens
- [ ] Integration: OAuth PKCE: authorize -> code -> token exchange -> userinfo
- [ ] Integration: OAuth: token -> refresh -> new tokens
- [ ] Integration: password forgot -> email -> reset -> login
- [ ] Integration: admin: create org -> create user -> assign role -> login
- [ ] Integration: session: login -> list sessions -> revoke -> verify revoked
- [ ] Integration: MFA: enroll TOTP -> verify -> login with MFA
- [ ] Integration: MFA: enroll SMS -> verify -> login with SMS
- [ ] Integration: concurrent logins from multiple devices
- [ ] Integration: database migrations (up and down)

### 12.3 E2E Tests
- [ ] E2E: server-rendered login page form submission
- [ ] E2E: OAuth PKCE flow with real browser redirect
- [ ] E2E: MFA enrollment via admin portal UI
- [ ] E2E: admin user management workflows
- [ ] E2E: admin organization management workflows
- [ ] E2E: audit log viewing and export

### 12.4 Security Tests
- [ ] Security: SQL injection attempts on all endpoints
- [ ] Security: XSS attempts on login form
- [ ] Security: CSRF token validation
- [ ] Security: token forgery detection
- [ ] Security: expired token rejection
- [ ] Security: rate limit enforcement verification
- [ ] Security: brute force lockout verification
- [ ] Security: privilege escalation attempts (regular user -> admin)
- [ ] Security: IDOR (Insecure Direct Object Reference) tests
- [ ] Security: header injection attempts
- [ ] Security: SSRF (Server-Side Request Forgery) tests
- [ ] Security: open redirect in OAuth callback
- [ ] Security: authorization code injection
- [ ] Security: token leakage via referrer
- [ ] Security: timing attacks on password comparison
- [ ] Security: JWT algorithm confusion attack (RS256 vs HS256)

### 12.5 Performance Tests
- [ ] Performance: login endpoint p99 < 500ms
- [ ] Performance: token validation p99 < 50ms
- [ ] Performance: JWKS endpoint p99 < 10ms
- [ ] Performance: admin list users p99 < 1s (1000 users)
- [ ] Performance: audit log query p99 < 2s (100k entries)
- [ ] Performance: concurrent login simulation (1000 req/s)

### 12.6 Admin Portal Tests (Frontend -- To Be Built)
- [ ] Unit tests: all React components
- [ ] Unit tests: Zustand stores
- [ ] Unit tests: API client functions
- [ ] Component tests: login flow
- [ ] Component tests: user management CRUD
- [ ] Component tests: org management CRUD
- [ ] Component tests: audit log viewer
- [ ] Component tests: token inspector
- [ ] E2E tests: admin login and navigation
- [ ] E2E tests: user CRUD workflow
- [ ] E2E tests: org CRUD workflow
- [ ] Visual regression: all admin pages (light + dark)
- [ ] Accessibility: aXe automated audit

### 12.7 Test Infrastructure
- [ ] Test database: separate PostgreSQL instance for tests
- [ ] Test Redis: separate Redis instance for tests
- [ ] Test fixtures: factory functions for User, Org, Session, Token
- [ ] Test fixtures: authenticated client helper
- [ ] Test fixtures: superadmin client helper
- [ ] Test coverage: > 80% line coverage
- [ ] Test coverage: 100% coverage on security-critical paths
- [ ] CI: tests run on every PR
- [ ] CI: test report published as PR comment
- [ ] CI: coverage report with diff

---

## 13. Documentation

### 13.1 Backend Documentation
- [ ] README.md: project overview
- [ ] README.md: architecture diagram
- [ ] README.md: local development setup
- [ ] README.md: environment variables reference
- [ ] README.md: database migration instructions
- [ ] README.md: API overview
- [ ] AUTHENTICATION_ANALYSIS.md: (confirmed present) review and update
- [ ] DEPLOYMENT_GUIDE.md: (confirmed present) review and update
- [ ] API docs: OpenAPI spec auto-generated (FastAPI /docs)
- [ ] API docs: Redoc alternative (/redoc)
- [ ] API docs: authentication section
- [ ] API docs: error response format
- [ ] API docs: rate limiting documentation
- [ ] API docs: OIDC discovery explanation
- [ ] API docs: PKCE flow walkthrough
- [ ] API docs: MFA flow walkthrough
- [ ] API docs: webhook events reference
- [ ] API docs: SCIM endpoints reference
- [ ] SDK docs: JavaScript/TypeScript client library
- [ ] SDK docs: Python client library
- [ ] SDK docs: Go client library
- [ ] CONTRIBUTING.md: how to contribute
- [ ] SECURITY.md: vulnerability reporting policy
- [ ] CHANGELOG.md: version history

### 13.2 Integration Guide (For Other Apps)
- [ ] Guide: how to integrate Gate auth into a new app
- [ ] Guide: PKCE flow implementation step-by-step
- [ ] Guide: token validation in Express.js middleware
- [ ] Guide: token validation in FastAPI middleware
- [ ] Guide: token validation in Go middleware
- [ ] Guide: handling token refresh in frontend
- [ ] Guide: protecting routes based on roles/permissions
- [ ] Guide: organization-scoped data access patterns
- [ ] Guide: WebSocket authentication with Gate tokens
- [ ] Guide: service-to-service authentication

---

## 14. Deployment & CI/CD

### 14.1 Docker
- [x] Docker Compose for local development (`docker-compose.yml`)
- [ ] Dockerfile: multi-stage build (builder + runtime)
- [ ] Dockerfile: non-root user
- [ ] Dockerfile: health check instruction
- [ ] Dockerfile: minimal base image (python:3.11-slim)
- [ ] Dockerfile: pip install from requirements.txt (no dev deps)
- [ ] Docker Compose: production config
- [ ] Docker Compose: PostgreSQL with persistent volume
- [ ] Docker Compose: Redis with persistent volume
- [ ] Docker Compose: network isolation
- [ ] Docker Compose: resource limits (CPU, memory)
- [ ] Container: graceful shutdown handling
- [ ] Container: signal handling (SIGTERM)

### 14.2 Kubernetes
- [ ] K8s: Deployment manifest
- [ ] K8s: Service manifest
- [ ] K8s: Ingress manifest (with TLS)
- [ ] K8s: ConfigMap for non-secret config
- [ ] K8s: Secret for sensitive config
- [ ] K8s: HorizontalPodAutoscaler
- [ ] K8s: PodDisruptionBudget
- [ ] K8s: liveness probe (`/health/live`)
- [ ] K8s: readiness probe (`/health/ready`)
- [ ] K8s: startup probe
- [ ] K8s: resource requests and limits
- [ ] K8s: network policy
- [ ] Helm chart: templated manifests
- [ ] Helm chart: values.yaml with defaults

### 14.3 CI/CD Pipeline
- [ ] GitHub Actions: CI workflow
- [ ] CI: lint (ruff or flake8)
- [ ] CI: type check (mypy)
- [ ] CI: unit tests (pytest)
- [ ] CI: integration tests
- [ ] CI: security tests
- [ ] CI: coverage report
- [ ] CI: dependency audit (pip-audit)
- [ ] CI: Docker image build
- [ ] CI: Docker image push to registry
- [ ] CI: database migration check (alembic check)
- [ ] CD: staging deployment on merge to develop
- [ ] CD: production deployment on merge to main (with approval)
- [ ] CD: database migration execution
- [ ] CD: rollback procedure
- [ ] CD: canary deployment support
- [ ] CD: blue-green deployment support

### 14.4 Health & Monitoring
- [x] Health check: `GET /health` (database + Redis)
- [x] Health check: `GET /health/ready` (Kubernetes readiness)
- [x] Health check: `GET /health/live` (Kubernetes liveness)
- [x] Prometheus: request count metric
- [x] Prometheus: request latency histogram
- [x] Prometheus: `GET /metrics` endpoint
- [ ] Monitoring: Grafana dashboard for Gate metrics
- [ ] Monitoring: alert on error rate > threshold
- [ ] Monitoring: alert on latency p99 > threshold
- [ ] Monitoring: alert on failed login spike
- [ ] Monitoring: alert on database connection pool exhaustion
- [ ] Monitoring: alert on Redis connection failure
- [ ] Logging: JSON structured logs in production
- [ ] Logging: request ID correlation across services
- [ ] Logging: log level configurable via environment
- [ ] Logging: sensitive data redaction in logs
- [ ] Tracing: OpenTelemetry integration
- [ ] Tracing: distributed trace ID propagation
- [ ] Uptime: external uptime monitoring (e.g., Pingdom, UptimeRobot)

---

## 15. Backend

### 15.1 FastAPI Application Structure
- [x] Main app in `app/main.py`
- [x] API router in `app/api/v1/router.py`
- [x] Route modules: auth, users, mfa, oauth, oidc, admin, audit
- [x] Dependencies in `app/api/deps.py`
- [x] Models in `app/models/` (user, session, mfa, oauth, organization, audit, application)
- [x] Schemas in `app/schemas/` (auth, user, oauth, mfa, organization)
- [x] Services in `app/services/` (auth, mfa, oauth, organization, token_manager, audit_logger, risk)
- [x] Core modules in `app/core/` (security, totp, session, rate_limiter, audit_logger, roles, policy_engine, email_service, sms, push_notification)
- [x] Middleware in `app/middleware/` (rate_limit, request_id, security_headers, audit_logging)
- [x] Configuration in `app/config.py`
- [x] Database in `app/database.py`
- [x] Celery in `app/celery_app.py`
- [x] Utils in `app/utils/` (datetime_utils, pagination, crypto, validators)
- [ ] Background tasks: Celery workers configured and running
- [ ] Background tasks: email sending via Celery
- [ ] Background tasks: webhook delivery via Celery
- [ ] Background tasks: token cleanup via Celery Beat
- [ ] Background tasks: audit log archival via Celery Beat
- [ ] Background tasks: session cleanup (expired sessions) via Celery Beat

### 15.2 Database Models
- [x] User model: id, email, username, hashed_password, profile fields, status, security fields, org_id, metadata, timestamps
- [x] User model: UserStatus enum (active, inactive, suspended, pending_verification, locked)
- [x] User model: relationships (mfa_devices, sessions, backup_codes)
- [x] User model: computed properties (full_name, is_locked)
- [x] User model: indexes (email_lower unique, org_id)
- [x] MFA model: MFADevice (id, user_id, device_type, device_name, secret, is_active, is_verified, timestamps)
- [x] Session model: UserSession
- [x] OAuth model: AuthorizationCode, OAuthApplication
- [x] Organization model: id, name, slug, domain, metadata, timestamps
- [x] Audit model: AuditLog (id, action, user_id, user_email, ip_address, status, description, created_at)
- [x] Application model: OAuth application registration
- [ ] Model: BackupCode (user_id, code_hash, used_at)
- [ ] Model: LoginAttempt (user_id, ip_address, success, timestamp)
- [ ] Model: DeviceFingerprint (user_id, fingerprint_hash, device_info, first_seen, last_seen)
- [ ] Model: WebhookEndpoint (app_id, url, secret, events, active)
- [ ] Model: WebhookDelivery (endpoint_id, event, payload, status, attempts)
- [ ] Model: ApiKey (user_id, org_id, key_hash, name, scopes, expires_at, last_used)
- [ ] Model: SAMLProvider (org_id, entity_id, sso_url, certificate, attribute_mapping)
- [ ] Model: SocialConnection (user_id, provider, provider_user_id, access_token_enc)
- [ ] Model: PasswordHistory (user_id, password_hash, created_at)

### 15.3 Database Migrations
- [x] Alembic configured with `env.py`
- [x] Initial migration: schema creation with MFA support
- [ ] Migration: add LoginAttempt table
- [ ] Migration: add DeviceFingerprint table
- [ ] Migration: add WebhookEndpoint and WebhookDelivery tables
- [ ] Migration: add ApiKey table
- [ ] Migration: add SAMLProvider table
- [ ] Migration: add SocialConnection table
- [ ] Migration: add PasswordHistory table
- [ ] Migration: add fields for enhanced session tracking
- [ ] Migration: add indexes for audit log queries
- [ ] Migration: seed data migration (default roles, default org)
- [ ] Alembic: down migrations tested
- [ ] Alembic: migration naming convention
- [ ] Alembic: CI check for unapplied migrations

### 15.4 Email Service
- [x] Email service module (`core/email_service.py`)
- [ ] Email: SMTP connection with TLS
- [ ] Email: connection pooling/reuse
- [ ] Email: HTML + plaintext multipart
- [ ] Email: template engine (Jinja2)
- [ ] Email template: registration verification
- [ ] Email template: password reset
- [ ] Email template: magic link
- [ ] Email template: MFA backup codes
- [ ] Email template: new device login alert
- [ ] Email template: account locked
- [ ] Email template: password changed
- [ ] Email template: organization invitation
- [ ] Email template: welcome email
- [ ] Email: queue via Celery for async sending
- [ ] Email: retry on SMTP failure
- [ ] Email: delivery tracking (sent/bounced/opened)
- [ ] Email: unsubscribe link for notification emails
- [ ] Email: SPF/DKIM/DMARC compliance

### 15.5 SMS Service
- [x] SMS module (`core/sms.py`)
- [ ] SMS: Twilio SDK integration
- [ ] SMS: send OTP message
- [ ] SMS: message template
- [ ] SMS: delivery status callback
- [ ] SMS: fallback provider (e.g., AWS SNS)
- [ ] SMS: cost tracking
- [ ] SMS: opt-out handling

### 15.6 Push Notification Service
- [x] Push notification module (`core/push_notification.py`)
- [ ] Push: Firebase Admin SDK integration
- [ ] Push: send MFA approval request
- [ ] Push: device token registration
- [ ] Push: device token refresh handling
- [ ] Push: iOS APNs support
- [ ] Push: delivery tracking

### 15.7 Celery Task Queue
- [x] Celery app configuration (`app/celery_app.py`)
- [ ] Celery: Redis as broker
- [ ] Celery: Redis as result backend
- [ ] Celery: worker concurrency configured
- [ ] Celery: task retry policies
- [ ] Celery: dead letter queue for failed tasks
- [ ] Celery: task monitoring (Flower)
- [ ] Celery Beat: scheduled tasks configured
- [ ] Celery Beat: token cleanup (hourly)
- [ ] Celery Beat: session cleanup (hourly)
- [ ] Celery Beat: audit log archival (daily)
- [ ] Celery Beat: GeoIP database update (weekly)
- [ ] Celery Beat: Tor exit node list update (daily)

### 15.8 Error Handling
- [x] Global exception handler (500 -> "Internal server error")
- [x] Structured error logging with structlog
- [x] Sentry integration for error tracking
- [ ] Error: custom exception classes (AuthError, TokenError, RateLimitError)
- [ ] Error: consistent error response format ({detail, code, field})
- [ ] Error: validation error formatting (422 -> readable messages)
- [ ] Error: database error handling (connection, timeout, constraint)
- [ ] Error: Redis error handling (connection, timeout)
- [ ] Error: external service error handling (SMTP, Twilio, FCM)
- [ ] Error: circuit breaker for external services

### 15.9 Logging
- [x] Structured logging: structlog configured
- [x] Logging: JSON format in production, console format in development
- [x] Logging: context variables (merge_contextvars)
- [x] Logging: timestamp, log level, logger name
- [ ] Logging: request ID in all log entries
- [ ] Logging: user ID in authenticated request logs
- [ ] Logging: organization ID in org-scoped logs
- [ ] Logging: sensitive data redaction (passwords, tokens)
- [ ] Logging: log level configurable per module
- [ ] Logging: correlation ID for cross-service tracing
- [ ] Logging: access log format

---

## Summary

| Section | Done | Todo | Total |
|---------|------|------|-------|
| 1. Project Setup & Configuration | ~46 | ~60 | ~106 |
| 2. Design System Integration (Admin UI) | 0 | ~55 | ~55 |
| 3. Dark Mode (Admin UI) | 0 | ~80 | ~80 |
| 4. Core Features | ~85 | ~310 | ~395 |
| 5. API Integration | ~1 | ~55 | ~56 |
| 6. State Management | ~2 | ~15 | ~17 |
| 7. Performance | ~5 | ~35 | ~40 |
| 8. Accessibility | 0 | ~25 | ~25 |
| 9. Mobile & Responsive | 0 | ~15 | ~15 |
| 10. Internationalization | 0 | ~15 | ~15 |
| 11. Security | ~15 | ~50 | ~65 |
| 12. Testing | ~7 | ~130 | ~137 |
| 13. Documentation | ~2 | ~35 | ~37 |
| 14. Deployment & CI/CD | ~7 | ~45 | ~52 |
| 15. Backend | ~30 | ~65 | ~95 |
| **TOTAL** | **~200** | **~990** | **~1190** |

---

> Generated: 2026-04-06
> Source: `/Gate/authx/` codebase analysis + PER_APP_CHECKLIST.md sections 16-A through 16-D
> Note: Gate is the CENTRAL authentication service for all 16 RM Orbit applications.
> Every security item in this checklist has platform-wide impact.
