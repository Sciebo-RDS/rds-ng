import time

from common.py.component import BackendComponent
from common.py.services import Service


def create_stub_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """
    from .stub_backend_service_context import StubBackendServiceContext

    from common.py.api import ListProjectsCommand, ListProjectsCommandReply

    svc = comp.create_service(
        "Stub Backend service", context_type=StubBackendServiceContext
    )

    @svc.message_handler(ListProjectsCommand)
    def list_projects(msg: ListProjectsCommand, ctx: StubBackendServiceContext) -> None:
        ListProjectsCommandReply.build(
            ctx.message_builder, msg, projects=ctx.storage_pool.project_storage.list()
        )

    # Add some initial data to the in-memory storage
    _fill_stub_data()

    return svc


def _fill_stub_data():
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
