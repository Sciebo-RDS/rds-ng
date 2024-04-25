import uuid
from dataclasses import dataclass

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
from common.py.data.entities.project.logbook import JobHistoryRecord

from .types import JSONEncodedDataType, ArrayType


@dataclass(kw_only=True)
class ProjectsTables:
    main: Table

    features: Table
    feature_metadata: Table
    feature_resources_metadata: Table
    feature_dmp: Table

    logbook: Table
    logbook_publishing_history: Table


def register_projects_tables(metadata: MetaData, reg: registry) -> ProjectsTables:
    """
    Registers the projects table.

    Args:
        metadata: The metadata object.
        reg: The mapper registry.

    Returns:
        The newly created tables.
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

    # -- Logbook

    table_project_logbook = Table(
        "project_logbook",
        metadata,
        Column(
            "project_id", Integer, ForeignKey("projects.project_id"), primary_key=True
        ),
    )

    table_logbook_publishing_history = Table(
        "project_logbook_publishing_history",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_logbook.project_id"),
            primary_key=True,
        ),
        Column("timestamp", Float, primary_key=True),
        Column("connector_instance", String(64), primary_key=True),
        Column("status", Integer),
        Column("message", Text),
    )

    # Map all tables

    reg.map_imperatively(
        Project,
        table_projects,
        properties={
            "features": relationship(
                Project.Features,
                backref="projects",
                uselist=False,
                cascade="all, delete",
            ),
            "options": composite(
                Project.Options,
                table_projects.c.opt__optional_features,
                table_projects.c.opt__use_all_connector_instances,
                table_projects.c.opt__active_connector_instances,
                table_projects.c.opt__ui,
            ),
            "logbook": relationship(
                Project.Logbook,
                backref="projects",
                uselist=False,
                cascade="all, delete",
            ),
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
                cascade="all, delete",
            ),
            "resources_metadata": relationship(
                ResourcesMetadataFeature,
                backref="project_features",
                uselist=False,
                cascade="all, delete",
            ),
            "dmp": relationship(
                DataManagementPlanFeature,
                backref="project_features",
                uselist=False,
                cascade="all, delete",
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
        Project.Logbook,
        table_project_logbook,
        properties={
            "job_history": relationship(
                JobHistoryRecord,
                backref="project_logbook",
                cascade="all, delete",
            ),
        },
    )

    reg.map_imperatively(
        JobHistoryRecord,
        table_logbook_publishing_history,
    )

    return ProjectsTables(
        main=table_projects,
        features=table_project_features,
        feature_metadata=table_feature_metadata,
        feature_resources_metadata=table_feature_resources_metadata,
        feature_dmp=table_feature_dmp,
        logbook=table_project_logbook,
        logbook_publishing_history=table_logbook_publishing_history,
    )
