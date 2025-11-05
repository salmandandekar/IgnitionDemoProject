# -*- coding: utf-8 -*-
"""Cache port shared across contexts."""
from __future__ import absolute_import


class CachePort(object):
    """Minimal caching interface for adapters."""

    def get(self, key):  # pragma: no cover - interface
        raise NotImplementedError

    def put(self, key, value, ttl=None):  # pragma: no cover - interface
        raise NotImplementedError

    def invalidate(self, key):  # pragma: no cover - interface
        raise NotImplementedError
