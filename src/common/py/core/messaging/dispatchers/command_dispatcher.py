from .message_dispatcher import MessageDispatcher
from ..command import Command


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__()

    def dispatch(self, command: Command):
        raise RuntimeError("Too lazy to accept commands")
