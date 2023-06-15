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
    
    def __init__(self, meta_information_type: typing.Type[MessageMetaInformationType]):
        self._meta_information_type = meta_information_type
        
    def process(self) -> None:
        pass
    
    def pre_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        if not isinstance(msg_meta, self._meta_information_type):
            raise RuntimeError(f"The meta information for dispatcher {str(self)} is of the wrong type ({type(msg_meta)})")

    @abc.abstractmethod
    def dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        try:
            with ctx(is_async=handler.is_async):  # The service context will not suppress exceptions so that the dispatcher can react to them
                if isinstance(msg, handler.message_type):
                    act_msg = typing.cast(handler.message_type, msg)
                    if handler.is_async:
                        MessageDispatcher._thread_pool.submit(handler.handler, act_msg, ctx)
                    else:
                        handler.handler(act_msg, ctx)
                else:
                    raise RuntimeError(f"Handler {str(handler.handler)} requires messages of type {str(handler.message_type)}, but got {str(type(msg))}")
        except Exception as e:
            self._context_exception(e, msg, msg_meta, ctx)

    def post_dispatch(self, msg: MessageType, msg_meta: MessageMetaInformationType) -> None:
        pass
    
    def _context_exception(self, exc: Exception, msg: MessageType, msg_meta: MessageMetaInformationType, ctx: ServiceContextType) -> None:
        pass
    
    @staticmethod
    @atexit.register
    def terminate() -> None:
        MessageDispatcher._thread_pool.shutdown(True, cancel_futures=True)
