from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMapping
from ..meta import CommandReplyMetaInformation
from ...service import ServiceContextType


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    """
    Message dispatcher specific to :class:`CommandReply`.
    """
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
        
    def pre_dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation) -> None:
        """
        Invokes reply callbacks associated with the replied command.

        Args:
            reply: The command reply that is about to be dispatched.
            reply_meta: The command reply meta information.
        """
        super().pre_dispatch(reply, reply_meta)
        
        from .command_dispatcher import CommandDispatcher
        CommandDispatcher.invoke_reply_callback(reply.unique, reply=reply)
        MessageDispatcher._meta_information_list.remove(reply.unique)
    
    def dispatch(self, reply: CommandReply, reply_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        """
        Dispatches a message to locally registered message handlers.

        Handlers can be either called synchronously or asynchronously, depending on how the handler was registered.

        Notes:
            Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.

        Args:
            reply: The message to be dispatched.
            reply_meta: The message meta information.
            handler: The handler to be invoked.
            ctx: The service context.

        Raises:
            RuntimeError: If the handler requires a different message type.
        """
        ctx.logger.debug(f"Dispatching command reply: {reply}", scope="bus")
        super().dispatch(reply, reply_meta, handler, ctx)
