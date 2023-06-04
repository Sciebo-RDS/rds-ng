import sys
import threading
import typing

from .message import Message
from .message_name import MessageName
from .handlers import MessageHandlerMappings
from ..networking.network_engine import NetworkEngine
from ...service import Service


class MessageBus:
    """ A thread-safe message bus for dispatching messages. """
    def __init__(self, nwe: NetworkEngine, *, print_tracebacks: bool = False):
        from .dispatchers import MessageDispatcher, CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._network_engine = nwe
        self._print_tracebacks = print_tracebacks
        
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
                    handlers = self._assemble_handlers(msg.name)
                    if len(handlers) > 0:
                        dispatcher.dispatch(typing.cast(msg_type, msg), handlers)
                except Exception as e:
                    import traceback
                    from ..logging import error
                    kwargs = {"message": str(msg), "exception": repr(e)}
                    if self._print_tracebacks:
                        kwargs["traceback"] = traceback.format_exc()
                    error("An exception occurred while processing a message", scope="bus", **kwargs)
                finally:
                    break
        else:
            raise RuntimeError(f"The message type '{type(msg)}' is unknown")

    def _assemble_handlers(self, msg_name: MessageName) -> MessageHandlerMappings:
        with self._lock:
            return [handler for svc in self._services for handler in svc.message_handlers(msg_name)]
