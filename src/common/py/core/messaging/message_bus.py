import typing

from ..networking.network_engine import NetworkEngine
from .message import Message


class MessageBus:
    """ A thread-safe message bus for dispatching messages. """
    # HINT: Thread-safety bei MO-Queue, Handler-Map-Zugriff; beim Callen selbst nicht
    
    def __init__(self, nwe: NetworkEngine):
        from .dispatchers import MessageDispatcher, CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._network_engine = nwe
        
        self._dispatchers: typing.Dict[typing.Type, MessageDispatcher] = {
            Command: CommandDispatcher(),
            CommandReply: CommandReplyDispatcher(),
            Event: EventDispatcher(),
        }
    
    def dispatch(self, msg: Message) -> None:
        for msg_type, dispatcher in self._dispatchers.items():
            if isinstance(msg, msg_type):
                try:
                    # Dispatching should never raise an exception; these are to be handled by the dispatcher
                    dispatcher.dispatch(typing.cast(msg_type, msg))
                except Exception as e:
                    from ..logging import error
                    error("Unhandled exception caught by the message bus", scope="bus", exception=repr(e))
                finally:
                    break
        else:
            raise RuntimeError(f"The message type '{type(msg)}' is unknown")
