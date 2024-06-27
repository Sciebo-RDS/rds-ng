import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .. import ResourcesBroker
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.resource import ResourcesList
from .....data.entities.user import UserToken
from .....services import Service


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class FilesystemBrokerConfiguration:
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
        config: FilesystemBrokerConfiguration,
        *,
        user_token: UserToken,
        auth_token: AuthorizationToken | None = None,
        auth_token_refresh: bool = True,
    ):
        super().__init__(
            comp,
            svc,
            FilesystemBroker.Broker,
            user_token=user_token,
            auth_token=auth_token,
            auth_token_refresh=auth_token_refresh,
            default_root=config.root,
        )

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


def create_filesystem_broker(
    comp: BackendComponent,
    svc: Service,
    config: typing.Any,
    *,
    user_token: UserToken,
    auth_token: AuthorizationToken | None = None,
    auth_token_refresh: bool = True,
) -> FilesystemBroker:
    """
    Creates a new filesystem broker instance, automatically configuring it.

    Args:
        comp: The main component.
        svc: The service used for message sending.
        config: The broker configuration.
        user_token: The user token.
        auth_token: An optional authorization token.
        auth_token_refresh: Whether expired authorization tokens should be refreshed automatically.

    Returns:
        The newly created broker.
    """
    fs_config = FilesystemBrokerConfiguration.from_dict(config)

    return FilesystemBroker(
        comp,
        svc,
        fs_config,
        user_token=user_token,
        auth_token=auth_token,
        auth_token_refresh=auth_token_refresh,
    )
