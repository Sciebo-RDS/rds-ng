import threading
import typing

from .dispatchers import MessageDispatcher
from .message import Message, MessageType
from .meta import MessageMetaInformationType
from ..logging import LoggerProxy, default_logger
from ..networking import NetworkEngine
from ..service import Service, ServiceContextType
from ...component import ComponentData


class MessageBus:
    """ A thread-safe message bus for dispatching messages. """
    def __init__(self, comp_data: ComponentData, nwe: NetworkEngine):
        from .dispatchers import CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._comp_data = comp_data
        self._network_engine = nwe
        
        self._services: typing.List[Service] = []
        self._dispatchers: typing.Dict[type[MessageType], MessageDispatcher] = {
            Command: CommandDispatcher(),
            CommandReply: CommandReplyDispatcher(),
            Event: EventDispatcher(),
        }
        self._router = self._comp_data.role.messaging_aspects.create_message_router(self._comp_data.comp_id)
        
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
        
    def run(self) -> None:
        for _, dispatcher in self._dispatchers.items():
            dispatcher.process()
            
        threading.Timer(1.0, self.run).start()
        
    def dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None:
        from .routing import RouterException
        try:
            self._router.verify_message(msg)
        except RouterException as e:
            from ..logging import error
            error(f"A routing mistake occurred: {str(e)}", scope="bus", message=str(msg))
        else:
            if self._router.check_remote_routing(msg):
                self._remote_dispatch(msg)
            
            if self._router.check_local_routing(msg):
                self._local_dispatch(msg, msg_meta)
            
    def _local_dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None:
        for msg_type, dispatcher in self._dispatchers.items():
            if not isinstance(msg, msg_type):
                continue
                
            dispatcher.pre_dispatch(msg, msg_meta)
            for svc in self._services:
                self._dispatch_to_service(dispatcher, msg, msg_type, msg_meta, svc)
            dispatcher.post_dispatch(msg, msg_meta)
        
    def _remote_dispatch(self, msg: Message) -> None:
        self._network_engine.send_message(msg)

    def _dispatch_to_service(self, dispatcher: MessageDispatcher, msg: Message, msg_type: type[MessageType], msg_meta: MessageMetaInformationType, svc: Service) -> None:
        for handler in svc.message_handlers(msg.name):
            try:
                act_msg = typing.cast(msg_type, msg)
                ctx = self._create_context(msg, svc)
                dispatcher.dispatch(act_msg, msg_meta, handler, ctx)
            except Exception as e:
                import traceback
                from ..logging import error, debug
                error(f"An exception occurred while processing a message: {str(e)}", scope="bus", message=str(msg), exception=type(e))
                debug(f"Traceback:\n{''.join(traceback.format_exc())}", scope="bus")

    def _create_context(self, msg: Message, svc: Service) -> ServiceContextType:
        logger_proxy = LoggerProxy(default_logger())
        logger_proxy.add_param("trace", str(msg.trace))
        return svc.create_context(self._comp_data.config, logger_proxy)
