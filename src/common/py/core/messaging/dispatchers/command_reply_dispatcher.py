from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMappings


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__()

    def dispatch(self, reply: CommandReply, handlers: MessageHandlerMappings):
        if len(handlers) > 1:
            raise RuntimeError(f"Command replies may only be handled by a single handler; got {len(handlers)} instead")
        
        raise RuntimeError("Too lazy to reply")
