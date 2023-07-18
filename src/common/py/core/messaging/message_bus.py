import threading
import typing

from .dispatchers import MessageDispatcher
from .message import Message, MessageType
from .message_router import MessageRouter
from .meta import MessageMetaInformationType
from .networking import NetworkEngine
from ..logging import LoggerProxy, default_logger, error, debug
from ..service import Service, ServiceContextType
from ...component import ComponentData


class MessageBus:
    """
    Bus for dispatching messages.
    
    The message bus is probably the most central aspect of the system as a whole. It not only invokes local message handlers (which are basically callback functions),
    it also sends messages across the network to other components if necessary. The message bus on the remote side will then decide what to do with the incoming message:
    Dispatch it locally there, send it to yet another component, or just ignore it.
    
    Message handlers are always registered through a :class:`Service`. When a message gets dispatched locally by the bus, it will call any handlers associated with the
    message (via its name). If a message needs to be sent to another component, the bus will invoke the :class:`NetworkEngine` to do so.
    
    To be error tolerant, any exceptions that arise during message handling will be logged but won't result in program termination.
    
    Args:
        comp_data: The global component data.
    
    Notes:
        The message bus is thread-safe.
    """
    
    """ A thread-safe message bus for dispatching messages. """
    def __init__(self, comp_data: ComponentData):
        from .dispatchers import CommandDispatcher, CommandReplyDispatcher, EventDispatcher
        from .command import Command
        from .command_reply import CommandReply
        from .event import Event
        
        self._comp_data = comp_data
        
        debug("-- Creating network engine", scope="bus")
        self._network_engine = self._create_network_engine()
        
        self._services: typing.List[Service] = []
        self._dispatchers: typing.Dict[type[MessageType], MessageDispatcher] = {
            Command: CommandDispatcher(),
            CommandReply: CommandReplyDispatcher(),
            Event: EventDispatcher(),
        }
        self._router = MessageRouter(comp_data.comp_id)
        
        self._lock = threading.Lock()
        
    def _create_network_engine(self) -> NetworkEngine:
        return NetworkEngine(self._comp_data, self)
        
    def add_service(self, svc: Service) -> bool:
        """
        Adds a new service to the bus.
        
        Args:
            svc: The service to add.

        Returns:
            Whether the service was added.
        """
        with self._lock:
            if svc in self._services:
                return False
            
            self._services.append(svc)
            return True
    
    def remove_service(self, svc: Service) -> bool:
        """
        Removes a service from the bus.
        
        Args:
            svc: The service to remove.

        Returns:
            Whether the service was removed.
        """
        with self._lock:
            if svc not in self._services:
                return False
            
            self._services.remove(svc)
            return True
        
    def run(self) -> None:
        """
        Initiates periodic tasks performed by the bus.
        """
        self._network_engine.run()
        self._process()
        
    def dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None:
        """
        Dispatches a message.
        
        To do so, the message is first checked for validity (whether it actually `may` be dispatched). If it is valid,
        the :class:`MessageRouter` will determine if it needs to be dispatched to another component or locally (or both).
        
        Args:
            msg: The message to be dispatched.
            msg_meta: The message meta information.
        """
        try:
            self._router.verify_message(msg, msg_meta)
        except MessageRouter.RoutingError as e:
            error(f"A routing error occurred: {str(e)}", scope="bus", message=str(msg))
        else:
            if self._router.check_remote_routing(msg, msg_meta):
                self._remote_dispatch(msg, msg_meta)
            
            # The local dispatchers are always invoked for their pre- and post-steps
            self._local_dispatch(msg, msg_meta)
    
    def _process(self) -> None:
        for _, dispatcher in self._dispatchers.items():
            dispatcher.process()
        
        threading.Timer(1.0, self._process).start()
        
    def _local_dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None:
        local_routing = self._router.check_local_routing(msg, msg_meta)
        for msg_type, dispatcher in self._dispatchers.items():
            if not isinstance(msg, msg_type):
                continue
            
            dispatcher.pre_dispatch(msg, msg_meta)
            if local_routing:
                for svc in self._services:
                    self._dispatch_to_service(dispatcher, msg, msg_type, msg_meta, svc)
            dispatcher.post_dispatch(msg, msg_meta)
        
    def _remote_dispatch(self, msg: Message, msg_meta: MessageMetaInformationType) -> None:
        self._network_engine.send_message(msg, msg_meta)

    def _dispatch_to_service(self, dispatcher: MessageDispatcher, msg: Message, msg_type: type[MessageType], msg_meta: MessageMetaInformationType, svc: Service) -> None:
        for handler in svc.message_handlers(msg.name):
            try:
                act_msg = typing.cast(msg_type, msg)
                ctx = self._create_context(msg, svc)
                dispatcher.dispatch(act_msg, msg_meta, handler, ctx)
            except Exception as e:
                import traceback
                error(f"An exception occurred while processing a message: {str(e)}", scope="bus", message=str(msg), exception=type(e))
                debug(f"Traceback:\n{''.join(traceback.format_exc())}", scope="bus")

    def _create_context(self, msg: Message, svc: Service) -> ServiceContextType:
        logger_proxy = LoggerProxy(default_logger())
        logger_proxy.add_param("trace", str(msg.trace))
        return svc.create_context(self._comp_data.config, logger_proxy)

    @property
    def network(self) -> NetworkEngine:
        """
        The network engine instance.
        """
        return self._network_engine
