import threading
import typing

import socketio

from ..logging import info, debug
from ..messaging import Message
from ...utils.config import Configuration


class Server(socketio.Server):
    def __init__(self, config: Configuration):
        super().__init__(async_mode="gevent_uwsgi", cors_allowed_origins=self._get_allowed_origins(config))
        
        self._lock = threading.Lock()
        
        self._connect_events()
        
    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)
        self.on("message", self._on_message)
    
    def run(self) -> None:
        pass
        
    def send_message(self, msg: Message) -> None:
        debug(f"Sending message: {msg}", scope="server")
        with self._lock:
            self.send(data=msg.data(), to=msg.target.target)
    
    def _on_connect(self, sid, _) -> None:
        info("Client connected", scope="server", session=sid)
    
    def _on_disconnect(self, sid) -> None:
        info("Client disconnected", scope="server", session=sid)
        
    def _on_message(self, _, data) -> None:
        # TODO: Turn data into msg; dispatch it (rebounce if needed)
        print(data)

    def _get_allowed_origins(self, config: Configuration) -> typing.List[str] | None:
        from ...settings import NetworkServerSettingIDs
        allowed_origins: str = config.value(NetworkServerSettingIDs.ALLOWED_ORIGINS)
        return allowed_origins.split(",") if allowed_origins != "" else None
