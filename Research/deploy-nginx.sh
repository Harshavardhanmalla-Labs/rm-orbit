#!/usr/bin/env bash
# Run once with sudo to install the Research nginx config
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/research.nginx.conf" /etc/nginx/sites-available/research.conf
ln -sf /etc/nginx/sites-available/research.conf /etc/nginx/sites-enabled/research.conf
nginx -t && nginx -s reload
echo "✓ research.freedomlabs.in → :10007 configured and nginx reloaded"
