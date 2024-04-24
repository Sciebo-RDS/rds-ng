import abc
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ProjectLogbookRecord(abc.ABC):
    """
    Base class for all project logbook records.

    Attributes:
        timestamp: The timestamp of the record.
    """

    timestamp: float
