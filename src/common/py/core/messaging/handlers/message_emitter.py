import typing

from .. import Message, MessageType, MessageBusProtocol, Channel, Command, CommandType, CommandReply, CommandReplyType, CommandDoneCallback,\
    CommandFailCallback, Event, EventType
from ..meta import MessageMetaInformation, MessageMetaInformationType, CommandMetaInformation, CommandReplyMetaInformation, EventMetaInformation
from ....utils import UnitID


class MessageEmitter:
    """
    A helper class to easily create and emit messages.
    
    This class stores a reference to the global message bus and offers methods to easily create new messages and send them through the bus.
    """
    def __init__(self, origin_id: UnitID, message_bus: MessageBusProtocol):
        """
        Args:
            origin_id: The component identifier of the origin of newly created messages.
            message_bus: The global message bus to use.
        """
        self._origin_id = origin_id
        self._message_bus = message_bus
        
        self._counters: typing.Dict[MessageType, int] = {
            CommandType: 0,
            CommandReplyType: 0,
            EventType: 0,
        }
        
    def emit_command(self, cmd_type: type[CommandType], target: Channel, done_callback: CommandDoneCallback | None = None,
                     fail_callback: CommandFailCallback | None = None, async_callbacks: bool = False, timeout: float = 0.0,
                     chain: Message | None = None, **kwargs) -> MessageType:
        """
        Emits a new command.
        
        Args:
            cmd_type: The command type (i.e., a subclass of ``Command``).
            target: The destination of the message.
            done_callback: Callback when a reply for the command was received.
            fail_callback: Callback when no reply for the command was received.
            async_callbacks: Whether to execute the callbacks asynchronously in their own thread.
            timeout: The timeout (in seconds) until a command is deemed *not answered*. Pass ``0`` to disable timeouts.
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional parameters.

        Returns:
            The newly created command.
            
        Raises:
            RuntimeError: ``cmd_type`` is not a subclass of ``Command``.
        """
        if not issubclass(cmd_type, Command):
            raise RuntimeError(f"Tried to emit a command, but got a {cmd_type}")
        
        if timeout > 0.0 and fail_callback is None:
            from ... import logging
            logging.warning(f"Sending a command ({cmd_type}) with a timeout but no fail callback", scope="bus")
        
        self._counters[CommandType] += 1
        
        meta = CommandMetaInformation(entrypoint=MessageMetaInformation.Entrypoint.LOCAL, done_callback=done_callback, fail_callback=fail_callback,
                                      async_callbacks=async_callbacks, timeout=timeout)
        return self._emit(cmd_type, meta, origin=self._origin_id, target=target, prev_hops=[], chain=chain, **kwargs)
    
    def emit_reply(self, reply_type: type[CommandReplyType], command: CommandType, *, success: bool = True, message: str = "",
                   **kwargs) -> MessageType:
        """
        Emits a new command reply.
        
        Most parameters, like the proper target, are extracted from the originating command.

        Args:
            reply_type: The reply type (i.e., a subclass of ``CommandReply``).
            command: The ``Command`` this reply is based on.
            success: Whether the command *succeeded* or not (how this is interpreted depends on the command).
            message: Additional message to include in the reply.
            **kwargs: Additional parameters.

        Returns:
            The newly created command reply.
            
        Raises:
            RuntimeError: ``reply_type`` is not a subclass of ``CommandReply``.
        """
        if not issubclass(reply_type, CommandReply):
            raise RuntimeError(f"Tried to emit a command reply, but got a {reply_type}")
        
        self._counters[CommandReplyType] += 1
        
        meta = CommandReplyMetaInformation(entrypoint=MessageMetaInformation.Entrypoint.LOCAL)
        return self._emit(reply_type, meta, origin=self._origin_id, target=Channel.direct(str(command.origin)), prev_hops=[], chain=command,
                          success=success, message=message, unique=command.unique, **kwargs)
    
    def emit_event(self, event_type: type[EventType], target: Channel, chain: Message | None = None, **kwargs) -> MessageType:
        """
        Emits a new event.

        Args:
            event_type: The event type (i.e., a subclass of ``Event``).
            target: The destination of the message.
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional parameters.

        Returns:
            The newly created event.
            
        Raises:
            RuntimeError: ``event_type`` is not a subclass of ``Event``.
        """
        if not issubclass(event_type, Event):
            raise RuntimeError(f"Tried to emit an event, but got a {event_type}")
        
        self._counters[EventType] += 1
        
        meta = EventMetaInformation(entrypoint=MessageMetaInformation.Entrypoint.LOCAL)
        return self._emit(event_type, meta, origin=self._origin_id, target=target, prev_hops=[], chain=chain, **kwargs)
    
    def get_message_count(self, msg_type: MessageType) -> int:
        """
        Gets how many messages of specific message types have beeen emitted.
        
        The message emitter keeps track of how many messages of the three major types ``Command``, ``CommandReply`` and
        ``Event`` have been emitted.
        
        Args:
            msg_type: The message type to get the count of. Must be either ``Command``, ``CommandReply`` or ``Event``.

        Returns:
            The number of messages already emitted of the specified type.
        """
        return self._counters[msg_type] if msg_type in self._counters else 0
    
    def _emit(self, msg_type: type[MessageType], msg_meta: MessageMetaInformationType, *, origin: UnitID, target: Channel,
              prev_hops: typing.List[UnitID], chain: Message | None, **kwargs) -> MessageType:
        msg = self._create_message(msg_type, origin=origin, target=target, prev_hops=prev_hops, chain=chain, **kwargs)
        self._message_bus.dispatch(msg, msg_meta)
        return msg

    def _create_message(self, msg_type: type[MessageType], *, origin: UnitID, target: Channel, prev_hops: typing.List[UnitID], chain: Message | None,
                        **kwargs) -> MessageType:
        if chain is not None:
            kwargs["trace"] = chain.trace
        
        return msg_type(origin=origin, sender=self._origin_id, target=target, hops=[*prev_hops, self._origin_id], **kwargs)
