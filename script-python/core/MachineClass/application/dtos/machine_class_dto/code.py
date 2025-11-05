# -*- coding: utf-8 -*-
"""DTO builders for the MachineClass context."""
from __future__ import absolute_import


def build_machine_class_dto(source):
    """Create a canonical DTO for MachineClass data."""
    normalized = source or {}
    return {
        "id": normalized.get("id"),
        "code": normalized.get("code"),
        "name": normalized.get("name"),
        "description": normalized.get("description"),
    }
