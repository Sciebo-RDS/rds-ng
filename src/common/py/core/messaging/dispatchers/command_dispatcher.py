import typing

from .message_dispatcher import MessageDispatcher
from .. import Trace, CommandReply
from ..command import Command
from ..handlers import MessageHandlerMapping
from ..meta import CommandMetaInformation
from ...service import ServiceContextType


class CommandDispatcher(MessageDispatcher[Command]):
    def __init__(self):
        super().__init__(CommandMetaInformation)
    
    def process(self) -> None:
        super().process()
        
        for unique in MessageDispatcher._meta_information_list.find_timed_out_entries():
            CommandDispatcher.invoke_reply_callback(unique, None, remove_entry=True, error="The command timed out")
            
    def pre_dispatch(self, command: Command, command_meta: CommandMetaInformation) -> None:
        super().pre_dispatch(command, command_meta)
        
        MessageDispatcher._meta_information_list.add(command.unique, command_meta, command_meta.timeout)

    def dispatch(self, command: Command, command_meta: CommandMetaInformation, handler: MessageHandlerMapping, ctx: ServiceContextType) -> None:
        ctx.logger.debug(f"Dispatching command: {command}", scope="bus")
        super().dispatch(command, command_meta, handler, ctx)

    def _context_exception(self, exc: Exception, command: Command, msg_meta: CommandMetaInformation, ctx: ServiceContextType) -> None:
        CommandDispatcher.invoke_reply_callback(command.unique, None, remove_entry=True, error=str(exc))

    @staticmethod
    def invoke_reply_callback(unique: Trace, reply: CommandReply | None, *, remove_entry: bool, error: str | None = None) -> None:
        from .. import CommandReplyCallback
        
        meta_information = MessageDispatcher._meta_information_list.find(unique)
        if meta_information is not None and isinstance(meta_information, CommandMetaInformation):
            command_meta = typing.cast(CommandMetaInformation, meta_information)
            callback: CommandReplyCallback | None = command_meta.done_callback if reply is not None and reply.success else command_meta.fail_callback
            if callback is not None:
                if command_meta.async_callbacks:
                    MessageDispatcher._thread_pool.submit(callback, reply, error)
                else:
                    callback(reply, error)

        if remove_entry:
            MessageDispatcher._meta_information_list.remove(unique)
