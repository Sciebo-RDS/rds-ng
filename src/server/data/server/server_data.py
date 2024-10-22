import pathlib

from common.py.data.entities.metadata import (
    containers_from_folder,
    MetadataProfileContainerList,
)


class ServerData:
    """
    Simple class holding some static server data.
    """

    def __init__(self):
        self._profile_containers = self._load_profile_containers()

    def _load_profile_containers(self) -> MetadataProfileContainerList:
        return containers_from_folder(pathlib.PosixPath("../common/assets/profiles"))

    @property
    def profile_containers(self) -> MetadataProfileContainerList:
        """
        List of all global metadata profile containers.
        """
        return self._profile_containers
