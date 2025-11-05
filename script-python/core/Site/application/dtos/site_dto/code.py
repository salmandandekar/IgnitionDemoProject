# -*- coding: utf-8 -*-
"""DTO builders for the Site context."""
from __future__ import absolute_import


def build_site_dto(source):
    """Create a canonical DTO for Site data."""
    normalized = source or {}
    return {
        "id": normalized.get("id"),
        "code": normalized.get("code"),
        "name": normalized.get("name"),
        "description": normalized.get("description"),
    }
