from common.py.component import BackendComponent
from common.py.core.messaging import Channel
from common.py.core.messaging.composers import MessageBuilder
from common.py.integration.resources.brokers.tunnels import MemoryBrokerTunnel
from common.py.services import Service

from ..zenodo import ZenodoClient
from ...base.data.entities.connector import ConnectorJob
from ...base.execution import ConnectorJobExecutor
from ...base.settings import TransmissionSettingIDs


class ZenodoJobExecutor(ConnectorJobExecutor):
    """
    Job executor for Zenodo.

    The executor performs the following steps:

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
        self.set_done()
