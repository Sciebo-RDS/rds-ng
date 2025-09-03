import pathlib

from common.py.data.entities.connector import Connector, ConnectorCategoryID
from common.py.data.entities.metadata import (
    MetadataProfileContainerList,
)
from common.py.utils.config import InformationFile


class ConnectorInformation(InformationFile):
    """
    Accesses information about the connector stored in a *JSON* file.

    Notes:
        The logos and metadata profile are loaded from other external files, referenced in the information file.
    """

    def __init__(
        self,
        *,
        info_file: str = "./.config/connector-information.json",
        env_prefix: str = "RDS_CONNECTOR",
    ):
        """
        Args:
            info_file: The JSON file to load the connector information from.
            env_prefix: The prefix to use when generating the environment variable name of a setting.

        Raises:
            ValueError: If the information file couldn't be loaded.
        """
        super().__init__(info_file=info_file, env_prefix=env_prefix)

        self._connector_id, self._name, self._description, self._category = (
            self._read_general_info()
        )
        self._options = self._read_options()
        self._logos = self._load_logos()
        self._metadata_profiles = self._load_metadata_profiles()

    def _read_general_info(self) -> tuple[str, str, str, ConnectorCategoryID]:
        con_id: str = self._value("id", "")
        name: str = self._value("name", "<invalid>")
        desc: str = self._value("description", "")
        category: ConnectorCategoryID = self._value("category", "<invalid>")
        return con_id, name, desc, category

    def _read_options(self) -> Connector.Options:
        options = Connector.Options.DEFAULT
        if self._value("options.upload_once", False):
            options |= Connector.Options.UPLOAD_ONCE

        return options

    def _load_logos(self) -> Connector.Logos:
        from common.py.utils.img_conversion import convert_image_to_img_source

        logo_default: str | None = None
        logo_horizontal: str | None = None

        if (path := self._value("logos.default", "")) != "":
            logo_default = convert_image_to_img_source(path)

        if (path := self._value("logos.horizontal", "")) != "":
            logo_horizontal = convert_image_to_img_source(path)

        return Connector.Logos(logo_default, logo_horizontal)

    def _load_metadata_profiles(self) -> MetadataProfileContainerList:
        from common.py.data.entities.metadata import containers_from_folder

        if (profiles_path := self._value("metadata_profiles", "")) != "":
            return containers_from_folder(
                pathlib.PosixPath(profiles_path),
                default_category=f"connector:{self._connector_id}",
            )

        return []

    @property
    def connector_id(self) -> str:
        """
        The connector ID.
        """
        return self._connector_id

    @property
    def category(self) -> ConnectorCategoryID:
        """
        The connector category.
        """
        return self._category

    @property
    def name(self) -> str:
        """
        The connector name.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        The connector description.
        """
        return self._description

    @property
    def options(self) -> Connector.Options:
        """
        The connector options.
        """
        return self._options

    @property
    def logos(self) -> Connector.Logos:
        """
        The connector logos.
        """
        return self._logos

    @property
    def metadata_profiles(self) -> MetadataProfileContainerList:
        """
        The metadata profiles.
        """
        return self._metadata_profiles
