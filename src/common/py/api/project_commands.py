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
from ..data.entities import Project, ProjectID, ProjectFeatureStore, ProjectFeatureID


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
        features_selection: List of enabled user-selectable features.

    Notes:
        Requires a ``CreateProjectReply`` reply.
    """

    title: str
    description: str

    features_selection: typing.List[ProjectFeatureID] = dataclasses.field(
        default_factory=list
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        title: str,
        description: str,
        features_selection: typing.List[ProjectFeatureID],
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
            features_selection=features_selection,
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
    Note that the project features are updated using a separate ``UpdateProjectFeaturesCommand`` message.

    Args:
        project_id: The ID of the project to update.
        title: The title of the project.
        description: An optional project description.
        features_selection: List of enabled user-selectable features.

    Notes:
        Requires an ``UpdateProjectReply`` reply.
    """

    project_id: ProjectID

    title: str
    description: str

    features_selection: typing.List[ProjectFeatureID] = dataclasses.field(
        default_factory=list
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        title: str,
        description: str,
        features_selection: typing.List[ProjectFeatureID],
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            UpdateProjectCommand,
            chain,
            project_id=project_id,
            title=title,
            description=description,
            features_selection=features_selection,
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
