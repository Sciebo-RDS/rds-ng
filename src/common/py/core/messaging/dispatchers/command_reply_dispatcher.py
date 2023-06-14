import typing

from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMapping
from ..meta import CommandReplyMetaInformation, MessageMetaInformationType
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
    
    def dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        print("RECV COMMAND REPLY", reply_meta)
        super().dispatch(reply, reply_meta, handler, ctx)
