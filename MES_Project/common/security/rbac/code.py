
"""Role-based access control helpers."""

from __future__ import annotations

from typing import Iterable, Optional, Sequence, Set

from ..exceptions.mes_exceptions import AccessDenied


def _normalise_roles(roles: Optional[Iterable[str]]) -> Set[str]:
    return {role for role in (roles or []) if role}


def require_role(user_roles: Optional[Iterable[str]], required: str) -> None:
    """Ensure ``required`` is present in ``user_roles``."""

    if required not in _normalise_roles(user_roles):
        raise AccessDenied(f"Missing role: {required}")


def require_any_role(user_roles: Optional[Iterable[str]], required: Sequence[str]) -> str:
    """Validate that at least one required role is granted.

    Returns the first matching role to aid auditing.
    """

    user_role_set = _normalise_roles(user_roles)
    for role in required:
        if role in user_role_set:
            return role
    raise AccessDenied("User lacks any of the required roles: {}".format(", ".join(required)))


def require_all_roles(user_roles: Optional[Iterable[str]], required: Sequence[str]) -> None:
    """Ensure the caller holds all roles in ``required``."""

    missing = _normalise_roles(required) - _normalise_roles(user_roles)
    if missing:
        raise AccessDenied("Missing roles: {}".format(", ".join(sorted(missing))))
