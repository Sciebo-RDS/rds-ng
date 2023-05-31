import typing

from .message import Message
from .command import Command
from .command_reply import CommandReply
from .event import Event


class MessageBus:
    """ A thread-safe message bus for dispatching messages. """
    
    # HINT: Thread-safety bei MO-Queue, Handler-Map-Zugriff; beim Callen selbst nicht
    
    def __init__(self):
        pass
    
    def dispatch(self, msg: Message) -> None:
        if isinstance(msg, Command):
            self._dispatch_command(typing.cast(Command, msg))
        elif isinstance(msg, CommandReply):
            self._dispatch_command_reply(typing.cast(CommandReply, msg))
        elif isinstance(msg, Event):
            self._dispatch_event(typing.cast(Event, msg))
        else:
            raise RuntimeError(f"The message type '{type(msg)}' is unknown")
        
    def _dispatch_command(self, cmd: Command) -> None:
        pass
    
    def _dispatch_command_reply(self, reply: CommandReply) -> None:
        pass
    
    def _dispatch_event(self, event: Event) -> None:
        print(event)
        pass
    