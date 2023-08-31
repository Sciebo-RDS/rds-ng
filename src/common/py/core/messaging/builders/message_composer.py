import abc

from .. import (
    Message,
    MessageType,
    MessageBusProtocol,
    Channel,
)
from ..meta import MessageMetaInformation
from ....utils import UnitID


class MessageComposer(abc.ABC):
    """
    A class to collect all information necessary to create and emit a message.
    """

    def __init__(
        self,
        origin_id: UnitID,
        message_bus: MessageBusProtocol,
        msg_type: type[MessageType],
        chain: Message | None = None,
        **kwargs
    ):
        """
        Args:
            origin_id: The component identifier of the origin of newly created messages.
            message_bus: The global message bus to use.
            msg_type: The message type.
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional message parameters.
        """
        if chain is not None:
            kwargs["trace"] = chain.trace

        self._origin_id = origin_id
        self._message_bus = message_bus

        self._msg_type = msg_type
        self._params = kwargs

    def emit(self, target: Channel) -> None:
        """
        Sends the built message through the message bus.

        Args:
            target: The target of the message.
        """
        self._verify()
        self._compose()

        msg_meta = self._create_meta_information()
        msg = self._create_message(target)

        self._message_bus.dispatch(msg, msg_meta)

    def _verify(self) -> None:
        pass

    def _compose(self) -> None:
        pass

    @abc.abstractmethod
    def _create_meta_information(self) -> MessageMetaInformation:
        ...

    def _create_message(self, target: Channel) -> MessageType:
        return self._msg_type(
            origin=self._origin_id,
            sender=self._origin_id,
            target=target,
            hops=[self._origin_id],
            **self._params,
        )
