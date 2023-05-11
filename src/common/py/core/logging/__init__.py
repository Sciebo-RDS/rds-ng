import logging

from .logger import Logger


logging.setLoggerClass(Logger)
_logger: Logger = logging.getLogger("rds_logger")


def debug(msg: str, *, scope: str | None = None, **kwargs):
    _logger.debug(msg, scope=scope, **kwargs)


def info(msg: str, *, scope: str | None = None, **kwargs):
    _logger.info(msg, scope=scope, **kwargs)


def warning(msg: str, *, scope: str | None = None, **kwargs):
    _logger.warning(msg, scope=scope, **kwargs)


def error(msg: str, *, scope: str | None = None, **kwargs):
    _logger.error(msg, scope=scope, **kwargs)
