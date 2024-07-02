import pathlib
import typing
import urllib.parse
from dataclasses import dataclass
from http import HTTPStatus

import webdav3.client
from dataclasses_json import dataclass_json

from .webdav_utils import parse_webdav_resource
from .. import ResourcesBroker, ResourcesBrokerTunnel
from ....authorization.strategies import AuthorizationStrategy
from .....component import BackendComponent
from .....core import logging
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.resource import (
    Resource,
    ResourceFiles,
    ResourceFolders,
    ResourcesList,
)
from .....data.entities.user import UserToken
from .....services import Service
from .....utils import ensure_starts_with


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class WebdavBrokerConfiguration:
    """
    The WebDAV broker configuration.
    """

    host: str = ""
    endpoint: str = ""
    requires_auth: bool = False


class WebdavBroker(ResourcesBroker):
    """
    WebDAV resources broker.
    """

    Broker: str = "webdav"

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        config: WebdavBrokerConfiguration,
        *,
        user_token: UserToken,
        auth_token: AuthorizationToken | None = None,
        auth_token_refresh: bool = True,
    ):
        super().__init__(
            comp,
            svc,
            WebdavBroker.Broker,
            user_token=user_token,
            auth_token=auth_token,
            auth_token_refresh=auth_token_refresh,
        )

        # Copy the configuration field-by-field, replacing placeholders on-the-go
        self._config = WebdavBrokerConfiguration(
            host=self._replace_user_token_placeholders(config.host),
            endpoint=ensure_starts_with(
                self._replace_user_token_placeholders(config.endpoint), "/"
            ),
            requires_auth=config.requires_auth,
        )

        self._client = self._create_webdav_client(comp)

    def list_resources(
        self,
        root: str,
        *,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList:
        root_path = pathlib.PurePosixPath(self._resolve_root(root))
        return self._execute_request(
            lambda: self._execute_list_resources(
                root_path,
                include_folders=include_folders,
                include_files=include_files,
                recursive=recursive,
            ),
            resource=root_path,
            refresh_unauthorized_token=self._auth_token_refresh,
        )

    def download_resource(
        self,
        resource: str,
        *,
        tunnel: ResourcesBrokerTunnel,
    ) -> None:
        resource = pathlib.PurePosixPath(self._resolve_root(resource))
        self._execute_request(
            lambda: self._execute_download_resource(resource, tunnel=tunnel),
            resource=resource,
            refresh_unauthorized_token=self._auth_token_refresh,
        )

    def _execute_request(
        self,
        cb: typing.Callable[[], typing.Any],
        *,
        resource: pathlib.PurePosixPath,
        refresh_unauthorized_token: bool,
    ) -> typing.Any:
        try:
            return cb()
        except webdav3.client.ResponseErrorCode as exc:
            # If the request throws a 401 (unauthorized), first try to refresh the auth token and re-do the call
            # If the second try fails, the auth token is removed and an error is thrown
            if exc.code == HTTPStatus.UNAUTHORIZED and refresh_unauthorized_token:
                try:
                    self._auth_strategy.refresh_authorization(self._auth_token)
                    return self._execute_request(
                        cb, resource=resource, refresh_unauthorized_token=False
                    )
                except:  # pylint: disable=bare-except
                    pass

            logging.warning(
                "Resource access error - removing authorization token",
                scope="webdav",
                resource=str(resource),
                error=str(exc),
            )

            # TODO: Less harsh
            self._revoke_auth_token()

            raise exc

    def _execute_list_resources(
        self,
        root: pathlib.PurePosixPath,
        *,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList:
        def _process_path(
            root_path: pathlib.PurePosixPath, *, process_resource: bool
        ) -> ResourcesList:
            folders: ResourceFolders = []
            files: ResourceFiles = []
            total_size: int = 0

            if process_resource:
                for child_resource in self._client.list(str(root_path), get_info=True):
                    if (
                        resource := parse_webdav_resource(
                            child_resource, self._config.endpoint
                        )
                    ) is not None:
                        child_path = pathlib.PurePosixPath(resource.path)
                        if (
                            child_path == root_path
                        ):  # WebDAV enumerates the current path, so we need to avoid endless recursion
                            continue

                        if resource.isdir and include_folders:
                            path_resources = _process_path(
                                child_path, process_resource=recursive
                            )
                            folders.append(path_resources)
                            total_size += path_resources.resource.size
                        elif not resource.isdir and include_files:
                            files.append(
                                Resource(
                                    filename=str(child_path),
                                    basename=child_path.name,
                                    type=Resource.Type.FILE,
                                    size=resource.size,
                                )
                            )
                            total_size += resource.size

            return ResourcesList(
                resource=Resource(
                    filename=str(root_path),
                    basename=root_path.name if root_path.name else "All files",
                    type=Resource.Type.FOLDER,
                    size=total_size,
                ),
                folders=folders,
                files=files,
            )

        return _process_path(root, process_resource=True)

    def _execute_download_resource(
        self,
        resource: pathlib.PurePosixPath,
        *,
        tunnel: ResourcesBrokerTunnel,
    ) -> None:
        total_size = int(self._client.info(str(resource))["size"])
        tunnel.transfer_begin(resource, total_size)

        try:
            self._client.download_from(
                tunnel.write_buffer,
                str(resource),
                lambda current, _: tunnel.transfer_progress(
                    resource, min(current, total_size), total_size
                ),
            )

            tunnel.transfer_done(resource, total_size)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            tunnel.transfer_failed(resource, str(exc))
            raise exc

    def _create_webdav_client(self, comp: BackendComponent) -> webdav3.client.Client:
        if self._config.host == "" or self._config.endpoint == "":
            raise RuntimeError(
                "No WebDAV host or endpoint provided for client creation"
            )
        if self._config.requires_auth and not self.has_authorization:
            raise RuntimeError(
                "The WebDAV endpoint requires authorization but none was provided"
            )

        from .....settings import NetworkSettingIDs

        options = {
            "webdav_hostname": urllib.parse.urljoin(
                self._config.host, self._config.endpoint
            ),
            "webdav_timeout": comp.data.config.value(
                NetworkSettingIDs.EXTERNAL_REQUESTS_TIMEOUT
            ),
        }

        def _add_option(
            content_type: AuthorizationStrategy.ContentType, key: str
        ) -> None:
            if self._auth_strategy.provides_token_content(content_type):
                options[key] = self._auth_strategy.get_token_content(
                    self._auth_token, content_type
                )

        if self._config.requires_auth and self.has_authorization:
            _add_option(AuthorizationStrategy.ContentType.AUTH_LOGIN, "webdav_login")
            _add_option(
                AuthorizationStrategy.ContentType.AUTH_PASSWORD, "webdav_password"
            )
            _add_option(AuthorizationStrategy.ContentType.AUTH_TOKEN, "webdav_token")

        return webdav3.client.Client(options)


def create_webdav_broker(
    comp: BackendComponent,
    svc: Service,
    config: typing.Any,
    *,
    user_token: UserToken,
    auth_token: AuthorizationToken | None = None,
    auth_token_refresh: bool = True,
) -> WebdavBroker:
    """
    Creates a new WebDAV broker instance, automatically configuring it.

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
    webdav_config: WebdavBrokerConfiguration = WebdavBrokerConfiguration.from_dict(
        config
    )

    return WebdavBroker(
        comp,
        svc,
        webdav_config,
        user_token=user_token,
        auth_token=auth_token,
        auth_token_refresh=auth_token_refresh,
    )
