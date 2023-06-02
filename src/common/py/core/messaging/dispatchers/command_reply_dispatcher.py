from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlersList


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__()

    def dispatch(self, reply: CommandReply, handlers: MessageHandlersList):
        raise RuntimeError("Too lazy to reply")
