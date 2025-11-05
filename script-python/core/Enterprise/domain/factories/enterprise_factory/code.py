# -*- coding: utf-8 -*-
"""Factories for the Enterprise context."""
from __future__ import absolute_import

from core.Enterprise.domain.aggregates.enterprise_aggregate import EnterpriseAggregate


def create_enterprise(identifier, name, description=None):
    """Create a new Enterprise aggregate instance."""
    return EnterpriseAggregate(identifier=identifier, name=name, description=description)
