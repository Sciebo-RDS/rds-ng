import dataclasses

from .message_meta_information import MessageMetaInformation
from ..command_reply import CommandDoneCallback, CommandFailCallback


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation):
    """
    Message meta information specific to ``Command``.
    
    Attributes:
        requires_reply: Commands always require a reply.
        done_callback: Called when a reply was received for this command.
        fail_callback: Called when no reply was received for this command or an exception occurred.
        async_callbacks: Whether the callbacks should be invoked asynchronously in their own thread.
        timeout: The timeout (in seconds) before a command is deemed not replied.
    """
    requires_reply: bool = True
    
    done_callback: CommandDoneCallback | None = None
    fail_callback: CommandFailCallback | None = None
    
    async_callbacks: bool = False
    
    timeout: float = 0.0
