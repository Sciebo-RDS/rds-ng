import pathlib
import random
import time

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.resource import (
    files_list_from_resources_list,
    ResourcesList,
)
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
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

        self.report_message(
            f"{len(files_list)} resources to transfer ({human_readable_file_size(resources.resource.size)})",
        )
        time.sleep(1)

        cur_file = 0

        def _file_done(res: pathlib.PurePosixPath, _: int) -> None:
            nonlocal cur_file

            cur_file += 1
            self.report(cur_file / len(files_list), f"Downloaded {res}")
            time.sleep(1)

        tunnel = MemoryBrokerTunnel()
        tunnel.begin(lambda res, _: self.report_message(f"Downloading {res}...")).done(
            _file_done
        )

        self._transmitter.download_done(lambda: self._download_done()).download_failed(
            lambda reason: self._download_failed(reason)
        ).download(tunnel=tunnel)

    def _prepare_failed(self, reason: str) -> None:
        pass

    def _download_done(self) -> None:
        self.set_done()

    def _download_failed(self, reason: str) -> None:
        pass

    def remove(self) -> None:
        pass
