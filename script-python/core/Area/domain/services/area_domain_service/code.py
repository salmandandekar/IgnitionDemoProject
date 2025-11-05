# -*- coding: utf-8 -*-
"""Domain services for the Area context."""
from __future__ import absolute_import

from core.Area.domain.events.area_events import AreaCreatedEvent


class AreaDomainService(object):
    """Domain service that orchestrates Area operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return AreaCreatedEvent(identity=identity)
