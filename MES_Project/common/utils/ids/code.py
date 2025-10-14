
"""Identifier generation helpers."""

from __future__ import annotations

import uuid
from typing import Optional


def new_id(prefix: Optional[str] = None) -> str:
    """Return a new RFC 4122 identifier optionally prefixed with ``prefix``."""

    value = str(uuid.uuid4())
    return f"{prefix}-{value}" if prefix else value
