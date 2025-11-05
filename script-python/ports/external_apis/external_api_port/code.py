# -*- coding: utf-8 -*-
"""External API port shared across integrations."""
from __future__ import absolute_import


class ExternalAPIPort(object):
    """Defines contract for calling external services."""

    def request(self, endpoint, payload=None):  # pragma: no cover - interface
        _ = payload or {}
        raise NotImplementedError
