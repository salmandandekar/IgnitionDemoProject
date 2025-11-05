# -*- coding: utf-8 -*-
"""Entity definitions for the MachineClass context."""
from __future__ import absolute_import

DEFAULT_DESCRIPTION = ""


class MachineClassEntity(object):
    """Basic entity representation for the MachineClass context."""

    def __init__(self, identity, name, description=None):
        if identity is None:
            raise ValueError("Identity is required.")
        if not name:
            raise ValueError("Name is required.")
        self._identity = identity
        self._name = name
        self._description = description or DEFAULT_DESCRIPTION

    @property
    def identity(self):
        return self._identity

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def update_name(self, name):
        if not name:
            raise ValueError("Name cannot be blank.")
        self._name = name

    def update_description(self, description):
        self._description = description or DEFAULT_DESCRIPTION

    def to_dict(self):
        return {
            "id": self._identity.value,
            "name": self._name,
            "description": self._description,
        }
