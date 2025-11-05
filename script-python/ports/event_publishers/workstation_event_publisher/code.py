# -*- coding: utf-8 -*-
"""Event publisher port for the Workstation context."""
from __future__ import absolute_import


class WorkstationEventPublisher(object):
    """Contract for publishing Workstation domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
