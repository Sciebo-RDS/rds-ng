from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..handlers import MessageHandlerMappings


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__()

    def dispatch(self, command: Command, handlers: MessageHandlerMappings):
        if len(handlers) > 1:
            raise RuntimeError(f"Commands may only be handled by a single handler; got {len(handlers)} instead")
        
        raise RuntimeError("Too lazy to accept commands")
