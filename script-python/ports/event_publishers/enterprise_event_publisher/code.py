# -*- coding: utf-8 -*-
"""Event publisher port for the Enterprise context."""
from __future__ import absolute_import


class EnterpriseEventPublisher(object):
    """Contract for publishing Enterprise domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
