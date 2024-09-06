import pathlib
from io import BytesIO

import requests

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.user import UserToken
from common.py.integration.resources.transmitters import ResourceBuffer
from common.py.services import Service

from .zenodo_callbacks import (
    ZenodoCreateProjectCallbacks,
    ZenodoDeleteProjectCallbacks,
    ZenodoUploadFileCallbacks,
)
from .zenodo_request_data import ZenodoFileData, ZenodoProjectData
from ...base.integration.execution import RequestsExecutor
from ...base.integration.execution.requests_executor import RequestsExecutorOptions


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
        requests_options: RequestsExecutorOptions = RequestsExecutorOptions(),
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
            requests_options: Additional requests options.
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
            requests_options=RequestsExecutorOptions(
                content_type=requests_options.content_type, trailing_slashes=False
            ),
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
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

    def upload_file(
        self,
        zenodo_project: ZenodoProjectData,
        *,
        path: str,
        file: ResourceBuffer,
        callbacks: ZenodoUploadFileCallbacks = ZenodoUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to a Zenodo project.

        Args:
            zenodo_project: The Zenodo project.
            path: The remote path of the file.
            file: The file data.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoFileData:
            file_path = pathlib.PurePosixPath(path)

            # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
            if file.seekable():
                file.seek(0)

            resp = self.put(
                session,
                f"{zenodo_project.bucket_link}/{file_path.name}",
                data=BytesIO(file.readall()),
            )
            return ZenodoFileData(resp)

        def _upload_done(data: ZenodoFileData) -> None:
            callbacks.invoke_done_callbacks(data)
            file.close()  # Free up the buffer to save memory

        def _upload_failed(reason: str) -> None:
            callbacks.invoke_fail_callbacks(reason)
            file.close()  # Free up the buffer to save memory

        self._execute(
            cb_exec=_execute,
            cb_done=_upload_done,
            cb_failed=_upload_failed,
        )
