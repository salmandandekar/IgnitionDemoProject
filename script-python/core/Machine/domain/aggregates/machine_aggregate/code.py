# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Machine context."""
from __future__ import absolute_import

from core.Machine.domain.entities.machine_entity import MachineEntity
from core.Machine.domain.value_objects.machine_identity import MachineIdentity


class MachineAggregate(object):
    """Aggregate root for Machine."""

    def __init__(self, identifier, name, description=None):
        identity = MachineIdentity(identifier)
        self._entity = MachineEntity(
            identity=identity,
            name=name,
            description=description,
        )

    @property
    def identity(self):
        return self._entity.identity

    @property
    def name(self):
        return self._entity.name

    @property
    def description(self):
        return self._entity.description

    def rename(self, name):
        self._entity.update_name(name)

    def update_description(self, description):
        self._entity.update_description(description)

    def to_dict(self):
        return self._entity.to_dict()
