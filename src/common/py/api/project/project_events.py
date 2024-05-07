import dataclasses
import typing

from ...core.messaging import (
    Message,
    Event,
)
from ...core.messaging.composers import (
    MessageBuilder,
    EventComposer,
)
from ...data.entities.project import Project, ProjectID


@Message.define("event/project/list")
class ProjectsListEvent(Event):
    """
    Emitted whenever the user's projects list has been updated.

    Args:
        projects: List of all projects.
    """

    projects: typing.List[Project] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        projects: typing.List[Project],
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(ProjectsListEvent, chain, projects=projects)


@Message.define("event/project/logbook")
class ProjectLogbookEvent(Event):
    """
    Emitted whenever the project's logbook has been updated.

    Args:
        project_id: The project ID.
        logbook: The new project logbook.
    """

    project_id: ProjectID

    logbook: Project.Logbook

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        logbook: Project.Logbook,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectLogbookEvent, chain, project_id=project_id, logbook=logbook
        )
