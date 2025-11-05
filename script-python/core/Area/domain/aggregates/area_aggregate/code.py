# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Area context."""
from __future__ import absolute_import

from core.Area.domain.entities.area_entity import AreaEntity
from core.Area.domain.value_objects.area_identity import AreaIdentity


class AreaAggregate(object):
    """Aggregate root for Area."""

    def __init__(self, identifier, name, description=None):
        identity = AreaIdentity(identifier)
        self._entity = AreaEntity(
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
