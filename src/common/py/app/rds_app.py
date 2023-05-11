import os.path

from semantic_version import Version
import json
import socketio

from ..core import Core
from ..core import logging


class RDSApp:
    """ Base application class for all RDS components. """
    def __init__(self, def_file: str = "./component.json", *, module_name: str):
        self._appid, self._name, self._version = self._load_definition(def_file)
        
        self._core = Core(module_name)
        
        logging.info(str(self))
        logging.info("-- Starting component application...")
            
    def _load_definition(self, def_file: str) -> (str, str, Version):
        if def_file == "" or not os.path.exists(def_file):
            raise ValueError("Invalid component definition file given")
        
        with open(def_file) as f:
            try:
                data = json.load(f)
                comp_info = data["component"]
                appid = comp_info["id"]
                name = comp_info["name"]
                version = Version(comp_info["version"])
            except Exception as e:
                return "<invalid>", str(e), Version("0.0.0")
            else:
                return appid, name, version
            
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
