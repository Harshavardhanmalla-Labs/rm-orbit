#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_step() {
  local name="$1"
  shift

  echo ""
  echo "==> ${name}"
  "$@"
}

run_step "Atlas envelope contract tests" \
  bash -lc "cd \"$ROOT_DIR/Atlas/backend\" && python3 -m unittest tests.test_ecosystem_event_contract tests.test_ecosystem_event_fixtures"

run_step "Calendar publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Calendar/server\" && node --test eventbus-contract.test.js"

run_step "Planet publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Planet/backend\" && python3 -m unittest tests.test_eventbus_contract"

run_step "Mail publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Mail/backend\" && PYTHONPATH=. pytest -q tests/test_eventbus_contract.py"

run_step "Connect envelope contract tests" \
  bash -lc "cd \"$ROOT_DIR/Connect/server\" && node --test event-envelope.test.js eventbus-consumer.test.js ecosystem-event-fixtures.test.js"

run_step "Meet publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Meet/server\" && node --test eventbus-contract.test.js"

run_step "Capital Hub publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Capital Hub/node-extension\" && node --test capitalhub-service.test.js"

run_step "Secure publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Secure/node-extension\" && node --test secure-service.test.js"

run_step "Writer publisher contract tests" \
  bash -lc "cd \"$ROOT_DIR/Writer/backend\" && pytest -q tests/test_eventbus_contract.py"

echo ""
echo "Contract gate passed."
