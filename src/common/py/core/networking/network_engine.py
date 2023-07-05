import typing

from .client import Client
from .route_resolver import RouteResolver
from .server import Server
from ..messaging import Message
from ...component import ComponentData


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, comp_data: ComponentData):
        self._comp_data = comp_data
        
        self._client = self._create_client() if self._comp_data.role.networking_aspect.has_client else None
        self._server = self._create_server() if self._comp_data.role.networking_aspect.has_server else None
        
        self._route_resolver = RouteResolver(has_client=self.has_client, has_server=self.has_server)  # TODO

    def _create_client(self) -> Client:
        return Client(self._comp_data.config)
    
    def _create_server(self) -> Server:
        return Server(self._comp_data.config)
    
    def run(self) -> None:
        if self.has_server:
            self._server.run()
            
        if self.has_client:
            self._client.run()
            
    def send_message(self, msg: Message) -> None:
        route_type = self._route_resolver.resolve(msg)
        
        if RouteResolver.Routing.CLIENT in route_type and self.has_client:
            self._client.send_message(msg)
            
        if RouteResolver.Routing.SERVER in route_type and self.has_server:
            self._server.send_message(msg)
        
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
