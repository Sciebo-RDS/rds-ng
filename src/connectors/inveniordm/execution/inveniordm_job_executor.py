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

from ..inveniordm import (
    InvenioRDMClient,
    InvenioRDMCreateProjectCallbacks,
    InvenioRDMDeleteAllFilesCallbacks,
    InvenioRDMFileObject,
    InvenioRDMGetProjectCallbacks,
    InvenioRDMProjectObject,
    InvenioRDMUpdateProjectCallbacks,
    InvenioRDMUploadFileCallbacks,
)
from ...base.data.entities.connector import ConnectorJob
from ...base.data.types import ProjectExternalStateCallbacks
from ...base.execution import ConnectorJobExecutor
from ...base.integration.execution.requests_executor import RequestsExecutorOptions
from ...base.settings import TransmissionSettingIDs


class InvenioRDMJobExecutor(ConnectorJobExecutor):
    """
    Job executor for InvenioRDM.
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
        super().__init__(
            comp,
            svc,
            job,
            message_builder=message_builder,
            target_channel=target_channel,
            tunnel_type=MemoryBrokerTunnel,
        )

        self._InvenioRDM_client = InvenioRDMClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
        )

        self._InvenioRDM_transmission_client = InvenioRDMClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
            max_attempts=comp.data.config.value(TransmissionSettingIDs.MAX_ATTEMPTS),
            attempts_delay=comp.data.config.value(
                TransmissionSettingIDs.ATTEMPTS_DELAY
            ),
        )

        self._InvenioRDM_upload_client = InvenioRDMClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
            requests_options=RequestsExecutorOptions(content_type=None),
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

        callbacks = InvenioRDMGetProjectCallbacks()
        callbacks.done(
            lambda data: self._query_external_project_state_done(data, state_callbacks)
        )
        callbacks.failed(
            lambda exc: self._query_external_project_state_failed(exc, state_callbacks)
        )

        self._InvenioRDM_client.get_project(
            external_state.external_id, callbacks=callbacks
        )

    def _query_external_project_state_done(
        self,
        inveniordm_project: InvenioRDMProjectObject,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        from .inveniordm_utils import process_external_project_state

        external_state = ProjectExternalState(
            external_id=inveniordm_project.project_id,
            external_state=ProjectExternalState.State.UNKNOWN,
        )
        process_external_project_state(inveniordm_project, external_state)

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

        callbacks = InvenioRDMCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_create_done(data))
        callbacks.failed(lambda exc: self._project_create_failed(exc))

        self._InvenioRDM_client.create_project(self._job.project, callbacks=callbacks)

    def _project_create_done(self, inveniordm_project: InvenioRDMProjectObject) -> None:
        self.report_message(
            f"Project created (InvenioRDM ID: {inveniordm_project.project_id})"
        )

        self._transmitter_prepare(inveniordm_project)

    def _project_create_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to create project: {str(exc)}")

    # -- Project update

    def _project_update(self, external_state: ProjectExternalState) -> None:
        self.report_message("Updating project...")

        callbacks = InvenioRDMUpdateProjectCallbacks()
        callbacks.done(lambda data: self._project_update_done(data))
        callbacks.failed(lambda exc: self._project_update_failed(exc))

        self._InvenioRDM_client.update_project(
            external_state.external_id, self._job.project, callbacks=callbacks
        )

    def _project_update_done(self, inveniordm_project: InvenioRDMProjectObject) -> None:
        self.report_message(
            f"Project updated (InvenioRDM ID: {inveniordm_project.project_id})"
        )

        self._project_update_cleanup(inveniordm_project)

    def _project_update_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to update project: {str(exc)}")

    def _project_update_cleanup(
        self, inveniordm_project: InvenioRDMProjectObject
    ) -> None:
        self.report_message("Clearing previous project files...")

        callbacks = InvenioRDMDeleteAllFilesCallbacks()
        callbacks.done(lambda: self._project_update_cleanup_done(inveniordm_project))
        callbacks.failed(lambda exc: self._project_update_failed(exc))

        self._InvenioRDM_client.delete_all_files(
            inveniordm_project, callbacks=callbacks
        )

    def _project_update_cleanup_done(
        self, inveniordm_project: InvenioRDMProjectObject
    ) -> None:
        self.report_message("Project cleaned up")

        self._transmitter_prepare(inveniordm_project)

    def _project_update_cleanup_failed(self, exc: Exception) -> None:
        self.set_failed(f"Unable to cleanup project: {str(exc)}")

    # -- Transmitter preparation

    def _transmitter_prepare(self, inveniordm_project: InvenioRDMProjectObject) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(
            lambda res: self._transmitter_prepare_done(
                inveniordm_project, resources=res
            )
        )
        callbacks.failed(lambda exc: self._transmitter_prepare_failed(exc))
        callbacks.failed(lambda _: self._delete_failed_project(inveniordm_project))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(
        self,
        inveniordm_project: InvenioRDMProjectObject,
        *,
        resources: ResourcesList,
    ) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )

            self._download_files(inveniordm_project, files=files_list)
        else:
            self.set_done(
                inveniordm_project.project_id,
                ext_data=self._get_job_ext_data(inveniordm_project),
            )

    def _transmitter_prepare_failed(self, exc: Exception) -> None:
        self.set_failed(f"Failed to prepare job: {str(exc)}")

    # -- File transfers

    def _download_files(
        self,
        inveniordm_project: InvenioRDMProjectObject,
        *,
        files: typing.List[Resource],
    ) -> None:
        def _report_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_file)
        callbacks.done(
            lambda res, buffer: self._download_file_done(
                inveniordm_project, resource=res, buffer=buffer
            )
        )
        callbacks.failed(lambda res, exc: self._download_file_failed(res, exc))
        callbacks.failed(lambda _, __: self._delete_failed_project(inveniordm_project))
        callbacks.all_done(
            lambda success: (
                self._upload_additional_files(inveniordm_project) if success else None
            )
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_file_done(
        self,
        inveniordm_project: InvenioRDMProjectObject,
        *,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        self.report_message(f"Uploading {resource.filename}...")

        callbacks = InvenioRDMUploadFileCallbacks()
        callbacks.done(lambda data: self._upload_file_done(resource, data))
        callbacks.failed(lambda exc: self._upload_file_failed(resource, exc))
        callbacks.failed(lambda _: self._delete_failed_project(inveniordm_project))

        self._InvenioRDM_upload_client.upload_file(
            inveniordm_project,
            path=relativize_path(resource.filename, self._job.project.resources_path),
            file_data=buffer,
            callbacks=callbacks,
        )

    def _download_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to download {res.filename}: {str(exc)}")

    def _upload_file_done(self, resource: Resource, _: InvenioRDMFileObject) -> None:
        self.report_message(f"Uploaded {resource.filename}")

    def _upload_file_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {res.filename}: {str(exc)}")

    def _upload_additional_files(
        self, inveniordm_project: InvenioRDMProjectObject
    ) -> None:
        self.report_message(f"Uploading additional files...")

        for path, file_data in self._job.additional_files.items():
            self.report_message(f"Uploading {path}...")

            callbacks = InvenioRDMUploadFileCallbacks()
            callbacks.done(lambda data: self._upload_additional_file_done(path, data))
            callbacks.failed(lambda exc: self._upload_additional_file_failed(path, exc))

            self._InvenioRDM_upload_client.upload_file(
                inveniordm_project,
                path=path,
                file_data=memory_broker_tunnel_from_data(path, file_data),
                callbacks=callbacks,
            )
        else:
            self.set_done(
                inveniordm_project.project_id,
                ext_data=self._get_job_ext_data(inveniordm_project),
            )

    def _upload_additional_file_done(self, path: str, _: InvenioRDMFileObject) -> None:
        self.report_message(f"Uploaded {path}")

    def _upload_additional_file_failed(self, path: str, exc: Exception) -> None:
        self.set_failed(f"Failed to upload {path}: {str(exc)}")

    # Miscellaneous

    def _delete_failed_project(
        self, inveniordm_project: InvenioRDMProjectObject
    ) -> None:
        if not self._reuse_external_project:
            self._InvenioRDM_client.delete_project(inveniordm_project)

    def _get_job_ext_data(
        self, inveniordm_project: InvenioRDMProjectObject
    ) -> ProjectJobHistoryRecordExtData:
        return {
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: inveniordm_project.project_id,
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_LINK: inveniordm_project.project_link,
        }
