from flask import Flask
from flask_socketio import SocketIO


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str):
        self._flask = self._create_flask(module_name)
        self._socketio = self._create_socketio()
        print(str(self._socketio))
        
    def _create_flask(self, module_name: str) -> Flask:
        return Flask(module_name)
    
    def _create_socketio(self) -> SocketIO:
        return SocketIO(self._flask, host="0.0.0.0", port="7070")
    
    @property
    def flask(self) -> Flask:
        return self._flask
    
    @property
    def socketio(self) -> SocketIO:
        return self._socketio
    