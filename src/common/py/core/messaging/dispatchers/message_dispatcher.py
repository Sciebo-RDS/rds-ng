import abc
import atexit
import typing
from concurrent.futures import ThreadPoolExecutor

from ..handlers import MessageHandlerMapping
from ..message import MessageType
from ..meta import MessageMetaInformationType, MessageMetaInformationList
from ...service import ServiceContextType


class MessageDispatcher(abc.ABC, typing.Generic[MessageType]):
    """ The dispatcher sends message to registered handlers while also performing additional tasks like context management. """
    _thread_pool = ThreadPoolExecutor()
    _meta_information_list = MessageMetaInformationList()
    
    def __init__(self, meta_information_type: type[MessageMetaInformationType]):
        self._meta_information_type = meta_information_type
        
    def process(self) -> None:
        pass
    
    def pre_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        if not isinstance(msg_meta, self._meta_information_type):
            raise RuntimeError(f"The meta information for dispatcher {str(self)} is of the wrong type ({type(msg_meta)})")

    @abc.abstractmethod
    def dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        # Callback wrapper for proper exception handling, even when used asynchronously
        def _dispatch(msg: MessageType, msg_meta: MessageMetaInformationType, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
            try:
                with ctx(requires_reply=msg_meta.requires_reply):  # The service context will not suppress exceptions so that the dispatcher can react to them
                    act_msg = typing.cast(handler.message_type, msg)
                    handler.handler(act_msg, ctx)
            except Exception as e:
                self._context_exception(e, msg, msg_meta, ctx)
        
        if isinstance(msg, handler.message_type):
            if handler.is_async:
                MessageDispatcher._thread_pool.submit(_dispatch, msg, msg_meta, handler, ctx)
            else:
                _dispatch(msg, msg_meta, handler, ctx)
        else:
            raise RuntimeError(f"Handler {str(handler.handler)} requires messages of type {str(handler.message_type)}, but got {str(type(msg))}")
        
    def post_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        pass
        
    def _context_exception(self, exc: Exception, msg: MessageType, msg_meta: MessageMetaInformationType, ctx: ServiceContextType) -> None:
        pass
    
    @staticmethod
    @atexit.register
    def terminate() -> None:
        MessageDispatcher._thread_pool.shutdown(True, cancel_futures=True)
