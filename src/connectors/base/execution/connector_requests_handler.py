import abc
import typing

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project, ProjectExternalState
from common.py.data.entities.user import UserToken
from common.py.services import Service

from ..data.types import ProjectExternalStateCallbacks


class ConnectorRequestsHandler(abc.ABC):
    """
    Base class to deal with non-job related requests.
    """

    def __init__(self, comp: BackendComponent, svc: Service, *, auth_channel: Channel):
        self._comp = comp
        self._service = svc

        self._auth_channel = auth_channel

    def query_external_project_state(
        self,
        project: Project,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
        *,
        external_state: ProjectExternalState,
        callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        """
        Called whenever an external project state needs to be renewed.

        Args:
            project: The project.
            connector_instance: The connector instance.
            user_token: The user token.
            external_state: The current external state.
            callbacks: Callbacks to be invoked upon completion.
        """
        raise NotImplementedError()


# pylint: disable=invalid-name
ConnectorRequestsHandlerType = typing.TypeVar(
    "ConnectorRequestsHandlerType", bound=ConnectorRequestsHandler
)
