import requests

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.user import UserToken
from common.py.integration.resources.transmitters import ResourceBuffer
from common.py.services import Service

from .osf_callbacks import (
    OSFCreateProjectCallbacks,
    OSFGetStorageCallbacks,
    OSFUploadFileCallbacks,
)
from .osf_request_data import (
    OSFFileData,
    OSFProjectData,
    OSFStorageData,
)
from ...base.integration.execution import RequestsExecutor


class OSFClient(RequestsExecutor):
    """
    Client to use the OSF API.
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
            base_url="https://api.test.osf.io/v2/",
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

    def create_project(
        self,
        project: Project,
        *,
        callbacks: OSFCreateProjectCallbacks = OSFCreateProjectCallbacks(),
    ) -> None:
        """
        Creates a new OSF project.

        Args:
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFProjectData:
            resp = self.post(
                session,
                ["nodes"],
                data={
                    "data": {
                        "type": "nodes",
                        "attributes": {
                            "title": project.title,
                            "category": "project",
                            "description": project.description,
                        },
                    }
                },
            )
            return OSFProjectData(resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )

    def get_storage(
        self,
        osf_project: OSFProjectData,
        *,
        provider: str = "osfstorage",
        callbacks: OSFGetStorageCallbacks = OSFGetStorageCallbacks(),
    ) -> None:
        """
        Gets information about an OSF storage.

        Args:
            osf_project: The OSF project.
            provider: The storage provider.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFStorageData:
            resp = self.get(
                session,
                ["nodes", osf_project.project_id, "files", "providers", provider],
            )
            return OSFStorageData(resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )

    def upload_file(
        self,
        osf_storage: OSFStorageData,
        *,
        path: str,
        file: ResourceBuffer,
        overwrite: bool = True,
        callbacks: OSFUploadFileCallbacks = OSFUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to an OSF storage, creating any missing folders on the fly.

        Args:
            osf_storage: The OSF storage.
            path: The remote path of the file.
            file: The file data.
            overwrite: Whether an existing file should be overwritten.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFFileData:
            pass

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda reason: callbacks.invoke_fail_callbacks(reason),
        )
