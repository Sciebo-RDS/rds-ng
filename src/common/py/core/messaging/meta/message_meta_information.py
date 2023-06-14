import dataclasses
import typing


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessageMetaInformation:
    """ A helper class storing information necessary for dispatching and handling messages. """
    pass


MessageMetaInformationType = typing.TypeVar("MessageMetaInformationType", bound=MessageMetaInformation)
