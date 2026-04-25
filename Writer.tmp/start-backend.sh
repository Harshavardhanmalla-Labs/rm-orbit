#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
PORT="${WRITER_BACKEND_PORT:-6011}"
HOST="${WRITER_BACKEND_HOST:-0.0.0.0}"
LOG_FILE="$ROOT_DIR/backend.log"
DATABASE_URL="${WRITER_DATABASE_URL:-sqlite:///$ROOT_DIR/data/writer.db}"
DB_INIT_MODE="${WRITER_DB_INIT_MODE:-}"
MIGRATE_ON_START="${WRITER_MIGRATE_ON_START:-1}"

if [ ! -d "$BACKEND_DIR" ]; then
  echo "Writer backend directory not found: $BACKEND_DIR"
  exit 1
fi

if ! python3 -c "import fastapi, sqlalchemy, uvicorn, jwt" >/dev/null 2>&1; then
  echo "Writer backend dependencies missing (fastapi/sqlalchemy/uvicorn/PyJWT)."
  echo "Install with: pip install -r Writer/backend/requirements.txt"
  exit 1
fi

cd "$BACKEND_DIR"
lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true

if [ "$MIGRATE_ON_START" = "1" ]; then
  if ! python3 -c "import alembic" >/dev/null 2>&1; then
    echo "Alembic is required for WRITER_MIGRATE_ON_START=1."
    echo "Install with: pip install -r Writer/backend/requirements.txt"
    exit 1
  fi
  run_migrations() {
    if WRITER_DATABASE_URL="$DATABASE_URL" python3 -m alembic upgrade head; then
      return 0
    fi

    echo "Alembic upgrade failed. Checking for legacy schema bootstrap state..."
    if WRITER_DATABASE_URL="$DATABASE_URL" python3 - <<'PY'
import os
import sys

from sqlalchemy import create_engine, inspect

url = os.environ["WRITER_DATABASE_URL"]
required_tables = {"documents", "blocks", "block_relations", "block_versions"}
engine = create_engine(url, future=True)

has_alembic_revision = False
with engine.connect() as connection:
    inspector = inspect(connection)
    existing_tables = set(inspector.get_table_names())
    if "alembic_version" in existing_tables:
        result = connection.exec_driver_sql("SELECT COUNT(*) FROM alembic_version")
        has_alembic_revision = int(result.scalar() or 0) > 0
missing_tables = required_tables - existing_tables

if not missing_tables and not has_alembic_revision:
    sys.exit(0)

sys.exit(1)
PY
    then
      echo "Detected existing Writer schema without Alembic metadata. Stamping head."
      WRITER_DATABASE_URL="$DATABASE_URL" python3 -m alembic stamp head
      WRITER_DATABASE_URL="$DATABASE_URL" python3 -m alembic upgrade head
      return 0
    fi

    echo "Writer migrations failed and could not be auto-recovered."
    return 1
  }

  run_migrations
fi

if [ -z "$DB_INIT_MODE" ] && [[ "$DATABASE_URL" == postgresql* ]]; then
  DB_INIT_MODE="skip"
fi

echo "Starting RM Writer backend on http://localhost:${PORT}"
WRITER_DATABASE_URL="$DATABASE_URL" WRITER_DB_INIT_MODE="$DB_INIT_MODE" \
  python3 -m uvicorn app.main:app --host "$HOST" --port "$PORT" >"$LOG_FILE" 2>&1 &
echo "RM Writer backend running in background (log: $LOG_FILE)."
