import dataclasses
import threading
import typing

from ..message import Trace
from .message_meta_information import MessageMetaInformation


class MessageMetaInformationList:
    """ A thread-safe list to store meta information objects. """
    @dataclasses.dataclass(frozen=True)
    class _Entry:
        meta_information: MessageMetaInformation
    
    def __init__(self):
        self._list: typing.Dict[Trace, MessageMetaInformationList._Entry] = {}
        
        self._lock = threading.Lock()
        
    def add(self, unique: Trace, meta: MessageMetaInformation) -> None:
        with self._lock:
            if unique not in self._list:
                self._list[unique] = MessageMetaInformationList._Entry(meta)
                
    def remove(self, unique: Trace) -> None:
        with self._lock:
            if unique in self._list:
                self._list.pop(unique)
                
    def find(self, unique: Trace) -> MessageMetaInformation | None:
        with self._lock:
            if unique in self._list:
                return self._list[unique].meta_information
            
        return None
