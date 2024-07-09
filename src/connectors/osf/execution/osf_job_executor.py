from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
from common.py.services import Service

from ..osf import OSFClient, OSFRootInformationCallbacks
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
        callbacks = OSFRootInformationCallbacks()
        callbacks.done(lambda: self.set_done())

        self._osf_client.get_root_information(callbacks=callbacks)
