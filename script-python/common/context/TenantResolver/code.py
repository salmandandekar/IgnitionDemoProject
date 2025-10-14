# Resolves tenant from session or request context (e.g., Perspective session props, JWT claims).
def resolve(default_tenant="default"):
    try:
        # Add real logic integrating with your identity provider if needed.
        return default_tenant
    except Exception:
        return default_tenant
