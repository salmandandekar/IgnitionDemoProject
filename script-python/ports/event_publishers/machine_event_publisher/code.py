# -*- coding: utf-8 -*-
"""Event publisher port for the Machine context."""
from __future__ import absolute_import


class MachineEventPublisher(object):
    """Contract for publishing Machine domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
