import typing

from ..config import Configuration
from ..logging import LoggerProxy, default_logger
from ..messaging import Message, Trace


class ServiceContext:
    """ An execution context for messages dispatched by the message bus. """
    def __init__(self, msg: Message, config: Configuration):
        self._message = msg
        self._config = config
        self._logger_proxy = self._create_logger_proxy(msg.trace)
        
    def _create_logger_proxy(self, trace: Trace) -> LoggerProxy:
        proxy = LoggerProxy(default_logger())
        proxy.add_param("trace", str(trace))
        return proxy
    
    def __enter__(self) -> typing.Self:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # TODO: Exception handling
        return True
    
    @property
    def config(self) -> Configuration:
        return self._config
    
    @property
    def logger(self) -> LoggerProxy:
        return self._logger_proxy


ServiceContextType = typing.TypeVar("ServiceContextType", bound=ServiceContext)
