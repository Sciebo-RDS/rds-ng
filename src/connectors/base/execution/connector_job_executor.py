import abc
import time
import typing

from common.py.component import BackendComponent
from common.py.core.logging import debug
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.integration.resources.transmitters import ResourcesTransmitter
from common.py.services import Service

from ..data.entities.connector import ConnectorJob


class ConnectorJobExecutor(abc.ABC):
    """
    Abstract base for job executors. A job is always executed using an executor; the executor offers various overridable methods
    and helper functions to work with a job.
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
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            job: The job (data).
            message_builder: A message builder to send messages through.
            target_channel: The target server channel.
        """
        from connectors.base.settings import TransmissionSettingIDs

        self._job = job

        self._mesage_builder = message_builder
        self._target_channel = target_channel

        self._transmitter: ResourcesTransmitter = ResourcesTransmitter(
            comp,
            svc,
            auth_channel=target_channel,
            user_token=self._job.user_token,
            broker_token=self._job.broker_token,
            max_attempts=comp.data.config.value(TransmissionSettingIDs.MAX_ATTEMPTS),
            attempts_delay=comp.data.config.value(
                TransmissionSettingIDs.ATTEMPTS_DELAY
            ),
            auth_token_refresh=False,
        )

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

    def report(self, progress: float, message: str) -> None:
        """
        Reports the current progress and activity of the job.

        Args:
            progress: The overall progress (0.0-1.0).
            message: The current activity message.
        """
        from common.py.api import ProjectJobProgressEvent

        contents: ProjectJobProgressEvent.Contents = (
            ProjectJobProgressEvent.Contents.NONE
        )

        if message != "":
            contents |= ProjectJobProgressEvent.Contents.MESSAGE

        if progress >= 0.0:
            contents |= ProjectJobProgressEvent.Contents.PROGRESS

        progress = max(0.0, min(progress, 1.0))
        ProjectJobProgressEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            contents=contents,
            progress=progress,
            message=message,
        ).emit(self._target_channel)

        self._log_debug(f"Job progression update: {message} ({progress*100:0.1f}%)")

    def report_message(self, message: str) -> None:
        """
        Reports the current activity of the job.

        Args:
            message: The current activity message.
        """
        self.report(-1.0, message)

    def report_progress(self, progress: float) -> None:
        """
        Reports the current progress of the job.

        Args:
            progress: The overall progress (0.0-1.0).
        """
        self.report(progress, "")

    def set_done(self) -> None:
        """
        Marks and reports the job as successfully finished.
        """
        from common.py.api import ProjectJobCompletionEvent
        from common.py.utils import format_elapsed_time

        self._is_active = False
        self.report(1.0, "Job completed successfully")

        ProjectJobCompletionEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            success=True,
            message=f"Job completed in {format_elapsed_time(time.time() - self._job.timestamp)}",
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
        self.report(1.0, failure_msg)

        ProjectJobCompletionEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            connector_instance=self._job.connector_instance,
            success=False,
            message=reason,
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
    def transmitter(self) -> ResourcesTransmitter | None:
        """
        The resources transmitter (if already created).
        """
        return self._transmitter

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
