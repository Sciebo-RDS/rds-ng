import typing
import flask

from .logging import info, debug, set_level
from .messaging import MessageBus
from .networking import NetworkEngine
from .service import Service
from ..component import ComponentID, ComponentRole
from ..utils.config import Configuration


class Core:
    """ The main portion of an RDS component. """
    def __init__(self, module_name: str, comp_id: ComponentID, config: Configuration, role: ComponentRole):
        info("Initializing core...", scope="core")
        
        self._config = config
        
        if self.is_debug_mode:
            self._enable_debug_mode()
        
        debug(f"-- Settings file: {config.settings_file}", scope="core")
        
        debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        debug("-- Creating network engine", scope="core", role=role)
        self._network_engine = self._create_network_engine(enable_client=(ComponentRole.CLIENT in role), enable_server=(ComponentRole.SERVER in role))
        
        debug("-- Creating message bus", scope="core")
        self._message_bus = self._create_message_bus(comp_id)
    
    def _create_flask(self, module_name: str) -> flask.Flask:
        from ..utils.random import generate_random_string
        
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
        return flsk
    
    def _create_network_engine(self, *, enable_client: bool, enable_server: bool) -> NetworkEngine:
        from .networking import NetworkRouteResolver
        route_resolver = NetworkRouteResolver(has_client=enable_client, has_server=enable_server)
        return NetworkEngine(route_resolver, self._config, enable_client=enable_client, enable_server=enable_server)
    
    def _create_message_bus(self, comp_id: ComponentID) -> MessageBus:
        from .messaging import ChannelResolver
        channel_resolver = ChannelResolver(comp_id)
        return MessageBus(channel_resolver, self._network_engine, self._config)
    
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
            
    def run(self) -> None:
        self._network_engine.run()
        self._message_bus.run()
    
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
        from ..settings import GeneralSettingIDs
        return self.config.value(GeneralSettingIDs.DEBUG)
