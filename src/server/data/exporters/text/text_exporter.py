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


class TextExporter(ProjectExporter):
    """
    Text-based project exporter.
    """

    ExporterID: ProjectExporterID = "text"

    def __init__(
        self,
    ):
        super().__init__(
            TextExporter.ExporterID,
            name="Plain Text",
            description="Exports to a plain text file",
            extension="txt",
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
        return ProjectExporterResult(mimetype="text/plain", data=b"Text stuff data")
