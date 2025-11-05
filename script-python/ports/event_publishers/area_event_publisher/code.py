# -*- coding: utf-8 -*-
"""Event publisher port for the Area context."""
from __future__ import absolute_import


class AreaEventPublisher(object):
    """Contract for publishing Area domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
