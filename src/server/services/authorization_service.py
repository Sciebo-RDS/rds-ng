from common.py.component import BackendComponent
from common.py.services import Service


def create_authorization_service(comp: BackendComponent) -> Service:
    """
    Creates the authorization service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.component import ComponentProcessEvent

    from .server_service_context import ServerServiceContext

    svc = comp.create_service(
        "Authorization service", context_type=ServerServiceContext
    )

    @svc.message_handler(ComponentProcessEvent)
    def process_authorization_tokens(
        msg: ComponentProcessEvent, ctx: ServerServiceContext
    ) -> None:
        pass

    return svc
