import abc
import typing

from ..handlers import MessageHandlerMappings
from ..message import MessageType


class MessageDispatcher(abc.ABC, typing.Generic[MessageType]):
    """ The dispatcher sends message to registered handlers while also performing additional tasks like context management. """
    def __init__(self):
        pass

    @abc.abstractmethod
    def dispatch(self, msg: MessageType, handlers: MessageHandlerMappings) -> None:
        for handler in handlers:
            if isinstance(msg, handler.message_type):
                handler.handler(typing.cast(handler.message_type, msg))
            else:
                raise RuntimeError(f"Handler {str(handler.handler)} requires messages of type {str(handler.message_type)}, but got {str(type(msg))}")
