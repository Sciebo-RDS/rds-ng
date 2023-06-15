import typing

from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply, CommandReplyCallback
from ..handlers import MessageHandlerMapping
from ..meta import CommandReplyMetaInformation, CommandMetaInformation
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
        
    def pre_dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation) -> None:
        super().pre_dispatch(reply, reply_meta)
        
        meta_information = MessageDispatcher._meta_information_list.find(reply.command.unique)
        if meta_information is not None and isinstance(meta_information, CommandMetaInformation):
            self._call_reply_callback(reply, typing.cast(CommandMetaInformation, meta_information))

        MessageDispatcher._meta_information_list.remove(reply.command.unique)
    
    def dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching command reply: {reply}", scope="bus")
        super().dispatch(reply, reply_meta, handler, ctx)

    def _call_reply_callback(self, reply: CommandReply, command_meta: CommandMetaInformation) -> None:
        callback: CommandReplyCallback | None = command_meta.done_callback if reply.success else command_meta.fail_callback
        if callback is not None:
            if command_meta.async_callbacks:
                MessageDispatcher._thread_pool.submit(callback, reply)
            else:
                callback(reply)
