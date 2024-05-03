import abc
import typing

from common.py.core.logging import debug
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder

from ..data.entities.connector import ConnectorJob


class ConnectorJobExecutor(abc.ABC):
    """
    Abstract base for job executors. A job is always executed using an executor; the executor offers various overridable methods
    and helper functions to work with a job.
    """

    def __init__(
        self,
        job: ConnectorJob,
        *,
        message_builder: MessageBuilder,
        target_channel: Channel,
    ):
        """
        Args:
            job: The job (data).
            message_builder: A message builder to send messages through.
            target_channel: The target server channel.
        """
        self._job = job

        self._mesage_builder = message_builder
        self._target_channel = target_channel

        self._is_active = True

    def start(self) -> None:
        """
        Called when the job execution is started. Must always be implemented.

        If the job cannot start, an exception should be thrown.
        """
        raise NotImplementedError()

    def process(self) -> None:
        """
        Called periodically to perform recurring tasks.
        """

    def remove(self) -> None:
        """
        Called before the job is removed from the job pool.
        """

    def report_progress(self, progress: float, message: str) -> None:
        """
        Reports the current progress and activity of the job.

        Args:
            progress: The overall progress (0.0-1.0).
            message: The current activity message.
        """
        from common.py.api import ProjectJobProgressEvent

        progress = max(0.0, min(progress, 1.0))
        ProjectJobProgressEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            progress=progress,
            message=message,
        ).emit(self._target_channel)

        self._log_debug(f"Job progression update: {message} ({progress*100:0.1f}%)")

    def set_done(self) -> None:
        """
        Marks and reports the job as successfully finished.
        """
        from common.py.api import ProjectJobCompletionEvent

        self._is_active = False
        self.report_progress(1.0, "Job completed successfully")

        ProjectJobCompletionEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            success=True,
            message="Job completed successfully",
        ).emit(self._target_channel)

        self._log_debug("Job done")

    def set_failed(self, reason: str) -> None:
        """
        Marks and reports the job as failed.

        Args:
            reason: The failure reason.
        """
        from common.py.api import ProjectJobCompletionEvent

        failure_msg = f"Job failed: {reason}"

        self._is_active = False
        self.report_progress(1.0, failure_msg)

        ProjectJobCompletionEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            success=False,
            message=failure_msg,
        ).emit(self._target_channel)

        self._log_debug(failure_msg)

    def _log_debug(self, message: str) -> None:
        debug(
            message,
            scope="jobs",
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
        )

    @property
    def job(self) -> ConnectorJob:
        """
        The connector job (data).
        """
        return self._job

    @property
    def is_active(self) -> bool:
        """
        Whether the job is still running.
        """
        return self._is_active


# pylint: disable=invalid-name
ConnectorJobExecutorType = typing.TypeVar(
    "ConnectorJobExecutorType", bound=ConnectorJobExecutor
)
