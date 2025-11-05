# -*- coding: utf-8 -*-
"""Factories for the Site context."""
from __future__ import absolute_import

from core.Site.domain.aggregates.site_aggregate import SiteAggregate


def create_site(identifier, name, description=None):
    """Create a new Site aggregate instance."""
    return SiteAggregate(identifier=identifier, name=name, description=description)
