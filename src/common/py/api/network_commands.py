from ..core.messaging import (
    Command,
    CommandReply,
    Message,
    Channel,
    CommandDoneCallback,
    CommandFailCallback,
)
from ..core.messaging.handlers import MessageEmitter


@Message.define("command/general/ping")
class PingCommand(Command):
    """
    A generic PING command.

    Notes:
        Requires a ``PingReply`` reply.
    """

    payload: str = "PING"

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        target: Channel,
        *,
        done_callback: CommandDoneCallback | None = None,
        fail_callback: CommandFailCallback | None = None,
        async_callbacks: bool = False,
        timeout: float = 0.0,
        chain: Message | None = None
    ) -> None:
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_command(
            PingCommand,
            target,
            done_callback=done_callback,
            fail_callback=fail_callback,
            async_callbacks=async_callbacks,
            timeout=timeout,
            chain=chain,
        )


@Message.define("command/general/ping/reply")
class PingReply(CommandReply):
    """
    Reply to the ``PingCommand``.
    """

    payload: str = "PONG"

    @staticmethod
    def emit(
        message_emitter: MessageEmitter,
        cmd: PingCommand,
        success: bool = True,
        message: str = "",
    ):
        """
        Helper function to easily emit this message.
        """
        message_emitter.emit_reply(PingReply, cmd, success=success, message=message)
