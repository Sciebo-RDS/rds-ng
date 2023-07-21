import typing

from .message_emitter import MessageEmitter
from .service_context import ServiceContextType, ServiceContext
from ..logging import LoggerProtocol
from ..messaging import Message, MessageName, MessageType, MessageBusProtocol
from ..messaging.handlers import MessageHandlers, MessageHandler, MessageHandlerMappings
from ...utils import UnitID
from ...utils.config import Configuration


@typing.final
class Service:
    """
    Base service class providing easy message handler mapping.
    
    A service can be seen as the bridge between the inner workings of a component (represented by a ``Core``) and the
    outside component domain.
    
    Services register the various message handlers that are called when a certain message is received by the message bus and
    dispatched locally. They also create instances of ``ServiceContext`` (or a subclass) that represent a single *unit of work*
    when executing a message handler.
    
    Message handlers are defined using the ``message_handler`` decorator, as can be seen in this example (``svc`` being a ``Service`` instance)::
        
        @svc.message_handler("msg/event", Event)
        def h(msg: Event, ctx: ServiceContext) -> None:
            ctx.logger.info(f"EVENT HANDLER CALLED")
    """
    def __init__(self, comp_id: UnitID, name: str, *, message_bus: MessageBusProtocol, context_type: type[ServiceContextType] = ServiceContext):
        """
        Args:
            comp_id: The global component identifier.
            name: The service name.
            message_bus: The global message bus.
            context_type: The type to use when creating a service context.
        """
        self._component_id = comp_id
        self._name = name
        
        self._message_bus = message_bus
        self._message_handlers = MessageHandlers()
        self._context_type = context_type

    def message_handler(self, fltr: str, /, message_type: type[MessageType] = Message, *, is_async: bool = False) -> typing.Callable[[MessageHandler], MessageHandler]:
        """
        A decorator to declare a message handler.
        
        To define a new message handler, use the following pattern::
        
            @svc.message_handler("msg/event", Event)
            def h(msg: Event, ctx: ServiceContext) -> None:
                ctx.logger.info(f"EVENT HANDLER CALLED")
        
        Args:
            fltr: The message name filter to match against; wildcards (*) are supported for more generic handlers.
            message_type: The type of the message.
            is_async: Whether to execute the handler asynchronously in its own thread.
        """
        def decorator(handler: MessageHandler) -> MessageHandler:
            self._message_handlers.add_handler(fltr, handler, message_type, is_async)
            return handler
        
        return decorator
    
    def message_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        """
        Gets a list of all message handlers for the specified name.
        
        Args:
            msg_name: The message name filter to match against; wildcards (*) are supported for more generic handlers.

        Returns:
            A list of all matching message handlers.
        """
        return self._message_handlers.find_handlers(msg_name)
    
    def create_context(self, config: Configuration, logger: LoggerProtocol) -> ServiceContextType:
        """
        Creates a new service context.
        
        Args:
            config: The global component configuration.
            logger: The logger to be used within the new context.

        Returns:
            The newly created service context.
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
    def name(self) -> str:
        """
        The name of this service.
        """
        return self._name
    
    @property
    def message_emitter(self) -> MessageEmitter:
        """
        The service's message emitter.
        """
        return self.create_message_emitter()

    def __str__(self) -> str:
        return self._name
