#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# RM Orbit Ecosystem – Production Orchestration Script 💎
# ═══════════════════════════════════════════════════════════════════════
# Features:
#   • Pre-flight port conflict detection
#   • Dependency-ordered startup (Gate → backends → frontends)
#   • Health-check after each service launch
#   • Automatic restart on crash (supervised background loop)
#   • Colour-coded status output
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail

ROOT_DIR="/home/sasi/Desktop/dev/RM Orbit"
cd "$ROOT_DIR"

# ─── Colours ──────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# ─── Logging helpers ──────────────────────────────────────────────────
info()  { printf "${CYAN}[INFO]${NC}  %s\n" "$*"; }
ok()    { printf "${GREEN}[  OK]${NC}  %s\n" "$*"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$*"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$*"; }

# ─── Sync shared UI assets if script exists ───────────────────────────
if [ -x "$ROOT_DIR/scripts/sync-orbit-ui-assets.sh" ]; then
  "$ROOT_DIR/scripts/sync-orbit-ui-assets.sh" || warn "orbit-ui asset sync failed; continuing startup"
fi

# ═══════════════════════════════════════════════════════════════════════
# wait_for_port  PORT  LABEL  [MAX_SECONDS]
#   Polls localhost:PORT until it responds (HTTP 000+ is fine) or times out.
# ═══════════════════════════════════════════════════════════════════════
wait_for_port() {
  local port=$1 label=$2 max=${3:-30} elapsed=0
  while ! curl -s -o /dev/null --connect-timeout 1 "http://localhost:$port" 2>/dev/null; do
    sleep 1
    elapsed=$((elapsed + 1))
    if [ "$elapsed" -ge "$max" ]; then
      warn "$label did not respond on :$port within ${max}s (may still be starting)"
      return 1
    fi
  done
  ok "$label is UP on :$port (${elapsed}s)"
  return 0
}

# ═══════════════════════════════════════════════════════════════════════
# kill_port  PORT
#   Kills any existing process on the port if occupied.
# ═══════════════════════════════════════════════════════════════════════
kill_port() {
  lsof -ti:"$1" | xargs kill -9 2>/dev/null || true
}

# ═══════════════════════════════════════════════════════════════════════
# run_supervised  LABEL  CWD  COMMAND...
#   Runs a command in the background. If it crashes, restarts up to 5 times.
# ═══════════════════════════════════════════════════════════════════════
run_supervised() {
  local label="$1" cwd="$2"; shift 2
  (
    local attempt=0 max_restarts=5
    while [ "$attempt" -lt "$max_restarts" ]; do
      cd "$cwd"
      "$@" &
      local pid=$!
      wait "$pid" 2>/dev/null || true
      attempt=$((attempt + 1))
      if [ "$attempt" -lt "$max_restarts" ]; then
        warn "$label crashed (attempt $attempt/$max_restarts). Restarting in 5s..."
        sleep 5
      else
        fail "$label crashed $max_restarts times. Giving up."
      fi
    done
  ) &
}

# ═══════════════════════════════════════════════════════════════════════
# PRE-FLIGHT: Check for port conflicts across ALL assigned ports
# ═══════════════════════════════════════════════════════════════════════
echo ""
printf "${BOLD}${CYAN}🚀 RM Orbit Enterprise Ecosystem — Starting...${NC}\n"
echo "═══════════════════════════════════════════════════════════════"

# Map of port → service name (for conflict detection)
declare -A PORT_MAP=(
  [45001]="Gate(AuthX)"
  [45003]="Meet-Frontend"
  [45004]="Mail-Frontend"
  [45005]="Calendar-Frontend"
  [45006]="Planet-Frontend"
  [45007]="RM-Fonts"
  [45008]="Connect-Frontend"
  [45009]="Learn-Docs"
  [45010]="Writer-Frontend"
  [45011]="ControlCenter-Frontend"
  [45012]="Secure-Frontend"
  [45013]="CapitalHub-Frontend"
  [6201]="Search-Frontend"
  [45016]="FitterMe-Frontend"
  [45018]="TurboTick-Frontend"
  [45019]="RMWallet-Frontend"
  [45020]="RMDock-Frontend"
  [45022]="Gate-Admin"
  [5173]="Atlas-Frontend"
  [8000]="Atlas-Backend"
  [8004]="Mail-Backend"
  [8077]="ControlCenter-Backend"
  [5001]="Calendar-Backend"
  [5000]="Connect-Backend"
  [6001]="Meet-Backend"
  [6004]="Secure-Backend"
  [6011]="Writer-Backend"
  [6200]="Search-Backend"
  [6100]="TurboTick-Backend"
  [6110]="RMWallet-Backend"
  [6120]="RMDock-Backend"
  [46000]="Planet-Backend"
  [6002]="FitterMe-Backend"
)

echo ""
info "Pre-flight port scan..."
CONFLICTS=0
for port in "${!PORT_MAP[@]}"; do
  pid=$(lsof -ti:"$port" 2>/dev/null || true)
  if [ -n "$pid" ]; then
    proc_name=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
    warn "Port $port (${PORT_MAP[$port]}) already in use by PID $pid ($proc_name)"
    CONFLICTS=$((CONFLICTS + 1))
  fi
done
if [ "$CONFLICTS" -eq 0 ]; then
  ok "All assigned ports are free."
else
  warn "$CONFLICTS port(s) already occupied. Existing processes will be replaced."
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: Docker Infrastructure (Gate, Mail, Connect)
# ═══════════════════════════════════════════════════════════════════════
echo "─── Phase 1: Docker Infrastructure ──────────────────────────"

# 1a. Gate (AuthX) — Port 45001
if [ -d "$ROOT_DIR/Gate" ]; then
  info "🔑 Starting Gate (AuthX)..."
  cd "$ROOT_DIR/Gate/authx"
  docker compose up -d 2>/dev/null || docker-compose up -d 2>/dev/null || warn "Gate docker compose failed"
  cd "$ROOT_DIR"
  wait_for_port 45001 "Gate(AuthX)" 60 || true
fi

# 1b. Mail — Port 45004/8004
if [ -d "$ROOT_DIR/Mail" ]; then
  info "📧 Starting Mail..."
  cd "$ROOT_DIR/Mail"
  if [ ! -f .env ]; then cp .env.example .env 2>/dev/null || true; fi
  docker compose up -d 2>/dev/null || docker-compose up -d 2>/dev/null || warn "Mail docker compose failed"
  cd "$ROOT_DIR"
  wait_for_port 45004 "Mail-Frontend" 60 || true
  wait_for_port 8004  "Mail-Backend"  60 || true
fi

# 1c. Connect — Port 45008/5000 (Docker)
if [ -d "$ROOT_DIR/Connect" ]; then
  info "💬 Starting Connect..."
  cd "$ROOT_DIR/Connect"
  docker compose up --build -d 2>/dev/null || docker-compose up --build -d 2>/dev/null || warn "Connect docker compose failed"
  cd "$ROOT_DIR"
  wait_for_port 45008 "Connect-Frontend" 90 || true
  wait_for_port 5000  "Connect-Backend"  90 || true
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: Native Backends (must start before their frontends)
# ═══════════════════════════════════════════════════════════════════════
echo "─── Phase 2: Native Backends ────────────────────────────────"

# 2a. Atlas Backend — Port 8000
if [ -d "$ROOT_DIR/Atlas/backend" ]; then
  info "🗺️  Starting Atlas Backend..."
  kill_port 8000
  run_supervised "Atlas-Backend" "$ROOT_DIR/Atlas/backend" \
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  wait_for_port 8000 "Atlas-Backend" 30 || true
fi

# 2b. Control Center Backend — Port 8077
if [ -d "$ROOT_DIR/Control Center/server" ]; then
  info "⚙️  Starting Control Center Backend..."
  kill_port 8077
  run_supervised "CC-Backend" "$ROOT_DIR/Control Center/server" \
    npm run dev
  wait_for_port 8077 "ControlCenter-Backend" 30 || true
fi

# 2c. Calendar Backend — Port 5001
if [ -d "$ROOT_DIR/Calendar/server" ]; then
  info "📅 Starting Calendar Backend..."
  kill_port 5001
  run_supervised "Calendar-Backend" "$ROOT_DIR/Calendar/server" \
    npm start
  wait_for_port 5001 "Calendar-Backend" 30 || true
fi

# 2d. Meet Backend — Port 6001
if [ -d "$ROOT_DIR/Meet/server" ]; then
  info "🎥 Starting Meet Backend..."
  kill_port 6001
  run_supervised "Meet-Backend" "$ROOT_DIR/Meet/server" \
    npm run dev
  wait_for_port 6001 "Meet-Backend" 30 || true
fi

# 2e. Planet Backend — Port 46000
if [ -d "$ROOT_DIR/Planet/backend" ]; then
  info "🪐 Starting Planet Backend..."
  kill_port 46000
  run_supervised "Planet-Backend" "$ROOT_DIR/Planet/backend" \
    bash -c 'python3 -m alembic upgrade head || true && uvicorn app.main:app --host 0.0.0.0 --port 46000 --reload'
  wait_for_port 46000 "Planet-Backend" 30 || true
fi

# 2f. Writer Backend — Port 6011
if [ -d "$ROOT_DIR/Writer/backend" ]; then
  info "✍️  Starting Writer Backend..."
  kill_port 6011
  run_supervised "Writer-Backend" "$ROOT_DIR/Writer/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6011'
  wait_for_port 6011 "Writer-Backend" 30 || true
fi

# 2g. Secure Backend — Port 6004 (NOT 8000!)
if [ -d "$ROOT_DIR/Secure/services/secure-service" ]; then
  info "🛡️  Starting Secure Backend..."
  kill_port 6004
  run_supervised "Secure-Backend" "$ROOT_DIR/Secure/services/secure-service" \
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6004
  wait_for_port 6004 "Secure-Backend" 30 || true
fi

# 2h. Search — Port 6200
if [ -d "$ROOT_DIR/Search/backend" ]; then
  info "🔎 Starting Orbit Search..."
  kill_port 6200
  run_supervised "Search-Backend" "$ROOT_DIR/Search/backend" \
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6200
  wait_for_port 6200 "Search-Backend" 30 || true
fi

# 2i. TurboTick Backend — Port 6100
if [ -d "$ROOT_DIR/TurboTick/backend" ]; then
  info "🎫 Starting TurboTick Backend..."
  kill_port 6100
  run_supervised "TurboTick-Backend" "$ROOT_DIR/TurboTick/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6100 --reload'
  wait_for_port 6100 "TurboTick-Backend" 30 || true
fi

# 2j. RM Wallet Backend — Port 6110
if [ -d "$ROOT_DIR/Wallet/backend" ]; then
  info "🔐 Starting RM Wallet Backend..."
  kill_port 6110
  run_supervised "RMWallet-Backend" "$ROOT_DIR/Wallet/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6110 --reload'
  wait_for_port 6110 "RMWallet-Backend" 30 || true
fi

# 2k. RM Dock Backend — Port 6120
if [ -d "$ROOT_DIR/Dock/backend" ]; then
  info "🏢 Starting RM Dock Backend..."
  kill_port 6120
  run_supervised "RMDock-Backend" "$ROOT_DIR/Dock/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6120 --reload'
  wait_for_port 6120 "RMDock-Backend" 30 || true
fi

# 2l. Capital Hub Backend — Port 6130
if [ -d "$ROOT_DIR/Capital Hub/backend" ]; then
  info "💼 Starting Capital Hub Backend..."
  kill_port 6130
  run_supervised "CapitalHub-Backend" "$ROOT_DIR/Capital Hub/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6130 --reload'
  wait_for_port 6130 "CapitalHub-Backend" 30 || true
fi

# 2m. FitterMe Backend — Port 6002
if [ -d "$ROOT_DIR/FitterMe/backend" ]; then
  info "🏃 Starting FitterMe Backend..."
  kill_port 6002
  run_supervised "FitterMe-Backend" "$ROOT_DIR/FitterMe/backend" \
    bash -c 'python3 -m alembic upgrade head || true && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 6002'
  wait_for_port 6002 "FitterMe-Backend" 30 || true
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════
# PHASE 3: Frontends (Vite / static servers)
# ═══════════════════════════════════════════════════════════════════════
echo "─── Phase 3: Frontends ──────────────────────────────────────"

# 3a. Atlas Frontend — Port 5173
if [ -d "$ROOT_DIR/Atlas/frontend" ]; then
  info "🗺️  Starting Atlas Frontend..."
  kill_port 5173
  run_supervised "Atlas-Frontend" "$ROOT_DIR/Atlas/frontend" \
    npm run dev -- --port 5173 --strictPort --host
  wait_for_port 5173 "Atlas-Frontend" 30 || true
fi

# 3b. Control Center Frontend — Port 45011
if [ -d "$ROOT_DIR/Control Center" ] && [ -f "$ROOT_DIR/Control Center/package.json" ]; then
  info "⚙️  Starting Control Center Frontend..."
  kill_port 45011
  run_supervised "CC-Frontend" "$ROOT_DIR/Control Center" \
    npm run dev -- --port 45011 --strictPort --host
  wait_for_port 45011 "ControlCenter-Frontend" 30 || true
fi

# 3c. Calendar Frontend — Port 45005
if [ -d "$ROOT_DIR/Calendar" ] && [ -f "$ROOT_DIR/Calendar/package.json" ]; then
  info "📅 Starting Calendar Frontend..."
  kill_port 45005
  run_supervised "Calendar-Frontend" "$ROOT_DIR/Calendar" \
    npm run dev -- --port 45005 --strictPort --host
  wait_for_port 45005 "Calendar-Frontend" 30 || true
fi

# 3d. Planet Frontend — Port 45006
if [ -d "$ROOT_DIR/Planet" ] && [ -f "$ROOT_DIR/Planet/package.json" ]; then
  info "🪐 Starting Planet Frontend..."
  kill_port 45006
  run_supervised "Planet-Frontend" "$ROOT_DIR/Planet" \
    npm run dev -- --port 45006 --strictPort --host
  wait_for_port 45006 "Planet-Frontend" 30 || true
fi

# 3e. Meet Frontend — Port 45003
if [ -d "$ROOT_DIR/Meet" ] && [ -f "$ROOT_DIR/Meet/package.json" ]; then
  info "🎥 Starting Meet Frontend..."
  kill_port 45003
  run_supervised "Meet-Frontend" "$ROOT_DIR/Meet" \
    npm run dev -- --port 45003 --strictPort --host
  wait_for_port 45003 "Meet-Frontend" 30 || true
fi

# 3f. RM Fonts — Port 45007 (static)
if [ -d "$ROOT_DIR/RM Fonts/RM Fonts" ]; then
  info "🔤 Starting RM Fonts..."
  kill_port 45007
  run_supervised "RM-Fonts" "$ROOT_DIR/RM Fonts/RM Fonts" \
    python3 -m http.server 45007 --bind 0.0.0.0
  wait_for_port 45007 "RM-Fonts" 10 || true
fi

# 3g. Learn Docs — Port 45009
if [ -d "$ROOT_DIR/Learn/frontend" ]; then
  info "📚 Starting Learn Docs..."
  kill_port 45009
  run_supervised "Learn-Docs" "$ROOT_DIR/Learn/frontend" \
    npm run dev -- --port 45009 --strictPort --host
  wait_for_port 45009 "Learn-Docs" 30 || true
elif [ -d "$ROOT_DIR/Learn/site" ]; then
  info "📚 Starting Learn Docs (static)..."
  kill_port 45009
  run_supervised "Learn-Docs" "$ROOT_DIR/Learn/site" \
    python3 -m http.server 45009 --bind 0.0.0.0
  wait_for_port 45009 "Learn-Docs" 10 || true
fi

# 3h. Writer Frontend — Port 45010
if [ -d "$ROOT_DIR/Writer/frontend" ]; then
  info "✍️  Starting Writer Frontend..."
  kill_port 45010
  run_supervised "Writer-Frontend" "$ROOT_DIR/Writer/frontend" \
    npm run dev -- --port 45010 --strictPort --host
  wait_for_port 45010 "Writer-Frontend" 30 || true
elif [ -d "$ROOT_DIR/Writer/site" ]; then
  info "✍️  Starting Writer Frontend (static)..."
  kill_port 45010
  run_supervised "Writer-Frontend" "$ROOT_DIR/Writer/site" \
    python3 -m http.server 45010 --bind 0.0.0.0
  wait_for_port 45010 "Writer-Frontend" 10 || true
fi

# 3i. Capital Hub — Port 45013
if [ -d "$ROOT_DIR/Capital Hub/frontend" ]; then
  info "💼 Starting Capital Hub..."
  kill_port 45013
  run_supervised "CapitalHub" "$ROOT_DIR/Capital Hub/frontend" \
    npm run dev -- --port 45013 --strictPort --host
  wait_for_port 45013 "CapitalHub" 30 || true
elif [ -d "$ROOT_DIR/Capital Hub/site" ]; then
  info "💼 Starting Capital Hub (static)..."
  kill_port 45013
  run_supervised "CapitalHub" "$ROOT_DIR/Capital Hub/site" \
    python3 -m http.server 45013 --bind 0.0.0.0
  wait_for_port 45013 "CapitalHub" 10 || true
fi

# 3j. Secure Frontend — Port 45012
if [ -d "$ROOT_DIR/Secure/frontend" ]; then
  info "🛡️  Starting Secure Frontend..."
  kill_port 45012
  # Try dev server first, fall back to build+serve
  if grep -q '"dev"' "$ROOT_DIR/Secure/frontend/package.json" 2>/dev/null; then
    run_supervised "Secure-Frontend" "$ROOT_DIR/Secure/frontend" \
      npm run dev -- --port 45012 --strictPort --host
  else
    cd "$ROOT_DIR/Secure/frontend" && npm run build 2>/dev/null || true
    run_supervised "Secure-Frontend" "$ROOT_DIR/Secure/frontend/dist" \
      python3 -m http.server 45012 --bind 0.0.0.0
  fi
  wait_for_port 45012 "Secure-Frontend" 30 || true
fi

# 3k. TurboTick Frontend — Port 45018
if [ -d "$ROOT_DIR/TurboTick/frontend" ]; then
  info "🎫 Starting TurboTick Frontend..."
  cd "$ROOT_DIR/TurboTick/frontend" && npm install --silent 2>/dev/null || true
  kill_port 45018
  run_supervised "TurboTick-Frontend" "$ROOT_DIR/TurboTick/frontend" npm run dev
  wait_for_port 45018 "TurboTick-Frontend" 45 || true
  cd "$ROOT_DIR"
fi

# 3l. RM Wallet Frontend — Port 45019
if [ -d "$ROOT_DIR/Wallet/frontend" ]; then
  info "🔐 Starting RM Wallet Frontend..."
  cd "$ROOT_DIR/Wallet/frontend" && npm install --silent 2>/dev/null || true
  kill_port 45019
  run_supervised "RMWallet-Frontend" "$ROOT_DIR/Wallet/frontend" npm run dev
  wait_for_port 45019 "RMWallet-Frontend" 45 || true
  cd "$ROOT_DIR"
fi

# 3m. RM Dock Frontend — Port 45020
if [ -d "$ROOT_DIR/Dock/frontend" ]; then
  info "🏢 Starting RM Dock Frontend..."
  cd "$ROOT_DIR/Dock/frontend" && npm install --silent 2>/dev/null || true
  kill_port 45020
  run_supervised "RMDock-Frontend" "$ROOT_DIR/Dock/frontend" npm run dev
  wait_for_port 45020 "RMDock-Frontend" 45 || true
  cd "$ROOT_DIR"
fi

# 3n. FitterMe Frontend — Port 45016 (backend is Docker-managed separately)
if [ -d "$ROOT_DIR/FitterMe/frontend" ]; then
  info "🏃 Starting FitterMe Frontend..."
  cd "$ROOT_DIR/FitterMe/frontend" && npm install --silent 2>/dev/null || true
  kill_port 45016
  run_supervised "FitterMe-Frontend" "$ROOT_DIR/FitterMe/frontend" npm run dev
  wait_for_port 45016 "FitterMe-Frontend" 45 || true
  cd "$ROOT_DIR"
fi

# 3o. Gate Admin Portal — Port 45022
if [ -d "$ROOT_DIR/Gate/admin" ]; then
  info "🔑 Starting Gate Admin Portal..."
  cd "$ROOT_DIR/Gate/admin" && npm install --silent 2>/dev/null || true
  kill_port 45022
  run_supervised "Gate-Admin" "$ROOT_DIR/Gate/admin" npm run dev
  wait_for_port 45022 "Gate-Admin" 45 || true
  cd "$ROOT_DIR"
fi

# 3p. Search Frontend — Port 6201
if [ -d "$ROOT_DIR/Search/frontend" ]; then
  info "🔎 Starting Search Frontend..."
  cd "$ROOT_DIR/Search/frontend" && npm install --silent 2>/dev/null || true
  kill_port 6201
  run_supervised "Search-Frontend" "$ROOT_DIR/Search/frontend" npm run dev
  wait_for_port 6201 "Search-Frontend" 45 || true
  cd "$ROOT_DIR"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════
# PHASE 4: Snitch Ecosystem (Prototype services)
# ═══════════════════════════════════════════════════════════════════════
echo "─── Phase 4: Snitch Ecosystem ───────────────────────────────"

if [ -d "$ROOT_DIR/Snitch/backend" ]; then
  info "🧪 Starting Snitch backend services..."
  cd "$ROOT_DIR/Snitch/backend" && npm install --silent 2>/dev/null || true
  run_supervised "Snitch-Backend"   "$ROOT_DIR/Snitch/backend" npm run dev
  run_supervised "Snitch-Learn"     "$ROOT_DIR/Snitch/backend" npm run learn
  run_supervised "Snitch-CapHub"    "$ROOT_DIR/Snitch/backend" npm run capitalhub
  run_supervised "Snitch-Secure"    "$ROOT_DIR/Snitch/backend" npm run secure
  run_supervised "Snitch-EventBus"  "$ROOT_DIR/Snitch/backend" npm run eventbus
  run_supervised "Snitch-TURN"      "$ROOT_DIR/Snitch/backend" npm run turn
  run_supervised "Snitch-Media"     "$ROOT_DIR/Snitch/backend" npm run media
  cd "$ROOT_DIR"
fi

if [ -d "$ROOT_DIR/Snitch/frontend" ]; then
  info "🌐 Starting Snitch frontend..."
  cd "$ROOT_DIR/Snitch/frontend" && npm install --silent 2>/dev/null || true
  kill_port 5179
  run_supervised "Snitch-Frontend" "$ROOT_DIR/Snitch/frontend" \
    npm run dev -- --port 5179 --strictPort --host
  wait_for_port 5179 "Snitch-Frontend" 30 || true
  cd "$ROOT_DIR"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════════
echo "═══════════════════════════════════════════════════════════════"
printf "${BOLD}${GREEN}✅ Ecosystem Initialization Complete${NC}\n"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  🔑 Gate (AuthX)           → http://localhost:45001"
echo "  📧 Mail Frontend          → http://localhost:45004"
echo "  📧 Mail Backend           → http://localhost:8004"
echo "  💬 Connect Frontend       → http://localhost:45008"
echo "  💬 Connect Backend        → http://localhost:5000"
echo "  🗺️  Atlas Frontend         → http://localhost:5173"
echo "  🗺️  Atlas Backend          → http://localhost:8000"
echo "  ⚙️  Control Center         → http://localhost:45011"
echo "  ⚙️  CC Backend             → http://localhost:8077"
echo "  📅 Chronos Calendar       → http://localhost:45005"
echo "  📅 Calendar Backend       → http://localhost:5001"
echo "  🪐 Planet                 → http://localhost:45006"
echo "  🪐 Planet Backend         → http://localhost:46000"
echo "  🎥 Meet                   → http://localhost:45003"
echo "  🎥 Meet Backend           → http://localhost:6001"
echo "  🔤 RM Fonts               → http://localhost:45007"
echo "  📚 Learn Docs             → http://localhost:45009"
echo "  ✍️  Writer                  → http://localhost:45010"
echo "  ✍️  Writer Backend          → http://localhost:6011"
echo "  💼 Capital Hub            → http://localhost:45013"
echo "  🛡️  Secure                 → http://localhost:45012"
echo "  🛡️  Secure Backend         → http://localhost:6004"
echo "  🔎 Search Backend         → http://localhost:6200"
echo "  🔎 Search Frontend        → http://localhost:6201"
echo "  🎫 TurboTick              → http://localhost:45018"
echo "  🎫 TurboTick Backend      → http://localhost:6100"
echo "  🔐 RM Wallet              → http://localhost:45019"
echo "  🔐 RM Wallet Backend      → http://localhost:6110"
echo "  🏢 RM Dock                → http://localhost:45020"
echo "  🏢 RM Dock Backend        → http://localhost:6120"
echo "  🏃 FitterMe               → http://localhost:45016"
echo "  🔑 Gate Admin Portal      → http://localhost:45022"
echo "  🧪 Snitch Frontend        → http://localhost:5179"
echo ""
echo "Use './status.sh' to monitor health."
echo "═══════════════════════════════════════════════════════════════"
