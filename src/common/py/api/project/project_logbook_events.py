from ...core.messaging import (
    Message,
    Event,
)
from ...core.messaging.composers import (
    MessageBuilder,
    EventComposer,
)
from ...data.entities.project import Project, ProjectID


@Message.define("event/project/logbook/update")
class ProjectLogbookUpdateEvent(Event):
    """
    Sent whenever the logbook of a project has changed.

    Args:
        project_id: The ID of the updated project.
        logbook: The new logbook contents.
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
            ProjectLogbookUpdateEvent,
            chain,
            project_id=project_id,
            logbook=logbook,
        )
