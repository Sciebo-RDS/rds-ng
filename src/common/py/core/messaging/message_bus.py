import threading
import typing

from .message import Message
from .message_name import MessageName
from .handlers import MessageHandlersList
from ..networking.network_engine import NetworkEngine
from ...service import Service


class MessageBus:
    """ A thread-safe message bus for dispatching messages. """
    # HINT: Thread-safety bei MO-Queue, Handler-Map-Zugriff; beim Callen selbst nicht
    
    def __init__(self, nwe: NetworkEngine):
        from .dispatchers import MessageDispatcher, CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._network_engine = nwe
        
        self._services: typing.List[Service] = []
        self._dispatchers: typing.Dict[typing.Type, MessageDispatcher] = {
            Command: CommandDispatcher(),
            CommandReply: CommandReplyDispatcher(),
            Event: EventDispatcher(),
        }
        
        self._lock = threading.Lock()
        
    def add_service(self, svc: Service) -> bool:
        with self._lock:
            if svc in self._services:
                return False
            
            self._services.append(svc)
            return True
    
    def remove_service(self, svc: Service) -> bool:
        with self._lock:
            if svc not in self._services:
                return False
            
            self._services.remove(svc)
            return True
        
    def dispatch(self, msg: Message) -> None:
        for msg_type, dispatcher in self._dispatchers.items():
            # TODO: Check target and compare to "self"; send to dispatchers only if this matches, send through NWE otherwise
            if isinstance(msg, msg_type):
                try:
                    # Dispatching should never raise an exception; they are to be handled by the dispatcher
                    dispatcher.dispatch(typing.cast(msg_type, msg), self._assemble_handlers(msg.name))
                except Exception as e:
                    from ..logging import error
                    error("Unhandled exception caught by the message bus", scope="bus", exception=repr(e))
                finally:
                    break
        else:
            raise RuntimeError(f"The message type '{type(msg)}' is unknown")

    def _assemble_handlers(self, msg_name: MessageName) -> MessageHandlersList:
        with self._lock:
            return [handler for svc in self._services for handler in svc.handlers(msg_name)]
