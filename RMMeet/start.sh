#!/bin/bash
# RMMeet Guest Join Frontend — port 45026
# Proxies /api and /socket.io to Meet backend on :6001
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_BIN="/home/sasi/.nvm/versions/node/v22.14.0/bin/node"

# Kill any squatter on 45026
lsof -ti:45026 | xargs kill -9 2>/dev/null || true

echo "Starting RMMeet Guest Frontend on :45026 ..."
cd "$ROOT_DIR"
"$NODE_BIN" ./node_modules/.bin/vite --port 45026 --strictPort --host > "$ROOT_DIR/frontend.log" 2>&1 &

echo "RMMeet guest frontend started in background. Log: $ROOT_DIR/frontend.log"
