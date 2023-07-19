import typing

from .logger import Logger


class LoggerProxy:
    """
    A proxy to automatically pass extra parameters to a logger.
    
    This class allows us to store additional, fixed parameters passed to an existing logger, avoiding the need to use
    a new logger instance. It offers the same public interface as an actual ``Logger`` and can thus be used like a
    *real* logger.
    
    Args:
        logger: The logger to use.
    """
    def __init__(self, logger: Logger):
        """
        Args:
            logger: The logger to use.
        """
        self._logger = logger
        
        self._auto_params: typing.Dict[str, typing.Any] = {}
        
    def add_param(self, name: str, value: typing.Any) -> None:
        """
        Adds a new paramter that is always automatically passed to the logger.
        
        Args:
            name: The name of the parameter.
            value: Its value.
        """
        self._auto_params[name] = value
        
    def remove_param(self, name: str) -> None:
        """
        Removes a parameter that has been added previously.
        """
        try:
            self._auto_params.pop(name)
        except KeyError:
            pass
        
    def clear_params(self) -> None:
        """
        Removes all stored parameters.
        """
        self._auto_params = {}
    
    def debug(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs a debugging message.
        
        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        self._logger.debug(msg, scope=scope, **(kwargs | self._auto_params))
    
    def info(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs an information message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        self._logger.info(msg, scope=scope, **(kwargs | self._auto_params))
    
    def warning(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs a warning message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        self._logger.warning(msg, scope=scope, **(kwargs | self._auto_params))
    
    def error(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs an error message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        self._logger.error(msg, scope=scope, **(kwargs | self._auto_params))
