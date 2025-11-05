# -*- coding: utf-8 -*-
"""Domain services for the Line context."""
from __future__ import absolute_import

from core.Line.domain.events.line_events import LineCreatedEvent


class LineDomainService(object):
    """Domain service that orchestrates Line operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return LineCreatedEvent(identity=identity)
