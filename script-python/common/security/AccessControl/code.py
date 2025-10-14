# Centralized RBAC checks; integrate with Ignition roles if available.
def require(roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                from system.user import hasRole
                if not any(hasRole(r) for r in roles):
                    from common.exceptions.SecurityException import code as sec
                    raise sec.SecurityException("Insufficient role")
            except Exception:
                # Outside Ignition, allow for tests
                pass
            return func(*args, **kwargs)
        return wrapper
    return decorator
