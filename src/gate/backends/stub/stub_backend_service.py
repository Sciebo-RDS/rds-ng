from common.py.api import DeleteProjectCommand, DeleteProjectReply
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

    from common.py.api import ListProjectsCommand, ListProjectsReply

    svc = comp.create_service(
        "Stub Backend service", context_type=StubBackendServiceContext
    )

    # Project commands
    @svc.message_handler(ListProjectsCommand)
    def list_projects(msg: ListProjectsCommand, ctx: StubBackendServiceContext) -> None:
        ListProjectsReply.build(
            ctx.message_builder, msg, projects=ctx.storage_pool.project_storage.list()
        ).emit()

    @svc.message_handler(DeleteProjectCommand)
    def delete_project(
        msg: DeleteProjectCommand, ctx: StubBackendServiceContext
    ) -> None:
        success = False
        message = ""

        if (
            project := ctx.storage_pool.project_storage.get(msg.project_id)
        ) is not None:
            try:
                ctx.storage_pool.project_storage.remove(project)
                success = True
            except Exception as exc:  # pylint: disable=broad-exception-caught
                message = str(exc)
        else:
            message = f"A project with ID {msg.project_id} was not found"

        DeleteProjectReply.build(
            ctx.message_builder,
            msg,
            project_id=project.project_id,
            success=success,
            message=message,
        ).emit()

    # Add some initial data to the in-memory storage
    from .stub_data import fill_stub_data

    fill_stub_data()

    return svc
