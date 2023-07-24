from .message_context import MessageContext, MessageContextType
from .message_emitter import MessageEmitter
from .. import MessageBusProtocol
from ...logging import LoggerProtocol
from ..handlers import MessageHandlers
from ....utils import UnitID
from ....utils.config import Configuration


class MessageService:
    """
    Base class for all message services.
    
    A *message service* wraps message handlers and proper message context creation (i.e., using a flexible context type). It
    is used by the message bus as an encapsulated layer for message dispatching.
    """
    def __init__(self, comp_id: UnitID, *, message_bus: MessageBusProtocol, context_type: type[MessageContextType] = MessageContext):
        """
        Args:
            comp_id: The global component identifier.
            message_bus: The global message bus.
            context_type: The type to use when creating a message context.
        """
        self._component_id = comp_id
        
        self._message_bus = message_bus
        self._message_handlers = MessageHandlers()
        self._context_type = context_type
    
    def create_context(self, config: Configuration, logger: LoggerProtocol) -> MessageContext:
        """
        Creates a new service context.
        
        Args:
            config: The global component configuration.
            logger: The logger to be used within the new context.

        Returns:
            The newly created message context.
        """
        return self._context_type(self.create_message_emitter(), config, logger)
    
    def create_message_emitter(self) -> MessageEmitter:
        """
        Creates a new message emitter.
        
        Returns:
            The newly created message emitter.
        """
        return MessageEmitter(self._component_id, self._message_bus)

    @property
    def message_handlers(self) -> MessageHandlers:
        """
        The message handlers maintained by this message service.
        """
        return self._message_handlers
