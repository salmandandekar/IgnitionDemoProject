# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Workstation context."""
from __future__ import absolute_import

from core.Workstation.domain.entities.workstation_entity import WorkstationEntity
from core.Workstation.domain.value_objects.workstation_identity import WorkstationIdentity


class WorkstationAggregate(object):
    """Aggregate root for Workstation."""

    def __init__(self, identifier, name, description=None):
        identity = WorkstationIdentity(identifier)
        self._entity = WorkstationEntity(
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
