from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.user import UserToken
from common.py.services import Service

from ...base.integration.execution import RequestsExecutor


class ZenodoClient(RequestsExecutor):
    """
    Client to use the Zenodo API.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        *,
        connector_instance: ConnectorInstanceID,
        auth_channel: Channel,
        user_token: UserToken,
        max_attempts: int = 1,
        attempts_delay: float = 3.0,
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            connector_instance: The connector instance ID.
            auth_channel: Channel to fetch authorization tokens from.
            user_token: The user token.
            max_attempts: The number of attempts for each operation; cannot be less than 1.
            attempts_delay: The delay (in seconds) between each attempt.
        """
        super().__init__(
            comp,
            svc,
            connector_instance=connector_instance,
            auth_channel=auth_channel,
            user_token=user_token,
            base_url="https://sandbox.zenodo.org/api/",
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )
