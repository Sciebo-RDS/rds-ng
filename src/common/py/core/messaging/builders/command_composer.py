import typing

from .message_composer import MessageComposer
from .. import (
    Message,
    MessageType,
    MessageBusProtocol,
    CommandDoneCallback,
    CommandFailCallback,
)
from ..meta import MessageMetaInformation
from ....utils import UnitID


class CommandComposer(MessageComposer):
    """
    Composer for ``Command`` messages.
    """

    def __init__(
        self,
        origin_id: UnitID,
        message_bus: MessageBusProtocol,
        msg_type: type[MessageType],
        chain: Message | None = None,
        **kwargs,
    ):
        """
        Args:
            origin_id: The component identifier of the origin of newly created messages.
            message_bus: The global message bus to use.
            msg_type: The message type.
            chain: A message that acts as the *predecessor* of the new message. Used to keep the same trace for multiple messages.
            **kwargs: Additional message parameters.
        """
        super().__init__(origin_id, message_bus, msg_type, chain, **kwargs)

        self._done_callback: CommandDoneCallback | None = None
        self._fail_callback: CommandFailCallback | None = None
        self._async_callbacks = False
        self._timeout = 0.0

    def done_callback(self, cb: CommandDoneCallback | None) -> typing.Self:
        """
        Assigns a *Done* callback.

        Args:
            cb: The callback to use.

        Returns:
            This composer instance to allow call chaining.
        """
        self._done_callback = cb
        return self

    def fail_callback(self, cb: CommandFailCallback | None) -> typing.Self:
        """
        Assigns a *Fail* callback.

        Args:
            cb: The callback to use.

        Returns:
            This composer instance to allow call chaining.
        """
        self._fail_callback = cb
        return self

    def async_callbacks(self, async_cbs: bool) -> typing.Self:
        """
        Sets whether to use asynchronous callbacks.

        Args:
            async_cbs: Enable asynchronous callbacks.

        Returns:
            This composer instance to allow call chaining.
        """
        self._async_callbacks = async_cbs
        return self

    def timeout(self, timeout: float) -> typing.Self:
        """
        Sets a reply timeout.

        Args:
            timeout: The timeout (in seconds).

        Returns:
            This composer instance to allow call chaining.
        """
        self._timeout = timeout
        return self

    def _verify(self) -> None:
        if self._timeout > 0.0 and self._fail_callback is None:
            from ... import logging

            logging.warning(
                f"Sending a command ({self._msg_type}) with a timeout but no fail callback",
                scope="bus",
            )

    def _create_meta_information(self) -> MessageMetaInformation:
        from ..meta import CommandMetaInformation

        return CommandMetaInformation(
            entrypoint=MessageMetaInformation.Entrypoint.LOCAL,
            done_callback=self._done_callback,
            fail_callback=self._fail_callback,
            async_callbacks=self._async_callbacks,
            timeout=self._timeout,
        )
