# -*- coding: utf-8 -*-
"""Event publisher port for the MachineClass context."""
from __future__ import absolute_import


class MachineClassEventPublisher(object):
    """Contract for publishing MachineClass domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
