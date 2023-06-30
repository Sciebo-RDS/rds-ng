import dataclasses
import threading

import socketio

from ..logging import info, warning, debug
from ..messaging import Message
from ...utils.config import Configuration


class Client(socketio.Client):
    def __init__(self, config: Configuration):
        super().__init__()
        
        from ...settings import NetworkClientSettingIDs
        self._server_address = config.value(NetworkClientSettingIDs.SERVER_ADDRESS)
        
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
            self.connect(self._server_address)
            
    def send_message(self, msg: Message) -> None:
        debug(f"Sending message: {msg}", scope="client")
        with self._lock:
            self.send(data=msg.to_json())
    
    def _on_connect(self) -> None:
        info("Connected to server", scope="client")
        
    def _on_connect_error(self, reason) -> None:
        warning("Unable to connect to server", scope="client", reason=str(reason))
    
    def _on_disconnect(self) -> None:
        info("Disconnected from server", scope="client")
        
    def _on_message(self, data) -> None:
        # TODO: Turn data into msg; dispatch it (rebounce if needed)
        print(data)
