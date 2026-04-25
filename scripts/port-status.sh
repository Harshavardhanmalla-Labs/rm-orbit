#!/bin/bash
# port-status.sh — show live status of every registered RM Orbit port.
# Usage:  ./scripts/port-status.sh [--conflicts-only]
#
# Columns: SERVICE  PORT  STATUS  PID  PROCESS

REGISTRY="$(dirname "$0")/ports.json"
CONFLICTS_ONLY="${1:-}"

if [[ ! -f "$REGISTRY" ]]; then
    echo "ERROR: ports.json not found at $REGISTRY" >&2
    exit 1
fi

python3 - "$REGISTRY" "$CONFLICTS_ONLY" <<'PYEOF'
import json, subprocess, sys, os

registry_path = sys.argv[1]
conflicts_only = sys.argv[2] == "--conflicts-only" if len(sys.argv) > 2 else False

with open(registry_path) as f:
    registry = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

uid_dir = f"/run/user/{os.getuid()}/orbit-ports"

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

print(f"\n{BOLD}{'SERVICE':<32} {'PORT':>6}  {'STATUS':<8}  {'PID':<7}  PROCESS{RESET}")
print("─" * 80)

conflicts = []

for service, port in sorted(registry.items(), key=lambda x: x[1]):
    result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
    pids = result.stdout.strip().split() if result.stdout.strip() else []

    if not pids:
        if not conflicts_only:
            print(f"{'  ' + service:<32} {port:>6}  {RED}DOWN{RESET}     {'—':<7}  (nothing on port)")
        continue

    pid = pids[0]
    cmd = subprocess.run(["ps", "-p", pid, "-o", "args="], capture_output=True, text=True).stdout.strip()[:60]

    # Check who last claimed this port
    owner_file = f"{uid_dir}/{port}.owner"
    last_owner = open(owner_file).read().strip() if os.path.exists(owner_file) else "unknown"

    is_conflict = last_owner != service and last_owner != "unknown"

    if is_conflict:
        conflicts.append((service, port, pid, cmd, last_owner))
        print(f"{'  ' + service:<32} {port:>6}  {RED}CONFLICT{RESET}  {pid:<7}  {cmd}")
        print(f"{'':32}        {YELLOW}^ last claimed by: {last_owner}{RESET}")
    elif not conflicts_only:
        print(f"{'  ' + service:<32} {port:>6}  {GREEN}UP{RESET}        {pid:<7}  {cmd}")

print()
if conflicts:
    print(f"{RED}{BOLD}⚠  {len(conflicts)} port conflict(s) detected.{RESET}")
    print(f"   Run: systemctl --user restart <service>  to reclaim its port.\n")
else:
    print(f"{GREEN}{BOLD}✓  No port conflicts.{RESET}\n")
PYEOF
