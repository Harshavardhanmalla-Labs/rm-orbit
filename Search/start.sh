#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
PORT="${SEARCH_PORT:-6200}"
HOST="${SEARCH_HOST:-0.0.0.0}"
LOG_FILE="$ROOT_DIR/backend.log"

if [ ! -d "$BACKEND_DIR" ]; then
  echo "Search backend directory not found: $BACKEND_DIR"
  exit 1
fi

if ! python3 -c "import fastapi, uvicorn, pydantic" >/dev/null 2>&1; then
  echo "Search backend dependencies missing (fastapi/uvicorn/pydantic)."
  echo "Install with: pip install -r Search/backend/requirements.txt"
  exit 1
fi

cd "$BACKEND_DIR"
lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true

echo "Starting Orbit Search on http://localhost:${PORT}"
python3 -m uvicorn app.main:app --host "$HOST" --port "$PORT" >"$LOG_FILE" 2>&1 &
echo "Orbit Search running in background (log: $LOG_FILE)."
