#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_FILE="$ROOT_DIR/code 3.html"
SITE_DIR="$ROOT_DIR/site"
TARGET_FILE="$SITE_DIR/index.html"
FONTS_SOURCE_DIR="$ROOT_DIR/../Fonts/RM Fonts/fonts"
FONTS_TARGET_DIR="$SITE_DIR/fonts"
SYNC_SCRIPT="$ROOT_DIR/../scripts/sync-orbit-ui-assets.sh"

if [ ! -f "$SOURCE_FILE" ]; then
  echo "Writer source prototype not found: $SOURCE_FILE"
  exit 1
fi

mkdir -p "$SITE_DIR"
cp "$SOURCE_FILE" "$TARGET_FILE"

mkdir -p "$FONTS_TARGET_DIR"
cp "$FONTS_SOURCE_DIR/RMForma-Regular.woff2" "$FONTS_TARGET_DIR/RMForma-Regular.woff2"
cp "$FONTS_SOURCE_DIR/RMForma-Bold.woff2" "$FONTS_TARGET_DIR/RMForma-Bold.woff2"
cp "$FONTS_SOURCE_DIR/RM-Samplet-Regular.ttf" "$FONTS_TARGET_DIR/RM-Samplet-Regular.ttf"

if [ -x "$SYNC_SCRIPT" ]; then
  "$SYNC_SCRIPT"
fi

echo "Writer site updated: $TARGET_FILE"
