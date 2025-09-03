import abc
import typing

from .configuration import Configuration
from .. import ExtendedDictionary


class InformationFile(abc.ABC):
    """
    Access information stored in a *JSON* file, supporting overrides via environment variables.
    """

    def __init__(self, *, info_file: str, env_prefix: str):
        """
        Args:
            info_file: The JSON file to load the meta information from.
            env_prefix: The prefix for environment variable overrides.

        Raises:
            ValueError: If the information file couldn't be loaded.
        """
        import os.path

        if info_file == "" or not os.path.exists(info_file):
            raise ValueError("Invalid information file given")

        self._env_prefix = env_prefix

        with open(info_file, encoding="utf-8") as file:
            import json

            self._data = ExtendedDictionary(json.load(file))

    def _value(self, path: str, default: typing.Any = None) -> typing.Any:
        try:
            from .. import get_env_value

            env_key = self._env_name(path)
            return get_env_value(env_key, type(default))
        except:  # pylint: disable=bare-except
            pass

        return self._data.value(path, default)

    def _env_name(self, path: str) -> str:
        return f"{self._env_prefix}_{path.replace('.', '_')}".upper()
