import enum
import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .project_logbook_record import ProjectLogbookRecord
from ...connector import ConnectorInstanceID

ProjectJobHistoryRecordExtData = typing.Dict[str, typing.Any]


class ProjectJobHistoryRecordExtDataIDs(enum.StrEnum):
    """
    Well-known IDs of extended data entries.
    """

    EXTERNAL_ID = "external_id"
    DOI = "doi"


@dataclass_json
@dataclass
class ProjectJobHistoryRecord(ProjectLogbookRecord):
    """
    A single record of a project's job history.

    Attributes:
        connector_instance: The connector instance ID.
        success: The success status (done or failed).
        message: An optional message (usually in case of an error).
        ext_data: Arbitrary extended data as a key-value dictionary.
    """

    connector_instance: ConnectorInstanceID = ""

    success: bool = True
    message: str = ""

    ext_data: ProjectJobHistoryRecordExtData = field(default_factory=dict)
