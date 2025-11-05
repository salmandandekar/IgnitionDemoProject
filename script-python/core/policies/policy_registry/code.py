# -*- coding: utf-8 -*-
"""Policy orchestration entry point."""
from __future__ import absolute_import


def evaluate(policy_name, context):
    """Evaluate a named policy against the provided context."""
    _ = context or {}
    raise NotImplementedError("Define policy '{}'".format(policy_name))
