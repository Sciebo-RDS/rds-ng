import abc
import io
import pathlib
import typing

from ....utils import ExecutionCallbacks

BrokerTunnelBeginCallback = typing.Callable[[int], None]
BrokerTunnelProgressCallback = typing.Callable[[int, int], None]
BrokerTunnelDoneCallback = typing.Callable[[int], None]
BrokerTunnelFailCallback = typing.Callable[[str], None]


class ResourcesBrokerTunnel(abc.ABC):
    """
    Class used to "tunnel" the data when up-/downloading files through a broker.

    The created tunnel must be reusable, i.e., resources should always be allocated anew during `_transfer_init`.
    """

    def __init__(self, resource: pathlib.PurePosixPath):
        """
        Args:
            resource: The resource the tunnel operates on.
        """
        self._resource = resource

        self._start_callbacks = ExecutionCallbacks[
            BrokerTunnelBeginCallback, BrokerTunnelProgressCallback
        ]()
        self._finish_callbacks = ExecutionCallbacks[
            BrokerTunnelDoneCallback, BrokerTunnelFailCallback
        ]()

    def begin(self, cb: BrokerTunnelBeginCallback) -> typing.Self:
        """
        Adds a *Begin* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        # We are "abusing" execution callbacks here, so done == begin
        self._transfer_init()

        self._start_callbacks.done(cb)
        return self

    def progress(self, cb: BrokerTunnelProgressCallback) -> typing.Self:
        """
        Adds a *Progress* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        # We are "abusing" execution callbacks here, so fail == progress
        self._start_callbacks.failed(cb)
        return self

    def done(self, cb: BrokerTunnelDoneCallback) -> typing.Self:
        """
        Adds a *Done* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        self._finish_callbacks.done(cb)
        return self

    def failed(self, cb: BrokerTunnelFailCallback) -> typing.Self:
        """
        Adds a *Fail* callback.

        Args:
            cb: The callback to add.

        Returns:
            This instance for easy chaining.
        """
        self._finish_callbacks.failed(cb)
        return self

    def transfer_begin(self, size: int) -> None:
        """
        Called to notify the tunnel about the beginning of the transmission.

        Args:
            size: The total size (in bytes) that will be transferred.
        """
        # We are "abusing" execution callbacks here, so done == begin
        self._start_callbacks.invoke_done_callbacks(size)

    def transfer_progress(self, current: int, size: int) -> None:
        """
        Called to notify the tunnel about the progression of the transmission.

        Args:
            current: The current size (in bytes) that has been transferred.
            size: The total size (in bytes) that will be transferred.
        """
        # We are "abusing" execution callbacks here, so fail == progress
        self._start_callbacks.invoke_fail_callbacks(current, size)

    def transfer_done(self, size: int) -> None:
        """
        Called to notify the tunnel about the end of the transmission.

        Args:
            size: The total size (in bytes) that were transferred.
        """
        self._finish_callbacks.invoke_done_callbacks(size)
        self._transfer_finalize()

    def transfer_failed(self, reason: str) -> None:
        """
        Called to notify the tunnel about the failure of the transmission.

        Args:
            reason: The failure reason.
        """
        self._finish_callbacks.invoke_fail_callbacks(reason)
        self._transfer_finalize(success=False)

    def _transfer_init(self) -> None:
        pass

    def _transfer_finalize(self, *, success: bool = True) -> None:
        pass

    @property
    def resource(self) -> pathlib.PurePosixPath:
        """
        The resource the tunnel operates on.
        """
        return self._resource

    @property
    @abc.abstractmethod
    def read_buffer(self) -> io.RawIOBase:
        """
        The buffer used for reading contents.
        """
        ...

    @property
    @abc.abstractmethod
    def write_buffer(self) -> io.RawIOBase:
        """
        The buffer used for writing contents.
        """
        ...
