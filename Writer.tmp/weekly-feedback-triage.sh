#!/usr/bin/env bash
set -euo pipefail

WRITER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$WRITER_DIR/scripts/generate_feedback_triage_report.py" "$@"
