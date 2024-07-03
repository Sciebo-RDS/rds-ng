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
from common.py.integration.resources.transmitters import ResourceBuffer
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
        )

    def start(self) -> None:
        self._transmitter.prepare_done(
            lambda res: self._prepare_done(res)
        ).prepare_failed(lambda reason: self._prepare_failed(reason)).prepare(
            self._job.project
        )

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
        self._transmitter.download_done(
            lambda res, buffer: self._download_done(res, buffer)
        ).download_failed(lambda res, reason: self._download_failed(res, reason))

        def _report_each_file(res: Resource, current: int, total: int) -> None:
            self.report(current / total, f"Downloading {res.filename}...")

        self._transmitter.download_list(
            files,
            tunnel_type=MemoryBrokerTunnel,
            cb_each=_report_each_file,
            cb_done=lambda: self.set_done(),
        )

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
