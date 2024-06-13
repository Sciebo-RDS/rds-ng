import os
import pathlib
import typing
import urllib.parse
from dataclasses import dataclass

import webdav3.client
from dataclasses_json import dataclass_json, Undefined

from .. import ResourcesBroker
from ....authorization.strategies import AuthorizationStrategy
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.resource import (
    ResourcesList,
    Resource,
    ResourceFolders,
    ResourceFiles,
)
from .....data.entities.user import UserToken
from .....services import Service
from .....utils import ensure_starts_with


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class WebdavConfiguration:
    """
    The WebDAV broker configuration.
    """

    host: str = ""
    endpoint: str = ""
    requires_auth: bool = False


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True, kw_only=True)
class WebdavResource:
    """
    A resource information object as returned by WebDAV.
    """

    path: str
    isdir: bool

    size: int | None  # Only filled for files


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
        user_token: UserToken,
        auth_token: AuthorizationToken | None = None,
    ):
        super().__init__(
            comp, svc, WebdavBroker.Broker, user_token=user_token, auth_token=auth_token
        )

        # Copy the configuration field-by-field, replacing placeholders on-the-go
        self._config = WebdavConfiguration(
            host=self._replace_user_token_placeholders(config.host),
            endpoint=ensure_starts_with(
                self._replace_user_token_placeholders(config.endpoint), "/"
            ),
            requires_auth=config.requires_auth,
        )

        self._client = self._create_webdav_client()

    def list_resources(
        self,
        root: str,
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
                        resource := self._parse_webdav_resource(child_resource)
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

        return _process_path(
            pathlib.PurePosixPath(self._resolve_root(root)), process_resource=True
        )

    def _create_webdav_client(self) -> webdav3.client.Client:
        if self._config.host == "" or self._config.endpoint == "":
            raise RuntimeError(
                "No WebDAV host or endpoint provided for client creation"
            )
        if self._config.requires_auth and not self.has_authorization:
            raise RuntimeError(
                "The WebDAV endpoint requires authorization but none was provided"
            )

        options = {
            "webdav_hostname": urllib.parse.urljoin(
                self._config.host, self._config.endpoint
            ),
        }

        if self._config.requires_auth and self.has_authorization:

            def _add_option(
                content_type: AuthorizationStrategy.ContentType, key: str
            ) -> None:
                if self._auth_strategy.provides_token_content(content_type):
                    options[key] = self._auth_strategy.get_token_content(
                        self._auth_token, content_type
                    )

            _add_option(AuthorizationStrategy.ContentType.AUTH_LOGIN, "webdav_login")
            _add_option(
                AuthorizationStrategy.ContentType.AUTH_PASSWORD, "webdav_password"
            )
            _add_option(AuthorizationStrategy.ContentType.AUTH_TOKEN, "webdav_token")

        return webdav3.client.Client(options)

    def _parse_webdav_resource(
        self, resource: typing.Dict[str, typing.Any]
    ) -> WebdavResource | None:
        try:
            resource = typing.cast(WebdavResource, WebdavResource.from_dict(resource))
            return WebdavResource(
                path=ensure_starts_with(
                    ensure_starts_with(resource.path, "/").replace(
                        self._config.endpoint, "", 1
                    ),
                    "/",
                ),
                isdir=resource.isdir,
                size=resource.size if resource.size else 0,
            )  # Return a cleaned up and standardized resource
        except:  # pylint: disable=bare-except
            return None


def create_webdav_broker(
    comp: BackendComponent,
    svc: Service,
    config: typing.Any,
    user_token: UserToken,
    auth_token: AuthorizationToken | None,
) -> WebdavBroker:
    """
    Creates a new WebDAV broker instance, automatically configuring it.

    Args:
        comp: The main component.
        svc: The service used for message sending.
        config: The broker configuration.
        user_token: The user token.
        auth_token: An optional authorization token.

    Returns:
        The newly created broker.
    """
    webdav_config: WebdavConfiguration = WebdavConfiguration.from_dict(config)

    return WebdavBroker(
        comp, svc, webdav_config, user_token=user_token, auth_token=auth_token
    )