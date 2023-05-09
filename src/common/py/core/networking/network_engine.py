import socketio


class NetworkEngine:
    """ The main network management class, based on socket.io. """
    def __init__(self):
        self._server: socketio.Server = self._create_server()
        self._client: socketio.Client = self._create_client()
        
    def _create_server(self) -> socketio.Server:
        from common.py.core import Core
        
        # TODO: Define proper CORS origins (nw-internal)
        allowed_origins = None
        if Core.is_debug_mode:
            allowed_origins = "*"
    
        svr = socketio.Server(async_mode="gevent_uwsgi", cors_allowed_origins=allowed_origins)
        return svr

    def _create_client(self) -> socketio.Client:
        return socketio.Client()

    @property
    def server(self):
        return self._server

    @property
    def client(self):
        return self._client
