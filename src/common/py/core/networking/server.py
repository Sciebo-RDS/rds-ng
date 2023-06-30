import json
import threading
import typing

import socketio

from ..logging import info, warning, debug
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
            self.send(data=msg.to_json(), to=msg.target.target)
    
    def _on_connect(self, sid, _) -> None:
        info("Client connected", scope="server", session=sid)
    
    def _on_disconnect(self, sid) -> None:
        info("Client disconnected", scope="server", session=sid)
        
    def _on_message(self, _, data) -> None:
        msg = Message.from_json(data)
        print("XXX", msg)
        
        # 1. Get base Message structure from data
        # 2. Check if the message needs to be dispatched locally
        #   a. If so, lookup the message name in a (yet to come) message name -> class map
        #   b. Create an instance of that class and fill the fields
        #   c. Dispatch the message (target -> local)
        # 3. Also check if it needs to be sent remotely
        #   a. Directly use the NWE for this; do not use the message bus (we might not know the message type)
        # Might need a channel resolver here as well; could be merged?

    def _get_allowed_origins(self, config: Configuration) -> typing.List[str] | None:
        from ...settings import NetworkServerSettingIDs
        allowed_origins: str = config.value(NetworkServerSettingIDs.ALLOWED_ORIGINS)
        return allowed_origins.split(",") if allowed_origins != "" else None
