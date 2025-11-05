# -*- coding: utf-8 -*-
"""Factories for the Machine context."""
from __future__ import absolute_import

from core.Machine.domain.aggregates.machine_aggregate import MachineAggregate


def create_machine(identifier, name, description=None):
    """Create a new Machine aggregate instance."""
    return MachineAggregate(identifier=identifier, name=name, description=description)
