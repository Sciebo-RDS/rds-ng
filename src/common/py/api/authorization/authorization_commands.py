import typing
from dataclasses import field

from ...core.messaging import Message, Command, CommandReply
from ...core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)
from ...data.entities.authorization import AuthorizationToken
from ...data.entities.user import UserID


@Message.define("command/authorization/request")
class RequestAuthorizationCommand(Command):
    """
    Command to perform an authorization request.

    Notes:
        Requires a ``RequestAuthorizationReply`` reply.

    Args:
        auth_id: The ID of this token.
        auth_type: The token type.
        auth_issuer: The entity that requires the authorization.
        auth_bearer: The bearer that will be authorized against.
        strategy: The token strategy (e.g., OAuth2).
        data: The actual token request data.
        fingerprint: The user's fingerprint.
    """

    auth_id: str
    auth_type: AuthorizationToken.TokenType
    auth_issuer: str
    auth_bearer: str

    strategy: str
    data: typing.Dict[str, typing.Any] = field(default_factory=dict)

    fingerprint: str = ""

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        auth_id: str,
        auth_type: str,
        auth_issuer: str,
        auth_bearer: str,
        strategy: str,
        data: typing.Dict[str, typing.Any],
        fingerprint: str,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            RequestAuthorizationCommand,
            chain,
            auth_id=auth_id,
            auth_type=auth_type,
            auth_issuer=auth_issuer,
            auth_bearer=auth_bearer,
            strategy=strategy,
            data=data,
            fingerprint=fingerprint,
        )


@Message.define("command/authorization/request/reply")
class RequestAuthorizationReply(CommandReply):
    """
    Reply to ``RequestAuthorizationCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: RequestAuthorizationCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            RequestAuthorizationReply, cmd, success, message
        )


@Message.define("command/authorization/revoke")
class RevokeAuthorizationCommand(Command):
    """
    Command to revoke an authorization.

    Notes:
        Requires a ``RevokeAuthorizationReply`` reply.

    Args:
        user_id: The user ID.
        auth_id: The ID of the token to revoke.
    """

    user_id: UserID
    auth_id: str

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        user_id: UserID,
        auth_id: str,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            RevokeAuthorizationCommand,
            chain,
            user_id=user_id,
            auth_id=auth_id,
        )


@Message.define("command/authorization/revoke/reply")
class RevokeAuthorizationReply(CommandReply):
    """
    Reply to ``RevokeAuthorizationCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: RevokeAuthorizationCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            RevokeAuthorizationReply, cmd, success, message
        )
