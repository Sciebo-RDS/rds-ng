from common.py.core.messaging.composers import MessageBuilder

from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor, ConnectorJobExecutorFactory


class StubJobExecutorFactory(ConnectorJobExecutorFactory):
    def create_executor(
        self, job: ConnectorJob, *, message_builder: MessageBuilder
    ) -> ConnectorJobExecutor:
        from .stub_job_executor import StubJobExecutor

        return StubJobExecutor(job, message_builder=message_builder)
