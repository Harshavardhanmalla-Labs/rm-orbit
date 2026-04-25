#!/usr/bin/env bash
# RM Orbit Research Platform — top-level launcher
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ACTION="${1:-start}"

start_lite_services() {
  echo "[Research] Starting lightweight support service (LanguageTool)..."
  docker compose up -d languagetool --remove-orphans
  echo "[Research] Waiting for LanguageTool to be ready..."
  for i in $(seq 1 20); do
    if curl -sf http://localhost:8072/v2/languages > /dev/null 2>&1; then
      echo "[Research] LanguageTool ready."
      return
    fi
    sleep 3
  done
  echo "[Research] WARNING: LanguageTool did not become ready in time."
}

start_full_services() {
  echo "[Research] Starting full support stack (GROBID + LanguageTool + Nougat)..."
  echo "[Research] This can download several GB the first time."
  docker compose up -d grobid languagetool nougat --remove-orphans
}

start_backend() {
  echo "[Research] Starting backend API on port 6420..."
  cd "$SCRIPT_DIR/backend"
  bash start.sh &
  BACKEND_PID=$!
  echo "[Research] Backend PID: $BACKEND_PID"
}

start_frontend() {
  echo "[Research] Starting frontend on port 10007..."
  cd "$SCRIPT_DIR/frontend"
  npm run dev &
  FRONTEND_PID=$!
  echo "[Research] Frontend PID: $FRONTEND_PID"
}

case "$ACTION" in
  start)
    start_lite_services
    start_backend
    start_frontend
    echo ""
    echo "  Research Platform running:"
    echo "  Frontend : http://localhost:10007"
    echo "  API      : http://localhost:6420"
    echo "  LangTool : http://localhost:8072"
    echo "  Brain    : http://localhost:6420/api/system/brain"
    echo ""
    wait
    ;;
  services)
    start_lite_services
    ;;
  full-services)
    start_full_services
    ;;
  brain)
    curl -sf http://localhost:6420/api/system/brain
    echo ""
    ;;
  test)
    cd "$SCRIPT_DIR/backend"
    ./test.sh
    ;;
  backend)
    start_backend
    wait
    ;;
  frontend)
    start_frontend
    wait
    ;;
  stop)
    docker compose down
    echo "[Research] Services stopped."
    ;;
  *)
    echo "Usage: ./start.sh [start|services|full-services|backend|frontend|brain|test|stop]"
    ;;
esac
