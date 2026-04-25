#!/usr/bin/env bash

set -euo pipefail

# RM_ORBIT_PRE_PUSH_HOOK

REPO_ROOT="$(git rev-parse --show-toplevel)"
ORBIT_ROOT="$(cd "${REPO_ROOT}/.." && pwd)"

RUNTIME_GATE="${ORBIT_ROOT}/runtime-matrix-gate.sh"
CONTRACT_GATE="${ORBIT_ROOT}/contract-gate.sh"

if [[ ! -x "${RUNTIME_GATE}" || ! -x "${CONTRACT_GATE}" ]]; then
  echo "[pre-push] Orbit gates not found at ${ORBIT_ROOT}. Skipping checks."
  exit 0
fi

echo "[pre-push] Running runtime matrix gate..."
"${RUNTIME_GATE}"

echo "[pre-push] Running envelope contract gate..."
"${CONTRACT_GATE}"
