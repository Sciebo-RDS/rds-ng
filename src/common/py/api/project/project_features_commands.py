import dataclasses
import typing

from common.py.core.messaging import (
    Command,
    CommandReply,
    Message,
)
from common.py.core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)
from common.py.data.entities import (
    ProjectID,
    ProjectOptions,
)
from common.py.data.entities.features import (
    ProjectFeatures,
    ProjectFeatureID,
)


@Message.define("command/project/features/update")
class UpdateProjectFeaturesCommand(Command):
    """
    Command to update the features (data) of a project.

    Args:
        project_id: The ID of the project to update.
        updated_features: List of all features (using their ID) to update.
        features: The new features data.

    Notes:
        Requires an ``UpdateProjectFeaturesReply`` reply.
    """

    project_id: ProjectID

    updated_features: typing.List[ProjectFeatureID] = dataclasses.field(
        default_factory=list
    )
    features: ProjectFeatures = dataclasses.field(default_factory=ProjectFeatures)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        updated_features: typing.List[ProjectFeatureID],
        features: ProjectFeatures,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            UpdateProjectFeaturesCommand,
            chain,
            project_id=project_id,
            updated_features=updated_features,
            features=features,
        )


@Message.define("command/project/features/update/reply")
class UpdateProjectFeaturesReply(CommandReply):
    """
    Reply to ``UpdateProjectFeaturesCommand``.

    Args:
        project_id: The ID of the updated project.
        updated_features: List of all updated features (using their ID).
    """

    project_id: ProjectID

    updated_features: typing.List[ProjectFeatureID] = dataclasses.field(
        default_factory=list
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: UpdateProjectFeaturesCommand,
        *,
        project_id: ProjectID,
        updated_features: typing.List[ProjectFeatureID],
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            UpdateProjectFeaturesReply,
            cmd,
            success,
            message,
            project_id=project_id,
            updated_features=updated_features,
        )
