import typing

from .message_dispatcher import MessageDispatcher
from .. import Trace, CommandReply
from ..command import Command
from ..handlers import MessageHandlerMapping
from ..meta import CommandMetaInformation
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    """
    Message dispatcher specific to :class:`Command`.
    """
    def __init__(self):
        super().__init__(CommandMetaInformation)
    
    def process(self) -> None:
        """
        Takes care of checking whether issued commands have already timed out.
        """
        super().process()
        
        for unique in MessageDispatcher._meta_information_list.find_timed_out_entries():
            CommandDispatcher.invoke_reply_callback(unique, fail_type=CommandReply.FailType.TIMEOUT, fail_msg="The command timed out")
            MessageDispatcher._meta_information_list.remove(unique)
            
    def pre_dispatch(self, command: Command, command_meta: CommandMetaInformation) -> None:
        """
        Adds command meta information to a global list so that command replies can be handled properly.
        
        Args:
            command: The command that is about to be dispatched.
            command_meta: The command meta information.
        """
        super().pre_dispatch(command, command_meta)
        
        MessageDispatcher._meta_information_list.add(command.unique, command_meta, command_meta.timeout)

    def dispatch(self, command: Command, command_meta: CommandMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        """
        Dispatches a message to locally registered message handlers.

        Handlers can be either called synchronously or asynchronously, depending on how the handler was registered.

        Notes:
            Exceptions arising within a message handler will not interrupt the running program; instead, such errors will only be logged.

        Args:
            command: The message to be dispatched.
            command_meta: The message meta information.
            handler: The handler to be invoked.
            ctx: The service context.

        Raises:
            RuntimeError: If the handler requires a different message type.
        """
        ctx.logger.debug(f"Dispatching command: {command}", scope="bus")
        super().dispatch(command, command_meta, handler, ctx)

    def _context_exception(self, exc: Exception, command: Command, msg_meta: CommandMetaInformation, ctx: ServiceContextType) -> None:
        CommandDispatcher.invoke_reply_callback(command.unique, fail_type=CommandReply.FailType.EXCEPTION, fail_msg=str(exc))
        MessageDispatcher._meta_information_list.remove(command.unique)

    @staticmethod
    def invoke_reply_callback(unique: Trace, *, reply: CommandReply | None = None, fail_type: CommandReply.FailType = CommandReply.FailType.NONE, fail_msg: str = "") -> None:
        """
        Invokes command reply handlers.
        
        When emitting a command, it is possible to specify reply callbacks that are invoked beside message handlers. This method will call the correct callback
        and take care of intercepting exceptions.
        
        Args:
            unique: The unique trace of the command.
            reply: The received command reply (if any).
            fail_type: The type of the command failure (in case of a timeout or exception).
            fail_msg: The failure message.
        """
        # Callback wrapper for proper exception handling, even when used asynchronously
        def _invoke_reply_callback(cb, *args) -> None:
            try:
                cb(*args)
            except Exception as e:
                import traceback
                from ...logging import error, debug
                error(f"An exception occurred within a command reply callback: {str(e)}", scope="bus", exception=type(e))
                debug(f"Traceback:\n{''.join(traceback.format_exc())}", scope="bus")
                
        meta_information = MessageDispatcher._meta_information_list.find(unique)
        if meta_information is not None and isinstance(meta_information, CommandMetaInformation):
            command_meta = typing.cast(CommandMetaInformation, meta_information)
            
            def _invoke(cb, is_async, *args):
                if cb is not None:
                    if is_async:
                        MessageDispatcher._thread_pool.submit(_invoke_reply_callback, cb, *args)
                    else:
                        _invoke_reply_callback(cb, *args)
            
            if reply is not None:
                _invoke(command_meta.done_callback, command_meta.async_callbacks, reply, reply.success, reply.message)
            else:
                _invoke(command_meta.fail_callback, command_meta.async_callbacks, fail_type, fail_msg)
