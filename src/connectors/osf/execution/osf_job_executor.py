import typing

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.project.logbook import (
    ProjectJobHistoryRecordExtData,
    ProjectJobHistoryRecordExtDataIDs,
)
from common.py.data.entities.resource import (
    files_list_from_resources_list,
    Resource,
    ResourcesList,
)
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
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
    OSFFileData,
    OSFGetStorageCallbacks,
    OSFProjectData,
    OSFStorageData,
    OSFUploadFileCallbacks,
)
from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor


class OSFJobExecutor(ConnectorJobExecutor):
    """
    Job executor for OSF.

    The executor performs the following steps:
        1. Create an OSF project
        2. Get storage information for the new project
        3. Retrieve the list of files to upload
        4. Down- and upload each file
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

        self._osf_transmission_client = OSFClient(
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

    def start(self) -> None:
        self._project_create()

    # -- Project creation

    def _project_create(self) -> None:
        self.report_message("Creating project...")

        callbacks = OSFCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_create_done(data))
        callbacks.failed(lambda reason: self._project_create_failed(reason))

        self._osf_client.create_project(self._job.project, callbacks=callbacks)

    def _project_create_done(self, osf_project: OSFProjectData) -> None:
        self.report_message(f"Project created (OSF ID: {osf_project.project_id})")

        self._storage_get(osf_project)

    def _project_create_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to create project: {reason}")

    # -- Storage retrieval

    def _storage_get(self, osf_project: OSFProjectData) -> None:
        self.report_message("Getting storage information...")

        callbacks = OSFGetStorageCallbacks()
        callbacks.done(lambda data: self._storage_fetched(osf_project, data))
        callbacks.failed(lambda reason: self._storage_failed(reason))
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._osf_client.get_storage(osf_project, callbacks=callbacks)

    def _storage_fetched(
        self, osf_project: OSFProjectData, osf_storage: OSFStorageData
    ) -> None:
        self._transmitter_prepare(osf_project, osf_storage)

    def _storage_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to get storage information: {reason}")

    # -- Transmitter preparation

    def _transmitter_prepare(
        self, osf_project: OSFProjectData, osf_storage: OSFStorageData
    ) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(
            lambda res: self._transmitter_prepare_done(
                osf_project, osf_storage, resources=res
            )
        )
        callbacks.failed(lambda reason: self._transmitter_prepare_failed(reason))
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(
        self,
        osf_project: OSFProjectData,
        osf_storage: OSFStorageData,
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
            self.set_done(ext_data=self._get_job_ext_data(osf_project))

    def _transmitter_prepare_failed(self, reason: str) -> None:
        self.set_failed(f"Failed to prepare job: {reason}")

    # -- File transfers

    def _download_files(
        self,
        osf_project: OSFProjectData,
        osf_storage: OSFStorageData,
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
        callbacks.failed(lambda res, reason: self._download_file_failed(res, reason))
        callbacks.failed(lambda _, __: self._delete_failed_project(osf_project))
        callbacks.all_done(
            lambda success: (
                self.set_done(ext_data=self._get_job_ext_data(osf_project))
                if success
                else None
            )
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_file_done(
        self,
        osf_project: OSFProjectData,
        osf_storage: OSFStorageData,
        *,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        self.report_message(f"Uploading {resource.filename}...")

        callbacks = OSFUploadFileCallbacks()
        callbacks.done(lambda data: self._upload_file_done(resource, data))
        callbacks.failed(lambda reason: self._upload_file_failed(resource, reason))
        callbacks.failed(lambda _: self._delete_failed_project(osf_project))

        self._osf_client.upload_file(
            osf_storage,
            path=relativize_path(resource.filename, self._job.project.resources_path),
            file=buffer,
            callbacks=callbacks,
        )

    def _download_file_failed(self, res: Resource, reason: str) -> None:
        self.set_failed(f"Failed to download {res.filename}: {reason}")

    def _upload_file_done(self, resource: Resource, _: OSFFileData) -> None:
        self.report_message(f"Uploaded {resource.filename}")

    def _upload_file_failed(self, res: Resource, reason: str) -> None:
        self.set_failed(f"Failed to upload {res.filename}: {reason}")

    # Miscellaneous
    def _delete_failed_project(self, osf_project: OSFProjectData) -> None:
        self._osf_client.delete_project(osf_project)

    def _get_job_ext_data(
        self, osf_project: OSFProjectData
    ) -> ProjectJobHistoryRecordExtData:
        return {ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: osf_project.project_id}
