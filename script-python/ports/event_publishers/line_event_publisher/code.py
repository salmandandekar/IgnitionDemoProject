# -*- coding: utf-8 -*-
"""Event publisher port for the Line context."""
from __future__ import absolute_import


class LineEventPublisher(object):
    """Contract for publishing Line domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
