import typing

from ..core.logging import LoggerProtocol
from ..core.messaging.handlers import MessageContext, MessageEmitter
from ..utils.config import Configuration


class ServiceContext(MessageContext):
    """
    An execution context for messages dispatched by the message bus to a service.

    This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
    """

    def __init__(
        self,
        msg_emitter: MessageEmitter,
        logger: LoggerProtocol,
        *,
        config: Configuration
    ):
        """
        Args:
            msg_emitter: A ``MessageEmitter`` to be assigned to this context.
            logger: A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
            config: The global component configuration.
        """
        super().__init__(msg_emitter, logger)

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
