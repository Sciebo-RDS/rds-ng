import typing

from .service_context import ServiceContextType, ServiceContext
from ..core.messaging import Message, MessageType, MessageBusProtocol
from ..core.messaging.composers import MessageBuilder
from ..core.messaging.handlers import MessageHandler, MessageService
from ..utils import UnitID


@typing.final
class Service(MessageService):
    """
    Base service class providing easy message handler mapping.

    A service can be seen as the bridge between the inner workings of a component (represented by a ``Core``) and the
    outside component domain.

    Services register the various message handlers that are called when a certain message is received by the message bus and
    dispatched locally. They also create instances of ``ServiceContext`` (or a subclass) that represent a single *unit of work*
    when executing a message handler.

    Message handlers are defined using the ``message_handler`` decorator, as can be seen in this example (``svc`` being a ``Service`` instance)::

        @svc.message_handler("msg/event", Event)
        def h(msg: Event, ctx: ServiceContext) -> None:
            ctx.logger.info(f"EVENT HANDLER CALLED")
    """

    def __init__(
        self,
        comp_id: UnitID,
        name: str,
        *,
        message_bus: MessageBusProtocol,
        context_type: type[ServiceContextType] = ServiceContext,
    ):
        """
        Args:
            comp_id: The global component identifier.
            name: The service name.
            message_bus: The global message bus.
            context_type: The type to use when creating a service context.
        """
        super().__init__(comp_id, message_bus=message_bus, context_type=context_type)

        self._name = name

        self._state = type("", (), {})()

    def message_handler(
        self,
        /,
        message_type: type[MessageType] = Message,
        *,
        name_filter: str = "",
        is_async: bool = True,
    ) -> typing.Callable[[MessageHandler], MessageHandler]:
        """
        A decorator to declare a message handler.

        To define a new message handler, use the following pattern::

            @svc.message_handler("msg/event", Event)
            def h(msg: Event, ctx: ServiceContext) -> None:
                ctx.logger.info(f"EVENT HANDLER CALLED")

        Args:
            message_type: The type of the message.
            name_filter: A more generic message name filter to match against; wildcards (*) are supported as well.
            is_async: Whether to execute the handler asynchronously in its own thread.
        """

        def decorator(handler: MessageHandler) -> MessageHandler:
            self.message_handlers.add_handler(
                name_filter if name_filter != "" else message_type.message_name(),
                handler,
                message_type,
                is_async,
            )
            return handler

        return decorator

    @property
    def name(self) -> str:
        """
        The name of this service.
        """
        return self._name

    @property
    def message_builder(self) -> MessageBuilder:
        """
        The service's message builder.
        """
        return self.create_message_builder()

    @property
    def state(self) -> typing.Any:
        """
        The service's state (i.e., arbitrary data associated with the service).
        """
        return self._state

    def __str__(self) -> str:
        return self._name
