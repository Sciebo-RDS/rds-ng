import io
import threading
import typing

from .resources_transmitter_contexts import (
    ResourcesTransmitterContext,
    ResourcesTransmitterDownloadContext,
)
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import (
    create_resources_broker,
    ResourcesBroker,
    ResourcesBrokerTunnel,
    ResourcesBrokerTunnelType,
)
from ....api import GetAuthorizationTokenCommand, GetAuthorizationTokenReply
from ....component import BackendComponent
from ....core.messaging import Channel
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.project import Project
from ....data.entities.resource import (
    Resource,
    ResourcesBrokerToken,
    ResourcesList,
)
from ....data.entities.user import UserToken
from ....services import Service
from ....utils.func import attempt, ExecutionCallbacks

ResourceBuffer = io.RawIOBase

TransmissionPrepareDoneCallback = typing.Callable[[ResourcesList], None]
TransmissionPrepareFailCallback = typing.Callable[[str], None]
TransmissionDownloadDoneCallback = typing.Callable[[Resource, ResourceBuffer], None]
TransmissionDownloadFailCallback = typing.Callable[[Resource, str], None]


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
        tunnel_type: type[ResourcesBrokerTunnelType],
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
            auth_channel: Channel to fetch authorization tokens from.
            tunnel_type: The type of the resources broker tunnel that will be created for downloading.
            user_token: The user token.
            broker_token: The broker token.
            max_attempts: The number of attempts for each operation; cannot be less than 1.
            attempts_delay: The delay (in seconds) between each attempt.
            auth_token_refresh: Whether expired authorization tokens should be refreshed automatically.
        """
        from ....settings import NetworkSettingIDs

        self._component = comp
        self._service = svc
        self._auth_channel = auth_channel
        self._tunnel_type = tunnel_type

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
            cb_done=lambda _: self._prepare_callbacks.invoke_done_callbacks(
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

    def download(self, resource: Resource) -> None:
        """
        Downloads a resource using the provided tunnel type.

        Args:
            resource: The resource to download.
        """
        self._context.download_list = [resource]
        self._context.download_index = 0

        self._download_resource(resource)

    def download_all(
        self,
        *,
        cb_progress: typing.Callable[[Resource, int, int], None] | None = None,
        cb_done: typing.Callable[[], None] | None = None,
    ):
        """
        Downloads all previously listed files.

        Args:
            cb_progress: A callback called for each file being downloaded.
            cb_done: A callback called when all downloads have finished.
        """
        if not self._context.resources:
            raise RuntimeError("Tried to use an empty transmitter context")

        from ....data.entities.resource import files_list_from_resources_list

        with self._lock:
            resources = files_list_from_resources_list(self._context.resources)

        self.download_list(
            resources,
            cb_progress=cb_progress,
            cb_done=cb_done,
        )

    def download_list(
        self,
        resources: typing.List[Resource],
        *,
        cb_progress: typing.Callable[[Resource, int, int], None] | None = None,
        cb_done: typing.Callable[[], None] | None = None,
    ) -> None:
        """
        Downloads an entire list of resources.

        Args:
            resources: The resources list.
            cb_progress: A callback called for each file being downloaded.
            cb_done: A callback called when all downloads have finished.
        """
        if len(resources) > 0:
            with self._lock:
                self._context.download_list = resources
                self._context.download_index = 0

            return self._download_list_next(
                resources,
                cb_progress=cb_progress,
                cb_done=cb_done,
            )
        else:
            if callable(cb_done):
                cb_done()

    def _download_resource(
        self,
        resource: Resource,
        *,
        cb_tunnel: typing.Callable[[ResourcesBrokerTunnel], None] | None = None,
    ) -> None:
        with self._lock:
            if not self._context.prepared:
                raise RuntimeError("Tried to use an unprepared transmitter context")

            def _download(
                broker: ResourcesBroker,
                download_ctx: ResourcesTransmitterDownloadContext,
            ) -> ResourcesTransmitterDownloadContext:
                download_ctx.tunnel = self._create_tunnel(
                    download_ctx.resource, cb_tunnel=cb_tunnel
                )
                broker.download_resource(resource, tunnel=download_ctx.tunnel)
                return download_ctx

            def _download_done(
                download_ctx: ResourcesTransmitterDownloadContext,
            ) -> None:
                self._download_callbacks.invoke_done_callbacks(
                    resource, typing.cast(ResourceBuffer, download_ctx.tunnel)
                )

            def _download_failed(reason: str) -> None:
                self._download_callbacks.invoke_fail_callbacks(resource, reason)

            self._execute(
                cb_exec=_download,
                cb_done=_download_done,
                cb_failed=_download_failed,
                download_ctx=ResourcesTransmitterDownloadContext(resource=resource),
            )

    def _download_list_next(
        self,
        resources: typing.List[Resource],
        *,
        cb_progress: typing.Callable[[Resource, int, int], None] | None = None,
        cb_done: typing.Callable[[], None] | None = None,
    ) -> None:
        with self._lock:
            resource = resources[self._context.download_index]
            if callable(cb_progress):
                cb_progress(resource, self._context.download_index, len(resources))

            def _chain_tunnel(tunnel: ResourcesBrokerTunnel) -> None:
                tunnel.on(
                    ResourcesBrokerTunnel.CallbackTypes.DONE,
                    lambda _: (
                        self._download_list_next(
                            resources,
                            cb_progress=cb_progress,
                            cb_done=cb_done,
                        )
                        if not self._context.all_downloads_done
                        else cb_done() if callable(cb_done) else None
                    ),
                )

            self._download_resource(resource, cb_tunnel=_chain_tunnel)

            self._context.download_index += 1

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
        cb_exec: typing.Callable[..., typing.Any],
        cb_done: typing.Callable[[typing.Any], None],
        cb_failed: typing.Callable[[str], None],
        cb_retry: typing.Callable[..., None] | None = None,
        **kwargs,
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
                    success, result = attempt(
                        cb_exec,
                        cb_retry=cb_retry,
                        cb_fail=lambda e: cb_failed(str(e)),
                        attempts=self._max_attempts,
                        delay=self._attempts_delay,
                        broker=broker,
                        **kwargs,
                    )
                    if success:
                        cb_done(result)

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

    def _create_tunnel(
        self,
        resource: Resource,
        *,
        cb_tunnel: typing.Callable[[ResourcesBrokerTunnel], None] | None,
    ) -> ResourcesBrokerTunnel:
        with self._lock:
            tunnel = self._tunnel_type(resource)
            if callable(cb_tunnel):
                cb_tunnel(tunnel)
            return tunnel
