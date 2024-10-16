import typing

from .project_logbook_type import ProjectLogbookType
from .project_logbook_record import ProjectLogbookRecord, RecordID

if typing.TYPE_CHECKING:
    from .. import Project


def find_logbook_by_type(
    project: "Project", logbook_type: ProjectLogbookType
) -> typing.List[ProjectLogbookRecord]:
    """
    Gets the logbook with the specified type of a project.

    Args:
        project: The project.
        logbook_type: The logbook type.

    Returns:
        The project logbook (contents); if the logbook doesn't exist, an empty list is returned.
    """
    if logbook_type == ProjectLogbookType.JOB_HISTORY:
        return project.logbook.job_history

    return typing.cast(typing.List[ProjectLogbookRecord], [])


def find_logbook_record_by_id(
    records: typing.List[ProjectLogbookRecord], record: RecordID
) -> ProjectLogbookRecord | None:
    """
    Searches for a project logbook record by its record ID within a list of records.

    Args:
        records: The list of records.
        record: The record to search for.

    Returns:
        The found record or **None** otherwise.
    """

    matching_record = (rec for rec in records if rec.record == record)
    return next(matching_record, None)


def get_next_record_id(records: typing.List[ProjectLogbookRecord]) -> RecordID:
    """
    Retrieves the next record ID of the project logbook.

    Args:
        records: The existing records.

    Returns:
        The next ID, starting at 1.
    """
    return max(map(lambda rec: rec.record, records)) + 1 if len(records) > 0 else 1


def append_logbook_record(
    records: typing.List[ProjectLogbookRecord], record: ProjectLogbookRecord
) -> None:
    """
    Appends an entry to a project logbook, automatically assigning the next record ID.

    Args:
        records: The list of records.
        record: The record to append.
    """
    record.record = get_next_record_id(records)
    records.append(record)
