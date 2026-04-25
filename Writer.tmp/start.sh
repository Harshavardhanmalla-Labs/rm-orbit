#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${WRITER_PORT:-45010}"
HOST="${WRITER_HOST:-0.0.0.0}"
LOG_FILE="$ROOT_DIR/frontend.log"
BACKEND_START_SCRIPT="$ROOT_DIR/start-backend.sh"
START_BACKEND="${WRITER_START_BACKEND:-1}"

if [ "$START_BACKEND" = "1" ] && [ -x "$BACKEND_START_SCRIPT" ]; then
  if ! "$BACKEND_START_SCRIPT"; then
    echo "RM Writer backend failed to start."
    exit 1
  fi
fi

echo "Starting RM Writer UI on http://${HOST}:${PORT}"
lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true

cd "$ROOT_DIR/frontend"
npm install
nohup npm run dev -- --port "$PORT" --strictPort --host "$HOST" > "$LOG_FILE" 2>&1 &
echo "RM Writer UI running in background (log: $LOG_FILE)."
