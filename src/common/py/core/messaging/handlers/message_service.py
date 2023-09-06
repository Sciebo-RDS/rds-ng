from .message_context import MessageContext, MessageContextType
from .message_handlers import MessageHandlers
from .. import MessageBusProtocol
from ..composers import MessageBuilder
from ..meta import MessageMetaInformation
from ...logging import LoggerProtocol
from ....utils import UnitID
from ....utils.config import Configuration


class MessageService:
    """
    Base class for all message services.

    A *message service* wraps message handlers and proper message context creation (i.e., using a flexible context type). It
    is used by the message bus as an encapsulated layer for message dispatching.
    """

    def __init__(
        self,
        comp_id: UnitID,
        *,
        message_bus: MessageBusProtocol,
        context_type: type[MessageContextType] = MessageContext,
    ):
        """
        Args:
            comp_id: The global component identifier.
            message_bus: The global message bus.
            context_type: The type to use when creating a message context.
        """
        self._component_id = comp_id

        self._message_bus = message_bus
        self._message_handlers = MessageHandlers()
        self._context_type = context_type

    def create_context(
        self,
        msg_meta: MessageMetaInformation,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ) -> MessageContext:
        """
        Creates a new service context.

        Args:
            msg_meta: The meta information of the message.
            logger: The logger to be used within the new context.
            config: The global component configuration.

        Returns:
            The newly created message context.
        """
        return self._context_type(
            msg_meta,
            self.create_message_builder(),
            logger=logger,
            config=config,
        )

    def create_message_builder(self) -> MessageBuilder:
        """
        Creates a new message builder.

        Returns:
            The newly created message builder.
        """
        return MessageBuilder(self._component_id, self._message_bus)

    @property
    def message_handlers(self) -> MessageHandlers:
        """
        The message handlers maintained by this message service.
        """
        return self._message_handlers
