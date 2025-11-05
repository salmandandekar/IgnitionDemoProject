# -*- coding: utf-8 -*-
"""Domain services for the Workstation context."""
from __future__ import absolute_import

from core.Workstation.domain.events.workstation_events import WorkstationCreatedEvent


class WorkstationDomainService(object):
    """Domain service that orchestrates Workstation operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return WorkstationCreatedEvent(identity=identity)
