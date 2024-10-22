import dataclasses

from ...core.messaging import (
    Command,
    CommandReply,
    Message,
)
from ...core.messaging.composers import (
    CommandComposer,
    CommandReplyComposer,
    MessageBuilder,
)
from ...data.entities.metadata import MetadataProfileContainerList


@Message.define("command/metadata/profiles")
class GetMetadataProfilesCommand(Command):
    """
    Command to fetch all global metadata profiles.

    Notes:
        Requires a ``GetMetadataProfilesReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(GetMetadataProfilesCommand, chain)


@Message.define("command/metadata/profiles/reply")
class GetMetadataProfilesReply(CommandReply):
    """
    Reply to ``GetMetadataProfilesCommand``.

    Args:
        profiles: List of all global profiles.
    """

    profiles: MetadataProfileContainerList = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetMetadataProfilesCommand,
        *,
        profiles: MetadataProfileContainerList,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetMetadataProfilesReply, cmd, success, message, profiles=profiles
        )
