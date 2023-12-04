import dataclasses
import typing
from enum import IntFlag, auto

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
from ..data.entities import Project, ProjectID, ProjectFeature


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

    Args:
        projects: List of all projects.
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


@Message.define("command/project/create")
class CreateProjectCommand(Command):
    """
    Command to create a new project.

    Args:
        title: The title of the project.
        description: An optional project description.

    Notes:
        Requires a ``CreateProjectReply`` reply.
    """

    title: str
    description: str

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        title: str,
        description: str,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            CreateProjectCommand,
            chain,
            title=title,
            description=description,
        )


@Message.define("command/project/create/reply")
class CreateProjectReply(CommandReply):
    """
    Reply to ``CreateProjectCommand``.

    Args:
        project_id: The ID of the created project.
    """

    project_id: ProjectID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: CreateProjectCommand,
        *,
        project_id: ProjectID,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            CreateProjectReply, cmd, success, message, project_id=project_id
        )


@Message.define("command/project/update")
class UpdateProjectCommand(Command):
    """
    Command to update an existing project.

    Args:
        project_id: The ID of the project to update.
        scope: The scope of which parts of the project to update.
        title: The title of the project.
        description: An optional project description.

    Notes:
        Requires an ``UpdateProjectReply`` reply.
    """

    class Scope(IntFlag):
        NONE = 0x0000
        HEAD = 0x0001
        FEATURES = 0x0002

    project_id: ProjectID
    scope: Scope

    # Scope: HEAD
    title: str
    description: str

    # Scope: FEATURES
    features: typing.List[ProjectFeature] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        scope: Scope,
        title: str,
        description: str,
        features: typing.List[ProjectFeature],
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            UpdateProjectCommand,
            chain,
            project_id=project_id,
            scope=scope,
            title=title,
            description=description,
            features=features,
        )


@Message.define("command/project/update/reply")
class UpdateProjectReply(CommandReply):
    """
    Reply to ``UpdateProjectCommand``.

    Args:
        project_id: The ID of the updated project.
    """

    project_id: ProjectID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: UpdateProjectCommand,
        *,
        project_id: ProjectID,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            UpdateProjectReply, cmd, success, message, project_id=project_id
        )


@Message.define("command/project/delete")
class DeleteProjectCommand(Command):
    """
    Command to delete a project of the current user.

    Args:
        project_id: The ID of the project to delete.

    Notes:
        Requires a ``DeleteProjectReply`` reply.
    """

    project_id: ProjectID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            DeleteProjectCommand, chain, project_id=project_id
        )


@Message.define("command/project/delete/reply")
class DeleteProjectReply(CommandReply):
    """
    Reply to ``DeleteProjectCommand``.

    Args:
        project_id: The ID of the deleted project.
    """

    project_id: ProjectID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: DeleteProjectCommand,
        *,
        project_id: ProjectID,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            DeleteProjectReply, cmd, success, message, project_id=project_id
        )
