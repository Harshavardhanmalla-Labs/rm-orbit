// ═══════════════════════════════════════════════════════════════════════
// RM Orbit – PM2 Ecosystem Config
// ═══════════════════════════════════════════════════════════════════════
// Always-online process management.
// Usage:
//   pm2 start ecosystem.config.cjs
//   pm2 startup              # auto-start on boot
//   pm2 save                 # save current process list
//   pm2 status               # check what's running
//   pm2 logs <name>          # tail logs
// ═══════════════════════════════════════════════════════════════════════

const RESTART_DELAY = 3000;        // 3 s between restart attempts
const MAX_RESTARTS  = 50;          // allow many restarts (production)
const MIN_UPTIME    = '5s';        // consider stable after 5 s

const defaults = {
  autorestart:                true,
  max_restarts:               MAX_RESTARTS,
  restart_delay:              RESTART_DELAY,
  min_uptime:                 MIN_UPTIME,
  exp_backoff_restart_delay:  100,       // exponential backoff on repeated crashes
  kill_timeout:               5000,      // graceful shutdown window
  listen_timeout:             10000,     // time to wait for app ready
  watch:                      false,
  merge_logs:                 true,
  log_date_format:            'YYYY-MM-DD HH:mm:ss Z',
};

module.exports = {
  apps: [
    // ─── Atlas ───────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Atlas-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload',
      cwd: './Atlas/backend',
    },
    {
      ...defaults,
      name: 'Atlas-Frontend',
      script: 'npx',
      args: 'vite --port 5173 --strictPort --host',
      cwd: './Atlas/frontend',
    },

    // ─── Calendar ────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Calendar-Backend',
      script: 'npm',
      args: 'start',
      cwd: './Calendar/server',
    },
    {
      ...defaults,
      name: 'Calendar-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45005 --strictPort --host',
      cwd: './Calendar',
    },

    // ─── Control Center ──────────────────────────────────────────
    {
      ...defaults,
      name: 'CC-Backend',
      script: 'npm',
      args: 'run dev',
      cwd: './Control Center/server',
    },
    {
      ...defaults,
      name: 'CC-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45011 --strictPort --host',
      cwd: './Control Center',
    },

    // ─── Connect ─────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Connect-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45008 --strictPort --host',
      cwd: './Connect',
    },

    // ─── Mail ────────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Mail-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45004 --strictPort --host',
      cwd: './Mail/frontend',
    },

    // ─── Meet ────────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Meet-Backend',
      script: '/home/sasi/.nvm/versions/node/v22.14.0/bin/node',
      args: 'index.js',
      cwd: './Meet/server',
    },
    {
      ...defaults,
      name: 'Meet-Frontend',
      script: '/home/sasi/.nvm/versions/node/v22.14.0/bin/node',
      args: './node_modules/.bin/vite --port 45003 --strictPort --host',
      cwd: './Meet',
    },
    {
      ...defaults,
      name: 'RMMeet-Guest',
      script: '/home/sasi/.nvm/versions/node/v22.14.0/bin/node',
      args: './node_modules/.bin/vite --port 45026 --strictPort --host',
      cwd: './RMMeet',
    },

    // ─── Planet ──────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Planet-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 46000 --reload',
      cwd: './Planet/backend',
    },
    {
      ...defaults,
      name: 'Planet-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45006 --strictPort --host',
      cwd: './Planet',
    },

    // ─── Writer ──────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Writer-Backend',
      script: '.venv/bin/python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6011',
      cwd: './Writer.tmp/backend',
      interpreter: 'none',
    },
    {
      ...defaults,
      name: 'Writer-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45010 --strictPort --host',
      cwd: './Writer.tmp/frontend',
    },

    // ─── Learn ───────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Learn-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45009 --strictPort --host',
      cwd: './Learn/frontend',
    },

    // ─── Capital Hub ─────────────────────────────────────────────
    {
      ...defaults,
      name: 'CapitalHub-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45013 --strictPort --host',
      cwd: './Capital Hub/frontend',
    },

    // ─── Secure ──────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Secure-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6004',
      cwd: './Secure/services/secure-service',
    },
    {
      ...defaults,
      name: 'Secure-Frontend',
      script: 'npm',
      args: 'run dev -- --port 45012 --strictPort --host',
      cwd: './Secure/frontend',
    },

    // ─── Search ──────────────────────────────────────────────────
    {
      ...defaults,
      name: 'Search-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6200',
      cwd: './Search/backend',
    },

    // ─── TurboTick / RM Wallet / RM Dock / FitterMe ──────────────
    {
      ...defaults,
      name: 'TurboTick-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6100 --reload',
      cwd: './TurboTick/backend',
    },
    {
      ...defaults,
      name: 'TurboTick-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './TurboTick/frontend',
    },
    {
      ...defaults,
      name: 'RMWallet-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6110 --reload',
      cwd: './Wallet/backend',
    },
    {
      ...defaults,
      name: 'RMWallet-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './Wallet/frontend',
    },
    {
      ...defaults,
      name: 'RMDock-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6120 --reload',
      cwd: './Dock/backend',
    },
    {
      ...defaults,
      name: 'RMDock-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './Dock/frontend',
    },
    // FitterMe backend is Docker-managed (docker compose up fitterme)
    // Frontend: ecosystem.freedomlabs.in → port 45016
    {
      ...defaults,
      name: 'FitterMe-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './FitterMe/frontend',
    },

    // ─── RM Fonts (static) ──────────────────────────────────────
    {
      ...defaults,
      name: 'RM-Fonts',
      script: 'python3',
      args: '-m http.server 45007 --bind 0.0.0.0',
      cwd: './Fonts',
    },

    // ─── Event Bus (Core Snitch) ───────────────────────────────────
    {
      ...defaults,
      name: 'EventBus-Backend',
      script: 'npm',
      args: 'run start',
      cwd: './EventBus',
    },
    {
      ...defaults,
      name: 'EventBus-Server',
      script: 'npm',
      args: 'run eventbus',
      cwd: './EventBus',
    },
    {
      ...defaults,
      name: 'EventBus-Frontend',
      script: 'npm',
      args: 'run dev -- --port 5179 --strictPort --host',
      cwd: './EventBus/frontend',
    },

    // ─── Node Extensions (Distributed Stitch) ───────────────────────
    {
      ...defaults,
      name: 'Learn-Extension-Service',
      script: 'npm',
      args: 'run learn',
      cwd: './Learn/node-extension',
    },
    {
      ...defaults,
      name: 'CapitalHub-Extension-Service',
      script: 'npm',
      args: 'run capitalhub',
      cwd: './Capital Hub/node-extension',
    },
    {
      ...defaults,
      name: 'Secure-Extension-Service',
      script: 'npm',
      args: 'run secure',
      cwd: './Secure/node-extension',
    },
    {
      ...defaults,
      name: 'Meet-TURN-Server',
      script: '/home/sasi/.nvm/versions/node/v22.14.0/bin/node',
      args: 'turn-server.js',
      cwd: './Meet/node-extension',
    },
    {
      ...defaults,
      name: 'Meet-Media-Relay',
      script: '/home/sasi/.nvm/versions/node/v22.14.0/bin/node',
      args: './node_modules/.bin/nodemon media-service.js',
      cwd: './Meet/node-extension',
    },

    // ─── Search Frontend ────────────────────────────────────────
    {
      ...defaults,
      name: 'Search-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './Search/frontend',
    },

    // ─── Orbit Shell (AI Conversational Interface) ────────────────
    {
      ...defaults,
      name: 'OrbitShell-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6300',
      cwd: './OrbitShell/backend',
      env: {
        PYTHONPATH: '.',
        PYTHONUNBUFFERED: '1',
      },
    },

    // ─── Scribe (AI Content Engine) ─────────────────────────────
    {
      ...defaults,
      name: 'Scribe-Backend',
      script: 'python3',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 6400 --reload',
      cwd: './Scribe/backend',
      interpreter: './Scribe/backend/.venv/bin/python3',
      env: { PYTHONPATH: '.' },
    },
    {
      ...defaults,
      name: 'Scribe-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './Scribe/frontend',
    },

    // ─── Gate Admin Portal ────────────────────────────────────────
    {
      ...defaults,
      name: 'Gate-Admin',
      script: 'npm',
      args: 'run dev',
      cwd: './Gate/admin',
      env: {
        NODE_ENV: 'development',
        PORT: '45022',
      },
    },

    // ─── Research (Autonomous Paper Writing) ──────────────────────
    {
      ...defaults,
      name: 'Research-Backend',
      script: 'bash',
      args: 'start.sh',
      cwd: './Research/backend',
      interpreter: 'none',
    },
    {
      ...defaults,
      name: 'Research-Frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './Research/frontend',
      env: {
        NODE_ENV: 'development',
        PORT: '10007',
      },
    },
  ],
};
