# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Enterprise context."""
from __future__ import absolute_import

import system.util

from ports.repositories.enterprise_repository import EnterpriseRepository


class IgnitionEnterpriseRepository(EnterpriseRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.enterprise.infrastructure.repositories.enterprise_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Enterprise repository.")
        raise NotImplementedError("Persist Enterprise aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Enterprise repository.")
        raise NotImplementedError("Retrieve Enterprise by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Enterprise repository.")
        raise NotImplementedError("List Enterprise aggregates.")
