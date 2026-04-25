#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

DATABASE_URL="${WRITER_DATABASE_URL:-sqlite:///../data/writer.db}"

echo "Running Writer migrations on: $DATABASE_URL"
WRITER_DATABASE_URL="$DATABASE_URL" python3 -m alembic upgrade head
echo "Writer migrations complete."
