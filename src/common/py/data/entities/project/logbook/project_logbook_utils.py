import typing

from .project_logbook_record import ProjectLogbookRecord


def get_next_record_id(records: typing.List[ProjectLogbookRecord]) -> int:
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
