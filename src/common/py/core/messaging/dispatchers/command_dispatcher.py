from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..handlers import MessageHandlerMappings


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__()

    def dispatch(self, command: Command, handlers: MessageHandlerMappings):
        raise RuntimeError("Too lazy to accept commands")
