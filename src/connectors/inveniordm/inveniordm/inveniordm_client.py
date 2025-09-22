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

from .inveniordm_callbacks import (
    InvenioRDMCreateProjectCallbacks,
    InvenioRDMDeleteAllFilesCallbacks,
    InvenioRDMDeleteFileCallbacks,
    InvenioRDMDeleteProjectCallbacks,
    InvenioRDMGetFileListCallbacks,
    InvenioRDMGetProjectCallbacks,
    InvenioRDMUpdateProjectCallbacks,
    InvenioRDMUploadFileCallbacks,
)
from .inveniordm_request_data import (
    InvenioRDMFileListObject,
    InvenioRDMFileObject,
    InvenioRDMProjectObject,
    InvenioRDMRequestData,
)
from ..metadata import InvenioRDMMetadataCreator
from ...base.integration.execution import RequestsExecutor
from ...base.integration.execution.requests_executor import RequestsExecutorOptions


class InvenioRDMClient(RequestsExecutor):
    """
    Client to use the InvenioRDM API.
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
        callbacks: InvenioRDMGetProjectCallbacks = InvenioRDMGetProjectCallbacks(),
    ) -> None:
        """
        Gets information about an existing project.

        Args:
            project_id: The project ID.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMProjectObject:
            resp = self.get(
                session,
                ["deposit", "depositions", project_id],
            )
            return InvenioRDMRequestData.data_from_response(
                InvenioRDMProjectObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def create_project(
        self,
        project: Project,
        *,
        callbacks: InvenioRDMCreateProjectCallbacks = InvenioRDMCreateProjectCallbacks(),
    ) -> None:
        """
        Creates a new InvenioRDM project.

        Args:
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMProjectObject:
            resp = self.post(
                session,
                ["deposit", "depositions"],
                json=self._get_project_metadata(project),
            )
            return InvenioRDMRequestData.data_from_response(
                InvenioRDMProjectObject, resp
            )

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
        callbacks: InvenioRDMUpdateProjectCallbacks = InvenioRDMUpdateProjectCallbacks(),
    ) -> None:
        """
        Updates an existing InvenioRDM project.

        Args:
            project_id: The remote project ID.
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMProjectObject:
            resp = self.put(
                session,
                ["deposit", "depositions", project_id],
                json=self._get_project_metadata(project),
            )
            return InvenioRDMRequestData.data_from_response(
                InvenioRDMProjectObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_project(
        self,
        InvenioRDM_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMDeleteProjectCallbacks = InvenioRDMDeleteProjectCallbacks(),
    ):
        """
        Deletes an existing InvenioRDM project.

        Args:
            InvenioRDM_project: The InvenioRDM project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            self.delete(
                session,
                ["deposit", "depositions", InvenioRDM_project.project_id],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_file_list(
        self,
        InvenioRDM_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMGetFileListCallbacks = InvenioRDMGetFileListCallbacks(),
    ) -> None:
        """
        Retrieves the complete file list of a InvenioRDM project.

        Args:
            InvenioRDM_project: The InvenioRDM project.
            callbacks:  Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMFileListObject:
            resp = self.get(
                session,
                ["deposit", "depositions", InvenioRDM_project.project_id, "files"],
            )
            return InvenioRDMRequestData.data_from_response(
                InvenioRDMFileListObject, resp
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def upload_file(
        self,
        InvenioRDM_project: InvenioRDMProjectObject,
        *,
        path: str,
        file_data: ResourceBuffer,
        callbacks: InvenioRDMUploadFileCallbacks = InvenioRDMUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to a InvenioRDM project.

        Args:
            InvenioRDM_project: The InvenioRDM project.
            path: The remote path of the file.
            file_data: The file data.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMFileObject:
            file_path = pathlib.PurePosixPath(path)

            # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
            if file_data.seekable():
                file_data.seek(0)

            resp = self.put(
                session,
                f"{InvenioRDM_project.bucket_link}/{file_path.name}",
                data=BytesIO(file_data.readall()),
            )
            return InvenioRDMRequestData.data_from_response(InvenioRDMFileObject, resp)

        def _upload_done(data: InvenioRDMFileObject) -> None:
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
        InvenioRDM_project: InvenioRDMProjectObject,
        InvenioRDM_file: InvenioRDMFileObject,
        *,
        callbacks: InvenioRDMDeleteFileCallbacks = InvenioRDMDeleteFileCallbacks(),
    ):
        """
        Deletes an existing InvenioRDM file.

        Args:
            InvenioRDM_project: The InvenioRDM project.
            InvenioRDM_file: The InvenioRDM file.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            self.delete(
                session,
                [
                    "deposit",
                    "depositions",
                    InvenioRDM_project.project_id,
                    "files",
                    InvenioRDM_file.file_id,
                ],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_all_files(
        self,
        InvenioRDM_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMDeleteAllFilesCallbacks = InvenioRDMDeleteAllFilesCallbacks(),
    ):
        """
        Deletes all files of a InvenioRDM project.

        Args:
            InvenioRDM_project: The InvenioRDM project.
            callbacks: Optional request callbacks.
        """

        def _get_file_list_done(files: InvenioRDMFileListObject):
            files_to_delete = len(files.files)
            if files_to_delete > 0:

                def _file_deleted():
                    nonlocal files_to_delete
                    files_to_delete -= 1

                    if files_to_delete <= 0:
                        callbacks.invoke_done_callbacks()

                for file in files.files:
                    delete_file_callbacks = InvenioRDMDeleteFileCallbacks()
                    delete_file_callbacks.done(_file_deleted)
                    delete_file_callbacks.failed(
                        lambda _: _file_deleted()
                    )  # We ignore errors here

                    self.delete_file(
                        InvenioRDM_project, file, callbacks=delete_file_callbacks
                    )
            else:
                callbacks.invoke_done_callbacks()

        def _get_file_list_failed(exc: Exception):
            callbacks.invoke_fail_callbacks(exc)

        file_list_callbacks = InvenioRDMGetFileListCallbacks()
        file_list_callbacks.done(_get_file_list_done)
        file_list_callbacks.failed(_get_file_list_failed)

        self.get_file_list(InvenioRDM_project, callbacks=file_list_callbacks)

    def _get_project_metadata(self, project: Project) -> typing.Any:
        creator = InvenioRDMMetadataCreator()
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
