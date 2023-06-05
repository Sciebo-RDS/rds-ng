import typing
from concurrent.futures import Future

from ..config import Configuration
from ..logging import LoggerProxy, default_logger
from ..messaging import Message, Trace


class ServiceContext:
    """ An execution context for messages dispatched by the message bus. """
    def __init__(self, msg: Message, config: Configuration):
        self._message = msg
        self._config = config
        self._logger_proxy = self._create_logger_proxy(msg.trace)
        
        self._is_async = False
        
    def _create_logger_proxy(self, trace: Trace) -> LoggerProxy:
        proxy = LoggerProxy(default_logger())
        proxy.add_param("trace", str(trace))
        return proxy
    
    def __enter__(self) -> typing.Self:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # TODO: Exception handling
        return True
    
    def __call__(self, is_async: bool = True) -> typing.Self:
        self._is_async = is_async
        return self
        
    @property
    def config(self) -> Configuration:
        return self._config
    
    @property
    def logger(self) -> LoggerProxy:
        return self._logger_proxy
    
    @property
    def is_async(self) -> bool:
        return self._is_async


ServiceContextType = typing.TypeVar("ServiceContextType", bound=ServiceContext)
