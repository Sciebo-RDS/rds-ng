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
        pass
