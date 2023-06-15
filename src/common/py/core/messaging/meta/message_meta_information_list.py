import dataclasses
import threading
import time
import typing

from ..message import Trace
from .message_meta_information import MessageMetaInformation


class MessageMetaInformationList:
    """ A thread-safe list to store meta information objects. """
    @dataclasses.dataclass(frozen=True)
    class _Entry:
        meta_information: MessageMetaInformation

        timeout: float = 0.0
        timestamp: float = dataclasses.field(default_factory=time.time)
        
        def has_timed_out(self) -> bool:
            return time.time() - self.timestamp > self.timeout if self.timeout > 0.0 else False
    
    def __init__(self):
        self._list: typing.Dict[Trace, MessageMetaInformationList._Entry] = {}
        
        self._lock = threading.Lock()
        
    def add(self, unique: Trace, meta: MessageMetaInformation, timeout: float) -> None:
        with self._lock:
            if unique not in self._list:
                self._list[unique] = MessageMetaInformationList._Entry(meta, timeout=timeout)
                
    def remove(self, unique: Trace) -> None:
        with self._lock:
            if unique in self._list:
                self._list.pop(unique)
                
    def find(self, unique: Trace) -> MessageMetaInformation | None:
        entry = self._find(unique)
        return entry.meta_information if entry is not None else None
    
    def find_timed_out_entries(self) -> typing.List[Trace]:
        with self._lock:
            return [unique for unique, entry in self._list.items() if entry.has_timed_out()]
        
    def _find(self, unique: Trace) -> _Entry | None:
        with self._lock:
            if unique in self._list:
                return self._list[unique]
        
        return None
