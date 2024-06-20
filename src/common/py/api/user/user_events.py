import dataclasses

from ...core.messaging import (
    Event,
    Message,
)
from ...core.messaging.composers import (
    EventComposer,
    MessageBuilder,
)
from ...data.entities.user import User


@Message.define("event/user/settings/changed")
class UserSettingsChangedEvent(Event):
    """
    Event sent when the user settings have changed on the server side.

    Args:
        settings: The new settings.
    """

    settings: User.Settings = dataclasses.field(default_factory=User.Settings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        settings: User.Settings,
        chain: Message | None = None,
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            UserSettingsChangedEvent, chain, settings=settings
        )
