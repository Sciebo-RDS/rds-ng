import threading
import typing

from .resources_transmitter_context import ResourcesTransmitterContext
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import create_resources_broker, ResourcesBroker
from ....api import GetAuthorizationTokenCommand, GetAuthorizationTokenReply
from ....component import BackendComponent
from ....core.messaging import Channel
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.project import Project
from ....data.entities.resource import ResourcesBrokerToken, ResourcesList
from ....data.entities.user import UserToken
from ....services import Service
from ....utils import ExecutionCallbacks

TransmissionPrepareDoneCallback = typing.Callable[[ResourcesList], None]
TransmissionPrepareFailCallback = typing.Callable[[str], None]


class ResourcesTransmitter:
    """
    Main class to transmit resources.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        user_token: UserToken,
        broker_token: ResourcesBrokerToken,
        auth_channel: Channel = Channel.local(),
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            user_token: The user token.
            broker_token: The broker token.
            auth_channel: Channel to fetch authorization tokens from; defaults to a local channel.
        """
        from ....settings import NetworkSettingIDs

        self._component = comp
        self._service = svc
        self._auth_channel = auth_channel

        self._user_token = user_token
        self._broker_token = broker_token

        self._prepare_callbacks = ExecutionCallbacks[
            TransmissionPrepareDoneCallback, TransmissionPrepareFailCallback
        ]()

        self._context = ResourcesTransmitterContext()
        self._prepared = False

        self._api_key = self._component.data.config.value(NetworkSettingIDs.API_KEY)
        self._lock = threading.RLock()

    def prepare(self, project: Project) -> None:
        """
        Prepares the transmission of resources; must always be called before any other method.

        Args:
            project: The project to work on.
        """

        # Get a list of all resources in the project's path
        # TODO: Error handling
        def _execute_prepare(broker: ResourcesBroker) -> None:
            self._context.resources = broker.list_resources(project.resources_path)
            self._prepare_callbacks.invoke_done_callbacks(self._context.resources)

            self._prepared = True

        def _failed_prepare(reason: str) -> None:
            self._prepare_callbacks.invoke_fail_callbacks(reason)

        self._execute(_execute_prepare, _failed_prepare)

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

    def reset(self) -> None:
        with self._lock:
            self._context = ResourcesTransmitterContext()
            self._prepared = False

    def _execute(
        self,
        cb_exec: typing.Callable[[ResourcesBroker], None],
        cb_failed: typing.Callable[[str], None],
    ) -> None:
        from ....settings import NetworkSettingIDs

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
                    cb_exec(broker)

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
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ResourcesTransmitterError(
                f"Unable to create resources broker"
            ) from exc
