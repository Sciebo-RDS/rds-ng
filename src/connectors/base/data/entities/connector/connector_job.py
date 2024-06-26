import time
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.resource import ResourcesBrokerToken
from common.py.data.entities.user import UserToken


@dataclass_json
@dataclass(kw_only=True)
class ConnectorJob:
    """
    Data class for jobs executed by a connector.

    Attributes:
        project: The project.
        connector_instance: The connector instance ID.
        user_token: The user token.
        broker_token: Token to create the resources broker.
        timestamp: The starting timestamp.
    """

    project: Project
    connector_instance: ConnectorInstanceID

    user_token: UserToken
    broker_token: ResourcesBrokerToken

    timestamp: float = field(default_factory=lambda: time.time())
