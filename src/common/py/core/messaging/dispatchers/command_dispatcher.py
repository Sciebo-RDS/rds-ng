import typing

from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..handlers import MessageHandlerMapping
from ..meta import CommandMetaInformation
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__(CommandMetaInformation)

    def dispatch(self, command: Command, command_meta: CommandMetaInformation, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        print("RECV COMMAND", command_meta)
        super().dispatch(command, command_meta, handler, ctx)
