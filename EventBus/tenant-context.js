function normalizeValue(value) {
  if (typeof value !== 'string') {
    return null;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : null;
}

function resolveTokenOrg(user) {
  if (!user || typeof user !== 'object') {
    return null;
  }
  return (
    normalizeValue(user.org_id) ||
    normalizeValue(user.orgId) ||
    normalizeValue(user.organization)
  );
}

function resolveUserId(user) {
  if (!user || typeof user !== 'object') {
    return null;
  }
  return (
    normalizeValue(user.sub) ||
    normalizeValue(user.user_id) ||
    normalizeValue(user.userId)
  );
}

function enforceTenantContext(req, res, next) {
  const headerOrg = normalizeValue(req.organization || req.header('x-org-id'));
  const tokenOrg = resolveTokenOrg(req.user);
  const resolvedOrg = headerOrg || tokenOrg;

  if (!resolvedOrg) {
    return res.status(400).json({ error: 'Missing organization context' });
  }

  if (headerOrg && tokenOrg && headerOrg !== tokenOrg) {
    return res.status(403).json({ error: 'Organization context mismatch' });
  }

  req.organization = resolvedOrg;
  req.tenantContext = {
    org_id: resolvedOrg,
    user_id: resolveUserId(req.user),
  };

  return next();
}

module.exports = {
  enforceTenantContext,
  resolveTokenOrg,
  resolveUserId,
};
