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
from ...integration.authorization import AuthorizationRequestPayload


@Message.define("command/authorization/request")
class RequestAuthorizationCommand(Command):
    """
    Command to perform an authorization request.

    Notes:
        Requires a ``RequestAuthorizationReply`` reply.

    Args:
        request_payload: The authorization request information.
        strategy: The token strategy (e.g., OAuth2).
        data: The actual token request data.
    """

    request_payload: AuthorizationRequestPayload = field(
        default_factory=AuthorizationRequestPayload
    )
    strategy: str
    data: typing.Dict[str, typing.Any] = field(default_factory=dict)

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        request_payload: AuthorizationRequestPayload,
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
            request_payload=request_payload,
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
        force: If true, the token will be removed immediately; otherwise, it will be marked as invalid only
    """

    user_id: UserID
    auth_id: str

    force: bool

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        user_id: UserID,
        auth_id: str,
        force: bool = True,
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
            force=force,
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


@Message.define("command/authorization/token/get", is_protected=True)
class GetAuthorizationTokenCommand(Command):
    """
    Command to retrieve an authorization token.

    Notes:
        This message is protected and requires an API key. Requires a ``GetAuthorizationTokenReply`` reply.

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
        api_key: str,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            GetAuthorizationTokenCommand,
            chain,
            user_id=user_id,
            auth_id=auth_id,
            api_key=api_key,
        )


@Message.define("command/authorization/token/get/reply", is_protected=True)
class GetAuthorizationTokenReply(CommandReply):
    """
    Reply to ``GetAuthorizationTokenCommand``.

    Notes:
        This message is protected and requires an API key.
    """

    auth_token: AuthorizationToken | None

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetAuthorizationTokenCommand,
        *,
        auth_token: AuthorizationToken | None,
        api_key: str,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetAuthorizationTokenReply,
            cmd,
            success,
            message,
            auth_token=auth_token,
            api_key=api_key,
        )
