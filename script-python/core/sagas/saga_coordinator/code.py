# -*- coding: utf-8 -*-
"""Saga coordinator placeholder."""
from __future__ import absolute_import


def execute(saga_name, payload):
    """Coordinate a long-running saga."""
    _ = payload or {}
    raise NotImplementedError("Implement saga '{}'".format(saga_name))
