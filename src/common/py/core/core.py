import os
import flask

from .networking import NetworkEngine
from ..utils.random import generate_random_string


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str):
        from ..core import logging
        logging.debug("Initializing core...", scope="core")
        
        self._flask = self._create_flask(module_name)
        logging.debug("-- Created Flask server", scope="core", module_name=module_name, secret=self._flask.config["SECRET"])
        
        self._network_engine = self._create_network_engine()
        logging.debug("-- Created network engine", scope="core")
        
    def _create_flask(self, module_name: str) -> flask.Flask:
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
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
