# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Area context."""
from __future__ import absolute_import

import system.util

from ports.repositories.area_repository import AreaRepository


class IgnitionAreaRepository(AreaRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.area.infrastructure.repositories.area_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Area repository.")
        raise NotImplementedError("Persist Area aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Area repository.")
        raise NotImplementedError("Retrieve Area by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Area repository.")
        raise NotImplementedError("List Area aggregates.")
