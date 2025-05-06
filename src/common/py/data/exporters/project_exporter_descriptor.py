import typing
from dataclasses import dataclass, field
from enum import IntFlag

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
        capabilities: Extended exporter capabilities.
        default_scope: A default scope when exporting if none is given.
        default_filename: A default filename used when none is given.
    """

    class Capabilities(IntFlag):
        """
        Flags specifying extended capabilities of the exporter.
        """

        NONE = 0
        AUTO_EXPORT = 0x0001

    exporter_id: ProjectExporterID

    name: str
    description: str
    extension: str

    scope: typing.List[ProjectFeatureID] = field(default_factory=list)

    capabilities: Capabilities

    default_scope: ProjectFeatureID | None = None
    default_filename: str = ""
