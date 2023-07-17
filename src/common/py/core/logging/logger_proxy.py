import typing

from .logger import Logger


class LoggerProxy:
    """ A proxy to automatically pass extra parameters to a logger. """
    def __init__(self, logger: Logger):
        self._logger = logger
        
        self._auto_params: typing.Dict[str, typing.Any] = {}
        
    def add_param(self, name: str, value: typing.Any) -> None:
        self._auto_params[name] = value
        
    def remove_param(self, name: str) -> None:
        try:
            self._auto_params.pop(name)
        except KeyError:
            pass
        
    def clear_params(self) -> None:
        self._auto_params = {}
    
    def debug(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        self._logger.debug(msg, scope=scope, **(kwargs | self._auto_params))
    
    def info(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        self._logger.info(msg, scope=scope, **(kwargs | self._auto_params))
    
    def warning(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        self._logger.warning(msg, scope=scope, **(kwargs | self._auto_params))
    
    def error(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        self._logger.error(msg, scope=scope, **(kwargs | self._auto_params))
