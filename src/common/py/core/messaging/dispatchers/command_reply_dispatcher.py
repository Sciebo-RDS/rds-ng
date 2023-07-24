from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..handlers import MessageHandlerMapping, MessageContextType
from ..meta import CommandReplyMetaInformation


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    """
    Message dispatcher specific to ``CommandReply``.
    """
    def __init__(self):
        super().__init__(CommandReplyMetaInformation)
        
    def pre_dispatch(self, msg: CommandReply, msg_meta: CommandReplyMetaInformation) -> None:
        """
        Invokes reply callbacks associated with the replied command.

        Args:
            msg: The command reply that is about to be dispatched.
            msg_meta: The command reply meta information.
        """
        super().pre_dispatch(msg, msg_meta)
        
        from .command_dispatcher import CommandDispatcher
        CommandDispatcher.invoke_reply_callback(msg.unique, reply=msg)
        MessageDispatcher._meta_information_list.remove(msg.unique)
    
    def dispatch(self, msg: CommandReply, msg_meta: CommandReplyMetaInformation, handler: MessageHandlerMapping, ctx: MessageContextType) -> None:
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
        ctx.logger.debug(f"Dispatching command reply: {msg}", scope="bus")
        super().dispatch(msg, msg_meta, handler, ctx)
