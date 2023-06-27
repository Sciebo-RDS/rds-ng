import typing
import flask

from .logging import info, debug, set_level
from .messaging import MessageBus
from .networking import NetworkEngine
from .service import Service
from ..config import Configuration


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str, config: Configuration, *, enable_server: bool, enable_client: bool):
        info("Initializing core...", scope="core")
        
        self._config = config
        
        if self.is_debug_mode:
            self._enable_debug_mode()
        
        debug(f"-- Settings file: {config.settings_file}", scope="core")
        
        debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        debug("-- Creating network engine", scope="core", enable_server=enable_server, enable_client=enable_client)
        self._network_engine = self._create_network_engine(enable_server=enable_server, enable_client=enable_client)
        
        debug("-- Creating message bus", scope="core")
        self._message_bus = self._create_message_bus()
        
    def _create_message_bus(self) -> MessageBus:
        return MessageBus(self._network_engine, self._config)
    
    def _create_flask(self, module_name: str) -> flask.Flask:
        from ..utils.random import generate_random_string
        
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
        return flsk
    
    def _create_network_engine(self, *, enable_server: bool, enable_client: bool) -> NetworkEngine:
        # TODO: Define proper CORS origins (nw-internal)
        allowed_origins: typing.List[str] | None = None
        if self.is_debug_mode:
            allowed_origins = ["*"]
        return NetworkEngine(enable_server=enable_server, enable_client=enable_client, allowed_origins=allowed_origins)
    
    def _enable_debug_mode(self) -> None:
        import logging as log
        set_level(log.DEBUG)
        debug("-- Debug mode enabled", scope="core")
    
    def register_service(self, svc: Service) -> None:
        if self._message_bus.add_service(svc):
            debug(f"Registered service: {svc}", scope="core")
        else:
            debug("Service already registered", scope="core", service=svc)

    def unregister_service(self, svc: Service) -> None:
        if self._message_bus.remove_service(svc):
            debug(f"Unregistered service: {svc}", scope="core")
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
        from ..config import GeneralSettings
        return self.config.value(GeneralSettings.DEBUG)
