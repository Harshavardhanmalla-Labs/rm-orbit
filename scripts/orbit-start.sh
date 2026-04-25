#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# RM Orbit — Start All Apps with PM2 (100% Uptime)
# ═══════════════════════════════════════════════════════════════════════
# Usage:
#   ./scripts/orbit-start.sh          # Start all Orbit apps
#   ./scripts/orbit-start.sh --save   # Start + persist across reboots
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ORBIT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$ORBIT_ROOT"

echo "╔══════════════════════════════════════════╗"
echo "║       RM Orbit — Starting All Apps       ║"
echo "╚══════════════════════════════════════════╝"

# Ensure pm2 is installed
if ! command -v pm2 &>/dev/null; then
  echo "[!] pm2 not found. Installing globally..."
  npm install -g pm2
fi

# Create log directories for all apps
APPS=(Atlas Calendar "Capital Hub" Connect "Control Center" Dock EventBus FitterMe Gate Learn Mail Meet OrbitShell Planet Scribe Search Secure TurboTick Wallet Writer)
for app in "${APPS[@]}"; do
  mkdir -p "$ORBIT_ROOT/$app/logs" 2>/dev/null || true
done

# Stop any existing Orbit processes cleanly
echo "[*] Stopping existing Orbit processes..."
pm2 delete ecosystem.config.cjs 2>/dev/null || true

# Start all apps
echo "[*] Starting all Orbit apps..."
pm2 start ecosystem.config.cjs

# Save process list so PM2 can restore on reboot
if [[ "${1:-}" == "--save" ]]; then
  echo "[*] Saving process list for auto-restart on reboot..."
  pm2 save
  pm2 startup 2>/dev/null || echo "[!] Run 'sudo env PATH=\$PATH:\$(which node) pm2 startup' manually for boot persistence"
fi

echo ""
echo "[+] All Orbit apps started. Use these commands:"
echo "    pm2 status          — see all app statuses"
echo "    pm2 monit           — live monitoring dashboard"
echo "    pm2 logs <name>     — tail specific app logs"
echo "    pm2 restart all     — restart everything"
echo "    pm2 save            — save for reboot persistence"
echo ""
pm2 status
