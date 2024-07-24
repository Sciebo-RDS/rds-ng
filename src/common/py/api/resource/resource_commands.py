import base64
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
from ...data.entities.resource import Resource, ResourcesList


@Message.define("command/resource/assign-broker")
class AssignResourcesBrokerCommand(Command):
    """
    Command to assign a broker to access the user's resources.

    Notes:
        Requires a ``AssignResourcesBrokerReply`` reply.

    Args:
        broker: The broker to use.
        config: The broker configuration.
    """

    broker: str
    config: typing.Dict[str, typing.Any] = dataclasses.field(default_factory=dict)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        broker: str,
        config: typing.Dict[str, typing.Any],
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            AssignResourcesBrokerCommand,
            chain,
            broker=broker,
            config=config,
        )


@Message.define("command/resource/assign-broker/reply")
class AssignResourcesBrokerReply(CommandReply):
    """
    Reply to ``AssignResourcesBrokerCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: AssignResourcesBrokerCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            AssignResourcesBrokerReply, cmd, success, message
        )


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


@Message.define("command/resource/get")
class GetResourceCommand(Command):
    """
    Command to fetch a single resource.

    Notes:
        Requires a ``GetResourceReply`` reply.

    Args:
        resource: The resource.
    """

    resource: Resource

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        resource: Resource,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            ListResourcesCommand,
            chain,
            resource=resource,
        )


@Message.define("command/resource/get/reply")
class GetResourceReply(CommandReply):
    """
    Reply to ``GetResourceCommand``.

    Args:
        resource: The resource path.
        data: The file data (currently base64-encoded).
    """

    resource: Resource
    data: str  # TODO: Support binary data

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetResourceCommand,
        *,
        resource: Resource,
        data: str | bytes,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetResourceReply,
            cmd,
            success,
            message,
            resource=resource,
            data=data if isinstance(data, str) else base64.b64encode(data).decode(),
        )
