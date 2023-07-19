import typing

from .message_emitter import MessageEmitter
from ..logging import LoggerProtocol
from ...utils.config import Configuration


class ServiceContext:
    """
    An execution context for messages dispatched by the message bus.
    
    When a message handler gets executed (i.e., called by the message bus dispatchers), an instance of ``ServiceContext`` (or a subclass)
    is passed to the handler. This context can be seen as a *unit of work* that exists during the execution of the handler. Its main task is to
    hold data that is specific to this single execution.
    
    A service context is used as a context manager. In its ``__exit__`` method, any exceptions will be catched, printed and passed on. This
    makes tracing of errors that occur during message handling easier.
    
    It is also possible to have message handlers receive custom subtypes of this class. See ``Component`` and its ``create_service`` method for
    details.
    
    Args:
        msg_emitter: A ``MessageEmitter`` to be assigned to this context.
        config: The global component configuration.
        logger: A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
    """
    def __init__(self, msg_emitter: MessageEmitter, config: Configuration, logger: LoggerProtocol):
        """
        Args:
            msg_emitter: A ``MessageEmitter`` to be assigned to this context.
            config: The global component configuration.
            logger: A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
        """
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
        """
        The message emitter to be used within this context.
        """
        return self._msg_emitter
    
    @property
    def config(self) -> Configuration:
        """
        The global component configuration.
        """
        return self._config
    
    @property
    def logger(self) -> LoggerProtocol:
        """
        The logger to be used within this context.
        """
        return self._logger


ServiceContextType = typing.TypeVar("ServiceContextType", bound=ServiceContext)
