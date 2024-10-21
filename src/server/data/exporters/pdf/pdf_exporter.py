from common.py.data.entities.metadata import filter_containers, MetadataProfileContainer
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
        # TODO: Use an external file
        template_header = """= #str("${project.title}") - Data Management Plan\n\n"""
        template_body = """% for key, value in dmp_metadata.items():
== #str("${value.label}")
% for item_value in value.values:
*#str("${item_value.label}")*

% for value_line in item_value.values:
#str("${value_line}")

% endfor

% endfor
% endfor

"""

        from .. import render_exporter_template
        from ....utils import typst_compile
        from ....component import ServerComponent

        profiles = filter_containers(
            ServerComponent.instance().server_data.profile_containers,
            category=DataManagementPlanFeature.feature_id,
            role=MetadataProfileContainer.Role.GLOBAL,
        )

        output = render_exporter_template(project, template_header)
        for profile in profiles:
            output += render_exporter_template(
                project, template_body, dmp_profile=profile.profile
            )
        pdf_data = typst_compile(output)
        return ProjectExporterResult(mimetype="text/plain", data=pdf_data)
