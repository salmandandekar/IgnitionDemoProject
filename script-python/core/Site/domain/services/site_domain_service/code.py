# -*- coding: utf-8 -*-
"""Domain services for the Site context."""
from __future__ import absolute_import

from core.Site.domain.events.site_events import SiteCreatedEvent


class SiteDomainService(object):
    """Domain service that orchestrates Site operations."""

    def build_created_event(self, aggregate):
        if aggregate is None:
            raise ValueError("Aggregate is required.")
        identity = aggregate.identity.value
        return SiteCreatedEvent(identity=identity)
