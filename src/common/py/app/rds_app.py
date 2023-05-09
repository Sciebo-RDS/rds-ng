from semantic_version import Version
import json
import socketio

from common.py.core import Core


class RDSApp:
    """ Base application class for all RDS components. """
    def __init__(self, def_file: str = "./component.json", *, module_name: str):
        self._appid, self._name, self._version = self._load_definition(def_file)
        
        self._core = Core(module_name)
            
    def _load_definition(self, def_file: str) -> (str, str, Version):
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
        return socketio.WSGIApp(self._core.server, self.core.flask)
    
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
    