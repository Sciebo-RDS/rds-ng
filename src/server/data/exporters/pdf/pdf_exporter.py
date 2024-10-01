from common.py.data.entities.project import Project
from common.py.data.entities.project.features import (
    DataManagementPlanFeature,
    ProjectFeatureID,
)

from common.py.data.exporters import (
    ProjectExporter,
    ProjectExporterException,
    ProjectExporterID,
    ProjectExporterResult,
)


class PDFExporter(ProjectExporter):
    """
    PDF project exporter.
    """

    ExporterID: ProjectExporterID = "pdf"

    def __init__(
        self,
    ):
        super().__init__(
            PDFExporter.ExporterID,
            name="PDF",
            description="Exports to a PDF file",
            extension="pdf",
            scope=[DataManagementPlanFeature.feature_id],
        )

    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult:
        if scope == DataManagementPlanFeature.feature_id:
            return self._export_dmp(project)

        raise ProjectExporterException(f"Unsupported scope {scope}")

    def _export_dmp(self, project: Project) -> ProjectExporterResult:
        # TODO
        return ProjectExporterResult(mimetype="text/plain", data=b"PDF stuff data")
