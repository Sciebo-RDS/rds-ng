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

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        config: FilesystemConfiguration,
        *,
        auth_token: AuthorizationToken | None = None,
    ):
        super().__init__(comp, svc, FilesystemBroker.Broker, auth_token=auth_token)

        self._config = config

    def list_resources(
        self,
        root: str,
        *,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList:
        from .....data.entities.resource import resources_list_from_syspath

        return resources_list_from_syspath(
            self._resolve_root(root),
            include_folders=include_folders,
            include_files=include_files,
            recursive=recursive,
        )

    def _resolve_root(self, root: str) -> str:
        return super()._resolve_root_path(root, self._config.root)


def create_filesystem_broker(
    comp: BackendComponent,
    svc: Service,
    config: typing.Any,
    auth_token: AuthorizationToken | None,
) -> FilesystemBroker:
    """
    Creates a new filesystem broker instance, automatically configuring it.

    Args:
        comp: The main component.
        svc: The service used for message sending.
        config: The broker configuration.
        auth_token: An optional authorization token.

    Returns:
        The newly created broker.
    """
    fs_config = FilesystemConfiguration.from_dict(config)

    return FilesystemBroker(comp, svc, fs_config, auth_token=auth_token)
