#!/bin/bash
# RM-Orbit Mail Rebuild Script
# This script applies the frontend fixes (auto-identity completion, custom fonts)
# to the running Docker containers.

echo "Rangudu@0007" | sudo -S docker compose -f Mail/docker-compose.yml up --build -d backend worker inbound_worker frontend
