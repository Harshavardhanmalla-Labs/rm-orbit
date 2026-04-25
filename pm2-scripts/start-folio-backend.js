const { spawn } = require('child_process');
const proc = spawn(
  '/home/sasi/.nvm/versions/node/v20.20.0/bin/node',
  ['/home/sasi/Desktop/dev/RM Orbit/Calendar/server/index.js'],
  { stdio: 'inherit', env: { ...process.env, PORT: '5001' } }
);
proc.on('exit', code => process.exit(code || 0));
process.on('SIGTERM', () => proc.kill('SIGTERM'));
process.on('SIGINT', () => proc.kill('SIGINT'));
