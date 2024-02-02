from common.py.core.logging import LoggerProtocol
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.data.storage import StoragePool
from common.py.utils import UnitID
from common.py.utils.config import Configuration

from ....services import GateServiceContext


class StubServiceContext(GateServiceContext):
    """
    Service context specific to the stub backend.
    """

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_origin: UnitID,
        msg_builder: MessageBuilder,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ):
        super().__init__(
            msg_meta, msg_origin, msg_builder, logger=logger, config=config
        )

        from ....data.storage.memory import MemoryStoragePool

        # Connectors are global for all users, projects are specific to each user
        self._storage_pool = MemoryStoragePool(
            connector_storage_id=None, project_storage_id=msg_origin
        )

    @property
    def storage_pool(self) -> StoragePool:
        """
        The storage pool used by the stub backend.
        """
        return self._storage_pool
