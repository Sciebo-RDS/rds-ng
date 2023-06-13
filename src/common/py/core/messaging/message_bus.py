import threading
import typing

from .dispatchers import MessageDispatcher
from .message import Message, MessageType
from .message_bus_protocol import MessageBusProtocol
from ..config import Configuration
from ..logging import LoggerProxy, default_logger, error
from ..networking.network_engine import NetworkEngine
from ..service import Service, ServiceContextType


class MessageBus(MessageBusProtocol):
    """ A thread-safe message bus for dispatching messages. """
    def __init__(self, nwe: NetworkEngine, config: Configuration, *, print_tracebacks: bool = False):
        from .dispatchers import CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._network_engine = nwe
        self._config = config
        self._print_tracebacks = print_tracebacks
        
        self._services: typing.List[Service] = []
        self._dispatchers: typing.Dict[typing.Type[MessageType], MessageDispatcher] = {
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
            if not isinstance(msg, msg_type):
                continue
                
            processed_msg = dispatcher.preprocess_message(msg)
            
            # TODO: Check target and compare to "self"; send to dispatchers only if this matches, send through NWE otherwise
            for svc in self._services:
                self._dispatch_to_service(dispatcher, processed_msg, msg_type, svc)

    def _dispatch_to_service(self, dispatcher: MessageDispatcher, msg: Message, msg_type: typing.Type[MessageType], svc: Service) -> None:
        for handler in svc.message_handlers(msg.name):
            try:
                act_msg = typing.cast(msg_type, msg)
                ctx = self._create_context(msg, svc)
                dispatcher.dispatch(act_msg, handler, ctx)
            except Exception as e:
                import traceback
                kwargs = {"message": str(msg), "exception": repr(e)}
                if self._print_tracebacks:
                    kwargs["traceback"] = traceback.format_exc()
                error("An exception occurred while processing a message", scope="bus", **kwargs)

    def _create_context(self, msg: Message, svc: Service) -> ServiceContextType:
        logger_proxy = LoggerProxy(default_logger())
        logger_proxy.add_param("trace", str(msg.trace))
        return svc.create_context(self._config, logger_proxy)
