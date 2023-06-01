from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__()

    def dispatch(self, reply: CommandReply):
        raise RuntimeError("Too lazy to reply")
