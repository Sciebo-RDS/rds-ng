import typing

from .message_dispatcher import MessageDispatcher
from .. import Trace, CommandReply
from ..command import Command
from ..handlers import MessageContextType
from ..meta import CommandMetaInformation


class CommandDispatcher(MessageDispatcher[Command]):
    # pylint: disable=protected-access
    """
    Message dispatcher specific to ``Command``.
    """

    def __init__(self):
        super().__init__(CommandMetaInformation)

    def process(self) -> None:
        """
        Takes care of checking whether issued commands have already timed out.
        """
        super().process()

        for unique in MessageDispatcher._meta_information_list.find_timed_out_entries():
            CommandDispatcher.invoke_reply_callbacks(
                unique,
                fail_type=CommandReply.FailType.TIMEOUT,
                fail_msg="The command timed out",
            )
            MessageDispatcher._meta_information_list.remove(unique)

    def pre_dispatch(self, msg: Command, msg_meta: CommandMetaInformation) -> None:
        """
        Adds command meta information to a global list so that command replies can be handled properly.

        Args:
            msg: The command that is about to be dispatched.
            msg_meta: The command meta information.
        """
        from ...logging import debug

        debug(f"Dispatching command: {msg}", scope="bus")
        super().pre_dispatch(msg, msg_meta)

        MessageDispatcher._meta_information_list.add(
            msg.unique, msg_meta, msg_meta.timeout
        )

    def _context_exception(
        self,
        exc: Exception,
        msg: Command,
        msg_meta: CommandMetaInformation,
        ctx: MessageContextType,
    ) -> None:
        CommandDispatcher.invoke_reply_callbacks(
            msg.unique, fail_type=CommandReply.FailType.EXCEPTION, fail_msg=str(exc)
        )
        MessageDispatcher._meta_information_list.remove(msg.unique)

    @staticmethod
    def invoke_reply_callbacks(
        unique: Trace,
        *,
        reply: CommandReply | None = None,
        fail_type: CommandReply.FailType = CommandReply.FailType.NONE,
        fail_msg: str = "",
    ) -> None:
        """
        Invokes command reply callbacks.

        When emitting a command, it is possible to specify reply callbacks that are invoked beside message handlers. This method will call the correct
        callback and take care of intercepting exceptions.

        Args:
            unique: The unique trace of the command.
            reply: The received command reply (if any).
            fail_type: The type of the command failure (in case of a timeout or exception).
            fail_msg: The failure message.
        """

        # Callback wrapper for proper exception handling, even when used asynchronously
        def _invoke_reply_callbacks(callbacks, *args) -> None:
            for callback in callbacks:
                try:
                    callback(*args)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    import traceback
                    from ...logging import error, debug

                    error(
                        f"An exception occurred within a command reply callback: {str(exc)}",
                        scope="bus",
                        exception=type(exc),
                    )
                    debug(f"Traceback:\n{''.join(traceback.format_exc())}", scope="bus")

        meta_information = MessageDispatcher._meta_information_list.find(unique)
        if meta_information is not None and isinstance(
            meta_information, CommandMetaInformation
        ):
            command_meta = typing.cast(CommandMetaInformation, meta_information)

            def _invoke(callbacks, is_async, *args):
                if len(callbacks) > 0:
                    if is_async:
                        MessageDispatcher._thread_pool.submit(
                            _invoke_reply_callbacks, callbacks, *args
                        )
                    else:
                        _invoke_reply_callbacks(callbacks, *args)

            if reply is not None:
                _invoke(
                    command_meta.done_callbacks,
                    command_meta.async_callbacks,
                    reply,
                    reply.success,
                    reply.message,
                )
            else:
                _invoke(
                    command_meta.fail_callbacks,
                    command_meta.async_callbacks,
                    fail_type,
                    fail_msg,
                )
