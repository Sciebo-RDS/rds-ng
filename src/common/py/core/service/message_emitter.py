import typing

from ..messaging import MessageBusProtocol, Message, MessageType, Channel, CommandReplyType, CommandType, EventType, Event, Command, CommandReply, CommandReplyCallback
from ..messaging.meta import MessageMetaInformationType, CommandMetaInformation, CommandReplyMetaInformation, EventMetaInformation
from ...component import ComponentID


class MessageEmitter:
    """ A helper class to create and emit messages; it basically stores senseful defaults for certain values and takes care of chaining and rerouting. """
    def __init__(self, origin_id: ComponentID, message_bus: MessageBusProtocol):
        self._origin_id = origin_id
        self._message_bus = message_bus
        
    def emit_command(self, cmd_type: typing.Type[CommandType], target: Channel, done_callback: CommandReplyCallback | None = None, fail_callback: CommandReplyCallback | None = None, async_callbacks: bool = False, timeout: float = 0.0, chain: Message | None = None, **kwargs) -> MessageType:
        if not issubclass(cmd_type, Command):
            raise RuntimeError(f"Tried to emit a command, but got a {cmd_type}")
        
        meta = CommandMetaInformation(done_callback=done_callback, fail_callback=fail_callback, async_callbacks=async_callbacks, timeout=timeout)
        return self._emit(cmd_type, meta, origin=self._origin_id, target=target, prev_hops=[], chain=chain, **kwargs)
    
    def emit_reply(self, reply_type: typing.Type[CommandReplyType], command: CommandType, *, success: bool = True, message: str = "", **kwargs):
        if not issubclass(reply_type, CommandReply):
            raise RuntimeError(f"Tried to emit a command reply, but got a {reply_type}")
        
        meta = CommandReplyMetaInformation()
        return self._emit(reply_type, meta, origin=self._origin_id, target=Channel.direct(str(command.origin)), prev_hops=[], chain=command, success=success, message=message, command=command, **kwargs)
    
    def emit_event(self, msg_type: typing.Type[EventType], target: Channel, chain: Message | None = None, **kwargs) -> MessageType:
        if not issubclass(msg_type, Event):
            raise RuntimeError(f"Tried to emit an event, but got a {msg_type}")
        
        meta = EventMetaInformation()
        return self._emit(msg_type, meta, origin=self._origin_id, target=target, prev_hops=[], chain=chain, **kwargs)
    
    def _emit(self, msg_type: typing.Type[MessageType], msg_meta: MessageMetaInformationType, *, origin: ComponentID, target: Channel, prev_hops: typing.List[ComponentID], chain: Message | None, **kwargs) -> MessageType:
        msg = self._create_message(msg_type, origin=origin, target=target, prev_hops=prev_hops, chain=chain, **kwargs)
        self._message_bus.dispatch(msg, msg_meta)
        return msg

    def _create_message(self, msg_type: typing.Type[MessageType], *, origin: ComponentID, target: Channel, prev_hops: typing.List[ComponentID], chain: Message | None, **kwargs) -> MessageType:
        if chain is not None:
            kwargs["trace"] = chain.trace
        
        return msg_type(origin=origin, sender=self._origin_id, target=target, hops=[*prev_hops, self._origin_id], **kwargs)
