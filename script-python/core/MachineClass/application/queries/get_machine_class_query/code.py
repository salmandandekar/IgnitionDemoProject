# -*- coding: utf-8 -*-
"""Placeholder query for the MachineClass context."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.machine_class.application.queries.get_machine_class_query"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(criteria):
    """Execute the placeholder get query for MachineClass."""
    _ = criteria or {}
    raise NotImplementedError("Implement the get query for MachineClass.")
