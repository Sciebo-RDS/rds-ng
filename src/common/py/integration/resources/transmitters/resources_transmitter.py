import threading
import typing

from .resources_transmitter_context import ResourcesTransmitterContext
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import create_resources_broker, ResourcesBroker, ResourcesBrokerTunnel
from ....api import GetAuthorizationTokenCommand, GetAuthorizationTokenReply
from ....component import BackendComponent
from ....core.messaging import Channel
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.project import Project
from ....data.entities.resource import (
    files_list_from_resources_list,
    Resource,
    ResourcesBrokerToken,
    ResourcesList,
)
from ....data.entities.user import UserToken
from ....services import Service
from ....utils import attempt, ExecutionCallbacks

TransmissionPrepareDoneCallback = typing.Callable[[ResourcesList], None]
TransmissionPrepareFailCallback = typing.Callable[[str], None]
TransmissionDownloadDoneCallback = typing.Callable[[], None]
TransmissionDownloadFailCallback = typing.Callable[[str], None]


class ResourcesTransmitter:
    """
    Main class to transmit resources.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        auth_channel: Channel,
        user_token: UserToken,
        broker_token: ResourcesBrokerToken,
        max_attempts: int = 1,
        attempts_delay: float = 3.0,
        auth_token_refresh: bool = True,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            user_token: The user token.
            broker_token: The broker token.
            auth_channel: Channel to fetch authorization tokens from.
            max_attempts: The number of attempts for each operation; cannot be less than 1.
            attempts_delay: The delay (in seconds) between each attempt.
            auth_token_refresh: Whether expired authorization tokens should be refreshed automatically.
        """
        from ....settings import NetworkSettingIDs

        self._component = comp
        self._service = svc
        self._auth_channel = auth_channel

        self._user_token = user_token
        self._broker_token = broker_token

        self._max_attempts = max(1, max_attempts)
        self._attempts_delay = attempts_delay

        self._auth_token_refresh = auth_token_refresh

        self._prepare_callbacks = ExecutionCallbacks[
            TransmissionPrepareDoneCallback, TransmissionPrepareFailCallback
        ]()
        self._download_callbacks = ExecutionCallbacks[
            TransmissionDownloadDoneCallback, TransmissionDownloadFailCallback
        ]()

        self._context = ResourcesTransmitterContext()

        self._api_key = self._component.data.config.value(NetworkSettingIDs.API_KEY)
        self._lock = threading.RLock()

    def prepare(self, project: Project) -> None:
        """
        Prepares the transmission of resources; must always be called before any other method.

        Args:
            project: The project to work on.
        """

        def _prepare(broker: ResourcesBroker) -> None:
            self._context.resources = broker.list_resources(project.resources_path)
            self._context.prepared = True

        self._execute(
            cb_exec=_prepare,
            cb_done=lambda: self._prepare_callbacks.invoke_done_callbacks(
                self._context.resources
            ),
            cb_failed=lambda reason: self._prepare_callbacks.invoke_fail_callbacks(
                reason
            ),
        )

    def prepare_done(self, callback: TransmissionPrepareDoneCallback) -> typing.Self:
        """
        Adds a callback for finished preparation.

        Args:
            callback: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        with self._lock:
            self._prepare_callbacks.done(callback)
            return self

    def prepare_failed(self, callback: TransmissionPrepareFailCallback) -> typing.Self:
        """
        Adds a callback for failed preparation.

        Args:
            callback: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        with self._lock:
            self._prepare_callbacks.failed(callback)
            return self

    def download(
        self,
        *,
        tunnel: ResourcesBrokerTunnel,
        predicate: typing.Callable[[Resource], bool] | None = None,
    ) -> None:
        """
        Downloads all previously listed resources using the provided tunnel.

        Args:
            tunnel: The broker tunnel.
            predicate: An optional filter predicate callback to filter out specific resources.
        """

        if not self._context.prepared or self._context.resources is None:
            raise RuntimeError("Tried to use an unprepared transmitter context")

        resources = files_list_from_resources_list(self._context.resources)
        downloaded_resources: typing.List[Resource] = []

        def _download(broker: ResourcesBroker) -> None:
            nonlocal resources, downloaded_resources

            for resource in resources:
                # Since the overall download action may get retried, we need to keep track of all already finished downloads
                if resource in downloaded_resources:
                    continue

                if not callable(predicate) or predicate(resource):
                    broker.download_resource(resource.filename, tunnel=tunnel)
                    downloaded_resources.append(resource)

        self._execute(
            cb_exec=_download,
            cb_done=lambda: self._download_callbacks.invoke_done_callbacks(),
            cb_failed=lambda reason: self._download_callbacks.invoke_fail_callbacks(
                reason
            ),
        )

    def download_done(self, callback: TransmissionDownloadDoneCallback) -> typing.Self:
        """
        Adds a callback for finished downloads.

        Args:
            callback: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        with self._lock:
            self._download_callbacks.done(callback)
            return self

    def download_failed(
        self, callback: TransmissionDownloadFailCallback
    ) -> typing.Self:
        """
        Adds a callback for failed downloads.

        Args:
            callback: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        with self._lock:
            self._download_callbacks.failed(callback)
            return self

    def reset(self) -> None:
        with self._lock:
            self._context = ResourcesTransmitterContext()

    def _execute(
        self,
        *,
        cb_exec: typing.Callable[[ResourcesBroker], None],
        cb_done: typing.Callable[[], None],
        cb_failed: typing.Callable[[str], None],
    ) -> None:
        # Get the authorization token for the host system, since we need to access its resources.
        # Once received, the actual execution can happen.
        def _get_auth_token_done(
            reply: GetAuthorizationTokenReply, success: bool, _
        ) -> None:
            with self._lock:
                try:
                    broker = self._create_broker(
                        auth_token=reply.auth_token if success else None
                    )
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    cb_failed(str(exc))
                else:
                    if attempt(
                        cb_exec,
                        broker=broker,
                        fail_callback=lambda e: cb_failed(str(e)),
                        attempts=self._max_attempts,
                        delay=self._attempts_delay,
                    ):
                        cb_done()

        def _get_auth_token_failed(_, msg: str) -> None:
            with self._lock:
                cb_failed(msg)

        GetAuthorizationTokenCommand.build(
            self._service.message_builder,
            user_id=self._user_token.user_id,
            auth_id=AuthorizationToken.TokenType.HOST,
            api_key=self._api_key,
        ).done(_get_auth_token_done).failed(_get_auth_token_failed).emit(
            self._auth_channel
        )

    def _create_broker(
        self, *, auth_token: AuthorizationToken | None
    ) -> ResourcesBroker:
        try:
            return create_resources_broker(
                self._component,
                self._service,
                self._broker_token.broker,
                self._broker_token.config,
                user_token=self._user_token,
                auth_token=auth_token,
                auth_token_refresh=self._auth_token_refresh,
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ResourcesTransmitterError(
                f"Unable to create resources broker"
            ) from exc
