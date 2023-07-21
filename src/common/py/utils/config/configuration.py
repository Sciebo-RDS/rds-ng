import typing
import os

from .setting_id import SettingID


class Configuration:
    """
    Encapsulates configuration settings and their fallback default values.
    
    Settings can be loaded from a configuration file (in *TOML* format) or provided as environment variables (see below).
    
    All settings are accessed by an identifier of type ``SettingID``, which represents settings in a path-like format;
    ``General.Debug``, for example, refers to a setting called ``Debug`` in the ``General` section.
    
    A corresponding configuration file would look like this::
    
        [General]
        Debug = True
        
    A setting identifier is translated to its corresponding environment variable name by replacing all dots (.) with underscores (_),
    prepending a prefix (defaults to *'RDS'*), as well as making everything uppercase::
    
        General.Debug -> RDS_GENERAL_DEBUG
        
    Notes:
        When accessing a setting value, a default value must *always* be present. This means that before a setting can be accessed,
        a default value must be added using ``add_defaults``.
    """
    def __init__(self, env_prefix: str = "RDS"):
        """
        Args:
            env_prefix: The prefix to use when generating the environment variable name of a setting.
        """
        self._settings_file = ""
        
        self._settings = {}
        self._defaults = {}
        
        self._env_prefix = env_prefix
        
    def load(self, filename: str) -> None:
        """
        Loads settings from a *TOML* file.
        
        Args:
            filename: The file to load.
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist or couldn't be opened.
        """
        self._settings_file = filename
        
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                import tomllib
                self._settings = tomllib.load(f)
        else:
            raise FileNotFoundError("Configuration file doesn't exist")
        
    def add_defaults(self, defaults: typing.Dict[SettingID, typing.Any]) -> None:
        """
        Adds default values for settings, merging the new defaults into the existing ones.
        
        Args:
            defaults: A dictionary containing the new default values.
            
        Notes:
            It is always necessary to add a default value for a setting before accessing it.
        """
        from deepmerge import always_merger
        for key, value in defaults.items():
            d = {}
            self._unfold_dict_item(key.split(), d, value)
            self._defaults = always_merger.merge(self._defaults, d)

    def value(self, key: SettingID) -> typing.Any:
        """
        Gets the value of a setting.
        
        The value is first looked up in the environment variables. If not found, the loaded settings are searched.
        If that also fails, the defaults are used.
        
        Args:
            key: The identifier of the setting.

        Returns:
            The value of the setting.
            
        Raises:
            KeyError: The setting identifier was not found in the defaults.
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
        """
        The name of the currently loaded settings file.
        """
        return self._settings_file
