# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Machine context."""
from __future__ import absolute_import

import system.util

from ports.repositories.machine_repository import MachineRepository


class IgnitionMachineRepository(MachineRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.machine.infrastructure.repositories.machine_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Machine repository.")
        raise NotImplementedError("Persist Machine aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Machine repository.")
        raise NotImplementedError("Retrieve Machine by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Machine repository.")
        raise NotImplementedError("List Machine aggregates.")
