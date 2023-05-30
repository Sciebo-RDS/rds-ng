from semantic_version import Version
import socketio

from .component_id import ComponentID
from ..core import Core


class Component:
    """ Base application class for all RDS components. """
    def __init__(self, comp_id: ComponentID, *, module_name: str):
        from .meta_information import MetaInformation
        meta_info = MetaInformation()
        comp_info = meta_info.get_component(comp_id.component)
        
        self._comp_id = comp_id
        self._title = meta_info.title
        self._name = comp_info["name"]
        self._version = meta_info.version
        
        from ..core import logging
        logging.info(str(self))
        logging.info("-- Starting component...")
        
        self._core = Core(module_name)
        
    @property
    def core(self) -> Core:
        return self._core
    
    def wsgi_app(self) -> socketio.WSGIApp:
        return socketio.WSGIApp(self._core.network.server, self.core.flask)
    
    @property
    def comp_id(self) -> ComponentID:
        return self._comp_id
    
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
