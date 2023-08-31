import dataclasses
import threading
import time
import typing
from enum import IntEnum, auto

import socketio

from .. import Message
from ..builders import MessageBuilder
from ...logging import info, warning, debug
from ....utils import UnitID
from ....utils.config import Configuration

ServerMessageHandler = typing.Callable[[str, str], None]


class Server(socketio.Server):
    """
    The server connection, based on ``socketio.Server``.
    """

    class SendTarget(IntEnum):
        """
        Enum telling whether an outgoing message is only sent to a single (direct) target or spread across all connected clients.
        """

        SPREAD = auto()
        DIRECT = auto()

    @dataclasses.dataclass()
    class _ComponentEntry:
        sid: str

        timeout: float = 0.0
        last_activity: float = dataclasses.field(default_factory=time.time)

        def has_timed_out(self) -> bool:
            """
            Whether the connected component has timed out.
            """
            return (
                time.time() - self.last_activity > self.timeout
                if self.timeout > 0.0
                else False
            )

    def __init__(
        self, comp_id: UnitID, config: Configuration, message_builder: MessageBuilder
    ):
        """
        Args:
            comp_id: The component identifier.
            config: The global configuration.
            message_builder: A message builder to use.
        """
        self._comp_id = comp_id
        self._config = config

        self._message_builder = message_builder

        super().__init__(
            async_mode="gevent",
            cors_allowed_origins=self._get_allowed_origins(),
            cors_credentials=True,
        )

        self._connected_components: typing.Dict[UnitID, Server._ComponentEntry] = {}

        self._message_handler: ServerMessageHandler | None = None

        self._lock = threading.RLock()

        self._connect_events()

    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)
        self.on("*", self._on_message)

    def set_message_handler(self, msg_handler: ServerMessageHandler) -> None:
        """
        Sets a handler that gets called when a message arrives.

        Args:
            msg_handler: The message handler to be called.
        """
        self._message_handler = msg_handler

    def run(self) -> None:
        """
        So far, does exactly nothing.
        """

    def process(self) -> None:
        """
        Periodically purges timed out clients.
        """
        with self._lock:
            for timed_out_component in self._find_timed_out_components():
                if timed_out_component in self._connected_components:
                    debug(
                        "Component timed out, disconnecting",
                        scope="server",
                        component=str(timed_out_component),
                        timeout=self._connected_components[timed_out_component].timeout,
                    )

                    self.disconnect(
                        self._connected_components[timed_out_component].sid
                    )  # This will trigger _on_disconnect, removing the client from the connected components

    def send_message(
        self, msg: Message, *, skip_components: typing.List[UnitID] | None = None
    ) -> SendTarget:
        """
        Sends a message to one or more clients.

        For this, the message will be encoded as *JSON* first.

        Args:
            msg: The message to send.
            skip_components: A list of components (clients) to be excluded from the targets.
        """
        with self._lock:
            debug(f"Sending message: {msg}", scope="server")

            if msg.target.is_direct and msg.target.target_id is not None:
                self._timestamp_component(msg.target.target_id)

            send_to = self._get_message_recipient(msg)
            self.emit(
                msg.name,
                data=msg.to_json(),
                to=send_to,
                skip_sid=self._component_ids_to_clients(skip_components),
            )
            return (
                Server.SendTarget.DIRECT
                if msg.target.is_direct and send_to is not None
                else Server.SendTarget.SPREAD
            )

    def _on_connect(self, sid: str, _, auth: typing.Dict[str, typing.Any]) -> None:
        with self._lock:
            try:
                comp_id = UnitID.from_string(auth["component_id"])
            except Exception as exc:  # pylint: disable=broad-exception-caught
                import socketio.exceptions as sioexc

                raise sioexc.ConnectionRefusedError(
                    f"The client {sid} did not provide proper authorization"
                ) from exc

            if comp_id in self._connected_components:
                warning(
                    f"A component with the ID {comp_id} has already been connected to the server",
                    scope="server",
                )

            if self._purge_client(sid):
                warning(
                    f"A client with the SID {sid} has already been connected to the server",
                    scope="server",
                )

            from ....settings import NetworkServerSettingIDs
            from ....component import ComponentType

            self._connected_components[comp_id] = Server._ComponentEntry(
                sid,
                timeout=self._config.value(NetworkServerSettingIDs.IDLE_TIMEOUT)
                if comp_id.type == ComponentType.WEB
                else 0.0,
            )

            from .. import Channel
            from ....api import ServerConnectedEvent

            ServerConnectedEvent.build(
                self._message_builder, comp_id=comp_id, client_id=sid
            ).emit(Channel.local())

            info("Client connected", scope="server", session=sid, component=comp_id)

    def _on_disconnect(self, sid: str) -> None:
        with self._lock:
            comp_id = self._lookup_client(sid)

            self._purge_client(sid)

            from .. import Channel
            from ....api import ServerDisconnectedEvent

            ServerDisconnectedEvent.build(
                self._message_builder, comp_id=comp_id, client_id=sid
            ).emit(Channel.local())

            info("Client disconnected", scope="server", session=sid)

    def _on_message(self, msg_name: str, sid: str, data: str) -> None:
        with self._lock:
            if (comp_id := self._lookup_client(sid)) is not None:
                self._timestamp_component(comp_id)

            if self._message_handler is not None:
                self._message_handler(msg_name, data)

    def _timestamp_component(self, comp_id: UnitID) -> None:
        if comp_id in self._connected_components:
            self._connected_components[comp_id].last_activity = time.time()

    def _find_timed_out_components(self) -> typing.List[UnitID]:
        """
        Finds all components that have timed out already.

        Returns:
            A list of all timed out components.
        """
        return [
            comp_id
            for comp_id, entry in self._connected_components.items()
            if entry.has_timed_out()
        ]

    def _purge_client(self, sid: str) -> bool:
        if (comp_id := self._lookup_client(sid)) is not None:
            self._connected_components.pop(comp_id)
            return True

        return False

    def _lookup_client(self, sid: str) -> UnitID | None:
        for comp_id, client_entry in self._connected_components.items():
            if client_entry.sid == sid:
                return comp_id

        return None

    def _component_id_to_client(self, comp_id: UnitID) -> str | None:
        return (
            self._connected_components[comp_id].sid
            if comp_id in self._connected_components
            else None
        )

    def _component_ids_to_clients(
        self, comp_ids: typing.List[UnitID]
    ) -> typing.List[str] | None:
        return (
            [
                sid
                for sid in map(self._component_id_to_client, comp_ids)
                if sid is not None
            ]
            if len(comp_ids) > 0
            else None
        )

    def _get_message_recipient(self, msg: Message) -> str | None:
        if msg.target.is_direct:
            return self._component_id_to_client(msg.target.target_id)

        return None

    def _get_allowed_origins(self) -> str | typing.List[str] | None:
        from ....settings import NetworkServerSettingIDs

        allowed_origins: str = self._config.value(
            NetworkServerSettingIDs.ALLOWED_ORIGINS
        )
        if allowed_origins != "":
            return "*" if allowed_origins == "*" else allowed_origins.split(",")

        return None
