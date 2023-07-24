import abc
import atexit
import typing
from concurrent.futures import ThreadPoolExecutor

from ..handlers import MessageHandlerMapping, MessageContextType
from ..message import MessageType
from ..meta import MessageMetaInformationType, MessageMetaInformationList


class MessageDispatcher(abc.ABC, typing.Generic[MessageType]):
    """
    Base message dispatcher responsible for sending messages to registered handlers.
    
    Dispatching a message (locally) is done by passing the message to one or more registered message handlers within a ``Service``.
    The message dispatcher also performs pre- and post-dispatching tasks and takes care of catching errors raised in a handler.
    """
    _thread_pool = ThreadPoolExecutor()
    _meta_information_list = MessageMetaInformationList()
    
    def __init__(self, meta_information_type: type[MessageMetaInformationType]):
        """
        Args:
            meta_information_type: The required type of the message meta information passed alongside the actual messages.
        """
        self._meta_information_type = meta_information_type
        
    def process(self) -> None:
        """
        Called to perform periodic tasks.
        """
    
    def pre_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        """
        Called to perform tasks *before* sending a message.
        
        This method is called before any service-registered message handler is invoked.
        
        Args:
            msg: The message that is about to be dispatched.
            msg_meta: The message meta information.
        """
        if not isinstance(msg_meta, self._meta_information_type):
            raise RuntimeError(f"The meta information for dispatcher {str(self)} is of the wrong type ({type(msg_meta)})")

    @abc.abstractmethod
    def dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType, handler: MessageHandlerMapping, ctx: MessageContextType) -> None:
        """
        Dispatches a message to locally registered message handlers.
        
        Handlers can be either called synchronously or asynchronously, depending on how the handler was registered.
        
        Notes:
            Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.
            
        Args:
            msg: The message to be dispatched.
            msg_meta: The message meta information.
            handler: The handler to be invoked.
            ctx: The message context.
            
        Raises:
            RuntimeError: If the handler requires a different message type.
        """
        # Callback wrapper for proper exception handling, even when used asynchronously
        def _dispatch(msg: MessageType, msg_meta: MessageMetaInformationType, handler: MessageHandlerMapping, ctx: MessageContextType) -> None:
            try:
                with ctx(requires_reply=msg_meta.requires_reply):  # The service context will not suppress exceptions so that the dispatcher can react to them
                    act_msg = typing.cast(handler.message_type, msg)
                    handler.handler(act_msg, ctx)
            except Exception as exc:
                self._context_exception(exc, msg, msg_meta, ctx)
        
        if isinstance(msg, handler.message_type):
            if handler.is_async:
                MessageDispatcher._thread_pool.submit(_dispatch, msg, msg_meta, handler, ctx)
            else:
                _dispatch(msg, msg_meta, handler, ctx)
        else:
            raise RuntimeError(f"Handler {str(handler.handler)} requires messages of type {str(handler.message_type)}, but got {str(type(msg))}")
        
    def post_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        """
        Called to perform tasks *after* sending a message.

        This method is called after any service-registered message handler have been invoked.

        Args:
            msg: The message that has just been dispatched.
            msg_meta: The message meta information.
        """
        
    def _context_exception(self, exc: Exception, msg: MessageType, msg_meta: MessageMetaInformationType, ctx: MessageContextType) -> None:
        pass
    
    @staticmethod
    @atexit.register
    def _terminate() -> None:
        MessageDispatcher._thread_pool.shutdown(True, cancel_futures=True)
