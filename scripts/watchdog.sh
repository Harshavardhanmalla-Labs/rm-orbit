#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# RM Orbit Watchdog — Ensures ALL services stay online
# ═══════════════════════════════════════════════════════════════════════
# Designed to run as a systemd timer / cron job every 60 seconds.
# Checks every assigned port. If a service is down, it restarts it.
# ═══════════════════════════════════════════════════════════════════════
set -uo pipefail

ROOT_DIR="/home/sasi/Desktop/dev/RM Orbit"
LOG_FILE="$ROOT_DIR/watchdog.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

is_port_up() {
  curl -s -o /dev/null --connect-timeout 3 "http://localhost:$1" 2>/dev/null
}

# ─── PM2 service restart ─────────────────────────────────────────────
restart_pm2() {
  local name="$1"
  log "RESTARTING PM2 app: $name"
  pm2 restart "$name" --update-env >> "$LOG_FILE" 2>&1 || true
}

# ─── Docker service restart ──────────────────────────────────────────
restart_docker() {
  local dir="$1"
  log "RESTARTING Docker compose in: $dir"
  cd "$dir" && docker compose up -d >> "$LOG_FILE" 2>&1 || true
  cd "$ROOT_DIR"
}

# ─── Check & heal loop ───────────────────────────────────────────────
HEALED=0
TOTAL=0

check() {
  local port="$1" label="$2" type="$3" target="$4"
  TOTAL=$((TOTAL + 1))
  if ! is_port_up "$port"; then
    log "DOWN: $label (:$port)"
    if [ "$type" = "pm2" ]; then
      restart_pm2 "$target"
    elif [ "$type" = "docker" ]; then
      restart_docker "$target"
    fi
    HEALED=$((HEALED + 1))
  fi
}

# ─── Native services (PM2-managed) ───────────────────────────────────
check 5173  "Atlas-Frontend"       pm2 "Atlas-Frontend"
check 8000  "Atlas-Backend"        pm2 "Atlas-Backend"
check 45005 "Calendar-Frontend"    pm2 "Calendar-Frontend"
check 5001  "Calendar-Backend"     pm2 "Calendar-Backend"
check 45011 "CC-Frontend"          pm2 "CC-Frontend"
check 8077  "CC-Backend"           pm2 "CC-Backend"
check 45003 "Meet-Frontend"        pm2 "Meet-Frontend"
check 6001  "Meet-Backend"         pm2 "Meet-Backend"
check 45006 "Planet-Frontend"      pm2 "Planet-Frontend"
check 46000 "Planet-Backend"       pm2 "Planet-Backend"
check 45010 "Writer-Frontend"      pm2 "Writer-Frontend"
check 6011  "Writer-Backend"       pm2 "Writer-Backend"
check 45009 "Learn-Frontend"       pm2 "Learn-Frontend"
check 45013 "CapitalHub-Frontend"  pm2 "CapitalHub-Frontend"
check 45012 "Secure-Frontend"      pm2 "Secure-Frontend"
check 6004  "Secure-Backend"       pm2 "Secure-Backend"
check 6200  "Search-Backend"       pm2 "Search-Backend"
check 45007 "RM-Fonts"             pm2 "RM-Fonts"

# ─── Docker services ─────────────────────────────────────────────────
check 45001 "Gate(AuthX)"          docker "$ROOT_DIR/Gate/authx"
check 45004 "Mail-Frontend"        docker "$ROOT_DIR/Mail"
check 8004  "Mail-Backend"         docker "$ROOT_DIR/Mail"
check 45008 "Connect-Frontend"     docker "$ROOT_DIR/Connect"
check 5000  "Connect-Backend"      docker "$ROOT_DIR/Connect"

# ─── Summary ─────────────────────────────────────────────────────────
if [ "$HEALED" -gt 0 ]; then
  log "WATCHDOG: Healed $HEALED/$TOTAL services"
fi
