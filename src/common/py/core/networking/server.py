import threading
import typing

import socketio

from ..logging import info, warning, debug
from ..messaging import Message
from ...component import ComponentID, ComponentData
from ...utils.config import Configuration


class Server(socketio.Server):
    def __init__(self, comp_data: ComponentData):
        self._comp_data = comp_data
        
        super().__init__(async_mode="gevent_uwsgi", cors_allowed_origins=self._get_allowed_origins(self._comp_data.config), cors_credentials=True)
        
        self._connected_components: typing.Dict[ComponentID, str] = {}
        
        self._lock = threading.Lock()
        
        self._connect_events()
        
    def _connect_events(self) -> None:
        self.on("connect", self._on_connect)
        self.on("disconnect", self._on_disconnect)
        self.on("message", self._on_message)
    
    def run(self) -> None:
        pass
        
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
        if (comp_id := self._lookup_client(sid)) is not None:
            self._connected_components.pop(comp_id)
        
        info("Client disconnected", scope="server", session=sid)
        
    def _on_message(self, _, data: str) -> None:
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
        
    def _lookup_client(self, sid: str) -> ComponentID | None:
        for comp_id, client_id in self._connected_components:
            if client_id == sid:
                return comp_id
        return None
    
    def _component_ids_to_clients(self, comp_ids: typing.List[ComponentID]) -> typing.List[str] | None:
        return [client_id for comp_id, client_id in self._connected_components.items() if comp_id in comp_ids] if len(comp_ids) > 0 else None

    def _get_allowed_origins(self, config: Configuration) -> typing.List[str] | None:
        from ...settings import NetworkServerSettingIDs
        allowed_origins: str = config.value(NetworkServerSettingIDs.ALLOWED_ORIGINS)
        return allowed_origins.split(",") if allowed_origins != "" else None
