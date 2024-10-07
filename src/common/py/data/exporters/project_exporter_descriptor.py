import typing
from dataclasses import dataclass, field

from dataclasses_json.api import dataclass_json

from ..entities.project.features import ProjectFeatureID

ProjectExporterID = str
ProjectExporterScope = typing.List[ProjectFeatureID]


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ProjectExporterDescriptor:
    """
    Describes a project exporter. This class is used to easily transfer information about an exporter.

    Attributes:
        exporter_id: The global exporter ID.
        name: The display name.
        description: The exporter's description.
        extension: The extension of exported files.
        scope: The scope where the exporter applies; if empty, it applies to the overall project.
    """

    exporter_id: ProjectExporterID

    name: str
    description: str
    extension: str

    scope: typing.List[ProjectFeatureID] = field(default_factory=list)
