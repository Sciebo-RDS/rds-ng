import time

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.resource import (
    files_list_from_resources_list,
    ResourcesList,
)
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
from common.py.integration.resources.transmitters import (
    ResourcesTransmitterPrepareCallbacks,
)
from common.py.services import Service
from common.py.utils import human_readable_file_size

from ..osf import (
    OSFClient,
    OSFCreateProjectCallbacks,
    OSFGetStorageCallbacks,
    OSFProjectData,
    OSFStorageData,
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

    def _storage_get(self, osf_project: OSFProjectData) -> None:
        self.report_message("Getting storage information...")

        callbacks = OSFGetStorageCallbacks()
        callbacks.done(lambda data: self._storage_fetched(osf_project, data))
        callbacks.failed(lambda reason: self._storage_failed(reason))

        self._osf_client.get_storage(osf_project, callbacks=callbacks)

    def _storage_fetched(
        self, osf_project: OSFProjectData, osf_storage: OSFStorageData
    ) -> None:
        self._transmitter_prepare()

    def _storage_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to get storage information: {reason}")

    def _transmitter_prepare(self) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(lambda res: self._transmitter_prepare_done(res))
        callbacks.failed(lambda reason: self._transmitter_prepare_failed(reason))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _transmitter_prepare_done(self, resources: ResourcesList) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )

            # TODO
            # self._download(files_list)
        else:
            self.set_done()

    def _transmitter_prepare_failed(self, reason: str) -> None:
        self.set_failed(f"Failed to prepare job: {reason}")
