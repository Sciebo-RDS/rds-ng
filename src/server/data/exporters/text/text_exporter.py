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
        # TODO: Use an external file
        template = """${project.title} - Data Management Plan
============================================================

% for key, value in dmp_metadata.items():
${value.label}
------------------------------------------------------------
% for item_value in value.values:
${item_value.label}
% for value_line in item_value.values:
${value_line}
% endfor

% endfor
% endfor
"""

        # TODO: Do not use a hardcoded profile
        with open("/component/common/assets/profiles/dfg.json") as file:
            profile = json.load(file)

        output = render_exporter_template(project, template, dmp_profile=profile)
        return ProjectExporterResult(mimetype="text/plain", data=output.encode())
