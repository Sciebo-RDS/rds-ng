import logging
import sys
import typing


class Logger(logging.Logger):
    """ Customized logger offering advanced formatting and parameters listing. """
    def __init__(self, name: str):
        from ..core import Core
        
        super().__init__(name, logging.DEBUG if Core.is_debug_mode else logging.INFO)
        
        self.addHandler(self._create_default_handler())

    def _create_default_handler(self) -> logging.Handler:
        from .formatter import Formatter
        
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.level)
        handler.setFormatter(Formatter())
        return handler

    def debug(self, msg: str, *, scope: str | None = None, **kwargs):
        super().debug(msg, extra=self._pack_extra_args(scope, **kwargs))

    def info(self, msg: str, *, scope: str | None = None, **kwargs):
        super().info(msg, extra=self._pack_extra_args(scope, **kwargs))
        
    def warning(self, msg: str, *, scope: str | None = None, **kwargs):
        super().warning(msg, extra=self._pack_extra_args(scope, **kwargs))
        
    def error(self, msg: str, *, scope: str | None = None, **kwargs):
        super().error(msg, extra=self._pack_extra_args(scope, **kwargs))

    def _pack_extra_args(self, scope: str | None, **kwargs) -> typing.Dict[str, typing.Any]:
        return {"scope": scope, "extra_params": kwargs}
    
