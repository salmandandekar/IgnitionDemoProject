# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Site context."""
from __future__ import absolute_import

import system.util

from ports.repositories.site_repository import SiteRepository


class IgnitionSiteRepository(SiteRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.site.infrastructure.repositories.site_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Site repository.")
        raise NotImplementedError("Persist Site aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Site repository.")
        raise NotImplementedError("Retrieve Site by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Site repository.")
        raise NotImplementedError("List Site aggregates.")
