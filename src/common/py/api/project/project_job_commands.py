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
from ...data.entities.project import ProjectID


@Message.define("command/job/initiate")
class InitiateJobCommand(Command):
    """
    Command to initiate a publishing job.

    Args:
        project_id: The project ID.
        connector_instance: The connector instance ID.

    Notes:
        Requires a ``InitiateJobReply`` reply.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        connector_instance: ConnectorInstanceID,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            InitiateJobCommand,
            chain,
            project_id=project_id,
            connector_instance=connector_instance,
        )


@Message.define("command/job/initiate/reply")
class InitiateJobReply(CommandReply):
    """
    Reply to ``InitiateJobCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: InitiateJobCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            InitiateJobReply, cmd, success, message
        )
