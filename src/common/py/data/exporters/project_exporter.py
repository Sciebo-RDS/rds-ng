import abc
import typing

from ..entities.project import Project
from ..entities.project.features import ProjectFeatureID

from .project_exporter_result import ProjectExporterResult

ProjectExporterID = str
ProjectExporterScope = typing.List[ProjectFeatureID]


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
        scope: ProjectExporterScope,
    ):
        """
        Args:
            exporter_id: The unique ID of the exporter.
            name: The name.
            description: The description.
            scope: The scope the exporter applies to.
        """
        self._exporter_id = exporter_id

        self._name = name
        self._description = description

        self._scope = scope

    @abc.abstractmethod
    def export(
        self, project: Project, scope: ProjectFeatureID | None = None
    ) -> ProjectExporterResult: ...

    @property
    def exporter_id(self) -> ProjectExporterID:
        """
        The ID of the exporter.
        """
        return self._exporter_id

    @property
    def name(self) -> str:
        """
        The exporter name.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        The exporter description.
        """
        return self._description

    @property
    def scope(self) -> ProjectExporterScope:
        """
        The exporter's scope.
        """
        return self._scope
