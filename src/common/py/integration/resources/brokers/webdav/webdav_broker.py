import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .. import ResourcesBroker
from .....component import BackendComponent
from .....data.entities.resource import ResourcesList


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class WebdavConfiguration:
    """
    The WebDAV broker configuration.
    """

    root: str = ""


class WebdavBroker(ResourcesBroker):
    """
    WebDAV resources broker.
    """

    Broker: str = "webdav"

    def __init__(self, comp: BackendComponent, config: WebdavConfiguration):
        super().__init__(comp, WebdavBroker.Broker)

        self._config = config

    def list_resources(
        self,
        root: str,
        *,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList:
        # TODO
        pass

    def _resolve_root(self, root: str) -> str:
        # TODO
        return super()._resolve_root_path(root, self._config.root)


def create_webdav_broker(comp: BackendComponent, config: typing.Any) -> WebdavBroker:
    """
    Creates a new WebDAV broker instance, automatically configuring it.

    Args:
        comp: The main component.
        config: The broker configuration.

    Returns:
        The newly created broker.
    """
    webdav_config = WebdavConfiguration.from_dict(config)

    return WebdavBroker(comp, webdav_config)
