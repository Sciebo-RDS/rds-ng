import logging
import typing

from .logger import Logger
from .logger_protocol import LoggerProtocol
from .logger_proxy import LoggerProxy

logging.setLoggerClass(Logger)
_logger = typing.cast(Logger, logging.getLogger("rds_logger"))
logging.setLoggerClass(logging.Logger)


def set_level(level: int) -> None:
    """
    Sets the global logging level.

    Args:
        level: The logging level.
    """
    _logger.setLevel(level)


def debug(msg: str, *, scope: str | None = None, **kwargs):
    """
    Logs a debugging message.

    Args:
        msg: The text to log.
        scope: The scope of the entry.
        **kwargs: Any additional parameters.
    """
    _logger.debug(msg, scope=scope, **kwargs)


def info(msg: str, *, scope: str | None = None, **kwargs):
    """
    Logs an information message.

    Args:
        msg: The text to log.
        scope: The scope of the entry.
        **kwargs: Any additional parameters.
    """
    _logger.info(msg, scope=scope, **kwargs)


def warning(msg: str, *, scope: str | None = None, **kwargs):
    """
    Logs a warning message.

    Args:
        msg: The text to log.
        scope: The scope of the entry.
        **kwargs: Any additional parameters.
    """
    _logger.warning(msg, scope=scope, **kwargs)


def error(msg: str, *, scope: str | None = None, **kwargs):
    """
    Logs an error message.

    Args:
    msg: The text to log.
    scope: The scope of the entry.
    **kwargs: Any additional parameters.
    """
    _logger.error(msg, scope=scope, **kwargs)


def default_logger() -> Logger:
    """
    Retrieves the default (global) logger.
    """
    return _logger
