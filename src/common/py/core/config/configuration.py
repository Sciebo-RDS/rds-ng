import typing
import os


class Configuration:
    """ A simple class for retrieving configuration settings. """
    def __init__(self, env_prefix: str = "RDS"):
        self._settings = {}
        self._defaults = {}
        
        self._env_prefix = env_prefix
        
    def load(self, filename: str) -> None:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                import tomllib
                self._settings = tomllib.load(f)
        else:
            raise FileNotFoundError("Configuration file doesn't exist")
        
    def add_defaults(self, defaults: typing.Dict) -> None:
        from deepmerge import always_merger
        self._defaults = always_merger.merge(self._defaults, defaults)

    def value(self, key: str) -> typing.Any:
        """ The value is first looked up in the environment variables. If not found, the loaded settings are searched.
            If that also fails, the defaults are used. In case the key is missing everywhere, an exception is raised.
        """
        default = self._traverse_dict(key.split("."), self._defaults)
        
        env_key = f"{self._env_prefix}_{key.replace('.', '_')}".upper()
        if env_key in os.environ:
            return self._convert_env_type(os.environ.get(env_key), type(default))
        
        try:
            return self._traverse_dict(key.split("."), self._settings)
        except:
            return default

    def _traverse_dict(self, path: typing.List[str], d: typing.Dict) -> typing.Any:
        d = d[path[0]]
        return d if len(path) == 1 else self._traverse_dict(path[1:], d)

    def _convert_env_type(self, value: typing.Any, target_type: typing.Type) -> typing.Any:
        if target_type == bool:
            if type(value) == str:
                value = value.casefold()
                return value == "1" or value == "yes".casefold() or value == "true".casefold()
            elif type(value) == int:
                return value >= 1

        return target_type(value)
        
