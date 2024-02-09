import dataclasses
import typing
from enum import IntEnum, auto


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageMetaInformation:
    """
    Stores additional information necessary for message dispatching.

    When a message is emitted, additional information is required to be able to properly handle it.
    This includes its entrypoint into the system, as well as whether the message type requires a reply.

    Attributes:
        entrypoint: From where the message entered the system (locally or remotely).
        requires_reply: Whether a reply is expected.
    """

    class Entrypoint(IntEnum):
        """
        Defines from where a message has entered the system.
        """

        LOCAL = auto()
        SERVER = auto()
        CLIENT = auto()

    entrypoint: Entrypoint

    requires_reply: bool = False

    @property
    def is_handled_externally(self) -> bool:
        """
        Whether the message is handled outside the message bus.
        """
        return False


MessageMetaInformationType = typing.TypeVar(
    "MessageMetaInformationType", bound=MessageMetaInformation
)  # pylint: disable=invalid-name
