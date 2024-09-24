import dataclasses
import typing

from ...core.messaging import Command, CommandReply, Message
from ...core.messaging.composers import (
    CommandComposer,
    CommandReplyComposer,
    MessageBuilder,
)
from ...data.exporters import ProjectExporterDescriptor


@Message.define("command/project/export/list")
class ListProjectExportersCommand(Command):
    """
    Command to fetch all project exporters.

    Notes:
        Requires a ``ListProjectExportersReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(ListProjectExportersCommand, chain)


@Message.define("command/project/export/list/reply")
class ListProjectExportersReply(CommandReply):
    """
    Reply to ``ListProjectExportersCommand``.

    Args:
        exporters: List of all project exporters.
    """

    exporters: typing.List[ProjectExporterDescriptor] = dataclasses.field(
        default_factory=list
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ListProjectExportersCommand,
        *,
        exporters: typing.List[ProjectExporterDescriptor],
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            ListProjectExportersReply, cmd, success, message, exporters=exporters
        )
