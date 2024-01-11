import dataclasses
import typing

from ...core.messaging import (
    Command,
    CommandReply,
    Message,
)
from ...core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)
from ...data.entities import (
    Connector,
)


@Message.define("command/connector/list")
class ListConnectorsCommand(Command):
    """
    Command to fetch all available connectors.

    Notes:
        Requires a ``ListConnectorsReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(ListConnectorsCommand, chain)


@Message.define("command/connector/list/reply")
class ListConnectorsReply(CommandReply):
    """
    Reply to ``ListConnectorsCommand``.

    Args:
        connectors: List of all connectors.
    """

    connectors: typing.List[Connector] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ListConnectorsCommand,
        *,
        connectors: typing.List[Connector],
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            ListConnectorsReply, cmd, success, message, connectors=connectors
        )
