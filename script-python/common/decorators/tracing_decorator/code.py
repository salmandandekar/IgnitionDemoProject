# -*- coding: utf-8 -*-
"""Tracing decorator to standardize execution logging."""
from __future__ import absolute_import

import functools
import time

import system.util


def tracing_decorator(logger_name):
    """Log function entry, exit, and duration."""

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logger = system.util.getLogger(logger_name)
            start_time = time.time()
            logger.info("Entering {0}".format(function.__name__))
            result = function(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000.0
            logger.info(
                "Exiting {0} in {1:.2f} ms".format(function.__name__, duration_ms)
            )
            return result

        return wrapper

    return decorator
