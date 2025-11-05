# -*- coding: utf-8 -*-
"""Placeholder query for the Line context."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.line.application.queries.get_line_query"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(criteria):
    """Execute the placeholder get query for Line."""
    _ = criteria or {}
    raise NotImplementedError("Implement the get query for Line.")
