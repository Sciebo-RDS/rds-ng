import typing

from ..core.messaging.handlers import MessageContext


class ServiceContext(MessageContext):
    """
    An execution context for messages dispatched by the message bus to a service.

    This class is an extension to the more general ``MessageContext`` specifically used by ``Service`` and its message handlers.
    """


ServiceContextType = typing.TypeVar(
    "ServiceContextType", bound=ServiceContext
)  # pylint: disable=invalid-name
