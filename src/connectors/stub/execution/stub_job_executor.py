import logging
import random
import time

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.resource import ResourcesList
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

        self._start_tick = 0
        self._job_time = 1

    def start(self) -> None:
        self._transmitter.prepare_done(
            lambda res: self._prepare_done(res)
        ).prepare_failed(lambda reason: self._prepare_failed(reason)).prepare(
            self._job.project
        )

    def process(self) -> None:
        progress = (time.time() - self._start_tick) / self._job_time
        self.report(progress, f"I have already done {progress*100:0.1f}%")

        if progress >= 1.0:
            (
                self.set_done()
                if random.uniform(0.0, 1.0) <= 0.8
                else self.set_failed("Totally random failure")
            )

    def _prepare_done(self, resources: ResourcesList) -> None:
        self._start_tick = time.time()
        self._job_time = random.uniform(10.0, 20.0)

        self.report_message(
            f"I got loads of resources to transfer: {human_readable_file_size(resources.resource.size)}",
        )

    def _prepare_failed(self, reason: str) -> None:
        pass

    def remove(self) -> None:
        pass
