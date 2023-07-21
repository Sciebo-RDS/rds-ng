import logging
import typing


class Logger(logging.Logger):
    """
    A customized logger offering advanced formatting and parameters listing.

    This logger and its corresponding ``Formatter`` display the log level, scope, as well as a parameters listing
    in a color-rich format for easy readability.
    """
    def __init__(self, name: str, level: int = logging.INFO):
        """
        Args:
            name: The name of the logger.
            level: The maximum level for log entries to be displayed.
        """
        super().__init__(name, level)
        
        self.addHandler(self._create_default_handler())

    def _create_default_handler(self) -> logging.Handler:
        import sys
        from .formatter import Formatter
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.level)
        handler.setFormatter(Formatter())
        return handler
    
    def setLevel(self, level: int) -> None:
        """
        Sets the logging level of this logger.
        
        Args:
            level: The maximum level for entries to be logged.
        """
        super().setLevel(level)
        for handler in self.handlers:
            handler.setLevel(level)

    def debug(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs a debugging message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        super().debug(msg, extra=self._pack_extra_params(scope, **kwargs))

    def info(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs an information message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        super().info(msg, extra=self._pack_extra_params(scope, **kwargs))
        
    def warning(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs a warning message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        super().warning(msg, extra=self._pack_extra_params(scope, **kwargs))
        
    def error(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        """
        Logs an error message.

        Args:
            msg: The text to log.
            scope: The scope of the entry.
            **kwargs: Any additional parameters.
        """
        super().error(msg, extra=self._pack_extra_params(scope, **kwargs))

    def _pack_extra_params(self, scope: str | None, **kwargs) -> typing.Dict[str, typing.Any]:
        return {"scope": scope, "extra_params": kwargs}
