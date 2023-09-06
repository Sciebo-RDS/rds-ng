import typing

from common.py.utils.config import Configuration
from ..composers import MessageBuilder
from ..meta import MessageMetaInformation
from ...logging import LoggerProtocol


class MessageContext:
    """
    An execution context for messages dispatched by the message bus.

    When a message handler gets executed (i.e., called by the message bus dispatchers), an instance of ``MessageContext`` (or a subclass)
    is passed to the handler. This context can be seen as a *unit of work* that exists during the execution of the handler. Its main task is to
    hold data that is specific to this single execution.

    A message context is used as a context manager. In its ``__exit__`` method, any exceptions will be catched, printed and passed on. This
    makes tracing of errors that occur during message handling easier.

    It is also possible to have message handlers receive custom subtypes of this class. See ``Component`` and its ``create_service`` method for
    details.
    """

    def __init__(
        self,
        msg_meta: MessageMetaInformation,
        msg_builder: MessageBuilder,
        *,
        logger: LoggerProtocol,
        config: Configuration,
    ):
        """
        Args:
            msg_builder: A ``MessageBuilder`` to be assigned to this context.
            msg_meta: The meta information of the message.
            logger: A logger that is configured to automatically print the trace belonging to the message that caused the handler to be executed.
            config: The global component configuration.
        """
        self._msg_meta = msg_meta
        self._msg_builder = msg_builder

        self._logger = logger
        self._config = config

        self._requires_reply = False

    def __enter__(self) -> typing.Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            import traceback

            self._logger.error(
                f"An exception occurred within a message context: {exc_val}",
                scope="bus",
                exception=str(exc_type),
            )
            self._logger.debug(
                f"Traceback:\n{''.join(traceback.format_tb(exc_tb))}", scope="bus"
            )
            return False

        self._check_command_reply()
        return True

    def __call__(self, *, requires_reply: bool) -> typing.Self:
        self._requires_reply = requires_reply
        return self

    def _check_command_reply(self) -> None:
        from ...messaging import CommandReplyType

        if (
            self._requires_reply
            and self._msg_builder.get_message_count(CommandReplyType) != 1
        ):
            self._logger.warning(
                "A message context required exactly one command reply, but either none or more than one was sent",
                scope="bus",
            )

    @property
    def is_entrypoint_local(self) -> bool:
        """
        Whether the message entered locally.
        """
        return self._msg_meta.entrypoint == MessageMetaInformation.Entrypoint.LOCAL

    @property
    def is_entrypoint_server(self) -> bool:
        """
        Whether the message entered through the server.
        """
        return self._msg_meta.entrypoint == MessageMetaInformation.Entrypoint.SERVER

    @property
    def is_entrypoint_client(self) -> bool:
        """
        Whether the message entered through the client.
        """
        return self._msg_meta.entrypoint == MessageMetaInformation.Entrypoint.CLIENT

    @property
    def message_builder(self) -> MessageBuilder:
        """
        The message builder to be used within this context.
        """
        return self._msg_builder

    @property
    def logger(self) -> LoggerProtocol:
        """
        The logger to be used within this context.
        """
        return self._logger

    @property
    def config(self) -> Configuration:
        """
        The global component configuration.
        """
        return self._config


MessageContextType = typing.TypeVar(
    "MessageContextType", bound=MessageContext
)  # pylint: disable=invalid-name
