import dataclasses
import typing
from enum import IntEnum, auto


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageMetaInformation:
    """ A helper class storing information necessary for dispatching and handling messages. """
    class Entrypoint(IntEnum):
        LOCAL = auto()
        SERVER = auto()
        CLIENT = auto()
    
    entrypoint: Entrypoint
    
    requires_reply: bool = False


MessageMetaInformationType = typing.TypeVar("MessageMetaInformationType", bound=MessageMetaInformation)
