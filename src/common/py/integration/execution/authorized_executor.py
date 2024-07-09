import abc
import threading
import typing

from ...api import GetAuthorizationTokenCommand, GetAuthorizationTokenReply
from ...component import BackendComponent
from ...core.messaging import Channel
from ...data.entities.authorization import AuthorizationToken
from ...data.entities.user import UserToken
from ...services import Service
from ...utils.func import attempt


class AuthorizedExecutor(abc.ABC):
    """
    Class to execute arbitrary functions that require an authorization token. It also supports multiple attempts to execute the function.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        auth_channel: Channel,
        auth_id: str,
        user_token: UserToken,
        max_attempts: int = 1,
        attempts_delay: float = 3.0,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            auth_channel: Channel to fetch authorization tokens from.
            auth_id: The ID of the authorization token to fetch.
            user_token: The user token.
            max_attempts: The number of attempts for each operation; cannot be less than 1.
            attempts_delay: The delay (in seconds) between each attempt.
        """
        from ...settings import NetworkSettingIDs

        self._component = comp
        self._service = svc
        self._auth_channel = auth_channel
        self._auth_id = auth_id

        self._user_token = user_token

        self._max_attempts = max(1, max_attempts)
        self._attempts_delay = attempts_delay

        self._api_key = self._component.data.config.value(NetworkSettingIDs.API_KEY)
        self._lock = threading.RLock()

    def _execute(
        self,
        *,
        cb_exec: typing.Callable[..., typing.Any],
        cb_done: typing.Callable[[typing.Any], None],
        cb_failed: typing.Callable[[str], None],
        cb_prepare: (
            typing.Callable[
                [AuthorizationToken | None], typing.Dict[str, typing.Any] | None
            ]
            | None
        ) = None,
        cb_retry: typing.Callable[..., None] | None = None,
        **kwargs,
    ) -> None:
        def _get_auth_token_done(
            reply: GetAuthorizationTokenReply, success: bool, _
        ) -> None:
            nonlocal kwargs

            with self._lock:
                try:
                    if callable(cb_prepare):
                        exargs = cb_prepare(reply.auth_token if success else None)
                        if exargs is not None:
                            kwargs |= exargs
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    cb_failed(str(exc))
                else:
                    attempt_success, result = attempt(
                        cb_exec,
                        cb_retry=cb_retry,
                        cb_fail=lambda e: cb_failed(str(e)),
                        attempts=self._max_attempts,
                        delay=self._attempts_delay,
                        **kwargs,
                    )
                    if attempt_success:
                        cb_done(result)

        def _get_auth_token_failed(_, msg: str) -> None:
            with self._lock:
                cb_failed(msg)

        GetAuthorizationTokenCommand.build(
            self._service.message_builder,
            user_id=self._user_token.user_id,
            auth_id=self._auth_id,
            api_key=self._api_key,
        ).done(_get_auth_token_done).failed(_get_auth_token_failed).emit(
            self._auth_channel
        )
