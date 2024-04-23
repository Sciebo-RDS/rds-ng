import uuid

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    Text,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import registry, composite, relationship

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    ProjectFeatureID,
    MetadataFeature,
    ResourcesMetadataFeature,
    DataManagementPlanFeature,
)
from common.py.data.entities.project.history import PublishingHistoryRecord

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

    # Define tables

    # -- Main

    table_projects = Table(
        "projects",
        metadata,
        # Main
        Column("project_id", Integer, primary_key=True),
        Column("user_id", String(1024)),
        Column("creation_time", Float),
        Column("resources_path", Text),
        Column("title", Text),
        Column("description", Text),
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

    # -- Features

    table_project_features = Table(
        "project_features",
        metadata,
        Column(
            "project_id", Integer, ForeignKey("projects.project_id"), primary_key=True
        ),
    )

    table_feature_metadata = Table(
        "project_feature_metadata",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_features.project_id"),
            primary_key=True,
        ),
        Column("metadata", JSONEncodedDataType),
    )

    table_feature_resources_metadata = Table(
        "project_feature_resources_metadata",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_features.project_id"),
            primary_key=True,
        ),
        Column("resources_metadata", JSONEncodedDataType),
    )

    table_feature_dmp = Table(
        "project_feature_dmp",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_features.project_id"),
            primary_key=True,
        ),
        Column("plan", JSONEncodedDataType),
    )

    # -- History

    table_project_history = Table(
        "project_history",
        metadata,
        Column(
            "project_id", Integer, ForeignKey("projects.project_id"), primary_key=True
        ),
    )

    table_history_publishing = Table(
        "project_history_publishing",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_history.project_id"),
            primary_key=True,
        ),
        Column("timestamp", Float, primary_key=True),
        Column("status", Integer),
        Column("message", Text),
    )

    # Map all tables

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
            "history": relationship(Project.History, backref="projects", uselist=False),
        },
    )

    reg.map_imperatively(
        Project.Features,
        table_project_features,
        properties={
            "metadata": relationship(
                MetadataFeature,
                backref="project_features",
                uselist=False,
            ),
            "resources_metadata": relationship(
                ResourcesMetadataFeature, backref="project_features", uselist=False
            ),
            "dmp": relationship(
                DataManagementPlanFeature, backref="project_features", uselist=False
            ),
        },
    )

    reg.map_imperatively(
        MetadataFeature,
        table_feature_metadata,
    )

    reg.map_imperatively(
        ResourcesMetadataFeature,
        table_feature_resources_metadata,
    )

    reg.map_imperatively(
        DataManagementPlanFeature,
        table_feature_dmp,
    )

    reg.map_imperatively(
        Project.History,
        table_project_history,
        properties={
            "publishing": relationship(
                PublishingHistoryRecord, backref="project_history"
            )
        },
    )

    reg.map_imperatively(
        PublishingHistoryRecord,
        table_history_publishing,
    )

    return table_projects
