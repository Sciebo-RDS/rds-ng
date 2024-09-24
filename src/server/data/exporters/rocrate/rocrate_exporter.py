from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    DataManagementPlanFeature,
    MetadataFeature,
    ProjectFeatureID,
)

from .. import ProjectExporter, ProjectExporterID, ProjectExporterResult


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
            name="ROCrate exporter",
            description="Exports to an RO (Research Object) Crate file",
            scope=[MetadataFeature.feature_id, DataManagementPlanFeature.feature_id],
        )

    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult:
        pass
