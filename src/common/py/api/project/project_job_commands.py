import dataclasses
import typing
from dataclasses import field

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
from ...data.entities.connector import ConnectorInstanceID
from ...data.entities.project import ProjectID, ProjectJob, Project
from ...data.entities.resource import ResourcesBrokerToken
from ...data.entities.user import UserToken
from ...data.exporters import ProjectExporterID


@Message.define("command/project-job/list")
class ListProjectJobsCommand(Command):
    """
    Command to fetch all project jobs of the current user.

    Notes:
        Requires a ``ListProjectJobsReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(ListProjectJobsCommand, chain)


@Message.define("command/project-job/list/reply")
class ListProjectJobsReply(CommandReply):
    """
    Reply to ``ListJobsCommand``.

    Args:
        jobs: List of all project jobs.
    """

    jobs: typing.List[ProjectJob] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ListProjectJobsCommand,
        *,
        jobs: typing.List[ProjectJob],
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            ListProjectJobsReply, cmd, success, message, jobs=jobs
        )


@Message.define("command/project-job/initiate")
class InitiateProjectJobCommand(Command):
    """
    Command to initiate a project job.

    Args:
        project_id: The project ID.
        connector_instance: The connector instance ID.
        auto_exports: List of enabled exporters for automatic file generation.

    Notes:
        Requires a ``InitiateJobReply`` reply.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    auto_exports: typing.List[ProjectExporterID] = field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        connector_instance: ConnectorInstanceID,
        auto_exports: typing.List[ProjectExporterID] | None = None,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            InitiateProjectJobCommand,
            chain,
            project_id=project_id,
            connector_instance=connector_instance,
            auto_exports=auto_exports if auto_exports is not None else [],
        )


@Message.define("command/project-job/initiate/reply")
class InitiateProjectJobReply(CommandReply):
    """
    Reply to ``InitiateProjectJobCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: InitiateProjectJobCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            InitiateProjectJobReply, cmd, success, message
        )


@Message.define("command/project-job/start")
class StartProjectJobCommand(Command):
    """
    Command to start a project job in the target connector.

    Args:
        project: The project to upload.
        connector_instance: The connector instance ID.
        user_token: The user token.
        broker_token: Token to create the resources broker.

    Notes:
        Requires a ``StartProjectJobReply`` reply.
    """

    project: Project
    connector_instance: ConnectorInstanceID

    user_token: UserToken
    broker_token: ResourcesBrokerToken

    @property
    def additional_files(self) -> typing.Dict[str, bytes]:
        """
        Any additional (auto-generated) files to be uploaded.

        Returns:
            A dictionary mapping file names to their data.
        """
        return (
            self.payload.get("additional_files")
            if "additional_files" in self.payload
            else {}
        )

    @additional_files.setter
    def additional_files(self, files: typing.Dict[str, bytes]) -> None:
        """
        Sets additional files to upload alongside the project files.

        Args:
            files: A filename->data map containing the additional files.
        """
        self.payload.set("additional_files", files)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project: Project,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
        broker_token: ResourcesBrokerToken,
        additional_files: typing.Dict[str, bytes] | None = None,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        composer = message_builder.build_command(
            StartProjectJobCommand,
            chain,
            project=project,
            connector_instance=connector_instance,
            user_token=user_token,
            broker_token=broker_token,
        )
        if additional_files is not None:
            composer.add_payload("additional_files", additional_files)
        return composer


@Message.define("command/project-job/start/reply")
class StartProjectJobReply(CommandReply):
    """
    Reply to ``StartProjectJobCommand``.

    Args:
        project_id: The project ID.
        connector_instance: The connector instance ID.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: StartProjectJobCommand,
        *,
        project_id: ProjectID,
        connector_instance: ConnectorInstanceID,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            StartProjectJobReply,
            cmd,
            success,
            message,
            project_id=project_id,
            connector_instance=connector_instance,
        )
