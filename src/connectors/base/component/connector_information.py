import typing

from common.py.data.entities.connector import Connector, ConnectorMetadataProfile


class ConnectorInformation:
    """
    Accesses information about the connector stored in a *JSON* file.

    The JSON file needs to be structured like this::

        {
            "name": "Zenodo",
            "description": "Connector for Zenodo",
            "logos": {
                "default": "/some/file.png",
                "horizontal": "/some/other/file.png"
            },
            "metadata_profile": "/the/profile_file.json"
        }

    Notes:
        The logos and metadata profile are loaded from other files.
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
            self._name, self._description = self._read_general_info(data)
            # TODO: Logos, metadata profile

    def _read_general_info(self, data: typing.Any) -> tuple[str, str]:
        try:
            name: str = data["name"]
            desc: str = data["description"]
        except Exception:  # pylint: disable=broad-exception-caught
            return "<invalid>", "<invalid>"

        return name, desc

    @property
    def connector_id(self) -> str:
        return self._connector_id

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
        raise NotImplementedError()

    @property
    def metadata_profile(self) -> ConnectorMetadataProfile:
        """
        The metadata profile.
        """
        raise NotImplementedError()
