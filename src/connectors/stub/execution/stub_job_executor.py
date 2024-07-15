import time
import typing

from common.py.component import BackendComponent
from common.py.core import logging
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
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
from ...base.execution import ConnectorJobExecutor


class StubJobExecutor(ConnectorJobExecutor):
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

    def start(self) -> None:
        callbacks = ResourcesTransmitterPrepareCallbacks()
        callbacks.done(lambda res: self._prepare_done(res))
        callbacks.failed(lambda reason: self._prepare_failed(reason))

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
            self.set_done()

    def _prepare_failed(self, reason: str) -> None:
        self.set_failed(f"Failed to prepare job: {reason}")

    def _download(self, files: typing.List[Resource]) -> None:
        def _report_each_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        callbacks = ResourcesTransmitterDownloadCallbacks()
        callbacks.progress(_report_each_file)
        callbacks.done(lambda res, buffer: self._download_done(res, buffer))
        callbacks.failed(lambda res, reason: self._download_failed(res, reason))
        callbacks.all_done(lambda _: self.set_done())

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

    def _download_failed(self, res: Resource, reason: str) -> None:
        self.set_failed(f"Failed to download {res.filename}: {reason}")
