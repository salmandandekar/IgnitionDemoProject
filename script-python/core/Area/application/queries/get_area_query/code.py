# -*- coding: utf-8 -*-
"""Placeholder query for the Area context."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.area.application.queries.get_area_query"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(criteria):
    """Execute the placeholder get query for Area."""
    _ = criteria or {}
    raise NotImplementedError("Implement the get query for Area.")
