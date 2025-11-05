# -*- coding: utf-8 -*-
"""Repository port definition for the Line context."""
from __future__ import absolute_import


class LineRepository(object):
    """Port describing persistence operations for Line aggregates."""

    def save(self, aggregate):  # pragma: no cover - interface
        raise NotImplementedError

    def get_by_identity(self, identity):  # pragma: no cover - interface
        raise NotImplementedError

    def list(self, filters=None):  # pragma: no cover - interface
        _ = filters or {}
        raise NotImplementedError
