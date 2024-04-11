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
)
from sqlalchemy.orm import registry, composite

from common.py.data.entities.connector import ConnectorInstanceID
from common.py.data.entities.project import Project, ProjectOptions
from common.py.data.entities.project.features import ProjectFeatureID, ProjectFeatures
from .types import JSONEncodedDataType, ArrayType


class ProjectFeaturesType(TypeDecorator):
    """
    Database type for user settings.
    """

    impl = Unicode

    cache_ok = True

    def process_bind_param(self, value: ProjectFeatures, dialect) -> str | None:
        return value.to_json() if value is not None else None

    def process_result_value(
        self, value: str | None, dialect
    ) -> ProjectFeatures | None:
        return ProjectFeatures.schema().loads(value) if value is not None else None


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
        # Main
        Column("project_id", Integer, primary_key=True),
        Column("user_id", Unicode),
        Column("creation_time", Float),
        Column("resources_path", Text),
        Column("title", Unicode),
        Column("description", Unicode),
        Column("status", Integer),
        # Features
        Column("features", ProjectFeaturesType),
        # Options
        Column("options_optional_features", ArrayType[ProjectFeatureID]),
        Column("options_use_all_connector_instances", Boolean),
        Column(
            "options_active_connector_instances",
            ArrayType[ConnectorInstanceID](value_conv=uuid.UUID),
        ),
        Column("options_ui", JSONEncodedDataType),
    )

    reg.map_imperatively(
        Project,
        table,
        properties={
            "options": composite(
                ProjectOptions,
                table.c.options_optional_features,
                table.c.options_use_all_connector_instances,
                table.c.options_active_connector_instances,
                table.c.options_ui,
            ),
        },
    )

    return table
