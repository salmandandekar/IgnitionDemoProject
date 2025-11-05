# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Workstation context."""
from __future__ import absolute_import

import system.util

from ports.repositories.workstation_repository import WorkstationRepository


class IgnitionWorkstationRepository(WorkstationRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.workstation.infrastructure.repositories.workstation_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Workstation repository.")
        raise NotImplementedError("Persist Workstation aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Workstation repository.")
        raise NotImplementedError("Retrieve Workstation by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Workstation repository.")
        raise NotImplementedError("List Workstation aggregates.")
