import io
import pathlib

from .. import ResourcesBrokerTunnel


class MemoryBrokerTunnel(ResourcesBrokerTunnel):
    """
    Tunnel based on simple in-memory buffering.
    """

    def __init__(self):
        super().__init__()

        self._buffer: io.BytesIO | None = None
        self._data_ready = False

    def _transfer_init(self, _: pathlib.PurePosixPath) -> None:
        if self._buffer is not None:
            self._buffer.close()

        self._buffer = io.BytesIO()
        self._data_ready = False

    def _transfer_finalize(
        self, _: pathlib.PurePosixPath, *, success: bool = True
    ) -> None:
        self._data_ready = success

    @property
    def read_buffer(self) -> io.BufferedIOBase:
        if not self._data_ready:
            raise RuntimeError(
                "Tried to access data from a tunnel that isn't ready for reading"
            )

        return self._buffer

    @property
    def write_buffer(self) -> io.BufferedIOBase:
        if self._data_ready:
            raise RuntimeError(
                "Tried to write data to a tunnel that is already ready for reading"
            )

        return self._buffer
