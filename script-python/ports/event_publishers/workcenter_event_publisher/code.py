# -*- coding: utf-8 -*-
"""Event publisher port for the Workcenter context."""
from __future__ import absolute_import


class WorkcenterEventPublisher(object):
    """Contract for publishing Workcenter domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
