import uuid

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Unicode,
    Float,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import registry, composite, relationship, mapped_column

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    ProjectFeatureID,
    MetadataFeature,
    ResourcesMetadataFeature,
    DataManagementPlanFeature,
)
from .types import JSONEncodedDataType, ArrayType


def register_projects_table(metadata: MetaData, reg: registry) -> Table:
    """
    Registers the projects table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created table.
    """

    table_projects = Table(
        "projects",
        metadata,
        # Main
        Column("project_id", Integer, primary_key=True),
        Column("user_id", Unicode),
        Column("creation_time", Float),
        Column("resources_path", Text),
        Column("title", Unicode),
        Column("description", Unicode),
        Column("status", Integer),
        # Options
        Column("opt__optional_features", ArrayType[ProjectFeatureID]),
        Column("opt__use_all_connector_instances", Boolean),
        Column(
            "opt__active_connector_instances",
            ArrayType[ConnectorInstanceID](value_conv=uuid.UUID),
        ),
        Column("opt__ui", JSONEncodedDataType),
    )

    table_project_features = Table(
        "project_features",
        metadata,
        Column(
            "project_id", Integer, ForeignKey("projects.project_id"), primary_key=True
        ),
        # Metadata
        Column("meta__metadata", JSONEncodedDataType),
        # Resources metadata
        Column("resmeta__resources_metadata", JSONEncodedDataType),
        # Data management plan
        Column("dmp__plan", JSONEncodedDataType),
    )

    reg.map_imperatively(
        Project,
        table_projects,
        properties={
            "features": relationship(
                Project.Features, backref="projects", uselist=False
            ),
            "options": composite(
                Project.Options,
                table_projects.c.opt__optional_features,
                table_projects.c.opt__use_all_connector_instances,
                table_projects.c.opt__active_connector_instances,
                table_projects.c.opt__ui,
            ),
        },
    )

    reg.map_imperatively(
        Project.Features,
        table_project_features,
        properties={
            "metadata": composite(
                MetadataFeature,
                table_project_features.c.meta__metadata,
            ),
            "resources_metadata": composite(
                ResourcesMetadataFeature,
                table_project_features.c.resmeta__resources_metadata,
            ),
            "dmp": composite(
                DataManagementPlanFeature,
                table_project_features.c.dmp__plan,
            ),
        },
    )

    return table_projects
