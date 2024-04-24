from dataclasses import dataclass
from enum import IntEnum

from dataclasses_json import dataclass_json

from .project_logbook_record import ProjectLogbookRecord
from ...connector import ConnectorInstanceID


@dataclass_json
@dataclass
class PublishingHistoryRecord(ProjectLogbookRecord):
    """
    A single record of a project's publishing history.

    Attributes:
        status: The status (done or failed).
        message: An optional message (usually in case of an error).
    """

    class Status(IntEnum):
        """
        The status of the publishing operation.
        """

        DONE = 0
        FAILED = -1

    connector_instance: ConnectorInstanceID

    status: Status
    message: str
