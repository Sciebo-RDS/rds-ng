import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .. import ResourcesBroker
from .....component import BackendComponent


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class FilesystemConfiguration:
    """
    The filesystem broker configuration.
    """

    root: str = ""


class FilesystemBroker(ResourcesBroker):
    """
    Filesystem resources broker.
    """

    Broker: str = "filesystem"

    def __init__(self, comp: BackendComponent, config: FilesystemConfiguration):
        super().__init__(comp, FilesystemBroker.Broker)

        self._config = config


def create_filesystem_broker(
    comp: BackendComponent, config: typing.Any
) -> FilesystemBroker:
    """
    Creates a new filesystem broker instance, automatically configuring it.

    Args:
        comp: The main component.
        config: The broker configuration.

    Returns:
        The newly created broker.
    """
    fs_config = FilesystemConfiguration.from_dict(config)

    return FilesystemBroker(comp, fs_config)
