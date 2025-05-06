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
from ...data.entities.connector import ConnectorInstanceID
from ...data.entities.project import Project, ProjectExternalState, ProjectID
from ...data.entities.user import UserID, UserToken


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


@Message.define("event/project/touch")
class ProjectTouchEvent(Event):
    """
    Emitted whenever a project has been "touched" (i.e., selected/activated) by the user.

    Args:
        project_id: The project ID.
    """

    project_id: ProjectID

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectExternalStateRenewalEvent,
            chain,
            project_id=project_id,
        )


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


@Message.define("event/project/external-state")
class ProjectExternalStateEvent(Event):
    """
    Emitted whenever the external state of a project has been updated.

    Args:
        project_id: The project ID.
        user_id: The user ID.
        connector_instance: The connector instance ID.
        external_state: The new project's external state.
    """

    project_id: ProjectID
    user_id: UserID
    connector_instance: ConnectorInstanceID

    external_state: ProjectExternalState

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_id: ProjectID,
        user_id: UserID,
        connector_instance: ConnectorInstanceID,
        external_state: ProjectExternalState,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectExternalStateEvent,
            chain,
            project_id=project_id,
            user_id=user_id,
            connector_instance=connector_instance,
            external_state=external_state,
        )


@Message.define("event/project/external-state/renewal")
class ProjectExternalStateRenewalEvent(Event):
    """
    Emitted whenever the external state of a project needs to be updated.
    Unlike `ProjectExternalStateEvent`, the entire project needs to be sent with this request, as more than the project ID will be needed.

    Args:
        project: The project.
        connector_instance: The connector instance ID.
        user_token: The user token.
    """

    project: Project
    connector_instance: ConnectorInstanceID

    user_token: UserToken

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project: Project,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            ProjectExternalStateRenewalEvent,
            chain,
            project=project,
            connector_instance=connector_instance,
            user_token=user_token,
        )
