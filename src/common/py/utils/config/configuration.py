import typing
import os

from .setting_id import SettingID


class Configuration:
    """ A simple class for retrieving configuration settings. """
    def __init__(self, env_prefix: str = "RDS"):
        self._settings_file = ""
        
        self._settings = {}
        self._defaults = {}
        
        self._env_prefix = env_prefix
        
    def load(self, filename: str) -> None:
        self._settings_file = filename
        
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                import tomllib
                self._settings = tomllib.load(f)
        else:
            raise FileNotFoundError("Configuration file doesn't exist")
        
    def add_defaults(self, defaults: typing.Dict[SettingID, typing.Any]) -> None:
        from deepmerge import always_merger
        for key, value in defaults.items():
            d = {}
            self._unfold_dict_item(key.split(), d, value)
            self._defaults = always_merger.merge(self._defaults, d)

    def value(self, key: SettingID) -> typing.Any:
        """ The value is first looked up in the environment variables. If not found, the loaded settings are searched.
            If that also fails, the defaults are used. In case the key is missing everywhere, an exception is raised.
        """
        default = self._traverse_dict(key.split(), self._defaults)
        
        env_key = key.env_name(self._env_prefix)
        if env_key in os.environ:
            return self._convert_env_type(os.environ.get(env_key), type(default))
        
        try:
            return self._traverse_dict(key.split(), self._settings)
        except:
            return default
    
    def _traverse_dict(self, path: typing.List[str], d: typing.Dict) -> typing.Any:
        d = d[path[0]]
        return d if len(path) == 1 else self._traverse_dict(path[1:], d)
    
    def _unfold_dict_item(self, path: typing.List[str], d: typing.Dict, v: typing.Any) -> None:
        if len(path) == 1:
            d[path[0]] = v
        else:
            if not path[0] in d:
                d[path[0]] = {}
            
            d = d[path[0]]
            self._unfold_dict_item(path[1:], d, v)

    def _convert_env_type(self, value: typing.Any, target_type: type) -> typing.Any:
        if target_type == bool:
            if type(value) == str:
                value = value.casefold()
                return value == "1" or value == "yes".casefold() or value == "true".casefold()
            elif type(value) == int:
                return value >= 1

        return target_type(value)
        
    @property
    def settings_file(self) -> str:
        return self._settings_file
