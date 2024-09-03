import json
import typing

import requests

from common.py.component import BackendComponent
from common.py.core import logging
from common.py.core.messaging import Channel
from common.py.data.entities.authorization import AuthorizationToken
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.user import UserToken
from common.py.integration.authorization.strategies import (
    AuthorizationStrategy,
    create_authorization_strategy,
)
from common.py.integration.execution import AuthorizedExecutor
from common.py.services import Service


class RequestsExecutor(AuthorizedExecutor):
    """
    Executes HTTP API calls via `requests`. It supports automatic authorization and attempt retries.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        connector_instance: ConnectorInstanceID,
        auth_channel: Channel,
        user_token: UserToken,
        base_url: str,
        max_attempts: int = 1,
        attempts_delay: float = 3.0,
        trailing_slashes: bool = True,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            connector_instance: The connector instance ID.
            auth_channel: Channel to fetch authorization tokens from.
            user_token: The user token.
            base_url: The base URL for all requests.
            max_attempts: The number of attempts for each operation; cannot be less than 1.
            attempts_delay: The delay (in seconds) between each attempt.
            trailing_slashes: Add trailing slashes to URLs.
        """
        from common.py.data.entities.authorization import (
            get_connector_instance_authorization_id,
        )
        from common.py.settings import NetworkSettingIDs

        super().__init__(
            comp,
            svc,
            auth_channel=auth_channel,
            auth_id=get_connector_instance_authorization_id(connector_instance),
            user_token=user_token,
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

        self._base_url = base_url.rstrip("/")
        self._trailing_slashes = trailing_slashes

        self._request_timeout = comp.data.config.value(
            NetworkSettingIDs.EXTERNAL_REQUESTS_TIMEOUT
        )

    def get(
        self, session: requests.Session, path: typing.List[str] | str, *args, **kwargs
    ) -> requests.Response:
        """
        Performs a GET request.

        Args:
            session: The session to use.
            path: The path as an array.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The response object.
        """
        return session.get(
            self._url(path), timeout=self._request_timeout, *args, **kwargs
        )

    def post(
        self,
        session: requests.Session,
        path: typing.List[str] | str,
        *args,
        **kwargs,
    ) -> requests.Response:
        """
        Performs a POST request.

        Args:
            session: The session to use.
            path: The path as an array.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The response object.
        """
        return session.post(
            self._url(path),
            *args,
            timeout=self._request_timeout,
            **kwargs,
        )

    def put(
        self,
        session: requests.Session,
        path: typing.List[str] | str,
        *args,
        **kwargs,
    ) -> requests.Response:
        """
        Performs a PUT request.

        Args:
            session: The session to use.
            path: The path as an array.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The response object.
        """
        return session.put(
            self._url(path),
            *args,
            timeout=self._request_timeout,
            **kwargs,
        )

    def delete(
        self,
        session: requests.Session,
        path: typing.List[str] | str,
        *args,
        **kwargs,
    ) -> requests.Response:
        """
        Performs a DELETE request.

        Args:
            session: The session to use.
            path: The path as an array.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The response object.
        """
        return session.delete(
            self._url(path),
            *args,
            timeout=self._request_timeout,
            **kwargs,
        )

    def _url(self, path: typing.List[str] | str) -> str:
        if isinstance(path, str):
            return path
        else:
            parts = [self._base_url, *path]
            return "/".join(parts) + ("/" if self._trailing_slashes else "")

    def _execute(
        self,
        *,
        cb_exec: typing.Callable[..., typing.Any],
        cb_done: typing.Callable[[typing.Any], None],
        cb_failed: typing.Callable[[str], None],
        cb_retry: typing.Callable[..., None] | None = None,
        **kwargs,
    ) -> None:
        # Get the authorization token for the connector system, since we need to access its resources.
        # Once received, the actual execution can happen.
        def _prepare_execute(
            auth_token: AuthorizationToken | None,
        ) -> typing.Dict[str, typing.Any]:
            return {"session": self._create_session(auth_token=auth_token)}

        super()._execute(
            cb_exec=cb_exec,
            cb_done=cb_done,
            cb_failed=cb_failed,
            cb_prepare=_prepare_execute,
            cb_retry=cb_retry,
            **kwargs,
        )

    def _create_session(
        self, *, auth_token: AuthorizationToken | None
    ) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                "Accept": "*/*",
                "Accept-Charset": "utf-8",
                "Content-Type": "application/json",
                "User-Agent": f"{self._component.data.title} {self._component.data.version}",
            }
        )

        if (
            auth_strategy := (
                self._create_auth_strategy(auth_token.strategy, auth_token=auth_token)
                if self._service is not None and auth_token is not None
                else None
            )
        ) is not None:
            if auth_strategy.provides_token_content(
                AuthorizationStrategy.ContentType.AUTH_TOKEN
            ):
                session.headers.update(
                    {
                        "Authorization": f"Bearer {auth_strategy.get_token_content(auth_token, AuthorizationStrategy.ContentType.AUTH_TOKEN)}"
                    }
                )
            elif auth_strategy.provides_token_content(
                AuthorizationStrategy.ContentType.AUTH_LOGIN
            ) and auth_strategy.provides_token_content(
                AuthorizationStrategy.ContentType.AUTH_PASSWORD
            ):
                session.auth = (
                    auth_strategy.get_token_content(
                        auth_token, AuthorizationStrategy.ContentType.AUTH_LOGIN
                    ),
                    auth_strategy.get_token_content(
                        auth_token, AuthorizationStrategy.ContentType.AUTH_PASSWORD
                    ),
                )

        return session

    def _create_auth_strategy(
        self,
        strategy: str,
        *,
        auth_token: AuthorizationToken,
    ) -> AuthorizationStrategy | None:
        try:
            return create_authorization_strategy(
                self._component,
                self._service,
                strategy,
                user_token=self._user_token,
                auth_token=auth_token,
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.warning(
                f"An error occurred while creating an authorization strategy for requests execution",
                scope="integration",
                strategy=strategy,
                error=str(exc),
            )
            return None
