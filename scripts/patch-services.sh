#!/bin/bash
# patch-services.sh — inject ExecStartPre=orbit-claim-port into every service
# file listed in ports.json.
#
# Safe to re-run: skips files that already have orbit-claim-port.
# Creates .bak backup of each file before editing.
#
# Usage:
#   ./scripts/patch-services.sh              # dry-run (shows what would change)
#   ./scripts/patch-services.sh --apply      # applies changes + reloads systemd

REGISTRY="$(dirname "$0")/ports.json"
APPLY="${1:-}"
CLAIM_BIN="/home/sasi/.local/bin/orbit-claim-port"
SERVICE_DIRS=(
    "/home/sasi/.config/systemd/user"
    "/home/sasi/.aibookly"
)

if [[ ! -f "$REGISTRY" ]]; then
    echo "ERROR: ports.json not found at $REGISTRY" >&2; exit 1
fi
if [[ ! -x "$CLAIM_BIN" ]]; then
    echo "ERROR: $CLAIM_BIN not found or not executable" >&2; exit 1
fi

GREEN="\033[32m"; YELLOW="\033[33m"; RESET="\033[0m"; BOLD="\033[1m"
CHANGED=0; SKIPPED=0; NOTFOUND=0

patch_service() {
    local service="$1" port="$2"
    local svc_file=""

    for dir in "${SERVICE_DIRS[@]}"; do
        [[ -f "$dir/${service}.service" ]] && svc_file="$dir/${service}.service" && break
    done

    if [[ -z "$svc_file" ]]; then
        echo -e "  ${YELLOW}NOT FOUND${RESET}  ${service}.service"
        NOTFOUND=$((NOTFOUND + 1))
        return
    fi

    if grep -q "orbit-claim-port" "$svc_file" 2>/dev/null; then
        echo -e "  ${GREEN}SKIP${RESET}       $svc_file  (already patched)"
        SKIPPED=$((SKIPPED + 1))
        return
    fi

    local inject="ExecStartPre=$CLAIM_BIN $service $port"

    if [[ "$APPLY" != "--apply" ]]; then
        echo -e "  ${BOLD}WOULD PATCH${RESET}  $svc_file"
        echo "             + $inject"
        CHANGED=$((CHANGED + 1))
        return
    fi

    cp "$svc_file" "${svc_file}.bak"
    # Insert ExecStartPre immediately before the first ExecStart= line
    sed -i "s|^ExecStart=|${inject}\nExecStart=|" "$svc_file"
    echo -e "  ${GREEN}PATCHED${RESET}    $svc_file"
    CHANGED=$((CHANGED + 1))
}

echo ""
if [[ "$APPLY" == "--apply" ]]; then
    echo -e "${BOLD}Patching service files…${RESET}\n"
else
    echo -e "${BOLD}Dry run — pass --apply to write changes:${RESET}\n"
fi

# Read ports.json via python into a temp file, then iterate
TMPFILE=$(mktemp)
python3 -c "
import json, sys
with open('$REGISTRY') as f:
    reg = {k: v for k, v in json.load(f).items() if not k.startswith('_')}
for service, port in sorted(reg.items()):
    print(service, port)
" > "$TMPFILE"

while read -r service port; do
    patch_service "$service" "$port"
done < "$TMPFILE"
rm -f "$TMPFILE"

echo ""
echo "────────────────────────────────────────"
printf "  Changed : %d\n" "$CHANGED"
printf "  Skipped : %d  (already patched)\n" "$SKIPPED"
printf "  Missing : %d  (service file not found)\n" "$NOTFOUND"
echo ""

if [[ "$APPLY" == "--apply" && $CHANGED -gt 0 ]]; then
    echo "Reloading systemd daemon…"
    systemctl --user daemon-reload && echo "Done." || echo "Reload failed"
fi

if [[ "$APPLY" != "--apply" && $CHANGED -gt 0 ]]; then
    echo "Run with --apply to apply these changes."
fi
