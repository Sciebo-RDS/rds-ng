import time
import typing

from common.py.component import BackendComponent
from common.py.core import logging
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.project import ProjectExternalState
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
    ResourcesTransmitterPrepareCallbacks,
    ResourcesTransmitterDownloadCallbacks,
)
from common.py.services import Service
from common.py.utils import human_readable_file_size

from ...base.data.entities.connector import ConnectorJob
from ...base.data.types import ProjectExternalStateCallbacks
from ...base.execution import ConnectorJobExecutor


class StubJobExecutor(ConnectorJobExecutor):
    """
    Job executor for the stub connector.
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

    def query_external_project_state(
        self,
        external_state: ProjectExternalState,
        *,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        from .stub_utils import process_external_project_state

        process_external_project_state(external_state)
        state_callbacks.invoke_done_callbacks(external_state)

    def start(self, _: ProjectExternalState) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(lambda res: self._prepare_done(res))
        callbacks.failed(lambda exc: self._prepare_failed(exc))

        self._transmitter.prepare(self._job.project, callbacks=callbacks)

    def _prepare_done(self, resources: ResourcesList) -> None:
        files_list = files_list_from_resources_list(resources)

        if len(files_list) > 0:
            self.report_message(
                f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
            )
            time.sleep(1)

            self._download(files_list)
        else:
            self.set_done("<unknown>", ext_data=self._get_job_ext_data())

    def _prepare_failed(self, exc: Exception) -> None:
        self.set_failed(f"Failed to prepare job: {str(exc)}")

    def _download(self, files: typing.List[Resource]) -> None:
        def _report_each_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_each_file)
        callbacks.done(lambda res, buffer: self._download_done(res, buffer))
        callbacks.failed(lambda res, exc: self._download_failed(res, exc))
        callbacks.all_done(
            lambda _: self.set_done("<unknown>", ext_data=self._get_job_ext_data())
        )

        self._transmitter.download_list(files, callbacks=callbacks)

    def _download_done(
        self,
        resource: Resource,
        buffer: ResourceBuffer,
    ) -> None:
        logging.info(
            "Downloaded resource",
            scope="stub",
            filename=resource.filename,
            size=len(buffer.readall()),
        )

    def _download_failed(self, res: Resource, exc: Exception) -> None:
        self.set_failed(f"Failed to download {res.filename}: {str(exc)}")

    def _get_job_ext_data(self) -> ProjectJobHistoryRecordExtData:
        from common.py.utils import generate_random_string

        return {
            ProjectJobHistoryRecordExtDataIDs.EXTERNAL_ID: generate_random_string(6),
        }
