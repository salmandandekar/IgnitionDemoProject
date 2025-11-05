# -*- coding: utf-8 -*-
"""Aggregate root definitions for the MachineClass context."""
from __future__ import absolute_import

from core.MachineClass.domain.entities.machine_class_entity import MachineClassEntity
from core.MachineClass.domain.value_objects.machine_class_identity import MachineClassIdentity


class MachineClassAggregate(object):
    """Aggregate root for MachineClass."""

    def __init__(self, identifier, name, description=None):
        identity = MachineClassIdentity(identifier)
        self._entity = MachineClassEntity(
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
