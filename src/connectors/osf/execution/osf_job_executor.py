import time

from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
from common.py.services import Service

from ..osf import OSFClient, OSFCreateProjectCallbacks, OSFCreateProjectData
from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor


class OSFJobExecutor(ConnectorJobExecutor):
    def __init__(
        self,
        comp: BackendComponent,
        svc: Service,
        job: ConnectorJob,
        *,
        message_builder: MessageBuilder,
        target_channel: Channel,
    ):
        from ...base.settings import TransmissionSettingIDs

        super().__init__(
            comp,
            svc,
            job,
            message_builder=message_builder,
            target_channel=target_channel,
            tunnel_type=MemoryBrokerTunnel,
        )

        self._osf_client = OSFClient(
            comp,
            svc,
            connector_instance=job.connector_instance,
            auth_channel=target_channel,
            user_token=self._job.user_token,
        )

        self._osf_transmission_client = OSFClient(
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

    def _project_create(self) -> None:
        self.report_message("Creating project...")

        callbacks = OSFCreateProjectCallbacks()
        callbacks.done(lambda data: self._project_created(data))
        callbacks.failed(lambda reason: self._project_failed(reason))

        self._osf_client.create_project(self._job.project, callbacks=callbacks)

    def _project_created(self, data: OSFCreateProjectData) -> None:
        self.report_message(f"Project created (OSF ID: {data.project_id})")
        time.sleep(5)

        print("---------------------------------------", flush=True)
        print(data.status_code, flush=True)
        print(data.error, flush=True)
        print(data.data, flush=True)
        print("---------------------------------------", flush=True)
        self.set_done()

    def _project_failed(self, reason: str) -> None:
        self.set_failed(f"Unable to create project: {reason}")
