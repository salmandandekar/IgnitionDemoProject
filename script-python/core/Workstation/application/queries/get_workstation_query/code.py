# -*- coding: utf-8 -*-
"""Placeholder query for the Workstation context."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.workstation.application.queries.get_workstation_query"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(criteria):
    """Execute the placeholder get query for Workstation."""
    _ = criteria or {}
    raise NotImplementedError("Implement the get query for Workstation.")
