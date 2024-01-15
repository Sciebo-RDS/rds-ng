from dataclasses import dataclass, field
from enum import IntEnum

from dataclasses_json import dataclass_json

from .features import ProjectFeatures
from .project_options import ProjectOptions

ProjectID = int


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
        features: All project features.
        options: All project options.
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
    options: ProjectOptions = field(default_factory=ProjectOptions)
