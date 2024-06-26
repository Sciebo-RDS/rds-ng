import typing
from threading import RLock

from common.py.component import BackendComponent
from common.py.core.logging import debug
from common.py.services import ClientServiceContext, Service

from .connector_job_executor import ConnectorJobExecutor, ConnectorJobExecutorType
from ..data.entities.connector import ConnectorJob


class ConnectorJobsEngine:
    """
    Main engine to manage running executors.
    """

    def __init__(
        self,
        *,
        executor_type: type[ConnectorJobExecutorType],
    ):
        """
        Args:
            executor_type: The type to create new executors.
        """
        self._executor_type = executor_type
        self._executors: typing.List[ConnectorJobExecutor] = []

        self._lock = RLock()

    def spawn(
        self,
        comp: BackendComponent,
        svc: Service,
        job: ConnectorJob,
        ctx: ClientServiceContext,
    ) -> None:
        """
        Creates a new executor for a connector job.

        Args:
            comp: The global component.
            svc: The service used for message sending.
            job: The connector job:
            ctx: The originating message context.
        """
        with self._lock:
            executor = self._executor_type(
                comp,
                svc,
                job,
                message_builder=ctx.message_builder,
                target_channel=ctx.remote_channel,
            )

            self._executors.append(executor)
            executor.start()

            debug(
                "Spawned job executor",
                scope="engine",
                project_id=job.project.project_id,
                connector_instance=job.connector_instance,
            )

    def process(self) -> None:
        """
        Processes all running executors, purging any obsolete ones.
        """
        with self._lock:
            for executor in self._executors:
                if executor.is_active:
                    executor.process()
                else:
                    executor.remove()

                    debug(
                        "Removed job executor",
                        scope="engine",
                        project_id=executor.job.project.project_id,
                        connector_instance=executor.job.connector_instance,
                    )

            # Remove obsolete executors
            self._executors = [
                executor for executor in self._executors if executor.is_active
            ]
