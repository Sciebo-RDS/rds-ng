import typing

from .message_dispatcher import MessageDispatcher
from .. import Trace
from ..command_reply import CommandReply, CommandReplyCallback
from ..handlers import MessageHandlerMapping
from ..meta import CommandReplyMetaInformation, CommandMetaInformation
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
        
    def process(self) -> None:
        super().process()
        
        for unique in MessageDispatcher._meta_information_list.find_timed_out_entries():
            self._invoke_reply_callback(unique, None)
        
    def pre_dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation) -> None:
        super().pre_dispatch(reply, reply_meta)
        
        self._invoke_reply_callback(reply.command.unique, reply)
    
    def dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching command reply: {reply}", scope="bus")
        super().dispatch(reply, reply_meta, handler, ctx)
        
    def _invoke_reply_callback(self, unique: Trace, reply: CommandReply | None) -> None:
        meta_information = MessageDispatcher._meta_information_list.find(unique)
        if meta_information is not None and isinstance(meta_information, CommandMetaInformation):
            command_meta = typing.cast(CommandMetaInformation, meta_information)
            callback: CommandReplyCallback | None = command_meta.done_callback if reply is not None and reply.success else command_meta.fail_callback
            if callback is not None:
                if command_meta.async_callbacks:
                    MessageDispatcher._thread_pool.submit(callback, reply)
                else:
                    callback(reply)
        
        MessageDispatcher._meta_information_list.remove(unique)
