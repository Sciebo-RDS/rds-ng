from common.py.core.logging import LoggerProtocol
from common.py.core.messaging.composers import MessageBuilder
from common.py.core.messaging.meta import MessageMetaInformation
from common.py.services import ServiceContext
from common.py.utils import UnitID
from common.py.utils.config import Configuration


class ServerServiceContext(ServiceContext):
    """
    Service context specific to the server.
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
