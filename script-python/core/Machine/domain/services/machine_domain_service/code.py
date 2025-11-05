# -*- coding: utf-8 -*-
"""Domain services for the Machine context."""
from __future__ import absolute_import

from core.Machine.domain.events.machine_events import MachineCreatedEvent


class MachineDomainService(object):
    """Domain service that orchestrates Machine operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return MachineCreatedEvent(identity=identity)
