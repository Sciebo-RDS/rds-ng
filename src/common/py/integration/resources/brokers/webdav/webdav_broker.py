import os
import typing
import urllib.parse
from dataclasses import dataclass

import webdav3.client
from dataclasses_json import dataclass_json

from .. import ResourcesBroker
from ....authorization.strategies import AuthorizationStrategy
from .....component import BackendComponent
from .....data.entities.authorization import AuthorizationToken
from .....data.entities.resource import ResourcesList, Resource
from .....data.entities.user import UserToken
from .....services import Service


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class WebdavConfiguration:
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
            endpoint=self._replace_user_token_placeholders(config.endpoint),
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
        resources = ResourcesList(
            resource=Resource(
                filename=root,
                basename=os.path.basename(root),
                type=Resource.Type.FOLDER,
            )
        )

        # Listing is _not_ recursive and contains both files and folders
        files = self._client.list(self._resolve_root(root), get_info=True)

        # TODO: Convert files
        # TODO: Remove endpoint portion from beginning; both must begin with a / (ensure)

        #  {
        #       "created":"None",
        #       "name":"None",
        #       "size":"13378",
        #       "modified":"Fri, 07 Jun 2024 08:58:55 GMT",
        #       "etag":"\"54944d8770ddcb128282a5c7485c212b\"",
        #       "content_type":"application/vnd.oasis.opendocument.spreadsheet",
        #       "isdir":false,
        #       "path":"/remote.php/dav/files/admin/Templates/Diagram & table.ods"
        #    },

        print("------------------------", flush=True)
        print(files, flush=True)
        print("------------------------", flush=True)
        print(self._config.endpoint, flush=True)
        print("------------------------", flush=True)

        return resources

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
