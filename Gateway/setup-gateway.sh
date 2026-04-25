#!/usr/bin/env bash

set -e

# Setup RM Orbit Gateway

echo "Setting up RM Orbit Unified API Gateway..."

mkdir -p certs

# Generate self-signed SAN certificate for freedomlabs.in domains
# Includes: auth, atlas, mail, chronos, connect, meet, writer, planet, secure, admin, search, learn, capital, fitter
if [ ! -f "certs/freedomlabs.crt" ]; then
  echo "Generating wildcard TLS certificate for RM Orbit ecosystem (*.freedomlabs.in)..."
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/freedomlabs.key \
    -out certs/freedomlabs.crt \
    -subj "/C=US/ST=State/L=City/O=RM Orbit/OU=Engineering/CN=*.freedomlabs.in" \
    -addext "subjectAltName = DNS:*.freedomlabs.in,DNS:auth.freedomlabs.in,DNS:atlas.freedomlabs.in,DNS:mail.freedomlabs.in,DNS:chronos.freedomlabs.in,DNS:connect.freedomlabs.in,DNS:meet.freedomlabs.in,DNS:writer.freedomlabs.in,DNS:planet.freedomlabs.in,DNS:secure.freedomlabs.in,DNS:admin.freedomlabs.in,DNS:search.freedomlabs.in,DNS:learn.freedomlabs.in,DNS:capital.freedomlabs.in,DNS:fitter.freedomlabs.in"
  echo "✅ Certificates generated in ./certs"
else
  echo "✅ Certificates already exist."
fi

# Create shared generic network explicitly if traefik goes up first
docker network create orbit_network 2>/dev/null || true

echo ""
echo "============================================="
echo "GATEWAY SETUP COMPLETE!"
echo ""
echo "To add these domains to your local machine, run (ROOT/SUDO):"
echo "echo \"127.0.0.1 auth.freedomlabs.in atlas.freedomlabs.in mail.freedomlabs.in chronos.freedomlabs.in connect.freedomlabs.in meet.freedomlabs.in writer.freedomlabs.in planet.freedomlabs.in secure.freedomlabs.in admin.freedomlabs.in search.freedomlabs.in learn.freedomlabs.in capital.freedomlabs.in fitter.freedomlabs.in\" >> /etc/hosts"
echo ""
echo "To start the gateway:"
echo "docker compose up -d"
echo "============================================="
