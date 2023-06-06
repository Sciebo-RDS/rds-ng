import logging
import typing

from .logger import Logger
from .extended_logger import ExtendedLogger
from .logger_proxy import LoggerProxy


logging.setLoggerClass(ExtendedLogger)
_logger = typing.cast(ExtendedLogger, logging.getLogger("rds_logger"))


def set_level(level: int) -> None:
    _logger.setLevel(level)
    
    
def debug(msg: str, *, scope: str | None = None, **kwargs):
    _logger.debug(msg, scope=scope, **kwargs)


def info(msg: str, *, scope: str | None = None, **kwargs):
    _logger.info(msg, scope=scope, **kwargs)


def warning(msg: str, *, scope: str | None = None, **kwargs):
    _logger.warning(msg, scope=scope, **kwargs)


def error(msg: str, *, scope: str | None = None, **kwargs):
    _logger.error(msg, scope=scope, **kwargs)


def default_logger() -> ExtendedLogger:
    return _logger
