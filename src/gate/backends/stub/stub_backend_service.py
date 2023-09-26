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
            ctx.message_builder, msg, projects=ctx.storage_pool.project_storage.list(), success=False, message="NE ALTER SO NICHT"
        ).emit()

    # Add some initial data to the in-memory storage
    from .stub_data import fill_stub_data

    fill_stub_data()

    return svc
