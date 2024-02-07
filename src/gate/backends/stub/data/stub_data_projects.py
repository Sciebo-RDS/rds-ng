import time
import typing

from common.py.data.entities.project import Project, ProjectOptions


def get_stub_data_projects() -> typing.List[Project]:
    """
    Gets some hardcoded projects data.
    """

    return [
        Project(
            project_id=1000,
            creation_time=time.time(),
            resource="/data",
            title="Our first project",
            description="This is our first attempt to create a project",
            options=ProjectOptions(
                optional_features=["files", "dmp"],
                ui={"optional_snapins": ["files", "dmp"]},
            ),
        ),
        Project(
            project_id=1001,
            creation_time=time.time(),
            resource="/data/science_proj",
            title="Top-secret experiments",
            description="If you read this, the FBI is already on their way to you!",
            options=ProjectOptions(
                optional_features=["metadata", "dmp"],
                ui={"optional_snapins": ["metadata", "dmp"]},
            ),
        ),
        Project(
            project_id=1002,
            creation_time=time.time(),
            resource="/data/not_existing",
            title="This is crap",
            description="To be honest, this project sucks. It is crap. Do not even look at it!",
            options=ProjectOptions(
                optional_features=["metadata"],
                ui={"optional_snapins": ["metadata"]},
            ),
        ),
        Project(
            project_id=1003,
            creation_time=time.time(),
            resource="/data/science_proj/img",
            title="Sorry, but this project has a way too long title to be displayed",
            description="And frankly, the description should also be shorter. But that's not my fault, it is yours. Of course. BAH! Let me tell you this, never write such a LONG description, trust me, it displays totally crappy.",
            options=ProjectOptions(
                optional_features=["dmp"],
                ui={"optional_snapins": ["dmp"]},
            ),
        ),
        Project(
            project_id=1004,
            creation_time=time.time(),
            resource="/data/personal",
            title="A fine project",
            description="Last but not least, a fine one.",
        ),
    ]
