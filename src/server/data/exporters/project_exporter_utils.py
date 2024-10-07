from typing import Any, Dict

from mako.template import Template

from common.py.data.entities.project import Project
from common.py.data.metadata import MetadataParser


def render_exporter_template(
    project: Project,
    template: str,
    *,
    metadata_profile: Dict[str, Dict[str, Any]] | None = None,
    dmp_profile: Dict[str, Dict[str, Any]] | None = None,
) -> str:
    """
    Renders a Mako template.

    Args:
        project: The project.
        template: The Mako template.
        metadata_profile: Optional project metadata profile.
        dmp_profile: Optional DMP metadata profile.

    Returns:
        The rendered output.
    """
    # TODO: Improve metadata handling
    return Template(template).render(
        project=project,
        project_metadata=(
            MetadataParser.list_values(
                metadata_profile,
                project.features.metadata.metadata,
                project.features.metadata.shared_objects,
            )
            if metadata_profile is not None
            else {}
        ),
        dmp_metadata=(
            MetadataParser.list_values(
                dmp_profile,
                project.features.dmp.plan,
                project.features.metadata.shared_objects,
            )
            if dmp_profile is not None
            else {}
        ),
    )
