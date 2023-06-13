import typing

from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMapping
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    def dispatch(self, reply: CommandReply, handler: MessageHandlerMapping, ctx: typing.Generic[ServiceContextType]) -> None:
        print("RECV COMMAND REPLY")
        super().dispatch(reply, handler, ctx)
