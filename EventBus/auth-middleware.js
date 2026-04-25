const path = require('path');
const { verifyGateTokenWithFallback } = require('../scripts/gate-token-verifier');

module.exports = function requireAuth(req, res, next) {
  const authHeader = req.headers['authorization'];
  let token = req.query.token;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({ error: 'Missing or invalid token' });
  }
  verifyGateTokenWithFallback(token, {
    defaultPublicKeyPath: path.join(__dirname, '../Gate/authx/certs/public.pem'),
    localSecret: process.env.SECRET_KEY || process.env.JWT_SECRET || 'snitch-secret-key',
  })
    .then((result) => {
      const payload = result.payload;
      if (payload.type && payload.type !== 'access') {
        return res.status(401).json({ error: 'Invalid token type' });
      }
      req.user = payload;
      return next();
    })
    .catch((_err) => res.status(401).json({ error: 'Invalid token' }));
};
