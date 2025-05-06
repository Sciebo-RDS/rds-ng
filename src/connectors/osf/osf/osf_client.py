import pathlib
import typing
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
from .osf_callbacks import (
    OSFCreateProjectCallbacks,
    OSFDeleteAllFilesCallbacks,
    OSFDeleteFileCallbacks,
    OSFDeleteProjectCallbacks,
    OSFGetFileListCallbacks,
    OSFGetProjectCallbacks,
    OSFGetStorageCallbacks,
    OSFUpdateProjectCallbacks,
    OSFUploadFileCallbacks,
)
from .osf_request_data import (
    OSFFileListObject,
    OSFFileObject,
    OSFProjectObject,
    OSFRequestData,
    OSFStorageObject,
)
from ..metadata import OSFMetadataCreator
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
        from ...base.settings import ConnectorSettingIDs

        super().__init__(
            comp,
            svc,
            connector_instance=connector_instance,
            auth_channel=auth_channel,
            user_token=user_token,
            base_url=comp.data.config.value(ConnectorSettingIDs.TARGET),
            max_attempts=max_attempts,
            attempts_delay=attempts_delay,
        )

    def get_project(
        self,
        project_id: str,
        *,
        callbacks: OSFGetProjectCallbacks = OSFGetProjectCallbacks(),
    ) -> None:
        """
        Gets information about an existing project.

        Args:
            project_id: The project ID.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFProjectObject:
            resp = self.get(
                session,
                ["nodes", project_id],
            )
            return OSFRequestData.data_from_response(OSFProjectObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
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

        def _execute(session: requests.Session) -> OSFProjectObject:
            resp = self.post(
                session,
                ["nodes"],
                json=self._get_project_metadata(project),
            )
            return OSFRequestData.data_from_response(OSFProjectObject, resp)

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
        callbacks: OSFUpdateProjectCallbacks = OSFUpdateProjectCallbacks(),
    ) -> None:
        """
        Updates an existing OSF project.

        Args:
            project_id: The remote project ID.
            project: The originating project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFProjectObject:
            resp = self.patch(
                session,
                ["nodes", project_id],
                json=self._get_project_metadata(project, external_id=project_id),
            )
            return OSFRequestData.data_from_response(OSFProjectObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_project(
        self,
        osf_project: OSFProjectObject,
        *,
        callbacks: OSFDeleteProjectCallbacks = OSFDeleteProjectCallbacks(),
    ):
        """
        Deletes an existing OSF project.

        Args:
            osf_project: The OSF project.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            resp = self.delete(
                session,
                ["nodes", osf_project.project_id],
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_storage(
        self,
        osf_project: OSFProjectObject,
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

        def _execute(session: requests.Session) -> OSFStorageObject:
            resp = self.get(
                session,
                ["nodes", osf_project.project_id, "files", "providers", provider],
            )
            return OSFRequestData.data_from_response(OSFStorageObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def get_file_list(
        self,
        osf_project: OSFProjectObject,
        osf_storage: OSFStorageObject,
        *,
        callbacks: OSFGetFileListCallbacks = OSFGetFileListCallbacks(),
    ) -> None:
        """
        Retrieves the complete file list of an OSF project for a specific storage provider.

        Args:
            osf_project: The OSF project.
            osf_storage: The OSF storage.
            callbacks:  Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFFileListObject:
            resp = self.get(
                session,
                ["nodes", osf_project.project_id, "files", osf_storage.name],
            )
            return OSFRequestData.data_from_response(OSFFileListObject, resp)

        self._execute(
            cb_exec=_execute,
            cb_done=lambda data: callbacks.invoke_done_callbacks(data),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def upload_file(
        self,
        osf_storage: OSFStorageObject,
        *,
        path: str,
        file_data: ResourceBuffer,
        callbacks: OSFUploadFileCallbacks = OSFUploadFileCallbacks(),
    ) -> None:
        """
        Uploads a file to an OSF storage, creating any missing folders on the fly.

        Args:
            osf_storage: The OSF storage.
            path: The remote path of the file.
            file_data: The file data.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> OSFFileObject:
            file_path = pathlib.PurePosixPath(path)
            target_storage = self._create_directory_tree(
                session, osf_storage, path=file_path.parent
            )

            # When uploading, always seek to the beginning of the buffer, as uploads might be retried multiple times
            if file_data.seekable():
                file_data.seek(0)

            resp = self.put(
                session,
                target_storage.file_link,
                data=BytesIO(file_data.readall()),
                params={"name": file_path.name},
            )
            return OSFRequestData.data_from_response(OSFFileObject, resp)

        def _upload_done(data: OSFFileObject) -> None:
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
        osf_file: OSFFileObject,
        *,
        callbacks: OSFDeleteFileCallbacks = OSFDeleteFileCallbacks(),
    ):
        """
        Deletes an existing OSF file.

        Args:
            osf_file: The OSF file.
            callbacks: Optional request callbacks.
        """

        def _execute(session: requests.Session) -> None:
            self.delete(
                session,
                osf_file.delete_link,
            )

        self._execute(
            cb_exec=_execute,
            cb_done=lambda _: callbacks.invoke_done_callbacks(),
            cb_failed=lambda exc: callbacks.invoke_fail_callbacks(exc),
        )

    def delete_all_files(
        self,
        osf_project: OSFProjectObject,
        osf_storage: OSFStorageObject,
        *,
        callbacks: OSFDeleteAllFilesCallbacks = OSFDeleteAllFilesCallbacks(),
    ):
        """
        Deletes all files of a Zenodo project.

        Args:
            osf_project: The OSF project.
            osf_storage: The OSF storage.
            callbacks: Optional request callbacks.
        """

        def _get_file_list_done(files: OSFFileListObject):
            files_to_delete = len(files.files)
            if files_to_delete > 0:

                def _file_deleted():
                    nonlocal files_to_delete
                    files_to_delete -= 1

                    if files_to_delete <= 0:
                        callbacks.invoke_done_callbacks()

                for file in files.files:
                    delete_file_callbacks = OSFDeleteFileCallbacks()
                    delete_file_callbacks.done(_file_deleted)
                    delete_file_callbacks.failed(
                        lambda _: _file_deleted()
                    )  # We ignore errors here

                    self.delete_file(file, callbacks=delete_file_callbacks)
            else:
                callbacks.invoke_done_callbacks()

        def _get_file_list_failed(exc: Exception):
            callbacks.invoke_fail_callbacks(exc)

        file_list_callbacks = OSFGetFileListCallbacks()
        file_list_callbacks.done(_get_file_list_done)
        file_list_callbacks.failed(_get_file_list_failed)

        self.get_file_list(osf_project, osf_storage, callbacks=file_list_callbacks)

    def _create_directory_tree(
        self,
        session: requests.Session,
        osf_storage: OSFStorageObject,
        *,
        path: pathlib.PurePosixPath,
    ) -> OSFStorageObject:
        storage = osf_storage
        for entry in path.parts:
            if entry == "" or entry == "/":
                continue

            storage = self._create_directory(session, storage, name=entry)
        return storage

    def _create_directory(
        self, session: requests.Session, osf_storage: OSFStorageObject, *, name: str
    ) -> OSFStorageObject:
        # Check if the subdirectory had already been created previously
        for folder in osf_storage.folders:
            if folder.name == name:
                return folder

        # If not, create it
        resp = self.put(
            session,
            osf_storage.folder_link,
            params={"name": name},
        )

        storage_data = OSFRequestData.from_response(
            OSFStorageObject, resp, verify_response=False
        )
        if (
            storage_data.is_erroneous
            and storage_data.status_code != HTTPStatus.CONFLICT
        ):
            raise requests.RequestException(resp.reason, response=resp)
        else:
            osf_storage.folders.append(storage_data.data)
            return storage_data.data

    def _get_project_metadata(
        self, project: Project, *, external_id: str = ""
    ) -> typing.Any:
        creator = OSFMetadataCreator()
        metadata = creator.create(project.features.project_metadata.metadata)
        # creator.validate(metadata)

        return {
            "data": {
                "type": "nodes",
                "id": external_id,
                "attributes": {
                    "title": (
                        metadata.title if metadata.title else "Uploaded via Sciebo RDS"
                    ),
                    "category": (metadata.category if metadata.category else "other"),
                    "description": (
                        metadata.description if metadata.description else ""
                    ),
                },
            }
        }
