from common.py.data.entities.connector.connector_instance import ConnectorInstanceID
from common.py.data.entities.project.project import Project
from common.py.data.entities.project.project_external_state import ProjectExternalState
from common.py.data.entities.user.user_token import UserToken
from connectors.base.data.types.callbacks import ProjectExternalStateCallbacks
from connectors.base.execution.connector_requests_handler import (
    ConnectorRequestsHandler,
)
from connectors.dataverse.dataverse.dataverse_callbacks import (
    DataverseGetDatasetCallbacks,
)
from connectors.dataverse.dataverse.dataverse_client import DataverseClient
from connectors.dataverse.dataverse.dataverse_request_data import DataverseDatasetObject


class DataverseRequestsHandler(ConnectorRequestsHandler):
    """
    Dataverse-specific class to deal with non-job related requests.
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
        def _get_project_done(dataverse_dataset: DataverseDatasetObject) -> None:
            from .dataverse_utils import process_external_project_state

            process_external_project_state(dataverse_dataset, external_state)
            callbacks.invoke_done_callbacks(external_state)

        def _get_project_failed(exc: Exception) -> None:
            callbacks.invoke_fail_callbacks(exc)

        if (
            client := self._create_client(
                connector_instance=connector_instance,
                user_token=user_token,
            )
        ) is not None:
            get_project_callbacks = DataverseGetDatasetCallbacks()
            get_project_callbacks.done(_get_project_done)
            get_project_callbacks.failed(_get_project_failed)

            client.get_dataset(
                external_state.external_id, callbacks=get_project_callbacks
            )

    def _create_client(
        self,
        *,
        connector_instance: ConnectorInstanceID,
        user_token: UserToken,
    ) -> DataverseClient:
        return DataverseClient(
            self._comp,
            self._service,
            connector_instance=connector_instance,
            auth_channel=self._auth_channel,
            user_token=user_token,
        )
