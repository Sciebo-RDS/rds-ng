from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project, ProjectExternalState
from common.py.data.entities.user import UserToken

from ..osf import OSFClient, OSFProjectObject
from ..osf.osf_callbacks import OSFGetProjectCallbacks
from ...base.data.types import ProjectExternalStateCallbacks
from ...base.execution import ConnectorRequestsHandler


class OSFRequestsHandler(ConnectorRequestsHandler):
    """
    OSF-specific class to deal with non-job related requests.
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
        def _get_project_done(osf_project: OSFProjectObject) -> None:
            from .osf_utils import process_external_project_state

            process_external_project_state(osf_project, external_state)
            callbacks.invoke_done_callbacks(external_state)

        def _get_project_failed(exc: Exception) -> None:
            callbacks.invoke_fail_callbacks(exc)

        if (
            client := self._create_client(
                connector_instance=connector_instance,
                user_token=user_token,
            )
        ) is not None:
            get_project_callbacks = OSFGetProjectCallbacks()
            get_project_callbacks.done(_get_project_done)
            get_project_callbacks.failed(_get_project_failed)

            client.get_project(
                external_state.external_id, callbacks=get_project_callbacks
            )

    def _create_client(
        self,
        *,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
    ) -> OSFClient:
        return OSFClient(
            self._comp,
            self._service,
            connector_instance=connector_instance,
            auth_channel=self._auth_channel,
            user_token=user_token,
        )
