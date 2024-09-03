from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
from common.py.services import Service

from ..zenodo import ZenodoClient, ZenodoCreateProjectCallbacks, ZenodoProjectData
from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor
from ...base.settings import TransmissionSettingIDs


class ZenodoJobExecutor(ConnectorJobExecutor):
    """
    Job executor for Zenodo.

    The executor performs the following steps:
        1. Create a Zenodo project
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
        super().__init__(
            comp,
            svc,
            job,
            message_builder=message_builder,
            target_channel=target_channel,
            tunnel_type=MemoryBrokerTunnel,
        )

        self._zenodo_client = ZenodoClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
        )

        self._zenodo_transmission_client = ZenodoClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
            max_attempts=comp.data.config.value(TransmissionSettingIDs.MAX_ATTEMPTS),
            attempts_delay=comp.data.config.value(
                TransmissionSettingIDs.ATTEMPTS_DELAY
            ),
        )

    def start(self) -> None:
        self._project_create()

    # -- Project creation

    def _project_create(self) -> None:
        self.report_message("Creating project...")

        callbacks = ZenodoCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_create_done(data))
        callbacks.failed(lambda reason: self._project_create_failed(reason))

        self._zenodo_client.create_project(self._job.project, callbacks=callbacks)

    def _project_create_done(self, zenodo_project: ZenodoProjectData) -> None:
        self.report_message(f"Project created (Zenodo ID: {zenodo_project.project_id})")

        # TODO: Next step

    def _project_create_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to create project: {reason}")
