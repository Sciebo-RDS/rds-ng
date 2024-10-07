from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    MetadataFeature,
    ProjectFeatureID,
)

from common.py.data.exporters import (
    ProjectExporter,
    ProjectExporterException,
    ProjectExporterID,
    ProjectExporterResult,
)


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
            scope=[MetadataFeature.feature_id],
        )

    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult:
        if scope == MetadataFeature.feature_id:
            return self._export_dmp(project)

        raise ProjectExporterException(f"Unsupported scope {scope}")

    def _export_dmp(self, project: Project) -> ProjectExporterResult:
        # TODO
        return ProjectExporterResult(mimetype="text/plain", data=b"RO stuff data")
