import logging
import typing

from .logger import Logger
from .logger_proxy import LoggerProxy


logging.setLoggerClass(Logger)
_logger: Logger = logging.getLogger("rds_logger")


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


def default_logger() -> Logger:
    return typing.cast(Logger, _logger)
