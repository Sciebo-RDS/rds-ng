import threading
import typing

import socketio

from .. import Message
from ...logging import info, warning, error, debug
from ....utils import UnitID
from ....utils.config import Configuration

ClientMessageHandler = typing.Callable[[str, str], None]


class Client(socketio.Client):
    """
    The client connection, based on ``socketio.Client``.
    """
    
    def __init__(self, comp_id: UnitID, config: Configuration):
        """
        Args:
            comp_id: The component identifier.
            config: The global configuration.
        """
        self._comp_id = comp_id
        self._config = config
        
        from ....settings import NetworkClientSettingIDs
        
        self._server_address: str = self._config.value(
            NetworkClientSettingIDs.SERVER_ADDRESS
        )
        self._connection_timeout: int = self._config.value(
            NetworkClientSettingIDs.CONNECTION_TIMEOUT
        )
        
        super().__init__(reconnection_delay_max=self._connection_timeout)
        
        self._message_handler: ClientMessageHandler | None = None
        
        self._lock = threading.Lock()
        
        self._connect_events()
    
    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("connect_error", self._on_connect_error)
        self.on("disconnect", self._on_disconnect)
        self.on("*", self._on_message)
    
    def set_message_handler(self, msg_handler: ClientMessageHandler) -> None:
        """
        Sets a handler that gets called when a message arrives.

        Args:
            msg_handler: The message handler to be called.
        """
        self._message_handler = msg_handler
    
    def run(self) -> None:
        """
        Automatically connects to a server if one was configured.
        """
        if self._server_address != "":
            info(f"Connecting to {self._server_address}...", scope="client")
            
            import socketio.exceptions as sioexc
            
            try:
                self.connect(
                    self._server_address,
                    auth=self._get_authentication(),
                    wait=True,
                    wait_timeout=self._connection_timeout,
                )
            except sioexc.ConnectionError as exc:
                error(f"Failed to connect to server: {str(exc)}", scope="client")
    
    def process(self) -> None:
        """
        Periodically performs certain tasks.
        """
    
    def send_message(self, msg: Message) -> None:
        """
        Sends a message to the server (if connected).

        For this, the message will be encoded as *JSON* first.

        Args:
            msg: The message to send.
        """
        if self.connected:
            debug(f"Sending message: {msg}", scope="client")
            with self._lock:
                self.emit(msg.name, data=msg.to_json())
    
    def _on_connect(self) -> None:
        info("Connected to server", scope="client")
    
    def _on_connect_error(self, reason: typing.Any) -> None:
        warning("Unable to connect to server", scope="client", reason=str(reason))
    
    def _on_disconnect(self) -> None:
        info("Disconnected from server", scope="client")
    
    def _on_message(self, msg_name: str, data: str) -> None:
        if self._message_handler is not None:
            self._message_handler(msg_name, data)
    
    def _get_authentication(self) -> typing.Dict[str, str]:
        return {"component_id": str(self._comp_id)}
