import typing

from .client import Client
from .routing import NetworkRouter
from .server import Server
from .. import Message, MessageBusProtocol
from ..meta import MessageMetaInformation
from ....component import ComponentData


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, comp_data: ComponentData, message_bus: MessageBusProtocol):
        self._comp_data = comp_data
        
        self._message_bus = message_bus
        
        self._client = self._create_client() if self._comp_data.role.networking_aspects.has_client else None
        self._server = self._create_server() if self._comp_data.role.networking_aspects.has_server else None
        
        self._router = typing.cast(NetworkRouter, self._comp_data.role.networking_aspects.router_type(comp_data.comp_id))
        if not isinstance(self._router, NetworkRouter):
            raise RuntimeError("An invalid router type was specified in the networking aspects")

    def _create_client(self) -> Client:
        return Client(self._comp_data)
    
    def _create_server(self) -> Server:
        return Server(self._comp_data)
    
    def run(self) -> None:
        if self.has_server:
            self._server.on("message", lambda sid, data: self._handle_received_message(MessageMetaInformation.Entrypoint.SERVER, sid, data))
            self._server.run()
            
        if self.has_client:
            self._client.on("message", lambda data: self._handle_received_message(MessageMetaInformation.Entrypoint.CLIENT, None, data))
            self._client.run()
            
    def send_message(self, msg: Message, msg_meta: MessageMetaInformation) -> None:
        try:
            self._router.verify_message(NetworkRouter.Direction.OUT, msg)
        except NetworkRouter.RoutingError as e:
            self._routing_error(str(e), message=str(msg))
        else:
            if self._router.check_server_routing(NetworkRouter.Direction.OUT, msg, msg_meta):
                self._server.send_message(msg, skip_components=[self._comp_data.comp_id])
                
            if self._router.check_client_routing(NetworkRouter.Direction.OUT, msg, msg_meta):
                self._client.send_message(msg)
    
    def _handle_received_message(self, entrypoint: MessageMetaInformation.Entrypoint, sid: str | None, data: str) -> None:
        try:
            msg = Message.from_json(data)  # TODO Real msg
            self._router.verify_message(NetworkRouter.Direction.IN, msg)
            
            from common.py.component import ComponentID
            comp_id: ComponentID | None = None
            if sid is not None and self.has_server:
                comp_id = self._server.lookup_client(sid)
            print("XXX", msg, comp_id)
            # 2. Check if the message needs to be dispatched locally
            #   a. If so, lookup the message name in a (yet to come) message name -> class map
            #   b. Create an instance of that class and fill the fields
            #   c. Dispatch the message (target -> local)
            # 3. Also check if it needs to be sent remotely
            #   a. Directly use the NWE for this; do not use the message bus (we might not know the message type)
            # Might need a channel resolver here as well; could be merged?
        except Exception as e:
            self._routing_error(str(e), data=data)
        
    def _routing_error(self, msg: str, **kwargs) -> None:
        from ...logging import error
        error(f"A routing error occurred: {msg}", scope="network", **kwargs)
    
    @property
    def has_server(self) -> bool:
        return self._server is not None
    
    @property
    def server(self) -> Server:
        return self._server

    @property
    def has_client(self) -> bool:
        return self._client is not None
    
    @property
    def client(self) -> Client:
        return self._client
