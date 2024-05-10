import abc
import time
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ProjectLogbookRecord(abc.ABC):
    """
    Base class for all project logbook records.

    Attributes:
        record: The record entry ID.
        timestamp: The timestamp of the record.
        seen: Whether the record has been seen by the user.
    """

    record: int = 0
    timestamp: float = field(default_factory=lambda: time.time())

    seen: bool = False
