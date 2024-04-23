import abc
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ProjectHistoryRecord(abc.ABC):
    """
    Base class for all project history records.

    Attributes:
        timestamp: The timestamp of the record.
    """

    timestamp: float
