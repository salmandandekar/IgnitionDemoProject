# -*- coding: utf-8 -*-
"""Factories for the Line context."""
from __future__ import absolute_import

from core.Line.domain.aggregates.line_aggregate import LineAggregate


def create_line(identifier, name, description=None):
    """Create a new Line aggregate instance."""
    return LineAggregate(identifier=identifier, name=name, description=description)
