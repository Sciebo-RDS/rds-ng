from semantic_version import Version
import socketio

from ..core import Core
from ..core import logging


class RDSApp:
    """ Base application class for all RDS components. """
    def __init__(self, appid: str, *, module_name: str):
        from .meta_information import MetaInformation
        meta_info = MetaInformation()
        comp_info = meta_info.get_component(appid)
        
        self._appid = appid
        self._name = comp_info["name"]
        self._version = meta_info.version
        
        self._core = Core(module_name)
        
        logging.info(str(self))
        logging.info("-- Starting component application...")
        
    @property
    def core(self) -> Core:
        return self._core
    
    def wsgi_app(self) -> socketio.WSGIApp:
        return socketio.WSGIApp(self._core.network.server, self.core.flask)
    
    @property
    def app_id(self) -> str:
        return self._appid
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> Version:
        return self._version
        
    def __str__(self) -> str:
        return f"{self._name} ({self._appid}), v{self._version}"
