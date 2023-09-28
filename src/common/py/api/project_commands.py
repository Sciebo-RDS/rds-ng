import dataclasses
import typing

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
from ..data.entities import Project


@Message.define("command/project/list")
class ListProjectsCommand(Command):
    """
    Command to fetch all projects of the current user.

    Notes:
        Requires a ``ListProjectsReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(ListProjectsCommand, chain)


@Message.define("command/project/list/reply")
class ListProjectsReply(CommandReply):
    """
    Reply to ``ListProjectsCommand``.
    """

    projects: typing.List[Project] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ListProjectsCommand,
        *,
        projects: typing.List[Project],
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            ListProjectsReply, cmd, success, message, projects=projects
        )
