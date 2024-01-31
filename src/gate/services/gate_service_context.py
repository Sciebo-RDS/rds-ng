from common.py.core.logging import LoggerProtocol
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.services import ServiceContext
from common.py.utils.config import Configuration

from ..data.storage.session import SessionStorage


class GateServiceContext(ServiceContext):
    """
    Service context specific to the gate.
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

        self._session_storage = SessionStorage()

    @property
    def session_storage(self) -> SessionStorage:
        """
        The global session storage.
        """
        return self._session_storage
