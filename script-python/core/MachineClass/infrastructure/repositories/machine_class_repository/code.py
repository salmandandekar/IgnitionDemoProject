# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the MachineClass context."""
from __future__ import absolute_import

import system.util

from ports.repositories.machine_class_repository import MachineClassRepository


class IgnitionMachineClassRepository(MachineClassRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.machine_class.infrastructure.repositories.machine_class_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for MachineClass repository.")
        raise NotImplementedError("Persist MachineClass aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for MachineClass repository.")
        raise NotImplementedError("Retrieve MachineClass by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for MachineClass repository.")
        raise NotImplementedError("List MachineClass aggregates.")
