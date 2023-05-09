import os
import flask

from .networking import NetworkEngine

from common.py.utils.random import generate_random_string


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str):
        self._flask: flask.Flask = self._create_flask(module_name)
        
        self._network_engine: NetworkEngine = self._create_network_engine()
        
    def _create_flask(self, module_name: str) -> flask.Flask:
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64, include_punctuation=True)
        return flsk
    
    def _create_network_engine(self) -> NetworkEngine:
        return NetworkEngine()
    
    @property
    def flask(self) -> flask.Flask:
        return self._flask
    
    @property
    def network(self) -> NetworkEngine:
        return self._network_engine
    
    @property
    @staticmethod
    def is_debug_mode() -> bool:
        return os.getenv("RDS_DEBUG", "0") == "1"
