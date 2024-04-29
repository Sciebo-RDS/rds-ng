from dataclasses import dataclass

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    Text,
    Uuid,
)
from sqlalchemy.orm import registry

from common.py.data.entities.project.project_job import ProjectJob


@dataclass(kw_only=True)
class ProjectJobsTables:
    main: Table


def register_project_jobs_tables(
    metadata: MetaData, reg: registry
) -> ProjectJobsTables:
    """
    Registers the project jobs table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created tables.
    """

    table_project_jobs = Table(
        "project_jobs",
        metadata,
        # Main
        Column("project_id", Integer, primary_key=True),
        Column("connector_instance", Uuid, primary_key=True),
        Column("user_id", Text),
        Column("timestamp", Float),
        # Progress
        Column("progress", Float),
        Column("message", Text),
    )

    reg.map_imperatively(
        ProjectJob,
        table_project_jobs,
    )

    return ProjectJobsTables(main=table_project_jobs)
