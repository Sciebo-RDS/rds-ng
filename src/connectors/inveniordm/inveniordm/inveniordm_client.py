import typing
from datetime import datetime
from http import HTTPStatus
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
        Gets information about an existing project. This checks first if there is a published version, otherwise, it checks if there is a draft one.

        Args:
            project_id: The project ID.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMProjectObject:
            resp = self.get(
                session,
                ["records", project_id],
            )
            if resp.status_code != HTTPStatus.OK:
                resp = self.get(
                    session,
                    ["records", project_id, "draft"],
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
                ["records"],
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
                ["records", project_id, "draft"],
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
        invenio_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMDeleteProjectCallbacks = InvenioRDMDeleteProjectCallbacks(),
    ):
        """
        Deletes an existing InvenioRDM project.

        Args:
            invenio_project: The InvenioRDM project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            self.delete(
                session,
                ["records", invenio_project.project_id, "draft"],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_file_list(
        self,
        invenio_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMGetFileListCallbacks = InvenioRDMGetFileListCallbacks(),
    ) -> None:
        """
        Retrieves the complete file list of a InvenioRDM project.

        Args:
            invenio_project: The InvenioRDM project.
            callbacks:  Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMFileListObject:
            resp = self.get(
                session,
                ["records", invenio_project.project_id, "draft", "files"],
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
        invenio_project: InvenioRDMProjectObject,
        *,
        path: str,
        file_data: ResourceBuffer,
        callbacks: InvenioRDMUploadFileCallbacks = InvenioRDMUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to a InvenioRDM project.

        Args:
            invenio_project: The InvenioRDM project.
            path: The remote path of the file.
            file_data: The file data.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> InvenioRDMFileObject:
            file_path = path.lstrip("/").replace("/", "__")

            resp = self.post(
                session,
                ["records", invenio_project.project_id, "draft", "files"],
                json=[{"key": file_path}],
            )
            if resp.status_code == HTTPStatus.CREATED:
                files = typing.cast(
                    InvenioRDMFileListObject,
                    InvenioRDMRequestData.data_from_response(
                        InvenioRDMFileListObject, resp
                    ),
                )
                file_obj = files.find_file(file_path)

                # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
                if file_data.seekable():
                    file_data.seek(0)

                resp = self.put(
                    session,
                    file_obj.content_link,
                    data=BytesIO(file_data.readall()),
                    headers={"Content-Type": "application/octet-stream"},
                )
                if resp.status_code == HTTPStatus.OK:
                    resp = self.post(
                        session,
                        file_obj.commit_link,
                    )
                    return InvenioRDMRequestData.data_from_response(
                        InvenioRDMFileObject, resp
                    )

            raise Exception(
                f"Error uploading {file_path}: {resp.content} ({resp.status_code})"
            )

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
        invenio_project: InvenioRDMProjectObject,
        invenio_file: InvenioRDMFileObject,
        *,
        callbacks: InvenioRDMDeleteFileCallbacks = InvenioRDMDeleteFileCallbacks(),
    ):
        """
        Deletes an existing InvenioRDM file.

        Args:
            invenio_project: The InvenioRDM project.
            invenio_file: The InvenioRDM file.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            resp = self.delete(
                session,
                [
                    "records",
                    invenio_project.project_id,
                    "draft",
                    "files",
                    invenio_file.key,
                ],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_all_files(
        self,
        invenio_project: InvenioRDMProjectObject,
        *,
        callbacks: InvenioRDMDeleteAllFilesCallbacks = InvenioRDMDeleteAllFilesCallbacks(),
    ):
        """
        Deletes all files of a InvenioRDM project.

        Args:
            invenio_project: The InvenioRDM project.
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
                        invenio_project, file, callbacks=delete_file_callbacks
                    )
            else:
                callbacks.invoke_done_callbacks()

        def _get_file_list_failed(exc: Exception):
            callbacks.invoke_fail_callbacks(exc)

        file_list_callbacks = InvenioRDMGetFileListCallbacks()
        file_list_callbacks.done(_get_file_list_done)
        file_list_callbacks.failed(_get_file_list_failed)

        self.get_file_list(invenio_project, callbacks=file_list_callbacks)

    def _get_project_metadata(self, project: Project) -> typing.Any:
        creator = InvenioRDMMetadataCreator()
        metadata = creator.create(
            project.features.project_metadata.metadata,
            project.features.shared_objects,
        )
        # creator.validate(metadata)

        project_metadata = {
            "title": (
                metadata.title
                if metadata.title is not None
                else "Uploaded via Sciebo RDS"
            ),
            "creators": [  # TODO
                {
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal",
                    }
                },
                {
                    "person_or_org": {
                        "family_name": "Collins",
                        "given_name": "Thomas",
                        "identifiers": [
                            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                        ],
                        "name": "Collins, Thomas",
                        "type": "personal",
                    }
                },
            ],
            "resource_type": (
                metadata.resource_type if metadata.resource_type else "other"
            ),
            "publication_date": (
                metadata.publication_date
                if metadata.publication_date
                else datetime.now().strftime("%Y-%m-%d")
            ),
        }

        if metadata.description:
            project_metadata["description"] = metadata.description

        return {
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": True},
            "metadata": project_metadata,
        }
