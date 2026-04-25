#!/usr/bin/env bash
# sync-tokens.sh — distribute orbit-tokens.css + fonts to all frontend apps
set -euo pipefail

ORBIT_UI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$ORBIT_UI_DIR/.." && pwd)"

TOKENS_CSS="$ORBIT_UI_DIR/tokens/orbit-tokens.css"
ORBIT_BAR_JS="$ORBIT_UI_DIR/orbit-bar.js"
ORBIT_BAR_CSS="$ORBIT_UI_DIR/orbit-ui.css"
THEME_INIT_JS="$ORBIT_UI_DIR/orbit-theme-init.js"
TAILWIND_V4_CSS="$ORBIT_UI_DIR/orbit-tailwind-v4.css"

# All frontend app directories (public folder targets)
# Format: "AppDir/subdir" OR "AppDir" (for apps with src at root)
FRONTENDS=(
  "Atlas/frontend"
  "Mail/frontend"
  "Connect"
  "Meet"
  "Calendar"
  "Writer/frontend"
  "Planet"
  "Secure/frontend"
  "Control Center"
  "Capital Hub/frontend"
  "TurboTick/frontend"
  "Dock/frontend"
  "Wallet/frontend"
  "FitterMe"
  "Learn/frontend"
  "Gate"
)

echo "🔄  Syncing Orbit UI assets..."
echo ""

for APP_PATH in "${FRONTENDS[@]}"; do
  FULL_PATH="$ROOT_DIR/$APP_PATH"
  PUBLIC_DIR="$FULL_PATH/public"

  if [ ! -d "$FULL_PATH" ]; then
    echo "  ⚠️   Skipping (not found): $APP_PATH"
    continue
  fi

  # Ensure public/orbit-ui directory exists
  mkdir -p "$PUBLIC_DIR/orbit-ui"

  # Copy tokens CSS
  cp "$TOKENS_CSS" "$PUBLIC_DIR/orbit-ui/orbit-tokens.css"

  # Copy orbit bar JS, legacy CSS, theme-init script, and TW v4 CSS
  cp "$ORBIT_BAR_JS"        "$PUBLIC_DIR/orbit-ui/orbit-bar.js"
  cp "$ORBIT_BAR_CSS"       "$PUBLIC_DIR/orbit-ui/orbit-ui.css"
  cp "$THEME_INIT_JS"       "$PUBLIC_DIR/orbit-ui/orbit-theme-init.js"
  cp "$TAILWIND_V4_CSS"     "$PUBLIC_DIR/orbit-ui/orbit-tailwind-v4.css"

  echo "  ✅  $APP_PATH"
done

echo ""
echo "✅  Tokens synced to ${#FRONTENDS[@]} apps."
echo ""
echo "📌  Remember: each app's index.css should start with:"
echo "    @import \"/orbit-ui/orbit-tokens.css\";"
