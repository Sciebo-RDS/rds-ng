import dataclasses

from .message_meta_information import MessageMetaInformation
from ..command_reply import CommandReplyCallback


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation):
    done_callback: CommandReplyCallback | None = None
    fail_callback: CommandReplyCallback | None = None
    async_callbacks: bool = False
