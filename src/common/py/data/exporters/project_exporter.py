import abc

from ..entities.project import Project
from ..entities.project.features import ProjectFeatureID
from .project_exporter_descriptor import (
    ProjectExporterDescriptor,
    ProjectExporterID,
    ProjectExporterScope,
)
from .project_exporter_result import ProjectExporterResult


class ProjectExporter(abc.ABC):
    """
    Base class for project exporters.
    """

    def __init__(
        self,
        exporter_id: ProjectExporterID,
        *,
        name: str,
        description: str,
        extension: str,
        scope: ProjectExporterScope,
        capabilities: ProjectExporterDescriptor.Capabilities = ProjectExporterDescriptor.Capabilities.NONE,
        default_scope: ProjectFeatureID | None = None,
        default_filename: str = ""
    ):
        """
        Args:
            exporter_id: The unique ID of the exporter.
            name: The name.
            description: The description.
            extension: The extension of exported files.
            scope: The scope the exporter applies to.
            default_scope: A default scope when exporting if none is given.
            default_filename: A default filename used when none is given.
        """
        if default_scope is not None and default_scope not in scope:
            raise RuntimeError("Invalid default scope")

        if ProjectExporterDescriptor.Capabilities.AUTO_EXPORT in capabilities:
            if default_scope is None:
                raise RuntimeError("Missing default scope for auto-export support")
            if default_filename == "":
                raise RuntimeError("Missing default filename for auto-export support")

        self._descriptor = ProjectExporterDescriptor(
            exporter_id=exporter_id,
            name=name,
            description=description,
            extension=extension,
            scope=scope,
            capabilities=capabilities,
            default_scope=default_scope,
            default_filename=default_filename,
        )

    @abc.abstractmethod
    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult: ...

    @property
    def descriptor(self) -> ProjectExporterDescriptor:
        """
        The exporter descriptor.
        """
        return self._descriptor

    @property
    def exporter_id(self) -> ProjectExporterID:
        """
        The ID of the exporter.
        """
        return self._descriptor.exporter_id

    @property
    def name(self) -> str:
        """
        The exporter name.
        """
        return self._descriptor.name

    @property
    def description(self) -> str:
        """
        The exporter description.
        """
        return self._descriptor.description

    @property
    def extension(self) -> str:
        """
        The extension of exported files.
        """
        return self._descriptor.extension

    @property
    def scope(self) -> ProjectExporterScope:
        """
        The exporter's scope.
        """
        return self._descriptor.scope

    @property
    def capabilities(self) -> ProjectExporterDescriptor.Capabilities:
        """
        The exporter's capabilities.
        """
        return self._descriptor.capabilities

    @property
    def default_scope(self) -> ProjectFeatureID | None:
        """
        The default scope when exporting if none is given.
        """
        return self._descriptor.default_scope

    @property
    def default_filename(self) -> str:
        """
        The default filename used when none is given.
        """
        return self._descriptor.default_filename
