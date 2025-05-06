from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project, ProjectExternalState
from common.py.data.entities.user import UserToken

from ...base.data.types import ProjectExternalStateCallbacks
from ...base.execution import ConnectorRequestsHandler


class StubRequestsHandler(ConnectorRequestsHandler):
    """
    Stub-specific class to deal with non-job related requests.
    """

    def query_external_project_state(
        self,
        project: Project,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
        *,
        external_state: ProjectExternalState,
        callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        from .stub_utils import process_external_project_state

        process_external_project_state(external_state)
        callbacks.invoke_done_callbacks(external_state)
