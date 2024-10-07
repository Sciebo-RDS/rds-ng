import abc

from .project_exporter_descriptor import ProjectExporterDescriptor, ProjectExporterID, ProjectExporterScope
from .project_exporter_result import ProjectExporterResult
from ..entities.project import Project
from ..entities.project.features import ProjectFeatureID


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
    ):
        """
        Args:
            exporter_id: The unique ID of the exporter.
            name: The name.
            description: The description.
            extension: The extension of exported files.
            scope: The scope the exporter applies to.
        """
        self._descriptor = ProjectExporterDescriptor(
            exporter_id=exporter_id,
            name=name,
            description=description,
            extension=extension,
            scope=scope
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
