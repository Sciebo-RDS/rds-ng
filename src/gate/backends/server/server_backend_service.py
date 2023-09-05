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
    from .server_backend_service_context import ServerBackendServiceContext

    svc = comp.create_service(
        "Server Backend service", context_type=ServerBackendServiceContext
    )

    return svc
