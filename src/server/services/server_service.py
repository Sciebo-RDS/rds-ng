from common.py.component import BackendComponent
from common.py.services import Service

from .server_service_context import ServerServiceContext


def create_server_service(comp: BackendComponent) -> Service:
    """
    Creates the main server service that reacts to general (mostly networking-related) messages.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.

    """

    svc = comp.create_service("Server service", context_type=ServerServiceContext)

    return svc
