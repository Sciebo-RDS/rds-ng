import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .. import ResourcesBroker
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.resource import ResourcesList
from .....services import Service


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

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        config: WebdavConfiguration,
        *,
        auth_token: AuthorizationToken | None = None,
    ):
        super().__init__(comp, svc, WebdavBroker.Broker, auth_token=auth_token)

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


def create_webdav_broker(
    comp: BackendComponent,
    svc: Service,
    config: typing.Any,
    auth_token: AuthorizationToken | None,
) -> WebdavBroker:
    """
    Creates a new WebDAV broker instance, automatically configuring it.

    Args:
        comp: The main component.
        svc: The service used for message sending.
        config: The broker configuration.
        auth_token: An optional authorization token.

    Returns:
        The newly created broker.
    """
    webdav_config: WebdavConfiguration = WebdavConfiguration.from_dict(config)

    return WebdavBroker(comp, svc, webdav_config, auth_token=auth_token)
