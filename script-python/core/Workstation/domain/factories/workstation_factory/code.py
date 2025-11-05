# -*- coding: utf-8 -*-
"""Factories for the Workstation context."""
from __future__ import absolute_import

from core.Workstation.domain.aggregates.workstation_aggregate import WorkstationAggregate


def create_workstation(identifier, name, description=None):
    """Create a new Workstation aggregate instance."""
    return WorkstationAggregate(identifier=identifier, name=name, description=description)
