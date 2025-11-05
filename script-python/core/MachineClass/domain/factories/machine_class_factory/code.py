# -*- coding: utf-8 -*-
"""Factories for the MachineClass context."""
from __future__ import absolute_import

from core.MachineClass.domain.aggregates.machine_class_aggregate import MachineClassAggregate


def create_machine_class(identifier, name, description=None):
    """Create a new MachineClass aggregate instance."""
    return MachineClassAggregate(identifier=identifier, name=name, description=description)
