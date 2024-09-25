import dataclasses
import typing

from ...core.messaging import Command, CommandReply, Message
from ...core.messaging.composers import (
    CommandComposer,
    CommandReplyComposer,
    MessageBuilder,
)
from ...data.entities.project import ProjectID
from ...data.entities.project.features import ProjectFeatureID
from ...data.exporters import (
    ProjectExporterDescriptor,
    ProjectExporterID,
    ProjectExporterResult,
)


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


@Message.define("command/project/export")
class ExportProjectCommand(Command):
    """
    Command to export a project.

    Notes:
        Requires an ``ExportProjectReply`` reply.
    """

    project_id: ProjectID

    exporter: ProjectExporterID
    scope: ProjectFeatureID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        exporter: ProjectExporterID,
        scope: ProjectFeatureID,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            ExportProjectCommand,
            chain,
            project_id=project_id,
            exporter=exporter,
            scope=scope,
        )


@Message.define("command/project/export/reply")
class ExportProjectReply(CommandReply):
    """
    Reply to ``ExportProjectCommand``.

    Args:
        mimetype: The MIME type of the export result.
    """

    mimetype: str

    @property
    def data(self) -> bytes | None:
        """
        The data of the export result.

        Returns:
            The binary data of the export result.
        """
        return self.payload.get("data") if "data" in self.payload else None

    @data.setter
    def data(self, data: bytes) -> None:
        """
        Sets the data of the export result.

        Args:
            data: The export result data.
        """
        self.payload.set("data", data)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: ExportProjectCommand,
        *,
        mimetype: str,
        data: bytes,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        composer = message_builder.build_command_reply(
            ExportProjectReply, cmd, success, message, mimetype=mimetype
        )
        composer.add_payload("data", data)
        return composer
