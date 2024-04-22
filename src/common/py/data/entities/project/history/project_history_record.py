from dataclasses import dataclass
from enum import IntEnum

from dataclasses_json import dataclass_json

ProjectFeatureID = str


@dataclass_json
@dataclass
class ProjectHistoryRecord:
    """
    A single record of a project's publishing history.

    Attributes:
        timestamp: The timestamp of the record.
        status: The status (done or failed).
        message: An optional message (usually in case of an error).
    """

    class Status(IntEnum):
        """
        The status of the publishing operation.
        """

        DONE = 0
        FAILED = -1

    timestamp: float

    status: Status
    message: str
