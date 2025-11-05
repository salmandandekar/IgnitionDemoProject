# -*- coding: utf-8 -*-
"""Logging decorator for consistent exception reporting."""
from __future__ import absolute_import

import functools
import traceback

import system.util


def exception_logger(logger_name):
    """Wrap a callable with structured exception logging."""

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logger = system.util.getLogger(logger_name)
            try:
                return function(*args, **kwargs)
            except Exception as error:
                message = "Unhandled exception in {0}: {1}".format(
                    function.__name__, error
                )
                logger.error(
                    "{0}\n{1}".format(message, traceback.format_exc())
                )
                raise

        return wrapper

    return decorator
