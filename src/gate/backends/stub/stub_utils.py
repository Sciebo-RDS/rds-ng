from common.py.core.messaging import Message, Channel

from .stub_service_context import StubServiceContext


def send_user_configuration(msg: Message, ctx: StubServiceContext) -> None:
    from common.py.api.user import UserConfigurationEvent

    UserConfigurationEvent.build(
        ctx.message_builder, configuration=ctx.user_configuration, chain=msg
    ).emit(Channel.direct(msg.origin))


def send_projects_list(msg: Message, ctx: StubServiceContext) -> None:
    from common.py.api.project import ProjectsListEvent

    ProjectsListEvent.build(
        ctx.message_builder,
        projects=ctx.storage_pool.project_storage.list(),
        chain=msg,
    ).emit(Channel.direct(msg.origin))
