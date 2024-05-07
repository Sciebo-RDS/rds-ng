import dataclasses
import typing
from enum import StrEnum

from ...core.messaging import (
    Message,
    Event,
)
from ...core.messaging.composers import (
    MessageBuilder,
    EventComposer,
)
from ...data.entities.connector import ConnectorInstanceID
from ...data.entities.project import ProjectJob, ProjectID


@Message.define("event/project-job/list")
class ProjectJobsListEvent(Event):
    """
    Emitted whenever the user's project jobs list has been updated.

    Args:
        jobs: List of all project jobs.
    """

    jobs: typing.List[ProjectJob] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        jobs: typing.List[ProjectJob],
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(ProjectJobsListEvent, chain, jobs=jobs)


@Message.define("event/project-job/progress")
class ProjectJobProgressEvent(Event):
    """
    Emitted to inform about the progression of a job.

    Args:
        project_id: The project ID.
        connector_instance: The connector instance ID.
        progress: The total progress (0.0 - 1.0).
        message: The current activity message.
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    progress: float
    message: str

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        connector_instance: ConnectorInstanceID,
        progress: float,
        message: str,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectJobProgressEvent,
            chain,
            project_id=project_id,
            connector_instance=connector_instance,
            progress=progress,
            message=message,
        )


@Message.define("event/project-job/completion")
class ProjectJobCompletionEvent(Event):
    """
    Emitted to inform about the completion (either succeeded or failed) of a job.

    Args:
        project_id: The project ID.
        connector_instance: The connector instance ID.
        success: The success status (done or failed).
        message: An optional message (usually in case of an error).
    """

    project_id: ProjectID
    connector_instance: ConnectorInstanceID

    success: bool
    message: str

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        connector_instance: ConnectorInstanceID,
        success: bool,
        message: str = "",
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectJobCompletionEvent,
            chain,
            project_id=project_id,
            connector_instance=connector_instance,
            success=success,
            message=message,
        )
