import json
import typing

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
from common.py.data.metadata import MetadataParser
from ....utils import typst_compile


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
        # TODO: Use a mako template
        output_lines: typing.List[str] = [
            f"= {project.title} - Data Management Plan",
            "",
        ]

        # TODO: Do not use a hardcoded profile
        with open("/component/common/assets/profiles/dfg.json") as file:
            profile = json.load(file)

        values = MetadataParser.list_values(
            profile, project.features.dmp.plan, project.features.metadata.shared_objects
        )

        for key, value in values.items():
            output_lines.append(f"== {value.label}")

            for item_value in value.values:
                output_lines.append(f"*{item_value.label}*")
                output_lines.append("")
                output_lines.append("\n".join(item_value.values))
                output_lines.append("")

        output_lines.append("")

        pdf_data = typst_compile("\n".join(output_lines))
        return ProjectExporterResult(mimetype="text/plain", data=pdf_data)
