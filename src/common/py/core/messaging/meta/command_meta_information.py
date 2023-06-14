import dataclasses

from common.py.core.messaging.command_reply import CommandReplyCallback
from .message_meta_information import MessageMetaInformation


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation):
    done_callback: CommandReplyCallback | None = None
    fail_callback: CommandReplyCallback | None = None
