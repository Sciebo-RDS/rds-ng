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
from ...data.entities.user import UserSettings


@Message.define("command/user/settings/get")
class GetUserSettingsCommand(Command):
    """
    Command to get the settings of the current user.

    Notes:
        Requires a ``GetUserSettingsReply`` reply.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(GetUserSettingsCommand, chain)


@Message.define("command/user/settings/get/reply")
class GetUserSettingsReply(CommandReply):
    """
    Reply to ``GetUserSettingsCommand``.

    Args:
        settings: The user settings.
    """

    settings: UserSettings = dataclasses.field(default_factory=UserSettings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetUserSettingsCommand,
        *,
        settings: UserSettings,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetUserSettingsReply,
            cmd,
            success,
            message,
            settings=settings,
        )


@Message.define("command/user/settings/set")
class SetUserSettingsCommand(Command):
    """
    Command to set the settings of the current user.

    Args:
        settings: The new user settings.

    Notes:
        Requires a ``SetUserSettingsReply`` reply.
    """

    settings: UserSettings = dataclasses.field(default_factory=UserSettings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        settings: UserSettings,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            SetUserSettingsCommand, chain, settings=settings
        )


@Message.define("command/user/settings/set/reply")
class SetUserSettingsReply(CommandReply):
    """
    Reply to ``SetUserSettingsCommand``.

    Args:
        settings: The new user settings (note that these might have been adjusted by the server).
    """

    settings: UserSettings = dataclasses.field(default_factory=UserSettings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: SetUserSettingsCommand,
        *,
        settings: UserSettings,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            SetUserSettingsReply,
            cmd,
            success,
            message,
            settings=settings,
        )
