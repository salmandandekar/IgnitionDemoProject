# -*- coding: utf-8 -*-
"""Factories for the Area context."""
from __future__ import absolute_import

from core.Area.domain.aggregates.area_aggregate import AreaAggregate


def create_area(identifier, name, description=None):
    """Create a new Area aggregate instance."""
    return AreaAggregate(identifier=identifier, name=name, description=description)
