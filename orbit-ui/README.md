# orbit-ui

Shared RM Orbit UI package for cross-app consistency.

## Included assets

- `orbit-ui.css`: shared typography tokens, colors, and Orbit Shell styles.
- `orbit-bar.js`: custom element (`<orbit-shell-bar>`) with:
  - app launcher
  - org switcher
  - identity menu/sign-out action

## Usage

```html
<link rel="stylesheet" href="/orbit-ui/orbit-ui.css" />
<script src="/orbit-ui/orbit-bar.js" defer></script>
<orbit-shell-bar app-id="meet" app-name="Meet"></orbit-shell-bar>
```

For static apps (Learn/Writer) and Meet, use `scripts/sync-orbit-ui-assets.sh` to copy assets/fonts into each runtime web root.

Current sync targets include active frontend roots across the workspace (Meet, Learn, Writer, Atlas, Connect, Mail, Calendar, Planet, Control Center, Secure, Capital Hub, TurboTick, RM Wallet, RM Dock, Snitch) plus static site assets where applicable.
