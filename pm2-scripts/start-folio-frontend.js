const { spawn } = require('child_process');
const proc = spawn(
  '/home/sasi/.nvm/versions/node/v18.20.8/bin/node',
  ['/home/sasi/Desktop/dev/RM Orbit/RMBook/node_modules/vite/bin/vite.js', 'preview'],
  { stdio: 'inherit', cwd: '/home/sasi/Desktop/dev/RM Orbit/RMBook', env: process.env }
);
proc.on('exit', code => process.exit(code || 0));
process.on('SIGTERM', () => proc.kill('SIGTERM'));
process.on('SIGINT', () => proc.kill('SIGINT'));
