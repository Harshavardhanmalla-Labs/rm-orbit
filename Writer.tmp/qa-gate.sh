#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

printf "\n==> Writer backend tests\n"
(
  cd "$ROOT_DIR/backend"
  pytest -q
)

printf "\n==> Writer frontend lint\n"
(
  cd "$ROOT_DIR/frontend"
  npm run lint
)

printf "\n==> Writer frontend build\n"
(
  cd "$ROOT_DIR/frontend"
  npm run build
)

printf "\nWriter QA gate passed.\n"
