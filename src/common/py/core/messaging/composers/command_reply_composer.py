from .message_composer import MessageComposer
from .. import MessageType, MessageBusProtocol, CommandType, Channel
from ..meta import MessageMetaInformation
from ....utils import UnitID


class CommandReplyComposer(MessageComposer):
    """
    Composer for ``CommandReply`` messages.
    """

    def __init__(
        self,
        origin_id: UnitID,
        message_bus: MessageBusProtocol,
        msg_type: type[MessageType],
        command: CommandType,
        **kwargs,
    ):
        """
        Args:
            origin_id: The component identifier of the origin of newly created messages.
            message_bus: The global message bus to use.
            msg_type: The message type.
            command: The ``Command`` this reply is based on.
            **kwargs: Additional message parameters.
        """
        super().__init__(origin_id, message_bus, msg_type, command, **kwargs)

        self._command = command

    def emit(self) -> None:  # pylint: disable=arguments-differ
        """
        Sends the built message through the message bus.
        """
        target = (
            Channel.local()
            if self._command.origin.equals(self._origin_id)
            else Channel.direct(self._command.origin)
        )
        super().emit(target)

    def _create_meta_information(self) -> MessageMetaInformation:
        from ..meta import CommandReplyMetaInformation

        return CommandReplyMetaInformation(
            entrypoint=MessageMetaInformation.Entrypoint.LOCAL
        )
