# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Enterprise context."""
from __future__ import absolute_import

from core.Enterprise.domain.entities.enterprise_entity import EnterpriseEntity
from core.Enterprise.domain.value_objects.enterprise_identity import EnterpriseIdentity


class EnterpriseAggregate(object):
    """Aggregate root for Enterprise."""

    def __init__(self, identifier, name, description=None):
        identity = EnterpriseIdentity(identifier)
        self._entity = EnterpriseEntity(
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
