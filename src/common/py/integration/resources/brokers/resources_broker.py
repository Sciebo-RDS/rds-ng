import abc

from ...authorization.strategies import (
    AuthorizationStrategy,
    create_authorization_strategy,
)
from ....component import BackendComponent
from ....core import logging
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.resource import ResourcesList
from ....data.entities.user import UserToken
from ....services import Service


class ResourcesBroker(abc.ABC):
    """
    Base class for all resources brokers.

    Notes:
        Brokers report errors through raising exceptions (usually *RuntimeError*).
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        broker: str,
        *,
        user_token: UserToken,
        auth_token: AuthorizationToken | None = None,
        default_root: str = "",
    ):
        """
        Args:
            comp: The global component.
            svc: The service to use for message sending.
            broker: The broker identifier.
            user_token: The user token.
            auth_token: An optional authorization token.
            default_root: The default root path (overrides the globally configured root).
        """
        self._component = comp

        self._broker = broker

        self._user_token = user_token
        self._auth_token = auth_token
        self._auth_strategy = (
            self._create_auth_strategy(svc, auth_token.strategy)
            if svc is not None and auth_token is not None
            else None
        )

        self._default_root = default_root

    @abc.abstractmethod
    def list_resources(
        self,
        root: str,
        include_folders: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> ResourcesList: ...

    def _create_auth_strategy(
        self, svc: Service, strategy: str
    ) -> AuthorizationStrategy | None:
        try:
            return create_authorization_strategy(
                self._component,
                svc,
                strategy,
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.warning(
                f"An error occurred while creating an authorization strategy for broker {self._broker}",
                scope="integration",
                strategy=strategy,
                error=str(exc),
            )
            return None

    def _replace_user_token_placeholders(self, s: str) -> str:
        s = s.replace("{USER_ID}", self._user_token.user_id)
        s = s.replace("{USER_NAME}", self._user_token.user_name)
        s = s.replace("{SYSTEM_ID}", self._user_token.system_id)
        s = s.replace("{ACCESS_ID}", self._user_token.access_id)

        return s

    def _resolve_root(self, root: str) -> str:
        root_path = root if root != "" else self._default_root
        if root_path == "":
            from ....settings.integration_setting_ids import IntegrationSettingIDs

            root_path = self._component.data.config.value(
                IntegrationSettingIDs.DEFAULT_ROOT_PATH
            )
        return root_path

    @property
    def broker(self) -> str:
        """
        The broker identifier.
        """
        return self._broker

    @property
    def has_authorization(self) -> bool:
        """
        Whether the broker has valid authorization information.
        """
        return self._auth_strategy is not None and self._auth_token is not None
