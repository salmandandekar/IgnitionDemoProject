# common/context/TenantResolver.py
"""
TenantResolver
--------------
Resolves the current tenant (plant/site/division) using a standards-based strategy chain.

- Works across Perspective sessions, Hybrid Authentication, and Gateway contexts.
- Integrates with ContextConfig (strategy order, defaults, allowed tenants).
- Validates tenant values using ContextValidator.
- Never raises exceptions — returns a valid tenant string or None.
"""

from common.context.ContextConfig import CONFIG
from common.context.ContextValidator import validate_tenant
from common.logging import LogFactory
log = LogFactory.get_logger("Context")

_STRATEGY_ORDER = CONFIG.get("STRATEGY_ORDER", [])
_ALLOWED_TENANTS = CONFIG.get("ALLOWED_TENANTS", [])
_HOST_TO_TENANT = CONFIG.get("HOST_TO_TENANT", {})

# --- Strategy Implementations ------------------------------------------------

def _from_incoming(incoming):
    """Directly supplied tenant (e.g., from script argument or session)."""
    if not incoming:
        return None
    t = incoming.get("tenant")
    return validate_tenant(t)

def _from_session_props(incoming=None):
    """Perspective session custom property (session.custom.tenant)."""
    try:
        sess = (incoming or {}).get("session")
        if sess:
            t = (sess.custom or {}).get("tenant")
            return validate_tenant(t)
    except Exception:
        pass
    return None

def _from_jwt_claims(incoming=None):
    """JWT or IdP claims via session.custom.claims."""
    try:
        sess = (incoming or {}).get("session")
        if sess:
            claims = (sess.custom or {}).get("claims") or {}
            t = claims.get("tenant")
            return validate_tenant(t)
    except Exception:
        pass
    return None

def _from_user_directory(incoming=None):
    """Look up tenant via hybrid authentication user metadata in Ignition."""
    try:
        from system.util import getUserName
        from system.user import getUser
        user = getUserName() or ""
        userObj = getUser("HybridAuth", user)  # "HybridAuth" = your user source name
        if userObj:
            t = userObj.get("tenant") or userObj.get("department")
            return validate_tenant(t)
    except Exception as ex:
        log.warn("Hybrid directory lookup failed: %s" % str(ex))
    return None

def _from_host_mapping(incoming=None):
    """Fallback to host→tenant mapping for gateway scripts."""
    try:
        from system.util import getHostName
        host = getHostName() or ""
        t = _HOST_TO_TENANT.get(host)
        return validate_tenant(t)
    except Exception:
        return None

# Map strategies
_STRATEGIES = {
    "from_incoming": _from_incoming,
    "from_session_props": _from_session_props,
    "from_jwt_claims": _from_jwt_claims,
    "from_user_directory": _from_user_directory,
    "from_host_mapping": _from_host_mapping,
}

# --- Main Resolver -----------------------------------------------------------

def resolve(default_tenant=None, allow_default=False, incoming=None):
    """
    Resolve tenant using configured strategies.
    Returns a valid tenant or None.
    """
    for key in _STRATEGY_ORDER:
        try:
            strat = _STRATEGIES.get(key)
            if not strat:
                continue
            t = strat(incoming)
            if t:
                return t
        except Exception:
            log.warn("TenantResolver strategy failed: %s" % key)

    # Default fallback
    if allow_default and default_tenant:
        t = validate_tenant(default_tenant)
        if t:
            return t
        else:
            log.warn("Default tenant not allowed: %s" % default_tenant)

    # Policy-based default tenant (from ContextConfig)
    if CONFIG.get("ALLOW_DEFAULT", False) and CONFIG.get("DEFAULT_TENANT"):
        return CONFIG.get("DEFAULT_TENANT")

    return None