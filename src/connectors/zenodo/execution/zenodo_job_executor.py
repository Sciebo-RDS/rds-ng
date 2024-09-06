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

from ..zenodo import (
    ZenodoClient,
    ZenodoCreateProjectCallbacks,
    ZenodoFileData,
    ZenodoProjectData,
    ZenodoUploadFileCallbacks,
)
from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor
from ...base.integration.execution.requests_executor import RequestsExecutorOptions
from ...base.settings import TransmissionSettingIDs


class ZenodoJobExecutor(ConnectorJobExecutor):
    """
    Job executor for Zenodo.

    The executor performs the following steps:
        1. Create a Zenodo project
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

        self._zenodo_client = ZenodoClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
        )

        self._zenodo_transmission_client = ZenodoClient(
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

        self._zenodo_upload_client = ZenodoClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
            requests_options=RequestsExecutorOptions(content_type=None),
        )

    def start(self) -> None:
        self._project_create()

    # -- Project creation

    def _project_create(self) -> None:
        self.report_message("Creating project...")

        callbacks = ZenodoCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_create_done(data))
        callbacks.failed(lambda reason: self._project_create_failed(reason))

        self._zenodo_client.create_project(self._job.project, callbacks=callbacks)

    def _project_create_done(self, zenodo_project: ZenodoProjectData) -> None:
        self.report_message(f"Project created (Zenodo ID: {zenodo_project.project_id})")

        self._transmitter_prepare(zenodo_project)

    def _project_create_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to create project: {reason}")

    # -- Transmitter preparation

    def _transmitter_prepare(self, zenodo_project: ZenodoProjectData) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(
            lambda res: self._transmitter_prepare_done(zenodo_project, resources=res)
        )
        callbacks.failed(lambda reason: self._transmitter_prepare_failed(reason))
        callbacks.failed(lambda _: self._delete_failed_project(zenodo_project))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(
        self,
        zenodo_project: ZenodoProjectData,
        *,
        resources: ResourcesList,
    ) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )

            self._download_files(zenodo_project, files=files_list)
        else:
            self.set_done(ext_data=self._get_job_ext_data(zenodo_project))

    def _transmitter_prepare_failed(self, reason: str) -> None:
        self.set_failed(f"Failed to prepare job: {reason}")

    # -- File transfers

    def _download_files(
        self,
        zenodo_project: ZenodoProjectData,
        *,
        files: typing.List[Resource],
    ) -> None:
        def _report_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_file)
        callbacks.done(
            lambda res, buffer: self._download_file_done(
                zenodo_project, resource=res, buffer=buffer
            )
        )
        callbacks.failed(lambda res, reason: self._download_file_failed(res, reason))
        callbacks.failed(lambda _, __: self._delete_failed_project(zenodo_project))
        callbacks.all_done(
            lambda success: (
                self.set_done(ext_data=self._get_job_ext_data(zenodo_project))
                if success
                else None
            )
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_file_done(
        self,
        zenodo_project: ZenodoProjectData,
        *,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        self.report_message(f"Uploading {resource.filename}...")

        callbacks = ZenodoUploadFileCallbacks()
        callbacks.done(lambda data: self._upload_file_done(resource, data))
        callbacks.failed(lambda reason: self._upload_file_failed(resource, reason))
        callbacks.failed(lambda _: self._delete_failed_project(zenodo_project))

        self._zenodo_upload_client.upload_file(
            zenodo_project,
            path=relativize_path(resource.filename, self._job.project.resources_path),
            file=buffer,
            callbacks=callbacks,
        )

    def _download_file_failed(self, res: Resource, reason: str) -> None:
        self.set_failed(f"Failed to download {res.filename}: {reason}")

    def _upload_file_done(self, resource: Resource, _: ZenodoFileData) -> None:
        self.report_message(f"Uploaded {resource.filename}")

    def _upload_file_failed(self, res: Resource, reason: str) -> None:
        self.set_failed(f"Failed to upload {res.filename}: {reason}")

    # Miscellaneous

    def _delete_failed_project(self, zenodo_project: ZenodoProjectData) -> None:
        self._zenodo_client.delete_project(zenodo_project)

    def _get_job_ext_data(
        self, zenodo_project: ZenodoProjectData
    ) -> ProjectJobHistoryRecordExtData:
        return {
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: zenodo_project.project_id,
        }
