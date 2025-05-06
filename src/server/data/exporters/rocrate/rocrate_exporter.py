import json

from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    ProjectFeatureID,
    ProjectMetadataFeature,
)
from common.py.data.exporters import (
    ProjectExporter,
    ProjectExporterDescriptor,
    ProjectExporterException,
    ProjectExporterID,
    ProjectExporterResult,
)
from server.data.exporters.rocrate.utils import make_ro_crate


class ROCrateExporter(ProjectExporter):
    """
    ROCrate project exporter.
    """

    ExporterID: ProjectExporterID = "rocrate"

    def __init__(
        self,
    ):
        super().__init__(
            ROCrateExporter.ExporterID,
            name="RO-Crate",
            description="Exports to an RO-Crate (Research Object) file",
            extension="json",
            scope=[ProjectMetadataFeature.feature_id],
            capabilities=ProjectExporterDescriptor.Capabilities.AUTO_EXPORT,
            default_scope=ProjectMetadataFeature.feature_id,
            default_filename="ro-crate-metadata.json",
        )

    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult:
        if scope == ProjectMetadataFeature.feature_id:
            return self._export_project_metadata(project)

        raise ProjectExporterException(f"Unsupported scope {scope}")

    def _export_project_metadata(self, project: Project) -> ProjectExporterResult:
        crate = make_ro_crate(project=project)

        metadata_bytes = str.encode(json.dumps(crate.metadata.generate(), indent=4))

        return ProjectExporterResult(
            mimetype="application/ld+json", data=metadata_bytes
        )
