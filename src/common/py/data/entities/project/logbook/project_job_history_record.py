from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .project_logbook_record import ProjectLogbookRecord
from ...connector import ConnectorInstanceID


@dataclass_json
@dataclass
class ProjectJobHistoryRecord(ProjectLogbookRecord):
    """
    A single record of a project's job history.

    Attributes:
        connector_instance: The connector instance ID.
        success: The success status (done or failed).
        message: An optional message (usually in case of an error).
    """

    connector_instance: ConnectorInstanceID = ""

    success: bool = True
    message: str = ""
