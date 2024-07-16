import abc
import enum
import io
import typing

from typing_extensions import Buffer

from ....core import logging
from ....data.entities.resource import Resource
from ....utils.func import CallbacksStack, CallbackType


class ResourcesBrokerTunnel(io.RawIOBase, metaclass=abc.ABCMeta):
    """
    Class used to "tunnel" the data when up-/downloading files through a broker.

    Tunnels are file-like objects and need to be used as context managers (i.e., using *with*).
    """

    class CallbackTypes(enum.StrEnum):
        OPEN = "open"
        DONE = "done"
        FAIL = "fail"
        PROGRESS = "progress"

    def __init__(self, resource: Resource):
        self._resource = resource
        self._bytes_written = 0

        self._callbacks = CallbacksStack()

    def __enter__(self) -> typing.Self:
        self._invoke_callback(ResourcesBrokerTunnel.CallbackTypes.OPEN)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            self._done()
        else:
            self._failed(str(exc_val))

            logging.warning(
                f"An exception occurred within a broker tunnel: {exc_val}",
                scope="broker",
                exception=str(exc_type),
            )

        return exc_type is None

    def _invoke_callback(self, key: CallbackTypes, *args, **kwargs) -> None:
        self._callbacks.invoke(key, self._resource, *args, **kwargs)

    def on(self, event: CallbackTypes, cb: CallbackType) -> typing.Self:
        """
        Registers a new callback for they specified event.
        Args:
            event: The event to react to.
            cb: The callback.
        """
        self._callbacks.assign(event, cb)
        return self

    def _done(self) -> None:
        self._invoke_callback(ResourcesBrokerTunnel.CallbackTypes.DONE)

    def _failed(self, reason: str) -> None:
        self._invoke_callback(ResourcesBrokerTunnel.CallbackTypes.FAIL, reason=reason)

    def _progress(self, bytes_written: int) -> None:
        self._bytes_written += bytes_written

        self._invoke_callback(
            ResourcesBrokerTunnel.CallbackTypes.PROGRESS,
            bytes_written=bytes_written,
            total_written=self._bytes_written,
        )

    # File-like interface (all need to be implemented by subclasses)

    def readable(self) -> bool:
        raise NotImplementedError()

    def read(self, size: int = -1) -> bytes | None:
        raise NotImplementedError()

    def readall(self) -> bytes | None:
        raise NotImplementedError()

    def writable(self) -> bool:
        raise NotImplementedError()

    def write(self, data: Buffer) -> int | None:
        raise NotImplementedError()

    # Default implementations

    def seek(self, *args, **kwargs):
        if not self.seekable():
            raise OSError("The tunnel isn't seekable")

    def seekable(self) -> bool:
        return False

    def close(self) -> None:
        super().close()

    @property
    def closed(self) -> bool:
        return super().closed

    def flush(self) -> None:
        super().flush()

    def readline(self, size: int | None = -1) -> bytes:
        return super().read(size)

    def readlines(self, hint: int = -1) -> list[bytes]:
        return [super().readall()]

    def readinto(self, buffer: Buffer) -> int | None:
        return super().readinto(buffer)

    def writelines(self, lines: typing.Iterable[Buffer]) -> None:
        for line in lines:
            self.write(line)

    # Behavior-defining overrides

    def isatty(self) -> bool:
        return False

    def fileno(self) -> int:
        raise OSError("The tunnel doesn't support file descriptors")

    def tell(self) -> int:
        return super().tell()

    def truncate(self, size: int | None = None) -> None:
        raise OSError("Tunnel contents can't be truncated")


ResourcesBrokerTunnelType = typing.TypeVar(
    "ResourcesBrokerTunnelType", bound=ResourcesBrokerTunnel
)
