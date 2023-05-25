import os
import flask

from .config import Configuration
from .networking import NetworkEngine


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str, config_file: str = "./config.toml"):
        from ..core import logging
        logging.debug("Initializing core...", scope="core")
        
        logging.debug("-- Loading configuration", scope="core", file=config_file)
        self._config = self._create_config(config_file)
        
        logging.debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        logging.debug("-- Creating network engine", scope="core")
        self._network_engine = self._create_network_engine()
        
    def _create_config(self, config_file: str) -> Configuration:
        config = Configuration()
        try:
            config.load(config_file)
        except Exception as e:
            from ..core import logging
            logging.warning("-- Component configuration could not be loaded", scope="core", error=str(e))
        return config
    
    def _create_flask(self, module_name: str) -> flask.Flask:
        from ..utils.random import generate_random_string
        
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
        return flsk
    
    def _create_network_engine(self) -> NetworkEngine:
        return NetworkEngine()
    
    @property
    def config(self) -> Configuration:
        return self._config
    
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
