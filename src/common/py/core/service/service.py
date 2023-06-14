import typing

from .message_emitter import MessageEmitter
from .service_context import ServiceContextType, ServiceContext
from ..config import Configuration
from ..logging import LoggerProtocol
from ..messaging import Message, MessageName, MessageType, MessageBusProtocol
from ..messaging.handlers import MessageHandlers, MessageHandler, MessageHandlerMappings
from ...component import ComponentID


@typing.final
class Service:
    """ Base service class providing easy message handler mapping. This is the entrypoint into the actual component domain. """
    def __init__(self, comp_id: ComponentID, name: str, *, message_bus: MessageBusProtocol, context_type: typing.Type[ServiceContextType] = ServiceContext):
        self._component_id = comp_id
        self._name = name
        
        self._message_handlers = MessageHandlers()
        self._message_emitter = MessageEmitter(comp_id, message_bus)
        self._context_type = context_type

    def message_handler(self, fltr: str, /, message_type: typing.Type[MessageType] = Message, *, is_async: bool = False) -> typing.Callable[[MessageHandler], MessageHandler]:
        def decorator(handler: MessageHandler) -> MessageHandler:
            self._message_handlers.add_handler(fltr, handler, message_type, is_async)
            return handler
        
        return decorator
    
    def message_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        return self._message_handlers.find_handlers(msg_name)
    
    def create_context(self, config: Configuration, logger: LoggerProtocol) -> ServiceContextType:
        return self._context_type(self._message_emitter, config, logger)

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def message_emitter(self) -> MessageEmitter:
        return self._message_emitter

    def __str__(self) -> str:
        return f"Service '{self._name}': {str(self._message_handlers)}"
