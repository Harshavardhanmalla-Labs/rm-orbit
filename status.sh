#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# RM Orbit Ecosystem – Health Dashboard
# ═══════════════════════════════════════════════════════════════════════
set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

printf "\n${BOLD}${CYAN}📊 RM Orbit Ecosystem Health Dashboard${NC}\n"
echo "═══════════════════════════════════════════════════════════════"
printf "  %-28s  %6s  %s\n" "SERVICE" "PORT" "STATUS"
echo "───────────────────────────────────────────────────────────────"

check_port() {
  local label="$1" port="$2"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://localhost:$port" 2>/dev/null || true)
  if [ -z "$status" ] || [ "$status" = "000" ]; then
    printf "  %-28s  %6s  ${RED}● DOWN${NC}\n" "$label" "$port"
  else
    printf "  %-28s  %6s  ${GREEN}● UP${NC} ${DIM}(HTTP $status)${NC}\n" "$label" "$port"
  fi
}

echo ""
printf "${BOLD}  Docker Services:${NC}\n"
check_port "Gate (AuthX)"         45001
check_port "Mail Frontend"        45004
check_port "Mail Backend"         8004
check_port "Connect Frontend"     45008
check_port "Connect Backend"      5000

echo ""
printf "${BOLD}  Native Backends:${NC}\n"
check_port "Atlas Backend"        8000
check_port "CC Backend"           8077
check_port "Calendar Backend"     5001
check_port "Meet Backend"         6001
check_port "Planet Backend"       46000
check_port "Writer Backend"       6011
check_port "Secure Backend"       6004
check_port "Search Backend"       6200
check_port "TurboTick Backend"    6100
check_port "RM Wallet Backend"    6110
check_port "RM Dock Backend"      6120

echo ""
printf "${BOLD}  Frontends:${NC}\n"
check_port "Atlas Frontend"       5173
check_port "Control Center"       45011
check_port "Calendar"             45005
check_port "Planet"               45006
check_port "Meet"                 45003
check_port "RM Fonts"             45007
check_port "Learn Docs"           45009
check_port "Writer"               45010
check_port "Capital Hub"          45013
check_port "Secure"               45012
check_port "TurboTick"            45018
check_port "RM Wallet"            45019
check_port "RM Dock"              45020

echo ""
printf "${BOLD}  Prototypes:${NC}\n"
check_port "Snitch Frontend"      5179

echo ""

# ─── Docker overview ──────────────────────────────────────────────────
printf "${BOLD}  Docker Containers:${NC}\n"
if command -v docker >/dev/null 2>&1; then
  docker ps --format "    {{.Names}}\t{{.Status}}" 2>/dev/null | head -20
  STOPPED=$(docker ps -a --filter "status=restarting" --filter "status=exited" --format "{{.Names}}" 2>/dev/null)
  if [ -n "$STOPPED" ]; then
    echo ""
    printf "  ${RED}Crash-looping / stopped containers:${NC}\n"
    echo "$STOPPED" | while read -r name; do
      printf "    ${RED}● $name${NC}\n"
    done
  fi
else
  printf "    ${DIM}Docker not found.${NC}\n"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
