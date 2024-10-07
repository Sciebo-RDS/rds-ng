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
        # TODO: Use a mako template
        output_lines: typing.List[str] = [
            f"{project.title} - Data Management Plan",
            "============================================================",
            "",
        ]

        # TODO: Do not use a hardcoded profile
        with open("/component/common/assets/profiles/dfg.json") as file:
            profile = json.load(file)

        values = MetadataParser.list_values(
            profile, project.features.dmp.plan, project.features.metadata.shared_objects
        )

        for key, value in values.items():
            output_lines.append(f"{value.label}")
            output_lines.append(
                "------------------------------------------------------------"
            )

            for item_value in value.values:
                output_lines.append(f"{item_value.label}")
                output_lines.append("\n".join(item_value.values))
                output_lines.append("")

        output_lines.append("")

        return ProjectExporterResult(
            mimetype="text/plain", data="\n".join(output_lines).encode()
        )
