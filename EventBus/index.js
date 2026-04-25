const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');

const app = express();
app.use(express.json());
const requireOrg = require('./org-middleware');
const requireAuth = require('./auth-middleware');
const { enforceTenantContext } = require('./tenant-context');
app.use(requireOrg);
app.use(requireAuth);
app.use(enforceTenantContext);

app.get('/health', (req, res) => {
  res.json({ status: 'snitch-backend ok' });
});

// provide OAuth client configuration for frontends
app.get('/oauth-config', (req, res) => {
  try {
    const data = fs.readFileSync('registered_apps.json', 'utf-8');
    const apps = JSON.parse(data);
    res.json(apps);
  } catch (err) {
    res.status(500).json({ error: 'unable to read config' });
  }
});

// simple route that returns decoded JWT claims for the authenticated user
app.get('/me', (req, res) => {
  if (req.user) {
    return res.json({ claims: req.user });
  }
  res.status(401).json({ error: 'not authenticated' });
});

// basic signalling server skeleton; will be expanded for voice/video
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

io.on('connection', (socket) => {
  console.log('snitch client connected', socket.id);

  socket.on('signal', (data) => {
    if (data.to) {
      io.to(data.to).emit('signal', data);
    }
  });

  socket.on('disconnect', () => {
    console.log('snitch client disconnected', socket.id);
  });
});

const PORT = process.env.PORT || 6000;
server.listen(PORT, () => {
  console.log(`Snitch backend listening on ${PORT}`);
});
