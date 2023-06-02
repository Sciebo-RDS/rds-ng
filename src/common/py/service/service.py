import typing

from ..core.messaging import Message, MessageName, MessageType
from ..core.messaging.handlers import MessageHandlers, MessageHandler, MessageHandlersList


@typing.final
class Service:
    """ Base service class providing easy message handler mapping. This is the entrypoint into the actual component domain. """
    def __init__(self, name: str):
        self._name = name
        
        self._message_handlers = MessageHandlers()

    def message_handler(self, fltr: str, /, message_type: typing.Generic[MessageType] = Message) -> typing.Callable[[MessageHandler], MessageHandler]:
        def decorator(handler: MessageHandler) -> MessageHandler:
            self._message_handlers.add_handler(fltr, handler, message_type)
            return handler
        
        return decorator
    
    def handlers(self, msg_name: MessageName) -> MessageHandlersList:
        return self._message_handlers.find_handlers(msg_name)

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Service {self._name}: {str(self._message_handlers)}"
