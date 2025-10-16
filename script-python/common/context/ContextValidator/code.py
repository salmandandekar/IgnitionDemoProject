"""
Validates and sanitizes context data in accordance with ISO 27001 A.12.4 (logging/monitoring).
"""

import re
from common.context.ContextConfig import CONFIG

_ALLOWED_TENANTS = set(CONFIG["ALLOWED_TENANTS"])
_TENANT_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")

def validate_tenant(tenant):
    """Return tenant if valid, else None."""
    if not tenant:
        return None
    if tenant in _ALLOWED_TENANTS:
        return tenant
    if _TENANT_PATTERN.match(tenant):
        # Optional: dynamically accept but log warning elsewhere
        return tenant
    return None

def sanitize_context(ctx):
    """
    Enforces schema: {user, tenant, correlationId, host, sessionId}.
    Drops unexpected keys; masks obvious secrets.
    """
    allowed = {"user", "tenant", "correlationId", "host", "sessionId"}
    out = {}
    for k, v in (ctx or {}).items():
        if k not in allowed:
            continue
        if isinstance(v, basestring) and any(x in k.lower() for x in ["pass", "token", "key"]):
            out[k] = "***"
        else:
            out[k] = v
    return out