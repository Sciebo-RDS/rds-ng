import typing

from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMapping
from ..meta import CommandReplyMetaInformation
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
        
    def pre_dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation) -> None:
        super().pre_dispatch(reply, reply_meta)
        
        from common.py.core.messaging.dispatchers import CommandDispatcher
        CommandDispatcher.invoke_reply_callback(reply.command.unique, reply, remove_entry=True)
    
    def dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching command reply: {reply}", scope="bus")
        super().dispatch(reply, reply_meta, handler, ctx)
