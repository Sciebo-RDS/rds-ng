import pathlib
import typing
from io import BytesIO

import requests

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.user import UserToken
from common.py.integration.resources.transmitters import ResourceBuffer
from common.py.services import Service
from . import ZenodoUpdateProjectCallbacks
from .zenodo_callbacks import (
    ZenodoCreateProjectCallbacks,
    ZenodoDeleteAllFilesCallbacks,
    ZenodoDeleteFileCallbacks,
    ZenodoDeleteProjectCallbacks,
    ZenodoGetFileListCallbacks,
    ZenodoGetProjectCallbacks,
    ZenodoUploadFileCallbacks,
)
from .zenodo_request_data import (
    ZenodoFileObject,
    ZenodoFileListObject,
    ZenodoProjectObject,
    ZenodoRequestData,
)
from ..metadata import ZenodoMetadataCreator
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
        from ...base.settings import ConnectorSettingIDs

        super().__init__(
            comp,
            svc,
            connector_instance=connector_instance,
            auth_channel=auth_channel,
            user_token=user_token,
            base_url=comp.data.config.value(ConnectorSettingIDs.TARGET),
            requests_options=RequestsExecutorOptions(
                content_type=requests_options.content_type, trailing_slashes=False
            ),
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

    def get_project(
        self,
        project_id: str,
        *,
        callbacks: ZenodoGetProjectCallbacks = ZenodoGetProjectCallbacks(),
    ) -> None:
        """
        Gets information about an existing project.

        Args:
            project_id: The project ID.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoProjectObject:
            resp = self.get(
                session,
                ["deposit", "depositions", project_id],
            )
            return ZenodoRequestData.data_from_response(ZenodoProjectObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
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

        def _execute(session: requests.Session) -> ZenodoProjectObject:
            resp = self.post(
                session,
                ["deposit", "depositions"],
                json=self._get_project_metadata(project),
            )
            return ZenodoRequestData.data_from_response(ZenodoProjectObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def update_project(
        self,
        project_id: str,
        project: Project,
        *,
        callbacks: ZenodoUpdateProjectCallbacks = ZenodoUpdateProjectCallbacks(),
    ) -> None:
        """
        Updates an existing Zenodo project.

        Args:
            project_id: The remote project ID.
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoProjectObject:
            resp = self.put(
                session,
                ["deposit", "depositions", project_id],
                json=self._get_project_metadata(project),
            )
            return ZenodoRequestData.data_from_response(ZenodoProjectObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_project(
        self,
        zenodo_project: ZenodoProjectObject,
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
            self.delete(
                session,
                ["deposit", "depositions", zenodo_project.project_id],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_file_list(
        self,
        zenodo_project: ZenodoProjectObject,
        *,
        callbacks: ZenodoGetFileListCallbacks = ZenodoGetFileListCallbacks(),
    ) -> None:
        """
        Retrieves the complete file list of a Zenodo project.

        Args:
            zenodo_project: The Zenodo project.
            callbacks:  Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoFileListObject:
            resp = self.get(
                session,
                ["deposit", "depositions", zenodo_project.project_id, "files"],
            )
            return ZenodoRequestData.data_from_response(ZenodoFileListObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def upload_file(
        self,
        zenodo_project: ZenodoProjectObject,
        *,
        path: str,
        file_data: ResourceBuffer,
        callbacks: ZenodoUploadFileCallbacks = ZenodoUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to a Zenodo project.

        Args:
            zenodo_project: The Zenodo project.
            path: The remote path of the file.
            file_data: The file data.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> ZenodoFileObject:
            file_path = pathlib.PurePosixPath(path)

            # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
            if file_data.seekable():
                file_data.seek(0)

            resp = self.put(
                session,
                f"{zenodo_project.bucket_link}/{file_path.name}",
                data=BytesIO(file_data.readall()),
            )
            return ZenodoRequestData.data_from_response(ZenodoFileObject, resp)

        def _upload_done(data: ZenodoFileObject) -> None:
            callbacks.invoke_done_callbacks(data)
            file_data.close()  # Free up the buffer to save memory

        def _upload_failed(exc: Exception) -> None:
            callbacks.invoke_fail_callbacks(exc)
            file_data.close()  # Free up the buffer to save memory

        self._execute(
            cb_exec=_execute,
            cb_done=_upload_done,
            cb_failed=_upload_failed,
        )

    def delete_file(
        self,
        zenodo_project: ZenodoProjectObject,
        zenodo_file: ZenodoFileObject,
        *,
        callbacks: ZenodoDeleteFileCallbacks = ZenodoDeleteFileCallbacks(),
    ):
        """
        Deletes an existing Zenodo file.

        Args:
            zenodo_project: The Zenodo project.
            zenodo_file: The Zenodo file.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            self.delete(
                session,
                [
                    "deposit",
                    "depositions",
                    zenodo_project.project_id,
                    "files",
                    zenodo_file.file_id,
                ],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_all_files(
        self,
        zenodo_project: ZenodoProjectObject,
        *,
        callbacks: ZenodoDeleteAllFilesCallbacks = ZenodoDeleteAllFilesCallbacks(),
    ):
        """
        Deletes all files of a Zenodo project.

        Args:
            zenodo_project: The Zenodo project.
            callbacks: Optional request callbacks.
        """

        def _get_file_list_done(files: ZenodoFileListObject):
            files_to_delete = len(files.files)
            if files_to_delete > 0:

                def _file_deleted():
                    nonlocal files_to_delete
                    files_to_delete -= 1

                    if files_to_delete <= 0:
                        callbacks.invoke_done_callbacks()

                for file in files.files:
                    delete_file_callbacks = ZenodoDeleteFileCallbacks()
                    delete_file_callbacks.done(_file_deleted)
                    delete_file_callbacks.failed(
                        lambda _: _file_deleted()
                    )  # We ignore errors here

                    self.delete_file(
                        zenodo_project, file, callbacks=delete_file_callbacks
                    )
            else:
                callbacks.invoke_done_callbacks()

        def _get_file_list_failed(exc: Exception):
            callbacks.invoke_fail_callbacks(exc)

        file_list_callbacks = ZenodoGetFileListCallbacks()
        file_list_callbacks.done(_get_file_list_done)
        file_list_callbacks.failed(_get_file_list_failed)

        self.get_file_list(zenodo_project, callbacks=file_list_callbacks)

    def _get_project_metadata(self, project: Project) -> typing.Any:
        creator = ZenodoMetadataCreator()
        metadata = creator.create(
            project.features.project_metadata.metadata,
            project.features.shared_objects,
        )
        # creator.validate(metadata)

        return {
            "metadata": {
                "publication_type": "other",
                "access_right": "closed",
                "license": "cc-by",
                "image_type": "other",
                "title": (
                    metadata.title
                    if metadata.title is not None
                    else "Uploaded via Sciebo RDS"
                ),
                "upload_type": (
                    metadata.upload_type
                    if metadata.upload_type is not None
                    else "other"
                ),
                "creators": (
                    metadata.creators if metadata.creators is not None else []
                ),
                "description": (
                    metadata.description
                    if metadata.description is not None
                    else "No description provided"
                ),
                "contributors": (
                    metadata.contributors if metadata.contributors is not None else []
                ),
                "version": (metadata.version if metadata.version is not None else ""),
                "grants": (metadata.grants if metadata.grants is not None else []),
                "dates": metadata.dates if metadata.dates is not None else [],
            }
        }
