from functools import wraps


# Centralized RBAC checks; integrate with Ignition roles if available.

def require(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                from system.user import hasRole
            except Exception:
                return func(*args, **kwargs)

            authorized = False
            for role in roles:
                try:
                    if hasRole(role):
                        authorized = True
                        break
                except Exception:
                    continue
            if not authorized:
                from common.exceptions.SecurityException import code as sec
                raise sec.SecurityException("Insufficient role")
            return func(*args, **kwargs)

        return wrapper

    return decorator
