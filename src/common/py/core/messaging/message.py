import abc
import collections.abc
import dataclasses
import typing
import uuid
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .channel import Channel
from .message_payload import MessagePayload
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
          api_key: An optional API key to access protected resources.
    """

    name: MessageName

    origin: UnitID
    sender: UnitID
    target: Channel

    hops: typing.List[UnitID] = field(default_factory=list)

    trace: Trace = field(default_factory=uuid.uuid4)

    api_key: str = ""

    @staticmethod
    def message_name() -> MessageName:
        """
        Retrieves the name of the message type on a message class basis.
        """
        return ""

    @staticmethod
    def is_protected() -> bool:
        """
        Whether this message is protected and thus requires an API key.
        """
        return False

    @staticmethod
    def define(name: str, is_protected: bool = False):
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
            is_protected: Whether the message requires an API key.
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
            setattr(cls, "message_name", lambda *args, **kwargs: name)
            setattr(cls, "is_protected", lambda *args, **kwargs: is_protected)

            from .message_types_catalog import MessageTypesCatalog

            MessageTypesCatalog.register_item(name, cls)

            return cls

        return decorator

    def __post_init__(self):
        object.__setattr__(self, "_payload", MessagePayload())

    @property
    def payload(self) -> MessagePayload:
        """
        The message payload.
        """
        return typing.cast(MessagePayload, object.__getattribute__(self, "_payload"))

    def __str__(self) -> str:
        def cleanup(cur_obj, parent_obj, parent_key):
            if isinstance(cur_obj, str):
                from ...utils import human_readable_file_size

                if cur_obj.startswith("data:"):
                    parent_obj[parent_key] = (
                        cur_obj.split(",", 1)[0]
                        + f",<data:{human_readable_file_size(len(cur_obj))}>"
                    )
                elif len(cur_obj) > 256:
                    parent_obj[parent_key] = (
                        cur_obj[0:256]
                        + f"... [{human_readable_file_size(len(cur_obj))} total]"
                    )
            elif isinstance(cur_obj, dict):
                for key, value in cur_obj.items():
                    cleanup(value, cur_obj, key)
            elif isinstance(cur_obj, collections.abc.Sequence):
                for value in cur_obj:
                    cleanup(value, parent_obj, parent_key)

        obj_dict = self.to_dict()
        obj_dict["payload"] = str(self.payload)
        cleanup(obj_dict, None, None)
        return str(obj_dict)


# pylint: disable=invalid-name
MessageType = typing.TypeVar("MessageType", bound=Message)
