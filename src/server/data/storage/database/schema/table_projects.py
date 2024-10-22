import uuid
from dataclasses import dataclass

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    String,
    Uuid,
    Numeric,
)
from sqlalchemy.orm import registry, composite, relationship

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    ProjectFeatureID,
    ProjectMetadataFeature,
    ResourcesMetadataFeature,
    DataManagementPlanFeature,
)
from common.py.data.entities.project.logbook import ProjectJobHistoryRecord

from .types import JSONEncodedDataType, ArrayType


@dataclass(kw_only=True)
class ProjectsTables:
    main: Table

    features: Table
    feature_project_metadata: Table
    feature_resources_metadata: Table
    feature_dmp: Table

    logbook: Table
    logbook_job_history: Table


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
        Column("user_id", String(256), ForeignKey("users.user_id")),
        Column("creation_time", Numeric(32, 8, asdecimal=False)),
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

    table_feature_project_metadata = Table(
        "project_feature_project_metadata",
        metadata,
        Column(
            "project_id",
            Integer,
            ForeignKey("project_features.project_id"),
            primary_key=True,
        ),
        Column("metadata", JSONEncodedDataType),
        Column("shared_objects", JSONEncodedDataType),
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
        Column("metadata", JSONEncodedDataType),
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

    table_logbook_job_history = Table(
        "project_logbook_job_history",
        metadata,
        Column("record", Integer, primary_key=True),
        Column(
            "project_id",
            Integer,
            ForeignKey("project_logbook.project_id"),
            primary_key=True,
        ),
        Column("timestamp", Numeric(32, 8, asdecimal=False)),
        Column("seen", Boolean),
        Column("connector_instance", Uuid),
        Column("success", Boolean),
        Column("message", Text),
        Column("ext_data", JSONEncodedDataType),
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
            "project_metadata": relationship(
                ProjectMetadataFeature,
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
        ProjectMetadataFeature,
        table_feature_project_metadata,
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
                ProjectJobHistoryRecord,
                backref="project_logbook",
                cascade="all, delete",
            ),
        },
    )

    reg.map_imperatively(
        ProjectJobHistoryRecord,
        table_logbook_job_history,
    )

    return ProjectsTables(
        main=table_projects,
        features=table_project_features,
        feature_project_metadata=table_feature_project_metadata,
        feature_resources_metadata=table_feature_resources_metadata,
        feature_dmp=table_feature_dmp,
        logbook=table_project_logbook,
        logbook_job_history=table_logbook_job_history,
    )
