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
    TypeDecorator,
    ForeignKey,
)
from sqlalchemy.orm import registry, composite, relationship

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    ProjectFeatureID,
    ProjectFeatures,
    MetadataFeature,
    ResourcesMetadataFeature,
    DataManagementPlanFeature,
)
from .types import JSONEncodedDataType, ArrayType


class ProjectFeaturesType(TypeDecorator):
    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: ProjectFeatures, dialect) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> ProjectFeatures | None:
        return ProjectFeatures.schema().loads(value) if value is not None else None


class MetadataFeatureType(TypeDecorator):
    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: MetadataFeature, dialect) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> MetadataFeature | None:
        return MetadataFeature.schema().loads(value) if value is not None else None


class ResourcesMetadataFeatureType(TypeDecorator):
    impl = Unicode

    cache_ok = True

    def process_bind_param(
        self, value: ResourcesMetadataFeature, dialect
    ) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> ResourcesMetadataFeature | None:
        return (
            ResourcesMetadataFeature.schema().loads(value)
            if value is not None
            else None
        )


class DataManagementPlanFeatureType(TypeDecorator):
    impl = Unicode

    cache_ok = True

    def process_bind_param(
        self, value: DataManagementPlanFeature, dialect
    ) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> DataManagementPlanFeature | None:
        return (
            DataManagementPlanFeature.schema().loads(value)
            if value is not None
            else None
        )


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
        # Features
        # Column("features", ProjectFeaturesType),
        # Options
        Column("options_optional_features", ArrayType[ProjectFeatureID]),
        Column("options_use_all_connector_instances", Boolean),
        Column(
            "options_active_connector_instances",
            ArrayType[ConnectorInstanceID](value_conv=uuid.UUID),
        ),
        Column("options_ui", JSONEncodedDataType),
    )

    table_project_features = Table(
        "project_features",
        metadata,
        Column(
            "project_id", Integer, ForeignKey("projects.project_id"), primary_key=True
        ),
        Column("metadata", MetadataFeatureType),
        Column("resources_metadata", ResourcesMetadataFeatureType),
        Column("dmp", DataManagementPlanFeatureType),
    )

    reg.map_imperatively(
        Project,
        table_projects,
        properties={
            "features": relationship(
                ProjectFeatures, backref="projects", uselist=False
            ),
            "options": composite(
                Project.Options,
                table_projects.c.options_optional_features,
                table_projects.c.options_use_all_connector_instances,
                table_projects.c.options_active_connector_instances,
                table_projects.c.options_ui,
                kw_only=True,
            ),
        },
    )
    reg.map_imperatively(ProjectFeatures, table_project_features)

    return table_projects
