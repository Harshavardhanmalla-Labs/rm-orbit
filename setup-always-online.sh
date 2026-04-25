#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# RM Orbit – Always-Online Setup
# ═══════════════════════════════════════════════════════════════════════
# Run this ONCE to configure the machine so all services stay online
# permanently — surviving crashes, terminal closures, and reboots.
#
# What this does:
#   1. Starts all Docker infrastructure (Gate, Mail, Connect)
#   2. Starts all native services via PM2
#   3. Configures PM2 to auto-start on boot
#   4. Enables the systemd watchdog timer (checks every 60s)
#   5. Enables lingering (keeps user services alive after logout)
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail

ROOT_DIR="/home/sasi/Desktop/dev/RM Orbit"
cd "$ROOT_DIR"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'
BOLD='\033[1m'; NC='\033[0m'

info()  { printf "${CYAN}[INFO]${NC}  %s\n" "$*"; }
ok()    { printf "${GREEN}[  OK]${NC}  %s\n" "$*"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$*"; }

echo ""
printf "${BOLD}${CYAN}🔒 RM Orbit — Always-Online Setup${NC}\n"
echo "═══════════════════════════════════════════════════════════════"

# ─── 1. Docker infrastructure ────────────────────────────────────────
echo ""
info "Phase 1: Docker infrastructure..."

if [ -d "$ROOT_DIR/Gate/authx" ]; then
  info "Starting Gate (AuthX)..."
  cd "$ROOT_DIR/Gate/authx" && docker compose up -d 2>/dev/null && ok "Gate started" || fail "Gate failed"
  cd "$ROOT_DIR"
fi

if [ -d "$ROOT_DIR/Mail" ]; then
  info "Starting Mail..."
  cd "$ROOT_DIR/Mail"
  [ ! -f .env ] && [ -f .env.example ] && cp .env.example .env
  docker compose up -d 2>/dev/null && ok "Mail started" || fail "Mail failed"
  cd "$ROOT_DIR"
fi

if [ -d "$ROOT_DIR/Connect" ]; then
  info "Starting Connect..."
  cd "$ROOT_DIR/Connect" && docker compose up -d 2>/dev/null && ok "Connect started" || fail "Connect failed"
  cd "$ROOT_DIR"
fi

if [ -d "$ROOT_DIR/FitterMe" ]; then
  info "Starting FitterMe..."
  cd "$ROOT_DIR/FitterMe" && docker compose up -d 2>/dev/null && ok "FitterMe started" || fail "FitterMe failed"
  cd "$ROOT_DIR"
fi

# ─── 2. PM2 native services ──────────────────────────────────────────
echo ""
info "Phase 2: Starting native services with PM2..."

# Kill any stale background processes from old start.sh runs
info "Cleaning stale background processes..."
pkill -f "http.server 45007" 2>/dev/null || true
pkill -f "http.server 45009" 2>/dev/null || true
pkill -f "http.server 45010" 2>/dev/null || true
pkill -f "http.server 45012" 2>/dev/null || true
pkill -f "http.server 45013" 2>/dev/null || true

# Stop any existing PM2 processes and start fresh
pm2 delete all 2>/dev/null || true
pm2 start "$ROOT_DIR/ecosystem.config.cjs"
ok "All PM2 processes started"

# ─── 3. PM2 boot persistence ─────────────────────────────────────────
echo ""
info "Phase 3: Configuring PM2 boot persistence..."
pm2 save
info "Run the following command ONCE (requires sudo) to survive reboots:"
echo ""
printf "  ${BOLD}pm2 startup${NC}\n"
echo ""
info "(Copy the command it outputs and run it with sudo)"

# ─── 4. Systemd watchdog timer ────────────────────────────────────────
echo ""
info "Phase 4: Enabling watchdog timer..."
chmod +x "$ROOT_DIR/scripts/watchdog.sh"
systemctl --user daemon-reload
systemctl --user enable orbit-watchdog.timer
systemctl --user start orbit-watchdog.timer
ok "Watchdog timer active (checks every 60 seconds)"

# ─── 5. Enable lingering ─────────────────────────────────────────────
echo ""
info "Phase 5: Enabling user session lingering..."
loginctl enable-linger sasi 2>/dev/null && ok "Lingering enabled" || info "Lingering may need sudo: sudo loginctl enable-linger sasi"

# ─── Summary ──────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════"
printf "${BOLD}${GREEN}✅ Always-Online Setup Complete${NC}\n"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  📋 Your services are now protected by THREE layers:"
echo ""
echo "  1. PM2 auto-restart   → crashes restart in 3 seconds"
echo "  2. Docker restart     → containers use 'unless-stopped'"
echo "  3. Watchdog timer     → checks all ports every 60s,"
echo "                          restarts anything that's down"
echo ""
echo "  📊 Check status:      pm2 status"
echo "                        ./status.sh"
echo "  📜 View logs:         pm2 logs <app-name>"
echo "  🔍 Watchdog log:      tail -f watchdog.log"
echo "  🔄 Manual restart:    pm2 restart <app-name>"
echo "                        pm2 restart all"
echo ""
echo "═══════════════════════════════════════════════════════════════"
