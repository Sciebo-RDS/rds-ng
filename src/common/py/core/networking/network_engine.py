import typing

import socketio


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self, allowed_origins: typing.List[str] | None):
        self._server = self._create_server(allowed_origins)
        self._client = self._create_client()
        
    def _create_server(self, allowed_origins: typing.List[str] | None) -> socketio.Server:
        svr = socketio.Server(async_mode="gevent_uwsgi", cors_allowed_origins=allowed_origins)
        return svr

    def _create_client(self) -> socketio.Client:
        return socketio.Client()

    @property
    def server(self) -> socketio.Server:
        return self._server

    @property
    def client(self) -> socketio.Client:
        return self._client