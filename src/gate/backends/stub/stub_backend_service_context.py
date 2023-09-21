from common.py.core.logging import LoggerProtocol
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.services import ServiceContext
from common.py.data.storage import StoragePool
from common.py.utils.config import Configuration


class StubBackendServiceContext(ServiceContext):
    """
    Service context specific to the stub backend.
    """

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_builder: MessageBuilder,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ):
        super().__init__(msg_meta, msg_builder, logger=logger, config=config)

        from ...data.storage.memory import MemoryStoragePool

        self._storage_pool = MemoryStoragePool()

    @property
    def storage_pool(self) -> StoragePool:
        return self._storage_pool
