import dataclasses
import typing
from dataclasses import dataclass, field
from enum import IntEnum

from dataclasses_json import dataclass_json

from .entity_types import ProjectID, ProjectFeatureID
from .project_feature_store import ProjectFeatureStore


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
        features_stores: The data stores of the various project features.
        features_selection: List of enabled user-selectable features.
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

    features_stores: typing.Dict[
        ProjectFeatureID, ProjectFeatureStore
    ] = dataclasses.field(default_factory=dict)
    features_selection: typing.List[ProjectFeatureID] = dataclasses.field(
        default_factory=list
    )
