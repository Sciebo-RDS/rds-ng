import typing

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


@Message.define("command/session/value/get")
class GetSessionValueCommand(Command):
    """
    Command to get a session value stored on the server.

    Args:
        key: The value key.

    Notes:
        Requires a ``GetSessionValueReply`` reply.
    """

    key: str

    @staticmethod
    def build(
        message_builder: MessageBuilder, *, key: str, chain: Message | None = None
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(GetSessionValueCommand, chain, key=key)


@Message.define("command/session/value/get/reply")
class GetSessionValueReply(CommandReply):
    """
    Reply to ``GetSessionValueCommand``.

    Args:
        value: The value or *None* if no such value was found.
    """

    value: typing.Any

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: GetSessionValueCommand,
        *,
        value: typing.Any,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            GetSessionValueReply,
            cmd,
            success,
            message,
            value=value,
        )


@Message.define("command/session/value/set")
class SetSessionValueCommand(Command):
    """
    Command to store a session value on the server.

    Args:
        key: The value key.
        value: The value to store.

    Notes:
        Requires a ``SetSessionValueReply`` reply.
    """

    key: str
    value: typing.Any

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        *,
        key: str,
        value: typing.Any,
        chain: Message | None = None,
    ) -> CommandComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command(
            SetSessionValueCommand, chain, key=key, value=value
        )


@Message.define("command/session/value/set/reply")
class SetSessionValueReply(CommandReply):
    """
    Reply to ``SetSessionValueCommand``.
    """

    @staticmethod
    def build(
        message_builder: MessageBuilder,
        cmd: SetSessionValueCommand,
        *,
        success: bool = True,
        message: str = "",
    ) -> CommandReplyComposer:
        """
        Helper function to easily build this message.
        """
        return message_builder.build_command_reply(
            SetSessionValueReply,
            cmd,
            success,
            message,
        )
