import json
import typing
from enum import Flag, auto

from semantic_version import Version
import socketio

from .component_id import ComponentID
from .config import Configuration
from ..core import Core
from ..core.service import Service, ServiceContext, ServiceContextType
from ..core.logging import info, warning


class Component:
    """ Base application class for all RDS components. """
    
    class Role(Flag):
        SERVER = auto()
        CLIENT = auto()
        
    def __init__(self, base_id: ComponentID, role:  Role, *, module_name: str, config_file: str = "./config.toml"):
        self._config = self._create_config(config_file)
        self._comp_id = self._generate_comp_id(base_id)
        
        from .meta_information import MetaInformation
        meta_info = MetaInformation()
        comp_info = meta_info.get_component(self._comp_id.component)
        
        self._role = role
        self._title = meta_info.title
        self._name = comp_info["name"]
        self._version = meta_info.version
        
        info(str(self))
        info("-- Starting component...")
        
        self._core = Core(module_name, self._config, enable_server=(Component.Role.SERVER in role), enable_client=(Component.Role.CLIENT in role))
        
        self._add_default_routes()
        
    def wsgi_app(self) -> socketio.WSGIApp:
        return socketio.WSGIApp(self._core.network.server, self.core.flask)
    
    def create_service(self, name: str, *, context_type: typing.Type[ServiceContextType] = ServiceContext) -> Service:
        svc = Service(self._comp_id, name, message_bus=self._core.message_bus, context_type=context_type)
        self._core.register_service(svc)
        return svc
    
    def _create_config(self, config_file: str) -> Configuration:
        from common.py.component.config import GeneralSettings
        config = Configuration()
        config.add_defaults({
            GeneralSettings.DEBUG: False,
        })
        
        try:
            config.load(config_file)
        except Exception as e:
            warning("-- Component configuration could not be loaded", scope="core", error=str(e))
        
        return config
    
    def _generate_comp_id(self, base_id: ComponentID) -> ComponentID:
        if base_id.instance is None:
            return ComponentID(base_id.type, base_id.component)
        else:
            return base_id
    
    @property
    def config(self) -> Configuration:
        return self._config

    @property
    def core(self) -> Core:
        return self._core
    
    @property
    def comp_id(self) -> ComponentID:
        return self._comp_id
    
    @property
    def role(self) -> Role:
        return self._role
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> Version:
        return self._version
        
    def __str__(self) -> str:
        return f"{self._title} v{self._version}: {self._name} ({self._comp_id})"
    
    def _add_default_routes(self) -> None:
        # The main entry point (/) returns basic component info as a JSON string
        self._core.flask.add_url_rule("/", view_func=lambda: json.dumps({
            "id": str(self._comp_id),
            "name": self._name,
            "version": str(self._version),
        }))
