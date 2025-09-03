import typing

from semantic_version import Version

from ..utils.config import InformationFile


class MetaInformation(InformationFile):
    """
    Accesses meta information about the entire project stored in a *JSON* file.
    """

    def __init__(
        self,
        *,
        info_file: str = "/config/meta-information.json",
        env_prefix: str = "RDS_META"
    ):
        """
        Args:
            info_file: The JSON file to load the meta information from.
            env_prefix: The prefix to use when generating the environment variable name of a setting.

        Raises:
            ValueError: If the information file couldn't be loaded.
        """
        super().__init__(info_file=info_file, env_prefix=env_prefix)

        self._title, self._version = self._read_global_info()

    def _read_global_info(self) -> tuple[str, Version]:
        title: str = self._value("global.title", "<invalid>")
        version: Version = Version(self._value("global.version", "0.0.0"))
        return title, version

    @property
    def title(self) -> str:
        """
        The project title.
        """
        return self._title

    @property
    def version(self) -> Version:
        """
        The project version (see https://semver.org).
        """
        return self._version
