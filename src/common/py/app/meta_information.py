import typing
import os.path
import json
from semantic_version import Version

from ..core import logging


class MetaInformation:
    """ This class is used to access the project meta information stored in a JSON file. """
    def __init__(self, info_file: str = "/config/meta-information.json"):
        if info_file == "" or not os.path.exists(info_file):
            raise ValueError("Invalid meta information file given")
        
        with open(info_file) as f:
            data = json.load(f)
            self._title, self._version = self._read_global_info(data)
            self._components = self._read_component_definitions(data)

    def _read_global_info(self, data: typing.Any) -> tuple[str, Version]:
        try:
            global_info = data["global"]
            title: str = global_info["title"]
            version = Version(global_info["version"])
        except Exception:
            return "<invalid>", Version("0.0.0")
        else:
            return title, version
        
    def _read_component_definitions(self, data: typing.Any) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
        try:
            comps_info: typing.Dict[str, typing.Dict[str, typing.Any]] = data["components"]
        except Exception:
            return {}
        else:
            return comps_info
        
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def version(self) -> Version:
        return self._version

    def get_components(self) -> typing.List[str]:
        return list(self._components.keys())
    
    def get_component(self, appid: str) -> typing.Dict[str, typing.Any]:
        if appid in self._components:
            return self._components[appid]
        else:
            return {
                "name": "<invalid>",
                "directory": "",
            }
