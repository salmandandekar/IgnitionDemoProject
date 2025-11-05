# -*- coding: utf-8 -*-
"""Placeholder command for the Workstation context."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.workstation.application.commands.create_workstation_command"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(payload):
    """Execute the placeholder create command for Workstation."""
    _ = payload or {}
    raise NotImplementedError("Implement the create command for Workstation.")
