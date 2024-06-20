import typing
from dataclasses import field

from ...core.messaging import Message, Command, CommandReply
from ...core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)
from ...data.entities.user import UserID
from ...integration.authorization import AuthorizationRequestPayload


@Message.define("command/authorization/request")
class RequestAuthorizationCommand(Command):
    """
    Command to perform an authorization request.

    Notes:
        Requires a ``RequestAuthorizationReply`` reply.

    Args:
        payload: The authorization request information.
        strategy: The token strategy (e.g., OAuth2).
        data: The actual token request data.
    """

    payload: AuthorizationRequestPayload = field(
        default_factory=AuthorizationRequestPayload
    )
    strategy: str
    data: typing.Dict[str, typing.Any] = field(default_factory=dict)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        payload: AuthorizationRequestPayload,
        strategy: str,
        data: typing.Dict[str, typing.Any],
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            RequestAuthorizationCommand,
            chain,
            payload=payload,
            strategy=strategy,
            data=data,
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
