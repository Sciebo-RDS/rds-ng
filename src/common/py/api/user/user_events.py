import dataclasses

from ...core.messaging import (
    Message,
    Event,
)
from ...core.messaging.composers import (
    MessageBuilder,
    EventComposer,
)
from ...data.entities.user import UserConfiguration


@Message.define("event/user/configuration")
class UserConfigurationEvent(Event):
    """
    Emitted whenever the user configuration has changed.

    Args:
        configuration: The user configuration.
    """

    configuration: UserConfiguration = dataclasses.field(
        default_factory=UserConfiguration
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        configuration: UserConfiguration,
        chain: Message | None = None
    ) -> EventComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_event(
            UserConfigurationEvent, chain, configuration=configuration
        )
