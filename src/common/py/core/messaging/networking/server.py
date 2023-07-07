import threading
import typing

import socketio

from .. import Message
from ...logging import info, warning, debug
from ....component import ComponentID, ComponentData


class Server(socketio.Server):
    def __init__(self, comp_data: ComponentData):
        self._comp_data = comp_data
        
        super().__init__(async_mode="gevent_uwsgi", cors_allowed_origins=self._get_allowed_origins(), cors_credentials=True)
        
        self._connected_components: typing.Dict[ComponentID, str] = {}
        
        self._lock = threading.Lock()
        
        self._connect_events()
        
    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)
    
    def run(self) -> None:
        pass
    
    def lookup_client(self, sid: str) -> ComponentID | None:
        for comp_id, client_id in self._connected_components.items():
            if client_id == sid:
                return comp_id
        return None
    
    def send_message(self, msg: Message, skip_components: typing.List[ComponentID] | None = None) -> None:
        debug(f"Sending message: {msg}", scope="server")
        with self._lock:
            self.send(data=msg.to_json(), to=msg.target.target, skip_sid=self._component_ids_to_clients(skip_components))
    
    def _on_connect(self, sid: str, _, auth: typing.Dict[str, typing.Any]) -> None:
        try:
            comp_id = ComponentID.from_string(auth["component_id"])
        except:
            from socketio.exceptions import ConnectionRefusedError
            raise ConnectionRefusedError(f"The client {sid} did not provide proper authorization")
        else:
            if comp_id in self._connected_components:
                warning(f"A component with the ID {comp_id} has already been connected to the server", scope="server")
            
            self._connected_components[comp_id] = sid
        
        info("Client connected", scope="server", session=sid, component=comp_id)
    
    def _on_disconnect(self, sid: str) -> None:
        if (comp_id := self.lookup_client(sid)) is not None:
            self._connected_components.pop(comp_id)
        
        info("Client disconnected", scope="server", session=sid)
        
    def _component_ids_to_clients(self, comp_ids: typing.List[ComponentID]) -> typing.List[str] | None:
        return [client_id for comp_id, client_id in self._connected_components.items() if comp_id in comp_ids] if len(comp_ids) > 0 else None

    def _get_allowed_origins(self) -> typing.List[str] | None:
        from ....settings import NetworkServerSettingIDs
        allowed_origins: str = self._comp_data.config.value(NetworkServerSettingIDs.ALLOWED_ORIGINS)
        return allowed_origins.split(",") if allowed_origins != "" else None
