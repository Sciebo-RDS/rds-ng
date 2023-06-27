import json
import typing

from semantic_version import Version
import socketio

from .component_id import ComponentID
from .component_role import ComponentRole
from ..core import Core
from ..core.service import Service, ServiceContext, ServiceContextType


class Component:
    """ Base application class for all RDS components. """
    def __init__(self, comp_id: ComponentID, role:  ComponentRole, *, module_name: str):
        from .meta_information import MetaInformation
        meta_info = MetaInformation()
        comp_info = meta_info.get_component(comp_id.component)
        
        self._comp_id = comp_id
        self._role = role
        self._title = meta_info.title
        self._name = comp_info["name"]
        self._version = meta_info.version
        
        from ..core import logging
        logging.info(str(self))
        logging.info("-- Starting component...")
        
        self._core = Core(module_name, self._role)
        
        self._add_default_routes()
        
    def wsgi_app(self) -> socketio.WSGIApp:
        return socketio.WSGIApp(self._core.network.server, self.core.flask)
    
    def create_service(self, name: str, *, context_type: typing.Type[ServiceContextType] = ServiceContext) -> Service:
        svc = Service(self._comp_id, name, message_bus=self._core.message_bus, context_type=context_type)
        self._core.register_service(svc)
        return svc
    
    @property
    def core(self) -> Core:
        return self._core
    
    @property
    def comp_id(self) -> ComponentID:
        return self._comp_id
    
    @property
    def role(self) -> ComponentRole:
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
