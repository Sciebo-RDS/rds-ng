import threading
import typing
from enum import IntEnum, auto

import socketio

from .. import Message
from ...logging import info, warning, debug
from ....utils import UnitID
from ....utils.config import Configuration


class Server(socketio.Server):
    """
    The server connection, based on ``socketio.Server``.
    """

    class SendTarget(IntEnum):
        """
        Flag telling whether an outgoing message is only sent to a single (direct) target or spread across all connected clients.
        """

        SPREAD = auto()
        DIRECT = auto()

    def __init__(self, comp_id: UnitID, config: Configuration):
        """
        Args:
            comp_id: The component identifier.
            config: The global configuration.
        """
        self._comp_id = comp_id
        self._config = config

        super().__init__(
            async_mode="gevent_uwsgi",
            cors_allowed_origins=self._get_allowed_origins(),
            cors_credentials=True,
        )

        self._connected_components: typing.Dict[UnitID, str] = {}

        self._lock = threading.Lock()

        self._connect_events()

    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)

    def run(self) -> None:
        """
        So far, does exactly nothing.
        """
        # TODO: Periodically purge obsolete frontends

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
        debug(f"Sending message: {msg}", scope="server")
        with self._lock:
            send_to: str | None = self._get_message_recipient(msg)
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
        try:
            comp_id = UnitID.from_string(auth["component_id"])
        except Exception as exc:  # pylint: disable=broad-exception-caught
            import socketio.exceptions as sioexc

            raise sioexc.ConnectionRefusedError(
                f"The client {sid} did not provide proper authorization"
            ) from exc

        # TODO: Purge components with the same sid
        if comp_id in self._connected_components:
            warning(
                f"A component with the ID {comp_id} has already been connected to the server",
                scope="server",
            )

        self._connected_components[comp_id] = sid

        info("Client connected", scope="server", session=sid, component=comp_id)

    def _on_disconnect(self, sid: str) -> None:
        if (comp_id := self._lookup_client(sid)) is not None:
            self._connected_components.pop(comp_id)

        info("Client disconnected", scope="server", session=sid)

    def _lookup_client(self, sid: str) -> UnitID | None:
        for comp_id, client_id in self._connected_components.items():
            if client_id == sid:
                return comp_id

        return None

    def _component_id_to_client(self, comp_id: UnitID) -> str | None:
        return (
            self._connected_components[comp_id]
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
        if msg.target.is_room:
            return msg.target.target

        return None

    def _get_allowed_origins(self) -> str | typing.List[str] | None:
        from ....settings import NetworkServerSettingIDs

        allowed_origins: str = self._config.value(
            NetworkServerSettingIDs.ALLOWED_ORIGINS
        )
        if allowed_origins != "":
            return "*" if allowed_origins == "*" else allowed_origins.split(",")

        return None
