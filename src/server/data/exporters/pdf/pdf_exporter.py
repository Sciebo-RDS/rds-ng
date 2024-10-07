import json

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
from .. import render_exporter_template
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
        # TODO: Use an external file
        template = """= #str("${project.title}") - Data Management Plan

% for key, value in dmp_metadata.items():
== #str("${value.label}")
% for item_value in value.values:
*#str("${item_value.label}")*

% for value_line in item_value.values:
#str("${value_line}")

% endfor

% endfor
% endfor
"""

        # TODO: Do not use a hardcoded profile
        with open("/component/common/assets/profiles/dfg.json") as file:
            profile = json.load(file)

        output = render_exporter_template(project, template, dmp_profile=profile)
        pdf_data = typst_compile(output)
        return ProjectExporterResult(mimetype="text/plain", data=pdf_data)
