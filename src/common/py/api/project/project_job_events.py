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
from ...data.entities.project import ProjectJob


@Message.define("event/job/list")
class JobsListEvent(Event):
    """
    Emitted whenever the user's project jobs list has been updated.

    Args:
        project_jobs: List of all project jobs.
    """

    project_jobs: typing.List[ProjectJob] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        project_jobs: typing.List[ProjectJob],
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            JobsListEvent, chain, project_jobs=project_jobs
        )
