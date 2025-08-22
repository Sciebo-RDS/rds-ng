import pathlib
import typing

from common.py.data.entities.connector import Connector, ConnectorCategoryID
from common.py.data.entities.metadata import (
    MetadataProfileContainer,
    MetadataProfileContainerList,
)
from common.py.data.entities.properties import ProfileMetadata, PropertyProfile
from common.py.utils.img_conversion import convert_image_to_img_source


class ConnectorInformation:
    """
    Accesses information about the connector stored in a *JSON* file.

    The JSON file needs to be structured like this::

        {
            "name": "Zenodo",
            "description": "Connector for Zenodo",
            "category": "repository",
            "options": {
                "upload_once": true
            },
            "logos": {
                "default": "/some/file.png",
                "horizontal": "/some/other/file.png"
            },
            "metadata_profiles": "/the/profiles_dir"
        }

    Notes:
        The logos and metadata profile are loaded from other external files, referenced in the information file.
    """

    def __init__(
        self,
        connector_id: str,
        info_file: str = "./.config/connector-information.json",
    ):
        """
        Args:
            connector_id: The identifier of the connector.
            info_file: The JSON file to load the connector information from.

        Raises:
            ValueError: If the information file couldn't be loaded.
        """
        import os.path

        self._connector_id = connector_id

        if info_file == "" or not os.path.exists(info_file):
            raise ValueError("Invalid connector information file given")

        with open(info_file, encoding="utf-8") as file:
            import json

            data = json.load(file)
            self._name, self._description, self._category = self._read_general_info(
                data
            )
            self._options = self._read_options(data)
            self._logos = self._load_logos(data)
            self._metadata_profiles = self._load_metadata_profiles(data)

    def _read_general_info(
        self, data: typing.Any
    ) -> tuple[str, str, ConnectorCategoryID]:
        try:
            name: str = data["name"]
            desc: str = data["description"]
            category: ConnectorCategoryID = data["category"]
        except Exception:  # pylint: disable=broad-exception-caught
            return "<invalid>", "<invalid>", "<invalid>"

        return name, desc, category

    def _read_options(self, data: typing.Any) -> Connector.Options:
        try:
            options = Connector.Options.DEFAULT
            options_data = data["options"]

            if "upload_once" in options_data and options_data["upload_once"] is True:
                options |= Connector.Options.UPLOAD_ONCE
        except Exception:  # pylint: disable=broad-exception-caught
            return Connector.Options.DEFAULT

        return options

    def _load_logos(self, data: typing.Any) -> Connector.Logos:
        try:
            logo_default = None
            logo_horizontal = None

            logo_files = data["logos"]

            if "default" in logo_files and (filename := logo_files["default"]) != "":
                logo_default = convert_image_to_img_source(filename)

            if (
                "horizontal" in logo_files
                and (filename := logo_files["horizontal"]) != ""
            ):
                logo_horizontal = convert_image_to_img_source(filename)
        except:  # pylint: disable=bare-except
            return Connector.Logos()

        return Connector.Logos(logo_default, logo_horizontal)

    def _load_metadata_profiles(self, data: typing.Any) -> MetadataProfileContainerList:
        from common.py.data.entities.metadata import containers_from_folder

        return containers_from_folder(
            pathlib.PosixPath(data["metadata_profiles"]),
            default_category=f"connector:{self._connector_id}",
        )

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
