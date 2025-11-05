# -*- coding: utf-8 -*-
"""Domain services for the Enterprise context."""
from __future__ import absolute_import

from core.Enterprise.domain.events.enterprise_events import EnterpriseCreatedEvent


class EnterpriseDomainService(object):
    """Domain service that orchestrates Enterprise operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return EnterpriseCreatedEvent(identity=identity)
