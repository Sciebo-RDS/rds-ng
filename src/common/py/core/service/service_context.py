import typing

from .message_emitter import MessageEmitter
from ..config import Configuration
from ..logging import LoggerProtocol


class ServiceContext:
    """ An execution context for messages dispatched by the message bus. """
    def __init__(self, msg_emitter: MessageEmitter, config: Configuration, logger: LoggerProtocol):
        self._msg_emitter = msg_emitter
        
        self._config = config
        self._logger = logger
        
        self._is_async = False
        
    def __enter__(self) -> typing.Self:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # TODO: Exception handling
        return True
    
    def __call__(self, is_async: bool = True) -> typing.Self:
        self._is_async = is_async
        return self
        
    @property
    def message_emitter(self) -> MessageEmitter:
        return self._msg_emitter
    
    @property
    def config(self) -> Configuration:
        return self._config
    
    @property
    def logger(self) -> LoggerProtocol:
        return self._logger
    
    @property
    def is_async(self) -> bool:
        return self._is_async


ServiceContextType = typing.TypeVar("ServiceContextType", bound=ServiceContext)
