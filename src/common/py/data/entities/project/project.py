from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Dict, Any

from dataclasses_json import dataclass_json

from .features import ProjectFeatures, ProjectFeatureID
from ..connector import ConnectorInstanceID
from ..user import UserID

ProjectID = int

UIOptions = Dict[str, Any]


@dataclass_json
@dataclass(kw_only=True)
class Project:
    """
    Data for a single **Project**.

    Attributes:
        project_id: The unique project identifier.
        user_id: The ID of the user this project belongs to.
        creation_time: A UNIX timestamp of the project creation time.
        resources_path: The resources path of the project.
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

    @dataclass_json
    @dataclass
    class Options:
        """
        Class holding all options of a **Project**.

        Attributes:
            optional_features: A list of all user-enabled optional features.
            use_all_connector_instances: Whether all available connector instances should be used.
            active_connector_instances: List of connector instances to use for the project (if *use_all_connector_instances* is false).
            ui: Arbitrary UI options.
        """

        optional_features: List[ProjectFeatureID] = field(default_factory=list)

        use_all_connector_instances: bool = True
        active_connector_instances: List[ConnectorInstanceID] = field(
            default_factory=list
        )

        ui: UIOptions = field(default_factory=dict)

    project_id: ProjectID
    user_id: UserID

    creation_time: float

    resources_path: str

    title: str
    description: str

    status: Status = Status.ACTIVE

    features: ProjectFeatures = field(default_factory=ProjectFeatures)
    options: Options = field(default_factory=Options)
