# No prints; central accessor of session-level context (user, tenant, correlationId).
# Uses Ignition 'system' if available, else safe fallbacks.
def current():
    ctx = {
        "user": None,
        "tenant": None,
        "correlationId": None
    }
    try:
        # Ignition user
        from system.util import getUserName
        ctx["user"] = getUserName()
    except Exception:
        ctx["user"] = "anonymous"
    # correlation id
    try:
        import uuid
        ctx["correlationId"] = str(uuid.uuid4())
    except Exception:
        ctx["correlationId"] = "na"
    # tenant resolution deferred to TenantResolver
    return ctx
