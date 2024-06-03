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
from ...data.entities.user import User, UserToken


@Message.define("command/user/authenticate")
class AuthenticateUserCommand(Command):
    """
    Command to authenticate a user. Note that the actual login/authentication is performed by the underlying host system.

    Args:
        user_token: The user token.

    Notes:
        Requires a ``AuthenticateUserReply`` reply.
    """

    user_token: UserToken = dataclasses.field(default_factory=UserToken)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        user_token: UserToken,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            AuthenticateUserCommand, chain, user_token=user_token
        )


@Message.define("command/user/authenticate/reply")
class AuthenticateUserReply(CommandReply):
    """
    Reply to ``AuthenticateUserCommand``.

    Args:
        is_authorized: Whether the user is authorized in his host system.
    """

    is_authorized: bool

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: AuthenticateUserCommand,
        *,
        is_authorized: bool,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            AuthenticateUserReply,
            cmd,
            success,
            message,
            is_authorized=is_authorized,
        )


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

    settings: User.Settings = dataclasses.field(default_factory=User.Settings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetUserSettingsCommand,
        *,
        settings: User.Settings,
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

    settings: User.Settings = dataclasses.field(default_factory=User.Settings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        settings: User.Settings,
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

    settings: User.Settings = dataclasses.field(default_factory=User.Settings)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: SetUserSettingsCommand,
        *,
        settings: User.Settings,
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
