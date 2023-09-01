import typing

from ..core.logging import LoggerProtocol
from ..core.messaging.composers import MessageBuilder
from ..core.messaging.handlers import MessageContext
from ..core.messaging.meta import MessageMetaInformation
from ..utils.config import Configuration


class ServiceContext(MessageContext):
    """
    An execution context for messages dispatched by the message bus to a service.

    This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
    """

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_builder: MessageBuilder,
        logger: LoggerProtocol,
        *,
        config: Configuration
    ):
        """
        Args:
            msg_meta: The meta information of the message.
            msg_builder: A ``MessageBuilder`` to be assigned to this context.
            logger: A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
            config: The global component configuration.
        """
        super().__init__(msg_meta, msg_builder, logger)

        self._config = config

    @property
    def config(self) -> Configuration:
        """
        The global component configuration.
        """
        return self._config


ServiceContextType = typing.TypeVar(
    "ServiceContextType", bound=ServiceContext
)  # pylint: disable=invalid-name
