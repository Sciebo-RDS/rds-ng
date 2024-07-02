import io
import pathlib

from .. import ResourcesBrokerTunnel


class MemoryBrokerTunnel(ResourcesBrokerTunnel):
    """
    Tunnel based on simple in-memory buffering.
    """

    def __init__(self, resource: pathlib.PurePosixPath):
        super().__init__(resource)

        self._buffer: io.BytesIO | None = None
        self._data_ready = False

    def _transfer_init(self) -> None:
        if self._buffer is not None:
            self._buffer.close()

        self._buffer = io.BytesIO()
        self._data_ready = False

    def _transfer_finalize(self, *, success: bool = True) -> None:
        self._data_ready = success

    @property
    def read_buffer(self) -> io.RawIOBase:
        if not self._data_ready:
            raise RuntimeError(
                "Tried to access data from a tunnel that isn't ready for reading"
            )

        return self._buffer.raw

    @property
    def write_buffer(self) -> io.RawIOBase:
        if self._data_ready:
            raise RuntimeError(
                "Tried to write data to a tunnel that is already ready for reading"
            )

        return self._buffer.raw
