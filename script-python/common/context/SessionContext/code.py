"""
SessionContext
--------------
Provides a unified, standards-compliant context dict:
{user, tenant, correlationId, host, sessionId}

- Calls TenantResolver to determine tenant.
- Validates & sanitizes output via ContextValidator.
- Generates UUID correlationId if missing.
"""

import uuid
from common.logging import LogFactory
from common.context import TenantResolver
from common.context.ContextConfig import CONFIG
from common.context.ContextValidator import sanitize_context
log = LogFactory.get_logger("Context")

def _uuid():
    try:
        return str(uuid.uuid4())
    except Exception:
        return "na"

def _username():
    try:
        from system.util import getUserName
        return getUserName() or "system"
    except Exception:
        return "system"

def _host():
    try:
        from system.util import getHostName
        return getHostName() or "unknown"
    except Exception:
        return "unknown"

def _session_id():
    try:
        from system.util import getSessionInfo
        sessions = getSessionInfo() or []
        return sessions[0].get("id") if sessions else None
    except Exception:
        return None

def current(incoming=None):
    """
    Returns the current session context dictionary.
    - Propagates incoming correlationId / tenant if present and valid.
    - Never raises exceptions.
    """
    inc = incoming or {}
    corr = inc.get("correlationId") or _uuid()

    tenant = None
    t_in = inc.get("tenant")
    if t_in:
        tenant = TenantResolver.resolve(incoming={"tenant": t_in})
    if not tenant:
        tenant = TenantResolver.resolve(
            default_tenant=CONFIG.get("DEFAULT_TENANT"),
            allow_default=CONFIG.get("ALLOW_DEFAULT", False),
            incoming=inc
        )

    ctx = {
        "user": _username(),
        "tenant": tenant,
        "correlationId": corr,
        "host": _host(),
        "sessionId": _session_id(),
    }

    ctx = sanitize_context(ctx)
    return ctx