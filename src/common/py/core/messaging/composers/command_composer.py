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
from ....utils.func import ExecutionCallbacks


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

        from ....component import BackendComponent
        from ....settings import NetworkSettingIDs

        self._callbacks = ExecutionCallbacks[CommandDoneCallback, CommandFailCallback]()
        self._async_callbacks = False

        self._timeout = BackendComponent.instance().data.config.value(
            NetworkSettingIDs.REGULAR_COMMAND_TIMEOUT
        )

    def done(self, callback: CommandDoneCallback) -> typing.Self:
        """
        Adds a *Done* callback.

        Args:
            callback: The callback to add.

        Returns:
            This composer instance to allow call chaining.
        """
        self._callbacks.done(callback)
        return self

    def failed(self, callback: CommandFailCallback) -> typing.Self:
        """
        Adds a *Fail* callback.

        Args:
            callback: The callback to add.

        Returns:
            This composer instance to allow call chaining.
        """
        self._callbacks.failed(callback)
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
        if self._timeout > 0.0 and len(self._callbacks.fail_callbacks) == 0:
            from ... import logging

            logging.warning(
                f"Sending a command ({self._msg_type}) with a timeout but no fail callback",
                scope="bus",
            )

    def _create_meta_information(
        self, suppress_logging: bool
    ) -> MessageMetaInformation:
        from ..meta import CommandMetaInformation

        return CommandMetaInformation(
            entrypoint=MessageMetaInformation.Entrypoint.LOCAL,
            done_callbacks=self._callbacks.done_callbacks,
            fail_callbacks=self._callbacks.fail_callbacks,
            async_callbacks=self._async_callbacks,
            timeout=self._timeout,
            suppress_logging=suppress_logging,
        )
