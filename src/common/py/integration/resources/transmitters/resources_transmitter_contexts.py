import typing
from dataclasses import dataclass

from ..brokers import ResourcesBrokerTunnel
from ....data.entities.resource import Resource, ResourcesList


@dataclass(kw_only=True)
class ResourcesTransmitterContext:
    """
    Internal data stored by the `ResourcesTransmitter`.

    Attributes:
        prepared: Whether the context has been prepared.
        resources: List of all available resources.
        download_list: List of all resources to download.
        download_index: The currently active download as its index in `download_list`.
    """

    prepared: bool = False

    resources: ResourcesList | None = None

    download_list: typing.List[Resource] | None = None
    download_index: int = 0
    download_failed: bool = False

    def begin_downloads(self, resources: typing.List[Resource]) -> None:
        self.download_list = resources
        self.download_index = 0
        self.download_failed = False

    @property
    def all_downloads_done(self) -> bool:
        """
        Checks if the entire list of downloads has been processed.
        """
        if self.download_failed:
            return True

        return (
            self.download_index >= len(self.download_list)
            if self.download_list is not None
            else True
        )


@dataclass(kw_only=True)
class ResourcesTransmitterDownloadContext:
    """
    Internal data stored by the `ResourcesTransmitter` for a single download.

    Attributes:
        resource: The resource being downloaded.
        tunnel: The tunnel used to download the resource.
    """

    resource: Resource
    tunnel: ResourcesBrokerTunnel | None = None
