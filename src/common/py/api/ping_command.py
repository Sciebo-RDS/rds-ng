from ..core.messaging import Command, CommandReply, Message


@Message.define("command/general/ping")
class PingCommand(Command):
    """
    A generic PING command.

    Notes:
        Requires a ``PingReply`` reply.
    """

    payload: str = "PING"


@Message.define("command/general/ping/reply")
class PingReply(CommandReply):
    """
    Reply to the ``PingCommand``.
    """

    payload: str = "PONG"
