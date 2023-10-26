import time


def fill_stub_data() -> None:
    """
    Adds some hardcoded data to the stub data storage.
    """
    from ...data.storage.memory import MemoryStoragePool

    from common.py.data.entities import Project

    pool = (
        MemoryStoragePool()
    )  # The memory storage pool uses shared data objects, so we can fill them using a new instance

    # -- Projects
    pool.project_storage.add(
        Project(
            project_id=1000,
            creation_time=time.time(),
            name="Our first project",
            description="This is our first attempt to create a project",
        )
    )
    pool.project_storage.add(
        Project(
            project_id=1001,
            creation_time=time.time(),
            name="Top-secret experiments",
            description="If you read this, the FBI is already on their way to you!",
        )
    )
    pool.project_storage.add(
        Project(
            project_id=1002,
            creation_time=time.time(),
            name="This is crap",
            description="To be honest, this project sucks. It is crap. Do not even look at it!",
        )
    )
    pool.project_storage.add(
        Project(
            project_id=1003,
            creation_time=time.time(),
            name="Sorry, but this project has a way too long title to be displayed",
            description="And frankly, the description should also be shorter. But that's not my fault, it is yours. Of course. BAH! Let me tell you this, never write such a LONG description, trust me, it displays totally crappy.",
        )
    )
    pool.project_storage.add(
        Project(
            project_id=1004,
            creation_time=time.time(),
            name="A fine project",
            description="Last but not least, a fine one.",
        )
    )
