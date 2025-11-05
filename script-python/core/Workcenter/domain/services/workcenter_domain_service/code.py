# -*- coding: utf-8 -*-
"""Domain services for the Workcenter context."""
from __future__ import absolute_import

from core.Workcenter.domain.events.workcenter_events import WorkcenterCreatedEvent


class WorkcenterDomainService(object):
    """Domain service that orchestrates Workcenter operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return WorkcenterCreatedEvent(identity=identity)
