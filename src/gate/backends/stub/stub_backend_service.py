from common.py.component import BackendComponent
from common.py.core.messaging import Message, Channel
from common.py.services import Service

from .stub_backend_service_context import StubBackendServiceContext


def _send_projects_list(msg: Message, ctx: StubBackendServiceContext) -> None:
    # Automatically send the updated projects list
    from common.py.api.project_events import ProjectsListEvent

    ProjectsListEvent.build(
        ctx.message_builder,
        projects=ctx.storage_pool.project_storage.list(),
        chain=msg,
    ).emit(Channel.direct(msg.origin))


def create_stub_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api import (
        ListProjectsCommand,
        ListProjectsReply,
        DeleteProjectCommand,
        DeleteProjectReply,
    )

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
            project_id=msg.project_id,
            success=success,
            message=message,
        ).emit()

        # Automatically send the updated projects list
        _send_projects_list(msg, ctx)

    # Add some initial data to the in-memory storage
    from .stub_data import fill_stub_data

    fill_stub_data()

    return svc
