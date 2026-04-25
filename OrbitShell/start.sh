#!/bin/bash
# Start the Orbit Shell backend
set -e

cd "$(dirname "$0")/backend"

# Create virtualenv if needed
if [ ! -d ".venv" ]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
fi

source .venv/bin/activate

# Install / sync deps
pip install -q -r requirements.txt

# Copy env if first run
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  Created .env from template. Set ANTHROPIC_API_KEY before running."
    echo "   Edit: $(pwd)/.env"
    echo ""
    exit 1
  fi
fi

PORT=${ORBIT_SHELL_PORT:-6300}
echo "Starting Orbit Shell on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload
