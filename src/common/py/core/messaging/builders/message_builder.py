import typing

from .command_composer import CommandComposer
from .command_reply_composer import CommandReplyComposer
from .event_composer import EventComposer
from .. import (
    Message,
    MessageType,
    MessageBusProtocol,
    Command,
    CommandType,
    CommandReply,
    CommandReplyType,
    Event,
    EventType,
)
from ....utils import UnitID


class MessageBuilder:
    """
    A helper class to easily build and emit new messages.

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

    def build_command(
        self, cmd_type: type[CommandType], chain: Message | None = None, **kwargs
    ) -> CommandComposer:
        """
        Builds a new command.

        Args:
            cmd_type: The command type (i.e., a subclass of ``Command``).
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional message parameters.

        Returns:
            A message composer to further build and finally emit the message.

        Raises:
            RuntimeError: ``cmd_type`` is not a subclass of ``Command``.
        """
        if not issubclass(cmd_type, Command):
            raise RuntimeError(f"Tried to build a command, but got a {cmd_type}")

        self._counters[CommandType] += 1

        return CommandComposer(
            self._origin_id, self._message_bus, cmd_type, chain, **kwargs
        )

    def build_command_reply(
        self,
        reply_type: type[CommandReplyType],
        command: CommandType,
        success: bool = True,
        message: str = "",
        **kwargs,
    ) -> CommandReplyComposer:
        """
        Builds a new command reply.

        Args:
            reply_type: The command reply type (i.e., a subclass of ``CommandReply``).
            command: The ``Command`` this reply is based on.
            success: Whether the command *succeeded* or not (how this is interpreted depends on the command).
            message: Additional message to include in the reply.
            **kwargs: Additional message parameters.

        Returns:
            A message composer to further build and finally emit the message.

        Raises:
            RuntimeError: ``reply_type`` is not a subclass of ``CommandReply``.
        """
        if not issubclass(reply_type, CommandReply):
            raise RuntimeError(
                f"Tried to build a command reply, but got a {reply_type}"
            )

        self._counters[CommandReplyType] += 1

        return CommandReplyComposer(
            self._origin_id,
            self._message_bus,
            reply_type,
            command,
            success=success,
            message=message,
            unique=command.unique,
            **kwargs,
        )

    def build_event(
        self, event_type: type[Event], chain: Message | None = None, **kwargs
    ) -> EventComposer:
        """
        Builds a new event.

        Args:
            event_type: The event type (i.e., a subclass of ``Event``).
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional message parameters.

        Returns:
            A message composer to further build and finally emit the message.

        Raises:
            RuntimeError: ``event_type`` is not a subclass of ``Event``.
        """
        if not issubclass(event_type, Event):
            raise RuntimeError(f"Tried to build an event, but got a {event_type}")

        self._counters[EventType] += 1

        return EventComposer(
            self._origin_id, self._message_bus, event_type, chain, **kwargs
        )

    def get_message_count(self, msg_type: MessageType) -> int:
        """
        Gets how many messages of specific message types have been created.

        The message builder keeps track of how many messages of the three major types ``Command``, ``CommandReply`` and
        ``Event`` have been created.

        Args:
            msg_type: The message type to get the count of. Must be either ``Command``, ``CommandReply`` or ``Event``.

        Returns:
            The number of messages already built of the specified type.
        """
        return self._counters[msg_type] if msg_type in self._counters else 0
