import json
import typing

from common.py.data.entities.connector import Connector, ConnectorMetadataProfile
from common.py.utils.img_conversion import convert_image_to_img_source


class ConnectorInformation:
    """
    Accesses information about the connector stored in a *JSON* file.

    The JSON file needs to be structured like this::

        {
            "type": "repository",
            "name": "Zenodo",
            "description": "Connector for Zenodo",
            "logos": {
                "default": "/some/file.png",
                "horizontal": "/some/other/file.png"
            },
            "metadata_profile": "/the/profile_file.json"
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
            self._type, self._name, self._description = self._read_general_info(data)
            self._logos = self._load_logos(data)
            self._metadata_profile = self._load_metadata_profile(data)

    def _read_general_info(self, data: typing.Any) -> tuple[Connector.Type, str, str]:
        try:
            ctype: Connector.Type = data["type"]
            name: str = data["name"]
            desc: str = data["description"]
        except Exception:  # pylint: disable=broad-exception-caught
            return "<invalid>", "<invalid>", "<invalid>"

        return ctype, name, desc

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

    def _load_metadata_profile(self, data: typing.Any) -> ConnectorMetadataProfile:
        try:
            with open(data["metadata_profile"], encoding="utf-8") as file:
                return json.load(file)
        except:  # pylint: disable=bare-except
            return {}

    @property
    def connector_id(self) -> str:
        return self._connector_id

    @property
    def type(self) -> Connector.Type:
        return self._type

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
    def logos(self) -> Connector.Logos:
        """
        The connector logos.
        """
        return self._logos

    @property
    def metadata_profile(self) -> ConnectorMetadataProfile:
        """
        The metadata profile.
        """
        return self._metadata_profile