# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Workcenter context."""
from __future__ import absolute_import

from core.Workcenter.domain.entities.workcenter_entity import WorkcenterEntity
from core.Workcenter.domain.value_objects.workcenter_identity import WorkcenterIdentity


class WorkcenterAggregate(object):
    """Aggregate root for Workcenter."""

    def __init__(self, identifier, name, description=None):
        identity = WorkcenterIdentity(identifier)
        self._entity = WorkcenterEntity(
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
