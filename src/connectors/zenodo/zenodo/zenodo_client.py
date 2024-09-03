import requests

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.user import UserToken
from common.py.services import Service

from .zenodo_callbacks import ZenodoCreateProjectCallbacks, ZenodoDeleteProjectCallbacks
from .zenodo_request_data import ZenodoProjectData
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
            trailing_slashes=False,
        )

    def create_project(
        self,
        project: Project,
        *,
        callbacks: ZenodoCreateProjectCallbacks = ZenodoCreateProjectCallbacks(),
    ) -> None:
        """
        Creates a new Zenodo project.

        Args:
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoProjectData:
            resp = self.post(
                session,
                ["deposit", "depositions"],
                json={
                    "metadata": {
                        "upload_type": "publication",
                        "publication_type": "other",
                        "title": project.title,
                        "creators": [{"name": "Doe, John"}],
                        "description": project.description,
                        "access_right": "open",
                        "license": "cc-by",
                    }
                },
            )
            return ZenodoProjectData(resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )

    def delete_project(
        self,
        zenodo_project: ZenodoProjectData,
        *,
        callbacks: ZenodoDeleteProjectCallbacks = ZenodoDeleteProjectCallbacks(),
    ):
        """
        Deletes an existing Zenodo project.

        Args:
            zenodo_project: The Zenodo project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            resp = self.delete(
                session,
                ["deposit", "depositions", zenodo_project.project_id],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )
