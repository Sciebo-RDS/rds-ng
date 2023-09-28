from dataclasses import dataclass

from dataclasses_json import dataclass_json

ProjectID = int


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class Project:
    """
    Data for a single **Project**.
    
    Attributes:
        project_id: The unique project identifier.
        creation_time: A UNIX timestamp of the project creation time.
        name: The name of the project.
        description: An optional project description.
    """
    project_id: ProjectID
    
    creation_time: float
    
    name: str
    description: str
