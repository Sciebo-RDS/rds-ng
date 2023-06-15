import typing

from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..handlers import MessageHandlerMapping
from ..meta import CommandMetaInformation
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__(CommandMetaInformation)
        
    def pre_dispatch(self, command: Command, command_meta: CommandMetaInformation) -> None:
        super().pre_dispatch(command, command_meta)
        
        MessageDispatcher._meta_information_list.add(command.unique, command_meta, command_meta.timeout)

    def dispatch(self, command: Command, command_meta: CommandMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching command: {command}", scope="bus")
        super().dispatch(command, command_meta, handler, ctx)
