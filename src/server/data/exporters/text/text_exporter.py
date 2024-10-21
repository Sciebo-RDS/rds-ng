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
        template_header = """${project.title} - Data Management Plan
============================================================

"""
        template_body = """% for key, value in dmp_metadata.items():
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
        
        from .. import render_exporter_template
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
        return ProjectExporterResult(mimetype="text/plain", data=output.encode())
