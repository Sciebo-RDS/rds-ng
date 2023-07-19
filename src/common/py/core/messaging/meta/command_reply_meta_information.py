import dataclasses

from .message_meta_information import MessageMetaInformation


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandReplyMetaInformation(MessageMetaInformation):
    """
    Message meta information specific to ``CommandReply``.
    """
    pass
