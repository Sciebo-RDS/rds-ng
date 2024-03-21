from common.py.component import BackendComponent
from common.py.services import Service


def create_server_backend_service(comp: BackendComponent) -> Service:
    """
    Creates the server backend service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.component import ComponentInformationEvent
    from common.py.api.network import (
        ClientDisconnectedEvent,
        ClientConnectionErrorEvent,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Server backend service", context_type=ServerServiceContext
    )

    @svc.message_handler(ComponentInformationEvent)
    def component_information(
        msg: ComponentInformationEvent, ctx: ServerServiceContext
    ) -> None:
        if ctx.is_entrypoint_client:
            from ..networking import set_server_channel

            set_server_channel(msg.comp_id)

    @svc.message_handler(ClientDisconnectedEvent)
    def client_disconnected(
        msg: ClientDisconnectedEvent, ctx: ServerServiceContext
    ) -> None:
        from ..networking import reset_server_channel

        reset_server_channel()

    @svc.message_handler(ClientConnectionErrorEvent)
    def client_connection_error(
        msg: ClientConnectionErrorEvent, ctx: ServerServiceContext
    ) -> None:
        from ..networking import reset_server_channel

        reset_server_channel()

    return svc
