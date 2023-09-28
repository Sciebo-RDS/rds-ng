import dataclasses
import typing

from .message_meta_information import MessageMetaInformation
from ..command_reply import CommandDoneCallback, CommandFailCallback


@dataclasses.dataclass(frozen=True, kw_only=True)
class CommandMetaInformation(MessageMetaInformation):
    """
    Message meta information specific to ``Command``.

    Attributes:
        requires_reply: Commands always require a reply.
        done_callbacks: Called when a reply was received for this command.
        fail_callbacks: Called when no reply was received for this command or an exception occurred.
        async_callbacks: Whether the callbacks should be invoked asynchronously in their own thread.
        timeout: The timeout (in seconds) before a command is deemed not replied.
    """

    requires_reply: bool = True

    done_callbacks: typing.List[CommandDoneCallback] = dataclasses.field(
        default_factory=list
    )
    fail_callbacks: typing.List[CommandFailCallback] = dataclasses.field(
        default_factory=list
    )

    async_callbacks: bool = False

    timeout: float = 0.0
