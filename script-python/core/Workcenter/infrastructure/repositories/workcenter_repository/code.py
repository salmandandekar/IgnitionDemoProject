# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Workcenter context."""
from __future__ import absolute_import

import system.util

from ports.repositories.workcenter_repository import WorkcenterRepository


class IgnitionWorkcenterRepository(WorkcenterRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.workcenter.infrastructure.repositories.workcenter_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Workcenter repository.")
        raise NotImplementedError("Persist Workcenter aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Workcenter repository.")
        raise NotImplementedError("Retrieve Workcenter by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Workcenter repository.")
        raise NotImplementedError("List Workcenter aggregates.")
