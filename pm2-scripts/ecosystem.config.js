module.exports = {
  apps: [
    {
      name: 'folio-backend',
      script: '/home/sasi/Desktop/dev/RM Orbit/Calendar/server/index.js',
      interpreter: '/home/sasi/.nvm/versions/node/v20.20.0/bin/node',
      cwd: '/home/sasi/Desktop/dev/RM Orbit/Calendar/server',
      env: { PORT: 5001 },
    },
    {
      name: 'folio-frontend',
      script: '/home/sasi/.nvm/versions/node/v18.20.8/bin/node',
      args: '/home/sasi/Desktop/dev/RM Orbit/RMBook/node_modules/vite/bin/vite.js preview',
      interpreter: 'none',
      cwd: '/home/sasi/Desktop/dev/RM Orbit/RMBook',
    },
  ],
};
