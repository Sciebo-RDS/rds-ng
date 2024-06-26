import threading
import typing

from .resources_transmitter_context import ResourcesTransmitterContext
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import create_resources_broker, ResourcesBroker
from ....component import BackendComponent
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
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            user_token: The user token.
            broker_token: The broker token.
        """
        self._component = comp
        self._service = svc

        self._user_token = user_token
        self._broker_token = broker_token

        self._prepare_callbacks = ExecutionCallbacks[
            TransmissionPrepareDoneCallback, TransmissionPrepareFailCallback
        ]()

        self._context = ResourcesTransmitterContext()
        self._lock = threading.RLock()

    def prepare(self, project: Project) -> None:
        """
        Prepares the transmission of resources; must always be called before any other method.

        Args:
            project: The project to work on.
        """

        # Get a list of all resources in the project's path
        with self._lock:
            # TODO: Async; Error Handling
            broker = self._create_broker()

            self._context.resources = broker.list_resources(project.resources_path)
            self._prepare_callbacks.invoke_done_callbacks(self._context.resources)

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

            self._prepare_callbacks = ExecutionCallbacks[
                TransmissionPrepareDoneCallback, TransmissionPrepareFailCallback
            ]()

    def _create_broker(self) -> ResourcesBroker:
        try:
            return create_resources_broker(
                self._component,
                self._service,
                self._broker_token.broker,
                self._broker_token.config,
                user_token=self._user_token,
                auth_token=None,  # TODO: Get current auth from svr
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ResourcesTransmitterError(
                f"Unable to create resources broker"
            ) from exc
