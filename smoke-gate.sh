#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRITER_FRONTEND_PORT="${WRITER_PORT:-45010}"
WRITER_BACKEND_PORT="${WRITER_BACKEND_PORT:-6011}"
MEET_BACKEND_PORT="${MEET_BACKEND_PORT:-6001}"
SEARCH_PORT="${SEARCH_PORT:-6200}"

WRITER_UI_PID=""
WRITER_API_PID=""
MEET_PID=""
SEARCH_PID=""

cleanup() {
  if [[ -n "$WRITER_UI_PID" ]]; then
    kill "$WRITER_UI_PID" 2>/dev/null || true
  fi
  if [[ -n "$WRITER_API_PID" ]]; then
    kill "$WRITER_API_PID" 2>/dev/null || true
  fi
  if [[ -n "$MEET_PID" ]]; then
    kill "$MEET_PID" 2>/dev/null || true
  fi
  if [[ -n "$SEARCH_PID" ]]; then
    kill "$SEARCH_PID" 2>/dev/null || true
  fi
}

wait_for_http() {
  local url="$1"
  local attempts="${2:-30}"
  local delay="${3:-0.5}"
  local i
  for ((i = 1; i <= attempts; i++)); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep "$delay"
  done
  echo "Timed out waiting for $url"
  return 1
}

trap cleanup EXIT

echo "==> Building Writer static site"
bash -lc "cd \"$ROOT_DIR/Writer\" && ./build-site.sh"

echo "==> Starting Writer UI"
(
  cd "$ROOT_DIR/Writer/site"
  python3 -m http.server "$WRITER_FRONTEND_PORT" --bind 127.0.0.1 > "$ROOT_DIR/Writer/frontend.log" 2>&1
) &
WRITER_UI_PID=$!

echo "==> Starting Writer backend"
(
  cd "$ROOT_DIR/Writer/backend"
  WRITER_DATABASE_URL="sqlite:///$ROOT_DIR/Writer/data/smoke-writer.db" \
    python3 -m uvicorn app.main:app --host 127.0.0.1 --port "$WRITER_BACKEND_PORT" > "$ROOT_DIR/Writer/backend.log" 2>&1
) &
WRITER_API_PID=$!

wait_for_http "http://127.0.0.1:${WRITER_FRONTEND_PORT}/index.html"
wait_for_http "http://127.0.0.1:${WRITER_BACKEND_PORT}/health"

echo "==> Verifying Writer API mutation flow"
curl -fsS -X POST \
  "http://127.0.0.1:${WRITER_BACKEND_PORT}/api/documents" \
  -H "X-Workspace-Id: smoke-workspace" \
  -H "X-Org-Id: smoke-org" \
  -H "Content-Type: application/json" \
  -d '{"title":"Smoke Gate Doc"}' >/tmp/writer-smoke-doc.json

python3 - <<'PY'
import json
from pathlib import Path
payload = json.loads(Path("/tmp/writer-smoke-doc.json").read_text(encoding="utf-8"))
assert payload.get("id"), "Writer smoke create document did not return id"
print("Writer smoke doc id:", payload["id"])
PY

echo "==> Starting Meet backend"
(
  cd "$ROOT_DIR/Meet/server"
  node index.js > "$ROOT_DIR/Meet/server/smoke.log" 2>&1
) &
MEET_PID=$!

wait_for_http "http://127.0.0.1:${MEET_BACKEND_PORT}/health"
echo "Meet health endpoint reachable."

echo "==> Starting Search aggregator"
(
  cd "$ROOT_DIR/Search/backend"
  SEARCH_WRITER_API_BASE="http://127.0.0.1:${WRITER_BACKEND_PORT}" \
    python3 -m uvicorn app.main:app --host 127.0.0.1 --port "$SEARCH_PORT" > "$ROOT_DIR/Search/backend.log" 2>&1
) &
SEARCH_PID=$!

wait_for_http "http://127.0.0.1:${SEARCH_PORT}/health"
echo "Search health endpoint reachable."

echo "==> Verifying Search API aggregation flow"
curl -fsS \
  "http://127.0.0.1:${SEARCH_PORT}/api/search?q=smoke&limit=5" \
  -H "X-Workspace-Id: smoke-workspace" \
  -H "X-Org-Id: smoke-org" >/tmp/search-smoke-results.json

python3 - <<'PY'
import json
from pathlib import Path
payload = json.loads(Path("/tmp/search-smoke-results.json").read_text(encoding="utf-8"))
assert payload.get("total", 0) >= 1, "Search smoke did not return any results"
sources = {item.get("source") for item in payload.get("results", [])}
assert "writer" in sources, "Search smoke did not include writer results"
print("Search smoke result count:", payload["total"])
PY

echo ""
echo "Smoke gate passed."
