import dataclasses

from .message_meta_information import MessageMetaInformation


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandReplyMetaInformation(MessageMetaInformation):
    """
    Message meta information specific to ``CommandReply``.
    """

    _is_handled_externally: bool = False

    @property
    def is_handled_externally(self) -> bool:
        """
        Whether the message is handled outside the message bus.
        """
        return self._is_handled_externally

    def set_handled_externally(self, value: bool = True) -> None:
        """
        Sets whether the message is handled outside the message bus.
        """
        object.__setattr__(self, "_is_handled_externally", value)
