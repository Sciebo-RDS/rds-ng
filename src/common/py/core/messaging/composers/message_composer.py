import abc
import typing

from .. import (
    Message,
    MessageType,
    MessageBusProtocol,
    Channel,
    Payload,
    PayloadData,
)
from ..meta import MessageMetaInformation
from ....utils import UnitID

BeforeDispatchCallback = typing.Callable[[Message, MessageMetaInformation], None]


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
        self._payload: Payload = {}

        self._before_callbacks: typing.List[BeforeDispatchCallback] = []

    def add_payload(self, key: str, data: PayloadData) -> None:
        """
        Adds a payload item to the message.

        Args:
            key: The item key.
            data: The item data.
        """
        self._payload[key] = data

    def before(self, callback: BeforeDispatchCallback) -> typing.Self:
        """
        Adds a callback that will be called immediately before the message is dispatched.

        Args:
            callback: The callback to add.

        Returns:
            This composer instance to allow call chaining.
        """
        self._before_callbacks.append(callback)
        return self

    def emit(self, target: Channel, *, suppress_logging: bool = False) -> None:
        """
        Sends the built message through the message bus.

        Args:
            target: The target of the message.
            suppress_logging: Suppresses debug logging.
        """
        self._verify()
        self._compose()

        msg_meta = self._create_meta_information(suppress_logging)
        msg = self._create_message(target)

        for callback in self._before_callbacks:
            callback(msg, msg_meta)

        self._message_bus.dispatch(msg, msg_meta)

    def _verify(self) -> None:
        pass

    def _compose(self) -> None:
        pass

    @abc.abstractmethod
    def _create_meta_information(
        self, suppress_logging: bool
    ) -> MessageMetaInformation: ...

    def _create_message(self, target: Channel) -> MessageType:
        msg = typing.cast(
            Message,
            self._msg_type(
                origin=self._origin_id,
                sender=self._origin_id,
                target=target,
                hops=[self._origin_id],
                **self._params,
            ),
        )
        msg.payload.decode(self._payload)
        return typing.cast(MessageType, msg)
