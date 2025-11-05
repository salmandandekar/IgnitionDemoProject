# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Line context."""
from __future__ import absolute_import

from core.Line.domain.entities.line_entity import LineEntity
from core.Line.domain.value_objects.line_identity import LineIdentity


class LineAggregate(object):
    """Aggregate root for Line."""

    def __init__(self, identifier, name, description=None):
        identity = LineIdentity(identifier)
        self._entity = LineEntity(
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
