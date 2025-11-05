# -*- coding: utf-8 -*-
"""Aggregate root definitions for the Site context."""
from __future__ import absolute_import

from core.Site.domain.entities.site_entity import SiteEntity
from core.Site.domain.value_objects.site_identity import SiteIdentity


class SiteAggregate(object):
    """Aggregate root for Site."""

    def __init__(self, identifier, name, description=None):
        identity = SiteIdentity(identifier)
        self._entity = SiteEntity(
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
