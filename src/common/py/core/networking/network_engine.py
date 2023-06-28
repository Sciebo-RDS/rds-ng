import typing

from .client import Client
from .server import Server
from ...utils.config import Configuration


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, config: Configuration, *, enable_server: bool, enable_client: bool):
        self._server = self._create_server(config) if enable_server else None
        self._client = self._create_client(config) if enable_client else None
        
    def _create_server(self, config: Configuration) -> Server:
        return Server(config)

    def _create_client(self, config: Configuration) -> Client:
        return Client(config)
    
    def run(self) -> None:
        if self.has_server:
            self._server.run()
            
        if self.has_client:
            self._client.run()
            
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
