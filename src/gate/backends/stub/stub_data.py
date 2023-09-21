import time


def fill_stub_data():
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
