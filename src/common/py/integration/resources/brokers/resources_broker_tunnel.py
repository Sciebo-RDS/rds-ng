import abc
import io
import pathlib
import typing

from ....utils.func import ExecutionCallbacks

BrokerTunnelBeginCallback = typing.Callable[[pathlib.PurePosixPath, int], None]
BrokerTunnelProgressCallback = typing.Callable[[pathlib.PurePosixPath, int, int], None]
BrokerTunnelDoneCallback = typing.Callable[[pathlib.PurePosixPath, int], None]
BrokerTunnelFailCallback = typing.Callable[[pathlib.PurePosixPath, str], None]


class ResourcesBrokerTunnel(abc.ABC):
    """
    Class used to "tunnel" the data when up-/downloading files through a broker.

    The created tunnel must be reusable, i.e., resources should always be allocated anew during `_transfer_init`.
    """

    def __init__(self):
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

    def transfer_begin(self, resource: pathlib.PurePosixPath, size: int) -> None:
        """
        Called to notify the tunnel about the beginning of the transmission.

        Args:
            resource: The resource path.
            size: The total size (in bytes) that will be transferred.
        """
        self._transfer_init(resource)

        # We are "abusing" execution callbacks here, so done == begin
        self._start_callbacks.invoke_done_callbacks(resource, size)

    def transfer_progress(
        self, resource: pathlib.PurePosixPath, current: int, size: int
    ) -> None:
        """
        Called to notify the tunnel about the progression of the transmission.

        Args:
            resource: The resource path.
            current: The current size (in bytes) that has been transferred.
            size: The total size (in bytes) that will be transferred.
        """
        # We are "abusing" execution callbacks here, so fail == progress
        self._start_callbacks.invoke_fail_callbacks(resource, current, size)

    def transfer_done(self, resource: pathlib.PurePosixPath, size: int) -> None:
        """
        Called to notify the tunnel about the end of the transmission.

        Args:
            resource: The resource path.
            size: The total size (in bytes) that were transferred.
        """
        self._transfer_finalize(resource)

        self._finish_callbacks.invoke_done_callbacks(resource, size)

    def transfer_failed(self, resource: pathlib.PurePosixPath, reason: str) -> None:
        """
        Called to notify the tunnel about the failure of the transmission.

        Args:
            resource: The resource path.
            reason: The failure reason.
        """
        self._finish_callbacks.invoke_fail_callbacks(resource, reason)
        self._transfer_finalize(resource, success=False)

    def _transfer_init(self, resource: pathlib.PurePosixPath) -> None:
        pass

    def _transfer_finalize(
        self, resource: pathlib.PurePosixPath, *, success: bool = True
    ) -> None:
        pass

    @property
    @abc.abstractmethod
    def read_buffer(self) -> io.BufferedIOBase:
        """
        The buffer used for reading contents.
        """
        ...

    @property
    @abc.abstractmethod
    def write_buffer(self) -> io.BufferedIOBase:
        """
        The buffer used for writing contents.
        """
        ...
