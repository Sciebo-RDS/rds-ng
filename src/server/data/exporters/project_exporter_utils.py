import typing
from dataclasses import dataclass
from typing import Any, Dict, List

from mako.template import Template

from common.py.data.entities.project import Project
from common.py.data.metadata import MetadataParser, MetadataValueList


@dataclass(kw_only=True, frozen=True)
class ExporterTemplateProfileData:
    """
    Additional profile data for rendering exporter templates.
    """

    profile: Dict[str, Dict[str, Any]]
    metadata: List[Dict[str, Any]]


def render_exporter_template(
    project: Project,
    template: str,
    *,
    profile_data: Dict[str, ExporterTemplateProfileData] | None = None,
) -> str:
    """
    Renders a Mako template.

    Args:
        project: The project.
        template: The Mako template.
        profile_data: Optional profile data.

    Returns:
        The rendered output.
    """
    data_params: typing.Dict[str, MetadataValueList] = {}

    if profile_data is not None:
        for name, data in profile_data.items():
            data_params[name] = MetadataParser.list_values(
                data.profile,
                data.metadata,
                project.features.metadata.shared_objects,
            )

    return Template(template).render(project=project, **data_params)
