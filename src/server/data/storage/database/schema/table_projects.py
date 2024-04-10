from sqlalchemy import MetaData, Table, Column, Integer, Unicode, Float, Text
from sqlalchemy.orm import registry

from common.py.data.entities.project import Project


def register_projects_table(metadata: MetaData, reg: registry) -> Table:
    """
    Registers the projects table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created table.
    """

    table = Table(
        "projects",
        metadata,
        Column("project_id", Integer, primary_key=True),
        Column("user_id", Unicode),
        Column("creation_time", Float),
        Column("resources_path", Text),
        Column("title", Unicode),
        Column("description", Unicode),
        Column("status", Integer),
        # TODO: Features, Options
    )

    reg.map_imperatively(Project, table)

    return table
