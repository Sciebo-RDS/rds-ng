import typing

from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..handlers import MessageHandlerMapping
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    def dispatch(self, command: Command, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]):
        print("RECV COMMAND")
        super().dispatch(command, handler, ctx)
