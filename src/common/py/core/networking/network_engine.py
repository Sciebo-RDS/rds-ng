import typing

import socketio


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, *, enable_server: bool, enable_client: bool, allowed_origins: typing.List[str] | None):
        self._server = self._create_server(allowed_origins) if enable_server else None
        self._client = self._create_client() if enable_client else None
        
    def _create_server(self, allowed_origins: typing.List[str] | None) -> socketio.Server:
        svr = socketio.Server(async_mode="gevent_uwsgi", cors_allowed_origins=allowed_origins)
        return svr

    def _create_client(self) -> socketio.Client:
        return socketio.Client()

    @property
    def has_server(self) -> bool:
        return self._server is not None
    
    @property
    def server(self) -> socketio.Server:
        return self._server

    @property
    def has_client(self) -> bool:
        return self._client is not None
    
    @property
    def client(self) -> socketio.Client:
        return self._client
