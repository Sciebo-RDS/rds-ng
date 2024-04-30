from typing import Protocol

from common.py.core.messaging.composers import MessageBuilder

from .connector_job_executor import ConnectorJobExecutor
from ..data.entities.connector import ConnectorJob


class ConnectorJobExecutorFactory(Protocol):
    """
    Protocol used to create new connector job executors for incoming jobs.

    Notes:
        Connectors must implement this protocol in a class and provide a respective instance to the framework.
    """

    def create_executor(
        self, job: ConnectorJob, *, message_builder: MessageBuilder
    ) -> ConnectorJobExecutor: ...
