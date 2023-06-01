import abc
import typing

from ..message import Message

MT = typing.TypeVar('MT', bound=Message)


class MessageDispatcher(abc.ABC, typing.Generic[MT]):
    """ The dispatcher sends message to registered handlers while also performing additional tasks like context management. """
    def __init__(self):
        pass

    @abc.abstractmethod
    def dispatch(self, msg: MT) -> None:
        pass
