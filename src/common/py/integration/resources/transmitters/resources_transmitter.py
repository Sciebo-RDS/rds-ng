from .resources_transmitter_context import ResourcesTransmitterContext
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import create_resources_broker
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.project import Project
from ....data.entities.resource import ResourcesBrokerToken, ResourcesList
from ....data.entities.user import UserToken
from ....services import Service


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
        auth_token: AuthorizationToken | None,
        broker_token: ResourcesBrokerToken,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            user_token: The user token.
            auth_token: An optional authorization token.
            broker_token: The broker token.
        """
        try:
            self._broker = create_resources_broker(
                comp,
                svc,
                broker_token.broker,
                broker_token.config,
                user_token=user_token,
                auth_token=auth_token,
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ResourcesTransmitterError(
                f"Unable to create resources broker"
            ) from exc

        self._context = ResourcesTransmitterContext()

    def prepare(self, project: Project) -> None:
        """
        Prepares the transmission of resources; must always be called before any other method.

        Args:
            project: The project to work on.
        """

        # Get a list of all resources in the project's path
        # TODO: Strategy performs re-authorization in case of expired tokens -> At least tell the server
        self._context.resources = self._fetch_resources(project.resources_path)

    def reset(self) -> None:
        self._context = ResourcesTransmitterContext()

    def _fetch_resources(self, root: str) -> ResourcesList:
        try:
            return self._broker.list_resources(root)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise ResourcesTransmitterError(f"Unable to list resources") from exc
