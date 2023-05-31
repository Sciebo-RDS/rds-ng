import typing
import flask

from .config import Configuration
from .messaging import MessageBus
from .networking import NetworkEngine


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str, config_file: str = "./config.toml"):
        from ..core import logging
        logging.info("Initializing core...", scope="core")
        
        logging.info("-- Loading configuration", scope="core", file=config_file)
        self._config = self._create_config(config_file)
        
        if self.is_debug_mode:
            self._enable_debug_mode()
            
        logging.debug("-- Creating message bus", scope="core")
        self._message_bus = self._create_message_bus()
        
        logging.debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        logging.debug("-- Creating network engine", scope="core")
        self._network_engine = self._create_network_engine()
        
    def _create_config(self, config_file: str) -> Configuration:
        from .config import GeneralSettings
        config = Configuration()
        config.add_defaults({
            GeneralSettings.DEBUG: False,
        })
        
        try:
            config.load(config_file)
        except Exception as e:
            from ..core import logging
            logging.warning("-- Component configuration could not be loaded", scope="core", error=str(e))
            
        return config
    
    def _create_message_bus(self) -> MessageBus:
        return MessageBus()
    
    def _create_flask(self, module_name: str) -> flask.Flask:
        from ..utils.random import generate_random_string
        
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
        return flsk
    
    def _create_network_engine(self) -> NetworkEngine:
        # TODO: Define proper CORS origins (nw-internal)
        allowed_origins: typing.List[str] | None = None
        if self.is_debug_mode:
            allowed_origins = ["*"]
        return NetworkEngine(allowed_origins)
    
    def _enable_debug_mode(self) -> None:
        from ..core import logging
        import logging as log
        logging.set_level(log.DEBUG)
        logging.debug("-- Debug mode enabled", scope="core")
    
    @property
    def config(self) -> Configuration:
        return self._config
    
    @property
    def message_bus(self) -> MessageBus:
        return self._message_bus
    
    @property
    def flask(self) -> flask.Flask:
        return self._flask
    
    @property
    def network(self) -> NetworkEngine:
        return self._network_engine
    
    @property
    def is_debug_mode(self) -> bool:
        from .config import GeneralSettings
        return self.config.value(GeneralSettings.DEBUG)
