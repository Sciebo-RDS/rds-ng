from ..core.messaging import (
    Command,
    CommandReply,
    Message,
)
from ..core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)


@Message.define("command/general/ping")
class PingCommand(Command):
    """
    A generic PING command.

    Notes:
        Requires a ``PingReply`` reply.
    """

    payload: str = "PING"

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(PingCommand, chain)


@Message.define("command/general/ping/reply")
class PingReply(CommandReply):
    """
    Reply to ``PingCommand``.
    """

    payload: str = "PONG"

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: PingCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(PingReply, cmd, success, message)
