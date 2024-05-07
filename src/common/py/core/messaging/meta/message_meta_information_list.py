import dataclasses
import threading
import time
import typing

from ..message import Trace
from .message_meta_information import MessageMetaInformation


class MessageMetaInformationList:
    """
    List to store message meta information objects.

    Notes:
        The list is thread-safe.
    """

    @dataclasses.dataclass(frozen=True)
    class _Entry:
        meta_information: MessageMetaInformation

        timeout: float = 0.0
        timestamp: float = dataclasses.field(default_factory=lambda: time.time())

        def has_timed_out(self) -> bool:
            """
            Whether the message has timed out.
            """
            return (
                time.time() - self.timestamp > self.timeout
                if self.timeout > 0.0
                else False
            )

    def __init__(self):
        self._list: typing.Dict[Trace, MessageMetaInformationList._Entry] = {}

        self._lock = threading.Lock()

    def add(self, unique: Trace, meta: MessageMetaInformation, timeout: float) -> None:
        """
        Adds a new entry to the list.

        Args:
            unique: The unique trace identifying the message.
            meta: The message meta information.
            timeout: A timeout (in seconds) after which a message is deemed timed out.
        """
        with self._lock:
            if unique not in self._list:
                self._list[unique] = MessageMetaInformationList._Entry(
                    meta, timeout=timeout
                )

    def remove(self, unique: Trace) -> None:
        """
        Removes an entry from the list.

        Args:
            unique: The unique trace identifying the message.
        """
        with self._lock:
            if unique in self._list:
                self._list.pop(unique)

    def find(self, unique: Trace) -> MessageMetaInformation | None:
        """
        Finds an entry associated with the given ``unique``.

        Args:
            unique: The unique trace identifying the message.

        Returns:
            The found meta information, if any.
        """
        entry = self._find(unique)
        return entry.meta_information if entry is not None else None

    def find_timed_out_entries(self) -> typing.List[Trace]:
        """
        Finds all entries that have timed out already.

        Returns:
            A list of all timed out entries.
        """
        with self._lock:
            return [
                unique for unique, entry in self._list.items() if entry.has_timed_out()
            ]

    def _find(self, unique: Trace) -> _Entry | None:
        with self._lock:
            if unique in self._list:
                return self._list[unique]

        return None
