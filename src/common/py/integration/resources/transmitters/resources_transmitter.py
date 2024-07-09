import io
import typing

from .resources_transmitter_callbacks import (
    ResourceBuffer,
    ResourcesTransmitterDownloadCallbacks,
    ResourcesTransmitterPrepareCallbacks,
)
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
from ...execution import AuthorizedExecutor
from ....component import BackendComponent
from ....core.messaging import Channel
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.project import Project
from ....data.entities.resource import (
    Resource,
    ResourcesBrokerToken,
)
from ....data.entities.user import UserToken
from ....services import Service


class ResourcesTransmitter(AuthorizedExecutor):
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
        auth_token_refresh: bool = False,
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
        super().__init__(
            comp,
            svc,
            auth_channel=auth_channel,
            auth_id=AuthorizationToken.TokenType.HOST,
            user_token=user_token,
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

        self._tunnel_type = tunnel_type

        self._broker_token = broker_token

        self._auth_token_refresh = auth_token_refresh

        self._context = ResourcesTransmitterContext()

    def prepare(
        self,
        project: Project,
        *,
        callbacks: ResourcesTransmitterPrepareCallbacks = ResourcesTransmitterPrepareCallbacks(),
    ) -> None:
        """
        Prepares the transmission of resources; must always be called before any other method.

        Args:
            project: The project to work on.
            callbacks: Optional execution callbacks.
        """

        def _prepare(broker: ResourcesBroker) -> None:
            self._context.resources = broker.list_resources(project.resources_path)
            self._context.prepared = True

        self._execute(
            cb_exec=_prepare,
            cb_done=lambda _: callbacks.invoke_done_callbacks(self._context.resources),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )

    def download(
        self,
        resource: Resource,
        *,
        callbacks: ResourcesTransmitterDownloadCallbacks = ResourcesTransmitterDownloadCallbacks(),
    ) -> None:
        """
        Downloads a resource using the provided tunnel type.

        Args:
            resource: The resource to download.
            callbacks: Optional execution callbacks.
        """
        self._context.download_list = [resource]
        self._context.download_index = 0

        self._download_resource(resource, callbacks=callbacks)

    def download_all(
        self,
        *,
        callbacks: ResourcesTransmitterDownloadCallbacks = ResourcesTransmitterDownloadCallbacks(),
    ):
        """
        Downloads all previously listed files.

        Args:
            callbacks: Optional execution callbacks.
        """
        if not self._context.resources:
            raise RuntimeError("Tried to use an empty transmitter context")

        from ....data.entities.resource import files_list_from_resources_list

        with self._lock:
            resources = files_list_from_resources_list(self._context.resources)

        self.download_list(
            resources,
            callbacks=callbacks,
        )

    def download_list(
        self,
        resources: typing.List[Resource],
        *,
        callbacks: ResourcesTransmitterDownloadCallbacks = ResourcesTransmitterDownloadCallbacks(),
    ) -> None:
        """
        Downloads an entire list of resources.

        Args:
            resources: The resources list.
            callbacks: Optional execution callbacks.
        """
        if len(resources) > 0:
            with self._lock:
                self._context.download_list = resources
                self._context.download_index = 0

            return self._download_list_next(
                resources,
                callbacks=callbacks,
            )
        else:
            callbacks.invoke_all_done_callbacks()

    def _download_resource(
        self,
        resource: Resource,
        *,
        callbacks: ResourcesTransmitterDownloadCallbacks,
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
                callbacks.invoke_done_callbacks(
                    resource, typing.cast(ResourceBuffer, download_ctx.tunnel)
                )

            def _download_failed(reason: str) -> None:
                callbacks.invoke_fail_callbacks(resource, reason)

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
        callbacks: ResourcesTransmitterDownloadCallbacks,
    ) -> None:
        with self._lock:
            resource = resources[self._context.download_index]
            callbacks.invoke_progress_callbacks(
                resource, self._context.download_index, len(resources)
            )

            def _chain_tunnel(tunnel: ResourcesBrokerTunnel) -> None:
                tunnel.on(
                    ResourcesBrokerTunnel.CallbackTypes.DONE,
                    lambda _: (
                        self._download_list_next(
                            resources,
                            callbacks=callbacks,
                        )
                        if not self._context.all_downloads_done
                        else callbacks.invoke_all_done_callbacks()
                    ),
                )

            self._download_resource(
                resource, callbacks=callbacks, cb_tunnel=_chain_tunnel
            )

            self._context.download_index += 1

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
        def _prepare_execute(
            auth_token: AuthorizationToken | None,
        ) -> typing.Dict[str, typing.Any]:
            return {"broker": self._create_broker(auth_token=auth_token)}

        super()._execute(
            cb_exec=cb_exec,
            cb_done=cb_done,
            cb_failed=cb_failed,
            cb_prepare=_prepare_execute,
            cb_retry=cb_retry,
            **kwargs,
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
