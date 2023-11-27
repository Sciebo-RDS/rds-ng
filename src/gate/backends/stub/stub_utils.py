from common.py.core.messaging import Message, Channel

from .stub_backend_service_context import StubBackendServiceContext


def send_projects_list(msg: Message, ctx: StubBackendServiceContext) -> None:
    from common.py.api.project_events import ProjectsListEvent

    ProjectsListEvent.build(
        ctx.message_builder,
        projects=ctx.storage_pool.project_storage.list(),
        chain=msg,
    ).emit(Channel.direct(msg.origin))
