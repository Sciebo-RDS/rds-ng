import dataclasses
import typing

from ...core.messaging import (
    Event,
    Message,
)
from ...core.messaging.composers import (
    EventComposer,
    MessageBuilder,
)


@Message.define("event/user/authorization/list")
class UserAuthorizationsListEvent(Event):
    """
    Event sent when the user authorizations have changed.

    Args:
        authorizations: The new list of all granted authorizations.
    """

    authorizations: typing.List[str] = dataclasses.field(default_factory=list)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        authorizations: typing.List[str],
        chain: Message | None = None,
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            UserAuthorizationsListEvent,
            chain,
            authorizations=authorizations,
        )
