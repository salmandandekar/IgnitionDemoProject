"""
TenantResolver
--------------
Resolves the current tenant (site/division) using a strategy chain defined in ContextConfig.
Validation and sanitization handled by ContextValidator.
Never raises exceptions — always returns a valid or None tenant.
"""

from common.context.ContextConfig import CONFIG
from common.context.ContextValidator import validate_tenant
from common.logging import LogFactory
log = LogFactory.get_logger("Context")

# Extract config
_STRATEGY_ORDER = CONFIG.get("STRATEGY_ORDER", [])
_ALLOWED_TENANTS = CONFIG.get("ALLOWED_TENANTS", [])
_HOST_TO_TENANT = CONFIG.get("HOST_TO_TENANT", {})

def _from_incoming(incoming):
    if not incoming:
        return None
    t = incoming.get("tenant")
    return validate_tenant(t)

def _from_session_props():
    try:
        from system.util import getSessionInfo
        sessions = getSessionInfo() or []
        for s in sessions:
            t = (s.get("custom") or {}).get("tenant")
            t = validate_tenant(t)
            if t:
                return t
    except Exception:
        pass
    return None

def _from_jwt_claims():
    try:
        from system.util import getSessionInfo
        sessions = getSessionInfo() or []
        for s in sessions:
            claims = (s.get("custom") or {}).get("claims") or {}
            t = claims.get("tenant")
            t = validate_tenant(t)
            if t:
                return t
    except Exception:
        pass
    return None

def _from_user_directory():
    try:
        from system.util import getUserName
        user = getUserName() or ""
        # Replace with real secure mapping (DB/UDM)
        mapping = {"jdoe": "PlantA", "asmith": "PlantB"}
        t = mapping.get(user)
        return validate_tenant(t)
    except Exception:
        return None

def _from_host_mapping():
    try:
        from system.util import getHostName
        host = getHostName() or ""
        t = _HOST_TO_TENANT.get(host)
        return validate_tenant(t)
    except Exception:
        return None

_STRATEGIES = {
    "from_incoming": _from_incoming,
    "from_session_props": lambda inc=None: _from_session_props(),
    "from_jwt_claims": lambda inc=None: _from_jwt_claims(),
    "from_user_directory": lambda inc=None: _from_user_directory(),
    "from_host_mapping": lambda inc=None: _from_host_mapping(),
}

def resolve(default_tenant=None, allow_default=False, incoming=None):
    """
    Resolve tenant using the configured strategy chain.
    Returns a valid tenant string or None.
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

    return None