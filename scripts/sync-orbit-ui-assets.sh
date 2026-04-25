#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_CSS="$ROOT_DIR/orbit-ui/orbit-ui.css"
SOURCE_JS="$ROOT_DIR/orbit-ui/orbit-bar.js"
SOURCE_TOKENS="$ROOT_DIR/orbit-ui/tokens/orbit-tokens.css"
SOURCE_THEME_INIT="$ROOT_DIR/orbit-ui/orbit-theme-init.js"
SOURCE_TW="$ROOT_DIR/orbit-ui/orbit-tailwind-v4.css"
FONT_SOURCE_DIR="$ROOT_DIR/Fonts/RM Fonts/fonts"

if [ ! -f "$SOURCE_CSS" ] || [ ! -f "$SOURCE_JS" ]; then
  echo "orbit-ui source assets are missing. Expected:"
  echo "  - $SOURCE_CSS"
  echo "  - $SOURCE_JS"
  exit 1
fi

copy_bundle() {
  local target_dir="$1"
  mkdir -p "$target_dir"
  cp "$SOURCE_CSS" "$target_dir/orbit-ui.css"
  cp "$SOURCE_JS" "$target_dir/orbit-bar.js"
  [ -f "$SOURCE_TOKENS" ]     && cp "$SOURCE_TOKENS"     "$target_dir/orbit-tokens.css"
  [ -f "$SOURCE_THEME_INIT" ] && cp "$SOURCE_THEME_INIT" "$target_dir/orbit-theme-init.js"
  [ -f "$SOURCE_TW" ]         && cp "$SOURCE_TW"         "$target_dir/orbit-tailwind-v4.css"
}

copy_fonts() {
  local target_dir="$1"
  if [ ! -d "$FONT_SOURCE_DIR" ]; then
    echo "Font source directory not found ($FONT_SOURCE_DIR). Skipping font sync for $target_dir."
    return 0
  fi
  mkdir -p "$target_dir"
  for font_file in \
    RMForma-Regular.woff2 \
    RMForma-SemiBold.woff2 \
    RMForma-Bold.woff2 \
    RM-Samplet-Regular.ttf
  do
    if [ -f "$FONT_SOURCE_DIR/$font_file" ]; then
      cp "$FONT_SOURCE_DIR/$font_file" "$target_dir/$font_file"
    else
      echo "Font file missing: $FONT_SOURCE_DIR/$font_file (skipping)"
    fi
  done
}

BUNDLE_TARGETS=(
  "$ROOT_DIR/Meet/public/orbit-ui"
  "$ROOT_DIR/Meet/meet-app/public/orbit-ui"
  "$ROOT_DIR/Learn/site/assets"
  "$ROOT_DIR/Learn/frontend/public/orbit-ui"
  "$ROOT_DIR/Writer/site/assets"
  "$ROOT_DIR/Writer/frontend/public/orbit-ui"
  "$ROOT_DIR/Atlas/frontend/public/orbit-ui"
  "$ROOT_DIR/Calendar/public/orbit-ui"
  "$ROOT_DIR/Connect/public/orbit-ui"
  "$ROOT_DIR/Control Center/public/orbit-ui"
  "$ROOT_DIR/Mail/frontend/public/orbit-ui"
  "$ROOT_DIR/Planet/public/orbit-ui"
  "$ROOT_DIR/Secure/frontend/public/orbit-ui"
  "$ROOT_DIR/Capital Hub/frontend/public/orbit-ui"
  "$ROOT_DIR/Snitch/frontend/public/orbit-ui"
  "$ROOT_DIR/TurboTick/frontend/public/orbit-ui"
  "$ROOT_DIR/Wallet/frontend/public/orbit-ui"
  "$ROOT_DIR/Dock/frontend/public/orbit-ui"
  "$ROOT_DIR/FitterMe/frontend/public/orbit-ui"
  "$ROOT_DIR/Gate/admin/public/orbit-ui"
  "$ROOT_DIR/Search/frontend/public/orbit-ui"
  "$ROOT_DIR/Capital Hub/site/assets"
  "$ROOT_DIR/Secure/site/assets"
)

FONT_TARGETS=(
  "$ROOT_DIR/Meet/public/fonts"
  "$ROOT_DIR/Meet/meet-app/public/fonts"
  "$ROOT_DIR/Learn/site/fonts"
  "$ROOT_DIR/Learn/frontend/public/fonts"
  "$ROOT_DIR/Writer/site/fonts"
  "$ROOT_DIR/Writer/frontend/public/fonts"
  "$ROOT_DIR/Atlas/frontend/public/fonts"
  "$ROOT_DIR/Calendar/public/fonts"
  "$ROOT_DIR/Connect/public/fonts"
  "$ROOT_DIR/Control Center/public/fonts"
  "$ROOT_DIR/Mail/frontend/public/fonts"
  "$ROOT_DIR/Planet/public/fonts"
  "$ROOT_DIR/Secure/frontend/public/fonts"
  "$ROOT_DIR/Capital Hub/frontend/public/fonts"
  "$ROOT_DIR/Snitch/frontend/public/fonts"
  "$ROOT_DIR/TurboTick/frontend/public/fonts"
  "$ROOT_DIR/Wallet/frontend/public/fonts"
  "$ROOT_DIR/Dock/frontend/public/fonts"
  "$ROOT_DIR/FitterMe/frontend/public/fonts"
  "$ROOT_DIR/Gate/admin/public/fonts"
  "$ROOT_DIR/Search/frontend/public/fonts"
  "$ROOT_DIR/Capital Hub/site/fonts"
  "$ROOT_DIR/Secure/site/fonts"
)

for target in "${BUNDLE_TARGETS[@]}"; do
  copy_bundle "$target"
done

for target in "${FONT_TARGETS[@]}"; do
  copy_fonts "$target"
done

echo "Synced orbit-ui assets and fonts for ${#BUNDLE_TARGETS[@]} frontend targets."
