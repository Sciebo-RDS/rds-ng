from common.py.component import BackendComponent
from common.py.services import Service


def create_stub_connectors_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend connectors service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.connector import ListConnectorsCommand, ListConnectorsReply

    from .stub_service_context import StubServiceContext

    svc = comp.create_service("Connectors service", context_type=StubServiceContext)

    @svc.message_handler(ListConnectorsCommand)
    def list_connectors(msg: ListConnectorsCommand, ctx: StubServiceContext) -> None:
        ListConnectorsReply.build(
            ctx.message_builder,
            msg,
            connectors=ctx.storage_pool.connector_storage.list(),
        ).emit()

    return svc
