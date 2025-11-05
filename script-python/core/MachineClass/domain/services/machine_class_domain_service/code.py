# -*- coding: utf-8 -*-
"""Domain services for the MachineClass context."""
from __future__ import absolute_import

from core.MachineClass.domain.events.machine_class_events import MachineClassCreatedEvent


class MachineClassDomainService(object):
    """Domain service that orchestrates MachineClass operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return MachineClassCreatedEvent(identity=identity)
