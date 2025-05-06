import abc
import time
import typing

from common.py.api import ProjectExternalStateEvent
from common.py.component import BackendComponent
from common.py.core.logging import debug
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.data.entities.connector import Connector
from common.py.data.entities.project import (
    get_last_known_external_project_state,
    ProjectExternalState,
)
from common.py.data.entities.project.logbook import ProjectJobHistoryRecordExtData
from common.py.integration.resources.brokers import ResourcesBrokerTunnelType
from common.py.integration.resources.transmitters import ResourcesTransmitter
from common.py.services import Service

from ..data.entities.connector import ConnectorJob
from ..data.types import ProjectExternalStateCallbacks


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
        tunnel_type: type[ResourcesBrokerTunnelType],
    ):
        """
        Args:
            comp: The global component.
            svc: The service used for message sending.
            job: The job (data).
            message_builder: A message builder to send messages through.
            target_channel: The target server channel.
            tunnel_type: The resources broker tunnel type to use for downloads.
        """
        from ..component import ConnectorComponent
        from ..settings import TransmissionSettingIDs

        self._job = job

        self._mesage_builder = message_builder
        self._target_channel = target_channel

        self._connector_options = typing.cast(
            ConnectorComponent, comp
        ).connector_info.options

        self._transmitter: ResourcesTransmitter = ResourcesTransmitter(
            comp,
            svc,
            auth_channel=target_channel,
            tunnel_type=tunnel_type,
            user_token=self._job.user_token,
            broker_token=self._job.broker_token,
            max_attempts=comp.data.config.value(TransmissionSettingIDs.MAX_ATTEMPTS),
            attempts_delay=comp.data.config.value(
                TransmissionSettingIDs.ATTEMPTS_DELAY
            ),
        )

        self._is_active = True

    def run(self) -> None:
        """
        Called to run the job execution.
        """

        # Get the last known external project state; this can only be DEFAULT or UPLOADED
        last_external_state = get_last_known_external_project_state(
            self._job.project, self._job.connector_instance
        )

        # If the project has already been uploaded, update its state to reflect the actual state; otherwise we can simply start the job
        if last_external_state.external_state == ProjectExternalState.State.UPLOADED:
            callbacks = ProjectExternalStateCallbacks()
            callbacks.done(lambda state: self._send_project_external_state_event(state))
            callbacks.done(lambda state: self._process_project_external_state(state))
            callbacks.failed(lambda exc: self.set_failed(str(exc)))

            self.query_external_project_state(
                last_external_state, state_callbacks=callbacks
            )
        else:
            self._send_project_external_state_event(last_external_state)
            self.start(last_external_state)

    def query_external_project_state(
        self,
        external_state: ProjectExternalState,
        *,
        state_callbacks: ProjectExternalStateCallbacks,
    ) -> None:
        """
        Queries the actual external project state from the remote service.

        Args:
            external_state: The currently stored external state.
            state_callbacks: The callbacks for asynchronous continuation.
        """

        raise NotImplementedError()

    def start(self, external_state: ProjectExternalState) -> None:
        """
        Called when the job execution is started. Must always be implemented.

        If the job cannot start, an exception should be thrown.

        Args:
            external_state: The external project state.
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

        if ProjectJobProgressEvent.Contents.MESSAGE in contents:
            if ProjectJobProgressEvent.Contents.PROGRESS in contents:
                self._log_debug(
                    f"Job progression update: {message} ({progress*100:0.1f}%)"
                )
            else:
                self._log_debug(f"Job progression update: {message}")

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

    def set_done(
        self,
        external_id: str,
        *,
        ext_data: ProjectJobHistoryRecordExtData | None = None,
    ) -> None:
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
            ext_data=ext_data,
        ).emit(self._target_channel)

        # Also refresh the external state after a completed job
        self._refresh_project_external_state(external_id)

        self._log_debug(f"Job done (external ID: {external_id})")

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

    def _refresh_project_external_state(self, external_id: str) -> None:
        callbacks = ProjectExternalStateCallbacks()
        callbacks.done(lambda state: self._send_project_external_state_event(state))

        self.query_external_project_state(
            ProjectExternalState(
                external_id=external_id,
                external_state=ProjectExternalState.State.UPLOADED,
            ),
            state_callbacks=callbacks,
        )

    def _send_project_external_state_event(
        self, external_state: ProjectExternalState
    ) -> None:
        # Notify the server about the new external state
        ProjectExternalStateEvent.build(
            self._mesage_builder,
            project_id=self._job.project.project_id,
            user_id=self._job.user_token.user_id,
            connector_instance=self._job.connector_instance,
            external_state=external_state,
        ).emit(self._target_channel)

    def _process_project_external_state(
        self, external_state: ProjectExternalState
    ) -> None:
        # Check for various fail states
        if external_state.external_state == ProjectExternalState.State.LOCKED:
            self.set_failed("The project is locked and cannot be updated anymore")
        elif (
            external_state.external_state == ProjectExternalState.State.UPLOADED
            and Connector.Options.UPLOAD_ONCE in self._connector_options
        ):
            self.set_failed("The project has already been uploaded")
        elif external_state.external_state == ProjectExternalState.State.UNKNOWN:
            self.set_failed(
                "The project is in an unknown state and cannot be updated at the moment"
            )
        else:
            # The project is in a valid state, so we can start the job
            self.start(external_state)

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
