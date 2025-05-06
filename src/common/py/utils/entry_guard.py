import threading
import typing


class EntryGuard:
    """
    A simple context-manager to protect functions from re-entry, usually during asynchronous execution.
    
    In order to check if the function should be executed, query the `can_execute` property.
    """
    
    _guards: typing.List[str] = []
    _lock = threading.RLock()
    
    def __init__(self, /, guard_key: str):
        self._guard_key = guard_key
        self._guard_acquired = False
        
    def __enter__(self) -> typing.Self:
        with EntryGuard._lock:
            if self._guard_key not in EntryGuard._guards:
                EntryGuard._guards.append(self._guard_key)
                self._guard_acquired = True
                
            return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with EntryGuard._lock:
            if self._guard_acquired and self._guard_key in EntryGuard._guards:
                EntryGuard._guards.remove(self._guard_key)

        return exc_type is not None

    @property
    def can_execute(self) -> bool:
        with EntryGuard._lock:
            return self._guard_acquired
