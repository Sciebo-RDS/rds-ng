from dataclasses import dataclass, field
from enum import IntEnum

from dataclasses_json import dataclass_json

from .entity_types import ProjectID
from .features import ProjectFeatures


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Project:
    """
    Data for a single **Project**.

    Attributes:
        project_id: The unique project identifier.
        creation_time: A UNIX timestamp of the project creation time.
        title: The title of the project.
        description: An optional project description.
        status: The project status.
        features: All project features data.
    """

    class Status(IntEnum):
        """
        The status of a project.
        """

        ACTIVE = 0x0
        DELETED = 0xFF

    project_id: ProjectID

    creation_time: float

    title: str
    description: str

    status: Status = Status.ACTIVE

    features: ProjectFeatures = field(default_factory=ProjectFeatures)
