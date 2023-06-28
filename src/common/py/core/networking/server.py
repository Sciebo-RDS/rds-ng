import typing

import socketio

from ..logging import info
from ...utils.config import Configuration


class Server(socketio.Server):
    def __init__(self, config: Configuration, *args, **kwargs):
        super().__init__(*args, async_mode="gevent_uwsgi", cors_allowed_origins=self._get_allowed_origins(config), **kwargs)
        
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)
        
    def run(self) -> None:
        pass
        
    def _on_connect(self, sid, _) -> None:
        info("Client connected", scope="server", session=sid)
    
    def _on_disconnect(self, sid) -> None:
        info("Client disconnected", scope="server", session=sid)

    def _get_allowed_origins(self, config: Configuration) -> typing.List[str] | None:
        from ...settings import NetworkServerSettingIDs
        allowed_origins: str = config.value(NetworkServerSettingIDs.ALLOWED_ORIGINS)
        return allowed_origins.split(",") if allowed_origins != "" else None
