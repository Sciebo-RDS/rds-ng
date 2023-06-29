import socketio

from ..logging import info, warning
from ...utils.config import Configuration


class Client(socketio.Client):
    def __init__(self, config: Configuration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from ...settings import NetworkClientSettingIDs
        self._server_address = config.value(NetworkClientSettingIDs.SERVER_ADDRESS)
        
        self.on("connect", self._on_connect)
        self.on("connect_error", self._on_connect_error)
        self.on("disconnect", self._on_disconnect)

    def run(self) -> None:
        if self._server_address != "":
            info(f"Connecting to {self._server_address}...", scope="client")
            self.connect(self._server_address)
            
    def _on_connect(self) -> None:
        info("Connected to server", scope="client")
        
    def _on_connect_error(self, reason) -> None:
        warning("Unable to connect to server", scope="client", reason=str(reason))
    
    def _on_disconnect(self) -> None:
        info("Disconnected from server", scope="client")
