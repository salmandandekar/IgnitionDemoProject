# common/context/SessionContext.py
"""
SessionContext
--------------
Provides a unified, validated context dictionary:
{user, tenant, correlationId, host, sessionId}

- Detects Perspective sessions and extracts identity safely.
- Falls back gracefully in Designer or Gateway scope.
- Integrates with ContextConfig (defaults) and ContextValidator.
- Compliant with SEI & ISO 25010/42010/27001 for logging & context governance.
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

def _username(session=None):
    """Determine current username (Perspective, Hybrid, or Gateway)."""
    try:
        if session and getattr(session, "props", None):
            u = getattr(session.props.auth.user, "username", None)
            if u:
                return u
    except Exception:
        pass
    try:
        from system.util import getUserName
        return getUserName() or "system"
    except Exception:
        return "system"

def _host():
    """Get gateway or client host identifier."""
    try:
        from system.util import getHostName
        return getHostName() or "unknown"
    except Exception:
        return "unknown"

def _session_id(session=None):
    """Get session ID if running in Perspective."""
    try:
        if session and hasattr(session, "id"):
            return session.id
        from system.util import getSessionInfo
        sessions = getSessionInfo() or []
        return sessions[0].get("id") if sessions else None
    except Exception:
        return None

def current(incoming=None):
    """
    Returns current execution context:
    {
      user, tenant, correlationId, host, sessionId
    }

    Supports:
    - Perspective sessions (pass 'session' in incoming)
    - Gateway / Designer / Timer scripts (fallback)
    - Hybrid Authentication users (via TenantResolver)
    """
    inc = incoming or {}
    sess = inc.get("session")
    corr = inc.get("correlationId") or _uuid()

    # Tenant resolution with full strategy chain
    tenant = TenantResolver.resolve(
        default_tenant=CONFIG.get("DEFAULT_TENANT"),
        allow_default=CONFIG.get("ALLOW_DEFAULT", False),
        incoming=inc
    )

    ctx = {
        "user": _username(sess),
        "tenant": tenant,
        "correlationId": corr,
        "host": _host(),
        "sessionId": _session_id(sess),
    }

    ctx = sanitize_context(ctx)
    return ctx