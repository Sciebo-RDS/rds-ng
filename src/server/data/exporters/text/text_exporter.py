from common.py.data.entities.metadata import (
    filter_containers_ex,
    MetadataProfileContainer,
)
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
from server.data.exporters import ExporterTemplateProfileData


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

        containers = filter_containers_ex(
            ServerComponent.instance().server_data.profile_containers,
            category=DataManagementPlanFeature.feature_id,
            roles=[
                MetadataProfileContainer.Role.DEFAULT,
                MetadataProfileContainer.Role.OPTIONAL,
            ],
            enabled_profiles=project.features.dmp.enabled_metadata_profiles,
        )

        output = render_exporter_template(project, template_header)
        for container in containers:
            output += render_exporter_template(
                project,
                template_body,
                profile_data={
                    "dmp_metadata": ExporterTemplateProfileData(
                        profile=container.profile,
                        metadata=project.features.dmp.plan,
                    )
                },
            )
        return ProjectExporterResult(mimetype="text/plain", data=output.encode())
