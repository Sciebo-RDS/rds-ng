import abc
import atexit
import typing
from concurrent.futures import ThreadPoolExecutor

from ..handlers import MessageHandlerMapping
from ..message import MessageType
from ...service import ServiceContextType


class MessageDispatcher(abc.ABC, typing.Generic[MessageType]):
    """ The dispatcher sends message to registered handlers while also performing additional tasks like context management. """
    _thread_pool = ThreadPoolExecutor()
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def dispatch(self, msg: MessageType, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        with ctx(is_async=handler.is_async):
            if isinstance(msg, handler.message_type):
                act_msg = typing.cast(handler.message_type, msg)
                if handler.is_async:
                    MessageDispatcher._thread_pool.submit(handler.handler, act_msg, ctx)
                else:
                    handler.handler(act_msg, ctx)
            else:
                raise RuntimeError(f"Handler {str(handler.handler)} requires messages of type {str(handler.message_type)}, but got {str(type(msg))}")

    @staticmethod
    @atexit.register
    def terminate() -> None:
        MessageDispatcher._thread_pool.shutdown(True, cancel_futures=True)
