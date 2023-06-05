import typing

from .service_context import ServiceContextType, ServiceContext
from ..config import Configuration
from ..messaging import Message, MessageName, MessageType
from ..messaging.handlers import MessageHandlers, MessageHandler, MessageHandlerMappings


@typing.final
class Service:
    """ Base service class providing easy message handler mapping. This is the entrypoint into the actual component domain. """
    def __init__(self, name: str, *, context_type: typing.Type[ServiceContextType] = ServiceContext):
        self._name = name
        
        self._message_handlers = MessageHandlers()
        self._context_type = context_type

    def message_handler(self, fltr: str, /, message_type: typing.Type[MessageType] = Message, *, is_async: bool = False) -> typing.Callable[[MessageHandler], MessageHandler]:
        def decorator(handler: MessageHandler) -> MessageHandler:
            self._message_handlers.add_handler(fltr, handler, message_type, is_async)
            return handler
        
        return decorator
    
    def message_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        return self._message_handlers.find_handlers(msg_name)
    
    def create_context(self, msg: Message, config: Configuration) -> ServiceContextType:
        return self._context_type(msg, config)

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Service '{self._name}': {str(self._message_handlers)}"
