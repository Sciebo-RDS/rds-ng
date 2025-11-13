import typing
from http import HTTPStatus

import requests

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.project import (
    check_reuse_external_project,
    ProjectExternalState,
)
from common.py.data.entities.project.logbook import (
    ProjectJobHistoryRecordExtData,
    ProjectJobHistoryRecordExtDataIDs,
)
from common.py.data.entities.resource import (
    files_list_from_resources_list,
    Resource,
    ResourcesList,
)
from common.py.integration.resources.brokers.tunnels import (
    memory_broker_tunnel_from_data,
    MemoryBrokerTunnel,
)
from common.py.integration.resources.transmitters import (
    ResourceBuffer,
    ResourcesTransmitterDownloadCallbacks,
    ResourcesTransmitterPrepareCallbacks,
)
from common.py.services import Service
from common.py.utils import human_readable_file_size, relativize_path

from ..osf import (
    OSFClient,
    OSFCreateProjectCallbacks,
    OSFFileObject,
    OSFGetStorageCallbacks,
    OSFProjectObject,
    OSFStorageObject,
    OSFUploadFileCallbacks,
)
from ..osf.osf_callbacks import (
    OSFDeleteAllFilesCallbacks,
    OSFGetProjectCallbacks,
    OSFUpdateProjectCallbacks,
)
from ...base.data.entities.connector import ConnectorJob
from ...base.data.types import ProjectExternalStateCallbacks
from ...base.execution import ConnectorJobExecutor


class OSFJobExecutor(ConnectorJobExecutor):
    """
    Job executor for OSF.
    """

    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        job: ConnectorJob,
        *,
        message_builder: MessageBuilder,
        target_channel: Channel,
    ):
        from ...base.settings import TransmissionSettingIDs

        super().__init__(
            comp,
            svc,
            job,
            message_builder=message_builder,
            target_channel=target_channel,
            tunnel_type=MemoryBrokerTunnel,
        )

        self._osf_client = OSFClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
        )

        self._reuse_external_project = False

    def start(self, external_state: ProjectExternalState) -> None:
        self._reuse_external_project = check_reuse_external_project(external_state)
        if self._reuse_external_project:
            self._project_update(external_state)
        else:
            self._project_create()

    # -- External state

    def query_external_project_state(
        self,
        external_state: ProjectExternalState,
        *,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        self.report_message("Querying external project...")

        callbacks = OSFGetProjectCallbacks()
        callbacks.done(
            lambda data: self._query_external_project_state_done(data, state_callbacks)
        )
        callbacks.failed(
            lambda exc: self._query_external_project_state_failed(exc, state_callbacks)
        )

        self._osf_client.get_project(external_state.external_id, callbacks=callbacks)

    def _query_external_project_state_done(
        self,
        osf_project: OSFProjectObject,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        from .osf_utils import process_external_project_state

        external_state = ProjectExternalState(
            external_id=osf_project.project_id,
            external_state=ProjectExternalState.State.UNKNOWN,
        )
        process_external_project_state(osf_project, external_state)

        state_callbacks.invoke_done_callbacks(external_state)

    def _query_external_project_state_failed(
        self,
        exc: Exception,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        if isinstance(exc, requests.exceptions.RequestException) and (
            exc.response.status_code == HTTPStatus.NOT_FOUND
            or exc.response.status_code == HTTPStatus.GONE
        ):
            self.report_message(
                "The previous project no longer exists, a new one will be created"
            )

            state_callbacks.invoke_done_callbacks(
                ProjectExternalState(
                    external_id="",
                    external_state=ProjectExternalState.State.DEFAULT,
                )
            )
        else:
            state_callbacks.invoke_fail_callbacks(str(exc))

    # -- Project creation

    def _project_create(self) -> None:
        self.report_message("Creating project...")

        callbacks = OSFCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_create_done(data))
        callbacks.failed(lambda exc: self._project_create_failed(exc))

        self._osf_client.create_project(self._job.project, callbacks=callbacks)

    def _project_create_done(self, osf_project: OSFProjectObject) -> None:
        self.report_message(f"Project created (OSF ID: {osf_project.project_id})")

        self._storage_get(osf_project, self._transmitter_prepare)

    def _project_create_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to create project: {str(exc)}")

    # -- Project update

    def _project_update(self, external_state: ProjectExternalState) -> None:
        self.report_message("Updating project...")

        callbacks = OSFUpdateProjectCallbacks()
        callbacks.done(lambda data: self._project_update_done(data))
        callbacks.failed(lambda exc: self._project_update_failed(exc))

        self._osf_client.update_project(
            external_state.external_id, self._job.project, callbacks=callbacks
        )

    def _project_update_done(self, osf_project: OSFProjectObject) -> None:
        self.report_message(f"Project updated (OSF ID: {osf_project.project_id})")

        self._storage_get(osf_project, self._project_update_cleanup)

    def _project_update_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to update project: {str(exc)}")

    def _project_update_cleanup(
        self, osf_project: OSFProjectObject, osf_storage: OSFStorageObject
    ) -> None:
        self.report_message("Clearing previous project files...")

        callbacks = OSFDeleteAllFilesCallbacks()
        callbacks.done(
            lambda: self._project_update_cleanup_done(osf_project, osf_storage)
        )
        callbacks.failed(lambda exc: self._project_update_failed(exc))

        self._osf_client.delete_all_files(osf_project, osf_storage, callbacks=callbacks)

    def _project_update_cleanup_done(
        self, osf_project: OSFProjectObject, osf_storage: OSFStorageObject
    ) -> None:
        self.report_message("Project cleaned up")

        self._transmitter_prepare(osf_project, osf_storage)

    def _project_update_cleanup_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to cleanup project: {str(exc)}")

    # -- Storage retrieval

    def _storage_get(
        self,
        osf_project: OSFProjectObject,
        cb: typing.Callable[[OSFProjectObject, OSFStorageObject], None],
    ) -> None:
        self.report_message("Getting storage information...")

        callbacks = OSFGetStorageCallbacks()
        callbacks.done(lambda data: cb(osf_project, data))
        callbacks.failed(
            lambda exc: self.set_failed(
                f"Unable to get storage information: {str(exc)}"
            )
        )
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._osf_client.get_storage(osf_project, callbacks=callbacks)

    # -- Transmitter preparation

    def _transmitter_prepare(
        self, osf_project: OSFProjectObject, osf_storage: OSFStorageObject
    ) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(
            lambda res: self._transmitter_prepare_done(
                osf_project, osf_storage, resources=res
            )
        )
        callbacks.failed(lambda exc: self._transmitter_prepare_failed(exc))
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(
        self,
        osf_project: OSFProjectObject,
        osf_storage: OSFStorageObject,
        *,
        resources: ResourcesList,
    ) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )

            self._download_files(osf_project, osf_storage, files=files_list)
        else:
            self.set_done(
                osf_project.project_id, ext_data=self._get_job_ext_data(osf_project)
            )

    def _transmitter_prepare_failed(self, exc: Exception) -> None:
        self.set_failed(f"Failed to prepare job: {str(exc)}")

    # -- File transfers

    def _download_files(
        self,
        osf_project: OSFProjectObject,
        osf_storage: OSFStorageObject,
        *,
        files: typing.List[Resource],
    ) -> None:
        def _report_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_file)
        callbacks.done(
            lambda res, buffer: self._download_file_done(
                osf_project, osf_storage, resource=res, buffer=buffer
            )
        )
        callbacks.failed(lambda res, exc: self._download_file_failed(res, exc))
        callbacks.failed(lambda _, __: self._delete_failed_project(osf_project))
        callbacks.all_done(
            lambda success: (
                self._upload_additional_files(osf_project, osf_storage)
                if success
                else None
            )
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_file_done(
        self,
        osf_project: OSFProjectObject,
        osf_storage: OSFStorageObject,
        *,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        self.report_message(f"Uploading {resource.filename}...")

        callbacks = OSFUploadFileCallbacks()
        callbacks.done(lambda data: self._upload_file_done(resource, data))
        callbacks.failed(lambda exc: self._upload_file_failed(resource, exc))
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._osf_client.upload_file(
            osf_storage,
            path=relativize_path(resource.filename, self._job.project.resources_path),
            file_data=buffer,
            callbacks=callbacks,
        )

    def _download_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to download {res.filename}: {str(exc)}")

    def _upload_file_done(self, resource: Resource, _: OSFFileObject) -> None:
        self.report_message(f"Uploaded {resource.filename}")

    def _upload_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {res.filename}: {str(exc)}")

    def _upload_additional_files(
        self, osf_project: OSFProjectObject, osf_storage: OSFStorageObject
    ) -> None:
        self.report_message(f"Uploading additional files...")

        for path, file_data in self._job.additional_files.items():
            self.report_message(f"Uploading {path}...")

            callbacks = OSFUploadFileCallbacks()
            callbacks.done(lambda data: self._upload_additional_file_done(path, data))
            callbacks.failed(lambda exc: self._upload_additional_file_failed(path, exc))

            self._osf_client.upload_file(
                osf_storage,
                path=path,
                file_data=memory_broker_tunnel_from_data(path, file_data),
                callbacks=callbacks,
            )
        else:
            self.set_done(
                osf_project.project_id,
                ext_data=self._get_job_ext_data(osf_project),
            )

    def _upload_additional_file_done(self, path: str, _: OSFFileObject) -> None:
        self.report_message(f"Uploaded {path}")

    def _upload_additional_file_failed(self, path: str, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {path}: {str(exc)}")

    # Miscellaneous

    def _delete_failed_project(self, osf_project: OSFProjectObject) -> None:
        if not self._reuse_external_project:
            self._osf_client.delete_project(osf_project)

    def _get_job_ext_data(
        self, osf_project: OSFProjectObject
    ) -> ProjectJobHistoryRecordExtData:
        return {
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: osf_project.project_id,
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_LINK: osf_project.project_link,
        }
