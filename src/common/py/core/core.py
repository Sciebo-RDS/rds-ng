import os
import flask
import socketio

from common.py.utils.random import generate_random_string


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str):
        self._flask: flask.Flask = self._create_flask(module_name)
        
        self._server: socketio.Server = self._create_server()
        self._client: socketio.Client = self._create_client()
        
    def _create_flask(self, module_name: str) -> flask.Flask:
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64, include_punctuation=True)
        return flsk
    
    def _create_server(self) -> socketio.Server:
        # TODO: Define proper CORS origins (nw-internal)
        allowed_origins = None
        if Core.is_debug_mode:
            allowed_origins = "*"
        
        svr = socketio.Server(async_mode="gevent_uwsgi", cors_allowed_origins=allowed_origins)
        return svr
    
    def _create_client(self) -> socketio.Client:
        return socketio.Client()
    
    @property
    def flask(self) -> flask.Flask:
        return self._flask
    
    @property
    def server(self):
        return self._server
    
    @property
    def client(self):
        return self._client

    @property
    @staticmethod
    def is_debug_mode() -> bool:
        return os.getenv("RDS_DEBUG", "0") == "1"
    