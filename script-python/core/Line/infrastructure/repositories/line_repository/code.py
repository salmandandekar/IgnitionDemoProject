# -*- coding: utf-8 -*-
"""Ignition repository implementation placeholder for the Line context."""
from __future__ import absolute_import

import system.util

from ports.repositories.line_repository import LineRepository


class IgnitionLineRepository(LineRepository):
    """Repository implementation using Ignition platform services."""

    def __init__(self):
        self._logger = system.util.getLogger("core.line.infrastructure.repositories.line_repository")

    def save(self, aggregate):  # pragma: no cover - infrastructure placeholder
        self._logger.warn("Save not implemented for Line repository.")
        raise NotImplementedError("Persist Line aggregate.")

    def get_by_identity(self, identity):  # pragma: no cover
        self._logger.warn("Lookup not implemented for Line repository.")
        raise NotImplementedError("Retrieve Line by identity.")

    def list(self, filters=None):  # pragma: no cover
        _ = filters or {}
        self._logger.warn("List not implemented for Line repository.")
        raise NotImplementedError("List Line aggregates.")
