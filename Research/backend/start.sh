#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[Research API] Starting on port 6420..."

# Create required directories
mkdir -p uploads exports logs

# Install deps if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "[Research API] Installing dependencies..."
  pip install -r requirements.txt -q
fi

# Check configured LLM provider
LLM_PROVIDER="${RESEARCH_LLM_PROVIDER:-ollama}"
LLM_MODEL="${RESEARCH_LLM_MODEL:-gemma4:e4b}"
echo "[Research API] LLM provider: $LLM_PROVIDER / model: $LLM_MODEL"
if [ "$LLM_PROVIDER" = "ollama" ] && ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "[Research API] WARNING: Ollama not reachable at localhost:11434 — AI generation will fail"
elif [ "$LLM_PROVIDER" != "ollama" ] && [ -z "${RESEARCH_LLM_API_KEY:-}" ]; then
  echo "[Research API] WARNING: RESEARCH_LLM_API_KEY is not set — API generation will fail"
fi

# Check GROBID
if ! curl -sf http://localhost:8070/api/isalive > /dev/null 2>&1; then
  echo "[Research API] WARNING: GROBID not running on port 8070 — run: docker compose up grobid -d"
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 6420 --reload
