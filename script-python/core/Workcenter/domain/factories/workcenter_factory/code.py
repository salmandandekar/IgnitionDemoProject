# -*- coding: utf-8 -*-
"""Factories for the Workcenter context."""
from __future__ import absolute_import

from core.Workcenter.domain.aggregates.workcenter_aggregate import WorkcenterAggregate


def create_workcenter(identifier, name, description=None):
    """Create a new Workcenter aggregate instance."""
    return WorkcenterAggregate(identifier=identifier, name=name, description=description)
