from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .project_logbook_record import ProjectLogbookRecord
from ...connector import ConnectorInstanceID


@dataclass_json
@dataclass
class PublishingJobRecord(ProjectLogbookRecord):
    """
    A single record of a project's running publication job.

    Attributes:
        connector_instance: The connector instance ID.
        progress: The total progress (0.0 - 1.0).
        message: The current activity message.
    """

    connector_instance: ConnectorInstanceID

    progress: float
    message: str
