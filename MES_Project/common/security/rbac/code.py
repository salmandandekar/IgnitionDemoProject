
from ..exceptions.mes_exceptions import AccessDenied
def require_role(user_roles, required):
    if required not in set(user_roles or []): raise AccessDenied("Missing role: %s"%required)
