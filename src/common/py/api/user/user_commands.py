import dataclasses

from ...core.messaging import (
    Command,
    CommandReply,
    Message,
)
from ...core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)
from ...data.entities.user import UserConfiguration


@Message.define("command/user/configuration/get")
class GetUserConfigurationCommand(Command):
    """
    Command to get the configuration of the current user.

    Notes:
        Requires a ``GetUserConfigurationReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(GetUserConfigurationCommand, chain)


@Message.define("command/user/configuration/get/reply")
class GetUserConfigurationReply(CommandReply):
    """
    Reply to ``GetUserConfigurationCommand``.

    Args:
        configuration: The user configuration.
    """

    configuration: UserConfiguration = dataclasses.field(
        default_factory=UserConfiguration
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetUserConfigurationCommand,
        *,
        configuration: UserConfiguration,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetUserConfigurationReply,
            cmd,
            success,
            message,
            configuration=configuration,
        )


@Message.define("command/user/configuration/set")
class SetUserConfigurationCommand(Command):
    """
    Command to set the configuration of the current user.

    Args:
        configuration: The new user configuration.

    Notes:
        Requires a ``SetUserConfigurationReply`` reply.
    """

    configuration: UserConfiguration = dataclasses.field(
        default_factory=UserConfiguration
    )

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        configuration: UserConfiguration,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            SetUserConfigurationCommand, chain, configuration=configuration
        )


@Message.define("command/user/configuration/set/reply")
class SetUserConfigurationReply(CommandReply):
    """
    Reply to ``SetUserConfigurationCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: SetUserConfigurationCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            SetUserConfigurationReply,
            cmd,
            success,
            message,
        )
