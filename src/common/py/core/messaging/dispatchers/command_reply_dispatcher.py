from .message_dispatcher import MessageDispatcher
from ..command_reply import CommandReply
from ..meta import CommandReplyMetaInformation


class CommandReplyDispatcher(MessageDispatcher[CommandReply]):
    # pylint: disable=protected-access
    """
    Message dispatcher specific to ``CommandReply``.
    """

    def __init__(self):
        super().__init__(CommandReplyMetaInformation)

    def pre_dispatch(
        self, msg: CommandReply, msg_meta: CommandReplyMetaInformation
    ) -> None:
        """
        Invokes reply callbacks associated with the replied command.

        Args:
            msg: The command reply that is about to be dispatched.
            msg_meta: The command reply meta information.
        """
        from .command_dispatcher import CommandDispatcher
        from ...logging import debug

        debug(f"Dispatching command reply: {msg}", scope="bus")
        super().pre_dispatch(msg, msg_meta)

        CommandDispatcher.invoke_reply_callbacks(msg.unique, reply=msg)
        MessageDispatcher._meta_information_list.remove(msg.unique)
