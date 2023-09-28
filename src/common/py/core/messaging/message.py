import abc
import dataclasses
import typing
import uuid
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .channel import Channel
from ...utils import UnitID

MessageName = str
Trace = uuid.UUID


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Message(abc.ABC):
    """
    Base class for all messages.

    A message, besides its actual data, consists mainly of information from where it came and where it should go.

    This class also offers a useful decorator to easily declare new messages, like in the following example::

        @Message.define("msg/command")
        class MyCommand(Command):
            some_number: int = 0

    Attributes:
          name: The name of the message.
          origin: The initial source component of the message.
          sender: The component from where the message came from.
          target: Where the message should go to.
          hops: A list of components the message was sent through.
          trace: A unique trace identifying messages that logically belong together.
    """

    name: MessageName

    origin: UnitID
    sender: UnitID
    target: Channel

    hops: typing.List[UnitID] = field(default_factory=list)

    trace: Trace = field(default_factory=uuid.uuid4)

    @staticmethod
    def message_name() -> MessageName:
        """
        Retrieves the name of the message type on a message class basis.
        """
        return ""

    @staticmethod
    def define(name: str):
        """
        Defines a new message.

        The decorator takes care of wrapping the new class as a dataclass, passing the correct message
        name to its constructor. It also registers the new message type in the global ``MessageTypesCatalog``.

        Examples::

            @Message.define("msg/command")
            class MyCommand(Command):
                some_number: int = 0

        Args:
            name: The name of the message.
        """

        def decorator(cls):
            cls = dataclasses.dataclass(frozen=True, kw_only=True)(
                cls
            )  # Wrap the class in a dataclass
            __init__ = cls.__init__

            def __new_init__(self, *args, **kwargs):
                if "name" in kwargs:
                    del kwargs["name"]

                __init__(self, *args, name=MessageName(name), **kwargs)

            setattr(cls, "__init__", __new_init__)
            setattr(cls, "message_name", lambda: name)

            from .message_types_catalog import MessageTypesCatalog

            MessageTypesCatalog.register_item(name, cls)

            return cls

        return decorator


# pylint: disable=invalid-name
MessageType = typing.TypeVar("MessageType", bound=Message)
