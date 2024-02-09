import dataclasses

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
from ...data.entities.resource import ResourcesList


@Message.define("command/resource/list")
class ListResourcesCommand(Command):
    """
    Command to fetch all available resources.

    Notes:
        Requires a ``ListResourcesReply`` reply.

    Args:
        root: The root path (or empty if the system root should be used).
        include_folders: Whether to list folders (if this is set to false, no recursion will occur independent of `recursive`).
        include_files: Whether to list files.
        recursive: Whether to recursively process all sub-folders as well.
    """

    root: str

    include_folders: bool
    include_files: bool

    recursive: bool

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        root: str = "",
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            ListResourcesCommand,
            chain,
            root=root,
            include_folders=include_folders,
            include_files=include_files,
            recursive=recursive,
        )


@Message.define("command/resource/list/reply")
class ListResourcesReply(CommandReply):
    """
    Reply to ``ListResourcesCommand``.

    Args:
        resources: List of all resources.
    """

    resources: ResourcesList = dataclasses.field(default_factory=ResourcesList)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ListResourcesCommand,
        *,
        resources: ResourcesList,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            ListResourcesReply, cmd, success, message, resources=resources
        )
