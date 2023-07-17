import dataclasses

from .message_meta_information import MessageMetaInformation
from ..command_reply import CommandDoneCallback, CommandFailCallback


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation):
    requires_reply: bool = True
    
    done_callback: CommandDoneCallback | None = None
    fail_callback: CommandFailCallback | None = None
    
    async_callbacks: bool = False
    
    timeout: float = 0.0
