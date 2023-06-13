import typing

from .message_dispatcher import MessageDispatcher
from ..command import Command
from ..command_wrapper import CommandWrapper
from ..handlers import MessageHandlerMapping
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    def preprocess_message(self, command: Command) -> Command:
        # Unpack wrapped commands
        # TODO: Store Meta Object etc.
        if isinstance(command, CommandWrapper):
            command = command.command
        
        return command
    
    def dispatch(self, command: Command, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        print("RECV COMMAND")
        super().dispatch(command, handler, ctx)
