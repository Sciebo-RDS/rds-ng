import dataclasses
import typing

from .client import Client
from .network_router import NetworkRouter
from .server import Server
from .. import Message, MessageBusProtocol, MessageType, Command, CommandReply, Event
from ..meta import (
    MessageMetaInformation,
    MessageMetaInformationType,
    CommandMetaInformation,
    CommandReplyMetaInformation,
    EventMetaInformation,
)
from ....component import BackendComponentData
from ....utils import UnitID


class NetworkEngine:
    """
    Main network management class.

    Messages go out to other components through this class, and new messages come in from the outside world here as well.
    The network engine takes care of listening to incoming messages, routing them properly, and sending new messages to other components.
    """

    def __init__(
        self, comp_data: BackendComponentData, message_bus: MessageBusProtocol
    ):
        """
        Args:
            comp_data: The global component data.
            message_bus: The global message bus.
        """
        self._comp_data = comp_data

        self._message_bus = message_bus

        self._client = (
            self._create_client()
            if self._comp_data.role.networking_aspects.has_client
            else None
        )
        self._server = (
            self._create_server()
            if self._comp_data.role.networking_aspects.has_server
            else None
        )
        self._meta_information_types: typing.Dict[
            type[MessageType], type[MessageMetaInformationType]
        ] = {
            Command: CommandMetaInformation,
            CommandReply: CommandReplyMetaInformation,
            Event: EventMetaInformation,
        }
        self._router = NetworkRouter(
            self._comp_data.comp_id,
            has_client=self.has_client,
            has_server=self.has_server,
        )

    def _create_client(self) -> Client:
        return Client(self._comp_data.comp_id, self._comp_data.config)

    def _create_server(self) -> Server:
        return Server(self._comp_data.comp_id, self._comp_data.config)

    def run(self) -> None:
        """
        Listens to incoming messages in order to properly route them.
        """
        if self.has_server:
            self._server.set_message_handler(
                lambda msg_name, data: self._handle_received_message(
                    MessageMetaInformation.Entrypoint.SERVER, msg_name, data
                )
            )
            self._server.run()

        if self.has_client:
            self._client.set_message_handler(
                lambda msg_name, data: self._handle_received_message(
                    MessageMetaInformation.Entrypoint.CLIENT, msg_name, data
                ),
            )
            self._client.run()

    def process(self) -> None:
        """
        Called to perform periodic tasks.
        """
        if self.has_server:
            self._server.process()

        if self.has_client:
            self._client.process()

    def send_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        """
        Sends a message across the network.

        To do so, the message is first checked for validity (whether it actually *may* be sent). If it is valid, it is routed through the
        client and/or server (the logic of this can be found in ``NetworkRouter``).

        Args:
            msg: The message to be sent.
            msg_meta: The message meta information.
        """
        try:
            self._router.verify_message(NetworkRouter.Direction.OUT, msg)
        except NetworkRouter.RoutingError as exc:
            self._routing_error(str(exc), message=str(msg))
        else:
            self._route_message(
                msg,
                msg_meta,
                NetworkRouter.Direction.OUT,
                skip_components=[self._comp_data.comp_id],
            )

    def _handle_received_message(
        self, entrypoint: MessageMetaInformation.Entrypoint, msg_name: str, data: str
    ) -> None:
        try:
            msg = self._unpack_message(msg_name, data)
            msg_meta = self._create_message_meta_information(msg, entrypoint)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self._routing_error(str(exc), data=data)
        else:
            from ...logging import debug

            debug(
                f"Received message: {msg}", scope="network", entrypoint=entrypoint.name
            )

            if self._router.check_local_routing(
                NetworkRouter.Direction.IN, msg, msg_meta
            ):
                self._message_bus.dispatch(msg, msg_meta)

            # Perform rerouting
            msg = dataclasses.replace(msg, sender=self._comp_data.comp_id)
            self._route_message(
                msg,
                msg_meta,
                NetworkRouter.Direction.IN,
                skip_components=[self._comp_data.comp_id, msg.sender],
            )

    def _unpack_message(self, msg_name: str, data: str) -> Message:
        # Look up the actual message via its name
        from .. import MessageTypesCatalog

        msg_type = MessageTypesCatalog.find_type(msg_name)
        if msg_type is None:
            raise RuntimeError(f"The message type '{msg_name}' is unknown")

        # Unpack the message into its actual type
        msg = typing.cast(Message, msg_type.from_json(data))
        self._router.verify_message(NetworkRouter.Direction.IN, msg)

        msg.hops.append(self._comp_data.comp_id)
        return msg

    def _route_message(
        self,
        msg: Message,
        msg_meta: MessageMetaInformation,
        direction: NetworkRouter.Direction,
        *,
        skip_components: typing.List[UnitID] | None = None,
    ):
        send_to_client = True

        if self._router.check_server_routing(direction, msg, msg_meta):
            send_to_client = (
                self._server.send_message(msg, skip_components=skip_components)
                == Server.SendTarget.SPREAD
            )

        if send_to_client and self._router.check_client_routing(
            direction, msg, msg_meta
        ):
            self._client.send_message(msg)

    def _create_message_meta_information(
        self, msg: Message, entrypoint: MessageMetaInformation.Entrypoint, **kwargs
    ) -> MessageMetaInformation:
        for msg_type, meta_type in self._meta_information_types.items():
            if isinstance(msg, msg_type):
                return meta_type(entrypoint=entrypoint, **kwargs)

        raise RuntimeError("No meta information type associated with message type")

    def _routing_error(self, msg: str, **kwargs) -> None:
        from ...logging import error

        error(f"A routing error occurred: {msg}", scope="network", **kwargs)

    @property
    def has_server(self) -> bool:
        """
        Whether the network runs a server.
        """
        return self._server is not None

    @property
    def server(self) -> Server | None:
        """
        The server instance.
        """
        return self._server

    @property
    def has_client(self) -> bool:
        """
        Whether the network runs a client.
        """
        return self._client is not None

    @property
    def client(self) -> Client | None:
        """
        The client instance.
        """
        return self._client
