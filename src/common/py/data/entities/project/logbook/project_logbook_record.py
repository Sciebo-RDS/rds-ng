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
        timestamp: The timestamp of the record.
    """

    timestamp: float = field(default_factory=lambda: time.time())
