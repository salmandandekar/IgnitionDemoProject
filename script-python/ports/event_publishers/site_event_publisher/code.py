# -*- coding: utf-8 -*-
"""Event publisher port for the Site context."""
from __future__ import absolute_import


class SiteEventPublisher(object):
    """Contract for publishing Site domain events."""

    def publish_created(self, event):  # pragma: no cover - interface
        raise NotImplementedError
