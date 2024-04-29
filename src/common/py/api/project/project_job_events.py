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
