import typing

from .client import Client
from .routing import NetworkRouter
from .server import Server
from ..messaging import Message
from ...component import ComponentData, ComponentID


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, comp_data: ComponentData):
        self._comp_data = comp_data
        
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
            self._server.run()
            
        if self.has_client:
            self._client.run()
            
    def send_message(self, msg: Message) -> None:
        try:
            self._router.verify_message(msg)
        except NetworkRouter.RoutingError as e:
            from ..logging import error
            error(f"A routing error occurred: {str(e)}", scope="network", message=str(msg))
        else:
            route_to_server, skip_components = self._router.check_server_routing(msg)
            if route_to_server:
                self._server.send_message(msg, skip_components=skip_components)
                
            if self._router.check_client_routing(msg):
                self._client.send_message(msg)
        
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
