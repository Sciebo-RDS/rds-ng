import typing
from dataclasses import field

from ...core.messaging import Message, Command, CommandReply
from ...core.messaging.composers import (
    MessageBuilder,
    CommandComposer,
    CommandReplyComposer,
)


@Message.define("command/authorization/request")
class RequestAuthorizationCommand(Command):
    """
    Command to perform an authorization request.

    Notes:
        Requires a ``RequestAuthorizationReply`` reply.

    Args:
        auth_id: The id of this token.
        strategy: The token strategy (e.g., OAuth2).
        data: The actual token request data.
        fingerprint: The user's fingerprint.
    """

    auth_id: str

    strategy: str
    data: typing.Dict[str, typing.Any] = field(default_factory=dict)

    fingerprint: str = ""

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        auth_id: str,
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