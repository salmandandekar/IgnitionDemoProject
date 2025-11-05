# -*- coding: utf-8 -*-
"""DTO builders for the Area context."""
from __future__ import absolute_import


def build_area_dto(source):
    """Create a canonical DTO for Area data."""
    normalized = source or {}
    return {
        "id": normalized.get("id"),
        "code": normalized.get("code"),
        "name": normalized.get("name"),
        "description": normalized.get("description"),
    }
