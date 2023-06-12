import logging
import typing

from .logger_protocol import LoggerProtocol


class Logger(logging.Logger, LoggerProtocol):
    """ Customized logger offering advanced formatting and parameters listing. """
    def __init__(self, name: str, level: int = logging.INFO):
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
        super().setLevel(level)
        for h in self.handlers:
            h.setLevel(level)

    def debug(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        super().debug(msg, extra=self._pack_extra_params(scope, **kwargs))

    def info(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        super().info(msg, extra=self._pack_extra_params(scope, **kwargs))
        
    def warning(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        super().warning(msg, extra=self._pack_extra_params(scope, **kwargs))
        
    def error(self, msg: str, *, scope: str | None = None, **kwargs) -> None:
        super().error(msg, extra=self._pack_extra_params(scope, **kwargs))

    def _pack_extra_params(self, scope: str | None, **kwargs) -> typing.Dict[str, typing.Any]:
        return {"scope": scope, "extra_params": kwargs}
