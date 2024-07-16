import io

from typing_extensions import Buffer

from .. import ResourcesBrokerTunnel
from .....data.entities.resource import Resource


class MemoryBrokerTunnel(ResourcesBrokerTunnel):
    """
    Tunnel based on simple in-memory buffering.
    """

    def __init__(self, resource: Resource):
        super().__init__(resource)

        self._buffer = io.BytesIO()
        self._data_ready = False

    def fileno(self) -> int:
        return self._buffer.fileno()

    def seek(self, *args, **kwargs):
        if self._data_ready:  # We only support seek during reads
            self._buffer.seek(*args, **kwargs)
        else:
            super().seek(*args, **kwargs)

    def seekable(self) -> bool:
        # We only support seek during reads
        return self._data_ready

    def readable(self) -> bool:
        return self._data_ready

    def read(self, size: int = -1) -> bytes | None:
        if not self.readable():
            raise RuntimeError("Tried to read from an unfinished memory broker tunnel")

        return self._buffer.read(size)

    def readall(self) -> bytes | None:
        return self.read()

    def writable(self) -> bool:
        return not self._data_ready

    def write(self, data: Buffer) -> int | None:
        if self.readable():
            raise RuntimeError("Tried to write to a finished memory broker tunnel")

        bytes_written = self._buffer.write(data)
        self._progress(bytes_written)
        return bytes_written

    def close(self) -> None:
        self._buffer.close()
        self._data_ready = False

        super().close()

    def _done(self) -> None:
        self._buffer.seek(0)
        self._data_ready = True

        super()._done()
