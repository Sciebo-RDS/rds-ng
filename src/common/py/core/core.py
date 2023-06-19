import typing
import flask

from .config import Configuration
from .logging import info, warning, debug, set_level
from .messaging import MessageBus
from .networking import NetworkEngine
from .service import Service


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str, config_file: str = "./config.toml"):
        info("Initializing core...", scope="core")
        
        info("-- Loading configuration", scope="core", file=config_file)
        self._config = self._create_config(config_file)
        
        if self.is_debug_mode:
            self._enable_debug_mode()
        
        debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        debug("-- Creating network engine", scope="core")
        self._network_engine = self._create_network_engine()
        
        debug("-- Creating message bus", scope="core")
        self._message_bus = self._create_message_bus()
        
    def _create_config(self, config_file: str) -> Configuration:
        from .config import GeneralSettings
        config = Configuration()
        config.add_defaults({
            GeneralSettings.DEBUG: False,
        })
        
        try:
            config.load(config_file)
        except Exception as e:
            warning("-- Component configuration could not be loaded", scope="core", error=str(e))
            
        return config
    
    def _create_message_bus(self) -> MessageBus:
        return MessageBus(self._network_engine, self._config)
    
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
        import logging as log
        set_level(log.DEBUG)
        debug("-- Debug mode enabled", scope="core")
    
    def register_service(self, svc: Service) -> None:
        if self._message_bus.add_service(svc):
            debug("Registered service", scope="core", service=svc)
        else:
            debug("Service already registered", scope="core", service=svc)

    def unregister_service(self, svc: Service) -> None:
        if self._message_bus.remove_service(svc):
            debug("Unregistered service", scope="core", service=svc)
        else:
            debug("Service not registered", scope="core", service=svc)
    
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
