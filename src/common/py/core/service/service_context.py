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
        
        self._requires_reply = False
        
    def __enter__(self) -> typing.Self:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            import traceback
            self._logger.error(f"An exception occurred within a service context: {exc_val}", scope="service", exception=str(exc_type))
            self._logger.debug(f"Traceback:\n{''.join(traceback.format_tb(exc_tb))}", scope="service")
            return False
        
        self._check_command_reply()
        return True
    
    def __call__(self, *, requires_reply: bool) -> typing.Self:
        self._requires_reply = requires_reply
        return self
    
    def _check_command_reply(self) -> None:
        from ..messaging import CommandReplyType
        if self._requires_reply and self._msg_emitter.get_message_count(CommandReplyType) == 0:
            self._logger.warning(f"A service context required a command reply, but none was sent", scope="service")
        
    @property
    def message_emitter(self) -> MessageEmitter:
        return self._msg_emitter
    
    @property
    def config(self) -> Configuration:
        return self._config
    
    @property
    def logger(self) -> LoggerProtocol:
        return self._logger


ServiceContextType = typing.TypeVar("ServiceContextType", bound=ServiceContext)
