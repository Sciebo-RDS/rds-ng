import typing

from .project_job_history_record import ProjectJobHistoryRecord
from .project_logbook_type import ProjectLogbookType
from ...connector import ConnectorInstanceID

if typing.TYPE_CHECKING:
    from .. import Project

JobHistoryRecordFilter = typing.Callable[[ProjectJobHistoryRecord], bool]


def get_most_recent_job_history_record(
    project: "Project", record_filter: JobHistoryRecordFilter | None = None
) -> ProjectJobHistoryRecord | None:
    """
    Gets the most recent job history entry of a project.

    Args:
        project: The project.
        record_filter: An optional record filter.

    Returns:
        The most recent entry or **None** if none exists.
    """

    from .project_logbook_utils import find_logbook_by_type

    records = typing.cast(
        typing.List[ProjectJobHistoryRecord],
        find_logbook_by_type(project, ProjectLogbookType.JOB_HISTORY),
    )
    if record_filter:
        records = [record for record in records if record_filter(record)]

    if len(records) == 0:
        return None

    records.sort(reverse=True, key=lambda record: record.timestamp)
    return records[0]


def get_most_recent_job_history_record_by_connector_instance(
    project: "Project",
    connector_instance: ConnectorInstanceID,
    *,
    succeeded_only: bool = False
) -> ProjectJobHistoryRecord | None:
    """
    Gets the most recent job history entry of a project for a specific connector instnace.
    Args:
        project: The project.
        connector_instance: The connector instance ID.
        succeeded_only: Whether to include only success entries.

    Returns:
        The most recent entry or **None** if none exists.
    """

    return get_most_recent_job_history_record(
        project,
        lambda rec: (not succeeded_only or rec.success)
        and rec.connector_instance == connector_instance,
    )
