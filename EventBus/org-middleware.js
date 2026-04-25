// simple middleware to enforce organization context
module.exports = function requireOrg(req, res, next) {
  const org = req.header('x-org-id') || req.query.org_id;
  if (!org) {
    return res.status(400).json({ error: 'Missing X-Org-Id header or org_id parameter' });
  }
  req.organization = org;
  next();
};
