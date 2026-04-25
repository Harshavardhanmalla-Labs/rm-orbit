#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR/backend"
python3 -m alembic upgrade head || echo "Alembic upgrade failed (or no revisions)"
exec uvicorn app.main:app --host 0.0.0.0 --port 6110 --reload
