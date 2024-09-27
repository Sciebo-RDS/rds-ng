from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    DataManagementPlanFeature,
    MetadataFeature,
    ProjectFeatureID,
)

from common.py.data.exporters import (
    ProjectExporter,
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
            name="ROCrate",
            description="Exports to an RO (Research Object) Crate file",
            scope=[MetadataFeature.feature_id],
        )

    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult:
        # TODO
        return ProjectExporterResult(mimetype="text/plain", data=b"RO stuff data")
