import dataclasses
import threading
import typing

import socketio

from ..logging import info, warning, error, debug
from ..messaging import Message
from ...component import ComponentData


class Client(socketio.Client):
    def __init__(self, comp_data: ComponentData):
        self._comp_data = comp_data
        
        from ...settings import NetworkClientSettingIDs
        self._server_address: str = self._comp_data.config.value(NetworkClientSettingIDs.SERVER_ADDRESS)
        self._connection_timeout: int = self._comp_data.config.value(NetworkClientSettingIDs.CONNECTION_TIMEOUT)
        
        super().__init__(reconnection_delay_max=self._connection_timeout)
        
        self._lock = threading.Lock()
        
        self._connect_events()
        
    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("connect_error", self._on_connect_error)
        self.on("disconnect", self._on_disconnect)
        self.on("message", self._on_message)

    def run(self) -> None:
        if self._server_address != "":
            info(f"Connecting to {self._server_address}...", scope="client")
            
            from socketio.exceptions import ConnectionError
            try:
                self.connect(self._server_address, auth=self._get_authentication(), wait=True, wait_timeout=self._connection_timeout)
            except ConnectionError as e:
                error(f"Failed to connect to server: {str(e)}", scope="client")
            
    def send_message(self, msg: Message) -> None:
        if self.connected:
            debug(f"Sending message: {msg}", scope="client")
            with self._lock:
                self.send(data=msg.to_json())
    
    def _on_connect(self) -> None:
        info("Connected to server", scope="client")
        
    def _on_connect_error(self, reason: typing.Any) -> None:
        warning("Unable to connect to server", scope="client", reason=str(reason))
    
    def _on_disconnect(self) -> None:
        info("Disconnected from server", scope="client")
        
    def _on_message(self, data: str) -> None:
        # TODO: Turn data into msg; dispatch it (rebounce if needed)
        print(data)

    def _get_authentication(self) -> typing.Dict[str, str]:
        return {"component_id": str(self._comp_data.comp_id)}
