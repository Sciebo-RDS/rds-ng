from .resources_transmitter_context import ResourcesTransmitterContext
from .resources_transmitter_exceptions import ResourcesTransmitterError
from ..brokers import create_resources_broker
from ....component import BackendComponent
from ....data.entities.authorization import AuthorizationToken
from ....data.entities.resource import ResourcesBrokerToken
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

    def reset(self) -> None:
        self._context = ResourcesTransmitterContext()
