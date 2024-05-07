import random
import time

from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder

from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor


class StubJobExecutor(ConnectorJobExecutor):
    def __init__(
        self,
        job: ConnectorJob,
        *,
        message_builder: MessageBuilder,
        target_channel: Channel,
    ):
        super().__init__(
            job, message_builder=message_builder, target_channel=target_channel
        )

        self._start_tick = 0
        self._job_time = 1

    def start(self) -> None:
        self._start_tick = time.time()
        self._job_time = random.uniform(5.0, 10.0)

    def process(self) -> None:
        progress = (time.time() - self._start_tick) / self._job_time
        self.report_progress(progress, f"I have already done {progress*100:0.1f}%")

        if progress >= 1.0:
            (
                self.set_done()
                if random.uniform(0.0, 1.0) <= 0.8
                else self.set_failed("Totally random failure")
            )

    def remove(self) -> None:
        pass
